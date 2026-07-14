"""ACM — Aria Cognitive Memory: host-agnostic cognitive memory engine."""

from __future__ import annotations

from acm._version import __version__
from acm.api.engine import CognitiveEngine, RememberResult
from acm.observability.trace import CognitiveTraceEvent
from acm.plugins import BaseExtension, ExtensionRegistry
from acm.validation.harness import ValidationHarness

__all__ = [
    "CognitiveEngine",
    "RememberResult",
    "CognitiveTraceEvent",
    "ValidationHarness",
    "BaseExtension",
    "ExtensionRegistry",
    "__version__",
]
