"""Preference pipeline diagnostics — D045 investigation and correction record.

These tests document the behavior of the Preference subsystem as traced in
docs/PREFERENCE_PIPELINE_TRACE.md and docs/PREFERENCE_CONFLICT_ANALYSIS.md.

The false competing_recollections defect was corrected by D045
(competitor admissibility — see docs/PREFERENCE_RECONSTRUCTION_FIX.md and
tests/cognitive/test_preference_reconstruction_fix.py). Tests named
``test_deferred_*`` pin defects that are intentionally NOT part of D045
(teach/query classification, evidence intent, introspection quality) and
must be updated when their own corrections land.
"""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT, TRUSTED_USER_TEACHING
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
    out = eng.encode(
        "My favorite color is blue.", kind="preference", provenance=TRUSTED_USER_STATEMENT
    )
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
    eng.encode("My favorite color is blue.", kind="preference", provenance=TRUSTED_USER_STATEMENT)
    eng.encode("My favorite color is blue.", kind="preference", provenance=TRUSTED_USER_STATEMENT)
    result = eng.cognitive_respond("What is my favorite color?")
    assert result["status"] == "known"
    assert result["memory"] == "Your favorite color is blue."
    active = [(c, a) for c, a in _favorite_color_attrs(eng) if a.active]
    assert len(active) == 1


def test_preference_update_replaces_value() -> None:
    """blue → red: old value deactivated, new value active, answer updates."""
    eng = _engine()
    eng.encode("My favorite color is blue.", kind="preference", provenance=TRUSTED_USER_STATEMENT)
    eng.encode(
        "Actually, my favorite color is red.", kind="preference", provenance=TRUSTED_USER_STATEMENT
    )
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
    eng.encode("My favorite color is blue.", kind="preference", provenance=TRUSTED_USER_STATEMENT)
    eng.encode("My favorite color is red.", kind="preference", provenance=TRUSTED_USER_STATEMENT)
    result = eng.cognitive_respond("What is my favorite color?")
    assert result["status"] == "known"
    assert result["memory"] == "Your favorite color is red."


# ---------------------------------------------------------------------------
# D045 corrected behavior — token nuclei never manufacture ambiguity
# ---------------------------------------------------------------------------


def test_token_nucleus_never_competes_after_d045() -> None:
    """FIXED by D045: lexical token concepts no longer count as competitors.

    Encoding the user's own question as a conversation turn re-ingests the
    token nucleus concept 'favorite' (attr mentioned='favorite'). Before D045
    its energy within COMPETE_RATIO made it a CompetingRecollection → false
    'competing_recollections'. With competitor admissibility, retrieval stays
    known: there is exactly ONE preference fact in the store.
    """
    eng = _engine()
    eng.encode("My favorite color is blue.", kind="preference", provenance=TRUSTED_USER_STATEMENT)
    eng.encode(
        "What is my favorite color?", provenance=TRUSTED_USER_STATEMENT
    )  # conversation turn, kind=experience

    active = [(c, a) for c, a in _favorite_color_attrs(eng) if a.active]
    assert len(active) == 1
    assert active[0][1].value == "blue"

    reconstruction = eng.remembering.what_do_i_remember("What is my favorite color?")
    assert reconstruction.answer == "Your favorite color is blue."
    assert reconstruction.ambiguous is False
    assert reconstruction.competing == []

    result = eng.cognitive_respond("What is my favorite color?")
    assert result["status"] == "known"
    assert result["memory"] == "Your favorite color is blue."
    assert result["uncertainty"] is None
    # The token nucleus still exists and keeps supporting retrieval.
    nuclei = [
        c
        for c in eng.store.concepts.values()
        if c.role == ConceptRole.ENTITY
        and any(a.key == "mentioned" and a.value == "favorite" for a in c.attributes)
    ]
    assert nuclei, "token nucleus must remain for cueing/emergence support"


def test_interrogative_no_longer_stored_as_preference_fact() -> None:
    """Preference certification: interrogatives must not mint preference attrs.

    Previously (deferred under D045) any sentence containing 'favorite' that
    did not match 'favorite X is Y' dumped the raw question onto
    preference=<question>. That path is closed — questions are retrieval cues.
    """
    eng = _engine()
    eng.encode("What is my favorite color?", provenance=TRUSTED_USER_STATEMENT)
    stored = [
        (c, a)
        for c in eng.store.concepts.values()
        for a in c.attributes
        if a.key == "preference" and a.active
    ]
    assert not stored, "interrogatives must not mint preference attributes"
    # Teaching still works after a question turn.
    eng.encode("My favorite color is blue.", provenance=TRUSTED_USER_TEACHING)
    assert eng.cognitive_respond("What is my favorite color?")["memory"] == (
        "Your favorite color is blue."
    )


def test_deferred_teach_statement_classified_as_retrieval() -> None:
    """DEFERRED (not D045): declarative teach dispatches as a preference query.

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


def test_deferred_evidence_inspection_bypassed_to_preference() -> None:
    """DEFERRED (not D045): evidence requests swallowed by preference cue.

    'Show the evidence for my favorite color.' matches preference_cue in Band B
    (there is no evidence/introspection intent in the taxonomy), so it routes to
    remembering and terminates at the same reconstruction terminal as the plain
    preference question. After D045 both correctly answer known instead of the
    false conflict, but the classification bypass remains a deferred decision.
    """
    eng = _engine()
    cl = eng.classify_request("Show the evidence for my favorite color.")
    intent = cl["intent"] if isinstance(cl, dict) else cl.intent.value
    assert intent == "preference"  # not an evidence/introspection intent

    eng.encode("My favorite color is blue.", kind="preference", provenance=TRUSTED_USER_STATEMENT)
    eng.encode("What is my favorite color?", provenance=TRUSTED_USER_STATEMENT)
    evidence = eng.cognitive_respond("Show the evidence for my favorite color.")
    assert evidence["diagnostics"]["primary_organ"] == "remembering"
    # D045: no more false conflict on the evidence request either.
    assert evidence["status"] == "known"
    assert evidence["uncertainty"] is None
