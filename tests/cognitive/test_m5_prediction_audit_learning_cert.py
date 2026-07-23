"""M5 Cap3 learning certification — hypotheses + prediction audit (L15–L16)."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.associations.model import RelationKind
from acm.provenance import TRUSTED_USER_STATEMENT


def _seed(eng: CognitiveEngine) -> str:
    eng.encode(
        "Coffee often comes after breakfast.", pin=True, provenance=TRUSTED_USER_STATEMENT
    )
    a = eng.store.find_concepts_by_label("breakfast")[0]
    b = eng.store.find_concepts_by_label("coffee")[0]
    eng.associations.relate(a.id, b.id, relation=RelationKind.PREDICTS, strength_forward=0.7)
    return b.id


def test_l15_competing_hypotheses_and_audit_never_invent_experiences() -> None:
    eng = CognitiveEngine(agent_id="m5-l15")
    coffee_id = _seed(eng)
    exp_n = len(eng.store.experiences)
    prov_n = len(eng.store.provenance)
    pred = eng.what_is_likely("After breakfast what is likely?")
    assert pred.get("hypothesis_ids")
    assert len(eng.store.experiences) == exp_n
    audited = eng.audit_prediction(pred["id"], observed_concept_id=coffee_id)
    assert audited["experiences_unchanged"] is True
    assert audited["provenance_unchanged"] is True
    assert len(eng.store.experiences) == exp_n
    assert len(eng.store.provenance) == prov_n
    # Disproved/superseded remain in store (history preserved).
    assert eng.store.hypotheses
    assert audited["audit"]["id"] in eng.store.prediction_audits
    # Confidence bounded
    assert 0.0 <= audited["confidence"] <= 1.0
    # Deterministic re-read of explanation
    e1 = eng.explain_belief_change(audit_id=audited["audit"]["id"])
    e2 = eng.explain_belief_change(audit_id=audited["audit"]["id"])
    assert e1.get("explanation") == e2.get("explanation") or e1 == e2


def test_l16_prediction_audit_learning_rollback_reproducible() -> None:
    eng = CognitiveEngine(agent_id="m5-l16")
    coffee_id = _seed(eng)
    pred = eng.what_is_likely("After breakfast what is likely?")
    concept = eng.store.concepts[coffee_id]
    before_conf = concept.confidence
    audited = eng.audit_prediction(pred["id"], observed_concept_id=coffee_id, apply_learning=True)
    ads = audited.get("adaptation_ids") or []
    # Learning may or may not create adaptations depending on living structure;
    # if it did, rollback must restore without inventing Experiences.
    exp_n = len(eng.store.experiences)
    if ads:
        rolled = eng.rollback_adaptation(ads[0])
        assert rolled["status"] == "rolled_back"
    assert len(eng.store.experiences) == exp_n
    assert 0.05 <= eng.store.concepts[coffee_id].confidence <= 1.0
    # Audit history immutable
    audit_id = audited["audit"]["id"]
    assert eng.store.prediction_audits[audit_id].comparison.value == audited["comparison"]
    # Re-run same seed path on fresh engine → same comparison class for hit path
    eng2 = CognitiveEngine(agent_id="m5-l16b")
    coffee2 = _seed(eng2)
    pred2 = eng2.what_is_likely("After breakfast what is likely?")
    a2 = eng2.audit_prediction(pred2["id"], observed_concept_id=coffee2)
    assert a2["comparison"] == audited["comparison"]
    assert before_conf >= 0.0
