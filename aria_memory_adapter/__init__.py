"""aria_memory_adapter — host-agnostic compatibility layer.

Separate from ACM cognition and from Aria application code.
Hosts inject a legacy backend; adapter never imports Aria.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter, time
from typing import Any, Protocol

from acm import CognitiveEngine
from acm._version import __version__ as acm_version
from acm.provenance import IngestionProvenance


class LegacyMemoryBackend(Protocol):
    """Host-supplied legacy memory — remember/recall only."""

    def remember(self, text: str, **kwargs: Any) -> dict[str, Any]: ...

    def recall(self, query: str, **kwargs: Any) -> dict[str, Any]: ...

    def health(self) -> dict[str, Any]: ...


@dataclass
class FeatureFlags:
    shadow_write: bool = True
    shadow_read: bool = True
    acm_read_primary: bool = False  # NEVER true in Phase 2 Shadow — reserved
    acm_writes_only: bool = False
    rollback_to_legacy: bool = False


@dataclass
class AdapterMetrics:
    remembers: int = 0
    recalls: int = 0
    shadow_compares: int = 0
    agreements: int = 0
    disagreements: int = 0
    errors: int = 0
    legacy_latency_ms_total: float = 0.0
    acm_latency_ms_total: float = 0.0
    last_agreement: bool | None = None
    events: list[dict[str, Any]] = field(default_factory=list)

    def record(self, event: dict[str, Any]) -> None:
        self.events.append(event)
        if len(self.events) > 2000:
            del self.events[: len(self.events) - 2000]

    def to_public(self) -> dict[str, Any]:
        return {
            "remembers": self.remembers,
            "recalls": self.recalls,
            "shadow_compares": self.shadow_compares,
            "agreements": self.agreements,
            "disagreements": self.disagreements,
            "errors": self.errors,
            "legacy_latency_ms_avg": (
                self.legacy_latency_ms_total / max(1, self.recalls + self.remembers)
            ),
            "acm_latency_ms_avg": (
                self.acm_latency_ms_total / max(1, self.recalls + self.remembers)
            ),
            "last_agreement": self.last_agreement,
            "events": list(self.events[-40:]),
        }


class NullLegacyBackend:
    """Safe default when no legacy backend is injected."""

    def remember(self, text: str, **kwargs: Any) -> dict[str, Any]:
        return {"ok": True, "text": text, "legacy": True, "id": ""}

    def recall(self, query: str, **kwargs: Any) -> dict[str, Any]:
        return {"ok": True, "query": query, "answer": "", "confidence": 0.0, "legacy": True}

    def health(self) -> dict[str, Any]:
        return {"ok": True, "backend": "null"}


class AcmMemoryAdapter:
    """Public memory interface + Shadow Mode.

    Legacy remains authoritative. ACM answers in parallel for comparison only.
    """

    def __init__(
        self,
        *,
        engine: CognitiveEngine | None = None,
        legacy: LegacyMemoryBackend | None = None,
        flags: FeatureFlags | None = None,
        agent_id: str = "adapter",
    ) -> None:
        self.engine = engine or CognitiveEngine(agent_id=agent_id)
        self.legacy = legacy or NullLegacyBackend()
        self.flags = flags or FeatureFlags()
        self.metrics = AdapterMetrics()
        self.adapter_version = "0.13.0"

    # --- capability / health -------------------------------------------------

    def capabilities(self) -> dict[str, Any]:
        return {
            "adapter_version": self.adapter_version,
            "acm_version": acm_version,
            "verbs": ["remember", "recall", "health", "capabilities", "shadow_report"],
            "shadow": True,
            "acm_read_primary": False,
            "host_coupling": False,
            "aria_import": False,
            "flags": {
                "shadow_write": self.flags.shadow_write,
                "shadow_read": self.flags.shadow_read,
                "acm_read_primary": self.flags.acm_read_primary,
                "acm_writes_only": self.flags.acm_writes_only,
                "rollback_to_legacy": self.flags.rollback_to_legacy,
            },
        }

    def health(self) -> dict[str, Any]:
        legacy_h = self.legacy.health()
        return {
            "ok": True,
            "adapter_version": self.adapter_version,
            "acm_version": acm_version,
            "legacy": legacy_h,
            "acm_experiences": len(self.engine.store.experiences),
            "acm_concepts": len(self.engine.store.concepts),
            "metrics": self.metrics.to_public(),
            "authoritative": "legacy",
        }

    # --- public memory interface ---------------------------------------------

    def remember(
        self,
        text: str,
        *,
        ingestion_provenance: IngestionProvenance | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Legacy authoritative write; optional ACM shadow encode."""
        t0 = perf_counter()
        legacy_result = self.legacy.remember(text, **kwargs)
        legacy_ms = (perf_counter() - t0) * 1000
        self.metrics.legacy_latency_ms_total += legacy_ms
        self.metrics.remembers += 1

        acm_result: dict[str, Any] | None = None
        acm_ms = 0.0
        if self.flags.shadow_write and not self.flags.rollback_to_legacy:
            try:
                t1 = perf_counter()
                acm_result = self.engine.encode(
                    text,
                    pin=True,
                    provenance=ingestion_provenance,
                )
                acm_ms = (perf_counter() - t1) * 1000
                self.metrics.acm_latency_ms_total += acm_ms
            except Exception as exc:  # noqa: BLE001 — shadow must never break legacy
                self.metrics.errors += 1
                acm_result = {"ok": False, "error": type(exc).__name__}

        event = {
            "timestamp": time(),
            "op": "remember",
            "legacy_latency_ms": round(legacy_ms, 3),
            "acm_latency_ms": round(acm_ms, 3),
            "acm_shadow": acm_result is not None,
        }
        self.metrics.record(event)
        return {
            "ok": True,
            "authoritative": "legacy",
            "legacy": legacy_result,
            "acm_shadow": acm_result,
            "timing": event,
            "user_visible_changed": False,
        }

    def recall(self, query: str, **kwargs: Any) -> dict[str, Any]:
        """Legacy authoritative recall; ACM shadow remember/compare."""
        t0 = perf_counter()
        legacy_result = self.legacy.recall(query, **kwargs)
        legacy_ms = (perf_counter() - t0) * 1000
        self.metrics.legacy_latency_ms_total += legacy_ms
        self.metrics.recalls += 1

        acm_result: dict[str, Any] | None = None
        acm_ms = 0.0
        comparison: dict[str, Any] | None = None
        if self.flags.shadow_read and not self.flags.rollback_to_legacy:
            try:
                t1 = perf_counter()
                remembered = self.engine.what_do_i_remember(query)
                certain = self.engine.how_certain_am_i(query)
                acm_ms = (perf_counter() - t1) * 1000
                self.metrics.acm_latency_ms_total += acm_ms
                acm_result = {
                    "answer": remembered.get("answer"),
                    "confidence": remembered.get("confidence"),
                    "certain": certain.get("overall_confidence"),
                    "ambiguous": remembered.get("ambiguous"),
                }
                comparison = self._compare(legacy_result, acm_result)
                self.metrics.shadow_compares += 1
                if comparison["agree"]:
                    self.metrics.agreements += 1
                else:
                    self.metrics.disagreements += 1
                self.metrics.last_agreement = comparison["agree"]
            except Exception as exc:  # noqa: BLE001
                self.metrics.errors += 1
                acm_result = {"ok": False, "error": type(exc).__name__}

        # Primary answer always legacy unless flags say otherwise (Phase 2: never)
        primary = legacy_result
        event = {
            "timestamp": time(),
            "op": "recall",
            "legacy_latency_ms": round(legacy_ms, 3),
            "acm_latency_ms": round(acm_ms, 3),
            "agreement": None if comparison is None else comparison["agree"],
        }
        self.metrics.record(event)
        return {
            "ok": True,
            "authoritative": "legacy",
            "result": primary,
            "legacy": legacy_result,
            "acm_shadow": acm_result,
            "comparison": comparison,
            "timing": event,
            "user_visible_changed": False,
            "trace": self.trace_block(legacy_result, acm_result, comparison, event),
        }

    def shadow_report(self) -> dict[str, Any]:
        return {
            "mode": "shadow",
            "authoritative": "legacy",
            "metrics": self.metrics.to_public(),
            "mission_control": self.mission_control_metrics(),
            "certified": False,
        }

    def mission_control_metrics(self) -> dict[str, Any]:
        """Engineering visibility only — no UI redesign."""
        m = self.metrics.to_public()
        return {
            "shadow_agreement": m["agreements"],
            "shadow_disagreement": m["disagreements"],
            "shadow_compares": m["shadow_compares"],
            "latency_legacy_ms_avg": m["legacy_latency_ms_avg"],
            "latency_acm_ms_avg": m["acm_latency_ms_avg"],
            "provenance_records": len(self.engine.store.provenance),
            "errors": m["errors"],
            "authoritative": "legacy",
        }

    def trace_block(
        self,
        legacy: dict[str, Any] | None,
        acm: dict[str, Any] | None,
        comparison: dict[str, Any] | None,
        timing: dict[str, Any],
    ) -> dict[str, Any]:
        """Conversation Trace engineering diagnostics."""
        return {
            "legacy_memory": {
                "used": legacy is not None,
                "confidence": None if legacy is None else legacy.get("confidence"),
            },
            "acm_memory": {
                "used": acm is not None,
                "confidence": None if acm is None else acm.get("confidence"),
            },
            "agreement": None if comparison is None else comparison.get("agree"),
            "provenance_count": len(self.engine.store.provenance),
            "timing": timing,
            "fallbacks": {"authoritative": "legacy"},
        }

    def _compare(self, legacy: dict[str, Any], acm: dict[str, Any]) -> dict[str, Any]:
        leg_ans = str(legacy.get("answer") or legacy.get("text") or "").strip().lower()
        acm_ans = str(acm.get("answer") or "").strip().lower()
        if not leg_ans and not acm_ans:
            agree = True
            reason = "both_empty"
        elif not leg_ans or not acm_ans:
            agree = False
            reason = "one_empty"
        else:
            # Token overlap — engineering heuristic, not cognitive judgment
            lt = {t for t in leg_ans.split() if len(t) > 2}
            at = {t for t in acm_ans.split() if len(t) > 2}
            if not lt or not at:
                agree = leg_ans[:40] == acm_ans[:40]
                reason = "prefix"
            else:
                overlap = len(lt & at) / max(1, len(lt | at))
                agree = overlap >= 0.25
                reason = f"token_overlap:{overlap:.2f}"
        return {
            "agree": agree,
            "reason": reason,
            "legacy_confidence": legacy.get("confidence"),
            "acm_confidence": acm.get("confidence"),
        }
