"""B29 permanent behavioral conversation — diagnostic privacy."""

from __future__ import annotations

import json

from acm.api.engine import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_behavioral_assistant_evidence_never_reveals_user_name() -> None:
    """Permanent conversation: assistant diagnostics must not leak user identity."""
    eng = CognitiveEngine(
        agent_id="aria",
        assistant_identity={"name": "Aria", "role": "assistant"},
    )
    eng.encode("My name is Jordan.", provenance=TRUSTED_USER_STATEMENT)
    eng.encode("My favorite color is teal.", provenance=TRUSTED_USER_STATEMENT)

    # Conversational assistant identity
    spoken = eng.cognitive_respond("Who are you?")
    spoken_blob = json.dumps(spoken).lower()
    assert "jordan" not in spoken_blob

    # Diagnostic inspect path
    fp = eng.store_fingerprint()
    for cue in (
        "Who are you?",
        "What is my favorite color?",
        "Show the evidence for my favorite color",
    ):
        if "who are you" in cue.lower():
            view = eng.inspect_identity(who="assistant")
        elif "evidence" in cue.lower():
            view = eng.inspect_evidence(cue)
        else:
            view = eng.inspect_reconstruction(cue)
        assert view.get("redaction_applied") is True
        assert "jordan" not in json.dumps(view).lower()
    assert eng.store_fingerprint() == fp


def test_behavioral_organ_views_do_not_defer_privacy() -> None:
    eng = CognitiveEngine(agent_id="aria-views")
    eng.encode("My name is Sam.", provenance=TRUSTED_USER_STATEMENT)
    report = eng.organ_views(["identity", "remembering", "learning"])
    for name, view in report["organs"].items():
        assert view["redaction"] == "strict", name
        assert "deferred to B29" not in str(view.get("note", "")).lower()
