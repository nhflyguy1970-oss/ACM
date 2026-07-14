# Testing Guide

Canonical contracts live in [`COGNITIVE_MEMORY_TEST_STRATEGY.md`](COGNITIVE_MEMORY_TEST_STRATEGY.md). This file is the practical how-to.

## Suites

| Path | Purpose |
|------|---------|
| `tests/unit/` | Types, attention, buffer, store helpers |
| `tests/behavioral/` | Encode / remember / sleep user-visible contracts |
| `tests/cognitive/` | Validation harness + reconsolidation / identity observables |
| `tests/performance/` | Lightweight latency/size guards (grow with milestones) |

## Commands

```bash
pytest
pytest tests/cognitive -q
pytest --cov=acm --cov-report=term-missing
```

## Cognitive validation checklist (M0)

- [ ] Encode preference → remember returns preference-class answer
- [ ] Superseding encode marks prior attribute inactive + reconsolidation event
- [ ] `remember` records activation + light reconsolidation
- [ ] Working buffer displaces under capacity pressure
- [ ] `sleep` prunes weak edges; merge proposals are not silently applied
- [ ] Explanations are template classes only
- [ ] `validation.snapshot()` contains schema `acm.validation/0.1`

## What not to assert

- Exact internal IDs
- Prompt text / model chain-of-thought
- Host-specific Mission Control fields
