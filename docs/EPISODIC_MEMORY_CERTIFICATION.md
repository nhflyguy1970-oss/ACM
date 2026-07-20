# M1 Certification — Episodic Autobiographical Memory

**Status:** CERTIFIED (standalone ACM)  
**Date:** 2026-07-19  
**Milestone:** M1  
**Version:** v0.25.0

---

## Scope

Standalone ACM only. Episodic cognition is **not** implemented in Aria host
routing; Aria receives this capability only by promoting the unchanged ACM
package after this certification.

---

## Definition of done

| Gate | Status |
|------|--------|
| Event teaching (5 required examples) | PASS |
| Temporal reconstruction | PASS |
| Event evidence | PASS |
| Event explanations | PASS |
| Unknown handling (no invention) | PASS |
| M0K / M0L regression | PASS |
| Full `tests/cognitive/` suite | PASS |

---

## Required teachings (encoded)

- Yesterday I bought a kayak.
- Yesterday I cleaned my garage.
- Last week I went fishing.
- This morning I installed a GPU.
- Last Tuesday I visited my brother.

Each yields ``FactKind.EXPERIENCE`` with temporal metadata and participates
in Teaching Recognition → Trusted Memory Ingestion encode.

## Required reconstruction (evidence-only)

- What happened yesterday?
- What did I buy yesterday?
- What did I clean yesterday?
- What happened last week?
- What happened before buying the kayak?
- What happened after cleaning the garage?
- Show me the evidence.
- Explain / tell-me-about event cues
- Insufficient evidence → ``unknown`` / ``I don't currently know.``

---

## Suite

```text
.venv/bin/pytest tests/cognitive/test_m1_episodic_memory.py \
  tests/cognitive/test_m0k_multi_domain_evidence.py \
  tests/cognitive/test_m0l_explanation_summary.py -q
.venv/bin/pytest tests/cognitive/ -q
```

---

## Release

| Field | Value |
|-------|-------|
| Version | `0.25.0` |
| Tag | `v0.25.0` |

Promote unchanged into Aria as `aria-acm-v0.25.0-1` after this pin.
Do **not** add Aria-side episodic cognition beyond the vendored ACM tree.
