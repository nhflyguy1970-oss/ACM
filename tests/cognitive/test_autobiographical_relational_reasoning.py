"""Autobiographical Relational Reasoning — standalone ACM certification."""

from __future__ import annotations

from acm.api.engine import CognitiveEngine
from acm.authority.classification import classify_memory_request
from acm.authority.teaching import detect_teaching
from acm.semantic import extract_semantics
from acm.semantic.model import FactKind


TEACHINGS = (
    "I upgraded my desktop to train larger AI models.",
    "My goal is to build the best local AI assistant possible.",
    "I'm building Aria to achieve that goal.",
    "BlackFly is part of my AI ecosystem.",
    "Aria uses ACM.",
    "I prefer local AI because I value privacy.",
    "I prefer Python.",
    "For systems programming I prefer Rust.",
)


def _engine() -> CognitiveEngine:
    return CognitiveEngine(agent_id="relational-autobio")


def _seed(engine: CognitiveEngine) -> None:
    for teaching in TEACHINGS:
        result = engine.cognitive_respond(teaching)
        assert "teaching_encoded" in (result.get("reasoning_path") or []), teaching


def _speak(engine: CognitiveEngine, text: str) -> tuple[dict, str]:
    result = engine.cognitive_respond(text)
    speech = result.get("memory") or ""
    if result.get("status") == "unknown" and not speech:
        speech = "I don't currently know."
    return result, speech


def test_relational_teaching_extraction() -> None:
    cases = (
        (
            "I upgraded my desktop to train larger AI models.",
            "desktop upgrade",
            "motivated_by",
            "train larger AI models",
        ),
        (
            "I'm building Aria to achieve that goal.",
            "Aria",
            "supports_goal",
            "current_goal",
        ),
        ("BlackFly is part of my AI ecosystem.", "BlackFly", "part_of", "AI ecosystem"),
        ("Aria uses ACM.", "Aria", "uses", "ACM"),
        (
            "I prefer local AI because I value privacy.",
            "local AI",
            "motivated_by",
            "privacy",
        ),
    )
    for text, source, relation, target in cases:
        assert detect_teaching(text).is_teaching is True, text
        facts = extract_semantics(text).facts
        assert any(
            fact.kind == FactKind.RELATIONSHIP
            and fact.relation_type == source
            and fact.property == relation
            and fact.value == target
            for fact in facts
        ), (text, facts)


def test_first_class_relationship_graph_has_evidence() -> None:
    engine = _engine()
    _seed(engine)

    learned = [
        association
        for association in engine.store.associations.values()
        if association.metadata.get("autobiographical")
    ]
    assert len(learned) >= 6
    assert all(association.evidence_ids for association in learned)
    learned_kinds = {
        association.metadata.get("learned_relation") for association in learned
    }
    assert {"motivated_by", "supports_goal", "part_of", "uses", "supports"} <= learned_kinds


def test_personal_why_and_goal_reasoning() -> None:
    engine = _engine()
    _seed(engine)

    result, speech = _speak(engine, "Why did I upgrade my desktop?")
    assert result["status"] == "known"
    assert "train larger ai models" in speech.lower()

    result, speech = _speak(engine, "What is my long-term goal?")
    assert result["status"] == "known"
    assert "best local ai assistant" in speech.lower()

    for question in (
        "Why am I building Aria?",
        "How does Aria relate to my goal?",
    ):
        result, speech = _speak(engine, question)
        assert result["status"] == "known"
        low = speech.lower()
        assert "aria" in low
        assert "building the best local ai assistant" in low


def test_project_relationships() -> None:
    engine = _engine()
    _seed(engine)

    result, speech = _speak(engine, "How are Aria and ACM related?")
    assert result["status"] == "known"
    assert "aria uses acm" in speech.lower()

    result, speech = _speak(engine, "How does BlackFly fit into my projects?")
    assert result["status"] == "known"
    low = speech.lower()
    assert "blackfly" in low and "ai ecosystem" in low


def test_motivated_preference_reasoning() -> None:
    engine = _engine()
    _seed(engine)

    result, speech = _speak(engine, "Why do I prefer local AI?")
    assert result["status"] == "known"
    low = speech.lower()
    assert "local ai" in low and "privacy" in low

    result, speech = _speak(engine, "Would cloud AI usually fit my preferences?")
    assert result["status"] == "known"
    low = speech.lower()
    assert "would not" in low
    assert "local ai" in low and "privacy" in low


def test_contextual_preferences_do_not_supersede_general_preference() -> None:
    engine = _engine()
    _seed(engine)

    result, speech = _speak(engine, "What programming language do I prefer?")
    assert result["status"] == "known"
    assert "python" in speech.lower()
    assert "rust" not in speech.lower()

    for question in (
        "What language do I prefer for systems programming?",
        "What programming language do I prefer for systems programming?",
    ):
        result, speech = _speak(engine, question)
        assert result["status"] == "known", (question, speech)
        low = speech.lower()
        assert "rust" in low and "systems programming" in low, (question, speech)
        assert "python" not in low, (question, speech)


def test_bounded_recommendation_reasoning() -> None:
    engine = _engine()
    _seed(engine)

    result, speech = _speak(
        engine, "Why is my desktop better for AI than my laptop?"
    )
    assert result["status"] == "known"
    low = speech.lower()
    assert "desktop" in low and "train larger ai models" in low

    result, speech = _speak(
        engine, "Which of my computers should I use for training AI?"
    )
    assert result["status"] == "known"
    low = speech.lower()
    assert "desktop" in low and "train larger ai models" in low


def test_unknown_motivations_and_unsupported_recommendation() -> None:
    engine = _engine()
    _seed(engine)

    for question in (
        "Why am I working on HouseFly?",
        "Which should I use for software development?",
        "Why did I buy my phone?",
    ):
        result, speech = _speak(engine, question)
        assert result["status"] == "unknown", (question, speech)
        assert speech == "I don't currently know."


def test_relational_questions_classified_as_memory() -> None:
    for question in (
        "Why did I upgrade my desktop?",
        "Why am I building Aria?",
        "How does Aria relate to my goal?",
        "How are Aria and ACM related?",
        "How does BlackFly fit into my projects?",
        "Would cloud AI usually fit my preferences?",
        "Which of my computers should I use for training AI?",
    ):
        classification = classify_memory_request(question)
        assert classification.is_memory_request is True, question
        assert classification.intent.value == "remembering", question


def test_previous_cognition_regression() -> None:
    engine = _engine()
    for teaching in (
        "My name is Jeffrey.",
        "My favorite color is green.",
        "Yesterday I caught three trout.",
        "My laptop runs Zorin.",
        "My laptop runs Fedora.",
        "I'm working on Aria.",
        "I'm building BlackFly.",
        "BlackFly is finished.",
        "My desktop has an RTX 4070.",
    ):
        engine.cognitive_respond(teaching)

    checks = (
        ("What is my name?", "jeffrey"),
        ("What is my favorite color?", "green"),
        ("What happened yesterday?", "trout"),
        ("What operating system does my laptop use?", "fedora"),
        ("What operating systems has my laptop used?", "zorin"),
        ("What projects am I working on?", "aria"),
    )
    for question, expected in checks:
        result, speech = _speak(engine, question)
        assert result["status"] == "known", (question, speech)
        assert expected in speech.lower(), (question, speech)

    _, projects = _speak(engine, "What projects am I working on?")
    assert "blackfly" not in projects.lower()
