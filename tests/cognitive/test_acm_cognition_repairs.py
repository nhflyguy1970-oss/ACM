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
    assert "from your evidence" not in spoken.lower()
    assert "from what you've shared" not in spoken.lower()
    assert spoken.lower().startswith("you caught")

    r, spoken = _speak(eng, "What fish did I catch?")
    assert r["status"] == "known"
    assert "trout" in spoken.lower()
    assert "you caught three trout" in spoken.lower()
    assert "•" not in spoken and not spoken.strip().startswith("-")


def test_duplicate_episodic_experiences_deduped() -> None:
    eng = _engine()
    for t in (
        "Yesterday I caught three trout.",
        "Yesterday I upgraded my RAM.",
        "Yesterday I upgraded my RAM.",
        "Yesterday I upgraded my RAM.",
        "Yesterday I upgraded my RAM.",
        "Yesterday I installed a second SSD.",
        "Yesterday I installed a second SSD.",
    ):
        eng.cognitive_respond(t)

    r, spoken = _speak(eng, "What happened yesterday?")
    assert r["status"] == "known"
    low = spoken.lower()
    assert low.count("you upgraded your ram yesterday") == 1
    assert low.count("you installed a second ssd yesterday") == 1
    assert low.count("you caught three trout yesterday") == 1

    r, spoken = _speak(eng, "What RAM did I upgrade?")
    assert r["status"] == "known"
    assert spoken.lower().count("you upgraded your ram yesterday") == 1


def test_natural_multi_event_presentation() -> None:
    eng = _engine()
    for t in (
        "Yesterday I caught three trout.",
        "Yesterday I upgraded my RAM.",
        "Yesterday I installed a second SSD.",
    ):
        assert "teaching_encoded" in (eng.cognitive_respond(t).get("reasoning_path") or [])

    r, spoken = _speak(eng, "What happened yesterday?")
    assert r["status"] == "known"
    low = spoken.lower()
    assert "trout" in low and "ram" in low and "ssd" in low
    assert "from your evidence" not in low
    assert "from what you've shared" not in low
    assert "you told me" not in low
    # Natural sentences, not evidence bullets
    assert "you caught three trout yesterday" in low
    assert "you upgraded your ram yesterday" in low
    assert "you installed a second ssd yesterday" in low
    assert not any(line.strip().startswith("-") for line in spoken.splitlines())


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
