"""B10 — Conversation-safe debugging (cognitive)."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.authority.debug_capture import (
    ConversationDebugPolicy,
    with_debug_enabled,
)
from acm.provenance import TRUSTED_USER_STATEMENT


def test_b10_disabled_by_default() -> None:
    eng = CognitiveEngine(agent_id="b10")
    eng.encode("My favorite color is blue.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    out = eng.debug_capture("What is my favorite color?")
    assert out["status"] == "disabled"
    assert out["invents_experiences"] is False


def test_b10_capture_zero_write_and_replay() -> None:
    eng = CognitiveEngine(
        agent_id="b10-on",
        conversation_debug_policy=with_debug_enabled(
            ConversationDebugPolicy(), enabled=True
        ),
    )
    eng.encode("My favorite color is blue.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    fp = eng.store_fingerprint()
    exp_n = len(eng.store.experiences)
    cap = eng.debug_capture("What is my favorite color?")
    assert cap["status"] == "captured"
    assert cap["store_unchanged"] is True
    assert cap["reconstruction"]["execution_mode"] == "read_only"
    assert eng.store_fingerprint() == fp
    assert len(eng.store.experiences) == exp_n
    mem1 = eng.cognitive_respond("What is my favorite color?")["memory"]
    for _ in range(5):
        eng.debug_capture("What is my favorite color?")
    mem2 = eng.cognitive_respond("What is my favorite color?")["memory"]
    assert mem1 == mem2
    replay = eng.debug_capture_replay("What is my favorite color?")
    assert replay["equivalent"] is True
    assert len(eng.debug_captures_recent()) >= 1


def test_b10_force_override_without_policy() -> None:
    eng = CognitiveEngine(agent_id="b10-force")
    eng.encode("I prefer tea.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    out = eng.debug_capture("What do I prefer?", force=True)
    assert out["status"] == "captured"
    assert out["store_unchanged"] is True
