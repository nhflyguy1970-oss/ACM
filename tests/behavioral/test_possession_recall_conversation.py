"""B47 permanent behavioral conversation — dog name vs Who am I."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_behavioral_dog_name_vs_who_am_i() -> None:
    eng = CognitiveEngine(
        agent_id="aria-b47-beh",
        assistant_identity={"name": "Aria", "role": "assistant"},
    )
    eng.encode("My name is Jeff.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode("My dog's name is Zeus.", pin=True, provenance=TRUSTED_USER_STATEMENT)

    assert "zeus" not in eng.cognitive_respond("Who am I?")["memory"].lower()
    dog = eng.cognitive_respond("What's my dog's name?")
    assert "zeus" in (dog.get("memory") or "").lower()
    assert "jeff" not in (dog.get("memory") or "").lower()
    asst = eng.cognitive_respond("Who are you?")["memory"].lower()
    assert "aria" in asst and "zeus" not in asst and "jeff" not in asst
