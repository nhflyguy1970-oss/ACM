from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_simulation_is_hypothetical_and_never_alters_history() -> None:
    engine = CognitiveEngine(agent_id="sim")
    engine.encode("A husky is a dog.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    engine.encode("Dogs enjoy snowy weather.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    before = len(engine.store.experiences)
    before_ids = set(engine.store.experiences)
    result = engine.what_futures_can_memory_imagine("husky in snow", branches=3)
    assert result["question"].startswith("What possible futures")
    assert result["hypothetical"] is True
    assert result["historical_experiences_created"] == 0
    assert result["experiences_unchanged"] is True
    assert result["plans"] is False
    assert len(engine.store.experiences) == before
    assert set(engine.store.experiences) == before_ids
    assert result["simulations"]
    for sim in result["simulations"]:
        assert sim["hypothetical"] is True
        assert sim["historical"] is False
        for step in sim["steps"]:
            assert step["hypothetical"] is True


def test_simulation_reuses_activation_and_prediction() -> None:
    engine = CognitiveEngine(agent_id="sim")
    engine.encode("Coffee after breakfast.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    result = engine.what_futures_can_memory_imagine("breakfast", branches=2)
    assert any(s.get("prediction_id") for s in result["simulations"])
    snap = engine.validation.snapshot()
    assert snap["simulation"]["simulations"] >= 1
    assert snap["counts"]["simulation_events"] >= 1
