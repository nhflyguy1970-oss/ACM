# Shadow Validation Results

**Executed:** 2026-07-15  
**Contract:** Legacy authoritative; ACM parallel; `user_visible_changed=false`.

## Setup

- Legacy backend: in-process list store (certification double — **not** Aria MemoryEngine)
- Adapter: `AcmMemoryAdapter` with `FeatureFlags(shadow_write=True, shadow_read=True)`
- Encoded 5 sample sentences; queried 6 cues

## Results

| Metric | Value |
|--------|------:|
| Compares | 6 |
| Agreements (token-overlap heuristic) | **0** |
| Disagreements | **6** |
| Missing legacy answers | 1 (`unknown xyz`) |
| ACM empty answers | 0 |
| Legacy latency p95 (ms) | ≈0.005 |
| ACM latency p95 (ms) | ≈1.03 |
| Overhead ratio (ACM/legacy) | ≈195× *(absolute ACM still ~1ms)* |

### Per-query notes

| Query | Agree? | Reason | Observation |
|-------|--------|--------|-------------|
| coffee | No | token_overlap:0.00 | Legacy full sentence vs ACM label reconstruction `coffee.` |
| tea | No | token_overlap:0.00 | Same format mismatch |
| harbor lights | No | token_overlap:0.00 | Same |
| sunrise | No | token_overlap:0.00 | Same |
| northward cargo | No | token_overlap:0.00 | Same |
| unknown xyz | No | one_empty | Legacy empty; ACM still returns a living concept |

## Contract checks

| Check | Result |
|-------|--------|
| Authoritative = legacy | **PASS** |
| User-visible changed | **PASS** (`false`) |
| Shadow compare recorded | **PASS** |
| Prediction/reconciliation agreement | Not scored on this synthetic batch (see Conditions) |

## Category result

**PASS WITH CONDITIONS**

### Conditions

1. Re-run against Aria real legacy recall outputs before ACM-read-primary.  
2. Treat absolute ACM latency (≈1ms here) as the performance signal; do not reject on ratio vs trivial legacy doubles.  
3. Improve or host-normalize agreement scoring **only with approval** (not performed this phase).

## Interpretation

Disagreement is **expected** when comparing full legacy strings to ACM concept reconstructions using naive token overlap. This does **not** fail the Shadow safety contract (legacy remains authoritative). It **does** block unqualified cutover evidence.
