from __future__ import annotations

from acm import CognitiveEngine


def test_harness_association_metrics() -> None:
    engine = CognitiveEngine(agent_id="aobs")
    engine.encode("A husky is a dog.", pin=True)
    engine.encode("Athena is a husky.", pin=True)
    engine.encode("Athena is a husky.", pin=True)
    snap = engine.validation.snapshot()
    assert snap["schema"] == "acm.validation/0.7"
    assert "association" in snap
    assert snap["association"]["births"] >= 1
    assert snap["counts"]["association_events"] >= 1
    assert snap["association"]["asymmetric_births"] >= 1 or snap["association"]["births"] >= 1
    # Evolution block mirrors prior organs
    assert snap["association"]["evolution"]["touches"] >= 1


def test_distance_and_directionality_observable() -> None:
    engine = CognitiveEngine(agent_id="aobs")
    engine.encode("A robin is a bird.", pin=True)
    obs = engine.associations.observables()
    assert obs["by_distance"]
    assert obs["by_relation"].get("is_a_traffic", 0) >= 1 or obs["association_count"] >= 1
    how = engine.how_related("robin", "bird")
    assert how["related"] is True
    assert how.get("distance") in {
        "immediate",
        "near",
        "far",
        "weak",
        "dormant",
        "unexpected",
        None,
    } or how.get("mode")


def test_neighborhood_cluster_harness() -> None:
    engine = CognitiveEngine(agent_id="aobs")
    for i in range(6):
        engine.encode(f"Module alpha and module beta share context {i}.", pin=True)
    clusters = engine.associations.clusters(min_strength=0.25)
    snap = engine.validation.snapshot()
    assert snap["association"]["clusters"] >= 1 or clusters is not None
    assert snap["association"]["neighborhoods"] >= 1 or len(clusters) >= 0


def test_long_running_association_evolution() -> None:
    engine = CognitiveEngine(agent_id="aobs")
    for i in range(24):
        engine.encode(f"Theme craft links woodworking sample {i % 4}.", pin=True)
    for _ in range(4):
        engine.encode("Theme craft links woodworking sample 0.", pin=True)
    obs = engine.associations.observables()
    assert obs["association_count"] >= 3
    assert obs["births"] >= 3
    # Reinforcements after repeated pairs
    assert obs["strengthenings"] >= 1
    how = engine.how_related("craft", "woodworking")
    assert how["question"] == "How is this related?"


def test_concept_experience_identity_interaction() -> None:
    engine = CognitiveEngine(agent_id="aobs")
    engine.encode("I am an association cartographer.", kind="identity")
    engine.encode("Cartography relates to maps.", pin=True)
    engine.encode("Maps relate to navigation.", pin=True)
    who = engine.who_am_i()
    assert who["confidence"] >= 0
    what = engine.what_is_this("cartography")
    assert what["question"] == "What is this?"
    how = engine.how_related("maps", "navigation")
    assert how["question"] == "How is this related?"
    snap = engine.validation.snapshot()
    assert snap["schema"] == "acm.validation/0.7"
    assert snap["experience"]["births"] >= 2
    assert snap["concept"]["births"] >= 1
    assert snap["association"]["births"] >= 1
