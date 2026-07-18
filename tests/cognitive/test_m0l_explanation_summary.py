"""M0L — memory explanation + active-only personal summary from certified lineage."""

from __future__ import annotations

from acm.api.engine import CognitiveEngine
from acm.authority.classification import classify_memory_request
from acm.provenance import TRUSTED_USER_TEACHING


def _engine() -> CognitiveEngine:
    return CognitiveEngine(agent_id="m0l")


def _seed(eng: CognitiveEngine) -> None:
    for t in (
        "My name is Jeffrey.",
        "My favorite color is blue.",
        "My favorite color is green.",
        "My favorite food is pizza.",
        "My favorite food is tacos.",
        "My favorite fish is brook trout.",
        "My favorite fish is brown trout.",
    ):
        eng.cognitive_respond(t)


def test_explanation_cues_classified_as_memory() -> None:
    for q in (
        "Why is green my favorite color?",
        "Why isn't blue active?",
        "What replaced pizza?",
        "Why is brown trout active?",
    ):
        c = classify_memory_request(q)
        assert c.is_memory_request is True, q
        assert c.intent.value == "remembering", q
        assert "memory_explanation_cue" in c.matched_signals, q


def test_definition_of_done_explanations_and_summary() -> None:
    eng = _engine()
    _seed(eng)

    r = eng.cognitive_respond("Why is green my favorite color?")
    assert r["status"] == "known"
    text = (r["memory"] or "").lower()
    assert "green" in text and "blue" in text
    assert "retired" in text or "replaced" in text or "later taught" in text
    assert r.get("uncertainty") is None

    r = eng.cognitive_respond("Why isn't blue active?")
    assert r["status"] == "known"
    text = (r["memory"] or "").lower()
    assert "blue" in text and "green" in text
    assert "retired" in text or "replaced" in text

    r = eng.cognitive_respond("What replaced pizza?")
    assert r["status"] == "known"
    text = (r["memory"] or "").lower()
    assert "tacos" in text and "pizza" in text

    r = eng.cognitive_respond("Why is brown trout active?")
    assert r["status"] == "known"
    text = (r["memory"] or "").lower()
    assert "brown trout" in text
    assert "brook trout" in text or "replaced" in text or "taught" in text

    r = eng.cognitive_respond("What do you know about me?")
    assert r["status"] == "known"
    text = (r["memory"] or "").lower()
    assert "jeffrey" in text
    assert "green" in text
    assert "tacos" in text
    assert "brown trout" in text
    # Active-only: retired values must not appear as current facts
    assert "blue" not in text
    assert "pizza" not in text
    assert "brook trout" not in text


def test_explanation_does_not_mutate_memory() -> None:
    eng = _engine()
    _seed(eng)
    n = len(eng.store.experiences)
    values_before = {
        (a.key, a.value, a.active)
        for c in eng.store.concepts.values()
        for a in c.attributes
        if a.key.startswith("favorite_")
    }
    for q in (
        "Why is green my favorite color?",
        "Why isn't blue active?",
        "What replaced pizza?",
        "Why is brown trout active?",
        "What do you know about me?",
    ):
        eng.cognitive_respond(q)
    assert len(eng.store.experiences) == n
    values_after = {
        (a.key, a.value, a.active)
        for c in eng.store.concepts.values()
        for a in c.attributes
        if a.key.startswith("favorite_")
    }
    assert values_before == values_after


def test_multi_domain_explanation_isolation() -> None:
    eng = _engine()
    _seed(eng)
    color = (eng.cognitive_respond("Why is green my favorite color?")["memory"] or "").lower()
    food = (eng.cognitive_respond("What replaced pizza?")["memory"] or "").lower()
    fish = (eng.cognitive_respond("Why is brown trout active?")["memory"] or "").lower()
    assert "green" in color and "pizza" not in color and "trout" not in color
    assert "tacos" in food and "green" not in food and "trout" not in food
    assert "brown trout" in fish and "pizza" not in fish and "green" not in fish
