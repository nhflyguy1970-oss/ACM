# ACM Certification — v1

**Date:** 2026-07-15  
**Subject under test:** ACM `v0.13.0` (operational baseline)  
**Report release:** `v0.14.0` (certification evidence only — no functional changes)  
**Scope:** Execute Phase 2 certification framework only. No new features, organs, architecture, or Aria integration.

---

## FINAL VERDICT

# CERTIFIED WITH CONDITIONS

ACM is **operationally certified** as a host-independent cognitive memory library for Shadow dual-write readiness, **subject to conditions** before declaring unqualified **ACM 1.0** as Aria’s sole authoritative memory.

ACM is **not** authorized for Aria primary cutover by this document alone.

---

## Category results

| Category | Result | Evidence summary |
|----------|--------|------------------|
| Framework gates (8/8) | **PASS** | All gates green; internal flag `certified=false` by design |
| Shadow validation | **PASS WITH CONDITIONS** | Legacy authoritative preserved; lexical agreement 0/6 on synthetic backend (format mismatch) |
| Long-duration validation | **PASS** | 40 ops, 0 errors |
| Persistence validation | **PASS** | Checksums OK; recover/restore/import OK |
| Migration rehearsal | **PASS** | 15/15 experiences + 30/30 provenance; Aria not migrated |
| Rollback rehearsal | **PASS** | Baseline preserved; 0 orphan provenance refs; adapter rollback flag works |
| Performance | **PASS** | Encode p95 ≈0.42ms; remember p95 ≈0.36ms; flush p95 ≈1.5ms |
| Provenance | **PASS** | 20/20 samples complete; 0 fabricated; 0 circular |
| Confidence | **PASS** | Assessment + conflict recalibration path exercised |
| Validation harness / pytest | **PASS** | Full suite green (140 tests) |
| Daily Use simulation | **PASS** | Representative organ cycle, 0 errors |

---

## Conditions (blocking for unqualified ACM 1.0 / Aria primary)

1. **Shadow agreement must be re-measured against real Aria legacy `MemoryEngine` answers** (or an approved answer-normalization layer). Synthetic sentence-vs-label overlap is **not** sufficient for cutover evidence.  
2. **Shadow overhead must be judged in absolute milliseconds against host SLOs**, not only as a ratio vs a trivial Null/test legacy backend. Absolute ACM recall ≈1ms in this run; production legacy latency baseline required.  
3. **Explicit approval** remains required before Aria application wiring and before setting `acm_read_primary`.

## Non-conditions (already satisfied)

- Durable store integrity, backup/restore, import/export  
- Provenance non-fabrication on encode  
- Adapter isolation (no Aria imports)  
- Legacy authoritative Shadow contract (`user_visible_changed=false`)  
- No new cognition introduced during certification  

---

## Explicitly not authorized

- Aria integration coding  
- Replacing Aria memory  
- Claiming framework `certified=true`  
- Silent repair of Shadow lexical scoring without approval  

---

## Evidence artifacts

- `docs/CERTIFICATION_RESULTS.md`  
- `docs/SHADOW_VALIDATION_RESULTS.md`  
- `docs/PERFORMANCE_CERTIFICATION.md`  
- `docs/MIGRATION_REHEARSAL.md`  
- `docs/ROLLBACK_REHEARSAL.md`  
- `docs/LONG_DURATION_VALIDATION.md`  
- `docs/artifacts_raw_certification_results.json`  
- `docs/artifacts_framework_report.json`  
- `docs/artifacts_pytest_certification.txt`  

---

## Sign-off ask

Approve remediation of Condition 1–2 under a follow-on cert delta **or** approve Aria integration in Shadow-only mode while Conditions remain active. Do **not** approve ACM-read-primary until Conditions 1–2 are closed.
