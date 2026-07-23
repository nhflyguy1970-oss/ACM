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
| L11 | Hierarchy evidence + no invented Experiences | Edges carry evidence; learn does not add Experiences |
| L12 | Hierarchy explainability deterministic | `concept_hierarchy` stable across repeated calls |
| L13 | Evidence aging never invents/deletes | `age_evidence_pass` keeps Experience + provenance counts |
| L14 | Reinforce after stale restores estimate | Learning reinforce refreshes influence / confidence |
| L15 | Hypotheses + audit never invent Experiences | Competing hypotheses + audit preserve history |
| L16 | Audit learning rollback reproducible | Adaptations from audit are reversible; comparison stable |
| L17 | Abstraction requires evidence; never invents | Insufficient evidence rejected; explain deterministic |
| L18 | Audit updates abstraction reproducibly | Hit/miss shifts abstraction confidence; comparison stable |
| L19 | Temporal patterns evidence-based | Form/reinforce cite Experiences; unknown id rejected |
| L20 | Inactive patterns weaken reproducibly | Aging lowers confidence; Experience counts unchanged |
| L21 | Explain learning preserves provenance | No internals; Experience/provenance counts unchanged |
| L22 | Explain tracks confidence change | Confidence history / evolution visible after reinforce |
| L23 | Stability check never invents | `check_learning_stability` read-only; counts unchanged |
| L24 | Enforce clamps + no recursive re-learn | Confidence bounded; second learn from same reflection is no-op |
| L25 | Diagnostic safety never invents | Inspect/evidence under B09 preserve Experience/provenance counts |

## Commands

```bash
.venv/bin/pytest tests/cognitive/test_m4_learning_certification.py -q
.venv/bin/pytest tests/cognitive/test_m5_*_learning_cert.py tests/cognitive/test_m5_learning_explainability_cert.py tests/cognitive/test_m5_learning_stability_cert.py tests/cognitive/test_diagnostic_safety_learning_cert.py -q
.venv/bin/pytest tests/ -q
.venv/bin/python scripts/acm_learning_certification.py
```

## Host idle policy

ACM exposes deterministic `sleep()` / `consolidate()` / `daily_learning_summary()`.
Hosts (e.g. Aria) decide when to invoke them. No internal schedulers.
