# Changelog

All notable changes to ACM are documented here.

## [0.3.0] — 2026-07-14

### Added

- **M2 Experience organ** — immutable cognitive events answering *What happened?*
- Dual identity: external modality + internal cognitive kind
- Multidimensional salience (birth frozen; current overlay evolves)
- Temporal links (near, concurrent, revises, reflects_on, …)
- Lineage via revise/reflect (never rewrite history)
- Multimodal envelopes with equal status across modalities
- APIs: `what_happened()`, `timeline()`, `revise_experience()`, `reflect_on()`
- Docs: `EXPERIENCE_MODEL.md`, `COGNITIVE_TIMELINE.md`
- Validation harness experience metrics — schema `acm.validation/0.3`
- Behavioral, cognitive, unit, and performance experience tests

### Notes

- Concepts / Associations / Remembering organs not expanded in M2
- Aria / host wiring remains out of scope
- Self-modification of ACM architecture still requires future explicit user authorization (not implemented)

## [0.2.0] — 2026-07-14

### Added

- **M1 Identity organ** — emergent privileged schemas (`agent` / `user` / `project`)
- Identity lineage, high-impact Policy Gate (propose / assent / reject)
- Identity influence on attention, remembering, goals, and concept formation
- `who_am_i()`, `identity_snapshot()`, `assent_identity()`, `reject_identity()`
- Minimal **plugin architecture** (`ExtensionRegistry`, `BaseExtension` hooks)
- Docs: `PLUGIN_ARCHITECTURE.md`, `CORE_BOUNDARIES.md`
- Validation harness identity metrics — schema `acm.validation/0.2`
- Behavioral + cognitive identity tests; plugin unit tests

### Notes

- Identity is not personality/consciousness and not a host profile blob
- Aria / AI-Platform wiring remains out of scope

## [0.1.0] — 2026-07-14

### Added

- Standalone ACM repository and `aria-cognitive-memory` Python package
- Public API: `CognitiveEngine` (`encode`, `remember`, `sleep`, `metacognitive_sketch`, goals/context)
- M0 Validation Harness
- Cognitive trace events (metadata only; no chain-of-thought)
- Canonical design triad + documentation suite
- Tests, CI, `examples/hello_acm.py`
