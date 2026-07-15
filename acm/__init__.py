"""ACM — Aria Cognitive Memory: host-agnostic cognitive memory engine."""

from __future__ import annotations

from acm._version import __version__
from acm.api.engine import CognitiveEngine, RememberResult
from acm.authority import (
    CognitiveIntent,
    CognitiveMemoryResult,
    MemoryStatus,
    classify_memory_request,
    speak_cognitive_result,
)
from acm.observability.trace import CognitiveTraceEvent
from acm.plugins import BaseExtension, ExtensionRegistry
from acm.validation.harness import ValidationHarness

__all__ = [
    "CognitiveEngine",
    "CognitiveIntent",
    "CognitiveMemoryResult",
    "MemoryStatus",
    "RememberResult",
    "CognitiveTraceEvent",
    "ValidationHarness",
    "BaseExtension",
    "ExtensionRegistry",
    "classify_memory_request",
    "speak_cognitive_result",
    "__version__",
]
