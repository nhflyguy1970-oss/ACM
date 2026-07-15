from __future__ import annotations

from acm import CognitiveEngine


def test_recombination_analogy_observables() -> None:
    engine = CognitiveEngine(agent_id="raobs")
    engine.encode("Toolkit alpha calibration.", pin=True)
    engine.encode("Toolkit beta calibration.", pin=True)
    engine.what_new_memories_can_emerge("toolkit")
    engine.what_is_analogous("toolkit alpha", other="toolkit beta")
    snap = engine.validation.snapshot()
    assert snap["schema"] == "acm.validation/0.11"
    assert "recombination" in snap and "analogy" in snap
    blob = str(snap).lower()
    assert "chain of thought" not in blob
