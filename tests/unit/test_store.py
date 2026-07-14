from __future__ import annotations

from acm.core.store import CognitiveStore
from acm.types import EdgeType


def test_neighbors_and_goals() -> None:
    store = CognitiveStore()
    a = store.add_concept("coffee")
    b = store.add_concept("roast")
    store.add_association(a.id, b.id, edge_type=EdgeType.RELATED_TO, weight=0.8)
    nbrs = store.neighbors(a.id)
    assert len(nbrs) == 1
    assert nbrs[0][1].id == b.id
    g = store.add_goal("learn coffee")
    assert store.active_goals()[0].id == g.id
