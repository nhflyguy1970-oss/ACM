"""M0K — multi-domain preference isolation + evidence lineage reconstruction."""

from __future__ import annotations

from acm.api.engine import CognitiveEngine
from acm.authority.classification import classify_memory_request
from acm.provenance import TRUSTED_USER_TEACHING


def _engine() -> CognitiveEngine:
    return CognitiveEngine(agent_id="m0k")


def test_evidence_request_classified_as_memory() -> None:
    for q in (
        "Show me the evidence.",
        "Show the evidence for my favorite color.",
        "What is the evidence for my favorite food?",
    ):
        c = classify_memory_request(q)
        assert c.is_memory_request is True, q
        assert c.intent.value in ("remembering", "preference"), q


def test_multi_domain_preferences_independent() -> None:
    eng = _engine()
    assert eng.encode("My favorite color is blue.", provenance=TRUSTED_USER_TEACHING)["encoded"]
    assert eng.encode("My favorite food is pizza.", provenance=TRUSTED_USER_TEACHING)["encoded"]
    assert eng.encode(
        "My favorite fish is brook trout.", provenance=TRUSTED_USER_TEACHING
    )["encoded"]

    assert eng.cognitive_respond("What is my favorite color?")["memory"] == (
        "Your favorite color is blue."
    )
    assert eng.cognitive_respond("What is my favorite food?")["memory"] == (
        "Your favorite food is pizza."
    )
    assert eng.cognitive_respond("What is my favorite fish?")["memory"] == (
        "Your favorite fish is brook trout."
    )

    # Update color only — food and fish unchanged
    eng.encode("My favorite color is green.", provenance=TRUSTED_USER_TEACHING)
    assert eng.cognitive_respond("What is my favorite color?")["memory"] == (
        "Your favorite color is green."
    )
    assert eng.cognitive_respond("What is my favorite food?")["memory"] == (
        "Your favorite food is pizza."
    )
    assert eng.cognitive_respond("What is my favorite fish?")["memory"] == (
        "Your favorite fish is brook trout."
    )

    values = {
        (a.key, a.value, a.active)
        for c in eng.store.concepts.values()
        for a in c.attributes
        if a.key.startswith("favorite_")
    }
    assert ("favorite_color", "blue", False) in values
    assert ("favorite_color", "green", True) in values
    assert ("favorite_food", "pizza", True) in values
    assert ("favorite_fish", "brook trout", True) in values


def test_teaching_response_uses_matching_domain() -> None:
    """After teaching food, the teach response must not speak an unrelated domain."""
    eng = _engine()
    eng.encode("My favorite color is black.", provenance=TRUSTED_USER_TEACHING)
    r = eng.cognitive_respond("My favorite food is pizza.")
    assert "teaching_encoded" in r["reasoning_path"]
    assert r["memory"] == "Your favorite food is pizza."
    assert "color" not in (r["memory"] or "").lower()


def test_evidence_lineage_after_multiple_updates() -> None:
    eng = _engine()
    for color in ("blue", "green", "red", "purple", "black"):
        eng.encode(f"My favorite color is {color}.", provenance=TRUSTED_USER_TEACHING)
    eng.encode("My favorite food is pizza.", provenance=TRUSTED_USER_TEACHING)

    n = len(eng.store.experiences)
    er = eng.cognitive_respond("Show me the evidence.")
    assert er["status"] == "known"
    text = (er["memory"] or "").lower()
    assert "favorite color" in text
    for color in ("blue", "green", "red", "purple", "black"):
        assert color in text
    assert "retired" in text
    assert "active" in text
    assert "pizza" in text
    # Evidence never mutates
    assert len(eng.store.experiences) == n

    scoped = eng.cognitive_respond("Show the evidence for my favorite color.")
    scoped_text = (scoped["memory"] or "").lower()
    assert "favorite color" in scoped_text
    assert "black" in scoped_text
    assert "retired" in scoped_text
    # Active value still retrieves correctly
    assert eng.cognitive_respond("What is my favorite color?")["memory"] == (
        "Your favorite color is black."
    )


def test_multi_domain_restart(tmp_path) -> None:
    path = str(tmp_path / "m0k.db")
    eng = CognitiveEngine(agent_id="m0k", persist_path=path, auto_persist=True)
    eng.encode("My favorite color is blue.", provenance=TRUSTED_USER_TEACHING)
    eng.encode("My favorite food is pizza.", provenance=TRUSTED_USER_TEACHING)
    eng.encode("My favorite fish is brook trout.", provenance=TRUSTED_USER_TEACHING)
    eng.encode("My favorite color is green.", provenance=TRUSTED_USER_TEACHING)
    eng.flush()

    eng2 = CognitiveEngine(agent_id="m0k", persist_path=path, auto_persist=True)
    assert eng2.cognitive_respond("What is my favorite color?")["memory"] == (
        "Your favorite color is green."
    )
    assert eng2.cognitive_respond("What is my favorite food?")["memory"] == (
        "Your favorite food is pizza."
    )
    assert eng2.cognitive_respond("What is my favorite fish?")["memory"] == (
        "Your favorite fish is brook trout."
    )
