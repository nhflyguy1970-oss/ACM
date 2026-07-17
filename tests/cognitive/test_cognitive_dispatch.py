"""End-to-end Cognitive Dispatch validation (D040)."""

from __future__ import annotations

import time

import pytest

from acm.api.engine import CognitiveEngine
from acm.authority.dispatch import CognitiveDispatchEngine
from acm.authority.handlers import FORBIDDEN_TERMINALS, sanitize_cognitive_text
from acm.authority.taxonomy import CognitiveIntent
from acm.provenance import TRUSTED_USER_STATEMENT


@pytest.fixture()
def eng(tmp_path):
    return CognitiveEngine(
        agent_id="aria",
        persist_path=str(tmp_path / "dispatch.db"),
        auto_persist=True,
    )


def test_user_identity_does_not_return_assistant_identity(eng):
    eng.encode("User's name is Jeff", kind="identity", pin=True, provenance=TRUSTED_USER_STATEMENT)
    result = eng.cognitive_respond("Who am I?")
    assert result["intent"] == CognitiveIntent.USER_IDENTITY.value
    speech = eng.speak_cognitive_result(result).lower()
    assert "i am aria" not in speech
    diag = result.get("diagnostics") or {}
    assert diag.get("terminated_at") == "identity"
    assert diag.get("primary_organ") == "identity"
    path = " ".join(result.get("reasoning_path") or [])
    assert "user_identity" in path or "user_schema" in path or "terminate:identity" in path


def test_assistant_identity_terminates_at_identity(eng):
    result = eng.cognitive_respond("Who are you?")
    assert result["intent"] == CognitiveIntent.ASSISTANT_IDENTITY.value
    diag = result["diagnostics"]
    assert diag["terminated_at"] == "identity"
    assert diag["primary_organ"] == "identity"
    path = " ".join(result.get("reasoning_path") or [])
    assert "who_am_i" in path or "terminate:identity" in path
    # May be known or low-confidence — never infrastructure / never raw dump
    speech = eng.speak_cognitive_result(result)
    assert not speech.startswith("{")
    assert "memory_store" not in speech.lower()


def test_goal_dispatch_uses_cognitive_organs(eng):
    eng.open_goal("Ship cognitive dispatch", importance=0.9)
    result = eng.cognitive_respond("What is our long-term goal?")
    assert result["is_memory_request"] is True
    assert result["intent"] == CognitiveIntent.GOAL.value
    diag = result["diagnostics"]
    assert diag["terminated_at"] == "goals"
    assert diag["primary_organ"] == "goals"
    assert "remembering" in diag["supporting_organs"]
    speech = eng.speak_cognitive_result(result)
    assert "Ship cognitive dispatch" in speech or "goal" in speech.lower()


def test_goal_without_open_goals_still_cognitive(eng):
    result = eng.cognitive_respond("What is our long-term goal?")
    assert result["is_memory_request"] is True
    assert result["diagnostics"]["terminated_at"] == "goals"
    # May be unknown — but never Chat/Knowledge infrastructure
    assert result["diagnostics"]["infrastructure_role"] == "substrate_only"


def test_understanding_change_reflection_not_raw_storage(eng):
    eng.encode(
        "Learned that fly tying requires hackle",
        kind="experience",
        pin=True,
        provenance=TRUSTED_USER_STATEMENT,
    )
    result = eng.cognitive_respond("How has your understanding changed?")
    assert result["intent"] == CognitiveIntent.REFLECTION.value
    diag = result["diagnostics"]
    assert diag["terminated_at"] == "reflection"
    assert "learning" in diag["supporting_organs"]
    speech = eng.speak_cognitive_result(result)
    assert not speech.startswith("{")
    assert "'kind':" not in speech
    assert "adp_" not in speech


def test_learning_formatted_not_dict_dump(eng):
    result = eng.cognitive_respond("What have you learned?")
    assert result["intent"] == CognitiveIntent.LEARNING.value
    speech = eng.speak_cognitive_result(result)
    assert "'id':" not in speech
    assert not speech.startswith("{")
    assert result["diagnostics"]["terminated_at"] == "learning"


def test_project_remembering_association_terminals(eng):
    for q, terminal in (
        ("What projects are we working on?", "remembering"),
        ("What do you remember about coffee?", "remembering"),
        ("How are coffee and tea related?", "associations"),
    ):
        result = eng.cognitive_respond(q)
        assert result["is_memory_request"] is True, q
        assert result["diagnostics"]["terminated_at"] == terminal, q


def test_dispatch_diagnostics_complete(eng):
    outcome = eng.dispatch_request("Who are you?")
    record = outcome["record"]
    assert record["schema"] == "cognitive_dispatch.v1"
    assert record["intent"] == "assistant_identity"
    assert record["primary_organ"] == "identity"
    assert record["terminated_at"] == "identity"
    assert record["dispatch_path"]
    assert record["reconstruction_path"]
    assert record["infrastructure_role"] == "substrate_only"


def test_forbidden_infrastructure_terminals_blocked(eng):
    dispatcher = CognitiveDispatchEngine(eng)
    for bad in ("memory_store", "MemoryEngine", "vector_store", "language_model"):
        with pytest.raises(RuntimeError):
            dispatcher._assert_cognitive_terminal(bad)  # noqa: SLF001


def test_sanitize_rejects_adaptation_dump():
    assert sanitize_cognitive_text("{'id': 'adp_1', 'kind': 'generalize'}") is None
    assert sanitize_cognitive_text("I am aria.", agent_id="aria") is None
    assert sanitize_cognitive_text("Your name is Jeff.", agent_id="aria") == "Your name is Jeff."


def test_multi_organ_contributions_listed(eng):
    result = eng.cognitive_respond("How has your understanding changed?")
    contribs = result["diagnostics"].get("contributions") or []
    organs = {c.get("organ") for c in contribs}
    assert "reflection" in organs
    assert "learning" in organs or "experiences" in organs or "remembering" in organs


def test_host_independence_dispatch(tmp_path):
    eng = CognitiveEngine(agent_id="solo", persist_path=str(tmp_path / "solo.db"))
    r = eng.cognitive_respond("Who am I?")
    assert r["diagnostics"]["terminated_at"] == "identity"
    assert "memory_store" not in str(r["diagnostics"]).lower()


def test_performance_dispatch_batch(eng):
    questions = [
        "Who are you?",
        "Who am I?",
        "What is our long-term goal?",
        "How has your understanding changed?",
    ] * 20
    t0 = time.perf_counter()
    for q in questions:
        eng.cognitive_respond(q)
    assert time.perf_counter() - t0 < 8.0


def test_forbidden_set_covers_infrastructure():
    for name in (
        "memory_store",
        "memory_engine",
        "knowledge_engine",
        "search_engine",
        "database",
        "index",
        "vector_store",
        "cache",
        "provider",
        "language_model",
        "storage",
    ):
        assert name in FORBIDDEN_TERMINALS
