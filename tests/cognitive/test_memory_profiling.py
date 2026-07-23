"""B28 — Long-duration / scaling memory profiling harness (instrumented soak)."""

from __future__ import annotations

import tracemalloc
from time import perf_counter

from acm.api.engine import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def run_memory_profile(*, operations: int = 40) -> dict:
    """Encode/recall soak with RSS/tracemalloc and latency percentiles."""
    eng = CognitiveEngine(agent_id="b28-profile")
    tracemalloc.start()
    t0 = perf_counter()
    latencies: list[float] = []
    for i in range(operations):
        text = f"Session fact {i}: I prefer topic-{i % 7}."
        t1 = perf_counter()
        eng.encode(text, provenance=TRUSTED_USER_STATEMENT)
        eng.remember(f"What do I prefer about topic-{i % 7}?")
        latencies.append((perf_counter() - t1) * 1000)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    latencies.sort()
    n = len(latencies)
    p50 = latencies[n // 2]
    p95 = latencies[max(0, int(n * 0.95) - 1)]
    fp = eng.store_fingerprint()
    return {
        "schema": "acm.memory_profile.v1",
        "operations": operations,
        "elapsed_ms": round((perf_counter() - t0) * 1000, 2),
        "latency_p50_ms": round(p50, 3),
        "latency_p95_ms": round(p95, 3),
        "tracemalloc_current_kb": round(current / 1024, 1),
        "tracemalloc_peak_kb": round(peak / 1024, 1),
        "concept_count": fp["concept_count"],
        "experience_count": fp["experience_count"],
        "ok": p95 < 500.0 and peak < 200 * 1024 * 1024,
    }


def test_b28_memory_profile_smoke() -> None:
    report = run_memory_profile(operations=24)
    assert report["schema"] == "acm.memory_profile.v1"
    assert report["operations"] == 24
    assert report["experience_count"] >= 24
    assert report["ok"] is True
