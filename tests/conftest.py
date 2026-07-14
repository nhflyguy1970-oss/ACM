from __future__ import annotations

import pytest

from acm import CognitiveEngine


@pytest.fixture
def engine() -> CognitiveEngine:
    return CognitiveEngine(agent_id="test-agent", buffer_capacity=7)
