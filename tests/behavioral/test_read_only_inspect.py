"""Permanent behavioral conversation — B07 read-only inspect."""

from __future__ import annotations

from acm.api.engine import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_behavioral_inspect_favorite_color_zero_write():
    """Conversation: teach preference → inspect repeatedly → store unchanged → normal recall mutates."""
    eng = CognitiveEngine(agent_id="b07-behav")
    eng.encode("My favorite color is blue.", provenance=TRUSTED_USER_STATEMENT)

    before = eng.store_fingerprint()
    replies = []
    for cue in (
        "What is my favorite color?",
        "Why do you think my favorite color is blue?",
        "Show the evidence for my favorite color.",
        "What have you learned about my favorite color?",
    ):
        result = eng.inspect(cue)
        replies.append((cue, result.get("memory"), result.get("status")))
        assert eng.store_fingerprint() == before
        assert (result.get("diagnostics") or {}).get("execution_mode") == "read_only"

    # At least one inspect recovered blue without mutation.
    assert any("blue" in ((m or "").lower()) for _, m, _ in replies)

    eng.cognitive_respond("What is my favorite color?")
    assert eng.store_fingerprint() != before
