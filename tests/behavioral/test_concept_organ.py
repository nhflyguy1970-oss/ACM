from __future__ import annotations

from acm import CognitiveEngine
from acm.concepts import ConceptStage
from acm.provenance import TRUSTED_USER_STATEMENT
from acm.types import ConceptRole


def test_what_is_this_from_experience() -> None:
    engine = CognitiveEngine(agent_id="con")
    engine.encode("Zeus is a golden retriever.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    result = engine.what_is_this("zeus")
    assert result["question"] == "What is this?"
    assert result["seen_before"] is True
    assert result["confidence"] > 0.0
    assert "zeus" in result["answer"].lower() or "golden" in result["answer"].lower()


def test_concept_emergence_and_stabilization() -> None:
    engine = CognitiveEngine(agent_id="con")
    for _ in range(7):
        engine.encode(
            "My favorite coffee is dark roast.",
            kind="preference",
            provenance=TRUSTED_USER_STATEMENT,
        )
    prefs = [
        c
        for c in engine.store.concepts.values()
        if c.role == ConceptRole.PREFERENCE
        and any(a.key.startswith("favorite_coffee") and a.active for a in c.attributes)
    ]
    assert prefs
    concept = prefs[0]
    assert concept.stage in {
        ConceptStage.GROWING,
        ConceptStage.STABLE,
        ConceptStage.MATURE,
    }
    assert len(concept.evidence_ids) >= 5
    assert concept.confidence > 0.5
    meaning = engine.what_is_this("favorite coffee")
    assert meaning["seen_before"] is True


def test_abstraction_hierarchy() -> None:
    engine = CognitiveEngine(agent_id="con")
    engine.encode("Yasha is a labrador.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    engine.encode("Zeus is a golden retriever.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    engine.encode("A labrador is a dog.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    engine.encode("A golden retriever is a dog.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    dog = engine.what_is_this("dog")
    assert dog["seen_before"] is True
    assert dog["concept"]["labels"][0] == "dog"
    assert dog["hierarchy"]["children"] or dog["concept"]["child_ids"]
    assert engine.concepts.observables()["hierarchy_edges"] >= 1


def test_prototype_and_exemplars() -> None:
    engine = CognitiveEngine(agent_id="con")
    engine.encode(
        "I noticed a surprising terminal failure.", pin=True, provenance=TRUSTED_USER_STATEMENT
    )
    engine.encode(
        "I noticed a surprising terminal failure.", pin=True, provenance=TRUSTED_USER_STATEMENT
    )
    hit = engine.what_is_this("terminal")
    assert hit["seen_before"] is True
    assert hit["prototype"]["features"]
    assert hit["exemplars"]


def test_weakening_lifecycle() -> None:
    engine = CognitiveEngine(agent_id="con")
    out = engine.encode(
        "Obscure hapax phenomenon xyzzy.", pin=True, provenance=TRUSTED_USER_STATEMENT
    )
    cid = out["concept_id"]
    for _ in range(10):
        engine.concepts.weaken(cid, amount=0.12)
    concept = engine.store.concepts[cid]
    assert concept.strength < 0.4
    engine.encode(
        "Obscure hapax phenomenon xyzzy returns.", pin=True, provenance=TRUSTED_USER_STATEMENT
    )
    assert engine.store.concepts[cid].strength >= concept.strength
