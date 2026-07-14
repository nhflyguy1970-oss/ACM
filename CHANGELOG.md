# Changelog

All notable changes to ACM are documented here.

## [0.4.0] — 2026-07-14

### Added

- **M3 Concept organ** — emergent meaning answering *What is this?*
- Concept nuclei → growing → stable → mature lifecycle (+ dormant/retired)
- Hierarchy (`is_a`) inside the Concept organ (not Association organ)
- Prototypes + exemplars (D015)
- Experience binding as evidence; `what_is_this()` / `recognize()` hooks
- Docs: `CONCEPT_ARCHITECTURE.md`, `COGNITIVE_ABSTRACTION.md`, `CONCEPT_LIFECYCLE.md`
- Validation harness concept metrics — schema `acm.validation/0.4`
- Behavioral, cognitive, unit, and performance concept tests

### Notes

- Associations / Remembering / Reflection / Learning organs not started
- Aria / host wiring remains out of scope
- Self-modification of ACM architecture still requires future explicit user authorization

## [0.3.0] — 2026-07-14

### Added

- **M2 Experience organ** — immutable cognitive events answering *What happened?*
- Dual identity, salience overlays, temporal lineage, multimodal envelopes
- Docs: `EXPERIENCE_MODEL.md`, `COGNITIVE_TIMELINE.md`
- Validation schema `acm.validation/0.3`

## [0.2.0] — 2026-07-14

### Added

- **M1 Identity organ** — *Who am I?*
- Plugin architecture + core boundaries
- Validation schema `acm.validation/0.2`

## [0.1.0] — 2026-07-14

### Added

- Standalone ACM foundation, M0 harness, docs suite, CI
