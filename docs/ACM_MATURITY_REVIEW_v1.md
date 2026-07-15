# ACM Maturity Review v1 — After M15 + M16

**Date:** 2026-07-15  
**Release under review:** v0.12.0  
**Scope:** First full maturity assessment of the core cognitive memory lifecycle after Memory Reconciliation (M15) and Uncertainty & Confidence (M16).

## Verdict

ACM now implements a **complete core cognitive memory lifecycle** for host-agnostic agents: experience → concept/association → remembering → reflection → learning → offline consolidation → attention/priority → accessibility → prediction → simulation → recombination → analogy → **reconciliation** → **confidence/uncertainty**.

Planning, Decision Making, Executive Reasoning, and Aria integration remain **intentionally out of scope** and should not be started without separate approval.

## Strengths

1. **Singular Activation Architecture** reused across active memory organs.
2. **Immutable Experiences** with living Concept/Association/confidence evolution.
3. **Explainable observables** via ValidationHarness (no prompts / CoT).
4. **Organ question discipline** — each milestone answers one cognitive memory question.
5. **Governance**: high-impact identity/learning gates; soft forgetting; no silent history rewrite.
6. **Reconciliation + Confidence** cooperate without ownership merge (lineage vs certainty).

## Weaknesses / technical debt

1. In-process `CognitiveStore` is still an informative substrate (persistence / durable media later).
2. Cue NLP remains lightweight tokenization — not a full linguistic encoder.
3. Confidence numerics are functional heuristics, not calibrated psychometrics.
4. Working-memory / Goal Space polish (M4b / M5b) still shallow relative to architecture ambition.
5. Multimodal envelopes are referenced, not fully organ-owned.
6. Analogy / recombination remain structural heuristics — not theorem-level structure-mapping.

## Scientific debt

1. Formal metacognitive calibration curves vs human FoK data.
2. Richer source-monitoring taxonomies (perception vs inference vs told).
3. Offline Cognition ↔ Reconciliation interaction under sleep needs longitudinal studies.
4. Context-dependent truth needs stronger contextual binding science→engineering mapping.

## Architectural gaps (intentional)

| Deferred | Owner when approved |
|----------|---------------------|
| Planning | Future milestone (not Memory Reconciliation) |
| Decision Making / Executive Reasoning | Future / Aria |
| Creativity as executive orchestration | Foundations in M13/M14 only |
| Safe Self-Improvement | Future gated milestone |
| Aria host adapters | Explicit host phase |

## Implementation gaps (memory-internal, optional polish)

- Goal Space organ depth
- Working buffer sophistication
- Knowledge ≠ Memory / meta-memory surfaces
- Stronger multimodal organs without core bloating (plugin pathway)

## Does ACM reduce uncertainty?

Yes — each organ makes a memory process observable and constrainable. M15/M16 explicitly target conflict and certainty. No organ introduces a second activation engine or hidden executive loop.

## Recommended roadmap after M16

1. **Pause for approval** before any Planning / Decision / Aria work.
2. Optional polish: Goal Space (M5b), Working memory (M4b), Multimodal / Knowledge≠Memory.
3. Empirical calibration of confidence against harness longitudinal runs.
4. Only then consider Planning as a **non-memory** organ with hard ACM boundary contracts.

## Capabilities intentionally excluded

Social persuasion engines; moral judges; autonomous architectural self-modification; LLM-as-memory.

## Sign-off criteria for this review

| Check | Status |
|-------|--------|
| Core lifecycle organs present | Pass |
| Experiences immutable under reconciliation | Pass |
| Confidence evolves from corroboration/conflict | Pass |
| Activation Architecture singular | Pass |
| Planning / Aria not started | Pass |
| Maturity review published | Pass (this document) |
