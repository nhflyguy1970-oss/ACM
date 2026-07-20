"""Standalone ACM repairs — episodic teaching/recall and preference cognition."""

from __future__ import annotations

from acm.api.engine import CognitiveEngine
from acm.authority.teaching import detect_teaching
from acm.semantic import extract_semantics
from acm.semantic.model import FactKind


def _engine() -> CognitiveEngine:
    return CognitiveEngine(agent_id="acm-cog-repair")


def _speak(eng: CognitiveEngine, text: str) -> tuple[dict, str]:
    r = eng.cognitive_respond(text)
    spoken = r.get("memory") or ""
    if r.get("status") == "unknown" and not spoken:
        spoken = "I don't currently know."
    return r, spoken


def test_caught_trout_teaching_and_recall() -> None:
    text = "Yesterday I caught three trout."
    facts = extract_semantics(text).facts
    assert any(f.kind == FactKind.EXPERIENCE and f.property == "caught" for f in facts)
    det = detect_teaching(text)
    assert det.is_teaching is True

    eng = _engine()
    r = eng.cognitive_respond(text)
    assert "teaching_encoded" in (r.get("reasoning_path") or [])

    r, spoken = _speak(eng, "What happened yesterday?")
    assert r["status"] == "known"
    assert "trout" in spoken.lower()

    r, spoken = _speak(eng, "What fish did I catch?")
    assert r["status"] == "known"
    assert "trout" in spoken.lower()


def test_where_did_i_go_temporal_recall() -> None:
    eng = _engine()
    r = eng.cognitive_respond("Last Friday I visited my brother.")
    assert "teaching_encoded" in (r.get("reasoning_path") or [])

    r, spoken = _speak(eng, "Where did I go last Friday?")
    assert r["status"] == "known", spoken
    low = spoken.lower()
    assert "brother" in low
    assert "visited" in low or "went" in low


def test_prefer_hooks_storage_and_recall() -> None:
    eng = _engine()
    r = eng.cognitive_respond("I prefer barbless hooks.")
    assert "teaching_encoded" in (r.get("reasoning_path") or [])

    # Preference concept attribute must exist (not only entity mentions).
    pref_attrs = []
    for c in eng.store.concepts.values():
        for a in c.attributes:
            if a.key.startswith("prefer_") or a.key == "preference":
                pref_attrs.append((a.key, a.value))
    assert pref_attrs, "prefer_* concept attribute missing"
    assert any("barbless" in v.lower() for _, v in pref_attrs)

    r, spoken = _speak(eng, "What kind of hooks do I prefer?")
    assert r["status"] == "known", spoken
    assert "barbless" in spoken.lower()
    assert "prefer" in spoken.lower()


def test_what_did_i_do_preserves_verb() -> None:
    eng = _engine()
    eng.cognitive_respond("Last Friday I visited my brother.")
    r, spoken = _speak(eng, "What did I do last Friday?")
    assert r["status"] == "known"
    assert "brother" in spoken.lower()
    assert "you do my brother" not in spoken.lower()


def test_harvested_and_observed_verbs_teach() -> None:
    for text, prop in (
        ("Yesterday I landed a brook trout.", "landed"),
        ("Yesterday I harvested tomatoes.", "harvested"),
        ("Yesterday I observed a bald eagle.", "observed"),
    ):
        facts = extract_semantics(text).facts
        assert any(f.kind == FactKind.EXPERIENCE and f.property == prop for f in facts), text
        assert detect_teaching(text).is_teaching is True, text
