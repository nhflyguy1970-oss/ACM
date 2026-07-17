"""Semantic Extraction — identity, perspective, facts, updates (D041)."""

from __future__ import annotations

import time

import pytest

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT
from acm.semantic import (
    extract_semantics,
    resolve_perspective,
    strip_instructional,
)
from acm.semantic.model import FactKind, PerspectiveSubject


@pytest.mark.parametrize(
    "raw,expect_substr,stripped",
    [
        ("My name is Jeff. Please remember that.", "My name is Jeff", True),
        ("Remember that I live in New Hampshire.", "I live in New Hampshire", True),
        ("I prefer tea.", "I prefer tea", False),
    ],
)
def test_strip_instructional(raw: str, expect_substr: str, stripped: bool) -> None:
    cleaned, did = strip_instructional(raw)
    assert expect_substr.lower() in cleaned.lower()
    assert did is stripped
    assert "please remember" not in cleaned.lower()


def test_perspective_remember_instruction_is_user() -> None:
    p = resolve_perspective("My name is Jeff. Please remember that.", kind="experience")
    assert p.first_person == PerspectiveSubject.USER
    assert "remember" in p.reason


def test_perspective_identity_kind_requires_speaker() -> None:
    """kind=identity alone no longer flips to assistant (D043)."""
    p = resolve_perspective("I am a research assistant.", kind="identity")
    assert p.first_person == PerspectiveSubject.USER
    p2 = resolve_perspective("I am a research assistant.", kind="identity", speaker="assistant")
    assert p2.first_person == PerspectiveSubject.ASSISTANT


def test_perspective_explicit_speaker() -> None:
    p = resolve_perspective("My name is Jeff.", kind="identity", speaker="user")
    assert p.first_person == PerspectiveSubject.USER


def test_extract_user_name_not_utterance() -> None:
    result = extract_semantics("My name is Jeff. Please remember that.", kind="experience")
    assert result.facts
    fact = result.facts[0]
    assert fact.subject == PerspectiveSubject.USER
    assert fact.property == "name"
    assert fact.value == "Jeff"
    assert "please" not in fact.value.lower()
    assert "remember" not in result.primary_summary.lower()
    assert "please remember" in result.evidence.lower()


def test_extract_im_jeff() -> None:
    result = extract_semantics("I'm Jeff.", kind="experience")
    assert any(f.property == "name" and f.value == "Jeff" for f in result.facts)


def test_extract_call_me() -> None:
    result = extract_semantics("Call me Jeff.", kind="experience")
    assert any(f.property == "preferred_name" and f.value == "Jeff" for f in result.facts)


def test_extract_assistant_you_are() -> None:
    result = extract_semantics("You are ARIA.", kind="experience")
    assert any(
        f.subject == PerspectiveSubject.ASSISTANT and f.value.upper() == "ARIA"
        for f in result.facts
    )


def test_extract_dog_relationship() -> None:
    result = extract_semantics("My dog's name is Zeus.", kind="experience")
    assert any(
        f.kind == FactKind.RELATIONSHIP and f.value == "Zeus" and f.relation_type == "dog"
        for f in result.facts
    )
    assert not any(
        f.property == "name" and f.subject == PerspectiveSubject.USER for f in result.facts
    )


def test_extract_location() -> None:
    result = extract_semantics("I live in New Hampshire.", kind="experience")
    assert any(f.property == "location" and "New Hampshire" in f.value for f in result.facts)


def test_extract_preference_goal_project() -> None:
    pref = extract_semantics("I prefer concise answers.", kind="preference")
    assert any(f.kind == FactKind.PREFERENCE for f in pref.facts)
    goal = extract_semantics("My goal is ship ACM.", kind="experience")
    assert any(f.kind == FactKind.GOAL for f in goal.facts)
    proj = extract_semantics("I'm working on Project Aria.", kind="experience")
    assert any(f.kind == FactKind.PROJECT for f in proj.facts)


def test_encode_stores_fact_not_utterance() -> None:
    eng = CognitiveEngine(agent_id="aria")
    out = eng.encode(
        "My name is Jeff. Please remember that.", pin=True, provenance=TRUSTED_USER_STATEMENT
    )
    assert out["encoded"] is True
    exp = eng.store.experiences[out["experience_id"]]
    assert "please remember" not in exp.summary.lower()
    assert "jeff" in exp.summary.lower()
    assert any(k == "evidence" for k, _ in exp.metadata)
    evidence = next(v for k, v in exp.metadata if k == "evidence")
    assert "please remember" in evidence.lower()
    user = eng.identity.schema_concept("user")
    names = [a.value for a in user.attributes if a.key == "name" and a.active]
    assert names == ["Jeff"]
    # Must not land on assistant schema
    agent = eng.identity.schema_concept("agent")
    agent_names = [a.value for a in agent.attributes if a.key == "name" and a.active]
    assert "Jeff" not in agent_names


def test_encode_assistant_identity_unchanged_path() -> None:
    eng = CognitiveEngine(agent_id="guide")
    eng.encode(
        "I am a research assistant.",
        kind="identity",
        speaker="assistant",
        provenance=TRUSTED_USER_STATEMENT,
    )
    who = eng.who_am_i()
    assert "research assistant" in who["answer"].lower()


def test_name_update_revises_not_duplicates() -> None:
    eng = CognitiveEngine(agent_id="aria")
    eng.encode(
        "My name is Jeff. Please remember that.", pin=True, provenance=TRUSTED_USER_STATEMENT
    )
    eng.encode(
        "My name is Jeffrey. Please remember that.", pin=True, provenance=TRUSTED_USER_STATEMENT
    )
    user = eng.identity.schema_concept("user")
    active = [a.value for a in user.attributes if a.key == "name" and a.active]
    assert active == ["Jeffrey"]
    assert sum(1 for a in user.attributes if a.key == "name") >= 1


def test_negation_and_false_extraction() -> None:
    neg = extract_semantics("My name is not Bob.", kind="experience")
    assert any(f.kind == FactKind.NEGATION for f in neg.facts)
    # Ambiguous weather — no false identity
    weather = extract_semantics("It is raining today.", kind="experience")
    assert not any(f.kind == FactKind.IDENTITY for f in weather.facts)


def test_multiple_entities() -> None:
    result = extract_semantics(
        "My name is Jeff. My dog's name is Zeus. I live in New Hampshire.",
        kind="experience",
    )
    kinds = {f.kind for f in result.facts}
    assert FactKind.IDENTITY in kinds
    assert FactKind.RELATIONSHIP in kinds
    assert FactKind.LOCATION in kinds


def test_host_independence_no_imports() -> None:
    import acm.semantic.extract as ex

    src = open(ex.__file__, encoding="utf-8").read()
    assert "openai" not in src.lower()
    assert "ollama" not in src.lower()
    assert "jarvis" not in src.lower()
    assert "aria_core" not in src.lower()


def test_performance_extraction_budget() -> None:
    t0 = time.perf_counter()
    for _ in range(200):
        extract_semantics("My name is Jeff. Please remember that.", kind="experience")
    elapsed = time.perf_counter() - t0
    assert elapsed < 1.0  # pure regex — well under 5ms avg
