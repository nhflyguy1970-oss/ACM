"""B21 learning certification — relationship presentation preserves governance (L31)."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_l31_relationship_presentation_read_only_and_isolated() -> None:
    eng = CognitiveEngine(
        agent_id="m-l31",
        assistant_identity={"name": "Aria", "role": "assistant"},
    )
    eng.encode("My name is Jeff.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode(
        "We collaborate on the ACM platform.",
        pin=True,
        provenance=TRUSTED_USER_STATEMENT,
    )
    before_exp = len(eng.store.experiences)
    before_prov = len(eng.store.provenance)
    out = eng.present_relationship_memory("How do we know each other?")
    assert out["status"] == "known"
    assert out["invents_experiences"] is False
    assert out["store_write"] is False
    assert len(eng.store.experiences) == before_exp
    assert len(eng.store.provenance) == before_prov
    # Simple identity unchanged
    who = eng.cognitive_respond("Who are you?")["memory"].lower()
    assert "jeff" not in who
    assert "collaborate" not in who
