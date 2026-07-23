"""B21 — Explicit relationship-memory presentation."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def _seed() -> CognitiveEngine:
    eng = CognitiveEngine(
        agent_id="aria-b21",
        assistant_identity={"name": "Aria", "role": "assistant"},
    )
    eng.encode("My name is Jeff.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode("My favorite color is blue.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode(
        "We are working on the ACM project together.",
        pin=True,
        provenance=TRUSTED_USER_STATEMENT,
    )
    return eng


def test_b21_simple_identity_stays_isolated() -> None:
    eng = _seed()
    who = eng.cognitive_respond("Who are you?")
    mem = (who.get("memory") or "").lower()
    assert "aria" in mem
    assert "jeff" not in mem
    assert "acm" not in mem
    assert "blue" not in mem
    user = eng.cognitive_respond("Who am I?")
    um = (user.get("memory") or "").lower()
    assert "jeff" in um
    assert "aria" not in um
    assert "acm project" not in um


def test_b21_relationship_queries_present_evidence() -> None:
    eng = _seed()
    rel = eng.cognitive_respond("How do we know each other?")
    assert rel["status"] == "known"
    assert rel["intent"] == "remembering"
    mem = (rel.get("memory") or "").lower()
    assert "aria" in mem
    assert "jeff" in mem or "acm" in mem
    api = eng.present_relationship_memory("How do we know each other?")
    assert api["status"] == "known"
    assert api["relationship_allowed"] is True
    assert api["invents_experiences"] is False
    assert api["store_write"] is False


def test_b21_learned_about_me_not_learning_organ_dump() -> None:
    eng = _seed()
    out = eng.cognitive_respond("What have you learned about me?")
    assert out["intent"] == "remembering"
    mem = (out.get("memory") or "").lower()
    assert "jeff" in mem or "blue" in mem
    assert "generalized pattern" not in mem
    assert "stabilized identity concept" not in mem


def test_b21_describe_relationship_not_not_memory() -> None:
    eng = _seed()
    out = eng.cognitive_respond("Describe our relationship.")
    assert out["status"] == "known"
    assert out["intent"] != "not_memory"
    assert out.get("memory")
