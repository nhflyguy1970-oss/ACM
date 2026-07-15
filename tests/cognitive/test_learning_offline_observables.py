from __future__ import annotations

from acm import CognitiveEngine


def test_learning_observables_in_harness() -> None:
    engine = CognitiveEngine(agent_id="lobs")
    engine.encode("My favorite tea is oolong.", kind="preference", pin=True)
    thought = engine.what_do_i_think("What is my favorite tea?")
    engine.learn(reflective_experience_id=thought["reflective_experience_id"])
    snap = engine.validation.snapshot()
    assert snap["schema"] == "acm.validation/0.8"
    assert snap["counts"]["learning_events"] >= 1
    assert "learning" in snap
    assert snap["learning"]["events"] >= 1


def test_offline_observables_in_harness() -> None:
    engine = CognitiveEngine(agent_id="oobs")
    engine.encode("Module gamma firmware update complete.", pin=True)
    engine.what_do_i_think("module gamma")
    engine.sleep()
    snap = engine.validation.snapshot()
    assert snap["counts"]["offline_events"] >= 1
    assert snap["offline"]["consolidations"] >= 1
    assert snap["counts"]["sleep_events"] >= 1


def test_no_prompts_in_learning_trace() -> None:
    engine = CognitiveEngine(agent_id="lobs")
    engine.encode("I enjoy fly tying.", kind="preference", pin=True)
    thought = engine.what_do_i_think("fly tying")
    engine.learn(reflective_experience_id=thought["reflective_experience_id"])
    snap = engine.validation.snapshot()
    blob = str(snap)
    for banned in ("chain of thought", "system prompt", "you are an AI"):
        assert banned not in blob.lower()
