"""M4 Learning Certification — Gate 3 longitudinal / governance scenarios."""

from __future__ import annotations

from acm.api.engine import CognitiveEngine
from acm.learning.model import AdaptationKind, AdaptationTarget, GovernanceClass
from acm.provenance import TRUSTED_USER_STATEMENT


def _eng(aid: str = "m4-learn") -> CognitiveEngine:
    return CognitiveEngine(agent_id=aid)


def test_l1_reinforce_does_not_invent_experiences() -> None:
    eng = _eng("l1")
    eng.encode("My favorite coffee is Ethiopian.", provenance=TRUSTED_USER_STATEMENT)
    before = len(eng.store.experiences)
    rid = eng.what_do_i_think("Ethiopian coffee")["reflective_experience_id"]
    mid = len(eng.store.experiences)
    learned = eng.learn(reflective_experience_id=rid)
    after = len(eng.store.experiences)
    assert after == mid  # learn invents nothing
    assert mid >= before  # reflection may birth reflective exp
    assert learned["applied"] + learned["abstained"] + learned["proposed"] >= 1


def test_l2_abstain_on_sparse_cue() -> None:
    eng = _eng("l2")
    rid = eng.what_do_i_think("obscure hapax xyzzy unused topic")["reflective_experience_id"]
    learned = eng.learn(reflective_experience_id=rid)
    assert learned["abstained"] >= 1 or learned["applied"] == 0


def test_l4_l5_l6_assent_reject_rollback() -> None:
    eng = _eng("l456")
    eng.encode("My name is Casey.", provenance=TRUSTED_USER_STATEMENT)
    user = eng.identity.schema_concept("user")
    conf0 = float(user.confidence)
    prop = eng.learning._propose(
        target_kind=AdaptationTarget.IDENTITY_CONCEPT,
        target_id=user.id,
        kind=AdaptationKind.WEAKEN,
        reflective_ids=[],
        summary="Assent required.",
    )
    assert prop.governance == GovernanceClass.PROPOSED
    assert abs(float(user.confidence) - conf0) < 1e-9

    # Reject path
    prop2 = eng.learning._propose(
        target_kind=AdaptationTarget.IDENTITY_CONCEPT,
        target_id=user.id,
        kind=AdaptationKind.WEAKEN,
        reflective_ids=[],
        summary="Reject me.",
    )
    assert eng.reject_adaptation(prop2.id)["status"] == "rejected"
    assert abs(float(user.confidence) - conf0) < 1e-9

    # Assent + rollback
    assert eng.assent_adaptation(prop.id)["status"] == "assented"
    assert float(user.confidence) < conf0
    assert eng.rollback_adaptation(prop.id)["status"] == "rolled_back"
    assert abs(float(user.confidence) - conf0) < 1e-6


def test_l7_host_callable_sleep_summary() -> None:
    eng = _eng("l7")
    eng.encode("I prefer quiet mornings.", provenance=TRUSTED_USER_STATEMENT)
    rid = eng.what_do_i_think("quiet mornings")["reflective_experience_id"]
    eng.learn(reflective_experience_id=rid)
    out = eng.sleep()
    assert out.get("sleep_batch_id") or "replay_count" in out or "adaptations_applied" in out
    assert "learning_summary" in out
    summary = eng.daily_learning_summary()
    assert summary["read_only"] is True


def test_l8_goal_nudge() -> None:
    eng = _eng("l8")
    gid = eng.open_goal("finish learning certification", importance=0.45)
    before = float(eng.store.goals[gid].importance)
    ad = eng.learning._adapt_goal(
        gid,
        delta=0.03,
        reflective_ids=[],
        evidence_ids=[],
        sleep_batch_id="",
        summary="Goal reinforce.",
    )
    assert ad is not None
    assert float(eng.store.goals[gid].importance) > before


def test_l9_adoption_boundary() -> None:
    eng = _eng("l9")
    ok = eng.adopt_knowledge("TCP provides reliable streams.", source_label="RFC793")
    assert ok["adopted"] is True
    assert ok["autobiographical"] is False
    assert eng.adopt_knowledge("x\n" * 50, source_label="bulk")["reason"] == "bulk_rejected"


def test_l3_weaken_cool_coordination() -> None:
    eng = _eng("l3")
    enc = eng.encode(
        "I briefly liked fad-widget gadgets.",
        kind="preference",
        pin=True,
        provenance=TRUSTED_USER_STATEMENT,
    )
    assert enc.get("encoded"), enc
    cid = enc["concept_id"]
    eng.forgetting.ensure(cid)
    ad = eng.learning._adapt_concept(
        cid,
        strength_delta=-0.05,
        confidence_delta=-0.04,
        kind=AdaptationKind.WEAKEN,
        reflective_ids=[],
        evidence_ids=[],
        sleep_batch_id="",
        summary="Weaken fad.",
    )
    assert ad is not None
    eng.forgetting.cool(cid, source="learning", steps=1)
    assert eng.store.experiences[enc["experience_id"]].summary
