"""Semantic Autobiographical Memory — standalone ACM certification tests."""

from __future__ import annotations

from acm.api.engine import CognitiveEngine
from acm.authority.classification import classify_memory_request
from acm.authority.teaching import detect_teaching
from acm.semantic import extract_semantics
from acm.semantic.model import FactKind


TEACHINGS = (
    "My laptop runs Zorin.",
    "My desktop runs Linux.",
    "I'm working on Aria.",
    "I'm building BlackFly.",
    "My desktop has an RTX 3060.",
    "I prefer local AI models.",
    "I like step-by-step debugging.",
)


def _engine() -> CognitiveEngine:
    return CognitiveEngine(agent_id="sem-autobio")


def _seed(eng: CognitiveEngine) -> None:
    for t in TEACHINGS:
        r = eng.cognitive_respond(t)
        assert "teaching_encoded" in (r.get("reasoning_path") or []), t


def _speak(eng: CognitiveEngine, text: str) -> tuple[dict, str]:
    r = eng.cognitive_respond(text)
    spoken = r.get("memory") or ""
    if r.get("status") == "unknown" and not spoken:
        spoken = "I don't currently know."
    return r, spoken


def test_possession_and_project_extraction() -> None:
    for text, kind, prop in (
        ("My laptop runs Zorin.", FactKind.POSSESSION, "os"),
        ("My desktop has an RTX 3060.", FactKind.POSSESSION, "gpu"),
        ("I'm working on Aria.", FactKind.PROJECT, "project"),
        ("I'm building BlackFly.", FactKind.PROJECT, "project"),
        ("I prefer local AI models.", FactKind.PREFERENCE, "prefer_ai"),
        ("I like step-by-step debugging.", FactKind.PREFERENCE, "prefer_debugging"),
    ):
        facts = extract_semantics(text).facts
        assert any(f.kind == kind and f.property == prop for f in facts), text
        assert detect_teaching(text).is_teaching is True, text


def test_semantic_personal_facts_recall() -> None:
    eng = _engine()
    _seed(eng)

    r, spoken = _speak(eng, "What operating system does my laptop use?")
    assert r["status"] == "known"
    assert "zorin" in spoken.lower() and "laptop" in spoken.lower()

    r, spoken = _speak(eng, "What projects am I working on?")
    assert r["status"] == "known"
    low = spoken.lower()
    assert "aria" in low and "blackfly" in low
    assert "project (project)" not in low

    r, spoken = _speak(eng, "What AI projects have I been building?")
    assert r["status"] == "known"
    assert "aria" in spoken.lower() or "blackfly" in spoken.lower()

    r, spoken = _speak(eng, "What graphics card is in my desktop?")
    assert r["status"] == "known"
    assert "3060" in spoken.lower()


def test_integrated_computer_and_ai_summaries() -> None:
    eng = _engine()
    _seed(eng)

    r, spoken = _speak(eng, "Tell me what you know about my computer.")
    assert r["status"] == "known"
    low = spoken.lower()
    assert "laptop" in low and "zorin" in low
    assert "desktop" in low and ("linux" in low or "3060" in low)
    assert "•" not in spoken
    assert "generic" not in low

    r, spoken = _speak(eng, "Tell me what you know about my AI setup.")
    assert r["status"] == "known"
    low = spoken.lower()
    assert "local" in low
    assert "aria" in low or "blackfly" in low


def test_preference_generalization() -> None:
    eng = _engine()
    _seed(eng)

    r, spoken = _speak(eng, "Do I prefer local AI models or cloud models?")
    assert r["status"] == "known"
    assert "local" in spoken.lower()
    assert "cloud" not in spoken.lower() or "prefer local" in spoken.lower()

    r, spoken = _speak(eng, "What kind of responses do I like when debugging?")
    assert r["status"] == "known"
    assert "step-by-step" in spoken.lower() or "debugging" in spoken.lower()

    r, spoken = _speak(eng, "What do I prefer?")
    assert r["status"] == "known"
    assert "local" in spoken.lower()


def test_autobiographical_summary() -> None:
    eng = _engine()
    _seed(eng)

    r, spoken = _speak(eng, "Summarize what you know about me.")
    assert r["status"] == "known"
    low = spoken.lower()
    assert "local" in low
    assert "aria" in low and "blackfly" in low
    assert "zorin" in low
    assert "3060" in low
    # Must not invent untaught facts
    assert "phone" not in low
    assert "64 gb" not in low


def test_cross_memory_reasoning() -> None:
    eng = _engine()
    _seed(eng)

    r, spoken = _speak(
        eng, "Which computer would probably be better for training larger AI models?"
    )
    assert r["status"] == "known"
    low = spoken.lower()
    assert "desktop" in low
    assert "3060" in low
    # No invented VRAM / world-knowledge filler
    assert "typically" not in low
    assert "in general" not in low


def test_unknown_boundary() -> None:
    eng = _engine()
    _seed(eng)

    r, spoken = _speak(eng, "What operating system does my phone use?")
    assert r["status"] == "unknown"
    assert spoken == "I don't currently know."


def test_contradiction_active_wins() -> None:
    eng = _engine()
    eng.cognitive_respond("My laptop runs Zorin.")
    eng.cognitive_respond("My laptop runs Ubuntu.")
    r, spoken = _speak(eng, "What operating system does my laptop use?")
    assert r["status"] == "known"
    assert "ubuntu" in spoken.lower()
    assert "zorin" not in spoken.lower()


def test_semantic_queries_classified_as_memory() -> None:
    for q in (
        "What operating system does my laptop use?",
        "What graphics card is in my desktop?",
        "Tell me what you know about my computer.",
        "Which computer would probably be better for training larger AI models?",
        "Summarize what you know about me.",
    ):
        c = classify_memory_request(q)
        assert c.is_memory_request is True, q


def test_m0_m1_regression_identity_pref_episodic() -> None:
    """Prior cognition remains intact alongside semantic autobiographical memory."""
    eng = _engine()
    for t in (
        "My name is Jeffrey.",
        "My favorite color is blue.",
        "My favorite color is green.",
        "Yesterday I caught three trout.",
        "Last Friday I visited my brother.",
    ):
        eng.cognitive_respond(t)

    r, spoken = _speak(eng, "What is my favorite color?")
    assert r["status"] == "known"
    assert "green" in spoken.lower()
    assert "blue" not in spoken.lower()

    r, spoken = _speak(eng, "What is my name?")
    assert r["status"] == "known"
    assert "jeffrey" in spoken.lower()

    r, spoken = _speak(eng, "What happened yesterday?")
    assert r["status"] == "known"
    assert "trout" in spoken.lower()
    assert spoken.lower().count("trout") == 1

    r, spoken = _speak(eng, "Where did I go last Friday?")
    assert r["status"] == "known"
    assert "brother" in spoken.lower()

    # Semantic still works in the same store
    eng.cognitive_respond("My laptop runs Zorin.")
    r, spoken = _speak(eng, "What operating system does my laptop use?")
    assert r["status"] == "known"
    assert "zorin" in spoken.lower()
