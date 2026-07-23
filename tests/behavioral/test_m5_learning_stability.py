"""M5 Cap7 — Learning stability (behavioral)."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.learning.stability import LearningStabilityLimits
from acm.provenance import TRUSTED_USER_STATEMENT


def test_check_and_enforce_learning_stability() -> None:
    eng = CognitiveEngine(agent_id="m5-c7")
    eng.encode("I drink tea every morning.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    report = eng.check_learning_stability()
    assert report["question"] == "Is learning stable?"
    assert report["invents_experiences"] is False
    assert report["exposes_internals"] is False
    assert "growth" in report
    exp_n = len(eng.store.experiences)
    # Push confidence out of bounds then enforce
    concept = next(iter(eng.store.concepts.values()))
    concept.confidence = 1.5
    out = eng.enforce_learning_stability()
    assert out["status"] == "enforced"
    assert out["clamped_confidence"] >= 1
    assert concept.confidence <= eng.learning.stability_limits.max_confidence
    assert len(eng.store.experiences) == exp_n
    assert out["invents_experiences"] is False


def test_no_recursive_learning_from_same_reflection() -> None:
    eng = CognitiveEngine(agent_id="m5-c7-rec")
    first = eng.encode("Practice piano daily.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    concept_ids = list(eng.store.concepts.keys())[:2]
    reflective = eng.experiences.reflect(
        first["experience_id"],
        "Reflection: practice is consistent.",
        concept_ids=tuple(concept_ids),
        metadata={"outcomes": "sufficient,insight"},
    )
    ads = eng.learning.learn_from_reflection(reflective.id)
    assert ads  # applied at least one
    second = eng.learning.learn_from_reflection(reflective.id)
    assert second == []
    sleep_out = eng.sleep()
    assert "learning_stability" in sleep_out
    assert sleep_out["learning_stability"]["status"] == "enforced"


def test_temporal_pattern_cap_rejects_explosion() -> None:
    eng = CognitiveEngine(agent_id="m5-c7-cap")
    eng.learning.stability_limits = LearningStabilityLimits(max_temporal_patterns=3)
    eng.encode("Note A.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eid = list(eng.store.experiences.keys())[-1]
    for i in range(5):
        out = eng.learning.observe_temporal_pattern(
            antecedent=f"ante{i}",
            consequent=f"cons{i}",
            experience_id=eid,
            period_hint="daily",
        )
        if i < 3:
            assert out["status"] == "formed"
        else:
            assert out["status"] == "rejected"
            assert out["reason"] == "temporal_pattern_cap"
    assert (
        sum(
            1
            for p in eng.store.temporal_patterns.values()
            if p.status.value != "retired"
        )
        <= 3
    )
