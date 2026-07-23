# Learning Certification — M4 Adaptive Memory & Learning

**Status:** Canonical certification for Learning / Offline / Governance  
**Scope:** Standalone ACM Gate 3 (learning) plus functional/behavioral prerequisites  
**Invariant:** Learning may reorganize living structure but must **never invent** Experiences or rewrite Experience history. Provenance preserved. Memory Authority and Cognitive Ownership absolute.

## Gate table

| Gate | Scenario | Expected |
|------|----------|----------|
| L1 | Reinforce after sufficient reflection | Applied Adaptation; Experience count unchanged by learn |
| L2 | Abstain on uncertainty-only | ABSTAINED record; no living-structure mutation required |
| L3 | Contradiction weaken + cool request | WEAKEN applied; Forgetting may cool accessibility |
| L4 | High-impact propose → assent → apply | Structure changes only after assent |
| L5 | Reject proposal | No living-structure change |
| L6 | Rollback after assent | Restores before snapshot |
| L7 | Host-callable sleep | consolidate runs; no timer; learning_summary attached |
| L8 | Goal importance nudge | GOAL Adaptation when cue overlaps active goal |
| L9 | Adopted knowledge boundary | External ref adopted; not autobiographical; bulk rejected |
| L10 | Full regression | `pytest tests/` green |

## Commands

```bash
.venv/bin/pytest tests/cognitive/test_m4_learning_certification.py -q
.venv/bin/pytest tests/ -q
.venv/bin/python scripts/acm_learning_certification.py
```

## Host idle policy

ACM exposes deterministic `sleep()` / `consolidate()` / `daily_learning_summary()`.
Hosts (e.g. Aria) decide when to invoke them. No internal schedulers.
