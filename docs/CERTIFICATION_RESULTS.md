# Certification Results — Execution Log

**Executed:** 2026-07-15  
**Baseline package:** ACM 0.13.0  
**Method:** Run existing `CertificationFramework` + extended measurement script + full pytest.  
**Code changes during run:** None.

## Framework gates

| Gate | Pass | Duration (ms) | Detail |
|------|------|---------------|--------|
| persistence_roundtrip | Yes | ~9.7 | experiences restored |
| checksum_integrity | Yes | ~8.4 | checksum ok |
| backup_restore | Yes | ~16.8 | restore ok |
| provenance_stamped | Yes | ~0.4 | provenance present |
| shadow_legacy_authoritative | Yes | ~0.4 | legacy authoritative |
| adapter_capabilities | Yes | ~0.1 | capabilities ok |
| performance_encode_p95 | Yes | ~6.9 | encode p95≈0.4ms |
| long_duration_smoke | Yes | ~3.0 | long smoke ok |

**Totals:** 8/8 passed. Report field `certified` remains **false** (framework rule).

## Extended execution

| Suite | Result |
|-------|--------|
| Shadow validation | PASS WITH CONDITIONS (see dedicated doc) |
| Long-duration | PASS (40 ops / 0 errors) |
| Persistence | PASS |
| Migration rehearsal | PASS (Aria not touched) |
| Rollback rehearsal | PASS |
| Performance | PASS |
| Provenance sampling | PASS |
| Confidence path | PASS |
| Full pytest | PASS (100%) |
| Daily Use simulation | PASS |

## Verdict linkage

See [`ACM_CERTIFIED_v1.md`](ACM_CERTIFIED_v1.md): **CERTIFIED WITH CONDITIONS**.

## Raw data

`artifacts_raw_certification_results.json` · `artifacts_framework_report.json` · `artifacts_pytest_certification.txt`
