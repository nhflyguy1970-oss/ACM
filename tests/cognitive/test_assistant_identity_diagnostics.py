"""B44 / B45 — Assistant identity pipeline diagnostics and isolation hardening."""

from __future__ import annotations

from acm.api.engine import CognitiveEngine
from acm.identity.pipeline_trace import trace_assistant_identity_pipeline
from acm.identity.rendering import IdentityRenderTarget, isolate_identity_text
from acm.provenance import TRUSTED_USER_STATEMENT


def test_trace_assistant_identity_pipeline_ok() -> None:
    eng = CognitiveEngine(
        agent_id="aria",
        assistant_identity={"name": "Aria", "role": "cognitive assistant"},
    )
    eng.encode("My name is Jeff.", provenance=TRUSTED_USER_STATEMENT)
    report = trace_assistant_identity_pipeline(eng)
    assert report["ok"] is True
    assert report["user_bleed"] is False
    assert report["operational_name"].lower() == "aria"
    assert any(s["stage"] == "identity_organ_render" for s in report["stages"])


def test_isolation_preserves_operational_name_when_user_token_substring() -> None:
    """B45: short user location token must not wipe 'My name is Aria.'"""
    text = "My name is Aria. My role is cognitive assistant."
    # User location "ri" would historically over-filter via substring/word rules;
    # operational name claims must survive unless the claimed name equals forbidden.
    out = isolate_identity_text(
        text,
        target=IdentityRenderTarget.ASSISTANT,
        forbidden_values={"Jeff", "ri"},
    )
    assert out is not None
    assert "my name is aria" in out.lower()
    assert "cognitive assistant" in out.lower()


def test_isolation_still_drops_true_name_collision() -> None:
    text = "My name is Jeff. My role is navigator."
    out = isolate_identity_text(
        text,
        target=IdentityRenderTarget.ASSISTANT,
        forbidden_values={"Jeff"},
    )
    assert out is not None
    assert "jeff" not in out.lower()
    assert "navigator" in out.lower()


def test_render_assistant_no_reseed_when_operational_present() -> None:
    eng = CognitiveEngine(
        agent_id="aria",
        assistant_identity={"name": "Aria", "role": "assistant"},
    )
    eng.encode("My name is Jeff.", provenance=TRUSTED_USER_STATEMENT)
    # Contaminate description with user-location-like token that is not the name claim
    eng.encode(
        "You are Aria.",
        provenance=TRUSTED_USER_STATEMENT,
    )
    rendered = eng.identity.render_assistant_identity()
    assert rendered.get("reseeded_operational_name") is False
    assert "aria" in (rendered.get("answer") or "").lower()
