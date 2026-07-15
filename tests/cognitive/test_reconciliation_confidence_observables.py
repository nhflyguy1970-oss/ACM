from __future__ import annotations

from acm import CognitiveEngine
from acm.associations.model import RelationKind


def test_reconciliation_confidence_observables() -> None:
    engine = CognitiveEngine(agent_id="rclobs")
    a = engine.encode("Signal alpha is reliable.", pin=True)
    b = engine.encode("Signal beta is unreliable.", pin=True)
    engine.associations.relate(
        a["concept_id"],
        b["concept_id"],
        RelationKind.CONFLICTS_WITH,
        strength_forward=0.7,
    )
    engine.how_should_memory_reconcile("signal")
    engine.how_certain_am_i("signal")
    snap = engine.validation.snapshot()
    assert snap["schema"] == "acm.validation/0.12"
    assert "reconciliation" in snap and "confidence" in snap
    assert snap["counts"]["reconciliation_events"] >= 1
    blob = str(snap).lower()
    assert "chain of thought" not in blob
    assert "prompt:" not in blob
