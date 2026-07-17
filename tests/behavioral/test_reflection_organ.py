from __future__ import annotations

from acm import CognitiveEngine
from acm.experiences.kinds import CognitiveKind
from acm.provenance import TRUSTED_USER_STATEMENT


def test_what_do_i_think_creates_reflective_experience() -> None:
    engine = CognitiveEngine(agent_id="ref")
    out = engine.encode(
        "My favorite coffee is dark roast.", kind="preference", provenance=TRUSTED_USER_STATEMENT
    )
    prior_id = out["experience_id"]
    prior_summary = engine.store.experiences[prior_id].summary
    result = engine.what_do_i_think("What is my favorite coffee?")
    assert result["question"] == "What do I think about what I remember?"
    assert result["reflective_experience_id"]
    assert result["activation_reused"] is True
    assert "sufficient" in result["outcomes"] or "consistency" in result["outcomes"]
    # Historical integrity
    assert engine.store.experiences[prior_id].summary == prior_summary
    reflective = engine.store.experiences[result["reflective_experience_id"]]
    assert reflective.cognitive_kind == CognitiveKind.REFLECTION
    assert reflective.reflects_on_id == prior_id


def test_uncertainty_when_unknown() -> None:
    engine = CognitiveEngine(agent_id="ref")
    result = engine.what_do_i_think("What is my favorite tea?")
    honest = (
        result["insufficient_evidence"]
        or "uncertainty" in result["outcomes"]
        or "unknown" in result["outcomes"]
    )
    assert honest
    assert result["questions"] or "don't know" in result["answer"].lower()


def test_no_silent_concept_mutation_on_reflection() -> None:
    engine = CognitiveEngine(agent_id="ref")
    engine.encode("Athena is a husky.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    before = {
        c.id: (c.confidence, c.strength, tuple(c.labels))
        for c in engine.store.concepts.values()
        if c.active
    }
    before_exp = {e.id: e.summary for e in engine.store.experiences.values()}
    engine.what_do_i_think("husky")
    for eid, summary in before_exp.items():
        assert engine.store.experiences[eid].summary == summary
    # Experience history immutable; Reflection births Reflective Experiences.
    kinds = [e.cognitive_kind for e in engine.store.experiences.values()]
    assert CognitiveKind.REFLECTION in kinds
    # Labels unchanged (meaning ownership stays with Concept organ)
    for cid, (_conf, _str, labels) in before.items():
        assert tuple(engine.store.concepts[cid].labels) == labels


def test_pattern_and_confidence_assessment() -> None:
    engine = CognitiveEngine(agent_id="ref")
    engine.encode("A husky is a dog.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    engine.encode("Athena is a husky.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    result = engine.what_do_i_think("husky")
    assert result["confidence_assessment"] >= 0.0
    assert result["activation_reused"] is True
    assert "insight" in result["outcomes"]
