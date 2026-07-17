"""Memory Authority — cognitive response pipeline & hallucinated recall prevention."""

from __future__ import annotations

import pytest

from acm.api.engine import CognitiveEngine
from acm.authority.classification import MemoryIntent, classify_memory_request
from acm.authority.result import CognitiveMemoryResult, MemoryStatus
from acm.authority.speak import speak_cognitive_result
from acm.provenance import TRUSTED_USER_STATEMENT


@pytest.fixture()
def eng(tmp_path):
    return CognitiveEngine(
        agent_id="aria",
        persist_path=str(tmp_path / "auth.db"),
        auto_persist=True,
    )


def test_classify_identity_and_remembering():
    who = classify_memory_request("Who are you?")
    assert who.is_memory_request is True
    assert who.intent == MemoryIntent.ASSISTANT_IDENTITY

    rem = classify_memory_request("What do you remember about coffee?")
    assert rem.is_memory_request is True
    assert rem.intent == MemoryIntent.REMEMBERING

    learned = classify_memory_request("What have you learned?")
    assert learned.intent == MemoryIntent.LEARNING

    non = classify_memory_request("Write a poem about the ocean")
    assert non.is_memory_request is False
    assert non.intent in {MemoryIntent.NOT_MEMORY, MemoryIntent.PROCEDURAL}


def test_known_memory_pipeline(eng: CognitiveEngine):
    eng.encode(
        "User favorite coffee is medium roast",
        kind="preference",
        pin=True,
        provenance=TRUSTED_USER_STATEMENT,
    )
    result = eng.cognitive_respond("What is my favorite coffee?")
    assert result["is_memory_request"] is True
    assert result["allow_encode_from_speech"] is False
    assert result["language_may_speak"] is True
    assert result["schema"] == "cognitive_memory_result.v1"
    # Prefer known or low_confidence with ACM content — never LM fill
    assert result["status"] in {
        MemoryStatus.KNOWN.value,
        MemoryStatus.LOW_CONFIDENCE.value,
        MemoryStatus.CONFLICTING.value,
    }
    speech = eng.speak_cognitive_result(result)
    assert "invent" not in speech.lower()
    if result["status"] == MemoryStatus.KNOWN.value:
        assert result["memory"]
        assert "coffee" in speech.lower() or "roast" in speech.lower()


def test_unknown_memory_is_knowledge(eng: CognitiveEngine):
    result = eng.cognitive_respond("What do you remember about my unicorn collection?")
    assert result["is_memory_request"] is True
    assert result["status"] in {
        MemoryStatus.UNKNOWN.value,
        MemoryStatus.INSUFFICIENT_EVIDENCE.value,
        MemoryStatus.LOW_CONFIDENCE.value,
    }
    assert result["memory"] is None
    speech = eng.speak_cognitive_result(result)
    assert speech
    assert any(
        phrase in speech.lower()
        for phrase in (
            "don't currently know",
            "enough experiences",
            "not confident",
            "don't yet",
        )
    )


def test_speak_never_invents_when_unknown():
    result = CognitiveMemoryResult(
        status=MemoryStatus.UNKNOWN,
        is_memory_request=True,
        intent="remembering",
        memory=None,
        confidence=0.0,
        language_may_speak=True,
    )
    speech = speak_cognitive_result(result)
    assert "don't currently know" in speech.lower()
    assert "unicorn" not in speech.lower()


def test_memory_protection_blocks_llm_tags(eng: CognitiveEngine):
    blocked = eng.encode(
        "I made up that the user loves pineapple pizza",
        kind="experience",
        context_tags=("llm_generated",),
        provenance=TRUSTED_USER_STATEMENT,
    )
    assert blocked.get("encoded") is False
    assert blocked.get("reason") == "memory_protection"

    blocked2 = eng.encode(
        "fabricated autobiography",
        kind="experience",
        external_kind="llm",
        provenance=TRUSTED_USER_STATEMENT,
    )
    assert blocked2.get("encoded") is False


def test_generated_response_isolation(eng: CognitiveEngine):
    """Speech about memories must not encode as Experience."""
    out = eng.encode(
        "As an AI language model I conclude your dog is named Spot",
        kind="experience",
        context_tags=("speech_output", "assistant_utterance"),
        provenance=TRUSTED_USER_STATEMENT,
    )
    assert out.get("encoded") is False
    # legitimate encode still works
    ok = eng.encode(
        "User dog is named River", kind="experience", pin=True, provenance=TRUSTED_USER_STATEMENT
    )
    assert ok.get("encoded") is True


def test_identity_recall_via_pipeline(eng: CognitiveEngine):
    result = eng.cognitive_respond("Who are you?")
    assert result["intent"] == MemoryIntent.ASSISTANT_IDENTITY.value
    assert result["is_memory_request"] is True
    assert any("classify" in step for step in result["reasoning_path"])
    assert any("who_am_i" in step or "owner:identity" in step for step in result["reasoning_path"])


def test_low_confidence_and_false_memory_prevention(eng: CognitiveEngine):
    # Neighborhood bleed: encode unrelated fact, ask distant question
    eng.encode(
        "Workspace uses Python 3.12", kind="experience", pin=True, provenance=TRUSTED_USER_STATEMENT
    )
    result = eng.cognitive_respond("What is my mother's birthday?")
    assert result["is_memory_request"] is True
    # Must not invent a birthday
    speech = eng.speak_cognitive_result(result)
    assert "invent" not in speech.lower()
    if result["memory"]:
        mem = result["memory"].lower()
        known = MemoryStatus.KNOWN.value
        assert "birthday" not in mem or result["status"] != known
    else:
        assert result["status"] != MemoryStatus.KNOWN.value


def test_non_memory_request_skips_reconstruction(eng: CognitiveEngine):
    result = eng.cognitive_respond("Translate hello to French")
    assert result["status"] == MemoryStatus.NOT_MEMORY.value
    assert result["is_memory_request"] is False
    assert eng.speak_cognitive_result(result) == ""


def test_provenance_and_supporting_structure(eng: CognitiveEngine):
    eng.encode(
        "User prefers terse documentation",
        kind="preference",
        pin=True,
        provenance=TRUSTED_USER_STATEMENT,
    )
    result = eng.cognitive_respond("What are my documentation preferences?")
    assert "supporting_concepts" in result
    assert "reasoning_path" in result
    assert result["allow_encode_from_speech"] is False


def test_learning_and_reflection_routes(eng: CognitiveEngine):
    learned = eng.cognitive_respond("What have you learned?")
    assert learned["is_memory_request"] is True
    assert learned["intent"] == MemoryIntent.LEARNING.value

    think = eng.cognitive_respond("How certain are you about that?")
    assert think["is_memory_request"] is True


def test_classify_request_engine_api(eng: CognitiveEngine):
    c = eng.classify_request("Do you remember my dog?")
    assert c["is_memory_request"] is True


def test_regression_remember_still_works(eng: CognitiveEngine):
    eng.encode(
        "Favorite tea is green tea", kind="preference", pin=True, provenance=TRUSTED_USER_STATEMENT
    )
    r = eng.remember("favorite tea")
    assert r.answer is not None
    assert r.confidence >= 0.0
