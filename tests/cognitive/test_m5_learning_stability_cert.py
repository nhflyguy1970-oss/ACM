"""M5 Cap7 learning certification — stability (L23–L24)."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_l23_stability_check_never_invents() -> None:
    eng = CognitiveEngine(agent_id="m5-l23")
    eng.encode("Bounded learning matters.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    exp_n = len(eng.store.experiences)
    prov_n = len(eng.store.provenance)
    r1 = eng.check_learning_stability()
    r2 = eng.check_learning_stability()
    assert r1["growth"] == r2["growth"]
    assert r1["stable"] == r2["stable"]
    assert r1["invents_experiences"] is False
    assert len(eng.store.experiences) == exp_n
    assert len(eng.store.provenance) == prov_n


def test_l24_enforce_clamps_and_blocks_recursive_relearn() -> None:
    eng = CognitiveEngine(agent_id="m5-l24")
    first = eng.encode(
        "Stability requires evidence.", pin=True, provenance=TRUSTED_USER_STATEMENT
    )
    concept = next(iter(eng.store.concepts.values()))
    concept.confidence = 2.0
    exp_n = len(eng.store.experiences)
    prov_n = len(eng.store.provenance)
    enforced = eng.enforce_learning_stability()
    assert enforced["status"] == "enforced"
    assert concept.confidence <= eng.learning.stability_limits.max_confidence
    assert concept.confidence >= eng.learning.stability_limits.min_confidence
    assert len(eng.store.experiences) == exp_n
    assert len(eng.store.provenance) == prov_n

    reflective = eng.experiences.reflect(
        first["experience_id"],
        "Reflection on stability.",
        concept_ids=(concept.id,),
        metadata={"outcomes": "sufficient"},
    )
    a1 = eng.learning.learn_from_reflection(reflective.id)
    a2 = eng.learning.learn_from_reflection(reflective.id)
    assert len(a1) >= 1
    assert a2 == []
    assert concept.confidence <= eng.learning.stability_limits.max_confidence
