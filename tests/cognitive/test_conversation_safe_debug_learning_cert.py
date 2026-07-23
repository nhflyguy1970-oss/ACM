"""B10 learning certification — debug capture never invents memory (L26)."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.authority.debug_capture import ConversationDebugPolicy, with_debug_enabled
from acm.provenance import TRUSTED_USER_STATEMENT


def test_l26_debug_capture_never_invents_experiences() -> None:
    eng = CognitiveEngine(
        agent_id="m-l26",
        conversation_debug_policy=with_debug_enabled(
            ConversationDebugPolicy(), enabled=True
        ),
    )
    eng.encode("Stable debug matters.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    exp_n = len(eng.store.experiences)
    prov_n = len(eng.store.provenance)
    for _ in range(12):
        out = eng.debug_capture("Stable debug matters")
        assert out["status"] == "captured"
        assert out["store_unchanged"] is True
    replay = eng.debug_capture_replay("Stable debug matters")
    assert replay["equivalent"] is True
    assert len(eng.store.experiences) == exp_n
    assert len(eng.store.provenance) == prov_n
