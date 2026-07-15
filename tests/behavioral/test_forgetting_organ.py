from __future__ import annotations

from acm import CognitiveEngine
from acm.forgetting import AccessibilityLevel
from acm.types import EdgeType


def test_cool_changes_accessibility_without_deleting_history() -> None:
    engine = CognitiveEngine(agent_id="forget")
    enc = engine.encode("Ephemeral sensor note about humidity.", pin=True)
    cid = enc["concept_id"]
    exp_id = enc["experience_id"]
    before_summary = engine.store.experiences[exp_id].summary
    before_n = len(engine.store.experiences)

    out = engine.cool_memory(cid, steps=3)
    assert out["deleted"] is False
    assert out["experiences_unchanged"] is True
    assert out["cooled"] is True
    assert len(engine.store.experiences) == before_n
    assert engine.store.experiences[exp_id].summary == before_summary
    level = engine.store.accessibility[cid]
    assert level in {
        AccessibilityLevel.LESS_ACCESSIBLE.value,
        AccessibilityLevel.DORMANT.value,
        AccessibilityLevel.RARELY_ACTIVATED.value,
        AccessibilityLevel.ARCHIVED.value,
        AccessibilityLevel.PRUNE_ELIGIBLE.value,
    }


def test_dormant_reactivates_on_strong_cue() -> None:
    engine = CognitiveEngine(agent_id="forget")
    enc = engine.encode("Woodworking chisel set storage tip.", pin=True)
    cid = enc["concept_id"]
    engine.cool_memory(cid, steps=4)
    assert engine.store.concepts[cid].active is False
    # Strong lexical cue should reactivate via remember path
    engine.remember("woodworking")
    assert engine.store.concepts[cid].active is True
    assert engine.store.accessibility[cid] in {
        AccessibilityLevel.LESS_ACCESSIBLE.value,
        AccessibilityLevel.ACCESSIBLE.value,
        AccessibilityLevel.HIGHLY_ACCESSIBLE.value,
    }


def test_sleep_delegates_association_cool_to_forgetting() -> None:
    engine = CognitiveEngine(agent_id="forget")
    a = engine.store.add_concept("alpha")
    b = engine.store.add_concept("beta")
    edge = engine.store.add_association(a.id, b.id, edge_type=EdgeType.RELATED_TO, weight=0.05)
    out = engine.sleep(apply_low_impact=True)
    assert out["pruned_edges"] >= 1
    assert edge.active is False
    assert engine.validation.forgetting_events
    harder = engine.what_should_be_harder_to_remember()
    assert harder["question"].startswith("What should become")
