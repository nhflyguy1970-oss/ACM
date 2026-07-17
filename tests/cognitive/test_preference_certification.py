"""Preference Behavioral Certification — Memory Foundation completion.

Certifies that Preferences work correctly end-to-end in the standalone ACM
reference implementation, including the live Aria failure mode:

    "What is my favorite color?"
    → "Your preference is Tool `memory_search` worked for:
       Show the evidence for my favorite color."

Root causes covered:
1. Artifact classifier missed backtick-quoted tool wrappers
   (``Tool `memory_search` worked for:``).
2. Cleanup skipped experiences with empty metadata / no semantic_extraction
   even when the summary was a tool wrapper.
3. Declared-user provenance alone was insufficient — hosts can mislabel tool
   output as trusted user speech; content-level trust now rejects artifacts.
4. Interrogatives and tool-wrapper fallbacks minted preference attributes
   ("conflicting?", full tool strings) via Semantic Extraction / concept cues.
5. Reconstruction rendered non-user artifact attribute values as answers.
"""

from __future__ import annotations

import os
import tempfile

import pytest

from acm.api.engine import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT, TRUSTED_USER_TEACHING
from acm.provenance.legacy_cleanup import classify_untrusted_artifact
from acm.types import Attribute

LIVE_TOOL_WRAPPERS = (
    "Tool `memory_search` worked for: Show the evidence for my favorite color.",
    "Tool `memory_search` worked for: My favorite color is blue.",
    "Tool `memory_about_user` worked for: Who am I?",
    "Tool memory_search worked for: probe-yellow",
    "Diagnostic: probe-yellow",
    "Auto-saved on exit — module memory; recent asks: who are you.",
)


@pytest.fixture()
def engine(tmp_path):
    path = tmp_path / "pref.db"
    return CognitiveEngine(agent_id="aria", persist_path=str(path), auto_persist=True)


def test_live_tool_wrapper_signatures_classified() -> None:
    assert classify_untrusted_artifact(LIVE_TOOL_WRAPPERS[0]) == "tool_output"
    assert classify_untrusted_artifact(LIVE_TOOL_WRAPPERS[2]) == "tool_output"
    assert classify_untrusted_artifact(LIVE_TOOL_WRAPPERS[3]) == "tool_output"
    assert classify_untrusted_artifact(LIVE_TOOL_WRAPPERS[4]) == "diagnostic_output"
    assert classify_untrusted_artifact(LIVE_TOOL_WRAPPERS[5]) == "host_autosave"
    assert classify_untrusted_artifact("My favorite color is blue.") is None


def test_preference_certification_fresh_teach_dedupe_supersede_restart(tmp_path) -> None:
    path = str(tmp_path / "cert.db")
    e = CognitiveEngine(agent_id="aria", persist_path=path, auto_persist=True)

    # Fresh → unknown
    r = e.cognitive_respond("What is my favorite color?")
    assert r["status"] == "unknown"

    # Teach blue
    assert e.encode("My favorite color is blue.", provenance=TRUSTED_USER_TEACHING)["encoded"]
    r = e.cognitive_respond("What is my favorite color?")
    assert r["status"] == "known"
    assert r["memory"] == "Your favorite color is blue."

    # Teach blue again → no duplicate active attribute
    e.encode("My favorite color is blue.", provenance=TRUSTED_USER_TEACHING)
    active = [
        a
        for c in e.store.concepts.values()
        for a in c.attributes
        if a.key == "favorite_color" and a.active
    ]
    assert len(active) == 1 and active[0].value == "blue"

    # Teach red → supersedes blue
    e.encode("My favorite color is red.", provenance=TRUSTED_USER_TEACHING)
    r = e.cognitive_respond("What is my favorite color?")
    assert r["memory"] == "Your favorite color is red."
    values = {
        (a.value, a.active)
        for c in e.store.concepts.values()
        for a in c.attributes
        if a.key == "favorite_color"
    }
    assert values == {("blue", False), ("red", True)}

    e.flush()
    # Restart → still red
    e2 = CognitiveEngine(agent_id="aria", persist_path=path, auto_persist=True)
    assert e2.cognitive_respond("What is my favorite color?")["memory"] == (
        "Your favorite color is red."
    )


def test_preference_certification_contamination_ignored(engine: CognitiveEngine) -> None:
    engine.encode("My favorite color is red.", provenance=TRUSTED_USER_TEACHING)
    before = len(engine.store.experiences)

    for wrap in LIVE_TOOL_WRAPPERS:
        rejected = engine.encode(wrap, provenance=TRUSTED_USER_STATEMENT)
        assert rejected["encoded"] is False
        assert rejected["reason"] == "memory_trust"

    # Interrogatives as user speech must not mint preference facts
    engine.encode("What is my favorite color?", provenance=TRUSTED_USER_STATEMENT)
    engine.encode(
        "Why do you think my favorite color is conflicting?",
        provenance=TRUSTED_USER_STATEMENT,
    )
    active = [
        (a.key, a.value)
        for c in engine.store.concepts.values()
        for a in c.attributes
        if a.key in ("favorite_color", "preference") and a.active
    ]
    assert active == [("favorite_color", "red")]

    # Evidence ask returns lineage; does not mutate memory
    n = len(engine.store.experiences)
    er = engine.cognitive_respond("Show the evidence for my favorite color.")
    assert er["status"] == "known"
    assert "favorite color" in (er["memory"] or "").lower()
    assert "red" in (er["memory"] or "").lower()
    assert er.get("supporting_experiences") or "v1" in (er["memory"] or "")
    assert len(engine.store.experiences) == n
    # Preference retrieval still returns the active value
    assert engine.cognitive_respond("What is my favorite color?")["memory"] == (
        "Your favorite color is red."
    )

    # Repeat contamination — preference remains red
    for _ in range(5):
        engine.encode(LIVE_TOOL_WRAPPERS[0], provenance=TRUSTED_USER_STATEMENT)
    assert engine.cognitive_respond("What is my favorite color?")["memory"] == (
        "Your favorite color is red."
    )
    assert len(engine.store.experiences) >= before  # questions may encode; tools do not


def test_live_format_cleanup_restores_blue() -> None:
    """Reproduce the live Aria graph shape and prove cleanup restores blue."""
    e = CognitiveEngine(agent_id="aria")
    e.encode("My favorite color is blue.", provenance=TRUSTED_USER_TEACHING)

    tool = LIVE_TOOL_WRAPPERS[0]
    exp = e.experiences.birth(
        summary=tool,
        metadata={
            "evidence": tool,
            "semantic_extraction": "1",
            "fact_0_kind": "preference",
            "fact_0_property": "favorite_color",
            "fact_0_subject": "user",
            "fact_0_value": "conflicting?",
        },
    )
    for c in e.store.concepts.values():
        if not any(a.key == "favorite_color" for a in c.attributes):
            continue
        for a in c.attributes:
            if a.key == "favorite_color" and a.value == "blue":
                a.active = False
        c.attributes.append(
            Attribute(
                key="favorite_color",
                value="conflicting?",
                confidence=0.8,
                active=True,
                version=2,
                evidence_ids=[exp.id],
            )
        )
        c.attributes.append(
            Attribute(
                key="preference",
                value=tool,
                confidence=0.8,
                active=True,
                version=1,
                evidence_ids=[exp.id],
            )
        )
        if exp.id not in c.evidence_ids:
            c.evidence_ids.append(exp.id)

    # Render defense alone must refuse the artifact answer.
    before = e.cognitive_respond("What is my favorite color?")
    assert before["memory"] != f"Your preference is {tool}"
    assert "Tool" not in (before["memory"] or "")

    report = e.cleanup_legacy_contamination()
    assert report["removed_experiences"] >= 1
    assert report["reactivated_attributes"] >= 1
    after = e.cognitive_respond("What is my favorite color?")
    assert after["memory"] == "Your favorite color is blue."
    values = {
        (a.key, a.value, a.active)
        for c in e.store.concepts.values()
        for a in c.attributes
        if a.key in ("favorite_color", "preference")
    }
    assert ("favorite_color", "blue", True) in values
    assert not any(a[0] == "preference" and a[2] for a in values)
    assert not any(a[1] == "conflicting?" and a[2] for a in values)


def test_identity_regression_untouched(engine: CognitiveEngine) -> None:
    engine.encode("My name is Jeff.", provenance=TRUSTED_USER_TEACHING)
    r = engine.cognitive_respond("Who am I?")
    assert r["status"] == "known"
    assert "jeff" in (r["memory"] or "").lower()
    # Preference path still clean
    engine.encode("My favorite color is blue.", provenance=TRUSTED_USER_TEACHING)
    assert engine.cognitive_respond("What is my favorite color?")["memory"] == (
        "Your favorite color is blue."
    )


def test_d046_provenance_gate_still_rejects_untrusted(engine: CognitiveEngine) -> None:
    from acm.provenance import (
        HostOperation,
        IngestionActor,
        IngestionProvenance,
        MessageRole,
    )

    engine.encode("My favorite color is blue.", provenance=TRUSTED_USER_TEACHING)
    before = len(engine.store.experiences)
    for actor, op, role in (
        (IngestionActor.TOOL, HostOperation.TOOL_EXECUTION, MessageRole.TOOL_RESULT),
        (IngestionActor.DIAGNOSTIC, HostOperation.DIAGNOSTIC, MessageRole.DIAGNOSTIC_OUTPUT),
        (IngestionActor.SYSTEM, HostOperation.SYSTEM_EVENT, MessageRole.SYSTEM_MESSAGE),
        (IngestionActor.UNKNOWN, HostOperation.UNKNOWN, MessageRole.UNKNOWN),
    ):
        rejected = engine.encode(
            "My favorite color is artifact-mauve.",
            provenance=IngestionProvenance(actor=actor, host_operation=op, message_role=role),
        )
        assert rejected["encoded"] is False
        assert rejected["reason"] == "memory_trust"
    assert len(engine.store.experiences) == before
    assert engine.cognitive_respond("What is my favorite color?")["memory"] == (
        "Your favorite color is blue."
    )


def test_valid_teaching_updates_via_cognitive_respond(tmp_path) -> None:
    """Live regression: a valid teaching spoken to Memory Authority must update.

    'My favorite color is green.' previously dispatched as a retrieval and the
    new value was never encoded — recall stayed 'blue'. Teaching Recognition
    now encodes declarative user statements before dispatch.
    """
    path = str(tmp_path / "teach.db")
    e = CognitiveEngine(agent_id="aria", persist_path=path, auto_persist=True)

    # Fresh → unknown
    assert e.cognitive_respond("What is my favorite color?")["status"] == "unknown"

    # Teach blue via the conversational pipeline (no explicit encode call)
    taught = e.cognitive_respond("My favorite color is blue.")
    assert "teaching_encoded" in taught["reasoning_path"]
    assert e.cognitive_respond("What is my favorite color?")["memory"] == (
        "Your favorite color is blue."
    )

    # Teach green — the exact live certification failure
    taught = e.cognitive_respond("My favorite color is green.")
    assert "teaching_encoded" in taught["reasoning_path"]
    assert taught["memory"] == "Your favorite color is green."
    assert e.cognitive_respond("What is my favorite color?")["memory"] == (
        "Your favorite color is green."
    )

    # Blue is retired; green active
    values = {
        (a.value, a.active)
        for c in e.store.concepts.values()
        for a in c.attributes
        if a.key == "favorite_color"
    }
    assert values == {("blue", False), ("green", True)}

    # Evidence shows the teaching history and never mutates memory
    er = e.cognitive_respond("Show the evidence for my favorite color.")
    assert er["status"] == "known"
    assert "favorite color" in (er["memory"] or "").lower()
    assert "blue" in (er["memory"] or "").lower()
    assert "green" in (er["memory"] or "").lower()
    assert "retired" in (er["memory"] or "").lower()
    assert er.get("supporting_experiences") or "v1" in (er["memory"] or "")
    n = len(e.store.experiences)
    e.cognitive_respond("Show the evidence for my favorite color.")
    assert len(e.store.experiences) == n
    assert e.cognitive_respond("What is my favorite color?")["memory"] == (
        "Your favorite color is green."
    )

    # Teach green again → no duplicate active attribute
    e.cognitive_respond("My favorite color is green.")
    active = [
        a
        for c in e.store.concepts.values()
        for a in c.attributes
        if a.key == "favorite_color" and a.active
    ]
    assert len(active) == 1 and active[0].value == "green"

    e.flush()
    # Restart → still green (no cache survives; state is persisted)
    e2 = CognitiveEngine(agent_id="aria", persist_path=path, auto_persist=True)
    assert e2.cognitive_respond("What is my favorite color?")["memory"] == (
        "Your favorite color is green."
    )


def test_teaching_recognition_never_teaches_questions_or_artifacts() -> None:
    """Questions and artifact payloads remain non-teaching through the pipeline."""
    e = CognitiveEngine(agent_id="aria")
    e.cognitive_respond("My favorite color is green.")
    before_attrs = {
        (a.key, a.value)
        for c in e.store.concepts.values()
        for a in c.attributes
        if a.active
    }

    # Interrogatives never teach — including ones that embed declarative shapes
    for q in (
        "Is my favorite color yellow?",
        "What is my favorite color?",
        "Is my name Bob?",
        "Show the evidence for my favorite color.",
    ):
        r = e.cognitive_respond(q)
        assert "teaching_encoded" not in r["reasoning_path"], q

    # Artifact payloads are detected as teachings but rejected by content trust
    for wrap in LIVE_TOOL_WRAPPERS:
        r = e.cognitive_respond(wrap)
        assert "teaching_encoded" not in r["reasoning_path"], wrap
    r = e.cognitive_respond(
        "Tool `memory_search` worked for: My favorite color is mauve."
    )
    assert "teaching_encoded" not in r["reasoning_path"]
    assert any(p.startswith("teaching_rejected:") for p in r["reasoning_path"])

    after_attrs = {
        (a.key, a.value)
        for c in e.store.concepts.values()
        for a in c.attributes
        if a.active
    }
    assert after_attrs == before_attrs
    assert e.cognitive_respond("What is my favorite color?")["memory"] == (
        "Your favorite color is green."
    )


def test_d047_fixture_cleanup_still_passes() -> None:
    """Prior D047 fixture still cleans and restores blue."""
    from pathlib import Path

    fixture = (
        Path(__file__).resolve().parents[1] / "fixtures" / "pre_d046_contaminated_snapshot.json"
    )
    d = tempfile.mkdtemp()
    e = CognitiveEngine(agent_id="aria", persist_path=os.path.join(d, "c.db"), auto_persist=True)
    e.import_snapshot(str(fixture))
    report = e.cleanup_legacy_contamination()
    assert report["removed_experiences"] == 5
    assert e.cognitive_respond("What is my favorite color?")["memory"] == (
        "Your favorite color is blue."
    )
    # idempotent
    assert e.cleanup_legacy_contamination()["clean"] is True
