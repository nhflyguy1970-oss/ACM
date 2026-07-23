"""B47 — Adjacent possession / relationship fact recall."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_b47_dog_name_recall_without_identity_pollution() -> None:
    eng = CognitiveEngine(
        agent_id="aria-b47",
        assistant_identity={"name": "Aria", "role": "assistant"},
    )
    eng.encode("My name is Jeff.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode("My dog's name is Zeus.", pin=True, provenance=TRUSTED_USER_STATEMENT)

    who = eng.cognitive_respond("Who am I?")
    assert "jeff" in (who.get("memory") or "").lower()
    assert "zeus" not in (who.get("memory") or "").lower()

    dog = eng.cognitive_respond("What's my dog's name?")
    assert dog["status"] == "known"
    mem = (dog.get("memory") or "").lower()
    assert "zeus" in mem
    assert mem.strip() != "jeff."
    assert "jeff" not in mem

    api = eng.present_possession_recall("What is my dog's name?")
    assert api["status"] == "known"
    assert "zeus" in (api.get("memory") or "").lower()
    assert api["pollutes_identity_speech"] is False


def test_b47_unknown_possession_honest() -> None:
    eng = CognitiveEngine(agent_id="b47-u")
    eng.encode("My name is Jeff.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    out = eng.cognitive_respond("What's my cat's name?")
    assert out["status"] in {"unknown", "known"}
    mem = (out.get("memory") or "").lower()
    assert "jeff" not in mem or "don't" in mem or "know" in mem
