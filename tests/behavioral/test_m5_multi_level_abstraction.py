"""M5 Cap4 — Multi-level abstraction & general principle formation."""

from __future__ import annotations

import tempfile
from pathlib import Path

from acm import CognitiveEngine
from acm.associations.model import RelationKind
from acm.concepts.model import AbstractionStatus, PrincipleModality
from acm.provenance import TRUSTED_USER_STATEMENT


def _hier_engine() -> CognitiveEngine:
    eng = CognitiveEngine(agent_id="m5-c4")
    eng.encode("A beagle is a dog.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode("A beagle is a dog.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode("A dog is an animal.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode("A dog is an animal.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    return eng


def test_insufficient_evidence_rejects_abstraction() -> None:
    eng = CognitiveEngine(agent_id="m5-c4-reject")
    eng.encode("Widget alpha exists.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    concept = next(c for c in eng.store.concepts.values() if c.evidence_ids)
    # Force single evidence only
    concept.evidence_ids = concept.evidence_ids[:1]
    out = eng.propose_abstraction(
        [concept.id],
        label="widget-gen",
        evidence_ids=concept.evidence_ids[:1],
    )
    assert out["status"] == "rejected"
    assert out["reason"] == "insufficient_evidence"
    assert len(eng.store.experiences) >= 1


def test_abstraction_candidate_promote_explain() -> None:
    eng = _hier_engine()
    beagle = next(c for c in eng.store.concepts.values() if c.labels and c.labels[0] == "beagle")
    dog = next(c for c in eng.store.concepts.values() if c.labels and c.labels[0] == "dog")
    evid = list(dict.fromkeys([*beagle.evidence_ids, *dog.evidence_ids]))[:4]
    assert len(evid) >= 2
    exp_n = len(eng.store.experiences)
    prov_n = len(eng.store.provenance)
    proposed = eng.propose_abstraction(
        [beagle.id, dog.id], label="dog", evidence_ids=evid
    )
    assert proposed["status"] == "candidate"
    aid = proposed["abstraction"]["id"]
    promoted = eng.concepts.promote_abstraction(aid)
    assert promoted["status"] == "active"
    explain = eng.explain_abstraction(aid)
    assert explain["known"] is True
    assert explain["revisable"] is True
    assert explain["invents_experiences"] is False
    assert explain["supporting_experiences"]
    assert len(eng.store.experiences) == exp_n
    assert len(eng.store.provenance) == prov_n
    levels = eng.abstraction_levels("beagle")
    assert levels["known"] is True
    assert levels["levels"]


def test_general_principle_is_probabilistic_not_absolute() -> None:
    eng = _hier_engine()
    beagle = next(c for c in eng.store.concepts.values() if c.labels[0] == "beagle")
    dog = next(c for c in eng.store.concepts.values() if c.labels[0] == "dog")
    evid = list(dict.fromkeys([*beagle.evidence_ids, *dog.evidence_ids]))
    abs_out = eng.propose_abstraction([beagle.id, dog.id], label="dog", evidence_ids=evid)
    eng.concepts.promote_abstraction(abs_out["abstraction"]["id"])
    principle = eng.form_general_principle(
        abs_out["abstraction"]["id"],
        modality="usually",
    )
    assert principle["status"] == "formed"
    assert principle["absolute"] is False
    assert principle["principle"]["modality"] == PrincipleModality.USUALLY.value
    assert "usually" in principle["principle"]["statement"].lower()
    assert 0.0 < principle["principle"]["confidence"] < 1.0


def test_refine_split_merge_retire_lifecycle() -> None:
    eng = _hier_engine()
    beagle = next(c for c in eng.store.concepts.values() if c.labels[0] == "beagle")
    dog = next(c for c in eng.store.concepts.values() if c.labels[0] == "dog")
    animal = next(c for c in eng.store.concepts.values() if c.labels[0] == "animal")
    evid = list(dict.fromkeys([*beagle.evidence_ids, *dog.evidence_ids, *animal.evidence_ids]))
    a = eng.propose_abstraction(
        [beagle.id, dog.id, animal.id], label="canine-line", evidence_ids=evid
    )
    aid = a["abstraction"]["id"]
    eng.concepts.promote_abstraction(aid)
    refined = eng.concepts.refine_abstraction(aid, add_evidence_ids=evid[:1])
    assert refined["status"] == "refined"
    split = eng.concepts.split_abstraction(
        aid, left_concept_ids=[beagle.id], right_concept_ids=[dog.id, animal.id]
    )
    assert split["status"] == "split"
    left_id = split["parts"][0]["id"]
    right_id = split["parts"][1]["id"]
    eng.concepts.promote_abstraction(left_id)
    eng.concepts.promote_abstraction(right_id)
    # Need enough evidence on both parts — ensure
    for part_id in (left_id, right_id):
        rec = eng.store.abstractions[part_id]
        if len(rec.supporting_experience_ids) < 2:
            rec.supporting_experience_ids = evid[:3]
    merged = eng.concepts.merge_abstractions(left_id, right_id, label="rejoined")
    assert merged["status"] == "merged"
    mid = merged["abstraction"]["id"]
    retired = eng.concepts.retire_abstraction(mid, reason="test_retire")
    assert retired["status"] == "retired"
    assert eng.store.abstractions[mid].status == AbstractionStatus.RETIRED
    # History preserved
    assert eng.store.abstractions[aid].status == AbstractionStatus.SPLIT


def test_prediction_audit_updates_abstraction_confidence() -> None:
    eng = CognitiveEngine(agent_id="m5-c4-audit")
    eng.encode(
        "Coffee often comes after breakfast.", pin=True, provenance=TRUSTED_USER_STATEMENT
    )
    eng.encode(
        "Coffee often comes after breakfast.", pin=True, provenance=TRUSTED_USER_STATEMENT
    )
    breakfast = eng.store.find_concepts_by_label("breakfast")[0]
    coffee = eng.store.find_concepts_by_label("coffee")[0]
    eng.associations.relate(
        breakfast.id, coffee.id, relation=RelationKind.PREDICTS, strength_forward=0.8
    )
    evid = list(dict.fromkeys([*breakfast.evidence_ids, *coffee.evidence_ids]))
    abs_out = eng.propose_abstraction(
        [breakfast.id, coffee.id], label="breakfast→coffee", evidence_ids=evid
    )
    aid = abs_out["abstraction"]["id"]
    eng.concepts.promote_abstraction(aid)
    before = eng.store.abstractions[aid].confidence
    pred = eng.what_is_likely("After breakfast what is likely?")
    audited = eng.audit_prediction(pred["id"], observed_concept_id=coffee.id)
    assert audited["status"] == "evaluated"
    after = eng.store.abstractions[aid].confidence
    if audited["comparison"] in {"hit", "partial"}:
        assert after >= before - 1e-9
    else:
        assert after <= before + 1e-9
    assert aid in eng.store.abstractions
    assert len(eng.store.abstractions[aid].prediction_audit_ids) >= 1 or after != before


def test_abstraction_persistence_roundtrip() -> None:
    eng = _hier_engine()
    beagle = next(c for c in eng.store.concepts.values() if c.labels[0] == "beagle")
    dog = next(c for c in eng.store.concepts.values() if c.labels[0] == "dog")
    evid = list(dict.fromkeys([*beagle.evidence_ids, *dog.evidence_ids]))
    out = eng.propose_abstraction([beagle.id, dog.id], label="dog", evidence_ids=evid)
    aid = out["abstraction"]["id"]
    eng.concepts.promote_abstraction(aid)
    eng.form_general_principle(aid, modality="tends")
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "snap.json"
        eng.export_snapshot(str(path))
        eng2 = CognitiveEngine(agent_id="m5-c4-load")
        eng2.import_snapshot(str(path))
        assert aid in eng2.store.abstractions
        assert eng2.store.general_principles


def test_cap1_cap2_cap3_cap4_systemwide() -> None:
    """Stress Cap1–Cap4 interactions without inventing memory."""
    eng = _hier_engine()
    eng.encode(
        "Coffee often comes after breakfast.", pin=True, provenance=TRUSTED_USER_STATEMENT
    )
    breakfast = eng.store.find_concepts_by_label("breakfast")[0]
    coffee = eng.store.find_concepts_by_label("coffee")[0]
    eng.associations.relate(
        breakfast.id, coffee.id, relation=RelationKind.PREDICTS, strength_forward=0.75
    )
    hier = eng.concept_hierarchy("beagle")
    assert hier["known"] is True
    eng.sleep()
    dog = next(c for c in eng.store.concepts.values() if c.labels[0] == "dog")
    snap = eng.confidence.estimate_concept(dog.id)
    assert 0.0 <= snap.value <= 1.0
    beagle = next(c for c in eng.store.concepts.values() if c.labels[0] == "beagle")
    evid = list(dict.fromkeys([*beagle.evidence_ids, *dog.evidence_ids]))
    abs_out = eng.propose_abstraction([beagle.id, dog.id], label="dog", evidence_ids=evid)
    eng.concepts.promote_abstraction(abs_out["abstraction"]["id"])
    eng.form_general_principle(abs_out["abstraction"]["id"], modality="commonly")
    pred = eng.what_is_likely("After breakfast what is likely?")
    exp_n = len(eng.store.experiences)
    audited = eng.audit_prediction(pred["id"], observed_concept_id=coffee.id)
    assert audited["experiences_unchanged"] is True
    assert len(eng.store.experiences) == exp_n
    explain = eng.explain_abstraction(abs_out["abstraction"]["id"])
    assert explain["known"] is True
    assert eng.explain_belief_change(prediction_id=pred["id"])
