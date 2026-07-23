"""M5 Cap6 — Learning explainability (unified why-learned surface)."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.associations.model import RelationKind
from acm.provenance import TRUSTED_USER_STATEMENT


def test_explain_learning_covers_evidence_and_confidence() -> None:
    eng = CognitiveEngine(agent_id="m5-c6")
    eng.encode("My favorite tea is oolong.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode("My favorite tea is oolong.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    prefs = [
        c
        for c in eng.store.concepts.values()
        if any(a.key.startswith("favorite_tea") and a.active for a in c.attributes)
    ]
    assert prefs
    concept = prefs[0]
    exp_n = len(eng.store.experiences)
    out = eng.explain_learning(concept.id)
    assert out["known"] is True
    assert out["exposes_internals"] is False
    assert out["invents_experiences"] is False
    assert out["supporting_experiences"]
    assert "confidence" in out
    assert "why_exists" in out
    assert "module" not in out["answer"].lower()
    assert "organ" not in out["answer"].lower()
    assert "acm/" not in out["answer"].lower()
    assert len(eng.store.experiences) == exp_n
    # Deterministic
    assert eng.explain_learning(concept.id)["answer"] == out["answer"]


def test_explain_learning_includes_cap_histories() -> None:
    eng = CognitiveEngine(agent_id="m5-c6-hist")
    eng.encode("A beagle is a dog.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode("A beagle is a dog.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode(
        "I usually drink coffee after breakfast.",
        pin=True,
        provenance=TRUSTED_USER_STATEMENT,
    )
    eng.encode(
        "I usually drink coffee after breakfast.",
        pin=True,
        provenance=TRUSTED_USER_STATEMENT,
    )
    beagle = next(c for c in eng.store.concepts.values() if c.labels and c.labels[0] == "beagle")
    dog = next(c for c in eng.store.concepts.values() if c.labels and c.labels[0] == "dog")
    evid = list(dict.fromkeys([*beagle.evidence_ids, *dog.evidence_ids]))
    abs_out = eng.propose_abstraction([beagle.id, dog.id], label="dog", evidence_ids=evid)
    eng.concepts.promote_abstraction(abs_out["abstraction"]["id"])
    breakfast = eng.store.find_concepts_by_label("breakfast")
    coffee = eng.store.find_concepts_by_label("coffee")
    if breakfast and coffee:
        eng.associations.relate(
            breakfast[0].id,
            coffee[0].id,
            relation=RelationKind.PREDICTS,
            strength_forward=0.7,
        )
        ids = list(eng.store.experiences.keys())
        eng.learning.observe_temporal_pattern(
            antecedent="breakfast",
            consequent="coffee",
            experience_id=ids[0],
            period_hint="morning",
        )
        pred = eng.what_is_likely("After breakfast what is likely?")
        eng.audit_prediction(pred["id"], observed_concept_id=coffee[0].id)
    out = eng.explain_learning("dog")
    assert out["known"] is True
    assert "abstraction_history" in out
    assert out["exposes_internals"] is False
    why = eng.why_was_this_learned("dog")
    assert why["answer"] == out["answer"]


def test_explain_learning_unknown_is_honest() -> None:
    eng = CognitiveEngine(agent_id="m5-c6-unk")
    out = eng.explain_learning("completely-unknown-xyz")
    assert out["known"] is False
    assert out["invents_experiences"] is False
