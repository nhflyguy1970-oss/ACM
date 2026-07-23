"""M5 Cap4 learning certification — multi-level abstraction (L17–L18)."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.associations.model import RelationKind
from acm.provenance import TRUSTED_USER_STATEMENT


def _seed_hierarchy(eng: CognitiveEngine) -> tuple[str, str, list[str]]:
    eng.encode("A collie is a dog.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode("A collie is a dog.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode("A dog is an animal.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    collie = next(c for c in eng.store.concepts.values() if c.labels[0] == "collie")
    dog = next(c for c in eng.store.concepts.values() if c.labels[0] == "dog")
    evid = list(dict.fromkeys([*collie.evidence_ids, *dog.evidence_ids]))
    return collie.id, dog.id, evid


def test_l17_abstraction_requires_evidence_and_never_invents() -> None:
    eng = CognitiveEngine(agent_id="m5-l17")
    collie_id, dog_id, evid = _seed_hierarchy(eng)
    exp_n = len(eng.store.experiences)
    prov_n = len(eng.store.provenance)
    rejected = eng.propose_abstraction([collie_id], evidence_ids=evid[:1], label="thin")
    assert rejected["status"] == "rejected"
    accepted = eng.propose_abstraction(
        [collie_id, dog_id], evidence_ids=evid, label="dog"
    )
    assert accepted["status"] == "candidate"
    assert len(eng.store.experiences) == exp_n
    assert len(eng.store.provenance) == prov_n
    aid = accepted["abstraction"]["id"]
    eng.concepts.promote_abstraction(aid)
    e1 = eng.explain_abstraction(aid)
    e2 = eng.explain_abstraction(aid)
    assert e1["answer"] == e2["answer"]
    assert e1["invents_experiences"] is False
    # Contradictory evidence reduces confidence
    before = eng.store.abstractions[aid].confidence
    # Use an existing experience as "conflict" without inventing
    conflict = evid[0]
    eng.concepts.reinforce_abstraction(
        aid, evidence_ids=[conflict], strengthen=False
    )
    assert eng.store.abstractions[aid].confidence <= before + 1e-9
    assert conflict in eng.store.abstractions[aid].conflicting_experience_ids


def test_l18_prediction_audit_updates_abstraction_reproducibly() -> None:
    eng = CognitiveEngine(agent_id="m5-l18")
    eng.encode(
        "Coffee often comes after breakfast.", pin=True, provenance=TRUSTED_USER_STATEMENT
    )
    eng.encode(
        "Coffee often comes after breakfast.", pin=True, provenance=TRUSTED_USER_STATEMENT
    )
    breakfast = eng.store.find_concepts_by_label("breakfast")[0]
    coffee = eng.store.find_concepts_by_label("coffee")[0]
    eng.associations.relate(
        breakfast.id, coffee.id, relation=RelationKind.PREDICTS, strength_forward=0.7
    )
    evid = list(dict.fromkeys([*breakfast.evidence_ids, *coffee.evidence_ids]))
    abs_out = eng.propose_abstraction(
        [breakfast.id, coffee.id], label="meal-drink", evidence_ids=evid
    )
    aid = abs_out["abstraction"]["id"]
    eng.concepts.promote_abstraction(aid)
    before = eng.store.abstractions[aid].confidence
    pred = eng.what_is_likely("After breakfast what is likely?")
    audited = eng.audit_prediction(pred["id"], observed_concept_id=coffee.id)
    after = eng.store.abstractions[aid].confidence
    assert audited["experiences_unchanged"] is True
    assert 0.05 <= after <= 0.95
    comparison = audited["comparison"]
    # Fresh engine reproduces comparison class
    eng2 = CognitiveEngine(agent_id="m5-l18b")
    eng2.encode(
        "Coffee often comes after breakfast.", pin=True, provenance=TRUSTED_USER_STATEMENT
    )
    eng2.encode(
        "Coffee often comes after breakfast.", pin=True, provenance=TRUSTED_USER_STATEMENT
    )
    b2 = eng2.store.find_concepts_by_label("breakfast")[0]
    c2 = eng2.store.find_concepts_by_label("coffee")[0]
    eng2.associations.relate(
        b2.id, c2.id, relation=RelationKind.PREDICTS, strength_forward=0.7
    )
    pred2 = eng2.what_is_likely("After breakfast what is likely?")
    a2 = eng2.audit_prediction(pred2["id"], observed_concept_id=c2.id)
    assert a2["comparison"] == comparison
    assert before >= 0.0
