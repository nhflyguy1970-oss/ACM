# Changelog

All notable changes to ACM are documented here.

## [0.32.0] — 2026-07-23

### Added — Temporal pattern recognition (M5 Cap5)

- ``TemporalPattern`` records for routines/schedules/habits/seasonal/recurring
  patterns; evidence-based observe/reinforce; idle aging to weakening/dormant/
  retired without deleting Experiences.
- Sleep ages unobserved patterns; Prediction may boost from active patterns;
  encode predictive hook observes patterns; docs ``TEMPORAL_PATTERNS.md``;
  backlog B57; learning gates L19–L20; long-duration stress test.

## [0.31.0] — 2026-07-23

### Added — Multi-level abstraction & general principles (M5 Cap4)

- ``AbstractionRecord`` lifecycle: candidate → active → refined / split /
  merged / retired; evidence threshold enforced.
- ``GeneralPrinciple`` modalities (usually / tends / commonly / rarely) —
  probabilistic, never absolute.
- Cap3 prediction audits strengthen/weaken supporting abstractions.
- Sleep may derive evidenced hierarchy abstractions; explainability APIs;
  persistence; docs ``MULTI_LEVEL_ABSTRACTION.md``; backlog B56; L17–L18.
- Invariant preserved: no Experience invention/rewrite; hierarchy integrity.

## [0.30.0] — 2026-07-23

### Added — Counterfactual reasoning & prediction audit (M5 Cap3)

- Competing ``Hypothesis`` records with lifecycle (active / disproved /
  superseded / withdrawn); closed hypotheses remain accessible.
- Append-only ``PredictionAudit`` pipeline: comparison → calibration →
  confidence update → reversible Learning Adaptations.
- Explanation APIs: ``explain_belief_change``, ``competing_hypotheses``,
  ``audit_prediction``, ``update_hypothesis``.
- Persistence of hypotheses + audits; docs ``PREDICTION_AUDIT.md``; backlog B55;
  learning gates L15–L16.
- Invariant preserved: no Experience rewrite, no provenance mutation, no invented
  autobiographical memory.

## [0.25.0] — 2026-07-19

### Added — Episodic autobiographical memory (M1)

Teaching Recognition rejected autobiographical events such as
``Yesterday I bought a kayak.`` with ``no_declarative_facts``. Temporal
reconstruction (``What happened yesterday?``, before/after anchors) had no
certified evidence path.

**Corrections (no redesign):**

- Semantic Extraction: ``FactKind.EXPERIENCE`` patterns for first-person past
  events with relative temporal cues (yesterday, last week, this morning,
  last weekday, …).
- Encode: resolve temporal cues to ``Experience.t_start``, stamp episodic
  metadata (cue / action / object / evidence), link nearest neighbors with
  ``PRECEDES`` / ``FOLLOWS``.
- Classification: expand ``experience_cue`` for buy/clean/before/after /
  explain / tell-me-about event queries.
- Remembering: reconstruct only from stored episodic experiences; evidence
  and event explanations ground in teaching provenance; unknown when
  insufficient evidence (never invent events).
- Certification: ``tests/cognitive/test_m1_episodic_memory.py`` plus full
  M0K/M0L regression.

## [0.24.0] — 2026-07-17

### Fixed — Memory explanation + active-only personal summary (M0L)

Live Aria certification showed core memory working, but explanation-style
queries failed reconstruction:

1. **Explanation cues** — ``Why isn't blue active?``, ``What replaced pizza?``,
   ``Why is brown trout active?`` classified as non-memory / general knowledge
   and returned ``no_reliable_reconstruction`` despite certified lineage.
2. **Personal summary** — ``What do you know about me?`` did not reconstruct
   from active identity + preference attributes.

**Corrections (no redesign):**

- Classification: ``memory_explanation_cue`` ahead of preference for why /
  replaced / active lineage questions.
- Remembering: evidence-backed explanation from attribute versions (active /
  retired / successor); active-only personal summary from user identity +
  ``favorite_*``; read-only (no reconsolidation).

## [0.23.0] — 2026-07-17

### Fixed — Multi-domain preference isolation + evidence lineage (M0K)

Live Aria certification showed:

1. **Domain collapse** — after teaching favorite color / food / fish, every
   query answered with the most recent preference (or conflicted). Root cause:
   cue token ``favorite`` made every ``favorite_*`` attribute answerable, and
   punctuation left ``color?`` unmatched so domain selection never fired.
2. **Evidence failure** — ``Show me the evidence.`` classified as
   ``not_memory``; scoped evidence cues were swallowed by preference
   reconstruction and returned the active value (or unknown) instead of
   lineage.

**Corrections (no redesign):**

- Cue tokens strip punctuation; favorite-domain extraction stops at the
  domain noun (``food is pizza`` → domain ``food``).
- Answerability / cue relevance require the named domain for ``favorite_*``
  keys; ``color``/``colour`` normalize as one domain so true conflicts remain.
- Evidence cues classify as remembering ahead of preference; Remembering
  reconstructs attribute version lineage (active/retired + teaching text)
  read-only (no reconsolidation).

## [0.22.0] — 2026-07-17

### Fixed — Valid preference teaching regression (Teaching Recognition)

Live Preference behavioral certification failed on a VALID teaching:

> User: "My favorite color is green."
> User: "What is my favorite color?"
> → "Your favorite color is blue."

Invalid teachings (tool wrappers, questions) were correctly rejected — the
regression was that a legitimate declarative teaching never updated memory.

**Root cause (single defect, located by full pipeline trace):** the
Cognitive Memory Response Pipeline had no declarative/teach discrimination.
"My favorite color is green." classified as intent=preference and dispatched
to the Remembering Organ as a *retrieval*, answering from the current store
("blue"). No encode was ever invoked, so extraction, supersede, persistence,
reconstruction, and evidence all operated on the stale value. (Identity
teachings such as "My name is Jeff." were similarly discarded — classified
``not_memory``.) This gap was previously pinned as a deferred decision in
``test_deferred_teach_statement_classified_as_retrieval``.

**Correction — Teaching Recognition (`acm/authority/teaching.py`):**

- `CognitiveResponsePipeline.respond` now runs a Teaching stage before
  dispatch: declarative, non-interrogative requests with extracted cognitive
  facts are encoded as trusted user statements, then dispatch proceeds so
  the reconstruction answers from the *updated* memory.
- No protection is weakened: the encode passes through the full D046
  Trusted Memory Ingestion gate and content-level artifact rejection.
  Tool/system/infra payloads are detected but rejected
  (``teaching_rejected:memory_trust`` in the reasoning path); interrogatives
  never reach the encode; evidence and retrieval requests carry no
  declarative facts and never mutate memory.
- Reasoning path exposes ``teaching_detected`` / ``teaching_encoded`` /
  ``teaching_rejected:<reason>`` for auditability.

**Certification:** fresh→unknown, teach blue→blue, teach green→green with
blue retired, re-teach green→no duplicate active attribute, restart→green,
artifacts rejected, questions non-teaching, evidence queries non-mutating —
all through ``cognitive_respond`` alone (no host-side explicit encode).
See ``tests/cognitive/test_preference_certification.py``
(``test_valid_teaching_updates_via_cognitive_respond``,
``test_teaching_recognition_never_teaches_questions_or_artifacts``).

## [0.21.0] — 2026-07-17

### Fixed — Preference Behavioral Certification (Memory Foundation completion)

Live Aria evidence showed Preferences still answering:

> Your preference is Tool \`memory_search\` worked for:
> Show the evidence for my favorite color.

Root causes (all in the standalone ACM reference implementation):

1. **Artifact classifier gap** — D047 signatures matched
   ``Tool memory_search worked for:`` but missed live backtick-quoted
   wrappers ``Tool \`memory_search\` worked for:``.
2. **Cleanup skip** — experiences with empty metadata / without
   ``semantic_extraction`` were treated as internal cognition even when
   their summary was a tool wrapper.
3. **Provenance-only trust** — hosts can mislabel tool output as trusted
   user speech; D046 evaluated declared provenance only.
4. **Interrogative / fallback preference minting** — questions and
   unmatched ``favorite`` mentions minted preference attributes
   (``conflicting?``, full tool strings) via Semantic Extraction and
   concept cues.
5. **Renderer** — reconstruction would answer from non-user artifact
   attribute values.

Corrections (architecture preserved — no organ redesign):

- Expanded artifact signatures (backtick tool wrappers, host autosave)
- Cleanup condemns content artifacts regardless of metadata survival;
  removes orphaned artifact-valued attributes; reactivates legitimate
  superseded preferences
- Content-level trust rejection in ``reject_speech_contamination``
- Interrogatives never mint preference facts or preference concept cues;
  unmatched favorite mentions no longer dump the full text as preference
- Reconstruction refuses artifact attribute values; prefers ``favorite_*``
  keys over generic ``preference``

Behavioral certification suite:
``tests/cognitive/test_preference_certification.py``

D038–D047 behavior retained. **Not promoted into Aria** until approval.

## [0.20.0] — 2026-07-17

### Added — Legacy memory contamination cleanup (D047)

- Investigated post-D046 contaminated recall: confirmed legacy-only data
  written before v0.19.0; no current encode path bypasses the trust gate
- One-time idempotent migration `cleanup_legacy_contamination`
  (`acm.provenance.legacy_cleanup`, also exposed as
  `CognitiveEngine.cleanup_legacy_contamination()`)
- D046-era records with ineligible recorded sources are removed fail-closed;
  legacy pre-D046 records are removed only on affirmative non-user artifact
  signatures (tool, memory-search, diagnostic, reflection, system, prompt,
  infrastructure, metadata)
- Legitimate user memories, identity, preferences, relationships, internal
  cognition, and valid provenance are preserved; attributes superseded by a
  contaminated encode are reactivated (probe-yellow → blue restoration)
- Fixture `tests/fixtures/pre_d046_contaminated_snapshot.json` generated by
  genuine ACM v0.18.4; decision **D047**; tests
  `tests/cognitive/test_legacy_memory_cleanup.py`
- Docs: `LEGACY_MEMORY_CLEANUP.md`

### Notes

- D046, Semantic Extraction, Reconstruction, and rendering are unchanged
- Standalone ACM only — cleanup is **not** promoted into Aria until explicit
  approval

## [Unreleased]

### Documentation — Authoritative future engineering backlog

- Consolidated 52 intentionally postponed Identity, Preference, explainability,
  diagnostic, scientific, operational, and ecosystem enhancements
- Added `FUTURE_ENHANCEMENTS_ROADMAP.md`, `ENGINEERING_BACKLOG.md`, and
  `FUTURE_RELEASE_CANDIDATES.md`
- No runtime behavior, architecture, or D045 release artifact changed

## [0.19.0] — 2026-07-17

### Fixed — Trusted Memory Ingestion (D046)

- Added explicit actor / host-operation / message-role provenance to every
  external `encode` request
- Missing, unknown, tool, assistant, system, diagnostic, retrieval, reflection,
  prompt, metadata, and infrastructure sources now reject before Semantic
  Extraction or any cognitive-memory mutation
- Genuine user statements, teachings, and corrections remain eligible
- Accepted Experience and Concept provenance records now retain source actor,
  entry operation, message role, and eligibility reason across persistence
- `revise_experience`, host-supplied `reflect_on`, identity trace, examples,
  certification, and compatibility adapter now use explicit ingestion
  provenance
- D038–D045 behavior remains unchanged; no new organs or architecture changes
- Docs: `TRUSTED_MEMORY_INGESTION.md`, `MEMORY_TRUST_MODEL.md`
- Decision **D046**; tests
  `tests/cognitive/test_trusted_memory_ingestion.py`

### Notes

- Standalone ACM only — **not** promoted into Aria until explicit approval
- v0.19.0 is a host-contract change: `encode` rejects missing provenance
- No deferred teach/query, evidence, diagnostic, editing, or presentation
  enhancement was implemented

## [0.18.4] — 2026-07-17

### Fixed — Preference reconstruction competitor admissibility (D045)

- Lexical support concepts (token nuclei, mentioned-only, cue/index concepts)
  no longer become primary answers or competing recollections
- `_answerable()` admissibility rule + lexical-metadata rendering exclusion in
  `RememberingOrgan._reconstruct` / `_format_from_concept`
- Artificial `competing_recollections` after a single healthy preference teach
  is eliminated; true semantic preference conflicts still report conflict
- Docs: `PREFERENCE_RECONSTRUCTION_FIX.md` (plus prior investigation docs)
- Decision **D045** (diagnosis + correction); tests
  `tests/cognitive/test_preference_reconstruction_fix.py`

### Notes

- Standalone ACM only — **not** promoted into Aria until explicit approval
- No new organs; no architectural redesign; deferred items (teach/query,
  evidence intent, introspection quality) unchanged

## [0.18.3] — 2026-07-16

### Fixed — Identity rendering isolation (implementation debug)

- Identity answers compose only from the requested identity (D044)
- `isolate_identity_text()` strips relationship glue / foreign names / blend forms
- `render_user_identity()` + strengthened `render_assistant_identity()`
- Pipeline + speak apply identity isolation before host speech
- Bans `you know me as`, `I am known as <user>`, user address on assistant answers
- Docs: `IDENTITY_RENDERING_ISOLATION.md`, `IDENTITY_RENDERING_PIPELINE.md`,
  `IDENTITY_CONTEXT_FILTERING.md`
- Decision **D044**; tests `tests/cognitive/test_identity_rendering_isolation.py`

### Notes

- Standalone ACM only — **not** promoted into Aria until explicit approval
- No new organs; no architectural redesign

## [0.18.2] — 2026-07-16

### Fixed — Assistant Identity pipeline (implementation debug)

- Assistant Identity is operational (config / `agent_id`), not learned user autobiography
- `kind=identity` no longer flips first-person to assistant (requires `speaker="assistant"`)
- Legacy identity signal no longer maps `my name is` onto the agent schema
- Dedicated `render_assistant_identity()` / `_assistant_identity` path (agent schema only)
- User/assistant dispatch no longer gap-fills from remembering (contamination path)
- Reject assistant name writes that collide with active user names (unless assent)
- Scrub non-operational agent names that equal the user name after user teach
- Docs: `ASSISTANT_IDENTITY.md`, `ASSISTANT_IDENTITY_PIPELINE.md`, `IDENTITY_SEPARATION.md`
- Decision **D043**; tests `tests/cognitive/test_assistant_identity_separation.py`

### Notes

- Standalone ACM only — **not** promoted into Aria until explicit approval
- No new organs; no architectural redesign

## [0.18.1] — 2026-07-16

### Fixed — Identity memory pipeline (implementation debug)

- Concept cue ingest no longer writes `mentioned`/noise onto privileged identity schemas
  (label collision on `user` from summary `User name is Jeff`)
- User-identity retrieval uses structured attribute confidence (name @ ~0.92), not schema
  nucleus confidence (~0.4)
- `_user_identity` speaks only structured autobiographical keys → clean `Your name is Jeff.`
- Observable `trace_identity_pipeline()` for encode→retrieve evidence
- Docs: `IDENTITY_PIPELINE_TRACE.md`, `IDENTITY_IMPLEMENTATION_DEBUG.md`
- Decision **D042**; tests `tests/cognitive/test_identity_pipeline_debug.py`

### Notes

- Standalone ACM only — **not** promoted into Aria until explicit approval
- No new organs; no architectural redesign

## [0.18.0] — 2026-07-16

### Added — Semantic Extraction (implementation correction)

- Package `acm.semantic` — LM/host/provider-independent Semantic Extraction
- Natural language → structured `CognitiveFact`s before organ storage
- Perspective resolution (user vs assistant vs third party)
- Instructional-language stripping (`please remember that`, …)
- Identity / relationship / preference / goal / project / location / skill extractors
- Update semantics: user identity attributes revise in place (no duplicate names)
- `encode(..., speaker=...)` optional speaker hint
- Experience.summary stores cognitive fact phrasing; original text in evidence metadata
- Docs: `SEMANTIC_EXTRACTION.md`, `IDENTITY_EXTRACTION.md`, `PERSPECTIVE_RESOLUTION.md`,
  `COGNITIVE_FACT_MODEL.md`, `FACT_EXTRACTION_RULES.md`
- Decision **D041**; tests `tests/cognitive/test_semantic_extraction.py`

### Notes

- Standalone ACM only — **not** promoted into Aria until explicit approval
- Existing organ architecture unchanged; extraction is a pipeline improvement
- D038–D040 Memory Authority / Intent / Dispatch remain intact

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
