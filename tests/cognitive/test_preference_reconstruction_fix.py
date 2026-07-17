"""D045 — Preference reconstruction fix: competitor admissibility.

Validates the correction described in docs/PREFERENCE_RECONSTRUCTION_FIX.md:
lexical support concepts (token nuclei, mentioned-only concepts) keep
supporting retrieval but never participate in ambiguity scoring, and lexical
metadata attributes are never rendered as cognitive answers. True semantic
conflicts still produce competing_recollections.
"""

from __future__ import annotations

from acm import CognitiveEngine
from acm.concepts.model import Concept
from acm.remembering.organ import LEXICAL_SUPPORT_KEYS, _answerable
from acm.types import Attribute, ConceptRole, ExplanationClass


def _engine() -> CognitiveEngine:
    return CognitiveEngine(agent_id="d045")


def _conversational_session(question_turns: int = 2) -> CognitiveEngine:
    """Teach once, then log the user's question repeatedly as conversation turns.

    Before D045 this deterministically manufactured the false conflict (the
    're-mention inflation' mechanism from PREFERENCE_CONFLICT_ANALYSIS.md).
    """
    eng = _engine()
    eng.encode("My favorite color is blue.", kind="preference")
    for _ in range(question_turns):
        eng.encode("What is my favorite color?")
    return eng


# ---------------------------------------------------------------------------
# Required behavioral matrix
# ---------------------------------------------------------------------------


def test_unknown_preference_stays_unknown() -> None:
    eng = _engine()
    result = eng.cognitive_respond("What is my favorite color?")
    assert result["status"] == "unknown"
    assert result["memory"] is None


def test_teach_store_retrieve_blue() -> None:
    eng = _engine()
    out = eng.encode("My favorite color is blue.", kind="preference")
    assert out["encoded"] is True
    result = eng.cognitive_respond("What is my favorite color?")
    assert result["status"] == "known"
    assert result["memory"] == "Your favorite color is blue."
    assert result["uncertainty"] is None


def test_repeated_identical_teach_no_conflict_no_duplicate() -> None:
    eng = _engine()
    eng.encode("My favorite color is blue.", kind="preference")
    eng.encode("My favorite color is blue.", kind="preference")
    result = eng.cognitive_respond("What is my favorite color?")
    assert result["status"] == "known"
    assert result["memory"] == "Your favorite color is blue."
    active = [
        a
        for c in eng.store.concepts.values()
        for a in c.attributes
        if a.key == "favorite_color" and a.active
    ]
    assert len(active) == 1


def test_preference_update_retires_old_value() -> None:
    eng = _engine()
    eng.encode("My favorite color is blue.", kind="preference")
    eng.encode("Actually, my favorite color is red.", kind="preference")
    result = eng.cognitive_respond("What is my favorite color?")
    assert result["status"] == "known"
    assert result["memory"] == "Your favorite color is red."
    values = {
        a.value: a.active
        for c in eng.store.concepts.values()
        for a in c.attributes
        if a.key == "favorite_color"
    }
    assert values["red"] is True
    assert values["blue"] is False


def test_lexical_support_concepts_never_produce_ambiguity() -> None:
    """The false-conflict session from the D045 investigation now stays known."""
    for turns in (1, 2, 3):
        eng = _conversational_session(question_turns=turns)
        reconstruction = eng.remembering.what_do_i_remember("What is my favorite color?")
        assert reconstruction.ambiguous is False, f"false ambiguity at {turns} turns"
        assert reconstruction.competing == []
        result = eng.cognitive_respond("What is my favorite color?")
        assert result["status"] == "known"
        assert result["uncertainty"] is None
        assert result["memory"] == "Your favorite color is blue."


def test_reported_behavioral_session_end_to_end() -> None:
    """The exact failing session from the investigation, replayed post-fix."""
    eng = _engine()
    fresh = eng.cognitive_respond("What is my favorite color?")
    assert fresh["status"] == "unknown"
    eng.encode("What is my favorite color?")
    eng.encode("My favorite color is blue.", kind="preference")
    eng.encode("My favorite color is blue.")  # teach turn also logged as experience
    asked = eng.cognitive_respond("What is my favorite color?")
    assert asked["status"] == "known"
    assert asked["memory"] == "Your favorite color is blue."
    evidence = eng.cognitive_respond("Show the evidence for my favorite color.")
    assert evidence["status"] == "known"
    assert evidence["uncertainty"] != "competing_recollections"


def test_true_semantic_conflict_still_reports_competing_recollections() -> None:
    """Two distinct stored semantic preference concepts genuinely compete."""
    eng = _engine()
    eng.encode("My favorite color is blue.", kind="preference")
    eng.encode("My favourite colour is red.", kind="preference")  # distinct concept/key
    reconstruction = eng.remembering.what_do_i_remember("What is my favorite color?")
    assert reconstruction.ambiguous is True
    assert reconstruction.competing
    rival = eng.store.concepts[reconstruction.competing[0].concept_id]
    # The rival is a semantic preference concept, not lexical noise.
    assert rival.role == ConceptRole.PREFERENCE
    assert reconstruction.competing[0].answer_preview == "Your favorite colour is red."
    result = eng.cognitive_respond("What is my favorite color?")
    assert result["status"] == "conflicting"
    assert result["uncertainty"] == "competing_recollections"


# ---------------------------------------------------------------------------
# Rendering + admissibility internals
# ---------------------------------------------------------------------------


def test_lexical_metadata_never_rendered_as_answer() -> None:
    """A mentioned-only concept must not render its surface form as an answer."""
    eng = _engine()
    concept = Concept(
        id="con_lexical_only",
        labels=["thing"],
        role=ConceptRole.ENTITY,
        attributes=[Attribute(key="mentioned", value="favorite", confidence=0.9)],
    )
    answer, expl, conf = eng.remembering._format_from_concept(
        "What is my favorite color?", concept, energy=1.0
    )
    assert answer == ""
    assert expl == ExplanationClass.UNKNOWN
    assert conf == 0.0


def test_answerability_rule() -> None:
    tokens = ["what", "favorite", "color"]
    lexical_only = Concept(
        id="c1",
        labels=["favorite"],
        attributes=[Attribute(key="mentioned", value="favorite")],
    )
    semantic = Concept(
        id="c2",
        labels=["favorite color"],
        role=ConceptRole.PREFERENCE,
        attributes=[Attribute(key="favorite_color", value="blue")],
    )
    mixed = Concept(
        id="c3",
        labels=["favorite color"],
        role=ConceptRole.PREFERENCE,
        attributes=[
            Attribute(key="mentioned", value="favorite"),
            Attribute(key="favorite_color", value="green"),
        ],
    )
    inactive = Concept(
        id="c4",
        labels=["favorite color"],
        attributes=[Attribute(key="favorite_color", value="blue", active=False)],
    )
    interrogative = Concept(
        id="c5",
        labels=["preference"],
        role=ConceptRole.PREFERENCE,
        attributes=[Attribute(key="preference", value="What is my favorite color?")],
    )
    assert _answerable(lexical_only, tokens) is False
    assert _answerable(semantic, tokens) is True
    assert _answerable(mixed, tokens) is True  # independently answerable content
    assert _answerable(inactive, tokens) is False
    assert _answerable(interrogative, tokens) is False  # cue restatement is not an answer
    assert _answerable(semantic, []) is False


def test_lexical_support_keys_cover_directive_vocabulary() -> None:
    for key in ("mentioned", "cue", "token", "surface", "lexeme", "index", "stem"):
        assert key in LEXICAL_SUPPORT_KEYS


def test_token_nuclei_still_support_retrieval() -> None:
    """Non-goal check: cueing/emergence support is preserved, not redesigned."""
    eng = _conversational_session(question_turns=2)
    field = eng.remembering.activation.activate(
        "What is my favorite color?",
        context_tags=(),
        attention_weight=0.5,
        identity_query=False,
    )
    labels = [n.label for n in field.ranked_concepts(limit=6)]
    assert "favorite" in labels  # token nucleus still activates in the field
    reconstruction = eng.remembering.what_do_i_remember("What is my favorite color?")
    assert reconstruction.answer == "Your favorite color is blue."
