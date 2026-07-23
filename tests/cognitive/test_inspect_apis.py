"""B08 — Non-mutating inspection API façades."""

from __future__ import annotations

import pytest

from acm.api.engine import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


@pytest.fixture
def eng() -> CognitiveEngine:
    e = CognitiveEngine(agent_id="test-b08")
    e.encode("My favorite color is blue.", provenance=TRUSTED_USER_STATEMENT)
    e.encode("My name is Jordan.", provenance=TRUSTED_USER_STATEMENT)
    return e


def test_inspect_reconstruction_zero_write(eng: CognitiveEngine) -> None:
    before = eng.store_fingerprint()
    view = eng.inspect_reconstruction("What is my favorite color?")
    assert view["schema"] == "acm.inspect.reconstruction.v1"
    assert view["execution_mode"] == "read_only"
    assert "blue" in (view.get("memory") or "").lower()
    assert eng.store_fingerprint() == before


def test_inspect_evidence_zero_write(eng: CognitiveEngine) -> None:
    before = eng.store_fingerprint()
    view = eng.inspect_evidence("What is my favorite color?")
    assert view["schema"] == "acm.inspect.evidence.v1"
    assert isinstance(view.get("supporting_experiences"), list)
    assert eng.store_fingerprint() == before


def test_inspect_confidence_zero_write(eng: CognitiveEngine) -> None:
    before = eng.store_fingerprint()
    view = eng.inspect_confidence("favorite color")
    assert view["schema"] == "acm.inspect.confidence.v1"
    assert view["execution_mode"] == "read_only"
    assert eng.store_fingerprint() == before


def test_inspect_identity_user_zero_write(eng: CognitiveEngine) -> None:
    before = eng.store_fingerprint()
    view = eng.inspect_identity(who="user")
    assert view["schema"] == "acm.inspect.identity.v1"
    assert view["who"] == "user"
    assert "jordan" in (view.get("memory") or "").lower()
    assert eng.store_fingerprint() == before


def test_inspect_conflict_zero_write(eng: CognitiveEngine) -> None:
    eng.encode("My favorite color is red.", provenance=TRUSTED_USER_STATEMENT)
    before = eng.store_fingerprint()
    view = eng.inspect_conflict("What is my favorite color?")
    assert view["schema"] == "acm.inspect.conflict.v1"
    assert eng.store_fingerprint() == before


def test_inspect_matches_pre_mutation_memory(eng: CognitiveEngine) -> None:
    """Façade memory equals a fresh inspect; normal respond may then mutate."""
    before = eng.store_fingerprint()
    a = eng.inspect("What is my favorite color?")
    b = eng.inspect_reconstruction("What is my favorite color?")
    assert a.get("memory") == b.get("memory")
    assert eng.store_fingerprint() == before
    eng.cognitive_respond("What is my favorite color?")
    assert eng.store_fingerprint() != before
