"""Stabilization repairs for autobiographical relational reasoning."""

from __future__ import annotations

from acm.api.engine import CognitiveEngine


def _engine() -> CognitiveEngine:
    return CognitiveEngine(agent_id="relational-stabilization")


def _speak(engine: CognitiveEngine, text: str) -> tuple[dict, str]:
    result = engine.cognitive_respond(text)
    speech = result.get("memory") or ""
    if result.get("status") == "unknown" and not speech:
        speech = "I don't currently know."
    return result, speech


def test_contextual_programming_language_preference_selection() -> None:
    engine = _engine()
    for teaching in (
        "I prefer Python.",
        "For systems programming I prefer Rust.",
    ):
        result = engine.cognitive_respond(teaching)
        assert "teaching_encoded" in (result.get("reasoning_path") or []), teaching

    result, speech = _speak(engine, "What programming language do I prefer?")
    assert result["status"] == "known"
    assert "python" in speech.lower()
    assert "rust" not in speech.lower()

    result, speech = _speak(
        engine, "What programming language do I prefer for systems programming?"
    )
    assert result["status"] == "known"
    low = speech.lower()
    assert "rust" in low and "systems programming" in low
    assert "python" not in low


def test_repeated_identical_goal_teaching_reuses_single_active_goal() -> None:
    engine = _engine()
    teaching = "My goal is to build the best local AI assistant possible."
    for _ in range(2):
        result = engine.cognitive_respond(teaching)
        assert "teaching_encoded" in (result.get("reasoning_path") or [])

    titles = [goal.title for goal in engine.store.active_goals()]
    assert len(titles) == 1
    assert "best local ai assistant" in titles[0].lower()

    result, speech = _speak(engine, "What is my long-term goal?")
    assert result["status"] == "known"
    low = speech.lower()
    assert "best local ai assistant" in low
    assert low.count("best local ai assistant") == 1


def test_upgrade_explainability_cites_supporting_memory_not_unrelated_ram() -> None:
    engine = _engine()
    engine.cognitive_respond("Yesterday I upgraded my RAM.")
    engine.cognitive_respond("I upgraded my desktop to train larger AI models.")

    result, speech = _speak(engine, "Why did I upgrade my desktop?")
    assert result["status"] == "known"
    assert "train larger ai models" in speech.lower()

    result, speech = _speak(engine, "How did you know why I upgraded my desktop?")
    assert result["status"] == "known"
    low = speech.lower()
    assert "train larger ai models" in low
    assert "upgraded your desktop" in low or "upgraded my desktop" in low
    assert "ram" not in low
    assert "previously taught" in low or "remembered autobiographical" in low
