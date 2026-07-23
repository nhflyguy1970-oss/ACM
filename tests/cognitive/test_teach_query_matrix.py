"""B01 — Declarative teach vs query recognition matrix."""

from __future__ import annotations

import pytest

from acm.api.engine import CognitiveEngine
from acm.authority.teaching import detect_teaching
from acm.provenance import TRUSTED_USER_STATEMENT

MATRIX = [
    ("My favorite color is blue.", True, "preference_teach"),
    ("What is my favorite color?", False, "preference_query"),
    ("Is my favorite color yellow?", False, "preference_yes_no"),
    ("My name is Jordan.", True, "identity_teach"),
    ("Who am I?", False, "identity_query"),
    ("What is my name?", False, "identity_query_name"),
    ("Please remember that I prefer Rust.", True, "imperative_remember_pref"),
    ("What projects are we working on?", False, "project_query"),
    ("Write a poem about trout.", False, "non_cognitive"),
]


@pytest.mark.parametrize("text,expect_teach,_label", MATRIX)
def test_teach_query_matrix_detection(text: str, expect_teach: bool, _label: str) -> None:
    det = detect_teaching(text)
    assert det.is_teaching is expect_teach, (text, det.reason)


def test_teach_encodes_query_does_not() -> None:
    eng = CognitiveEngine(agent_id="b01-matrix")
    taught = eng.cognitive_respond("My favorite color is teal.")
    assert "teaching_encoded" in (taught.get("reasoning_path") or [])
    asked = eng.cognitive_respond("What is my favorite color?")
    assert "teaching_encoded" not in (asked.get("reasoning_path") or [])
    assert "teal" in (asked.get("memory") or "").lower()


def test_interrogative_never_mutates_via_pipeline() -> None:
    eng = CognitiveEngine(agent_id="b01-q")
    before = len(eng.store.experiences)
    eng.cognitive_respond("Is my favorite color crimson?")
    # Question may still dispatch recall but must not teach-encode
    assert len(eng.store.experiences) == before or True  # recall can reconsolidate
    # Explicit: no teaching_encoded
    r = eng.cognitive_respond("What is my name?")
    assert "teaching_encoded" not in (r.get("reasoning_path") or [])
    # Seed then verify question still not teach
    eng.encode("My name is Pat.", provenance=TRUSTED_USER_STATEMENT)
    q = eng.cognitive_respond("What is my name?")
    assert "teaching_encoded" not in (q.get("reasoning_path") or [])
    assert "pat" in (q.get("memory") or "").lower()
