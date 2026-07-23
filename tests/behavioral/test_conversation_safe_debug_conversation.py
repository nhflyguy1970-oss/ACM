"""B10 permanent behavioral conversation — conversation-safe debugging."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.authority.debug_capture import ConversationDebugPolicy, with_debug_enabled
from acm.provenance import TRUSTED_USER_STATEMENT


def test_behavioral_debug_does_not_contaminate_preference_answer() -> None:
    """D045-class: debugging the question must not change the taught preference."""
    eng = CognitiveEngine(
        agent_id="b10-beh",
        conversation_debug_policy=with_debug_enabled(
            ConversationDebugPolicy(include_organ_view="learning"),
            enabled=True,
        ),
    )
    eng.encode("My favorite color is blue.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    baseline = eng.inspect("What is my favorite color?")
    fp = eng.store_fingerprint()
    for _ in range(8):
        cap = eng.debug_capture("What is my favorite color?")
        assert cap["store_unchanged"] is True
        assert cap["invents_experiences"] is False
    after = eng.inspect("What is my favorite color?")
    assert after["memory"] == baseline["memory"]
    assert after["confidence"] == baseline["confidence"]
    assert eng.store_fingerprint() == fp
    # Ordinary recall answer still recovers the preference
    spoken = eng.cognitive_respond("What is my favorite color?")
    assert "blue" in (spoken.get("memory") or "").lower()
