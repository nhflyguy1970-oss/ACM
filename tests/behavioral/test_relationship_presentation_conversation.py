"""B21 permanent behavioral conversation — relationship presentation."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_behavioral_relationship_vs_simple_identity_matrix() -> None:
    eng = CognitiveEngine(
        agent_id="aria-b21-beh",
        assistant_identity={"name": "Aria", "role": "assistant"},
    )
    eng.encode("My name is Jeff.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode(
        "We are building Aria Cognitive Memory together.",
        pin=True,
        provenance=TRUSTED_USER_STATEMENT,
    )

    simple_a = eng.cognitive_respond("Who are you?")
    assert "jeff" not in (simple_a.get("memory") or "").lower()
    assert "building" not in (simple_a.get("memory") or "").lower()

    simple_u = eng.cognitive_respond("Who am I?")
    assert "aria" not in (simple_u.get("memory") or "").lower()
    assert "building" not in (simple_u.get("memory") or "").lower()

    rel = eng.cognitive_respond("What have we worked on together?")
    assert rel["status"] == "known"
    low = (rel.get("memory") or "").lower()
    assert "building" in low or "aria cognitive memory" in low or "together" in low
