"""Preference pipeline diagnostics — investigation of false competing_recollections.

These tests document the CURRENT behavior of the Preference subsystem as traced
in docs/PREFERENCE_PIPELINE_TRACE.md and docs/PREFERENCE_CONFLICT_ANALYSIS.md.

Tests named ``test_defect_*`` reproduce implementation defects on purpose and
assert the *observed defective* behavior so the investigation is executable.
They must be updated when the approved correction lands. No production
behavior is changed by this investigation.
"""

from __future__ import annotations

from acm import CognitiveEngine
from acm.semantic import extract_semantics
from acm.types import ConceptRole


def _engine() -> CognitiveEngine:
    return CognitiveEngine(agent_id="pref-debug")


def _favorite_color_attrs(eng: CognitiveEngine) -> list:
    out = []
    for concept in eng.store.concepts.values():
        for attr in concept.attributes:
            if attr.key == "favorite_color":
                out.append((concept, attr))
    return out


# ---------------------------------------------------------------------------
# Healthy stages — behave as designed
# ---------------------------------------------------------------------------


def test_unknown_preference_fresh_memory() -> None:
    """Fresh memory → preference question → honest unknown."""
    eng = _engine()
    result = eng.cognitive_respond("What is my favorite color?")
    assert result["intent"] == "preference"
    assert result["status"] == "unknown"
    assert result["memory"] is None
    assert result["uncertainty"] == "no_reliable_reconstruction"


def test_semantic_extraction_single_preference_fact() -> None:
    """'My favorite color is blue.' → exactly one structured preference fact."""
    extraction = extract_semantics("My favorite color is blue.", kind="preference")
    assert len(extraction.facts) == 1
    fact = extraction.facts[0]
    assert fact.kind.value == "preference"
    assert fact.subject.value == "user"
    assert fact.property == "favorite_color"
    assert fact.value == "blue"


def test_single_preference_teach_then_known() -> None:
    """Teach once → ask → known, no conflict."""
    eng = _engine()
    out = eng.encode("My favorite color is blue.", kind="preference")
    assert out["encoded"] is True
    result = eng.cognitive_respond("What is my favorite color?")
    assert result["status"] == "known"
    assert result["memory"] == "Your favorite color is blue."
    assert result["uncertainty"] is None
    # Storage: exactly one active favorite_color attribute exists.
    active = [(c, a) for c, a in _favorite_color_attrs(eng) if a.active]
    assert len(active) == 1
    assert active[0][1].value == "blue"


def test_repeated_identical_preference_no_conflict() -> None:
    """Repeating the identical teach must not manufacture a conflict."""
    eng = _engine()
    eng.encode("My favorite color is blue.", kind="preference")
    eng.encode("My favorite color is blue.", kind="preference")
    result = eng.cognitive_respond("What is my favorite color?")
    assert result["status"] == "known"
    assert result["memory"] == "Your favorite color is blue."
    active = [(c, a) for c, a in _favorite_color_attrs(eng) if a.active]
    assert len(active) == 1


def test_preference_update_replaces_value() -> None:
    """blue → red: old value deactivated, new value active, answer updates."""
    eng = _engine()
    eng.encode("My favorite color is blue.", kind="preference")
    eng.encode("Actually, my favorite color is red.", kind="preference")
    result = eng.cognitive_respond("What is my favorite color?")
    assert result["status"] == "known"
    assert result["memory"] == "Your favorite color is red."
    values = {a.value: a.active for _, a in _favorite_color_attrs(eng)}
    assert values.get("red") is True
    assert values.get("blue") is False


def test_contradictory_preference_current_semantics_last_write_wins() -> None:
    """Two contradictory plain teaches: current schema semantics = update (SET).

    Documenting current behavior: no conflict is surfaced; the second value
    replaces the first. Whether this should surface as a reconcilable conflict
    is a design question outside this investigation.
    """
    eng = _engine()
    eng.encode("My favorite color is blue.", kind="preference")
    eng.encode("My favorite color is red.", kind="preference")
    result = eng.cognitive_respond("What is my favorite color?")
    assert result["status"] == "known"
    assert result["memory"] == "Your favorite color is red."


# ---------------------------------------------------------------------------
# Defect demonstrations — current (incorrect) behavior, per investigation
# ---------------------------------------------------------------------------


def test_defect_false_conflict_from_token_nucleus_concept() -> None:
    """DEFECT (root cause): lexical token concepts count as competing recollections.

    Encoding any additional sentence containing the word 'favorite' (here the
    user's own question logged as a conversation turn) re-ingests the token
    nucleus concept 'favorite' (attr mentioned='favorite'). Its activation
    energy then falls within COMPETE_RATIO of the true preference concept and
    RememberingOrgan._reconstruct records it as a CompetingRecollection →
    ambiguous → gate CONFLICTING → 'competing_recollections'.

    There is exactly ONE preference fact in the store. The 'conflict' is the
    word 'favorite' itself, not a contradictory memory.
    """
    eng = _engine()
    eng.encode("My favorite color is blue.", kind="preference")
    eng.encode("What is my favorite color?")  # conversation turn, kind=experience

    # Storage truth: still a single active preference fact — no real conflict.
    active = [(c, a) for c, a in _favorite_color_attrs(eng) if a.active]
    assert len(active) == 1
    assert active[0][1].value == "blue"

    reconstruction = eng.remembering.what_do_i_remember("What is my favorite color?")
    assert reconstruction.answer == "Your favorite color is blue."
    # Current defective behavior: ambiguity from a token-nucleus rival.
    assert reconstruction.ambiguous is True
    assert reconstruction.competing, "expected the false competitor to be recorded"
    rival = eng.store.concepts[reconstruction.competing[0].concept_id]
    assert rival.role == ConceptRole.ENTITY  # not a preference concept
    assert any(a.key == "mentioned" for a in rival.attributes)  # lexical noise

    result = eng.cognitive_respond("What is my favorite color?")
    assert result["status"] == "conflicting"
    assert result["uncertainty"] == "competing_recollections"


def test_defect_question_turn_stored_as_preference_fact() -> None:
    """DEFECT (contributing): interrogative text stored as a preference attribute.

    extract_cues treats any sentence containing 'favorite' as preference-bearing;
    a question that does not match 'favorite X is Y' falls into the fallback
    branch and stores the raw question text as attr preference=<question>.
    """
    eng = _engine()
    eng.encode("What is my favorite color?")
    stored = [
        (c, a)
        for c in eng.store.concepts.values()
        for a in c.attributes
        if a.key == "preference" and a.active
    ]
    assert stored, "current behavior: question text lands on a preference concept"
    assert stored[0][1].value == "What is my favorite color?"


def test_defect_teach_statement_classified_as_retrieval() -> None:
    """DEFECT (contributing): declarative teach dispatches as a preference query.

    'My favorite color is blue.' classifies as intent=preference /
    is_memory_request=True and routes to remembering (retrieval). There is no
    declarative/teach discrimination, so the reply to a teach is a retrieval
    result over whatever the store currently contains.
    """
    eng = _engine()
    cl = eng.classify_request("My favorite color is blue.")
    intent = cl["intent"] if isinstance(cl, dict) else cl.intent.value
    assert intent == "preference"
    route = eng.route_request("My favorite color is blue.")
    ownership = route.get("ownership") or {}
    assert ownership.get("primary_organ") == "remembering"


def test_defect_evidence_inspection_bypassed_to_preference() -> None:
    """DEFECT (introspection): evidence requests swallowed by preference cue.

    'Show the evidence for my favorite color.' matches preference_cue in Band B
    (there is no evidence/introspection intent in the taxonomy), so it routes to
    remembering and terminates with the same reconstruction terminal as the
    plain preference question — introspection is bypassed at classification.
    """
    eng = _engine()
    cl = eng.classify_request("Show the evidence for my favorite color.")
    intent = cl["intent"] if isinstance(cl, dict) else cl.intent.value
    assert intent == "preference"  # not an evidence/introspection intent

    # On identically contaminated stores both requests terminate at the same
    # remembering reconstruction terminal with the same conflicting status.
    # Two question turns are needed: the false conflict scales with how often
    # the word 'favorite' has been re-encoded (see conflict analysis), and the
    # longer evidence cue dilutes activation slightly. Two engines are used
    # because each query mutates confidence via reconsolidation.
    def _contaminated() -> CognitiveEngine:
        e = _engine()
        e.encode("My favorite color is blue.", kind="preference")
        e.encode("What is my favorite color?")
        e.encode("What is my favorite color?")
        return e

    base = _contaminated().cognitive_respond("What is my favorite color?")
    evidence = _contaminated().cognitive_respond("Show the evidence for my favorite color.")
    assert base["status"] == "conflicting"
    assert evidence["status"] == "conflicting"
    assert evidence["uncertainty"] == base["uncertainty"] == "competing_recollections"
    assert evidence["diagnostics"]["primary_organ"] == "remembering"


def test_defect_conflict_explanation_does_not_name_competitors() -> None:
    """DEFECT (introspection): 'Why ... conflicting?' routes to reflection but the
    terminal memory text never names the actual competing facts, and the status
    again gates on the same ambiguous reconstruction.
    """
    eng = _engine()
    eng.encode("My favorite color is blue.", kind="preference")
    eng.encode("What is my favorite color?")
    cl = eng.classify_request("Why do you think my favorite color is conflicting?")
    intent = cl["intent"] if isinstance(cl, dict) else cl.intent.value
    assert intent == "reflection"
    result = eng.cognitive_respond("Why do you think my favorite color is conflicting?")
    memory = (result["memory"] or "").lower()
    # The specific competing concept ('favorite' token nucleus) is never named.
    assert "competing recollection" not in memory
    assert "blue" not in memory or "favorite" not in memory
