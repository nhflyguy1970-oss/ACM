# Changelog

All notable changes to ACM are documented here.

## [0.2.0] — 2026-07-14

### Added

- **M1 Identity organ** — emergent privileged schemas (`agent` / `user` / `project`)
- Identity lineage, high-impact Policy Gate (propose / assent / reject)
- Identity influence on attention, remembering, goals, and concept formation
- `who_am_i()`, `identity_snapshot()`, `assent_identity()`, `reject_identity()`
- Minimal **plugin architecture** (`ExtensionRegistry`, `BaseExtension` hooks)
- Docs: `PLUGIN_ARCHITECTURE.md`, `CORE_BOUNDARIES.md`
- Validation harness identity metrics (growth, stability, change, confidence, influence, lineage, evolution) — schema `acm.validation/0.2`
- Behavioral + cognitive identity tests; plugin unit tests

### Notes

- Identity is not personality/consciousness and not a host profile blob
- Aria / AI-Platform wiring remains out of scope

## [0.1.0] — 2026-07-14

### Added

- Standalone ACM repository and `aria-cognitive-memory` Python package
- Public API: `CognitiveEngine` (`encode`, `remember`, `sleep`, `metacognitive_sketch`, goals/context)
- M0 Validation Harness (activations, confidence, associations, lifecycle, working, reconsolidation, sleep, identity touches)
- Cognitive trace events (metadata only; no chain-of-thought)
- Canonical design triad: Principles, Architecture (v2.1), Test Strategy
- Documentation suite (vision, roadmap, API, developer, testing, observability, decisions, etc.)
- Unit, behavioral, and cognitive validation tests; CI workflow scaffold
- Example: `examples/hello_acm.py`
