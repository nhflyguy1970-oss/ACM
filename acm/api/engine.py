"""Public ACM engine API — plug-and-play for any agent host."""

from __future__ import annotations

import re
from dataclasses import dataclass
from time import perf_counter, time
from typing import Any

from acm._version import __version__ as acm_version
from acm.attention.field import classify_attention, encode_weight
from acm.context.frame import ContextFrame, infer_context
from acm.core.store import CognitiveStore, Concept
from acm.identity import IdentityOrgan
from acm.observability.trace import CognitiveTraceEvent, TraceLog
from acm.plugins import ExtensionRegistry
from acm.types import (
    AttentionClass,
    Attribute,
    ConceptRole,
    EdgeType,
    ExplanationClass,
    MemoryVerb,
)
from acm.validation.harness import (
    ActivationRecord,
    AssociationChange,
    ConfidenceDelta,
    LifecycleEvent,
    ValidationHarness,
    WorkingTransition,
)
from acm.working.buffer import BufferItem, WorkingBuffer


@dataclass
class RememberResult:
    answer: str
    explanation: str
    explanation_class: ExplanationClass
    activated_concept_ids: list[str]
    confidence: float
    trace: dict[str, Any]


class CognitiveEngine:
    """Host-agnostic cognitive memory engine.

    Adapters for Aria / FlyTying / robotics belong *outside* this package.
    """

    def __init__(
        self,
        *,
        agent_id: str = "agent",
        buffer_capacity: int = 7,
    ) -> None:
        self.agent_id = agent_id
        self.store = CognitiveStore()
        self.buffer = WorkingBuffer(capacity=buffer_capacity)
        self.context = ContextFrame()
        self.validation = ValidationHarness()
        self.trace = TraceLog()
        self.identity = IdentityOrgan(
            agent_id=agent_id, store=self.store, validation=self.validation
        )
        self.extensions = ExtensionRegistry(core_version=acm_version)
        self.extensions.bind_engine(self)
        # Metacognitive sketches — emerge from state; not scripted “consciousness”
        self._encode_count = 0
        self._remember_count = 0
        # Nuclei exist as organizational anchors; content still arrives via experience
        self.identity.ensure_schemas()

    # --- public cognitive verbs -------------------------------------------------

    def set_context(self, *tags: str, activity: str = "", place: str = "") -> ContextFrame:
        self.context = ContextFrame(tags=tuple(tags), activity=activity, place=place)
        return self.context

    def open_goal(self, title: str, *, importance: float = 0.6) -> str:
        goal = self.store.add_goal(title, importance=importance)
        displaced = self.buffer.push(
            BufferItem(
                kind="goal",
                ref_id=goal.id,
                label=title,
                attention=0.8,
                importance=importance,
            )
        )
        self._note_displace(displaced)
        self.validation.record_lifecycle(
            LifecycleEvent(time(), MemoryVerb.ENCODE.value, goal.id, f"goal_open:{title}")
        )
        # Goals bias identity reconstruction (active pursuits are part of “who”)
        agent = self.identity.schema_concept("agent")
        self.store.add_association(
            agent.id, goal.id, edge_type=EdgeType.RELATED_TO, weight=0.45 + 0.2 * importance
        )
        self.validation.record_identity(
            action="goal_bind",
            schema_id=agent.id,
            goal_id=goal.id,
            influence=1,
        )
        return goal.id

    def complete_goal(self, goal_id: str) -> None:
        goal = self.store.goals.get(goal_id)
        if not goal:
            return
        goal.status = "completed"
        goal.completed = time()
        self.validation.record_lifecycle(
            LifecycleEvent(time(), "goal_complete", goal_id, goal.title)
        )

    def encode(
        self,
        text: str,
        *,
        kind: str = "experience",
        pin: bool = False,
        context_tags: tuple[str, ...] | None = None,
        assent: bool = False,
        proposal_id: str | None = None,
    ) -> dict[str, Any]:
        t0 = perf_counter()
        self.context = infer_context(text, self.context)
        if context_tags:
            tags = tuple(dict.fromkeys(list(self.context.tags) + list(context_tags)))
            self.context = ContextFrame(
                tags=tags, activity=self.context.activity, place=self.context.place
            )

        has_goal = bool(self.store.active_goals())
        attention = classify_attention(text, has_open_goal=has_goal)
        if pin:
            attention = AttentionClass.USER_PIN
        elif kind == "preference" and attention == AttentionClass.DEFAULT:
            attention = AttentionClass.NOVELTY
        elif kind == "identity" and attention == AttentionClass.DEFAULT:
            attention = AttentionClass.STAKES
        elif self.identity.classify_identity_signal(text, kind=kind) in ("agent", "user"):
            if attention == AttentionClass.DEFAULT:
                attention = AttentionClass.STAKES
        weight = min(1.0, encode_weight(attention) + self.identity.attention_boost(text, kind=kind))

        # Low default attention may still encode lightly — pin/preference/identity durable
        durable = weight >= 0.5 or kind in ("preference", "identity")
        if not durable:
            self.validation.record_lifecycle(
                LifecycleEvent(time(), MemoryVerb.ENCODE.value, "", "skipped_low_attention")
            )
            return {"encoded": False, "reason": "low_attention", "attention": attention.value}

        exp = self.store.add_experience(
            text.strip(),
            context_tags=self.context.tags,
            goal_ids=[g.id for g in self.store.active_goals()],
            attention_class=attention.value,
            importance=weight,
        )

        concept = self._upsert_concept_from_text(text, kind=kind, weight=weight)
        self.identity.mark_concept_formation(concept, text=text, kind=kind)
        # Bind concept evidence without degenerate self-edges.
        if concept.id not in (exp.metadata.get("concept_ids") or []):
            exp.metadata.setdefault("concept_ids", []).append(concept.id)
        for attr in concept.attributes:
            if exp.id not in attr.evidence_ids:
                attr.evidence_ids.append(exp.id)

        identity_result = self.identity.integrate_encode(
            text=text,
            kind=kind,
            concept=concept,
            experience_id=exp.id,
            weight=weight,
            assent=assent,
            proposal_id=proposal_id,
        )

        displaced = self.buffer.push(
            BufferItem(
                kind="concept",
                ref_id=concept.id,
                label=concept.labels[0],
                attention=weight,
                importance=concept.importance,
            )
        )
        self._note_displace(displaced)
        self.validation.record_working(
            WorkingTransition(time(), "enter", concept.id, concept.labels[0])
        )
        self.validation.record_lifecycle(
            LifecycleEvent(time(), MemoryVerb.ENCODE.value, concept.id, kind)
        )

        # Goal bias: associate concept with active goals
        for goal in self.store.active_goals():
            g_edge = self.store.add_association(
                concept.id, goal.id, edge_type=EdgeType.RELATED_TO, weight=0.4 + 0.2 * weight
            )
            self.validation.record_association(
                AssociationChange(
                    time(),
                    g_edge.id,
                    "added",
                    concept.id,
                    goal.id,
                    g_edge.edge_type.value,
                    g_edge.weight,
                )
            )

        latency = (perf_counter() - t0) * 1000
        self.trace.append(
            CognitiveTraceEvent(
                verb=MemoryVerb.ENCODE.value,
                attention_class=attention.value,
                context_tags=list(self.context.tags),
                goal_ids=[g.id for g in self.store.active_goals()],
                activated_concept_ids=[concept.id],
                explanation_class=ExplanationClass.EXPERIENCE.value,
                latency_ms=latency,
                metadata={"identity": identity_result},
            )
        )
        self._encode_count += 1
        payload = {
            "encoded": True,
            "experience_id": exp.id,
            "concept_id": concept.id,
            "attention": attention.value,
            "importance": weight,
            "identity": identity_result,
        }
        self.extensions.emit("after_encode", dict(payload))
        return payload

    def remember(self, query: str) -> RememberResult:
        t0 = perf_counter()
        self.context = infer_context(query, self.context)
        has_goal = bool(self.store.active_goals())
        attention = classify_attention(query, has_open_goal=has_goal)

        if self.identity.is_who_query(query):
            who = self.identity.who_am_i()
            latency = (perf_counter() - t0) * 1000
            activated = [c["concept_id"] for c in who.get("central_concepts", [])]
            event = CognitiveTraceEvent(
                verb=MemoryVerb.REMEMBER.value,
                attention_class=attention.value,
                context_tags=list(self.context.tags),
                goal_ids=[g.id for g in self.store.active_goals()],
                activated_concept_ids=activated,
                explanation_class=ExplanationClass.EXPERIENCE.value,
                reconsolidation="light",
                latency_ms=latency,
                metadata={"identity_query": True, "evolution": who.get("evolution")},
            )
            self.trace.append(event)
            self.validation.record_activation(
                ActivationRecord(
                    time(),
                    query,
                    activated,
                    [c["label"] for c in who.get("central_concepts", [])],
                    ["identity", "reconstruction"],
                    goal_ids=[g.id for g in self.store.active_goals()],
                    attention_class=attention.value,
                    context_tags=list(self.context.tags),
                )
            )
            self._remember_count += 1
            result = RememberResult(
                answer=who["answer"],
                explanation=self._explanation_text(
                    ExplanationClass.EXPERIENCE, float(who["confidence"])
                ),
                explanation_class=ExplanationClass.EXPERIENCE,
                activated_concept_ids=activated,
                confidence=float(who["confidence"]),
                trace=event.to_public(),
            )
            self.extensions.emit(
                "after_remember",
                {"query": query, "answer": result.answer, "identity_query": True},
            )
            return result

        hits = self._rank_concepts(query)
        why = ["lexical"]
        if has_goal:
            why.append("goal_bias")
        if self.context.tags:
            why.append("context_match")
        if any(c.identity for c in hits[:3]):
            why.append("identity_bias")

        activated_ids = [c.id for c in hits[:5]]
        labels = [c.labels[0] for c in hits[:5]]
        self.validation.record_activation(
            ActivationRecord(
                time(),
                query,
                activated_ids,
                labels,
                why,
                goal_ids=[g.id for g in self.store.active_goals()],
                attention_class=attention.value,
                context_tags=list(self.context.tags),
            )
        )

        edge_types: list[str] = []
        if hits:
            for edge, _nbr in self.store.neighbors(hits[0].id)[:5]:
                edge_types.append(edge.edge_type.value)
                # spreading strengthens association weight (reconsolidation light)
                before = edge.weight
                edge.weight = min(1.0, edge.weight + 0.02)
                if edge.weight != before:
                    self.validation.record_association(
                        AssociationChange(
                            time(),
                            edge.id,
                            "strengthened",
                            edge.source_id,
                            edge.target_id,
                            edge.edge_type.value,
                            edge.weight,
                        )
                    )

        answer, expl_class, confidence = self._format_answer(query, hits)
        explanation = self._explanation_text(expl_class, confidence)

        # Reconsolidation: refresh access + confidence nudge
        reconsolidation = "null"
        if hits:
            reconsolidation = self._reconsolidate_on_recall(hits[0], query)
            displaced = self.buffer.push(
                BufferItem(
                    kind="concept",
                    ref_id=hits[0].id,
                    label=hits[0].labels[0],
                    attention=0.7,
                    importance=hits[0].importance,
                )
            )
            self._note_displace(displaced)

        latency = (perf_counter() - t0) * 1000
        event = CognitiveTraceEvent(
            verb=MemoryVerb.REMEMBER.value,
            attention_class=attention.value,
            context_tags=list(self.context.tags),
            goal_ids=[g.id for g in self.store.active_goals()],
            activated_concept_ids=activated_ids,
            association_edge_types=edge_types,
            explanation_class=expl_class.value,
            reconsolidation=reconsolidation,
            latency_ms=latency,
        )
        self.trace.append(event)
        self._remember_count += 1
        result = RememberResult(
            answer=answer,
            explanation=explanation,
            explanation_class=expl_class,
            activated_concept_ids=activated_ids,
            confidence=confidence,
            trace=event.to_public(),
        )
        self.extensions.emit(
            "after_remember",
            {"query": query, "answer": result.answer, "identity_query": False},
        )
        return result

    def sleep(self, *, apply_low_impact: bool = True) -> dict[str, Any]:
        """M0 stub Sleep — weak-edge prune proposal; high-impact not auto-applied."""
        pruned = 0
        proposals: list[str] = []
        for edge in list(self.store.associations.values()):
            if edge.weight < 0.15 and edge.active:
                if apply_low_impact:
                    edge.active = False
                    pruned += 1
                else:
                    proposals.append(edge.id)
        # Alias candidate proposal (not applied): duplicate labels
        label_map: dict[str, list[str]] = {}
        for c in self.store.concepts.values():
            if not c.active:
                continue
            key = c.labels[0].lower()
            label_map.setdefault(key, []).append(c.id)
        for label, ids in label_map.items():
            if len(ids) > 1:
                proposals.append(f"merge_candidate:{label}:{','.join(ids)}")
            identity_ids = [
                i for i in ids if self.store.concepts.get(i) and self.store.concepts[i].identity
            ]
            if len(identity_ids) > 1:
                proposals.append(
                    f"identity_merge_requires_assent:{label}:{','.join(identity_ids)}"
                )

        payload = {
            "pruned_edges": pruned,
            "proposals": proposals,
            "applied_low_impact": apply_low_impact,
        }
        self.validation.record_sleep(**payload)
        self.trace.append(
            CognitiveTraceEvent(
                verb=MemoryVerb.SLEEP.value,
                reconsolidation="null",
                metadata={"pruned_edges": pruned, "proposal_count": len(proposals)},
            )
        )
        self.extensions.emit("after_sleep", dict(payload))
        return payload

    def who_am_i(self) -> dict[str, Any]:
        """Reconstruct agent identity from schemas + lived structure."""
        return self.identity.who_am_i()

    def identity_snapshot(self) -> dict[str, Any]:
        snap = self.identity.snapshot()
        return {
            "agent_id": snap.agent_id,
            "schemas": snap.schemas,
            "central_concepts": snap.central_concepts,
            "active_goals": snap.active_goals,
            "capabilities": snap.capabilities,
            "uncertainties": snap.uncertainties,
            "lineage_tail": snap.lineage_tail,
            "confidence": snap.confidence,
            "evolution": snap.evolution,
        }

    def assent_identity(self, proposal_id: str) -> dict[str, Any]:
        return self.identity.assent(proposal_id)

    def reject_identity(self, proposal_id: str) -> dict[str, Any]:
        return self.identity.reject(proposal_id)

    def metacognitive_sketch(self) -> dict[str, Any]:
        """Foundations for self-modeling — not consciousness."""
        active_concepts = [c for c in self.store.concepts.values() if c.active]
        uncertain = [
            c
            for c in active_concepts
            if c.confidence < 0.55 or any(a.confidence < 0.55 for a in c.attributes if a.active)
        ]
        ident = self.identity.observables()
        return {
            "agent_id": self.agent_id,
            "what_i_know_count": len(active_concepts),
            "what_i_do_not_know_well_count": len(uncertain),
            "experiences": len(self.store.experiences),
            "active_goals": [g.title for g in self.store.active_goals()],
            "identity_concepts": [c.labels[0] for c in active_concepts if c.identity],
            "identity": ident,
            "encode_count": self._encode_count,
            "remember_count": self._remember_count,
            "buffer_occupancy": len(self.buffer),
            "context_tags": list(self.context.tags),
            "extensions": self.extensions.names(),
        }

    # --- internals --------------------------------------------------------------

    def _note_displace(self, displaced: list[BufferItem]) -> None:
        for item in displaced:
            self.validation.record_working(
                WorkingTransition(time(), "displace", item.ref_id, item.label)
            )

    def _upsert_concept_from_text(self, text: str, *, kind: str, weight: float) -> Concept:
        role = ConceptRole.ENTITY
        identity = False
        label = text.strip()[:80]
        attr_key = "statement"
        attr_val = text.strip()

        if kind == "preference" or re.search(r"\b(prefer|favorite|favourite)\b", text, re.I):
            role = ConceptRole.PREFERENCE
            m = re.search(
                r"(?:favorite|favourite)\s+(\w+(?:\s+\w+)?)\s+is\s+(.+?)(?:\.|$)",
                text,
                re.I,
            )
            if m:
                attr_key = f"favorite_{m.group(1).strip().lower().replace(' ', '_')}"
                attr_val = m.group(2).strip().rstrip(".")
                label = attr_key.replace("_", " ")
            else:
                m2 = re.search(r"prefer\s+(.+?)(?:\.|$)", text, re.I)
                if m2:
                    attr_key = "preference"
                    attr_val = m2.group(1).strip().rstrip(".")
                    label = "preference"
        elif kind == "identity":
            role = ConceptRole.IDENTITY
            identity = True
            label = "identity"

        existing = self.store.find_concepts_by_label(label)
        # Prefer matching preference key
        concept = None
        for cand in existing:
            if any(a.key == attr_key and a.active for a in cand.attributes):
                concept = cand
                break
            if label.lower() in " ".join(cand.labels).lower():
                concept = cand
                break

        if concept is None:
            concept = self.store.add_concept(
                label,
                role=role,
                identity=identity,
                provisional=weight < 0.9,
                importance=weight,
                confidence=min(0.9, 0.5 + weight / 2),
                strength=weight,
            )
            concept.attributes.append(
                Attribute(
                    key=attr_key,
                    value=attr_val,
                    confidence=min(0.9, 0.55 + weight / 2),
                    importance=weight,
                    context_tags=self.context.tags,
                )
            )
        else:
            # strengthen existing
            before_c = concept.confidence
            concept.strength = min(1.0, concept.strength + 0.08)
            concept.importance = max(concept.importance, weight)
            concept.confidence = min(1.0, concept.confidence + 0.05)
            concept.access_count += 1
            concept.last_activated = time()
            concept.provisional = concept.strength < 0.75
            matched = False
            for attr in concept.attributes:
                if attr.key == attr_key and attr.active:
                    if attr.value.lower() != attr_val.lower():
                        # prediction error path — supersede
                        attr.active = False
                        concept.attributes.append(
                            Attribute(
                                key=attr_key,
                                value=attr_val,
                                confidence=min(0.95, attr.confidence + 0.1),
                                importance=weight,
                                context_tags=self.context.tags,
                                version=attr.version + 1,
                            )
                        )
                        self.validation.record_reconsolidation(
                            concept_id=concept.id,
                            attribute_key=attr_key,
                            kind="supersede",
                            previous=attr.value,
                            current=attr_val,
                        )
                    else:
                        before = attr.confidence
                        attr.confidence = min(1.0, attr.confidence + 0.05)
                        self.validation.record_confidence(
                            ConfidenceDelta(
                                time(),
                                concept.id,
                                attr_key,
                                before,
                                attr.confidence,
                                "repeated_encode",
                            )
                        )
                    matched = True
                    break
            if not matched:
                concept.attributes.append(
                    Attribute(
                        key=attr_key,
                        value=attr_val,
                        confidence=min(0.9, 0.55 + weight / 2),
                        importance=weight,
                        context_tags=self.context.tags,
                    )
                )
            self.validation.record_confidence(
                ConfidenceDelta(
                    time(),
                    concept.id,
                    "concept",
                    before_c,
                    concept.confidence,
                    "strengthen",
                )
            )
        return concept

    def _rank_concepts(self, query: str) -> list[Concept]:
        q = query.lower()
        scored: list[tuple[float, Concept]] = []
        active_goal_ids = {g.id for g in self.store.active_goals()}
        for concept in self.store.concepts.values():
            if not concept.active:
                continue
            score = 0.0
            blob = " ".join(concept.labels).lower()
            if any(tok in blob for tok in q.split() if len(tok) > 2):
                score += 2.0
            for attr in concept.attributes:
                if not attr.active:
                    continue
                if attr.value.lower() in q or any(
                    tok in attr.value.lower() for tok in q.split() if len(tok) > 2
                ):
                    score += 3.0 * attr.confidence
                if any(tok in attr.key for tok in q.split() if len(tok) > 2):
                    score += 2.5
                score += 0.5 * self.context.matches(attr.context_tags)
            # goal bias
            for edge, other in self.store.neighbors(concept.id):
                if other.id in active_goal_ids or edge.target_id in active_goal_ids:
                    score += 0.8 * edge.weight
            score *= 0.5 + 0.5 * concept.importance
            score *= 0.5 + 0.5 * concept.strength
            # Identity bias only when already cued, or for explicit who-queries
            if score > 0 or self.identity.is_who_query(query):
                score += self.identity.rank_bonus(concept, query=query)
            if score > 0:
                scored.append((score, concept))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in scored]

    def _format_answer(
        self, query: str, hits: list[Concept]
    ) -> tuple[str, ExplanationClass, float]:
        if not hits:
            return (
                "I don't have anything solid about that yet.",
                ExplanationClass.UNKNOWN,
                0.0,
            )
        top = hits[0]
        # Prefer attribute matching query tokens
        q = query.lower()
        best_attr = None
        for attr in top.attributes:
            if not attr.active:
                continue
            tokens = [tok for tok in q.split() if len(tok) > 2]
            if any(tok in attr.key or tok in attr.value.lower() for tok in tokens):
                best_attr = attr
                break
        if best_attr is None:
            active_attrs = [a for a in top.attributes if a.active]
            best_attr = active_attrs[0] if active_attrs else None
        if best_attr is None:
            return (top.labels[0], ExplanationClass.EXPERIENCE, top.confidence)

        if top.role == ConceptRole.PREFERENCE or best_attr.key.startswith("favorite_"):
            pretty = best_attr.key.replace("favorite_", "favorite ").replace("_", " ")
            answer = f"Your {pretty} is {best_attr.value}."
            return answer, ExplanationClass.PREFERENCE, best_attr.confidence
        answer = best_attr.value
        if not answer.endswith("."):
            answer += "."
        cls = ExplanationClass.EXPERIENCE
        if best_attr.confidence < 0.55:
            cls = ExplanationClass.STALE
        return answer, cls, best_attr.confidence

    def _explanation_text(self, cls: ExplanationClass, confidence: float) -> str:
        # Template classes only — principle P22
        mapping = {
            ExplanationClass.PREFERENCE: (
                "I remembered this because it is one of your preferences."
            ),
            ExplanationClass.EXPERIENCE: (
                "I remembered this from something you shared with me."
            ),
            ExplanationClass.REPEATED: (
                "This strengthened because it has appeared repeatedly."
            ),
            ExplanationClass.STALE: (
                "This information is uncertain because it has not been confirmed strongly."
            ),
            ExplanationClass.CONTESTED: "This is contested; I may need confirmation.",
            ExplanationClass.CONTEXT: "This depends on the current context.",
            ExplanationClass.GOAL: "This came up because of an active goal.",
            ExplanationClass.PROCEDURE: "This is part of a practiced procedure.",
            ExplanationClass.ADOPTED_KNOWLEDGE: (
                "This was adopted into memory from knowledge you accepted."
            ),
            ExplanationClass.UNKNOWN: "I don't have a reliable memory for that yet.",
        }
        text = mapping.get(cls, mapping[ExplanationClass.UNKNOWN])
        if confidence and confidence < 0.55 and cls != ExplanationClass.UNKNOWN:
            text += " Confidence is still developing."
        return text

    def _reconsolidate_on_recall(self, concept: Concept, query: str) -> str:
        before = concept.confidence
        concept.access_count += 1
        concept.last_activated = time()
        concept.strength = min(1.0, concept.strength + 0.03)
        # Correction cue
        if re.search(r"\b(actually|instead|correct|update)\b", query, re.I):
            self.validation.record_reconsolidation(
                concept_id=concept.id, kind="contest_signal", query=query[:80]
            )
            return "contest"
        concept.confidence = min(1.0, concept.confidence + 0.01)
        self.validation.record_confidence(
            ConfidenceDelta(time(), concept.id, "concept", before, concept.confidence, "recall")
        )
        self.validation.record_reconsolidation(
            concept_id=concept.id, kind="light", query=query[:80]
        )
        return "light"
