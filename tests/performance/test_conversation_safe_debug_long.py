"""B10 long-duration — many debug captures leave store stable."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.authority.debug_capture import ConversationDebugPolicy, with_debug_enabled
from acm.provenance import TRUSTED_USER_STATEMENT


def test_long_duration_debug_captures_bounded() -> None:
    eng = CognitiveEngine(
        agent_id="b10-long",
        conversation_debug_policy=with_debug_enabled(
            ConversationDebugPolicy(max_captures=32), enabled=True
        ),
    )
    for i in range(20):
        eng.encode(
            f"Note {i}: coffee after breakfast.",
            pin=True,
            provenance=TRUSTED_USER_STATEMENT,
        )
    fp = eng.store_fingerprint()
    exp_n = len(eng.store.experiences)
    for _ in range(100):
        cap = eng.debug_capture("What happens after breakfast?")
        assert cap["store_unchanged"] is True
    assert eng.store_fingerprint() == fp
    assert len(eng.store.experiences) == exp_n
    assert len(eng.debug_captures_recent(50)) <= 32
