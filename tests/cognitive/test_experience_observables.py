from __future__ import annotations

from acm import CognitiveEngine


def test_harness_experience_metrics() -> None:
    engine = CognitiveEngine(agent_id="exobs")
    engine.open_goal("Observe experiences")
    first = engine.encode("I noticed a surprising result.", pin=True)
    engine.revise_experience(first["experience_id"], "Actually, the result was expected.")
    engine.experiences.touch(first["experience_id"])
    snap = engine.validation.snapshot()
    assert snap["schema"] == "acm.validation/0.8"
    assert snap["experience"]["births"] >= 2
    assert snap["experience"]["lineage"] >= 1
    assert snap["experience"]["temporal_links"] >= 1
    assert snap["experience"]["lifecycle"] >= 1
    assert snap["counts"]["experience_events"] >= 1


def test_salience_evolution_does_not_mutate_birth() -> None:
    engine = CognitiveEngine(agent_id="exobs")
    out = engine.encode("I asked a hard question about time?", pin=True)
    eid = out["experience_id"]
    birth = engine.store.experiences[eid].salience_birth.composite()
    engine.experiences.touch(eid, boost=0.2)
    after_birth = engine.store.experiences[eid].salience_birth.composite()
    assert after_birth == birth
    current = engine.experiences.current_salience(eid)
    assert current is not None
    assert current.composite() != birth or current.recency == 1.0


def test_long_running_experience_evolution() -> None:
    engine = CognitiveEngine(agent_id="exobs")
    ids: list[str] = []
    for i in range(25):
        out = engine.encode(f"Observation number {i} about sequencing.", pin=True)
        ids.append(out["experience_id"])
    # Reflect on an early event
    engine.reflect_on(ids[0], "I realized early ordering mattered.")
    events = engine.what_happened(limit=50, include_dormant=True)
    assert len(events) >= 26
    assert events[0]["sequence"] <= events[-1]["sequence"]
    obs = engine.experiences.observables()
    assert obs["experience_count"] >= 26
    assert obs["link_count"] >= 1
