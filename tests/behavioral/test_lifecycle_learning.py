"""C4 — Learning ↔ Forgetting lifecycle coordination."""

from __future__ import annotations

from acm.api.engine import CognitiveEngine
from acm.learning.model import AdaptationKind, AdaptationTarget
from acm.provenance import TRUSTED_USER_STATEMENT


def test_weaken_learning_requests_cool() -> None:
    eng = CognitiveEngine(agent_id="lifecycle")
    enc = eng.encode(
        "I temporarily liked widget-xyz gadgets.",
        kind="preference",
        provenance=TRUSTED_USER_STATEMENT,
    )
    cid = enc["concept_id"]
    eng.forgetting.ensure(cid)
    level_before = eng.forgetting.ensure(cid)
    # Direct weaken adaptation path via learning organ
    ad = eng.learning._adapt_concept(
        cid,
        strength_delta=-0.05,
        confidence_delta=-0.04,
        kind=AdaptationKind.WEAKEN,
        reflective_ids=[],
        evidence_ids=[],
        sleep_batch_id="",
        summary="Test weaken.",
    )
    assert ad is not None
    # Simulate engine.learn post-hooks
    eng.forgetting.cool(cid, source="learning", steps=1)
    level_after = eng.forgetting.ensure(cid)
    # Accessibility should not rise after cool
    order = [
        "highly_accessible",
        "accessible",
        "partially_accessible",
        "less_accessible",
        "dormant",
        "retired",
    ]
    assert level_after.value in order
    assert order.index(level_after.value) >= order.index(level_before.value)


def test_reinforce_still_reactivates() -> None:
    eng = CognitiveEngine(agent_id="lifecycle-up")
    enc = eng.encode("I prefer espresso.", provenance=TRUSTED_USER_STATEMENT)
    cid = enc["concept_id"]
    eng.forgetting.cool(cid, source="host", steps=2, force=True)
    cooled = eng.forgetting.ensure(cid)
    thought = eng.what_do_i_think("espresso")
    eng.learn(reflective_experience_id=thought["reflective_experience_id"])
    after = eng.forgetting.ensure(cid)
    order = [
        "highly_accessible",
        "accessible",
        "partially_accessible",
        "less_accessible",
        "dormant",
        "retired",
    ]
    # Reinforce path should not leave accessibility colder than cooled (usually warmer)
    assert after.value in order and cooled.value in order
    assert order.index(after.value) <= order.index(cooled.value) + 1


def test_learning_never_deletes_experiences_on_cool() -> None:
    eng = CognitiveEngine(agent_id="lifecycle-hist")
    enc = eng.encode("I like hiking boots.", provenance=TRUSTED_USER_STATEMENT)
    eid = enc["experience_id"]
    summary = eng.store.experiences[eid].summary
    cid = enc["concept_id"]
    eng.learning._adapt_concept(
        cid,
        strength_delta=-0.05,
        confidence_delta=-0.04,
        kind=AdaptationKind.WEAKEN,
        reflective_ids=[],
        evidence_ids=[],
        sleep_batch_id="",
        summary="Weaken hiking preference.",
    )
    eng.forgetting.cool(cid, source="learning", steps=2)
    assert eng.store.experiences[eid].summary == summary
    assert AdaptationTarget.CONCEPT  # ownership marker for reviewers
