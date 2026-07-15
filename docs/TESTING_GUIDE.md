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
- [ ] `validation.snapshot()` contains schema `acm.validation/0.7`
- [ ] Identity emerges from encode experiences (not manual profile fields)
- [ ] Identity conflict proposes; assent supersedes with lineage
- [ ] `who_am_i` / remember(“Who am I?”) reconstruct from schemas + goals
- [ ] Identity metrics: growth, stability, change, confidence, influence, lineage
- [ ] Experiences immutable; revise/reflect create lineage
- [ ] `what_happened` chronological; multimodal envelopes equal
- [ ] Salience birth frozen; current overlay may evolve
- [ ] Experience harness metrics present
- [ ] Concepts emerge from Experiences (nuclei → stronger stages)
- [ ] `what_is_this` returns meaning + hierarchy/prototype when supported
- [ ] Hierarchy `is_a` forms from category language
- [ ] Concept harness metrics present (`acm.validation/0.7`)
- [ ] Associations emerge from co-activation / hierarchy mirror
- [ ] `how_related` returns relationship (direct or neighborhood)
- [ ] Directed asymmetry retained (forward ≠ reverse when appropriate)
- [ ] Neighborhoods / clusters form over related Concepts
- [ ] Association harness metrics present (`acm.validation/0.7`)
- [ ] Remembering reconstructs (not search); Experiences immutable under recall
- [ ] Spreading activation observable (propagation / decay)
- [ ] Context / identity / working influence stamps available
- [ ] Competing recollections can surface ambiguity
- [ ] Remembering harness metrics present (`acm.validation/0.7`)
- [ ] Reflection evaluates reconstructions; births Reflective Experiences
- [ ] Prior Experiences immutable under Reflection
- [ ] Uncertainty / contradiction / question outcomes available
- [ ] Activation Architecture reused (no second activation model)
- [ ] Reflection harness metrics present (`acm.validation/0.7`)

## What not to assert

- Exact internal IDs
- Prompt text / model chain-of-thought
- Host-specific Mission Control fields
