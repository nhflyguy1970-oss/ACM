"""M5 Cap6 learning certification — explainability (L21–L22)."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_l21_explain_learning_preserves_provenance_no_internals() -> None:
    eng = CognitiveEngine(agent_id="m5-l21")
    eng.encode("I prefer local AI models.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode("I prefer local AI models.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    exp_n = len(eng.store.experiences)
    prov_n = len(eng.store.provenance)
    concept = max(
        (c for c in eng.store.concepts.values() if c.evidence_ids),
        key=lambda c: len(c.evidence_ids),
    )
    e1 = eng.explain_learning(concept.id)
    e2 = eng.explain_learning(concept.id)
    assert e1["answer"] == e2["answer"]
    assert e1["exposes_internals"] is False
    assert "traceback" not in e1["answer"].lower()
    assert len(eng.store.experiences) == exp_n
    assert len(eng.store.provenance) == prov_n
    assert e1.get("provenance_ids") is not None or e1["supporting_experiences"]


def test_l22_explain_learning_tracks_confidence_change() -> None:
    eng = CognitiveEngine(agent_id="m5-l22")
    eng.encode("Rust is a programming language.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    concept = next(
        c for c in eng.store.concepts.values() if c.labels and "rust" in c.labels[0]
    )
    before = concept.confidence
    eng.confidence.evolve_from_learning(concept.id, reinforce=True)
    out = eng.explain_learning(concept.id)
    assert out["known"] is True
    assert out["confidence_history"] or out["confidence"] >= before - 1e-9
    assert out["has_evolved"] is True or len(out.get("confidence_history") or []) >= 1
