from __future__ import annotations

from acm import CognitiveEngine
from acm.types import EdgeType


def test_goal_open_complete(engine: CognitiveEngine) -> None:
    gid = engine.open_goal("Ship ACM foundation", importance=0.9)
    assert engine.store.active_goals()
    engine.complete_goal(gid)
    assert not engine.store.active_goals()


def test_sleep_prunes_weak_edges(engine: CognitiveEngine) -> None:
    a = engine.store.add_concept("a")
    b = engine.store.add_concept("b")
    edge = engine.store.add_association(a.id, b.id, edge_type=EdgeType.RELATED_TO, weight=0.05)
    out = engine.sleep(apply_low_impact=True)
    assert out["pruned_edges"] >= 1
    assert edge.active is False
    assert engine.validation.sleep_events
