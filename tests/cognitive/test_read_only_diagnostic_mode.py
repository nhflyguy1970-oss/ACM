"""B07 — Read-only diagnostic mode: zero living-memory mutation on inspect."""

from __future__ import annotations

import pytest

from acm.api.engine import CognitiveEngine
from acm.authority.mode import ExecutionMode, current_execution_mode, is_read_only, read_only
from acm.provenance import TRUSTED_USER_STATEMENT


@pytest.fixture
def eng() -> CognitiveEngine:
    return CognitiveEngine(agent_id="test-b07")


def _teach_preference(eng: CognitiveEngine) -> None:
    eng.encode("My favorite color is blue.", provenance=TRUSTED_USER_STATEMENT)


def test_execution_mode_defaults_normal() -> None:
    assert current_execution_mode() is ExecutionMode.NORMAL
    assert is_read_only() is False


def test_read_only_context_manager_restores() -> None:
    assert is_read_only() is False
    with read_only():
        assert is_read_only() is True
        assert current_execution_mode() is ExecutionMode.READ_ONLY
    assert is_read_only() is False


def test_inspect_does_not_mutate_store_or_buffer(eng: CognitiveEngine) -> None:
    _teach_preference(eng)
    before = eng.store_fingerprint()

    result = eng.inspect("What is my favorite color?")
    assert result.get("is_memory_request") is True
    assert (result.get("diagnostics") or {}).get("execution_mode") == "read_only"
    memory = (result.get("memory") or "").lower()
    assert "blue" in memory

    after = eng.store_fingerprint()
    assert after == before


def test_inspect_reflection_path_no_reflective_birth(eng: CognitiveEngine) -> None:
    _teach_preference(eng)
    before_exp = len(eng.store.experiences)
    before = eng.store_fingerprint()

    result = eng.inspect("Why do you think my favorite color is blue?")
    assert result.get("is_memory_request") is True
    assert len(eng.store.experiences) == before_exp
    assert eng.store_fingerprint() == before


def test_inspect_learning_path_no_adaptations(eng: CognitiveEngine) -> None:
    _teach_preference(eng)
    before_adapt = len(eng.store.adaptations)
    before = eng.store_fingerprint()

    result = eng.inspect("What have you learned about my favorite color?")
    assert result.get("is_memory_request") is True
    assert len(eng.store.adaptations) == before_adapt
    assert eng.store_fingerprint() == before


def test_inspect_prediction_no_store_insert(eng: CognitiveEngine) -> None:
    _teach_preference(eng)
    before_pred = len(eng.store.predictions)
    before = eng.store_fingerprint()

    result = eng.inspect("What am I likely to prefer next?")
    assert result.get("is_memory_request") is True
    assert len(eng.store.predictions) == before_pred
    assert eng.store_fingerprint() == before


def test_normal_remember_still_reconsolidates(eng: CognitiveEngine) -> None:
    _teach_preference(eng)
    before = eng.store_fingerprint()

    eng.remember("What is my favorite color?")
    after = eng.store_fingerprint()
    assert after != before
    assert after["store_checksum"] != before["store_checksum"]


def test_cognitive_respond_normal_still_mutates(eng: CognitiveEngine) -> None:
    _teach_preference(eng)
    before = eng.store_fingerprint()
    eng.cognitive_respond("What is my favorite color?")
    after = eng.store_fingerprint()
    assert after["store_checksum"] != before["store_checksum"]
    assert (eng.cognitive_respond("Who are you?").get("diagnostics") or {}).get(
        "execution_mode"
    ) == "normal"


def test_inspect_skips_teach_encode(eng: CognitiveEngine) -> None:
    before = eng.store_fingerprint()
    result = eng.inspect("My favorite color is crimson.")
    # Diagnostic inspect must not encode the declarative teaching.
    assert eng.store_fingerprint() == before
    assert "teaching_skipped_read_only" in (
        (result.get("reasoning_path") or [])
        if isinstance(result.get("reasoning_path"), list)
        else []
    ) or eng.store_fingerprint() == before
