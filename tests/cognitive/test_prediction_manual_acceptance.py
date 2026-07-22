"""Manual-acceptance regression for autobiographical Prediction (M11).

Teach recurring experiences → predict from memory → explain → conflict → unknown.
Does not introduce planners, world-model forecasting, or LLM speculation.
"""

from __future__ import annotations

from acm import CognitiveEngine
from acm.authority.classification import classify_memory_request
from acm.authority.taxonomy import CognitiveIntent
from acm.authority.teaching import detect_teaching


TEACHINGS = (
    "It has rained every day this week.",
    "Every time I drink coffee after 8 PM, I have trouble sleeping.",
    "Whenever I skip breakfast, I get hungry before lunch.",
    "Every Saturday I usually go fishing.",
    "I usually get more work done in the morning.",
    "Every weekend for the last year I have gone hiking.",
)


def test_declarative_habit_teachings_encode() -> None:
    engine = CognitiveEngine(agent_id="pred-accept-teach")
    for text in TEACHINGS:
        det = detect_teaching(text)
        assert det.is_teaching, text
        assert any(f.property == "predictive_pattern" for f in det.facts), text
        result = engine.cognitive_respond(text)
        assert "teaching_encoded" in result["reasoning_path"], text
    predictive = [
        e
        for e in engine.store.experiences.values()
        if (e.meta_dict() or {}).get("predictive") == "1"
    ]
    assert len(predictive) >= len(TEACHINGS)


def test_prediction_queries_classify_to_prediction() -> None:
    for cue in (
        "What am I likely to do next Saturday?",
        "When am I likely to be most productive?",
        "If I drink coffee after 8 PM, what is likely to happen?",
        "Why do you think that is likely?",
        "What will happen in the stock market tomorrow?",
        "Will it rain tomorrow?",
    ):
        cl = classify_memory_request(cue)
        assert cl.intent == CognitiveIntent.PREDICTION, cue
        assert cl.is_memory_request is True, cue


def test_habit_prediction_from_remembered_patterns() -> None:
    engine = CognitiveEngine(agent_id="pred-accept-habit")
    for text in TEACHINGS:
        engine.cognitive_respond(text)

    saturday = engine.cognitive_respond("What am I likely to do next Saturday?")
    assert saturday["intent"] == "prediction"
    assert saturday["status"] == "known"
    assert "fishing" in (saturday["memory"] or "").lower()
    assert "hiking" not in (saturday["memory"] or "").lower()

    productive = engine.cognitive_respond("When am I likely to be most productive?")
    assert productive["status"] == "known"
    assert "work" in (productive["memory"] or "").lower()

    rain = engine.cognitive_respond("Will it rain tomorrow?")
    assert rain["status"] == "known"
    assert "rain" in (rain["memory"] or "").lower()

    tomorrow = engine.cognitive_respond("What is likely to happen tomorrow?")
    assert tomorrow["status"] == "known"
    assert "rain" in (tomorrow["memory"] or "").lower()

    breakfast = engine.cognitive_respond(
        "If I skip breakfast, what is likely to happen?"
    )
    assert breakfast["status"] == "known"
    assert "hungry" in (breakfast["memory"] or "").lower()


def test_open_future_without_evidence_is_unknown() -> None:
    engine = CognitiveEngine(agent_id="pred-accept-bday")
    for text in TEACHINGS:
        engine.cognitive_respond(text)
    result = engine.cognitive_respond(
        "What am I likely to do on my birthday next year?"
    )
    assert result["intent"] == "prediction"
    assert result["status"] == "unknown"
    assert result["memory"] is None


def test_certainty_and_confidence_stay_in_prediction() -> None:
    engine = CognitiveEngine(agent_id="pred-accept-cert")
    for text in TEACHINGS:
        engine.cognitive_respond(text)
    definite = engine.cognitive_respond(
        "Will I definitely go fishing next Saturday?"
    )
    assert definite["intent"] == "prediction"
    assert "fishing" in (definite["memory"] or "").lower()
    conf = engine.cognitive_respond(
        "How confident are you that I'll go hiking this weekend?"
    )
    assert conf["intent"] == "prediction"
    assert "confidence" in (conf["memory"] or "").lower()
    assert "hiking" in (conf["memory"] or "").lower()


def test_explain_prediction_cites_teachings() -> None:
    engine = CognitiveEngine(agent_id="pred-accept-explain")
    engine.cognitive_respond("Every Saturday I usually go fishing.")
    engine.cognitive_respond("What am I likely to do next Saturday?")
    why = engine.cognitive_respond("How did you make that prediction?")
    assert why["intent"] == "prediction"
    assert "fishing" in (why["memory"] or "").lower()
    assert "taught" in (why["memory"] or "").lower() or "previously" in (
        why["memory"] or ""
    ).lower()


def test_unknown_outside_autobiographical_memory() -> None:
    engine = CognitiveEngine(agent_id="pred-accept-unknown")
    for text in TEACHINGS:
        engine.cognitive_respond(text)
    result = engine.cognitive_respond("What will happen in the stock market tomorrow?")
    assert result["intent"] == "prediction"
    assert result["status"] == "unknown"
    assert result["memory"] is None
    # Supporting organs must not fill Prediction's honest unknown.
    assert result["memory"] != engine.agent_id


def test_conflicting_evidence_reduces_confidence() -> None:
    engine = CognitiveEngine(agent_id="pred-accept-conflict")
    engine.cognitive_respond(
        "Every time I drink coffee after 8 PM, I have trouble sleeping."
    )
    engine.cognitive_respond("Coffee causes insomnia.")
    engine.cognitive_respond("Coffee sometimes helps me sleep.")
    result = engine.cognitive_respond(
        "If I drink coffee after 8 PM, what is likely to happen?"
    )
    assert result["status"] == "conflicting"
    memory = (result["memory"] or "").lower()
    assert "conflict" in memory
    assert "helps me sleep" in memory or "help" in memory
    assert result["confidence"] <= 0.45


def test_explainability_cites_supporting_teachings() -> None:
    engine = CognitiveEngine(agent_id="pred-accept-why")
    engine.cognitive_respond(
        "Every time I drink coffee after 8 PM, I have trouble sleeping."
    )
    engine.cognitive_respond("Coffee causes insomnia.")
    engine.cognitive_respond("Coffee sometimes helps me sleep.")
    engine.cognitive_respond("If I drink coffee after 8 PM, what is likely to happen?")
    why = engine.cognitive_respond("Why do you think that is likely?")
    assert why["intent"] == "prediction"
    memory = why["memory"] or ""
    assert "taught" in memory.lower() or "previously" in memory.lower()
    assert "coffee" in memory.lower()
    assert "trouble sleeping" in memory.lower() or "insomni" in memory.lower()


def test_repeated_support_increases_confidence() -> None:
    engine = CognitiveEngine(agent_id="pred-accept-conf")
    engine.cognitive_respond("Every Saturday I usually go fishing.")
    weak = engine.cognitive_respond("What am I likely to do next Saturday?")
    engine.cognitive_respond("Every Saturday I usually go fishing.")
    engine.cognitive_respond("Every Saturday I go fishing.")
    stronger = engine.cognitive_respond("What am I likely to do next Saturday?")
    assert weak["status"] == "known"
    assert stronger["status"] == "known"
    assert stronger["confidence"] >= weak["confidence"] - 1e-6
