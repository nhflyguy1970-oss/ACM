from __future__ import annotations

from acm import CognitiveEngine


def test_attention_and_forgetting_observables() -> None:
    engine = CognitiveEngine(agent_id="afobs")
    enc = engine.encode("Favorite tea is oolong.", kind="preference", pin=True)
    engine.remember("tea")
    engine.cool_memory(enc["concept_id"], steps=2)
    engine.reactivate_memory(enc["concept_id"], steps=1)
    snap = engine.validation.snapshot()
    assert snap["schema"] == "acm.validation/0.12"
    assert snap["counts"]["attention_events"] >= 1
    assert snap["counts"]["forgetting_events"] >= 1
    assert snap["attention"]["allocations"] >= 1
    assert snap["forgetting"]["cools"] >= 1


def test_priority_affects_offline_replay_selection() -> None:
    engine = CognitiveEngine(agent_id="afobs")
    a = engine.encode("Module gamma firmware update.", pin=True)["concept_id"]
    b = engine.encode("Unrelated weather anecdote.", pin=True)["concept_id"]
    engine.attention.invest(a, delta=0.2, source="test", factors=["importance"])
    ranked = engine.attention.replay_candidates(limit=8)
    assert a in ranked
    # Higher priority tends to appear earlier
    if b in ranked:
        assert ranked.index(a) <= ranked.index(b)
    engine.what_do_i_think("module gamma")
    engine.sleep()
    snap = engine.validation.snapshot()
    assert snap["offline"]["consolidations"] >= 1
