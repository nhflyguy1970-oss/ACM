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
- [ ] `validation.snapshot()` contains schema `acm.validation/0.3`
- [ ] Identity emerges from encode experiences (not manual profile fields)
- [ ] Identity conflict proposes; assent supersedes with lineage
- [ ] `who_am_i` / remember(“Who am I?”) reconstruct from schemas + goals
- [ ] Identity metrics: growth, stability, change, confidence, influence, lineage
- [ ] Experiences immutable; revise/reflect create lineage
- [ ] `what_happened` chronological; multimodal envelopes equal
- [ ] Salience birth frozen; current overlay may evolve
- [ ] Experience harness metrics present

## What not to assert

- Exact internal IDs
- Prompt text / model chain-of-thought
- Host-specific Mission Control fields
