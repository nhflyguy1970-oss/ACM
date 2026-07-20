"""M1 — Episodic autobiographical memory (standalone ACM certification)."""

from __future__ import annotations

from acm.api.engine import CognitiveEngine
from acm.authority.classification import classify_memory_request
from acm.authority.teaching import detect_teaching
from acm.semantic import extract_semantics
from acm.semantic.model import FactKind


TEACHINGS = (
    "Yesterday I bought a kayak.",
    "Yesterday I cleaned my garage.",
    "Last week I went fishing.",
    "This morning I installed a GPU.",
    "Last Tuesday I visited my brother.",
)


def _engine() -> CognitiveEngine:
    return CognitiveEngine(agent_id="m1-episodic")


def _seed_events(eng: CognitiveEngine) -> None:
    for t in TEACHINGS:
        r = eng.cognitive_respond(t)
        assert "teaching_encoded" in (r.get("reasoning_path") or []), t


def _speak(eng: CognitiveEngine, text: str) -> tuple[dict, str]:
    r = eng.cognitive_respond(text)
    if r.get("status") == "unknown":
        spoken = "I don't currently know."
    else:
        spoken = r.get("memory") or ""
    return r, spoken


def test_episodic_teachings_extract_and_detect() -> None:
    for t in TEACHINGS:
        facts = extract_semantics(t).facts
        assert any(f.kind == FactKind.EXPERIENCE for f in facts), t
        assert any(f.relation_type for f in facts), t
        det = detect_teaching(t)
        assert det.is_teaching is True, t
        assert det.reason == "declarative_facts_extracted"


def test_episodic_event_teaching_encodes_temporal_metadata() -> None:
    eng = _engine()
    _seed_events(eng)
    episodic = [
        e for e in eng.store.experiences.values() if e.meta_dict().get("episodic") == "1"
    ]
    assert len(episodic) == 5
    cues = {e.meta_dict().get("temporal_cue") for e in episodic}
    assert "yesterday" in cues
    assert "last_week" in cues
    assert "this_morning" in cues
    assert "last_tuesday" in cues
    actions = {e.meta_dict().get("event_action") for e in episodic}
    assert actions >= {"bought", "cleaned", "went", "installed", "visited"}
    # Temporal links exist between episodic neighbors
    assert len(eng.experiences.links) >= 2


def test_temporal_reconstruction() -> None:
    eng = _engine()
    _seed_events(eng)

    r, spoken = _speak(eng, "What happened yesterday?")
    assert r["status"] == "known"
    low = spoken.lower()
    assert "kayak" in low and "garage" in low

    r, spoken = _speak(eng, "What did I buy yesterday?")
    assert r["status"] == "known"
    assert "kayak" in spoken.lower()

    r, spoken = _speak(eng, "What did I clean yesterday?")
    assert r["status"] == "known"
    assert "garage" in spoken.lower()

    r, spoken = _speak(eng, "What happened last week?")
    assert r["status"] == "known"
    assert "fishing" in spoken.lower()

    r, spoken = _speak(eng, "What happened before buying the kayak?")
    assert r["status"] == "known"
    low = spoken.lower()
    assert "fishing" in low or "brother" in low
    assert "kayak" not in low or "before" in low

    r, spoken = _speak(eng, "What happened after cleaning the garage?")
    assert r["status"] == "known"
    assert "gpu" in spoken.lower()


def test_event_evidence_and_explanations() -> None:
    eng = _engine()
    _seed_events(eng)

    r, spoken = _speak(eng, "Show me the evidence.")
    assert r["status"] == "known"
    low = spoken.lower()
    assert "kayak" in low and "garage" in low and "fishing" in low
    assert "gpu" in low and "brother" in low
    # Provenance: original teaching wording present
    assert "yesterday i bought a kayak" in low

    r, spoken = _speak(eng, "Tell me about buying the kayak.")
    assert r["status"] == "known"
    assert "kayak" in spoken.lower()

    r, spoken = _speak(eng, "Explain what happened.")
    assert r["status"] == "known"
    assert "kayak" in spoken.lower() or "fishing" in spoken.lower()


def test_unknown_handling_no_invention() -> None:
    eng = _engine()
    _seed_events(eng)
    r, spoken = _speak(eng, "What happened last month?")
    assert r["status"] == "unknown"
    assert spoken == "I don't currently know."
    # Must not invent events
    assert "kayak" not in (r.get("memory") or "").lower()

    empty = _engine()
    r, spoken = _speak(empty, "What happened yesterday?")
    assert r["status"] == "unknown"
    assert spoken == "I don't currently know."


def test_episodic_queries_classified_as_experience() -> None:
    for q in (
        "What happened yesterday?",
        "What did I buy yesterday?",
        "What happened before buying the kayak?",
        "What happened after cleaning the garage?",
    ):
        c = classify_memory_request(q)
        assert c.is_memory_request is True, q
        assert c.intent.value == "experience", q


def test_episodic_does_not_mutate_on_recall() -> None:
    eng = _engine()
    _seed_events(eng)
    n = len(eng.store.experiences)
    for q in (
        "What happened yesterday?",
        "What did I buy yesterday?",
        "Show me the evidence.",
        "What happened last month?",
    ):
        eng.cognitive_respond(q)
    assert len(eng.store.experiences) == n


def test_m0_regression_preference_identity_explanation() -> None:
    """Certified M0 capabilities remain intact alongside episodic memory."""
    eng = _engine()
    for t in (
        "My name is Jeffrey.",
        "My favorite color is blue.",
        "My favorite color is green.",
        "My favorite food is pizza.",
    ):
        eng.cognitive_respond(t)

    r = eng.cognitive_respond("What is my favorite color?")
    assert r["status"] == "known"
    assert "green" in (r.get("memory") or "").lower()

    r = eng.cognitive_respond("What is my name?")
    assert r["status"] == "known"
    assert "jeffrey" in (r.get("memory") or "").lower()

    r = eng.cognitive_respond("Show me the evidence.")
    assert r["status"] == "known"
    text = (r.get("memory") or "").lower()
    assert "green" in text and "blue" in text

    r = eng.cognitive_respond("Why isn't blue active?")
    assert r["status"] == "known"
    text = (r.get("memory") or "").lower()
    assert "blue" in text and "green" in text

    r = eng.cognitive_respond("What do you know about me?")
    assert r["status"] == "known"
    text = (r.get("memory") or "").lower()
    assert "jeffrey" in text and "green" in text
    assert "blue" not in text  # active-only

    # Episodic still works in the same store
    eng.cognitive_respond("Yesterday I bought a kayak.")
    r = eng.cognitive_respond("What did I buy yesterday?")
    assert r["status"] == "known"
    assert "kayak" in (r.get("memory") or "").lower()
