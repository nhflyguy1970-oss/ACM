"""B27 — Organ-scoped observability views."""

from __future__ import annotations

from acm.api.engine import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT
from acm.validation.organ_views import SCHEMA, available_organ_views


def test_organ_view_remembering_after_recall() -> None:
    eng = CognitiveEngine(agent_id="b27")
    eng.encode("My favorite color is blue.", provenance=TRUSTED_USER_STATEMENT)
    eng.remember("What is my favorite color?")
    view = eng.organ_view("remembering")
    assert view["schema"] == SCHEMA
    assert view["organ"] == "remembering"
    assert view["empty"] is False
    assert "remembering" in view["harness"] or view["observables"]


def test_organ_view_unknown_is_empty_contract() -> None:
    eng = CognitiveEngine(agent_id="b27-empty")
    view = eng.organ_view("not_an_organ")
    assert view["schema"] == SCHEMA
    assert view["empty"] is True
    assert view["redaction"] == "none"


def test_organ_views_batch_includes_identity() -> None:
    eng = CognitiveEngine(agent_id="b27-batch")
    eng.encode("My name is Sam.", provenance=TRUSTED_USER_STATEMENT)
    report = eng.organ_views(["identity", "remembering"])
    assert report["schema"] == "acm.organ_views.v1"
    assert "identity" in report["organs"]
    assert report["organs"]["identity"]["schema"] == SCHEMA


def test_available_organ_views_stable() -> None:
    names = available_organ_views()
    assert "remembering" in names
    assert "identity" in names
    assert names == tuple(sorted(names))
