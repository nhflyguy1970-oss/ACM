# Benchmark Strategy

Benchmarks serve cognition first, performance second.

## Categories

1. **Cognitive correctness** — preference recall, supersession, goal bias, contextual discrimination
2. **Evolution** — association growth, confidence trajectories across N encode/remember cycles
3. **Working memory** — interference under capacity pressure
4. **Sleep effects** — prune counts and proposal quality (later: merge acceptance rates)
5. **Latency / scale** — encode/remember p50/p95 at growing concept counts (informative only)

## Rules

- Do not sacrifice cognitive contracts for microbenchmarks.
- Publish workloads under `benchmarks/` with deterministic seeds when possible.
- Compare against prior ACM versions, not against host products, until adapters exist.

## M0 bar

`tests/performance/` holds a smoke latency guard (encode+remember under a modest budget). Full suite expands from M3 onward.
