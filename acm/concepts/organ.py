"""Concept organ — answers: What is this?"""

from __future__ import annotations

from time import time
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from acm.concepts.extract import ConceptCue, extract_cues
from acm.concepts.model import (
    Concept,
    ConceptProposal,
    ConceptStage,
    HierarchyEdge,
    HierarchyKind,
)
from acm.types import Attribute, ConceptRole, new_id
from acm.validation.harness import ConfidenceDelta

if TYPE_CHECKING:
    from acm.associations.organ import AssociationOrgan
    from acm.core.store import CognitiveStore
    from acm.experiences.model import Experience
    from acm.validation.harness import ValidationHarness

_GROWING_EVIDENCE = 2
_STABLE_STRENGTH = 0.65
_STABLE_CONF = 0.6
_STABLE_EVIDENCE = 3
_MATURE_STRENGTH = 0.8
_MATURE_CONF = 0.75
_MATURE_EVIDENCE = 5


class ConceptOrgan:
    """Emergent meaning structures over Experiences."""

    def __init__(self, store: CognitiveStore, validation: ValidationHarness) -> None:
        self.store = store
        self.validation = validation
        self.proposals: dict[str, ConceptProposal] = {}
        self.associations: AssociationOrgan | None = None
        self._births = 0
        self._strengthenings = 0
        self._weakenings = 0
        self._abstractions = 0
        self._stage_changes = 0
        self._inheritances = 0

    @property
    def hierarchy(self) -> dict[str, HierarchyEdge]:
        """Taxonomic edges live on the store so persistence can capture them (D016)."""
        return self.store.hierarchy_edges

    def bind_associations(self, associations: AssociationOrgan) -> None:
        self.associations = associations

    # --- public cognitive surface ----------------------------------------------

    def ingest_from_encode(
        self,
        text: str,
        *,
        encode_kind: str,
        weight: float,
        context_tags: tuple[str, ...] = (),
    ) -> tuple[Concept, list[str]]:
        """Create/reinforce Concepts from text prior to Experience birth."""
        cues = extract_cues(text, encode_kind=encode_kind)
        primary: Concept | None = None
        touched: list[Concept] = []
        for cue in cues:
            concept = self._upsert_from_cue(cue, weight=weight, context_tags=context_tags)
            touched.append(concept)
            if primary is None:
                primary = concept
            elif cue.role in (ConceptRole.PREFERENCE, ConceptRole.IDENTITY):
                primary = concept
            elif cue.is_instance and primary and primary.role != ConceptRole.PREFERENCE:
                primary = concept
        assert primary is not None
        for cue in cues:
            if cue.parent_label:
                child = self._find_by_label(cue.label)
                parent = self._find_by_label(cue.parent_label)
                if child and parent:
                    self.link_is_a(
                        child.id,
                        parent.id,
                        weight=min(1.0, 0.4 + weight * 0.4),
                    )
        self._maybe_propose_merges(touched)
        # unique ids preserve order
        ids: list[str] = []
        for c in touched:
            if c.id not in ids:
                ids.append(c.id)
        return primary, ids

    def bind_experience(self, experience: Experience, concept_ids: list[str] | None = None) -> None:
        """Attach Experience evidence; reinforce listed Concepts (or those on the Experience)."""
        ids = list(concept_ids or experience.concept_ids)
        # Also emerge extra token nuclei already partially handled in ingest
        for cid in ids:
            concept = self.store.concepts.get(cid)
            if concept is None:
                continue
            self._add_evidence(concept, experience.id)
            self._reinforce(concept, weight=experience.importance, reason="experience_bind")
            self._update_prototype(concept, experience.summary)
            self._add_exemplar(concept, experience.id)
            self._recompute_stage(concept)
            # Stamp Experience onto existing hierarchy edges involving this concept.
            self._stamp_hierarchy_evidence(cid, experience.id)

    def what_is_this(self, cue: str) -> dict[str, Any]:
        """Cognitive question M3: What is this?"""
        matches = self.recognize(cue, limit=5)
        if not matches:
            return {
                "question": "What is this?",
                "answer": "I don't have a stable concept for that yet.",
                "seen_before": False,
                "confidence": 0.0,
                "matches": [],
            }
        top = matches[0]
        concept = self.store.concepts[top["concept_id"]]
        parents = [self._label_of(p) for p in concept.parent_ids if p in self.store.concepts]
        children = [self._label_of(c) for c in concept.child_ids if c in self.store.concepts]
        siblings = [s["label"] for s in self.siblings(concept.id)]
        kind_phrase = concept.labels[0]
        if parents:
            answer = f"This appears to be {kind_phrase}, a kind of {parents[0]}."
        else:
            answer = f"This appears to be {kind_phrase}."
        if concept.stage == ConceptStage.NUCLEUS:
            answer += " (emerging nucleus)"
        return {
            "question": "What is this?",
            "answer": answer,
            "seen_before": len(concept.evidence_ids) > 0,
            "confidence": concept.confidence,
            "concept": concept.to_public(),
            "hierarchy": {
                "parents": parents,
                "children": children,
                "siblings": siblings,
            },
            "prototype": concept.prototype.to_public(),
            "exemplars": list(concept.exemplar_ids[-8:]),
            "matches": matches,
            "stage": concept.stage.value,
        }

    def recognize(self, cue: str, *, limit: int = 5) -> list[dict[str, Any]]:
        """Future recognition hook — not Remembering; similarity over Concepts only."""
        q = (cue or "").lower().strip()
        scored: list[tuple[float, Concept]] = []
        for concept in self.store.concepts.values():
            if concept.stage == ConceptStage.RETIRED:
                continue
            if not concept.active and concept.stage != ConceptStage.DORMANT:
                continue
            score = 0.0
            for lab in concept.labels:
                lab_l = lab.lower()
                if q == lab_l:
                    score += 5.0
                elif q in lab_l or lab_l in q:
                    score += 3.0
                else:
                    overlap = set(q.split()) & set(lab_l.split())
                    score += 1.2 * len(overlap)
            for attr in concept.attributes:
                if not attr.active:
                    continue
                if q in attr.value.lower() or q in attr.key:
                    score += 2.0 * attr.confidence
            for feat, val in concept.prototype.features.items():
                if q in feat or q in val.lower():
                    score += 1.5 * concept.prototype.feature_weights.get(feat, 0.5)
            # Prefer mature meanings
            stage_bonus = {
                ConceptStage.NUCLEUS: 0.2,
                ConceptStage.GROWING: 0.5,
                ConceptStage.STABLE: 1.0,
                ConceptStage.MATURE: 1.3,
                ConceptStage.DORMANT: 0.1,
                ConceptStage.RETIRED: 0.0,
            }[concept.stage]
            score *= 0.5 + 0.5 * concept.confidence
            score *= 0.5 + 0.5 * concept.strength
            score += stage_bonus
            if score > 0.5:
                scored.append((score, concept))
        scored.sort(key=lambda x: x[0], reverse=True)
        out: list[dict[str, Any]] = []
        for score, concept in scored[:limit]:
            out.append(
                {
                    "concept_id": concept.id,
                    "label": concept.labels[0],
                    "score": round(score, 3),
                    "stage": concept.stage.value,
                    "confidence": concept.confidence,
                    "seen_before": len(concept.evidence_ids) > 0,
                }
            )
        return out

    def link_is_a(
        self,
        child_id: str,
        parent_id: str,
        *,
        weight: float = 0.5,
        evidence_ids: tuple[str, ...] | list[str] = (),
        kind: HierarchyKind = HierarchyKind.IS_A,
    ) -> HierarchyEdge | None:
        """Create or reinforce an evidence-based taxonomic edge. Never invents Experiences."""
        if child_id == parent_id:
            return None
        child = self.store.concepts.get(child_id)
        parent = self.store.concepts.get(parent_id)
        if not child or not parent:
            return None
        if self._would_create_cycle(child_id, parent_id):
            return None
        evidence = tuple(eid for eid in evidence_ids if eid)
        now = time()
        for edge in list(self.hierarchy.values()):
            if edge.child_id == child_id and edge.parent_id == parent_id:
                merged = tuple(dict.fromkeys([*edge.evidence_ids, *evidence]))
                reinforced = HierarchyEdge(
                    id=edge.id,
                    child_id=edge.child_id,
                    parent_id=edge.parent_id,
                    kind=edge.kind if edge.kind != HierarchyKind.IS_A else kind,
                    weight=min(1.0, edge.weight + 0.08 * max(weight, 0.2)),
                    evidence_ids=merged,
                    created=edge.created or now,
                    last_reinforced=now,
                )
                self.hierarchy[edge.id] = reinforced
                if self.associations is not None:
                    evid = evidence[0] if evidence else ""
                    self.associations.absorb_hierarchy_edge(
                        child_id, parent_id, weight=reinforced.weight, evidence_id=evid
                    )
                    self.associations.absorb_siblings(parent_id, evidence_id=evid)
                return reinforced
        edge = HierarchyEdge(
            id=new_id("hier"),
            child_id=child_id,
            parent_id=parent_id,
            kind=kind,
            weight=weight,
            evidence_ids=evidence,
            created=now,
            last_reinforced=now,
        )
        self.hierarchy[edge.id] = edge
        if parent_id not in child.parent_ids:
            child.parent_ids.append(parent_id)
        if child_id not in parent.child_ids:
            parent.child_ids.append(child_id)
        if child_id not in parent.instance_ids and child.metadata.get("is_instance"):
            parent.instance_ids.append(child_id)
        self._abstractions += 1
        self.validation.record_concept(
            action="abstraction",
            child_id=child_id,
            parent_id=parent_id,
            hierarchy=1,
            abstraction=1,
            evidence_count=len(evidence),
        )
        # Parent gains gentle abstraction reinforcement
        self._reinforce(parent, weight=weight * 0.4, reason="abstraction_parent")
        if self.associations is not None:
            evid = evidence[0] if evidence else ""
            self.associations.absorb_hierarchy_edge(
                child_id, parent_id, weight=weight, evidence_id=evid
            )
            self.associations.absorb_siblings(parent_id, evidence_id=evid)
        return edge

    def parents(self, concept_id: str) -> list[dict[str, Any]]:
        concept = self.store.concepts.get(concept_id)
        if concept is None:
            return []
        out: list[dict[str, Any]] = []
        for pid in concept.parent_ids:
            parent = self.store.concepts.get(pid)
            if parent is None:
                continue
            edge = self._edge_between(concept_id, pid)
            out.append(
                {
                    "concept_id": pid,
                    "label": parent.labels[0] if parent.labels else pid,
                    "weight": edge.weight if edge else 0.0,
                    "evidence_ids": list(edge.evidence_ids) if edge else [],
                    "kind": edge.kind.value if edge else HierarchyKind.IS_A.value,
                }
            )
        return out

    def children(self, concept_id: str) -> list[dict[str, Any]]:
        concept = self.store.concepts.get(concept_id)
        if concept is None:
            return []
        out: list[dict[str, Any]] = []
        for cid in concept.child_ids:
            child = self.store.concepts.get(cid)
            if child is None:
                continue
            edge = self._edge_between(cid, concept_id)
            out.append(
                {
                    "concept_id": cid,
                    "label": child.labels[0] if child.labels else cid,
                    "weight": edge.weight if edge else 0.0,
                    "evidence_ids": list(edge.evidence_ids) if edge else [],
                    "kind": edge.kind.value if edge else HierarchyKind.IS_A.value,
                }
            )
        return out

    def siblings(self, concept_id: str) -> list[dict[str, Any]]:
        concept = self.store.concepts.get(concept_id)
        if concept is None:
            return []
        seen: set[str] = set()
        out: list[dict[str, Any]] = []
        for pid in concept.parent_ids:
            parent = self.store.concepts.get(pid)
            if parent is None:
                continue
            for cid in parent.child_ids:
                if cid == concept_id or cid in seen:
                    continue
                sib = self.store.concepts.get(cid)
                if sib is None:
                    continue
                seen.add(cid)
                out.append(
                    {
                        "concept_id": cid,
                        "label": sib.labels[0] if sib.labels else cid,
                        "shared_parent_id": pid,
                        "shared_parent": parent.labels[0] if parent.labels else pid,
                    }
                )
        return out

    def explain_hierarchy(self, cue_or_id: str) -> dict[str, Any]:
        """Explain taxonomic placement: parents, children, siblings, supporting evidence."""
        concept = self.store.concepts.get(cue_or_id)
        if concept is None:
            matches = self.recognize(cue_or_id, limit=1)
            if not matches:
                return {
                    "question": "How is this concept organized?",
                    "answer": "I don't have a stable concept hierarchy for that yet.",
                    "known": False,
                }
            concept = self.store.concepts[matches[0]["concept_id"]]
        parents = self.parents(concept.id)
        children = self.children(concept.id)
        siblings = self.siblings(concept.id)
        edges = [
            e.to_public()
            for e in self.hierarchy.values()
            if e.child_id == concept.id or e.parent_id == concept.id
        ]
        evidence: list[str] = []
        for e in edges:
            evidence.extend(e.get("evidence_ids") or [])
        evidence = list(dict.fromkeys(evidence))
        label = concept.labels[0] if concept.labels else concept.id
        if parents:
            answer = (
                f"{label} specializes under {parents[0]['label']} "
                f"({len(evidence)} supporting experience(s))."
            )
        elif children:
            answer = (
                f"{label} generalizes {len(children)} child concept(s) "
                f"({len(evidence)} supporting experience(s))."
            )
        else:
            answer = f"{label} has no taxonomic links yet."
        return {
            "question": "How is this concept organized?",
            "answer": answer,
            "known": True,
            "concept_id": concept.id,
            "label": label,
            "parents": parents,
            "children": children,
            "siblings": siblings,
            "edges": edges,
            "evidence_ids": evidence,
            "reversible": True,
            "can_reverse": "Hierarchy edges can be weakened; Experiences are never rewritten.",
        }

    def inherit_attributes(
        self,
        child_id: str,
        parent_id: str,
        *,
        evidence_ids: tuple[str, ...] | list[str] = (),
        keys: tuple[str, ...] | list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Copy active parent attributes onto child — values already evidenced on parent only.

        Never invents attribute values. Inherited attrs are marked and carry evidence lineage.
        """
        child = self.store.concepts.get(child_id)
        parent = self.store.concepts.get(parent_id)
        if not child or not parent:
            return []
        if parent_id not in child.parent_ids and not self.link_is_a(
            child_id, parent_id, evidence_ids=evidence_ids, kind=HierarchyKind.SPECIALIZES
        ):
            # Still allow inherit if already linked or just linked; if cycle blocked, abort.
            if parent_id not in child.parent_ids:
                return []
        allowed = {k.lower() for k in keys} if keys else None
        evidence = tuple(eid for eid in evidence_ids if eid)
        inherited: list[dict[str, Any]] = []
        for attr in parent.attributes:
            if not attr.active:
                continue
            if allowed is not None and attr.key.lower() not in allowed:
                continue
            # Skip if child already has an active same-key attribute (specialization wins).
            if any(a.key == attr.key and a.active for a in child.attributes):
                continue
            child.attributes.append(
                Attribute(
                    key=attr.key,
                    value=attr.value,
                    confidence=min(0.7, attr.confidence * 0.85),
                    importance=attr.importance * 0.8,
                    context_tags=tuple(
                        dict.fromkeys([*attr.context_tags, f"inherited_from:{parent_id}"])
                    ),
                    evidence_ids=list(
                        dict.fromkeys([*attr.evidence_ids, *parent.evidence_ids[-4:], *evidence])
                    ),
                    active=True,
                    version=1,
                )
            )
            inherited.append({"key": attr.key, "value": attr.value, "from_parent": parent_id})
            self._inheritances += 1
        if inherited:
            self.validation.record_concept(
                action="inherit",
                child_id=child_id,
                parent_id=parent_id,
                inherited=len(inherited),
                hierarchy=1,
            )
            prop = ConceptProposal(
                id=new_id("cprop"),
                kind="inherit",
                concept_ids=(child_id, parent_id),
                reason=f"Inherited {len(inherited)} attribute(s) from parent (evidence-gated).",
                status="accepted",
                evidence_ids=evidence,
                metadata={"inherited": inherited},
            )
            self.proposals[prop.id] = prop
        return inherited

    def specialize(
        self,
        child_id: str,
        parent_id: str,
        *,
        evidence_ids: tuple[str, ...] | list[str] = (),
    ) -> HierarchyEdge | None:
        """Evidence-based specialization: child is_a / specializes parent."""
        return self.link_is_a(
            child_id,
            parent_id,
            weight=0.55,
            evidence_ids=evidence_ids,
            kind=HierarchyKind.SPECIALIZES,
        )

    def generalize_children(
        self,
        parent_id: str,
        child_ids: list[str],
        *,
        evidence_ids: tuple[str, ...] | list[str] = (),
    ) -> list[HierarchyEdge]:
        """Link multiple evidenced children under an existing parent (generalization)."""
        out: list[HierarchyEdge] = []
        for cid in child_ids:
            edge = self.link_is_a(
                cid,
                parent_id,
                weight=0.5,
                evidence_ids=evidence_ids,
                kind=HierarchyKind.IS_A,
            )
            if edge:
                out.append(edge)
        if out:
            prop = ConceptProposal(
                id=new_id("cprop"),
                kind="generalize",
                concept_ids=(parent_id, *child_ids[:8]),
                reason="Generalized children under shared parent from evidence.",
                status="accepted",
                evidence_ids=tuple(evidence_ids),
            )
            self.proposals[prop.id] = prop
        return out

    def propose_hierarchy_from_clusters(
        self, *, min_cluster: int = 2, max_proposals: int = 8
    ) -> list[ConceptProposal]:
        """Observational clustering → hierarchy *proposals* only (never invent Concepts).

        Uses Association clusters among Concepts that already share evidence mass.
        Requires an existing candidate parent Concept (by shared label fragment) —
        does not mint new category labels.
        """
        if self.associations is None:
            return []
        clusters = self.associations.clusters(min_strength=0.35)
        created: list[ConceptProposal] = []
        for cluster in clusters:
            if len(created) >= max_proposals:
                break
            ids = [c for c in (cluster.get("concept_ids") or []) if c]
            if len(ids) < min_cluster:
                continue
            # Prefer an existing parent already linked to ≥2 members; else skip (no invention).
            parent_votes: dict[str, int] = {}
            for cid in ids:
                concept = self.store.concepts.get(cid)
                if not concept:
                    continue
                for pid in concept.parent_ids:
                    parent_votes[pid] = parent_votes.get(pid, 0) + 1
            if not parent_votes:
                continue
            parent_id = max(parent_votes, key=parent_votes.get)
            if parent_votes[parent_id] < 1:
                continue
            orphans = [
                cid
                for cid in ids
                if cid != parent_id
                and parent_id not in (self.store.concepts.get(cid).parent_ids if self.store.concepts.get(cid) else [])
            ]
            if not orphans:
                continue
            evidence: list[str] = []
            for cid in orphans[:6]:
                c = self.store.concepts.get(cid)
                if c:
                    evidence.extend(c.evidence_ids[-2:])
            prop = ConceptProposal(
                id=new_id("cprop"),
                kind="hierarchy_link",
                concept_ids=(parent_id, *orphans[:6]),
                reason="Cluster shares structure; propose linking orphans under existing parent.",
                status="pending",
                evidence_ids=tuple(dict.fromkeys(evidence)),
                metadata={"parent_id": parent_id, "child_ids": orphans[:6]},
            )
            self.proposals[prop.id] = prop
            created.append(prop)
        return created

    def accept_hierarchy_proposal(self, proposal_id: str) -> HierarchyEdge | list[HierarchyEdge] | None:
        """Apply a pending hierarchy_link / generalize proposal via ConceptOrgan only."""
        prop = self.proposals.get(proposal_id)
        if prop is None or prop.status != "pending":
            return None
        parent_id = str((prop.metadata or {}).get("parent_id") or "")
        child_ids = list((prop.metadata or {}).get("child_ids") or [])
        if not parent_id and len(prop.concept_ids) >= 2:
            parent_id = prop.concept_ids[0]
            child_ids = list(prop.concept_ids[1:])
        if not parent_id or not child_ids:
            prop.status = "rejected"
            return None
        edges = self.generalize_children(
            parent_id, child_ids, evidence_ids=prop.evidence_ids
        )
        prop.status = "accepted"
        return edges

    def rebuild_hierarchy_index(self) -> int:
        """Rebuild edge index from parent_ids/child_ids when edges were not persisted."""
        rebuilt = 0
        if self.hierarchy:
            # Sync denormalized lists from edges.
            for edge in self.hierarchy.values():
                child = self.store.concepts.get(edge.child_id)
                parent = self.store.concepts.get(edge.parent_id)
                if not child or not parent:
                    continue
                if edge.parent_id not in child.parent_ids:
                    child.parent_ids.append(edge.parent_id)
                if edge.child_id not in parent.child_ids:
                    parent.child_ids.append(edge.child_id)
            return len(self.hierarchy)
        for concept in self.store.concepts.values():
            for pid in list(concept.parent_ids):
                if pid not in self.store.concepts:
                    continue
                if self._edge_between(concept.id, pid):
                    continue
                edge = HierarchyEdge(
                    id=new_id("hier"),
                    child_id=concept.id,
                    parent_id=pid,
                    kind=HierarchyKind.IS_A,
                    weight=0.45,
                    evidence_ids=tuple(concept.evidence_ids[-3:]),
                    created=concept.first_seen,
                    last_reinforced=concept.last_activated,
                )
                self.hierarchy[edge.id] = edge
                rebuilt += 1
        return rebuilt

    def weaken(self, concept_id: str, *, amount: float = 0.05) -> Concept | None:
        concept = self.store.concepts.get(concept_id)
        if concept is None:
            return None
        before = concept.strength
        concept.strength = max(0.0, concept.strength - amount)
        concept.confidence = max(0.05, concept.confidence - amount * 0.5)
        self._weakenings += 1
        self.validation.record_concept(
            action="weaken",
            concept_id=concept.id,
            strength_before=before,
            strength_after=concept.strength,
            weakening=1,
        )
        self._recompute_stage(concept)
        return concept

    def resurrect(self, concept_id: str) -> Concept | None:
        concept = self.store.concepts.get(concept_id)
        if concept is None:
            return None
        if concept.stage in (ConceptStage.DORMANT, ConceptStage.RETIRED):
            concept.active = True
            concept.stage = ConceptStage.GROWING if concept.evidence_ids else ConceptStage.NUCLEUS
            concept.provisional = concept.stage == ConceptStage.NUCLEUS
            self._stage_changes += 1
            self.validation.record_concept(
                action="resurrect",
                concept_id=concept.id,
                stage=concept.stage.value,
                lifecycle=1,
            )
        return concept

    def pending_proposals(self) -> list[dict[str, Any]]:
        return [
            {
                "id": p.id,
                "kind": p.kind,
                "concept_ids": list(p.concept_ids),
                "reason": p.reason,
                "status": p.status,
                "evidence_ids": list(p.evidence_ids),
            }
            for p in self.proposals.values()
            if p.status == "pending"
        ]

    def observables(self) -> dict[str, Any]:
        by_stage: dict[str, int] = {}
        for c in self.store.concepts.values():
            by_stage[c.stage.value] = by_stage.get(c.stage.value, 0) + 1
        return {
            "concept_count": len(self.store.concepts),
            "hierarchy_edges": len(self.hierarchy),
            "nuclei": by_stage.get(ConceptStage.NUCLEUS.value, 0),
            "mature": by_stage.get(ConceptStage.MATURE.value, 0),
            "births": self._births,
            "strengthenings": self._strengthenings,
            "weakenings": self._weakenings,
            "abstractions": self._abstractions,
            "stage_changes": self._stage_changes,
            "inheritances": self._inheritances,
            "by_stage": by_stage,
            "pending_proposals": len(self.pending_proposals()),
        }

    def register_existing(self, concept: Concept) -> None:
        """Track Concepts created outside ingest (e.g. Identity schema anchors)."""
        if not concept.evidence_ids and concept.stage == ConceptStage.NUCLEUS:
            pass
        self.validation.record_concept(
            action="register",
            concept_id=concept.id,
            stage=concept.stage.value,
            label=concept.labels[0] if concept.labels else "",
        )

    # --- internals --------------------------------------------------------------

    def _edge_between(self, child_id: str, parent_id: str) -> HierarchyEdge | None:
        for edge in self.hierarchy.values():
            if edge.child_id == child_id and edge.parent_id == parent_id:
                return edge
        return None

    def _would_create_cycle(self, child_id: str, parent_id: str) -> bool:
        """True if making parent_id a parent of child_id would cycle."""
        stack = [parent_id]
        seen: set[str] = set()
        while stack:
            cur = stack.pop()
            if cur == child_id:
                return True
            if cur in seen:
                continue
            seen.add(cur)
            concept = self.store.concepts.get(cur)
            if concept is None:
                continue
            stack.extend(concept.parent_ids)
        return False

    def _stamp_hierarchy_evidence(self, concept_id: str, experience_id: str) -> None:
        if not experience_id:
            return
        now = time()
        for edge in list(self.hierarchy.values()):
            if edge.child_id != concept_id and edge.parent_id != concept_id:
                continue
            if experience_id in edge.evidence_ids:
                continue
            self.hierarchy[edge.id] = HierarchyEdge(
                id=edge.id,
                child_id=edge.child_id,
                parent_id=edge.parent_id,
                kind=edge.kind,
                weight=edge.weight,
                evidence_ids=tuple([*edge.evidence_ids, experience_id]),
                created=edge.created or now,
                last_reinforced=now,
            )

    def _upsert_from_cue(
        self,
        cue: ConceptCue,
        *,
        weight: float,
        context_tags: tuple[str, ...],
    ) -> Concept:
        existing = self._find_by_label(cue.label)
        # Preference keys are globally unique identity keys for upsert
        if existing is None and (
            cue.attr_key.startswith("favorite_")
            or cue.attr_key.startswith("prefer_")
            or cue.attr_key == "preference"
        ):
            for c in self.store.concepts.values():
                if any(a.key == cue.attr_key and a.active for a in c.attributes):
                    existing = c
                    break

        if existing is None:
            concept = self.store.add_concept(
                cue.label,
                role=cue.role,
                identity=cue.identity,
                provisional=True,
                importance=max(0.35, weight * 0.9),
                confidence=min(0.7, 0.35 + weight * 0.35),
                strength=min(0.55, 0.25 + weight * 0.35),
                stage=ConceptStage.NUCLEUS,
            )
            concept.metadata["is_instance"] = cue.is_instance
            concept.attributes.append(
                Attribute(
                    key=cue.attr_key,
                    value=cue.attr_value,
                    confidence=min(0.85, 0.4 + weight * 0.4),
                    importance=weight,
                    context_tags=context_tags,
                )
            )
            self._births += 1
            self.validation.record_concept(
                action="birth",
                concept_id=concept.id,
                stage=concept.stage.value,
                label=cue.label,
                nucleus=1,
                birth=1,
            )
            return concept

        # Privileged identity schemas must not absorb token-nucleus noise
        # (e.g. cue label "user" from "User name is Jeff" → mentioned=user).
        if (
            existing.identity
            and existing.metadata.get("schema")
            and not cue.identity
            and cue.attr_key in ("mentioned", "statement", "category")
        ):
            return existing

        # Reinforce + attribute update
        self._apply_attribute(existing, cue, weight=weight, context_tags=context_tags)
        self._reinforce(existing, weight=weight * 0.8, reason="cue_match")
        if cue.is_instance:
            existing.metadata["is_instance"] = True
        self._recompute_stage(existing)
        return existing

    def _apply_attribute(
        self,
        concept: Concept,
        cue: ConceptCue,
        *,
        weight: float,
        context_tags: tuple[str, ...],
    ) -> None:
        for attr in concept.attributes:
            if attr.key == cue.attr_key and attr.active:
                if attr.value.lower() != cue.attr_value.lower():
                    attr.active = False
                    concept.attributes.append(
                        Attribute(
                            key=cue.attr_key,
                            value=cue.attr_value,
                            confidence=min(0.95, attr.confidence + 0.08),
                            importance=weight,
                            context_tags=context_tags,
                            version=attr.version + 1,
                        )
                    )
                    self.validation.record_reconsolidation(
                        concept_id=concept.id,
                        attribute_key=cue.attr_key,
                        kind="supersede",
                        previous=attr.value,
                        current=cue.attr_value,
                    )
                    concept.confidence = max(0.2, concept.confidence - 0.05)
                else:
                    before = attr.confidence
                    attr.confidence = min(1.0, attr.confidence + 0.05)
                    self.validation.record_confidence(
                        ConfidenceDelta(
                            time(),
                            concept.id,
                            cue.attr_key,
                            before,
                            attr.confidence,
                            "concept_reinforce",
                        )
                    )
                return
        concept.attributes.append(
            Attribute(
                key=cue.attr_key,
                value=cue.attr_value,
                confidence=min(0.85, 0.4 + weight * 0.4),
                importance=weight,
                context_tags=context_tags,
            )
        )

    def _reinforce(self, concept: Concept, *, weight: float, reason: str) -> None:
        before_s = concept.strength
        before_c = concept.confidence
        concept.strength = min(1.0, concept.strength + 0.07 * weight)
        concept.confidence = min(1.0, concept.confidence + 0.05 * weight)
        concept.importance = max(concept.importance, weight * 0.9)
        concept.access_count += 1
        concept.last_activated = time()
        concept.active = True
        if concept.stage == ConceptStage.DORMANT:
            self.resurrect(concept.id)
        self._strengthenings += 1
        self.validation.record_concept(
            action="strengthen",
            concept_id=concept.id,
            reason=reason,
            strength_before=before_s,
            strength_after=concept.strength,
            confidence_before=before_c,
            confidence_after=concept.confidence,
            strengthening=1,
        )
        self.validation.record_confidence(
            ConfidenceDelta(
                time(),
                concept.id,
                "concept",
                before_c,
                concept.confidence,
                reason,
            )
        )
        self._recompute_stage(concept)

    def _add_evidence(self, concept: Concept, experience_id: str) -> None:
        if experience_id and experience_id not in concept.evidence_ids:
            concept.evidence_ids.append(experience_id)

    def _add_exemplar(self, concept: Concept, experience_id: str) -> None:
        if not experience_id:
            return
        if experience_id in concept.exemplar_ids:
            return
        concept.exemplar_ids.append(experience_id)
        if len(concept.exemplar_ids) > 24:
            del concept.exemplar_ids[:-24]

    def _update_prototype(self, concept: Concept, summary: str) -> None:
        # Lightweight: fold active attributes into prototype features
        for attr in concept.attributes:
            if not attr.active:
                continue
            key = attr.key
            prev_w = concept.prototype.feature_weights.get(key, 0.0)
            new_w = prev_w + attr.confidence
            # Keep value with higher cumulative weight
            if key not in concept.prototype.features or new_w >= prev_w:
                concept.prototype.features[key] = attr.value
            concept.prototype.feature_weights[key] = min(10.0, new_w)
        # Mention token as a soft feature
        token = summary.strip().split()[:3]
        if token:
            feat = "surface"
            concept.prototype.features.setdefault(feat, " ".join(token).lower())
            concept.prototype.feature_weights[feat] = min(
                5.0, concept.prototype.feature_weights.get(feat, 0.0) + 0.2
            )
        self.validation.record_concept(
            action="prototype_update",
            concept_id=concept.id,
            prototype=1,
        )

    def _recompute_stage(self, concept: Concept) -> None:
        if concept.stage == ConceptStage.RETIRED:
            return
        old = concept.stage
        n = len(concept.evidence_ids)
        if concept.strength < 0.15 and n <= 1 and not concept.identity:
            concept.stage = ConceptStage.DORMANT
            concept.active = False
            concept.provisional = True
        elif (
            concept.strength >= _MATURE_STRENGTH
            and concept.confidence >= _MATURE_CONF
            and n >= _MATURE_EVIDENCE
        ):
            concept.stage = ConceptStage.MATURE
            concept.provisional = False
            concept.active = True
        elif (
            concept.strength >= _STABLE_STRENGTH
            and concept.confidence >= _STABLE_CONF
            and n >= _STABLE_EVIDENCE
        ):
            concept.stage = ConceptStage.STABLE
            concept.provisional = False
            concept.active = True
        elif n >= _GROWING_EVIDENCE or concept.strength >= 0.45:
            concept.stage = ConceptStage.GROWING
            concept.provisional = concept.strength < 0.6
            concept.active = True
        else:
            concept.stage = ConceptStage.NUCLEUS
            concept.provisional = True
            concept.active = True
        if concept.stage != old:
            self._stage_changes += 1
            self.validation.record_concept(
                action="stage_change",
                concept_id=concept.id,
                stage_before=old.value,
                stage=concept.stage.value,
                maturity=1,
                lifecycle=1,
            )

    def _find_by_label(self, label: str) -> Concept | None:
        q = label.lower().strip()
        exact: Concept | None = None
        for c in self.store.concepts.values():
            if c.stage == ConceptStage.RETIRED:
                continue
            if any(lab.lower() == q for lab in c.labels):
                exact = c
                break
        if exact is not None:
            return exact
        # Conservative near-match: equal after stripping plural 's', not substring contain
        stem = q[:-1] if q.endswith("s") and len(q) > 4 else q
        for c in self.store.concepts.values():
            if c.stage == ConceptStage.RETIRED:
                continue
            for lab in c.labels:
                lab_l = lab.lower()
                lab_stem = lab_l[:-1] if lab_l.endswith("s") and len(lab_l) > 4 else lab_l
                if lab_stem == stem:
                    return c
        return None

    def _label_of(self, concept_id: str) -> str:
        c = self.store.concepts.get(concept_id)
        return c.labels[0] if c and c.labels else concept_id

    def _maybe_propose_merges(self, concepts: list[Concept]) -> None:
        labels: dict[str, list[Concept]] = {}
        for c in concepts:
            key = c.labels[0].lower()
            labels.setdefault(key, []).append(c)
        # Cross-scan store for near-duplicate labels
        for c in list(self.store.concepts.values()):
            if c.stage in (ConceptStage.RETIRED, ConceptStage.DORMANT):
                continue
            for other in concepts:
                if other.id == c.id:
                    continue
                a, b = c.labels[0].lower(), other.labels[0].lower()
                if a == b or a in b or b in a:
                    if abs(len(a) - len(b)) <= 2 or a == b:
                        self._propose(
                            "merge",
                            (c.id, other.id),
                            reason=f"similar_labels:{a}|{b}",
                        )

    def _propose(self, kind: str, concept_ids: tuple[str, ...], *, reason: str) -> None:
        # Dedup pending
        key = (kind, tuple(sorted(concept_ids)))
        for p in self.proposals.values():
            if p.status == "pending" and p.kind == kind and tuple(sorted(p.concept_ids)) == key[1]:
                return
        prop = ConceptProposal(
            id=f"cprop_{uuid4().hex[:10]}",
            kind=kind,
            concept_ids=tuple(sorted(concept_ids)),
            reason=reason,
        )
        self.proposals[prop.id] = prop
        self.validation.record_concept(
            action="proposal",
            proposal_id=prop.id,
            kind=kind,
            concept_ids=list(prop.concept_ids),
            merge=1 if kind == "merge" else 0,
            split=1 if kind == "split" else 0,
        )
