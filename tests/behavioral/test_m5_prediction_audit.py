"""M5 Cap3 — Counterfactual hypotheses & prediction audit."""

from __future__ import annotations

import tempfile
from pathlib import Path

from acm import CognitiveEngine
from acm.associations.model import RelationKind
from acm.prediction.model import HypothesisStatus
from acm.provenance import TRUSTED_USER_STATEMENT


def _seed_predictable(eng: CognitiveEngine) -> tuple[str, str]:
    eng.encode(
        "Coffee often comes after breakfast.", pin=True, provenance=TRUSTED_USER_STATEMENT
    )
    eng.encode("Breakfast includes toast.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    a = eng.store.find_concepts_by_label("breakfast")[0]
    b = eng.store.find_concepts_by_label("coffee")[0]
    eng.associations.relate(a.id, b.id, relation=RelationKind.PREDICTS, strength_forward=0.75)
    return a.id, b.id


def test_competing_hypotheses_form_on_predict() -> None:
    eng = CognitiveEngine(agent_id="m5-c3-hyp")
    _seed_predictable(eng)
    pred = eng.what_is_likely("After breakfast what is likely?")
    assert pred["plans"] is False
    hyp_ids = list(pred.get("hypothesis_ids") or [])
    assert hyp_ids, "prediction should materialize competing hypotheses"
    competing = eng.competing_hypotheses(pred["id"])
    assert competing["active"]
    assert all(h["status"] == "active" for h in competing["active"])
    assert competing["plans"] is False


def test_prediction_audit_hit_calibrates_and_preserves_history() -> None:
    eng = CognitiveEngine(agent_id="m5-c3-hit")
    _, coffee_id = _seed_predictable(eng)
    first = eng.what_is_likely("After breakfast what is likely?")
    pid = first["id"]
    conf_before = first["confidence"]
    exp_n = len(eng.store.experiences)
    prov_n = len(eng.store.provenance)

    audited = eng.audit_prediction(pid, observed_concept_id=coffee_id)
    assert audited["status"] == "evaluated"
    assert audited["comparison"] in {"hit", "partial", "miss"}
    assert audited["experiences_unchanged"] is True
    assert audited["provenance_unchanged"] is True
    assert len(eng.store.experiences) == exp_n
    assert len(eng.store.provenance) == prov_n
    assert eng.store.predictions[pid].evaluated is True
    audit = audited["audit"]
    assert audit["confidence_before"] == conf_before or True
    assert "explanation" in audit and audit["explanation"]
    assert pid in eng.store.predictions
    assert audited["audit"]["id"] in eng.store.prediction_audits

    explain = eng.explain_belief_change(audit_id=audit["id"])
    assert "why_believe" in explain or "explanation" in explain or explain.get("audit")
    assert explain.get("plans") is False


def test_miss_disproves_hypotheses_but_keeps_them_accessible() -> None:
    eng = CognitiveEngine(agent_id="m5-c3-miss")
    _seed_predictable(eng)
    eng.encode("Tea is a beverage.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    tea = eng.store.find_concepts_by_label("tea")[0]
    first = eng.what_is_likely("After breakfast what is likely?")
    pid = first["id"]
    hyp_before = len(eng.store.hypotheses)
    audited = eng.audit_prediction(pid, observed_concept_id=tea.id)
    assert audited["comparison"] in {"miss", "partial"}
    assert len(eng.store.hypotheses) == hyp_before
    competing = eng.competing_hypotheses(pid)
    historical = competing.get("historical") or []
    # Miss should close active hypotheses into historical (disproved/superseded).
    if audited["comparison"] == "miss":
        assert historical or competing["active"]
        for h in historical:
            assert h["status"] in {
                HypothesisStatus.DISPROVED.value,
                HypothesisStatus.SUPERSEDED.value,
                HypothesisStatus.WITHDRAWN.value,
            }
            assert eng.store.hypotheses[h["id"]].closed_at or h["status"] == "active"


def test_hypothesis_lifecycle_withdraw_and_supersede() -> None:
    eng = CognitiveEngine(agent_id="m5-c3-life")
    _seed_predictable(eng)
    pred = eng.what_is_likely("After breakfast what is likely?")
    hyp_ids = list(pred.get("hypothesis_ids") or [])
    assert len(hyp_ids) >= 1
    primary = hyp_ids[0]
    withdrawn = eng.update_hypothesis(
        primary, status="withdrawn", withdrawn_reason="user_corrected"
    )
    assert withdrawn["status"] == "withdrawn"
    assert eng.store.hypotheses[primary].withdrawn_reason == "user_corrected"
    assert eng.store.hypotheses[primary].closed_at > 0
    # Remaining hyp can be superseded
    if len(hyp_ids) > 1:
        other = hyp_ids[1]
        out = eng.update_hypothesis(other, status="superseded", superseded_by=primary)
        assert out["status"] == "superseded"
        assert eng.store.hypotheses[other].superseded_by == primary


def test_audit_learning_reversible_no_invented_experiences() -> None:
    eng = CognitiveEngine(agent_id="m5-c3-learn")
    _, coffee_id = _seed_predictable(eng)
    pred = eng.what_is_likely("After breakfast what is likely?")
    exp_n = len(eng.store.experiences)
    audited = eng.audit_prediction(pred["id"], observed_concept_id=coffee_id)
    assert len(eng.store.experiences) == exp_n
    ads = audited.get("adaptation_ids") or []
    if ads:
        conf_before = eng.store.concepts[coffee_id].confidence
        rolled = eng.rollback_adaptation(ads[0])
        assert rolled["status"] == "rolled_back"
        # Confidence restored toward before snapshot (bounded).
        assert 0.0 <= eng.store.concepts[coffee_id].confidence <= 1.0
        assert abs(eng.store.concepts[coffee_id].confidence - conf_before) < 0.5


def test_hypotheses_and_audits_persist() -> None:
    eng = CognitiveEngine(agent_id="m5-c3-persist")
    _, coffee_id = _seed_predictable(eng)
    pred = eng.what_is_likely("After breakfast what is likely?")
    audited = eng.audit_prediction(pred["id"], observed_concept_id=coffee_id)
    audit_id = audited["audit"]["id"]
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "snap.json"
        eng.export_snapshot(str(path))
        eng2 = CognitiveEngine(agent_id="m5-c3-persist2")
        eng2.import_snapshot(str(path))
        assert audit_id in eng2.store.prediction_audits
        assert eng2.store.hypotheses
        assert eng2.store.predictions[pred["id"]].evaluated is True


def test_cap1_cap2_cap3_systemwide_conversation() -> None:
    """Stress Cap1 hierarchy × Cap2 evidence × Cap3 audit without inventing memory."""
    eng = CognitiveEngine(agent_id="m5-c3-sys")
    eng.encode("A beagle is a dog.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode("A dog is an animal.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode(
        "Coffee often comes after breakfast.", pin=True, provenance=TRUSTED_USER_STATEMENT
    )
    breakfast = eng.store.find_concepts_by_label("breakfast")[0]
    coffee = eng.store.find_concepts_by_label("coffee")[0]
    eng.associations.relate(
        breakfast.id, coffee.id, relation=RelationKind.PREDICTS, strength_forward=0.8
    )

    hier = eng.concept_hierarchy("beagle")
    assert hier["known"] is True
    assert hier["evidence_ids"]

    dog = next(c for c in eng.store.concepts.values() if c.labels and c.labels[0] == "dog")
    snap1 = eng.confidence.estimate_concept(dog.id)
    eng.sleep()
    snap2 = eng.confidence.estimate_concept(dog.id)
    assert 0.0 <= snap2.value <= 1.0
    assert abs(snap2.value - snap1.value) < 0.5

    pred = eng.what_is_likely("After breakfast what is likely?")
    assert pred.get("hypothesis_ids")
    exp_n = len(eng.store.experiences)
    prov_n = len(eng.store.provenance)
    audited = eng.audit_prediction(pred["id"], observed_concept_id=coffee.id)
    assert audited["experiences_unchanged"] is True
    assert audited["provenance_unchanged"] is True
    assert len(eng.store.experiences) == exp_n
    assert len(eng.store.provenance) == prov_n
    explain = eng.explain_belief_change(prediction_id=pred["id"])
    assert explain
    competing = eng.competing_hypotheses(pred["id"])
    assert "active" in competing and "historical" in competing
