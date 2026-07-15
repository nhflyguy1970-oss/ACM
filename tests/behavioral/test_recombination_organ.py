from __future__ import annotations

from acm import CognitiveEngine


def test_recombination_never_alters_history() -> None:
    engine = CognitiveEngine(agent_id="rcb")
    engine.encode("Fly tying uses feathers and thread.", pin=True)
    engine.encode("Woodworking uses chisels and wood.", pin=True)
    before = len(engine.store.experiences)
    before_ids = set(engine.store.experiences)
    result = engine.what_new_memories_can_emerge("craft tools", blends=3)
    assert result["question"].startswith("What new memories")
    assert result["historical_experiences_created"] == 0
    assert result["experiences_unchanged"] is True
    assert result["plans"] is False
    assert len(engine.store.experiences) == before
    assert set(engine.store.experiences) == before_ids
    assert result["recombinations"]
    for r in result["recombinations"]:
        assert r["recombined"] is True
        assert r["historical"] is False
        assert len(r["fragments"]) >= 2


def test_prediction_and_simulation_influence_recombination() -> None:
    engine = CognitiveEngine(agent_id="rcb")
    engine.encode("Breakfast precedes coffee.", pin=True)
    engine.encode("Coffee supports morning focus.", pin=True)
    result = engine.what_new_memories_can_emerge("morning coffee", blends=2)
    assert any(r.get("prediction_id") or r.get("simulation_id") for r in result["recombinations"])
    snap = engine.validation.snapshot()
    assert snap["schema"] == "acm.validation/0.11"
    assert snap["recombination"]["recombinations"] >= 1
