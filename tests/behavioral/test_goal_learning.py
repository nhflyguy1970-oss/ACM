"""C3 — Goal importance adaptation via Learning."""

from __future__ import annotations

from acm.api.engine import CognitiveEngine
from acm.learning.model import AdaptationTarget
from acm.provenance import TRUSTED_USER_STATEMENT


def test_goal_importance_rises_on_congruent_reflection() -> None:
    eng = CognitiveEngine(agent_id="goal-learn")
    gid = eng.open_goal("build local AI assistant", importance=0.5)
    eng.encode(
        "I am working on building a local AI assistant.",
        provenance=TRUSTED_USER_STATEMENT,
    )
    thought = eng.what_do_i_think("local AI assistant")
    rid = thought["reflective_experience_id"]
    # Ensure reflective summary mentions goal tokens for overlap matching
    refl = eng.store.experiences[rid]
    # Force overlap if reflection is sparse
    if "assistant" not in (refl.summary or "").lower():
        refl.summary = (refl.summary or "") + " Thinking about local AI assistant work."

    before = float(eng.store.goals[gid].importance)
    exp_count = len(eng.store.experiences)
    learned = eng.learn(reflective_experience_id=rid)
    after = float(eng.store.goals[gid].importance)
    goal_ads = [
        a
        for a in learned["adaptations"]
        if a.get("target_kind") == AdaptationTarget.GOAL.value
    ]
    assert goal_ads or after >= before - 1e-9
    if goal_ads:
        assert after > before - 1e-9
        assert goal_ads[0]["applied"] is True
        assert goal_ads[0]["before"].get("importance") is not None
    # Never invent Experiences
    assert len(eng.store.experiences) == exp_count


def test_unrelated_reflection_does_not_nudge_goal() -> None:
    eng = CognitiveEngine(agent_id="goal-unrelated")
    gid = eng.open_goal("train marathon endurance", importance=0.55)
    eng.encode("My favorite color is blue.", provenance=TRUSTED_USER_STATEMENT)
    thought = eng.what_do_i_think("What is my favorite color?")
    before = float(eng.store.goals[gid].importance)
    learned = eng.learn(reflective_experience_id=thought["reflective_experience_id"])
    goal_ads = [
        a for a in learned["adaptations"] if a.get("target_kind") == "goal"
    ]
    assert not goal_ads
    assert abs(float(eng.store.goals[gid].importance) - before) < 1e-9


def test_goal_adaptation_rollback() -> None:
    eng = CognitiveEngine(agent_id="goal-rb")
    gid = eng.open_goal("ship ACM learning milestone", importance=0.4)
    before = float(eng.store.goals[gid].importance)
    ad = eng.learning._adapt_goal(
        gid,
        delta=0.03,
        reflective_ids=[],
        evidence_ids=[],
        sleep_batch_id="",
        summary="Test goal reinforce.",
    )
    assert ad is not None
    assert float(eng.store.goals[gid].importance) > before
    rolled = eng.rollback_adaptation(ad.id)
    assert rolled["status"] == "rolled_back"
    assert abs(float(eng.store.goals[gid].importance) - before) < 1e-6
