"""B29 — Diagnostic privacy / redaction (Gate 1 + Gate 2)."""

from __future__ import annotations

import json

import pytest

from acm.api.engine import CognitiveEngine
from acm.authority.redaction import (
    RedactionLevel,
    RedactionPolicy,
    build_redaction_context,
    redact_text,
    scrub_sensitive_patterns,
)
from acm.identity.rendering import IdentityRenderTarget
from acm.provenance import TRUSTED_USER_STATEMENT


def _engine(**kwargs: object) -> CognitiveEngine:
    return CognitiveEngine(agent_id="aria-b29", **kwargs)  # type: ignore[arg-type]


def test_scrub_email_and_phone() -> None:
    text = "Contact me at jeff@example.com or +1-555-123-4567 please."
    out = scrub_sensitive_patterns(text)
    assert "jeff@example.com" not in out
    assert "555-123-4567" not in out
    assert "[redacted]" in out


def test_redact_text_drops_forbidden_identity() -> None:
    from acm.authority.redaction import RedactionContext

    ctx = RedactionContext(
        target=IdentityRenderTarget.ASSISTANT,
        forbidden_values=frozenset({"Jordan"}),
    )
    out = redact_text(
        "I am Aria. Your name is Jordan.",
        ctx=ctx,
        policy=RedactionPolicy(level=RedactionLevel.STRICT),
    )
    assert out is None or "jordan" not in (out or "").lower()


def test_inspect_assistant_never_leaks_user_name() -> None:
    eng = _engine(
        assistant_identity={"name": "Aria", "role": "assistant"},
    )
    eng.encode("My name is Jordan.", provenance=TRUSTED_USER_STATEMENT)
    eng.encode("I prefer local AI.", provenance=TRUSTED_USER_STATEMENT)

    before = eng.store_fingerprint()
    view = eng.inspect_identity(who="assistant")
    assert view["redaction"] == "strict"
    assert view["redaction_applied"] is True
    blob = json.dumps(view).lower()
    assert "jordan" not in blob
    assert eng.store_fingerprint() == before


def test_inspect_evidence_redacts_email_in_summaries() -> None:
    eng = _engine()
    eng.encode(
        "My contact email is secret.user@example.org for work.",
        provenance=TRUSTED_USER_STATEMENT,
    )
    before = eng.store_fingerprint()
    view = eng.inspect_evidence("What is my contact email?")
    assert view["redaction_applied"] is True
    blob = json.dumps(view)
    assert "secret.user@example.org" not in blob
    assert eng.store_fingerprint() == before


def test_inspect_user_identity_keeps_user_name() -> None:
    eng = _engine(assistant_identity={"name": "Aria"})
    eng.encode("My name is Jordan.", provenance=TRUSTED_USER_STATEMENT)
    view = eng.inspect_identity(who="user")
    assert "jordan" in (view.get("memory") or "").lower()
    schemas = (view.get("snapshot") or {}).get("schemas") or {}
    for key in ("agent", "assistant"):
        if key in schemas:
            assert schemas[key].get("redacted") is True


def test_organ_view_applies_strict_redaction() -> None:
    eng = _engine()
    eng.encode("My favorite color is blue.", provenance=TRUSTED_USER_STATEMENT)
    eng.remember("What is my favorite color?")
    view = eng.organ_view("remembering")
    assert view["redaction"] == "strict"
    assert view.get("redaction_applied") is True
    assert "note" not in view or "deferred" not in str(view.get("note", "")).lower()


def test_redaction_none_passthrough() -> None:
    eng = _engine(redaction_policy=RedactionPolicy(level=RedactionLevel.NONE))
    eng.encode("My name is Jordan.", provenance=TRUSTED_USER_STATEMENT)
    view = eng.inspect_identity(who="assistant")
    assert view["redaction"] == "none"
    assert view["redaction_applied"] is False


def test_build_context_assistant_forbids_user() -> None:
    eng = _engine(assistant_identity={"name": "Aria"})
    eng.encode("My name is Jordan.", provenance=TRUSTED_USER_STATEMENT)
    ctx = build_redaction_context(eng, cue="Who are you?", who="assistant")
    assert ctx.target == IdentityRenderTarget.ASSISTANT
    assert any(v.casefold() == "jordan" for v in ctx.forbidden_values)


def test_preference_evidence_inspect_zero_write() -> None:
    eng = _engine()
    eng.encode("My favorite color is blue.", provenance=TRUSTED_USER_STATEMENT)
    before = eng.store_fingerprint()
    view = eng.inspect_evidence("Show the evidence for my favorite color")
    assert view["schema"] == "acm.inspect.evidence.v1"
    assert view["redaction_applied"] is True
    assert eng.store_fingerprint() == before


@pytest.mark.parametrize(
    "method,args",
    [
        ("inspect_reconstruction", ("What is my favorite color?",)),
        ("inspect_evidence", ("What is my favorite color?",)),
        ("inspect_confidence", ("favorite color",)),
        ("inspect_conflict", ("What is my favorite color?",)),
    ],
)
def test_all_inspect_facades_mark_redaction(method: str, args: tuple[str, ...]) -> None:
    eng = _engine()
    eng.encode("My favorite color is blue.", provenance=TRUSTED_USER_STATEMENT)
    eng.encode("My favorite color is red.", provenance=TRUSTED_USER_STATEMENT)
    view = getattr(eng, method)(*args)
    assert view.get("redaction") == "strict"
    assert view.get("redaction_applied") is True
