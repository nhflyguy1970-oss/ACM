from __future__ import annotations

from acm.concepts.extract import extract_cues
from acm.types import ConceptRole


def test_is_a_and_preference_cues() -> None:
    cues = extract_cues("Zeus is a golden retriever.")
    labels = {c.label for c in cues}
    assert "zeus" in labels
    assert any(c.parent_label == "golden retriever" for c in cues)

    prefs = extract_cues("My favorite tea is green.", encode_kind="preference")
    assert any(c.role == ConceptRole.PREFERENCE for c in prefs)
