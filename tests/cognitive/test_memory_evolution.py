"""Memory Evolution & Historical Reasoning — standalone ACM certification."""

from __future__ import annotations

from acm.api.engine import CognitiveEngine
from acm.authority.classification import classify_memory_request
from acm.authority.teaching import detect_teaching
from acm.semantic import extract_semantics
from acm.semantic.model import FactKind, UpdateOp


TEACHINGS = (
    "My laptop runs Zorin.",
    "My laptop runs Fedora.",
    "I prefer local AI models.",
    "I now prefer cloud AI models.",
    "I'm working on Aria.",
    "I'm building BlackFly.",
    "BlackFly is finished.",
    "I'm now working on HouseFly.",
    "My desktop has an RTX 3060.",
    "My desktop has an RTX 4070.",
    "I no longer use my laptop.",
    "My phone is a Pixel 10.",
)


def _engine() -> CognitiveEngine:
    return CognitiveEngine(agent_id="mem-evo")


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


def test_lifecycle_teaching_recognition() -> None:
    for text, kind, prop in (
        ("BlackFly is finished.", FactKind.PROJECT, "status"),
        ("I no longer use my laptop.", FactKind.POSSESSION, "status"),
        ("I now prefer cloud AI models.", FactKind.PREFERENCE, "prefer_ai"),
        ("I'm now working on HouseFly.", FactKind.PROJECT, "project"),
        ("I switched to Fedora.", FactKind.POSSESSION, "os"),
        ("I replaced my RTX 3060 with an RTX 4070.", FactKind.POSSESSION, "gpu"),
        ("My phone is a Pixel 10.", FactKind.POSSESSION, "model"),
        ("My truck is a Ford F-150.", FactKind.POSSESSION, "model"),
        ("My printer is an HP LaserJet.", FactKind.POSSESSION, "model"),
        ("My kayak is an Old Town Sportsman.", FactKind.POSSESSION, "model"),
    ):
        assert detect_teaching(text).is_teaching is True, text
        facts = extract_semantics(text).facts
        assert any(f.kind == kind and f.property == prop for f in facts), (text, facts)


def test_historical_os_lineage() -> None:
    eng = _engine()
    _seed(eng)

    r, spoken = _speak(eng, "What operating systems has my laptop used?")
    assert r["status"] == "known"
    low = spoken.lower()
    assert "zorin" in low and "fedora" in low

    r, spoken = _speak(eng, "What operating system does my laptop use?")
    assert r["status"] == "known"
    assert "fedora" in spoken.lower()


def test_active_vs_historical_projects() -> None:
    eng = _engine()
    _seed(eng)

    r, spoken = _speak(eng, "What projects am I working on?")
    assert r["status"] == "known"
    low = spoken.lower()
    assert "aria" in low and "housefly" in low
    assert "blackfly" not in low

    r, spoken = _speak(eng, "What projects have I worked on?")
    assert r["status"] == "known"
    low = spoken.lower()
    assert "aria" in low and "housefly" in low and "blackfly" in low


def test_preference_change_and_current() -> None:
    eng = _engine()
    _seed(eng)

    r, spoken = _speak(eng, "Do I prefer local AI or cloud AI?")
    assert r["status"] == "known"
    assert "cloud" in spoken.lower()

    r, spoken = _speak(eng, "Have my AI preferences changed?")
    assert r["status"] == "known"
    low = spoken.lower()
    assert "yes" in low and "local" in low and "cloud" in low


def test_hardware_change_detection() -> None:
    eng = _engine()
    _seed(eng)

    r, spoken = _speak(eng, "Has my desktop hardware changed?")
    assert r["status"] == "known"
    low = spoken.lower()
    assert "yes" in low and "3060" in low and "4070" in low


def test_computers_current_vs_historical() -> None:
    eng = _engine()
    _seed(eng)

    r, spoken = _speak(eng, "Tell me about my computers.")
    assert r["status"] == "known"
    low = spoken.lower()
    assert "current" in low and "historical" in low
    assert "desktop" in low and "4070" in low
    assert "laptop" in low
    assert "phone" not in low


def test_ai_setup_timeline() -> None:
    eng = _engine()
    _seed(eng)

    r, spoken = _speak(eng, "How has my AI setup changed over time?")
    assert r["status"] == "known"
    low = spoken.lower()
    assert "blackfly" in low and "finished" in low
    assert "housefly" in low
    assert "zorin" in low and "fedora" in low
    assert "3060" in low and "4070" in low
    assert "cloud" in low


def test_expanded_entity_ownership() -> None:
    eng = _engine()
    _seed(eng)

    r, spoken = _speak(eng, "What phone do I own?")
    assert r["status"] == "known"
    assert "pixel" in spoken.lower()

    r, spoken = _speak(eng, "What printer do I have?")
    assert r["status"] == "unknown"
    assert "don't currently know" in spoken.lower()


def test_evolution_queries_classified_as_memory() -> None:
    for q in (
        "Has my desktop hardware changed?",
        "Have my AI preferences changed?",
        "How has my AI setup changed over time?",
        "What operating systems has my laptop used?",
        "What projects have I worked on?",
        "Tell me about my computers.",
        "What phone do I own?",
    ):
        c = classify_memory_request(q)
        assert c.is_memory_request is True, q


def test_lifecycle_ops_are_revise_or_negate() -> None:
    fin = extract_semantics("BlackFly is finished.").facts[0]
    assert fin.update_op == UpdateOp.NEGATE
    now = extract_semantics("I now prefer cloud AI models.").facts[0]
    assert now.update_op == UpdateOp.REVISE


def test_prior_semantic_and_episodic_regression() -> None:
    eng = _engine()
    for t in (
        "My name is Jeffrey.",
        "My favorite color is blue.",
        "My favorite color is green.",
        "Yesterday I caught three trout.",
        "My laptop runs Zorin.",
    ):
        eng.cognitive_respond(t)

    r, spoken = _speak(eng, "What is my favorite color?")
    assert "green" in spoken.lower() and "blue" not in spoken.lower()

    r, spoken = _speak(eng, "What is my name?")
    assert "jeffrey" in spoken.lower()

    r, spoken = _speak(eng, "What happened yesterday?")
    assert "trout" in spoken.lower()
    assert spoken.lower().count("trout") == 1

    r, spoken = _speak(eng, "What operating system does my laptop use?")
    assert "zorin" in spoken.lower()
