# Changelog

All notable changes to ACM are documented here.

## [0.6.0] — 2026-07-15

### Added

- **M5 Remembering organ** — first active cognitive process answering *What do I remember?*
- **Cognitive Activation Architecture** — shared cue → spread → field for all future active organs
- Spreading activation with decay, thresholds, lateral inhibition, directional Association traversal
- Reconstruction with confidence, competing recollections / ambiguity, Experience participation (read-only)
- Public `what_do_i_remember()` / `remember()` delegated to Remembering organ
- Docs: `REMEMBERING_MODEL.md`, `REMEMBERING_DESIGN_PRINCIPLES.md`, `SPREADING_ACTIVATION.md`, `COGNITIVE_RECONSTRUCTION.md`, `COGNITIVE_ACTIVATION_ARCHITECTURE.md`
- Validation harness remembering metrics — schema `acm.validation/0.6`
- Behavioral, cognitive, unit, and performance remembering / activation tests
- Decision D018 (activation architecture + reconstruction ownership)

### Notes

- Remembering never rewrites Experiences (historical integrity)
- Forgetting not implemented — accessibility designed for future cooling without deletion
- Reflection / Learning / Prediction / Planning / Creativity not started
- Aria / host wiring remains out of scope
- Structural activation-policy changes remain assent-gated (Learning ≠ self-improvement)

## [0.5.0] — 2026-07-15

### Added

- **M4 Association organ** — living cognitive relationships answering *How is this related?*
- Directed asymmetric strengths (`strength_forward` / `strength_backward`) — D017
- Association lifecycle: birth → active/strong ⇄ dormant (+ reactivation); weaken path
- Cognitive distance bands: immediate / near / far / weak / dormant / unexpected
- Evolvable `RelationKind` vocabulary (not a closed mega-ontology)
- Experience co-activation + `belongs_with`; hierarchy mirrored as `is_a_traffic`
- Sibling `resembles`; neighborhoods + simple cognitive clusters
- Public `how_related()`; organ `neighborhood()` / `clusters()` / `observables()`
- Docs: `ASSOCIATION_MODEL.md`, `COGNITIVE_NETWORKS.md`, `ANALOGICAL_FOUNDATIONS.md`
- Validation harness association metrics — schema `acm.validation/0.5`
- Behavioral, cognitive, unit, and performance association tests

### Notes

- Remembering / Reflection / Learning / Prediction organs not started
- Analogy not implemented — architecture prepared only
- Taxonomy `is_a` remains owned by the Concept organ (D016); Associations mirror traffic
- Aria / host wiring remains out of scope
- Self-modification of ACM architecture still requires future explicit user authorization

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
