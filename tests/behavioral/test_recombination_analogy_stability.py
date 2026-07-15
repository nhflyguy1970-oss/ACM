from __future__ import annotations

from acm import CognitiveEngine


def test_long_running_recombination_analogy_cycle() -> None:
    engine = CognitiveEngine(agent_id="long-ra")
    engine.encode("Fly tying uses delicate tools.", pin=True)
    engine.encode("Woodworking uses sturdy tools.", pin=True)
    engine.encode("Sewing uses delicate tools.", pin=True)
    for i in range(8):
        before = len(engine.store.experiences)
        engine.what_new_memories_can_emerge("tools craft", blends=2)
        engine.what_is_analogous("fly tying", other="sewing")
        assert len(engine.store.experiences) == before  # recombine/analogy never birth
        if i % 3 == 0:
            engine.what_do_i_think("tools")
            engine.learn(cue="tools")
            engine.sleep()
    for r in engine.store.recombinations.values():
        assert r.historical is False
    snap = engine.validation.snapshot()
    assert snap["schema"] == "acm.validation/0.12"
    meta = engine.metacognitive_sketch()
    assert "recombination" in meta and "analogy" in meta
