from __future__ import annotations

from acm import CognitiveEngine


def test_learn_adapts_concepts_without_rewriting_experiences() -> None:
    engine = CognitiveEngine(agent_id="learn")
    enc = engine.encode("My favorite coffee is Ethiopian pour-over.", kind="preference", pin=True)
    experience_id = enc["experience_id"]
    before_summary = engine.store.experiences[experience_id].summary
    before_meta = dict(engine.store.experiences[experience_id].metadata)

    thought = engine.what_do_i_think("What is my favorite coffee?")
    rid = thought["reflective_experience_id"]
    assert rid

    concept_id = enc["concept_id"]
    strength_before = engine.store.concepts[concept_id].strength
    conf_before = engine.store.concepts[concept_id].confidence

    learned = engine.learn(reflective_experience_id=rid)
    assert learned["applied"] + learned["abstained"] + learned["proposed"] >= 1

    # History immutable
    assert engine.store.experiences[experience_id].summary == before_summary
    assert dict(engine.store.experiences[experience_id].metadata) == before_meta

    concept = engine.store.concepts[concept_id]
    # Reinforcing reflections strengthen (or at least leave) living structure with lineage
    if learned["applied"]:
        assert concept.strength >= strength_before - 1e-9 or concept.confidence != conf_before
        assert engine.store.adaptations
        assert any(a.applied for a in engine.store.adaptations.values())

    lessons = engine.what_have_i_learned("coffee")
    assert lessons["question"] == "What have I learned?"
    assert "lesson_count" in lessons


def test_learn_abstains_on_uncertainty() -> None:
    engine = CognitiveEngine(agent_id="learn")
    thought = engine.what_do_i_think("obscure unused hapax topic xyzzy")
    rid = thought["reflective_experience_id"]
    learned = engine.learn(reflective_experience_id=rid)
    # Sparse cue → insufficient/uncertainty path tends to abstain
    assert learned["abstained"] >= 1 or learned["applied"] == 0
    snap = engine.validation.snapshot()
    assert snap["schema"] == "acm.validation/0.10"
    assert "learning" in snap


def test_adaptation_rollback_restores_before() -> None:
    engine = CognitiveEngine(agent_id="learn")
    engine.encode("I like woodworking as a hobby.", kind="preference", pin=True)
    thought = engine.what_do_i_think("woodworking")
    learned = engine.learn(reflective_experience_id=thought["reflective_experience_id"])
    applied = [a for a in learned["adaptations"] if a["applied"] and a["before"]]
    if not applied:
        return
    ad = applied[0]
    target_id = ad["target_id"]
    kind = ad["target_kind"]
    rolled = engine.rollback_adaptation(ad["id"])
    assert rolled["status"] == "rolled_back"
    if kind == "concept" and target_id in engine.store.concepts:
        c = engine.store.concepts[target_id]
        assert abs(c.strength - ad["before"].get("strength", c.strength)) < 1e-6
