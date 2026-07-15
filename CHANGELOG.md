# Changelog

All notable changes to ACM are documented here.

## [0.17.0] — 2026-07-15

### Added — End-to-End Cognitive Dispatch (architectural correction)

- `CognitiveDispatchEngine` (`acm.authority.dispatch`) — classify → ownership →
  dispatch → organ terminate → `CognitiveMemoryResult`
- Organ handlers (`acm.authority.handlers`) with forbidden-infrastructure terminals
- Multi-organ reconstruction + dispatch diagnostics on results
- Engine API: `dispatch_request`
- Docs: `COGNITIVE_DISPATCH_ENGINE.md`, `COGNITIVE_EXECUTION_PIPELINE.md`,
  `COGNITIVE_HANDLER_MODEL.md`, `ORGAN_OWNERSHIP_VALIDATION.md`,
  `COGNITIVE_DISPATCH_VALIDATION.md`, `INFRASTRUCTURE_ABSTRACTION.md`
- Decision **D040**; tests `tests/cognitive/test_cognitive_dispatch.py`

### Changed

- “How has your understanding changed?” → Reflection (+ Learning/Experiences)
- Learning answers formatted as cognitive speech (never raw adaptation dumps)
- User identity reconstruction strips assistant “I am {agent}” bleed
- Goal/project paths terminate at cognitive organs with supporting contributions

### Notes

- Standalone ACM only — **not** promoted into Aria until explicit approval
- D038 Memory Authority and D039 Intent Classification remain intact
- Certification (v0.14.0) unchanged until re-certification after promotion/acceptance

## [0.16.0] — 2026-07-15

### Added — Cognitive Intent Classification & Routing (architectural correction)

- Package updates: `acm.authority.taxonomy`, expanded `classification`, new `routing`
  (`CognitiveRoutingEngine`, `CognitiveOwnership`, `route_request`)
- Distinct `assistant_identity` vs `user_identity`; goal/project/decision/working-memory intents
- Non-cognitive taxonomy still classified by ACM (`procedural`, `planning`, `tool_request`, …)
- Uncertain classification policy: no silent LM ownership for self/shared cognitive cues
- Docs: `COGNITIVE_INTENT_CLASSIFICATION.md`, `COGNITIVE_ROUTING.md`, `INTENT_TAXONOMY.md`,
  `COGNITIVE_OWNERSHIP.md`, `QUESTION_CLASSIFICATION.md`, `COGNITIVE_ROUTING_VALIDATION.md`
- Decision **D039**; tests `tests/cognitive/test_cognitive_intent_routing.py`

### Changed

- Cognitive Response Pipeline routes via Cognitive Routing Engine
- Identity questions: “Who am I?” → user identity path (not assistant `who_am_i`)
- Goal / project questions no longer fall through as weak `general_memory` when specialized cues match

### Notes

- Standalone ACM only — **not** promoted into Aria until explicit approval
- Memory Authority (D038) remains intact and is required before speech for cognitive intents
- Certification (v0.14.0) unchanged until re-certification after promotion/acceptance

## [0.15.0] — 2026-07-15

### Added — Memory Authority architectural correction

- Package `acm.authority`: classification, `CognitiveMemoryResult`, response pipeline, speak templates, encode protection, confidence/evidence gates
- Engine APIs: `classify_request`, `cognitive_respond`, `speak_cognitive_result`
- Docs: `MEMORY_AUTHORITY_MODEL.md`, `COGNITIVE_RESPONSE_PIPELINE.md`, `MEMORY_CLASSIFICATION.md`, `HALLUCINATION_PREVENTION.md`, `UNKNOWN_MEMORY.md`, `MEMORY_PROTECTION.md`, `COGNITIVE_MEMORY_OBJECT.md`
- Decision **D038**; tests `tests/cognitive/test_memory_authority.py`

### Changed

- Remembering: refuse soft attribute confabulation when cue does not ground; UNKNOWN when ungrounded
- Reconsolidation: no confidence boost on UNKNOWN / low-confidence reconstructions
- Encode: reject LM/speech contamination tags and forbidden external kinds

### Notes

- Standalone ACM only — **not** promoted into Aria vendored copy until explicit approval
- Hosts must call ACM before language generation for memory requests
- Certification (v0.14.0) unchanged until re-certification after promotion/acceptance

## [0.14.1] — 2026-07-15

### Added (design / governance only — no organ or runtime code)

- Decisions **D036** (Aria full memory replacement via independent ACM copy) and **D037** (ACM Supremacy Rules)
- Roadmap + project history updates for Aria integration blueprint posture
- Pointer: Aria/Jarvis blueprint set at `jarvis/docs/acm_integration/`

### Notes

- No new cognition in 0.14.1 itself; cognition lands in **0.15.0** (Memory Authority)
- Standalone ACM remains research/reference relative to Aria’s vendored copy

## [0.14.0] — 2026-07-15

### Certification execution (no functional changes)

- Executed Phase 2 Operational Certification against ACM 0.13.0 baseline
- Verdict: **CERTIFIED WITH CONDITIONS** (`docs/ACM_CERTIFIED_v1.md`)
- Evidence docs: Certification Results, Shadow, Performance, Migration/Rollback Rehearsals, Long-Duration
- Raw artifacts under `docs/artifacts_*`
- Full pytest green; framework gates 8/8 pass (`certified` flag remains false by design)

### Notes

- No new features, organs, architecture, or Aria integration
- Conditions block unqualified ACM 1.0 / Aria primary cutover until Shadow is revalidated on real Aria legacy answers

## [0.13.0] — 2026-07-15

### Added (engineering only — no new cognition)

- **P2.1** Durable CognitiveStore — SQLite backend, snapshots, checksums, backup/restore, import/export
- **P2.2** Provenance model — non-fabricated lineage stamps on encode
- **P2.3** `aria_memory_adapter` — separate package; legacy API translation; feature flags; health
- **P2.4** Shadow Mode — legacy authoritative; ACM parallel compare; MC/Trace engineering metrics
- **P2.5** Certification framework — gates + report generator (`certified` always false)
- Validation harness schema `acm.validation/0.13` — storage / provenance / shadow aggregates
- Docs: CognitiveStore, Provenance, Adapter, Shadow, Certification, Operational Readiness, Migration, Rollback, Daily Use Validation
- Decisions D033–D035

### Notes

- No new cognitive organs or capabilities
- No Aria application integration
- No certification execution
- Singular Activation Architecture unchanged

## [0.12.1] — 2026-07-15

### Added (design only — no organ code)

- **Phase Gate P1** — Integration Readiness Review + Scientific Gap Analysis
- Docs: `ACM_V1_READINESS_REVIEW.md`, `SCIENTIFIC_GAP_ANALYSIS.md`, `ARIA_INTEGRATION_ARCHITECTURE.md`, `ACM_COMPARATIVE_RESEARCH.md`, `ACM_PHASE2_RECOMMENDATIONS.md`
- Decisions D031 (P1 verdict: READY WITH MINOR CHANGES), D032 (no new organs before Aria Shadow)

### Verdict

**READY WITH MINOR CHANGES** — durable CognitiveStore + Aria-side adapter Shadow required before ACM 1.0 / Aria primary memory. Planning / Decision / Aria coding not authorized by this release.

## [0.12.0] — 2026-07-15

### Added

- **M15 Memory Reconciliation** — *When memories disagree, how should memory reconcile them?*
- **M16 Uncertainty & Confidence** — *How certain am I that this memory is accurate?*
- Public APIs: `how_should_memory_reconcile`, `how_certain_am_i`
- `ReconciliationRecord` lineage artifacts (never rewrite Experiences)
- Confidence evolution events + uncertainty kinds; recalibration from corroboration/conflict
- Validation harness schema `acm.validation/0.12` — `reconciliation` + `confidence` aggregates
- Docs: `MEMORY_RECONCILIATION.md`, `CONFIDENCE_MODEL.md`, `UNCERTAINTY_MODEL.md`, `EVIDENCE_AND_CORROBORATION.md`, `HUMAN_MEMORY_CONFLICTS.md`, `ACM_MATURITY_REVIEW_v1.md`
- Decisions D029 (Reconciliation≠history rewrite), D030 (Confidence≠executive cognition)

### Notes

- Core cognitive memory lifecycle complete through M16
- No Planning / Decision Making / Executive Reasoning / Aria
- Singular Cognitive Activation Architecture retained

## [0.11.0] — 2026-07-15

### Added

- **M13 Memory Recombination** — *What new memories can emerge by recombining existing memories?*
- **M14 Analogical Reasoning** — *What existing memories are analogous even when they appear different?*
- Public APIs: `what_new_memories_can_emerge`, `what_is_analogous`
- Temporary `RecombinedMemory` / explainable `AnalogyMapping` artifacts (never Experience history)
- Recombination may use Prediction/Simulation as hints; Analogy uses structure-mapping why-codes
- Validation harness schema `acm.validation/0.11`
- Docs: `MEMORY_RECOMBINATION.md`, `ANALOGICAL_REASONING.md`, `CREATIVITY_FOUNDATIONS.md`
- Decisions D027 (Recombination≠planning), D028 (Analogy≠executive reasoning)

### Notes

- No Planning / Decision Making / Aria
- Creativity foundations documented without a separate executive Creativity organ

## [0.10.0] — 2026-07-15

### Added

- **M11 Prediction** — *Based upon memory, what is likely?* probabilistic Predicted Outcomes
- **M12 Mental Simulation** — *What possible futures can memory imagine?* hypothetical sequences (never Experience history)
- Public APIs: `what_is_likely`, `what_futures_can_memory_imagine`, `evaluate_prediction`
- Prediction accuracy feedback from later encodes; confidence evolution
- Simulation reuses Activation + optional Prediction anchors; reality wall enforced
- Validation harness schema `acm.validation/0.10` — `prediction` + `simulation` aggregates
- Docs: `PREDICTION_MODEL.md`, `MENTAL_SIMULATION.md`, `PREDICTIVE_MEMORY.md`, `HYPOTHETICAL_MEMORY.md`, `BIOLOGICAL_VS_TECHNICAL_FUNCTION.md`
- Decisions D025 (Prediction≠planning), D026 (Simulation≠history/planning)

### Notes

- No Planning / Decision Making / Creativity / Aria
- Singular Cognitive Activation Architecture retained

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
