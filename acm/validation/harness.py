"""M0/M1 Cognitive Memory Validation Harness — development/validation capability."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from time import time
from typing import Any


@dataclass
class ActivationRecord:
    timestamp: float
    cue: str
    concept_ids: list[str]
    concept_labels: list[str]
    why: list[str]  # cue classes — not chain-of-thought
    goal_ids: list[str] = field(default_factory=list)
    attention_class: str = "default"
    context_tags: list[str] = field(default_factory=list)


@dataclass
class ConfidenceDelta:
    timestamp: float
    concept_id: str
    attribute_key: str
    before: float
    after: float
    reason: str


@dataclass
class AssociationChange:
    timestamp: float
    edge_id: str
    change: str  # added | strengthened | weakened | superseded
    source_id: str
    target_id: str
    edge_type: str
    weight: float


@dataclass
class LifecycleEvent:
    timestamp: float
    verb: str
    subject_id: str
    detail: str


@dataclass
class WorkingTransition:
    timestamp: float
    action: str  # enter | displace | clear
    ref_id: str
    label: str


class ValidationHarness:
    """Records observable cognitive state for milestone validation.

    Not a runtime organ. Not host-specific. Safe metadata only.
    """

    def __init__(self, *, max_events: int = 2000) -> None:
        self.max_events = max_events
        self.activations: list[ActivationRecord] = []
        self.confidence_deltas: list[ConfidenceDelta] = []
        self.association_changes: list[AssociationChange] = []
        self.lifecycle: list[LifecycleEvent] = []
        self.working_transitions: list[WorkingTransition] = []
        self.reconsolidations: list[dict[str, Any]] = []
        self.sleep_events: list[dict[str, Any]] = []
        self.identity_touches: list[dict[str, Any]] = []
        self.experience_events: list[dict[str, Any]] = []
        self.concept_events: list[dict[str, Any]] = []
        # Aggregated identity observables (M1)
        self.identity_metrics: dict[str, float | int] = {
            "growth": 0,
            "stability": 0,
            "change": 0,
            "influence": 0,
            "lineage_events": 0,
            "last_confidence": 0.0,
        }
        # Aggregated experience observables (M2)
        self.experience_metrics: dict[str, float | int] = {
            "births": 0,
            "lineage": 0,
            "salience_evolutions": 0,
            "temporal_links": 0,
            "lifecycle": 0,
            "multimodal": 0,
            "identity_influenced": 0,
            "goal_influenced": 0,
        }
        # Aggregated concept observables (M3)
        self.concept_metrics: dict[str, float | int] = {
            "births": 0,
            "nuclei": 0,
            "strengthenings": 0,
            "weakenings": 0,
            "maturity_changes": 0,
            "abstractions": 0,
            "hierarchy": 0,
            "merges": 0,
            "splits": 0,
            "prototypes": 0,
        }
        self.association_events: list[dict[str, Any]] = []
        self.association_metrics: dict[str, float | int] = {
            "births": 0,
            "strengthenings": 0,
            "weakenings": 0,
            "dormancies": 0,
            "reactivations": 0,
            "neighborhoods": 0,
            "clusters": 0,
            "goal_influenced": 0,
            "identity_influenced": 0,
            "temporal": 0,
            "asymmetric_births": 0,
        }
        self.remembering_events: list[dict[str, Any]] = []
        self.remembering_metrics: dict[str, float | int] = {
            "reconstructions": 0,
            "activations": 0,
            "ambiguities": 0,
            "propagations": 0,
            "decays": 0,
            "experience_participants": 0,
            "goal_influenced": 0,
            "identity_influenced": 0,
            "context_influenced": 0,
            "working_influenced": 0,
        }
        self.reflection_events: list[dict[str, Any]] = []
        self.reflection_metrics: dict[str, float | int] = {
            "reflections": 0,
            "contradictions": 0,
            "patterns": 0,
            "questions": 0,
            "hypotheses": 0,
            "insufficient_evidence": 0,
            "activation_reused": 0,
            "reflective_experiences": 0,
        }

    def _trim(self, seq: list[Any]) -> None:
        overflow = len(seq) - self.max_events
        if overflow > 0:
            del seq[:overflow]

    def record_activation(self, record: ActivationRecord) -> None:
        self.activations.append(record)
        self._trim(self.activations)

    def record_confidence(self, delta: ConfidenceDelta) -> None:
        self.confidence_deltas.append(delta)
        self._trim(self.confidence_deltas)

    def record_association(self, change: AssociationChange) -> None:
        self.association_changes.append(change)
        self._trim(self.association_changes)

    def record_lifecycle(self, event: LifecycleEvent) -> None:
        self.lifecycle.append(event)
        self._trim(self.lifecycle)

    def record_working(self, transition: WorkingTransition) -> None:
        self.working_transitions.append(transition)
        self._trim(self.working_transitions)

    def record_reconsolidation(self, **payload: Any) -> None:
        self.reconsolidations.append({"timestamp": time(), **payload})
        self._trim(self.reconsolidations)

    def record_sleep(self, **payload: Any) -> None:
        self.sleep_events.append({"timestamp": time(), **payload})
        self._trim(self.sleep_events)

    def record_identity(self, **payload: Any) -> None:
        event = {"timestamp": time(), **payload}
        self.identity_touches.append(event)
        self._trim(self.identity_touches)
        # Roll metrics from observable fields
        for key in ("growth", "stability", "change", "influence"):
            if key in payload and payload[key]:
                self.identity_metrics[key] = int(self.identity_metrics[key]) + int(
                    payload[key]
                )
        if payload.get("lineage") or payload.get("lineage_length") is not None:
            self.identity_metrics["lineage_events"] = int(
                self.identity_metrics["lineage_events"]
            ) + (1 if payload.get("lineage") else 0)
            if payload.get("lineage_length") is not None:
                # keep max observed lineage length as evolution proxy
                self.identity_metrics["lineage_events"] = max(
                    int(self.identity_metrics["lineage_events"]),
                    int(payload["lineage_length"]),
                )
        if "confidence" in payload and payload["confidence"] is not None:
            self.identity_metrics["last_confidence"] = float(payload["confidence"])
        elif "confidence_after" in payload:
            self.identity_metrics["last_confidence"] = float(payload["confidence_after"])

    def record_experience(self, **payload: Any) -> None:
        event = {"timestamp": time(), **payload}
        self.experience_events.append(event)
        self._trim(self.experience_events)
        action = str(payload.get("action", ""))
        if action == "birth":
            self.experience_metrics["births"] = int(self.experience_metrics["births"]) + 1
            if payload.get("lineage"):
                self.experience_metrics["lineage"] = int(self.experience_metrics["lineage"]) + 1
            if payload.get("identity_influenced"):
                self.experience_metrics["identity_influenced"] = (
                    int(self.experience_metrics["identity_influenced"]) + 1
                )
            if int(payload.get("goal_count") or 0) > 0:
                self.experience_metrics["goal_influenced"] = (
                    int(self.experience_metrics["goal_influenced"]) + 1
                )
        elif action == "salience_evolution":
            self.experience_metrics["salience_evolutions"] = (
                int(self.experience_metrics["salience_evolutions"]) + 1
            )
        elif action == "temporal_link":
            self.experience_metrics["temporal_links"] = (
                int(self.experience_metrics["temporal_links"]) + 1
            )
        elif action == "lifecycle":
            self.experience_metrics["lifecycle"] = int(self.experience_metrics["lifecycle"]) + 1
        elif action == "envelope" or payload.get("multimodal"):
            self.experience_metrics["multimodal"] = int(self.experience_metrics["multimodal"]) + 1

    def record_concept(self, **payload: Any) -> None:
        event = {"timestamp": time(), **payload}
        self.concept_events.append(event)
        self._trim(self.concept_events)
        if payload.get("birth") or payload.get("action") == "birth":
            self.concept_metrics["births"] = int(self.concept_metrics["births"]) + 1
        if payload.get("nucleus"):
            self.concept_metrics["nuclei"] = int(self.concept_metrics["nuclei"]) + 1
        if payload.get("strengthening"):
            self.concept_metrics["strengthenings"] = (
                int(self.concept_metrics["strengthenings"]) + 1
            )
        if payload.get("weakening"):
            self.concept_metrics["weakenings"] = int(self.concept_metrics["weakenings"]) + 1
        if payload.get("maturity") or payload.get("lifecycle"):
            self.concept_metrics["maturity_changes"] = (
                int(self.concept_metrics["maturity_changes"]) + 1
            )
        if payload.get("abstraction"):
            self.concept_metrics["abstractions"] = int(self.concept_metrics["abstractions"]) + 1
        if payload.get("hierarchy"):
            self.concept_metrics["hierarchy"] = int(self.concept_metrics["hierarchy"]) + 1
        if payload.get("merge"):
            self.concept_metrics["merges"] = int(self.concept_metrics["merges"]) + 1
        if payload.get("split"):
            self.concept_metrics["splits"] = int(self.concept_metrics["splits"]) + 1
        if payload.get("prototype"):
            self.concept_metrics["prototypes"] = int(self.concept_metrics["prototypes"]) + 1

    def record_association_organ(self, **payload: Any) -> None:
        event = {"timestamp": time(), **payload}
        self.association_events.append(event)
        self._trim(self.association_events)
        if payload.get("birth") or payload.get("action") == "birth":
            self.association_metrics["births"] = int(self.association_metrics["births"]) + 1
            fwd = float(payload.get("strength_forward") or 0)
            back = float(payload.get("strength_backward") or 0)
            if abs(fwd - back) > 0.08:
                self.association_metrics["asymmetric_births"] = (
                    int(self.association_metrics["asymmetric_births"]) + 1
                )
        if payload.get("strengthening"):
            self.association_metrics["strengthenings"] = (
                int(self.association_metrics["strengthenings"]) + 1
            )
        if payload.get("weakening"):
            self.association_metrics["weakenings"] = int(self.association_metrics["weakenings"]) + 1
        if payload.get("action") == "reactivate" or payload.get("reactivation"):
            self.association_metrics["reactivations"] = (
                int(self.association_metrics["reactivations"]) + 1
            )
        if payload.get("distance") == "dormant":
            self.association_metrics["dormancies"] = int(self.association_metrics["dormancies"]) + 1
        if payload.get("neighborhood") or payload.get("clusters"):
            self.association_metrics["neighborhoods"] = (
                int(self.association_metrics["neighborhoods"]) + 1
            )
        if payload.get("clusters"):
            self.association_metrics["clusters"] = int(self.association_metrics["clusters"]) + 1
        if payload.get("goal_influenced"):
            self.association_metrics["goal_influenced"] = (
                int(self.association_metrics["goal_influenced"]) + 1
            )
        if payload.get("identity_influenced"):
            self.association_metrics["identity_influenced"] = (
                int(self.association_metrics["identity_influenced"]) + 1
            )
        if payload.get("temporal"):
            self.association_metrics["temporal"] = int(self.association_metrics["temporal"]) + 1

    def record_remembering(self, **payload: Any) -> None:
        event = {"timestamp": time(), **payload}
        self.remembering_events.append(event)
        self._trim(self.remembering_events)
        action = payload.get("action")
        if action == "activation":
            self.remembering_metrics["activations"] = (
                int(self.remembering_metrics["activations"]) + 1
            )
            steps = int(payload.get("propagation_steps") or 0)
            if steps:
                self.remembering_metrics["propagations"] = (
                    int(self.remembering_metrics["propagations"]) + steps
                )
            decayed = int(payload.get("decayed") or 0)
            if decayed:
                self.remembering_metrics["decays"] = (
                    int(self.remembering_metrics["decays"]) + decayed
                )
        if payload.get("reconstruction") or action == "reconstruction":
            self.remembering_metrics["reconstructions"] = (
                int(self.remembering_metrics["reconstructions"]) + 1
            )
        if payload.get("ambiguity") or payload.get("ambiguous"):
            self.remembering_metrics["ambiguities"] = (
                int(self.remembering_metrics["ambiguities"]) + 1
            )
        participants = int(payload.get("experience_participants") or 0)
        if participants:
            self.remembering_metrics["experience_participants"] = (
                int(self.remembering_metrics["experience_participants"]) + participants
            )
        if payload.get("goal_influenced"):
            self.remembering_metrics["goal_influenced"] = (
                int(self.remembering_metrics["goal_influenced"]) + 1
            )
        if payload.get("identity_influenced"):
            self.remembering_metrics["identity_influenced"] = (
                int(self.remembering_metrics["identity_influenced"]) + 1
            )
        if payload.get("context_influenced"):
            self.remembering_metrics["context_influenced"] = (
                int(self.remembering_metrics["context_influenced"]) + 1
            )
        if payload.get("working_influenced"):
            self.remembering_metrics["working_influenced"] = (
                int(self.remembering_metrics["working_influenced"]) + 1
            )

    def record_reflection(self, **payload: Any) -> None:
        event = {"timestamp": time(), **payload}
        self.reflection_events.append(event)
        self._trim(self.reflection_events)
        if payload.get("reflection") or payload.get("action") == "evaluation":
            self.reflection_metrics["reflections"] = (
                int(self.reflection_metrics["reflections"]) + 1
            )
        if payload.get("contradiction"):
            self.reflection_metrics["contradictions"] = (
                int(self.reflection_metrics["contradictions"]) + 1
            )
        if payload.get("pattern"):
            self.reflection_metrics["patterns"] = int(self.reflection_metrics["patterns"]) + 1
        if payload.get("question"):
            self.reflection_metrics["questions"] = int(self.reflection_metrics["questions"]) + 1
        if payload.get("hypothesis"):
            self.reflection_metrics["hypotheses"] = (
                int(self.reflection_metrics["hypotheses"]) + 1
            )
        if payload.get("insufficient_evidence"):
            self.reflection_metrics["insufficient_evidence"] = (
                int(self.reflection_metrics["insufficient_evidence"]) + 1
            )
        if payload.get("activation_reused"):
            self.reflection_metrics["activation_reused"] = (
                int(self.reflection_metrics["activation_reused"]) + 1
            )
        if payload.get("reflective_experience_id"):
            self.reflection_metrics["reflective_experiences"] = (
                int(self.reflection_metrics["reflective_experiences"]) + 1
            )

    def snapshot(self) -> dict[str, Any]:
        """Public validation snapshot — metadata only, no chain-of-thought."""
        return {
            "schema": "acm.validation/0.7",
            "counts": {
                "activations": len(self.activations),
                "confidence_deltas": len(self.confidence_deltas),
                "association_changes": len(self.association_changes),
                "lifecycle": len(self.lifecycle),
                "working_transitions": len(self.working_transitions),
                "reconsolidations": len(self.reconsolidations),
                "sleep_events": len(self.sleep_events),
                "identity_touches": len(self.identity_touches),
                "experience_events": len(self.experience_events),
                "concept_events": len(self.concept_events),
                "association_events": len(self.association_events),
                "remembering_events": len(self.remembering_events),
                "reflection_events": len(self.reflection_events),
            },
            "identity": {
                "growth": self.identity_metrics["growth"],
                "stability": self.identity_metrics["stability"],
                "change": self.identity_metrics["change"],
                "confidence": self.identity_metrics["last_confidence"],
                "influence": self.identity_metrics["influence"],
                "lineage": self.identity_metrics["lineage_events"],
                "evolution": {
                    "touches": len(self.identity_touches),
                    "growth": self.identity_metrics["growth"],
                    "stability": self.identity_metrics["stability"],
                    "change": self.identity_metrics["change"],
                    "influence": self.identity_metrics["influence"],
                },
            },
            "experience": {
                "births": self.experience_metrics["births"],
                "lineage": self.experience_metrics["lineage"],
                "salience_evolutions": self.experience_metrics["salience_evolutions"],
                "temporal_links": self.experience_metrics["temporal_links"],
                "lifecycle": self.experience_metrics["lifecycle"],
                "multimodal": self.experience_metrics["multimodal"],
                "identity_influenced": self.experience_metrics["identity_influenced"],
                "goal_influenced": self.experience_metrics["goal_influenced"],
                "context_events": sum(
                    1 for e in self.experience_events if e.get("context_tags")
                ),
            },
            "concept": {
                "births": self.concept_metrics["births"],
                "nuclei": self.concept_metrics["nuclei"],
                "strengthenings": self.concept_metrics["strengthenings"],
                "weakenings": self.concept_metrics["weakenings"],
                "maturity": self.concept_metrics["maturity_changes"],
                "hierarchy": self.concept_metrics["hierarchy"],
                "abstraction": self.concept_metrics["abstractions"],
                "merge_proposals": self.concept_metrics["merges"],
                "split_proposals": self.concept_metrics["splits"],
                "prototypes": self.concept_metrics["prototypes"],
                "evolution": {
                    "touches": len(self.concept_events),
                    "births": self.concept_metrics["births"],
                    "strengthenings": self.concept_metrics["strengthenings"],
                    "weakenings": self.concept_metrics["weakenings"],
                },
            },
            "association": {
                "births": self.association_metrics["births"],
                "strengthenings": self.association_metrics["strengthenings"],
                "weakenings": self.association_metrics["weakenings"],
                "dormancies": self.association_metrics["dormancies"],
                "reactivations": self.association_metrics["reactivations"],
                "neighborhoods": self.association_metrics["neighborhoods"],
                "clusters": self.association_metrics["clusters"],
                "goal_influenced": self.association_metrics["goal_influenced"],
                "identity_influenced": self.association_metrics["identity_influenced"],
                "temporal": self.association_metrics["temporal"],
                "asymmetric_births": self.association_metrics["asymmetric_births"],
                "evolution": {
                    "touches": len(self.association_events),
                    "births": self.association_metrics["births"],
                    "strengthenings": self.association_metrics["strengthenings"],
                    "weakenings": self.association_metrics["weakenings"],
                },
            },
            "remembering": {
                "reconstructions": self.remembering_metrics["reconstructions"],
                "activations": self.remembering_metrics["activations"],
                "ambiguities": self.remembering_metrics["ambiguities"],
                "propagations": self.remembering_metrics["propagations"],
                "decays": self.remembering_metrics["decays"],
                "experience_participants": self.remembering_metrics["experience_participants"],
                "goal_influenced": self.remembering_metrics["goal_influenced"],
                "identity_influenced": self.remembering_metrics["identity_influenced"],
                "context_influenced": self.remembering_metrics["context_influenced"],
                "working_influenced": self.remembering_metrics["working_influenced"],
                "evolution": {
                    "touches": len(self.remembering_events),
                    "reconstructions": self.remembering_metrics["reconstructions"],
                    "activations": self.remembering_metrics["activations"],
                    "ambiguities": self.remembering_metrics["ambiguities"],
                },
            },
            "activations": [asdict(a) for a in self.activations[-40:]],
            "confidence_deltas": [asdict(c) for c in self.confidence_deltas[-40:]],
            "association_changes": [asdict(a) for a in self.association_changes[-40:]],
            "lifecycle": [asdict(e) for e in self.lifecycle[-40:]],
            "working_transitions": [asdict(w) for w in self.working_transitions[-40:]],
            "reconsolidations": deepcopy(self.reconsolidations[-40:]),
            "sleep_events": deepcopy(self.sleep_events[-40:]),
            "identity_touches": deepcopy(self.identity_touches[-40:]),
            "experience_events": deepcopy(self.experience_events[-40:]),
            "concept_events": deepcopy(self.concept_events[-40:]),
            "association_events": deepcopy(self.association_events[-40:]),
            "remembering_events": deepcopy(self.remembering_events[-40:]),
            "reflection": {
                "reflections": self.reflection_metrics["reflections"],
                "contradictions": self.reflection_metrics["contradictions"],
                "patterns": self.reflection_metrics["patterns"],
                "questions": self.reflection_metrics["questions"],
                "hypotheses": self.reflection_metrics["hypotheses"],
                "insufficient_evidence": self.reflection_metrics["insufficient_evidence"],
                "activation_reused": self.reflection_metrics["activation_reused"],
                "reflective_experiences": self.reflection_metrics["reflective_experiences"],
                "evolution": {
                    "touches": len(self.reflection_events),
                    "reflections": self.reflection_metrics["reflections"],
                    "contradictions": self.reflection_metrics["contradictions"],
                    "questions": self.reflection_metrics["questions"],
                },
            },
            "reflection_events": deepcopy(self.reflection_events[-40:]),
        }

    def reset(self) -> None:
        self.activations.clear()
        self.confidence_deltas.clear()
        self.association_changes.clear()
        self.lifecycle.clear()
        self.working_transitions.clear()
        self.reconsolidations.clear()
        self.sleep_events.clear()
        self.identity_touches.clear()
        self.experience_events.clear()
        self.concept_events.clear()
        self.association_events.clear()
        self.remembering_events.clear()
        self.reflection_events.clear()
        self.identity_metrics = {
            "growth": 0,
            "stability": 0,
            "change": 0,
            "influence": 0,
            "lineage_events": 0,
            "last_confidence": 0.0,
        }
        self.experience_metrics = {
            "births": 0,
            "lineage": 0,
            "salience_evolutions": 0,
            "temporal_links": 0,
            "lifecycle": 0,
            "multimodal": 0,
            "identity_influenced": 0,
            "goal_influenced": 0,
        }
        self.concept_metrics = {
            "births": 0,
            "nuclei": 0,
            "strengthenings": 0,
            "weakenings": 0,
            "maturity_changes": 0,
            "abstractions": 0,
            "hierarchy": 0,
            "merges": 0,
            "splits": 0,
            "prototypes": 0,
        }
        self.association_metrics = {
            "births": 0,
            "strengthenings": 0,
            "weakenings": 0,
            "dormancies": 0,
            "reactivations": 0,
            "neighborhoods": 0,
            "clusters": 0,
            "goal_influenced": 0,
            "identity_influenced": 0,
            "temporal": 0,
            "asymmetric_births": 0,
        }
        self.remembering_metrics = {
            "reconstructions": 0,
            "activations": 0,
            "ambiguities": 0,
            "propagations": 0,
            "decays": 0,
            "experience_participants": 0,
            "goal_influenced": 0,
            "identity_influenced": 0,
            "context_influenced": 0,
            "working_influenced": 0,
        }
        self.reflection_metrics = {
            "reflections": 0,
            "contradictions": 0,
            "patterns": 0,
            "questions": 0,
            "hypotheses": 0,
            "insufficient_evidence": 0,
            "activation_reused": 0,
            "reflective_experiences": 0,
        }
