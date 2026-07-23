"""B04 — Conflict explanation names semantic competitors."""

from __future__ import annotations

from acm.api.engine import CognitiveEngine
from acm.concepts.model import ConceptRole
from acm.provenance import TRUSTED_USER_STATEMENT


def test_conflict_speech_names_competitors() -> None:
    eng = CognitiveEngine(agent_id="b04")
    eng.encode("My favorite color is blue.", kind="preference", provenance=TRUSTED_USER_STATEMENT)
    eng.encode(
        "My favourite colour is red.", kind="preference", provenance=TRUSTED_USER_STATEMENT
    )
    result = eng.cognitive_respond("What is my favorite color?")
    assert result["status"] == "conflicting"
    blob = ((result.get("memory") or "") + " " + eng.speak_cognitive_result(result)).lower()
    assert "conflict" in blob
    assert "blue" in blob
    assert "red" in blob


def test_inspect_conflict_lists_competing() -> None:
    eng = CognitiveEngine(agent_id="b04-inspect")
    eng.encode("My favorite color is blue.", kind="preference", provenance=TRUSTED_USER_STATEMENT)
    eng.encode(
        "My favourite colour is red.", kind="preference", provenance=TRUSTED_USER_STATEMENT
    )
    before = eng.store_fingerprint()
    view = eng.inspect_conflict("What is my favorite color?")
    assert eng.store_fingerprint() == before
    assert view["ambiguous"] is True or view["status"] == "conflicting"
    blob = (str(view.get("competing")) + " " + str(view.get("memory") or "")).lower()
    assert "blue" in blob
    assert "red" in blob
