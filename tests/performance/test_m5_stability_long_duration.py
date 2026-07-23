"""M5 Cap7 long-duration stress — thousands of experiences, bounded growth."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_long_duration_learning_stability_bounded() -> None:
    eng = CognitiveEngine(agent_id="m5-c7-long")
    # Simulate many experiences + consolidations (months of operation)
    for i in range(120):
        eng.encode(
            f"Day {i}: breakfast then coffee. Note {i % 7}.",
            pin=True,
            provenance=TRUSTED_USER_STATEMENT,
        )
        eid = list(eng.store.experiences.keys())[-1]
        eng.learning.observe_temporal_pattern(
            antecedent="breakfast",
            consequent="coffee",
            experience_id=eid,
            period_hint="morning",
            kind="habit",
        )
        if i % 15 == 14:
            eng.sleep()
            report = eng.check_learning_stability()
            assert report["invents_experiences"] is False
            for c in eng.store.concepts.values():
                if c.active:
                    assert (
                        eng.learning.stability_limits.min_confidence
                        <= c.confidence
                        <= eng.learning.stability_limits.max_confidence
                    )
    # Single habit key — no pattern explosion
    assert len(eng.store.temporal_patterns) == 1
    final = eng.check_learning_stability()
    assert final["stable"] is True or "confidence_bounds" not in final["breaches"]
    assert final["growth"]["temporal_patterns"] == 1
    assert len(eng.store.experiences) == 120
    # Deterministic report fields
    again = eng.check_learning_stability()
    assert again["growth"] == final["growth"]
    assert again["breaches"] == final["breaches"]
