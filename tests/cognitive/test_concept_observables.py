from __future__ import annotations

from acm import CognitiveEngine


def test_harness_concept_metrics() -> None:
    engine = CognitiveEngine(agent_id="cobs")
    engine.encode("Athena is a husky.", pin=True)
    engine.encode("A husky is a dog.", pin=True)
    engine.encode("Athena is a husky.", pin=True)
    snap = engine.validation.snapshot()
    assert snap["schema"] == "acm.validation/0.8"
    assert snap["concept"]["births"] >= 1
    assert snap["concept"]["nuclei"] >= 1
    assert snap["concept"]["strengthenings"] >= 1
    assert snap["concept"]["hierarchy"] >= 1 or snap["concept"]["abstraction"] >= 1
    assert snap["counts"]["concept_events"] >= 1


def test_long_running_concept_evolution() -> None:
    engine = CognitiveEngine(agent_id="cobs")
    for i in range(20):
        engine.encode(f"Observation about robotics module {i % 3}.", pin=True)
    for _ in range(5):
        engine.encode("Robotics module is a subsystem.", pin=True)
    obs = engine.concepts.observables()
    assert obs["concept_count"] >= 3
    assert obs["strengthenings"] >= 5
    meaning = engine.what_is_this("robotics")
    assert meaning["matches"] or meaning["seen_before"]


def test_identity_and_experience_interaction() -> None:
    engine = CognitiveEngine(agent_id="cobs")
    engine.encode("I am a concept cartographer.", kind="identity")
    engine.encode("Cartography is a craft.", pin=True)
    who = engine.who_am_i()
    assert "cartographer" in who["answer"].lower() or who["confidence"] >= 0
    what = engine.what_is_this("cartography")
    assert what["question"] == "What is this?"
    assert engine.validation.snapshot()["experience"]["births"] >= 2
