"""Public ACM engine API — plug-and-play for any agent host."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter, time
from typing import Any

from acm._version import __version__ as acm_version
from acm.activation import ActivationEngine
from acm.associations import AssociationOrgan
from acm.attention.field import classify_attention, encode_weight
from acm.concepts import ConceptOrgan
from acm.context.frame import ContextFrame, infer_context
from acm.core.store import CognitiveStore
from acm.experiences import ExperienceOrgan
from acm.identity import IdentityOrgan
from acm.learning import LearningOrgan
from acm.observability.trace import CognitiveTraceEvent, TraceLog
from acm.plugins import ExtensionRegistry
from acm.reflection import ReflectionOrgan
from acm.remembering import RememberingOrgan
from acm.sleep import OfflineCognitionOrgan
from acm.types import (
    AttentionClass,
    EdgeType,
    ExplanationClass,
    MemoryVerb,
)
from acm.validation.harness import (
    AssociationChange,
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
    ambiguous: bool = False
    reconstruction: dict[str, Any] | None = None


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
        self.experiences = ExperienceOrgan(store=self.store, validation=self.validation)
        self.concepts = ConceptOrgan(store=self.store, validation=self.validation)
        self.associations = AssociationOrgan(
            store=self.store, validation=self.validation, concepts=self.concepts
        )
        self.concepts.bind_associations(self.associations)
        self.identity = IdentityOrgan(
            agent_id=agent_id, store=self.store, validation=self.validation
        )
        self.activation = ActivationEngine(
            store=self.store,
            validation=self.validation,
            associations=self.associations,
            identity=self.identity,
            buffer=self.buffer,
        )
        self.remembering = RememberingOrgan(
            store=self.store,
            validation=self.validation,
            activation=self.activation,
            identity=self.identity,
            associations=self.associations,
            buffer=self.buffer,
        )
        self.reflection = ReflectionOrgan(
            store=self.store,
            validation=self.validation,
            remembering=self.remembering,
            experiences=self.experiences,
            buffer=self.buffer,
        )
        self.learning = LearningOrgan(
            store=self.store,
            validation=self.validation,
            concepts=self.concepts,
            associations=self.associations,
            identity=self.identity,
        )
        self.offline = OfflineCognitionOrgan(
            store=self.store,
            validation=self.validation,
            learning=self.learning,
            activation=self.activation,
        )
        self.extensions = ExtensionRegistry(core_version=acm_version)
        self.extensions.bind_engine(self)
        # Metacognitive sketches — emerge from state; not scripted “consciousness”
        self._encode_count = 0
        self._remember_count = 0
        self._reflect_count = 0
        self._learn_count = 0
        self._sleep_count = 0
        # Nuclei exist as organizational anchors; content still arrives via experience
        self.identity.ensure_schemas()
        for cid in self.identity._schema_ids.values():
            concept = self.store.concepts.get(cid)
            if concept is not None:
                self.concepts.register_existing(concept)

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
        # Goal completion is itself an Experience — nothing bypasses Experience
        self.experiences.birth(
            f"Goal completed: {goal.title}",
            encode_kind="experience",
            attention_class=AttentionClass.GOAL.value,
            attention_weight=0.85,
            goal_ids=(goal_id,),
            goal_completed=True,
            context_tags=self.context.tags,
            metadata={"goal_id": goal_id},
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
        external_kind: str = "text",
        envelope_ids: tuple[str, ...] | None = None,
        revises_id: str | None = None,
        reflects_on_id: str | None = None,
        t_start: float | None = None,
        t_end: float | None = None,
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
        durable = weight >= 0.5 or kind in ("preference", "identity") or bool(revises_id)
        if not durable:
            self.validation.record_lifecycle(
                LifecycleEvent(time(), MemoryVerb.ENCODE.value, "", "skipped_low_attention")
            )
            return {"encoded": False, "reason": "low_attention", "attention": attention.value}

        # M3 Concept organ — meaning emerges from encode cues, then binds Experience evidence
        concept, concept_ids = self.concepts.ingest_from_encode(
            text,
            encode_kind=kind,
            weight=weight,
            context_tags=self.context.tags,
        )
        self.identity.mark_concept_formation(concept, text=text, kind=kind)
        identity_signal = self.identity.classify_identity_signal(text, kind=kind)
        identity_influenced = identity_signal in ("agent", "user", "adjacent")

        goal_ids = tuple(g.id for g in self.store.active_goals())
        exp = self.experiences.birth(
            text.strip(),
            external_kind=external_kind,
            encode_kind=kind,
            attention_class=attention.value,
            attention_weight=weight,
            context_tags=self.context.tags,
            goal_ids=goal_ids,
            envelope_ids=tuple(envelope_ids or ()),
            concept_ids=tuple(concept_ids),
            t_start=t_start,
            t_end=t_end,
            revises_id=revises_id,
            reflects_on_id=reflects_on_id,
            identity_influenced=identity_influenced,
        )
        self.concepts.bind_experience(exp, concept_ids=concept_ids)
        self.associations.absorb_experience(
            exp, concept_ids, identity_influenced=identity_influenced
        )

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

        # Goal bias residue: keep legacy concept↔goal edge for compatibility
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
                    g_edge.relation.value,
                    g_edge.weight,
                )
            )

        latency = (perf_counter() - t0) * 1000
        self.trace.append(
            CognitiveTraceEvent(
                verb=MemoryVerb.ENCODE.value,
                attention_class=attention.value,
                context_tags=list(self.context.tags),
                goal_ids=list(goal_ids),
                activated_concept_ids=[concept.id],
                explanation_class=ExplanationClass.EXPERIENCE.value,
                latency_ms=latency,
                metadata={
                    "identity": identity_result,
                    "experience": {
                        "id": exp.id,
                        "cognitive_kind": exp.cognitive_kind.value,
                        "external_kind": exp.external_kind.value,
                        "sequence": exp.sequence,
                    },
                    "concept_ids": concept_ids,
                    "concept_stage": concept.stage.value,
                },
            )
        )
        self._encode_count += 1
        payload = {
            "encoded": True,
            "experience_id": exp.id,
            "concept_id": concept.id,
            "concept_ids": concept_ids,
            "concept": concept.to_public(),
            "attention": attention.value,
            "importance": weight,
            "identity": identity_result,
            "experience": self.experiences.public_view(exp),
        }
        self.extensions.emit("after_encode", dict(payload))
        return payload

    def what_happened(self, **kwargs: Any) -> list[dict[str, Any]]:
        """Cognitive question M2: What happened?"""
        return self.experiences.what_happened(**kwargs)

    def what_is_this(self, cue: str) -> dict[str, Any]:
        """Cognitive question M3: What is this?"""
        return self.concepts.what_is_this(cue)

    def how_related(self, left: str, right: str) -> dict[str, Any]:
        """Cognitive question M4: How is this related?"""
        return self.associations.how_related(left, right)

    def what_do_i_remember(self, cue: str) -> dict[str, Any]:
        """Cognitive question M5: What do I remember?"""
        result = self.remember(cue)
        public = result.reconstruction or {
            "question": "What do I remember?",
            "answer": result.answer,
            "confidence": result.confidence,
            "ambiguous": result.ambiguous,
            "activated_concept_ids": result.activated_concept_ids,
        }
        return public

    def what_do_i_think(self, cue: str) -> dict[str, Any]:
        """Cognitive question M6: What do I think about what I remember?"""
        self.context = infer_context(cue, self.context)
        has_goal = bool(self.store.active_goals())
        attention = classify_attention(cue, has_open_goal=has_goal)
        weight = encode_weight(attention)
        evaluation = self.reflection.what_do_i_think(
            cue,
            context_tags=self.context.tags,
            attention_weight=weight,
            attention_class=attention.value,
        )
        self._reflect_count += 1
        return evaluation.to_public()

    def what_have_i_learned(self, cue: str = "") -> dict[str, Any]:
        """Cognitive question M7: What have I learned?"""
        return self.learning.what_have_i_learned(cue)

    def learn(
        self,
        *,
        reflective_experience_id: str = "",
        cue: str = "",
    ) -> dict[str, Any]:
        """Apply Learning from a Reflective Experience (explicit online adaptation)."""
        rid = reflective_experience_id
        if not rid and cue:
            thought = self.what_do_i_think(cue)
            rid = str(thought.get("reflective_experience_id") or "")
        if not rid:
            return {
                "question": "What have I learned?",
                "answer": "No Reflective Experience available to learn from.",
                "adaptations": [],
            }
        adaptations = self.learning.learn_from_reflection(rid)
        self._learn_count += 1
        self.validation.record_lifecycle(
            LifecycleEvent(time(), MemoryVerb.LEARN.value, rid, f"adaptations:{len(adaptations)}")
        )
        self.trace.append(
            CognitiveTraceEvent(
                verb=MemoryVerb.LEARN.value,
                activated_concept_ids=[],
                metadata={
                    "reflective_experience_id": rid,
                    "adaptation_count": len(adaptations),
                    "applied": sum(1 for a in adaptations if a.applied),
                },
            )
        )
        payload = {
            "question": "What have I learned?",
            "reflective_experience_id": rid,
            "adaptations": [a.to_public() for a in adaptations],
            "applied": sum(1 for a in adaptations if a.applied),
            "proposed": sum(
                1 for a in adaptations if a.governance.value == "proposed"
            ),
            "abstained": sum(
                1 for a in adaptations if a.governance.value == "abstained"
            ),
            "lessons": self.learning.what_have_i_learned().get("lessons", [])[:10],
        }
        self.extensions.emit("after_learn", dict(payload))
        return payload

    def assent_adaptation(self, adaptation_id: str) -> dict[str, Any]:
        return self.learning.assent_adaptation(adaptation_id)

    def reject_adaptation(self, adaptation_id: str) -> dict[str, Any]:
        return self.learning.reject_adaptation(adaptation_id)

    def rollback_adaptation(self, adaptation_id: str) -> dict[str, Any]:
        rolled = self.learning.rollback_adaptation(adaptation_id)
        if rolled is None:
            return {"status": "missing"}
        return {"status": "rolled_back", "adaptation": rolled.to_public()}

    def timeline(self, **kwargs: Any) -> dict[str, Any]:
        return self.experiences.timeline(**kwargs)

    def revise_experience(self, experience_id: str, text: str, **kwargs: Any) -> dict[str, Any]:
        """Correction path — always births a new immutable Experience."""
        return self.encode(text, revises_id=experience_id, **kwargs)

    def reflect_on(self, experience_id: str, text: str, **kwargs: Any) -> dict[str, Any]:
        """Host-supplied Reflective Experience lineage helper.

        Prefer `what_do_i_think` for organ evaluation.
        """
        return self.encode(text, reflects_on_id=experience_id, pin=True, **kwargs)

    def remember(self, query: str) -> RememberResult:
        """Active Remembering — reconstructs via shared Cognitive Activation Architecture."""
        t0 = perf_counter()
        self.context = infer_context(query, self.context)
        has_goal = bool(self.store.active_goals())
        attention = classify_attention(query, has_open_goal=has_goal)
        weight = encode_weight(attention)

        reconstruction = self.remembering.what_do_i_remember(
            query,
            context_tags=self.context.tags,
            attention_weight=weight,
            attention_class=attention.value,
        )
        # Working-memory displacement observability
        for item in reconstruction.activation.get("working_displaced") or []:
            self.validation.record_working(
                WorkingTransition(time(), "displace", item["ref_id"], item["label"])
            )

        try:
            expl_class = ExplanationClass(reconstruction.explanation_class)
        except ValueError:
            expl_class = ExplanationClass.UNKNOWN
        explanation = self.remembering.explanation_text(expl_class, reconstruction.confidence)

        latency = (perf_counter() - t0) * 1000
        assoc_types: list[str] = []
        for aid in reconstruction.association_ids[:8]:
            edge = self.store.associations.get(aid)
            if edge is not None:
                assoc_types.append(edge.relation.value)

        reconsolidation = "null"
        if reconstruction.primary_concept_id:
            reconsolidation = "light"
            if any(
                r.get("kind") == "contest_signal"
                for r in self.validation.reconsolidations[-3:]
            ):
                reconsolidation = "contest"

        event = CognitiveTraceEvent(
            verb=MemoryVerb.REMEMBER.value,
            attention_class=attention.value,
            context_tags=list(self.context.tags),
            goal_ids=[g.id for g in self.store.active_goals()],
            activated_concept_ids=list(reconstruction.activated_concept_ids),
            association_edge_types=assoc_types,
            explanation_class=expl_class.value,
            reconsolidation=reconsolidation,
            latency_ms=latency,
            metadata={
                "ambiguous": reconstruction.ambiguous,
                "identity_query": reconstruction.identity_influenced
                and self.identity.is_who_query(query),
                "activation_steps": reconstruction.activation.get("propagation_steps", 0),
                "experience_participants": len(reconstruction.experience_ids),
            },
        )
        self.trace.append(event)
        self._remember_count += 1
        result = RememberResult(
            answer=reconstruction.answer,
            explanation=explanation,
            explanation_class=expl_class,
            activated_concept_ids=list(reconstruction.activated_concept_ids),
            confidence=reconstruction.confidence,
            trace=event.to_public(),
            ambiguous=reconstruction.ambiguous,
            reconstruction=reconstruction.to_public(),
        )
        self.extensions.emit(
            "after_remember",
            {
                "query": query,
                "answer": result.answer,
                "identity_query": bool(event.metadata.get("identity_query")),
                "ambiguous": result.ambiguous,
            },
        )
        return result

    def sleep(self, *, apply_low_impact: bool = True) -> dict[str, Any]:
        """M8 Offline Cognition — functional consolidation (replay + stabilize)."""
        payload = self.offline.consolidate(apply_low_impact=apply_low_impact)
        self._sleep_count += 1
        self.trace.append(
            CognitiveTraceEvent(
                verb=MemoryVerb.SLEEP.value,
                reconsolidation="sleep",
                metadata={
                    "sleep_batch_id": payload.get("sleep_batch_id"),
                    "replay_count": payload.get("replay_count", 0),
                    "pruned_edges": payload.get("pruned_edges", 0),
                    "proposal_count": len(payload.get("proposals") or []),
                    "adaptations_applied": payload.get("adaptations_applied", 0),
                },
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
        exobs = self.experiences.observables()
        cob = self.concepts.observables()
        aobs = self.associations.observables()
        robs = self.remembering.observables()
        fobs = self.reflection.observables()
        lobs = self.learning.observables()
        oobs = self.offline.observables()
        return {
            "agent_id": self.agent_id,
            "what_i_know_count": len(active_concepts),
            "what_i_do_not_know_well_count": len(uncertain),
            "experiences": len(self.store.experiences),
            "what_happened_count": exobs["experience_count"],
            "active_goals": [g.title for g in self.store.active_goals()],
            "identity_concepts": [c.labels[0] for c in active_concepts if c.identity],
            "identity": ident,
            "experience": exobs,
            "concept": cob,
            "association": aobs,
            "remembering": robs,
            "reflection": fobs,
            "learning": lobs,
            "offline": oobs,
            "encode_count": self._encode_count,
            "remember_count": self._remember_count,
            "reflect_count": self._reflect_count,
            "learn_count": self._learn_count,
            "sleep_count": self._sleep_count,
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
