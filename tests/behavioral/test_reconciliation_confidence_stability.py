from __future__ import annotations

from acm import CognitiveEngine
from acm.associations.model import RelationKind


def test_long_running_reconciliation_confidence_cycle() -> None:
    engine = CognitiveEngine(agent_id="long-rcl")
    engine.encode("Harbor lights guide inbound ships.", pin=True)
    engine.encode("Harbor lights confuse inbound ships.", pin=True)
    a = [c for c in engine.store.concepts.values() if "harbor" in " ".join(c.labels).lower()]
    if len(a) >= 2:
        engine.associations.relate(a[0].id, a[1].id, RelationKind.CONFLICTS_WITH)
    elif len(a) == 1:
        other = next(
            c for c in engine.store.concepts.values()
            if not c.identity and c.id != a[0].id
        )
        engine.associations.relate(a[0].id, other.id, RelationKind.CONFLICTS_WITH)
    for i in range(8):
        before = len(engine.store.experiences)
        before_ids = set(engine.store.experiences)
        engine.how_should_memory_reconcile("harbor lights")
        engine.how_certain_am_i("harbor")
        # Reconciliation / confidence never birth or rewrite Experiences
        assert len(engine.store.experiences) == before
        assert set(engine.store.experiences) == before_ids
        if i % 3 == 0:
            # Reflective Experiences may be born by Reflection/Learning — expected
            engine.what_do_i_think("harbor")
            engine.learn(cue="harbor")
            engine.sleep()
    assert engine.store.reconciliations
    assert engine.validation.snapshot()["schema"] == "acm.validation/0.13"
    meta = engine.metacognitive_sketch()
    assert "reconciliation" in meta and "confidence" in meta
