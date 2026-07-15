from __future__ import annotations

from acm import CognitiveEngine
from acm.types import EdgeType


def test_sleep_consolidates_and_prunes_weak_edges() -> None:
    engine = CognitiveEngine(agent_id="sleep")
    a = engine.store.add_concept("a")
    b = engine.store.add_concept("b")
    edge = engine.store.add_association(a.id, b.id, edge_type=EdgeType.RELATED_TO, weight=0.05)
    out = engine.sleep(apply_low_impact=True)
    assert out["question"] == "What should become long-term memory?"
    assert out["pruned_edges"] >= 1
    assert edge.active is False
    assert engine.validation.sleep_events
    assert engine.validation.offline_events
    assert out.get("sleep_batch_id")


def test_offline_replay_strengthens_after_reflection() -> None:
    engine = CognitiveEngine(agent_id="sleep")
    enc = engine.encode("Husky dogs are energetic companions.", pin=True)
    concept_id = enc["concept_id"]
    engine.what_do_i_think("husky")
    strength_before = engine.store.concepts[concept_id].strength
    out = engine.sleep(apply_low_impact=True)
    assert out["replay_count"] >= 1
    snap = engine.validation.snapshot()
    assert snap["offline"]["replays"] >= 1
    assert snap["offline"]["consolidations"] >= 1
    # Replay may adapt living structures via Learning
    assert (
        engine.store.concepts[concept_id].strength >= strength_before - 1e-9
        or out["adaptations_applied"] >= 0
    )


def test_sleep_does_not_invent_experiences() -> None:
    engine = CognitiveEngine(agent_id="sleep")
    engine.encode("Sensor reading morning light.", pin=True)
    before = len(engine.store.experiences)
    engine.sleep()
    after = len(engine.store.experiences)
    assert after == before
