"""B11 learning certification — preference edits preserve provenance (L27)."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_l27_preference_edit_preserves_provenance() -> None:
    eng = CognitiveEngine(agent_id="m-l27")
    eng.encode("My favorite color is blue.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    prov_before = len(eng.store.provenance)
    eng.apply_preference_change(key="color", value="red")
    assert len(eng.store.provenance) >= prov_before
    # Experiences only grow via authorized encode — not invented silently
    assert any("red" in (e.summary or "").lower() for e in eng.store.experiences.values())
    view = eng.inspect_preference("color")
    assert view["active"]["value"] == "red"
    # Reject leaves store preference unchanged
    eng.propose_preference_change(key="color", value="green")
    # use pending
    pending = eng._preference_gate.pending()
    assert pending
    eng.reject_preference_change(pending[0].id)
    assert eng.inspect_preference("color")["active"]["value"] == "red"
