from __future__ import annotations

import pytest

from acm import CognitiveEngine
from acm.plugins import BaseExtension, ExtensionError


def test_duplicate_registration_fails() -> None:
    engine = CognitiveEngine(agent_id="p")
    ext = BaseExtension()
    ext.name = "x.demo"
    ext.version = "0.1.0"
    engine.extensions.register(ext)
    with pytest.raises(ExtensionError):
        engine.extensions.register(ext)
