from __future__ import annotations

from acm import CognitiveEngine
from acm.associations import AssociationStage, CognitiveDistance, RelationKind
from acm.provenance import TRUSTED_USER_STATEMENT


def test_how_related_from_shared_experience() -> None:
    engine = CognitiveEngine(agent_id="asc")
    engine.encode("A husky is a dog.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    engine.encode("Athena is a husky.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    result = engine.how_related("husky", "dog")
    assert result["question"] == "How is this related?"
    assert result["related"] is True
    assert result["links"] or result.get("mode") == "neighborhood"
    assert "related" in result["answer"].lower() or "near" in result["answer"].lower()


def test_association_emergence_and_strengthening() -> None:
    engine = CognitiveEngine(agent_id="asc")
    for _ in range(4):
        engine.encode(
            "Fly tying and craftsmanship go together.", pin=True, provenance=TRUSTED_USER_STATEMENT
        )
    obs = engine.associations.observables()
    assert obs["association_count"] >= 1
    assert obs["births"] >= 1
    # Repeated co-activation should reinforce
    before = obs["strengthenings"]
    engine.encode(
        "Fly tying and craftsmanship go together.", pin=True, provenance=TRUSTED_USER_STATEMENT
    )
    after = engine.associations.observables()["strengthenings"]
    assert after >= before


def test_asymmetric_is_a_traffic() -> None:
    engine = CognitiveEngine(agent_id="asc")
    engine.encode("A labrador is a dog.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    ties = [
        a for a in engine.store.associations.values() if a.relation == RelationKind.IS_A_TRAFFIC
    ]
    assert ties
    edge = ties[0]
    assert edge.strength_forward > edge.strength_backward
    related = engine.how_related("labrador", "dog")
    assert related["related"] is True
    assert related.get("asymmetric") is True


def test_weakening_and_dormancy() -> None:
    engine = CognitiveEngine(agent_id="asc")
    engine.encode("Obscure widget pairs with gizmos.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    assocs = list(engine.store.associations.values())
    assert assocs
    target = assocs[0]
    for _ in range(12):
        engine.associations.weaken(target.id, amount=0.12)
    refreshed = engine.store.associations[target.id]
    assert refreshed.strength_forward < 0.25
    assert refreshed.stage in {AssociationStage.DORMANT, AssociationStage.NASCENT}
    assert refreshed.distance_band() in {
        CognitiveDistance.DORMANT,
        CognitiveDistance.WEAK,
        CognitiveDistance.FAR,
    }


def test_neighborhood_and_clusters() -> None:
    engine = CognitiveEngine(agent_id="asc")
    engine.encode("Woodworking is a craft.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    engine.encode("Fly tying is a craft.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    engine.encode("Tool use belongs with woodworking.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    craft = engine.what_is_this("craft")
    assert craft["seen_before"]
    neigh = engine.associations.neighborhood("craft", limit=10)
    assert isinstance(neigh, list)
    clusters = engine.associations.clusters(min_strength=0.2)
    assert isinstance(clusters, list)
    assert any(c["size"] >= 2 for c in clusters) or len(engine.store.associations) >= 2


def test_identity_and_goal_influence_stamps() -> None:
    engine = CognitiveEngine(agent_id="asc")
    engine.open_goal("Master fly tying", importance=0.9)
    engine.encode(
        "I am a craftsperson.",
        kind="identity",
        speaker="assistant",
        provenance=TRUSTED_USER_STATEMENT,
    )
    engine.encode(
        "Fly tying and craftsmanship share practice.", pin=True, provenance=TRUSTED_USER_STATEMENT
    )
    snap = engine.validation.snapshot()["association"]
    assert snap["births"] >= 1
    stamped = [
        a for a in engine.store.associations.values() if a.goal_influenced or a.identity_influenced
    ]
    assert stamped
    assert snap["goal_influenced"] >= 1 or snap["identity_influenced"] >= 1
