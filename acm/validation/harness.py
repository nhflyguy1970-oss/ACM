"""M0 Cognitive Memory Validation Harness — development/validation capability."""

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
        self.identity_touches.append({"timestamp": time(), **payload})
        self._trim(self.identity_touches)

    def snapshot(self) -> dict[str, Any]:
        """Public validation snapshot — metadata only, no chain-of-thought."""
        return {
            "schema": "acm.validation/0.1",
            "counts": {
                "activations": len(self.activations),
                "confidence_deltas": len(self.confidence_deltas),
                "association_changes": len(self.association_changes),
                "lifecycle": len(self.lifecycle),
                "working_transitions": len(self.working_transitions),
                "reconsolidations": len(self.reconsolidations),
                "sleep_events": len(self.sleep_events),
                "identity_touches": len(self.identity_touches),
            },
            "activations": [asdict(a) for a in self.activations[-40:]],
            "confidence_deltas": [asdict(c) for c in self.confidence_deltas[-40:]],
            "association_changes": [asdict(a) for a in self.association_changes[-40:]],
            "lifecycle": [asdict(e) for e in self.lifecycle[-40:]],
            "working_transitions": [asdict(w) for w in self.working_transitions[-40:]],
            "reconsolidations": deepcopy(self.reconsolidations[-40:]),
            "sleep_events": deepcopy(self.sleep_events[-40:]),
            "identity_touches": deepcopy(self.identity_touches[-40:]),
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
