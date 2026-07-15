# Performance Certification

**Executed:** 2026-07-15  
**Environment:** local Linux, CPython 3.x, process-local ACM

## Benchmarks (milliseconds)

| Operation | n | p50 | p95 | mean | max |
|-----------|--:|----:|----:|-----:|----:|
| encode | 30 | 0.36 | **0.42** | 0.38 | 0.61 |
| remember (`what_do_i_remember`) | 30 | 0.34 | **0.36** | 0.35 | 0.44 |
| assess (`how_certain_am_i`) | 20 | 0.05 | **0.07** | 0.06 | 0.08 |
| persist flush | 15 | 1.06 | **1.50** | 1.03 | 1.62 |

## Shadow latency

| Signal | Value |
|--------|------:|
| Legacy p95 (synthetic) | 0.005 ms |
| ACM p95 | 1.03 ms |
| Ratio | ~195× (see Shadow Conditions) |

## Storage

| Signal | Value |
|--------|------:|
| Sample SQLite size after flush workload | 4096 bytes |

## Gates vs design targets (from integration architecture)

| Target | Observation | Result |
|--------|-------------|--------|
| encode p95 < 50 ms | 0.42 ms | **PASS** |
| remember p95 < 100 ms | 0.36 ms | **PASS** |
| harness/ops acceptable | flush ~1.5 ms | **PASS** |

## Category result

**PASS**
