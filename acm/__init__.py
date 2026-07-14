"""ACM — Aria Cognitive Memory: host-agnostic cognitive memory engine."""

from __future__ import annotations

from acm.api.engine import CognitiveEngine, RememberResult
from acm.observability.trace import CognitiveTraceEvent
from acm.validation.harness import ValidationHarness

__version__ = "0.1.0"
__all__ = [
    "CognitiveEngine",
    "RememberResult",
    "CognitiveTraceEvent",
    "ValidationHarness",
    "__version__",
]
