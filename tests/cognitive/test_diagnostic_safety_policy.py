"""B09 — Diagnostic safety policy (cognitive)."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.authority.diagnostic_policy import (
    DiagnosticSafetyPolicy,
    with_safety_enabled,
)
from acm.authority.redaction import RedactionLevel, RedactionPolicy
from acm.provenance import TRUSTED_USER_STATEMENT


def test_b09_inspect_applies_safety_and_never_invents() -> None:
    eng = CognitiveEngine(agent_id="b09")
    eng.encode("My favorite color is blue.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    before = eng.store_fingerprint()
    exp_n = len(eng.store.experiences)
    view = eng.inspect("What is my favorite color?")
    assert view.get("safety_policy_applied") is True
    assert view.get("safety_policy_enabled") is True
    assert view.get("redaction_applied") is True
    assert (view.get("diagnostics") or {}).get("execution_mode") == "read_only"
    # No raw store / infrastructure dumps
    blob = str(view).lower()
    assert "memory_store" not in blob
    assert "traceback" not in blob
    assert eng.store_fingerprint() == before
    assert len(eng.store.experiences) == exp_n


def test_b09_strips_organ_raw_and_cross_identity() -> None:
    eng = CognitiveEngine(
        agent_id="aria-b09",
        assistant_identity={"name": "Aria", "role": "assistant"},
    )
    eng.encode("My name is Jeffrey.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode("My email is jeff@example.com.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    asst = eng.inspect_identity(who="assistant")
    assert asst["safety_policy_applied"] is True
    blob = str(asst).lower()
    assert "jeffrey" not in blob
    assert "jeff@example.com" not in blob or "[redacted]" in blob
    # façade still zero-write
    fp = eng.store_fingerprint()
    eng.inspect_evidence("What is my favorite color?")
    assert eng.store_fingerprint() == fp


def test_b09_disabled_passthrough_for_dev() -> None:
    eng = CognitiveEngine(
        agent_id="b09-dev",
        diagnostic_safety_policy=with_safety_enabled(
            DiagnosticSafetyPolicy(redaction=RedactionPolicy(level=RedactionLevel.NONE)),
            enabled=False,
        ),
        redaction_policy=RedactionPolicy(level=RedactionLevel.NONE),
    )
    eng.encode("My favorite tea is oolong.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    view = eng.inspect("favorite tea")
    assert view.get("safety_policy_enabled") is False
    assert view.get("safety_policy_applied") is False


def test_b09_facades_and_organ_views_mark_policy() -> None:
    eng = CognitiveEngine(agent_id="b09-views")
    eng.encode("I prefer local AI.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    for view in (
        eng.inspect_reconstruction("What do I prefer?"),
        eng.inspect_confidence("prefer"),
        eng.organ_view("learning"),
    ):
        assert view.get("safety_policy_applied") is True
        assert view.get("redaction") == "strict"
