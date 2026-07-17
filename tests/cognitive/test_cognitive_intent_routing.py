"""Cognitive Intent Classification & Routing validation (D039)."""

from __future__ import annotations

import time

import pytest

from acm.api.engine import CognitiveEngine
from acm.authority.classification import classify_memory_request, classify_request
from acm.authority.routing import CognitiveRoutingEngine, ownership_for_intent
from acm.authority.taxonomy import ORGAN_NONE, CognitiveIntent
from acm.provenance import TRUSTED_USER_STATEMENT


@pytest.fixture()
def eng(tmp_path):
    return CognitiveEngine(
        agent_id="aria",
        persist_path=str(tmp_path / "intent.db"),
        auto_persist=True,
    )


# ---------------------------------------------------------------------------
# Classification matrix
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text,intent,is_mem",
    [
        ("Who are you?", CognitiveIntent.ASSISTANT_IDENTITY, True),
        ("Tell me about yourself", CognitiveIntent.ASSISTANT_IDENTITY, True),
        ("What's your name?", CognitiveIntent.ASSISTANT_IDENTITY, True),
        ("Who am I?", CognitiveIntent.USER_IDENTITY, True),
        ("What is my name?", CognitiveIntent.USER_IDENTITY, True),
        ("What do you know about me?", CognitiveIntent.AUTOBIOGRAPHY, True),
        ("What projects are we working on?", CognitiveIntent.PROJECT, True),
        ("What is our long-term goal?", CognitiveIntent.GOAL, True),
        ("What is our plan?", CognitiveIntent.GOAL, True),
        ("What are we working on?", CognitiveIntent.GOAL, True),
        ("How has your understanding changed?", CognitiveIntent.REFLECTION, True),
        ("What have you learned?", CognitiveIntent.LEARNING, True),
        ("What do you remember about fly tying?", CognitiveIntent.REMEMBERING, True),
        ("How are coffee and tea related?", CognitiveIntent.ASSOCIATION, True),
        ("What do you think about ACM?", CognitiveIntent.REFLECTION, True),
        ("How certain are you?", CognitiveIntent.CONFIDENCE, True),
        ("What is my favorite coffee?", CognitiveIntent.PREFERENCE, True),
        ("What happened yesterday?", CognitiveIntent.EXPERIENCE, True),
        ("What did we decide about the API?", CognitiveIntent.DECISION_HISTORY, True),
        ("Write a poem about the ocean", CognitiveIntent.PROCEDURAL, False),
        ("Translate hello to French", CognitiveIntent.GENERAL_KNOWLEDGE, False),
        ("Help me plan a vacation", CognitiveIntent.PLANNING, False),
        ("hello", CognitiveIntent.CONVERSATION_MANAGEMENT, False),
    ],
)
def test_classification_matrix(text, intent, is_mem):
    c = classify_memory_request(text)
    assert c.intent == intent, f"{text!r} → {c.intent} (expected {intent})"
    assert c.is_memory_request is is_mem


def test_who_am_i_not_assistant_who_am_i():
    """User identity must not be routed as assistant identity."""
    user = classify_request("Who am I?")
    assistant = classify_request("Who are you?")
    assert user.intent == CognitiveIntent.USER_IDENTITY
    assert assistant.intent == CognitiveIntent.ASSISTANT_IDENTITY
    assert user.ownership_hint == "identity"
    assert assistant.ownership_hint == "identity"


def test_uncertain_does_not_bypass_to_lm_for_self_referents():
    c = classify_memory_request("What about our earlier approach to this?")
    assert c.is_memory_request is True
    assert c.intent in {
        CognitiveIntent.GENERAL_MEMORY,
        CognitiveIntent.UNCERTAIN,
        CognitiveIntent.HISTORY,
    }


def test_bare_world_knowledge_not_forced_cognitive():
    c = classify_memory_request("What is the speed of light?")
    assert c.is_memory_request is False
    assert c.intent in {
        CognitiveIntent.GENERAL_KNOWLEDGE,
        CognitiveIntent.NOT_MEMORY,
    }


# ---------------------------------------------------------------------------
# Ownership / routing
# ---------------------------------------------------------------------------


def test_ownership_table_covers_cognitive_intents():
    for intent in CognitiveIntent:
        own = ownership_for_intent(intent)
        assert own.primary_organ
        if intent in {
            CognitiveIntent.PROCEDURAL,
            CognitiveIntent.REASONING,
            CognitiveIntent.PLANNING,
            CognitiveIntent.TOOL_REQUEST,
            CognitiveIntent.GENERAL_KNOWLEDGE,
            CognitiveIntent.CONVERSATION_MANAGEMENT,
            CognitiveIntent.NOT_MEMORY,
        }:
            assert own.primary_organ == ORGAN_NONE
        else:
            assert own.primary_organ != ORGAN_NONE


def test_routing_identity_organs(eng):
    router = CognitiveRoutingEngine(eng)
    a = router.decide("Who are you?")
    assert a.ownership.primary_organ == "identity"
    assert a.classification.intent == CognitiveIntent.ASSISTANT_IDENTITY

    u = router.decide("Who am I?")
    assert u.ownership.primary_organ == "identity"
    assert u.classification.intent == CognitiveIntent.USER_IDENTITY


def test_routing_project_and_goal(eng):
    router = CognitiveRoutingEngine(eng)
    p = router.decide("What projects are we working on?")
    assert p.classification.intent == CognitiveIntent.PROJECT
    assert p.ownership.primary_organ == "remembering"
    assert "experiences" in p.ownership.supporting_organs

    g = router.decide("What is our long-term goal?")
    assert g.classification.intent == CognitiveIntent.GOAL
    assert g.ownership.primary_organ == "goals"


def test_routing_reflection_learning_association(eng):
    router = CognitiveRoutingEngine(eng)
    assert router.decide("What do you think about memory?").ownership.primary_organ == "reflection"
    assert router.decide("What have you learned?").ownership.primary_organ == "learning"
    changed = router.decide("How has your understanding changed?")
    assert changed.ownership.primary_organ == "reflection"
    assert "learning" in changed.ownership.supporting_organs
    assert (
        router.decide("How are fly tying and camping related?").ownership.primary_organ
        == "associations"
    )


# ---------------------------------------------------------------------------
# End-to-end pipeline routing
# ---------------------------------------------------------------------------


def test_pipeline_assistant_identity(eng):
    result = eng.cognitive_respond("Who are you?")
    assert result["is_memory_request"] is True
    assert result["intent"] == CognitiveIntent.ASSISTANT_IDENTITY.value
    assert "owner:identity" in result["reasoning_path"] or "who_am_i" in result["reasoning_path"]
    speech = eng.speak_cognitive_result(result)
    assert speech
    assert "invent" not in speech.lower()


def test_pipeline_user_identity_does_not_claim_to_be_agent(eng):
    result = eng.cognitive_respond("Who am I?")
    assert result["intent"] == CognitiveIntent.USER_IDENTITY.value
    speech = eng.speak_cognitive_result(result).lower()
    assert "invent" not in speech
    assert result["classification"]["ownership"]["primary_organ"] == "identity"
    path_text = " ".join(result["reasoning_path"])
    assert "user_identity" in path_text or "user_identity_reconstruct" in path_text


def test_pipeline_goals(eng):
    eng.open_goal("Ship ACM cognitive intent classification", importance=0.9)
    result = eng.cognitive_respond("What is our long-term goal?")
    assert result["is_memory_request"] is True
    assert result["intent"] == CognitiveIntent.GOAL.value
    if result["status"] == "known":
        assert "goal" in (result["memory"] or "").lower() or "Ship ACM" in (result["memory"] or "")


def test_pipeline_projects(eng):
    eng.encode(
        "We are working on the ACM cognitive routing project",
        kind="experience",
        pin=True,
        provenance=TRUSTED_USER_STATEMENT,
    )
    result = eng.cognitive_respond("What projects are we working on?")
    assert result["is_memory_request"] is True
    assert result["intent"] == CognitiveIntent.PROJECT.value


def test_pipeline_learning(eng):
    result = eng.cognitive_respond("What have you learned?")
    assert result["intent"] == CognitiveIntent.LEARNING.value
    assert result["is_memory_request"] is True


def test_pipeline_understanding_change_is_reflection(eng):
    result = eng.cognitive_respond("How has your understanding changed?")
    assert result["intent"] == CognitiveIntent.REFLECTION.value
    assert result["is_memory_request"] is True
    speech = eng.speak_cognitive_result(result)
    assert not speech.strip().startswith("{")
    assert "'id':" not in speech


def test_pipeline_remembering(eng):
    eng.encode(
        "User practices fly tying on weekends",
        kind="experience",
        pin=True,
        provenance=TRUSTED_USER_STATEMENT,
    )
    result = eng.cognitive_respond("What do you remember about fly tying?")
    assert result["intent"] == CognitiveIntent.REMEMBERING.value
    assert result["is_memory_request"] is True


def test_false_routing_prevention_poem(eng):
    result = eng.cognitive_respond("Write a poem about the ocean")
    assert result["is_memory_request"] is False
    assert result["status"] == "not_memory"


def test_lm_never_owns_cognitive_question(eng):
    for q in (
        "Who are you?",
        "Who am I?",
        "What projects are we working on?",
        "What is our long-term goal?",
        "How has your understanding changed?",
        "What have you learned?",
    ):
        result = eng.cognitive_respond(q)
        assert result["is_memory_request"] is True, q
        assert result["status"] != "not_memory" or result["is_memory_request"] is True
        assert result.get("allow_encode_from_speech") is False


def test_route_request_api(eng):
    decision = eng.route_request("What have you learned?")
    assert decision["ownership"]["primary_organ"] == "learning"
    assert decision["classification"]["is_memory_request"] is True


def test_memory_authority_preserved_unknown(eng):
    result = eng.cognitive_respond("What do you remember about my unicorn collection?")
    assert result["is_memory_request"] is True
    speech = eng.speak_cognitive_result(result).lower()
    assert "unicorn" not in speech


def test_host_independence_classification_pure():
    """Classification requires no host, model, or store."""
    c = classify_memory_request("What is our long-term goal?")
    assert c.intent == CognitiveIntent.GOAL
    assert c.is_memory_request is True


def test_performance_classify_batch():
    questions = [
        "Who are you?",
        "Who am I?",
        "What projects are we working on?",
        "What is our long-term goal?",
        "How has your understanding changed?",
        "Write a poem",
    ] * 50
    t0 = time.perf_counter()
    for q in questions:
        classify_memory_request(q)
    elapsed = time.perf_counter() - t0
    # < 50ms per 300 classifications typical; allow generous CI bound
    assert elapsed < 2.0


def test_ambiguous_mixed_prefers_cognitive_when_self_referent():
    c = classify_memory_request("Can you explain what we decided earlier?")
    # Self/shared + cognitive → must not be NOT_MEMORY
    assert c.is_memory_request is True
