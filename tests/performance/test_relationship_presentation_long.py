"""B21 long-duration — relationship presentation remains stable."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_long_duration_relationship_presentation_stable() -> None:
    eng = CognitiveEngine(
        agent_id="aria-b21-long",
        assistant_identity={"name": "Aria", "role": "assistant"},
    )
    eng.encode("My name is Jeff.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    for i in range(8):
        eng.encode(
            f"We are working on milestone {i} of ACM together.",
            pin=True,
            provenance=TRUSTED_USER_STATEMENT,
        )
        if i % 3 == 0:
            eng.sleep()
        rel = eng.cognitive_respond("How do we know each other?")
        assert rel["status"] == "known"
        mem = (rel.get("memory") or "").lower()
        assert "aria" in mem
        # Isolation holds across the run
        asst = eng.cognitive_respond("Who are you?")["memory"].lower()
        assert "jeff" not in asst
        assert "milestone" not in asst
