# Changelog

All notable changes to ACM are documented here.

## [0.9.0] — 2026-07-15

### Added

- **M9 Attention & Memory Priority** — *What deserves cognitive attention and continued memory investment?*
- **M10 Memory Accessibility & Forgetting** — *What should become harder to remember?* (accessibility stages; never deletes Experiences)
- Evolving Concept priority investment; Attention allocation factors from living state (not a frozen weight table)
- Accessibility lifecycle: highly accessible → … → prune-eligible (proposal only)
- Strong-cue reactivation of dormant structures via singular Activation Architecture
- Offline Cognition delegates weak-association cool to Forgetting; uses Attention for replay ranking
- Public APIs: `what_deserves_attention`, `what_should_be_harder_to_remember`, `cool_memory`, `reactivate_memory`
- Validation harness schema `acm.validation/0.9` — `attention` + `forgetting` aggregates
- Docs: `ATTENTION_MODEL.md`, `MEMORY_PRIORITY.md`, `MEMORY_ACCESSIBILITY.md`, `FORGETTING_MODEL.md`, `MEMORY_PRIORITY_LIFECYCLE.md`
- Decisions D023 (Attention≠planning), D024 (Forgetting≠deletion; Offline requests / Forgetting applies)

### Notes

- History and Experiences remain immutable
- No Prediction / Planning / Creativity / Aria
- Singular Cognitive Activation Architecture retained

## [0.8.0] — 2026-07-15

### Added

- **M7 Learning organ** — *What have I learned?* governed Adaptation Records from Reflective Experiences
- **M8 Offline Cognition** — *What should become long-term memory?* sleep/consolidation (replay, stabilize, cool, propose)
- Public APIs: `what_have_i_learned`, `learn`, `assent_adaptation` / `reject_adaptation` / `rollback_adaptation`; `sleep` delegates to Offline organ
- Validation harness schema `acm.validation/0.8` — `learning` + `offline` aggregates
- Docs: `LEARNING_MODEL.md`, `OFFLINE_COGNITION.md`, `CONSOLIDATION_MODEL.md`, `GENERALIZATION.md`, `ONLINE_OFFLINE_MEMORY.md`
- Decisions D021 (separate organs), D022 (confidence triad)
- Behavioral, cognitive, performance, and long-running learn/sleep tests

### Notes

- Experiences remain immutable; Learning never rewrites history
- Offline Cognition never invents memories or performs external I/O
- Forgetting / Prediction / Planning / Creativity / Aria not started
- Architectural self-improvement remains user-governed

## [0.7.1] — 2026-07-15

### Added (design only — no Learning organ)

- **L0 Learning research & architecture** — canonical design package for future M7
- `docs/LEARNING_ARCHITECTURE.md` — organ ownership, lineage, verbs (design)
- `docs/LEARNING_RESEARCH_FOUNDATIONS.md` — science grades + engineering translations
- `docs/COGNITIVE_RESEARCH_FOUNDATIONS.md` — permanent per-organ research ledger
- `docs/LEARNING_GOVERNANCE.md` — automatic vs assent vs never-automatic
- `docs/LEARNING_LIFECYCLE.md` — adaptation lifecycle
- `docs/ACM_ARCHITECTURE_REVIEW_M6.md` — full post-M6 architecture & roadmap review
- Decision D020 — L0 design authorization; M7 blocked until accepted
- Roadmap reconciled; Capability Map Learning (design) section

### Notes

- **No Learning / Prediction / Planning / Creativity / Forgetting implementation**
- No prototypes, no hidden Learning code
- M7 Learning remains unauthorized until L0 is accepted

## [0.7.0] — 2026-07-15

### Added

- **M6 Reflection organ** — first metacognitive organ answering *What do I think about what I remember?*
- Evaluation of Remembering reconstructions (confidence, contradiction, consistency, pattern, question, hypothesis, uncertainty)
- Reflective Experiences as immutable lineage (`reflects_on`) — never rewrite history
- Reuses shared Cognitive Activation Architecture via Remembering (no second activation model)
- Public `what_do_i_think()`; harness schema `acm.validation/0.7`
- Docs: `REFLECTION_MODEL.md`, `METACOGNITION_FOUNDATIONS.md`, `REFLECTIVE_EXPERIENCES.md`, `COGNITIVE_CAPABILITY_MAP.md`
- Decision D019 (Reflection ownership + Reflective Experiences)
- Behavioral, cognitive, unit, and performance reflection tests

### Notes

- Learning / Prediction / Planning / Creativity / Forgetting not started
- Reflection does not silently mutate Concepts or Experiences
- Aria / host wiring remains out of scope

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
