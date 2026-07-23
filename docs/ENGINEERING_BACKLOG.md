# ACM Engineering Backlog

**Status:** Authoritative backlog  
**Established:** 2026-07-17, after D045  
**Scope:** Future ACM engineering and research; no item is authorized merely by
appearing here.

This document is the detailed source of truth for intentionally postponed
enhancements. `FUTURE_ENHANCEMENTS_ROADMAP.md` defines ordering and governance;
`FUTURE_RELEASE_CANDIDATES.md` groups items into possible releases. Historical
documents remain evidence, but new backlog decisions must update this file.

## Status and complexity

- **READY** — bounded, evidence-supported, and suitable for a focused proposal.
- **DEPENDENT** — bounded, but requires listed prerequisites.
- **DEFERRED** — intentionally postponed pending a product/scope decision.
- **RESEARCH** — requires investigation or measurement before implementation.
- **FUTURE** — valid long-range candidate without present scheduling.
- Complexity: **S** (small), **M** (medium), **L** (large), **XL** (program).

## Backlog

### B01 — Declarative teach vs query recognition

- **Status / order / complexity:** COMPLETE · 1 · M
- **Completed:** 2026-07-22 (Teaching Recognition already landed; contract + matrix certified)
- **Purpose:** Distinguish statements that teach memory from questions that
  request reconstruction.
- **Problem:** `My favorite color is blue.` currently classifies as preference
  retrieval because the cue classifier does not model utterance function.
- **Why deferred:** Explicitly excluded from D045 to keep that correction inside
  reconstruction.
- **Architectural impact:** Classification/encode orchestration only; preserve
  Cognitive Ownership and Memory Authority. No new organ.
- **Dependencies:** A written teach/query contract and negative corpus.
- **Behavioral example:** Teach statement → encode acknowledgement; `What is my
  favorite color?` → Remembering reconstruction.
- **Validation:** Declarative/interrogative/imperative matrix across Identity,
  Preference, Goals, Projects, and non-cognitive text; no silent host bypass.
- **Promotion:** Standalone release, certify behavioral corpus, then explicit
  vendored promotion.
- **Implementation references:**
  - `acm/authority/teaching.py` — `detect_teaching`
  - `acm/authority/pipeline.py` — `_teach_if_declarative`
  - `docs/TEACH_QUERY_CONTRACT.md`
  - `tests/cognitive/test_teach_query_matrix.py`
  - `tests/cognitive/test_preference_certification.py`
- **Sources:** `PREFERENCE_INTROSPECTION.md`,
  `PREFERENCE_RECONSTRUCTION_FIX.md`, D045 diagnostic tests.

### B02 — Evidence introspection intent

- **Status / order / complexity:** COMPLETE · 2 · M
- **Completed:** 2026-07-22 (evidence_cue precedes preference_cue; certified)
- **Purpose:** Recognize requests to inspect evidence without confusing them
  with the remembered subject.
- **Problem:** `Show the evidence for my favorite color` is classified as a
  preference query because `preference_cue` wins.
- **Why deferred:** Intent taxonomy and routing were non-goals for D045.
- **Architectural impact:** Likely a bounded intent/handler contract using
  existing provenance and result evidence; must not create a storage/search
  authority.
- **Dependencies:** B01 utterance-function rules; evidence response contract.
- **Behavioral example:** Evidence question → evidence view, not another
  preference answer.
- **Validation:** Classification precedence, organ ownership, unknown evidence,
  conflicting evidence, and no raw-storage dumps.
- **Promotion:** Standalone classification/dispatch certification, then host
  integration tests before promotion.
- **Implementation references:**
  - `acm/authority/classification.py` — `evidence_cue` (confidence 0.95) before
    `preference_cue`
  - Remembering evidence / lineage reconstruction paths
  - Preference certification + pipeline debug suites
- **Sources:** `PREFERENCE_INTROSPECTION.md`,
  `COGNITIVE_INTENT_CLASSIFICATION.md`, `COGNITIVE_HANDLER_MODEL.md`.

### B03 — Memory evidence presentation

- **Status / order / complexity:** COMPLETE · 3 · M
- **Completed:** 2026-07-23 (M4 AML C5)
- **Implementation references:**
  - `acm/authority/evidence_present.py`
  - `acm/authority/inspect_api.py` (`presentation` block)
  - `tests/cognitive/test_m4_aml_capabilities.py`
- **Purpose:** Present supporting Experiences, concepts, and corroboration in
  concise user-facing language.
- **Problem:** Evidence already exists in `CognitiveMemoryResult`, but callers
  receive IDs or generic status speech rather than an intelligible explanation.
- **Why deferred:** Requires an approved presentation contract and privacy
  policy; not needed to correct reconstruction.
- **Architectural impact:** Read-only rendering over existing evidence. Never
  infer new evidence or expose substrate records verbatim.
- **Dependencies:** B02, B14, B29.
- **Behavioral example:** “You told me on July 17 that your favorite color is
  blue; one experience supports it.”
- **Validation:** Golden renderings, missing/redacted evidence, fabricated=false,
  bounded output, no identity/context leakage.
- **Promotion:** Standalone renderer tests followed by host speech/UX validation.
- **Sources:** `PROVENANCE_MODEL.md`, `EVIDENCE_AND_CORROBORATION.md`,
  `PREFERENCE_INTROSPECTION.md`.

### B04 — Conflict explanation

- **Status / order / complexity:** COMPLETE · 4 · M
- **Completed:** 2026-07-22
- **Implementation references:** `acm/authority/handlers.py` competing speech; `tests/cognitive/test_conflict_explanation.py`
- **Purpose:** Name the actual semantic recollections that conflict and why they
  were admitted.
- **Problem:** Reflection records `contradictions[]`, but terminal speech says
  only that multiple interpretations remain plausible.
- **Why deferred:** Reflection explanation quality was explicitly excluded from
  D045.
- **Architectural impact:** Rendering and structured explanation only; preserve
  Reconciliation ownership and conflict gates.
- **Dependencies:** D045 answerability invariants; B03 recommended.
- **Behavioral example:** “I have blue from one experience and red from another;
  both answer favorite color with similar activation.”
- **Validation:** True semantic conflicts only, no lexical rivals, deterministic
  competitor ordering, redaction, and unknown handling.
- **Promotion:** Standalone behavioral certification, then host presentation
  validation.
- **Sources:** `PREFERENCE_INTROSPECTION.md`,
  `MEMORY_RECONCILIATION.md`, `REFLECTION_MODEL.md`.

### B05 — Explainable confidence

- **Status / order / complexity:** COMPLETE · 5 · M
- **Completed:** 2026-07-22
- **Implementation references:** `acm/confidence/organ.py` factor narrative; `tests/cognitive/test_explainability_ready_items.py`
- **Purpose:** Explain which evidence and events raised or lowered confidence.
- **Problem:** Confidence is dynamic and auditable internally, but users see a
  scalar or generic low-confidence refusal.
- **Why deferred:** Calibration and presentation were not part of D038–D045.
- **Architectural impact:** Read-only view over ConfidenceSnapshot/Event and
  provenance; no executive action thresholds.
- **Dependencies:** B03 and B14; calibration work B22 is optional.
- **Behavioral example:** “Confidence is 0.78 because two experiences corroborate
  this; one recent contradiction lowered it.”
- **Validation:** Event-to-explanation traceability, monotonic explanation checks,
  conflict/corroboration cases, no invented causes.
- **Promotion:** Standalone explanation contract, host display validation.
- **Sources:** `CONFIDENCE_MODEL.md`, `EVIDENCE_AND_CORROBORATION.md`,
  `ACM_MATURITY_REVIEW_v1.md`.

### B06 — Explainable uncertainty

- **Status / order / complexity:** COMPLETE · 6 · M
- **Completed:** 2026-07-22
- **Implementation references:** `acm/authority/speak.py` `_UNCERTAINTY_SPEECH`; explainability tests
- **Purpose:** Distinguish no evidence, low accessibility, conflict, stale
  evidence, prediction uncertainty, and learning uncertainty.
- **Problem:** Status labels exist, but user-facing explanations often collapse
  to generic “I don’t know” or `competing_recollections`.
- **Why deferred:** D038 established honest gates, not a complete explanation UX.
- **Architectural impact:** Renderer over existing uncertainty taxonomy; no new
  uncertainty organ.
- **Dependencies:** B05; B26 for richer retrieval-failure distinctions.
- **Behavioral example:** “I have evidence, but two active values conflict” vs
  “I have no relevant experience.”
- **Validation:** One golden case per uncertainty kind, mixed-kind precedence,
  safe fallback, language/status consistency.
- **Promotion:** Standalone behavioral suite, then host speech validation.
- **Sources:** `UNCERTAINTY_MODEL.md`, `MEMORY_AUTHORITY_MODEL.md`,
  `authority/gates.py`.

### B07 — Read-only diagnostic mode

- **Status / order / complexity:** COMPLETE · 1 · L
- **Completed:** 2026-07-22
- **Purpose:** Inspect cognition without reconsolidation, reflection birth,
  confidence deltas, working-buffer writes, or learning adaptations.
- **Problem:** Diagnostic questions can alter the memory being inspected.
- **Why deferred:** Diagnostic mutation was explicitly outside D045.
- **Architectural impact:** Cross-cutting execution-mode contract; must preserve
  normal biologically inspired update-on-retrieval behavior by default.
- **Dependencies:** Mutation inventory and transaction/before-after assertions.
- **Behavioral example:** `inspect("favorite color")` returns reconstruction and
  evidence while store hashes and counters remain unchanged.
- **Validation:** Deep snapshots before/after every organ path; persistence and
  restart checks; normal mode still mutates as designed.
- **Promotion:** Standalone-only certification first; hosts consume only after
  safe API contract is frozen.
- **Implementation references:**
  - `acm/authority/mode.py` — `ExecutionMode`, `read_only()`, `is_read_only()`
  - `CognitiveEngine.inspect` / `store_fingerprint` / diagnostics.execution_mode
  - Mutation gates in remembering, reflection, learning, prediction,
    reconciliation, simulation, attention, forgetting, associations, pipeline
  - `docs/READ_ONLY_DIAGNOSTIC_MODE.md`
  - `tests/cognitive/test_read_only_diagnostic_mode.py`
- **Sources:** `PREFERENCE_INTROSPECTION.md`,
  `MEMORY_DESIGN_PRINCIPLES.md`, D045 diagnostic evidence.

### B08 — Non-mutating inspection APIs

- **Status / order / complexity:** COMPLETE · 2 · M
- **Completed:** 2026-07-22
- **Purpose:** Provide stable APIs for reconstruction, evidence, confidence,
  identity, and conflict inspection.
- **Problem:** Today callers must use cognitive APIs whose side effects are
  intentional for ordinary recall but unsafe for diagnostics.
- **Why deferred:** Requires B07’s execution semantics.
- **Architectural impact:** Read-model façades over organs; no duplicate
  cognition and no direct store authority.
- **Dependencies:** B07 (COMPLETE).
- **Behavioral example:** `inspect_reconstruction(cue)` returns the same ranked
  semantic candidates without reconsolidating.
- **Validation:** Equality with normal pre-mutation reconstruction, zero-write
  assertions, concurrency and persistence checks.
- **Promotion:** Standalone API stabilization; adapter/host contract tests before
  promotion.
- **Implementation references:**
  - `acm/authority/inspect_api.py`
  - `CognitiveEngine.inspect_reconstruction|evidence|confidence|identity|conflict`
  - `docs/INSPECT_APIS.md`
  - `tests/cognitive/test_inspect_apis.py`
- **Sources:** `PREFERENCE_INTROSPECTION.md`, `PLUGIN_ARCHITECTURE.md`.

### B09 — Diagnostic safety policy

- **Status / order / complexity:** DEPENDENT · 3 · M
- **Purpose:** Define what diagnostic output may expose and which operations are
  forbidden.
- **Problem:** Raw provenance, identity values, context, and storage structures
  can leak through debugging surfaces.
- **Why deferred:** Needs read-only APIs and privacy decisions first.
- **Architectural impact:** Policy/sanitization layer over diagnostics; preserve
  host independence and Memory Authority.
- **Dependencies:** B07 (COMPLETE), B08 (COMPLETE), B29.

- **Behavioral example:** Diagnostics show evidence classes and redacted values,
  never unrelated user/assistant identity or raw DB rows.
- **Validation:** Adversarial leakage corpus, foreign-identity filtering,
  deterministic redaction, disabled-by-default production policy.
- **Promotion:** Security/privacy review before any host exposure.
- **Sources:** `HALLUCINATION_PREVENTION.md`,
  `IDENTITY_CONTEXT_FILTERING.md`, `authority/handlers.py`.

### B10 — Conversation-safe debugging

- **Status / order / complexity:** DEPENDENT · 4 · L
- **Purpose:** Trace live conversational cognition without contaminating the
  autobiographical store or influencing subsequent activation.
- **Problem:** Logging a question as an Experience can alter cue strength and
  behavior, as the D045 investigation demonstrated.
- **Why deferred:** Needs diagnostic isolation and an explicit conversation
  capture policy.
- **Architectural impact:** Host/engine boundary and observability; no alternate
  memory path.
- **Dependencies:** B07–B09, B27.
- **Behavioral example:** Capture classify→route→reconstruct trace while repeated
  debugging leaves answer and store unchanged.
- **Validation:** Replay equivalence, no new Experience/Concept/Association,
  concurrency, restart, and long-session tests.
- **Promotion:** Shadow-only host rollout, then explicit operator enablement.
- **Sources:** D045 trace documents, `SHADOW_MODE.md`,
  `COGNITIVE_EXECUTION_PIPELINE.md`.

### B11 — Preference editing UX

- **Status / order / complexity:** DEPENDENT · 7 · M
- **Purpose:** Let users view and intentionally edit active preferences.
- **Problem:** Current encode semantics support updates, but there is no explicit,
  explainable edit interaction.
- **Why deferred:** Preference editing UX was excluded from D045.
- **Architectural impact:** Existing semantic fact/update operations; no direct
  store edits and no new organ.
- **Dependencies:** B01, B03, B08.
- **Behavioral example:** “Change my favorite color to red” previews old/new
  values and records lineage.
- **Validation:** Set/replace/remove/cancel, repeated edits, persistence,
  provenance, and unrelated-preference isolation.
- **Promotion:** Standalone API certification, then host UX/manual validation.
- **Sources:** `PREFERENCE_RECONSTRUCTION_FIX.md`,
  `COGNITIVE_FACT_MODEL.md`.

### B12 — Preference correction UX

- **Status / order / complexity:** DEPENDENT · 8 · M
- **Purpose:** Distinguish a correction from a new preference observation and
  preserve correction lineage.
- **Problem:** “Actually…” works through SET semantics, but correction intent and
  explanation are implicit.
- **Why deferred:** D045 preserved storage and preference-editing behavior.
- **Architectural impact:** Semantic update metadata and presentation; preserve
  immutable Experiences.
- **Dependencies:** B01, B11, B14.
- **Behavioral example:** “Actually, red” retires blue, activates red, and
  explains that the user corrected the prior value.
- **Validation:** Correction phrases, ambiguous referents, rollback/cancel,
  confidence and provenance lineage.
- **Promotion:** Standalone behavioral release before vendored promotion.
- **Sources:** `SEMANTIC_EXTRACTION.md`, `PREFERENCE_RECONSTRUCTION_FIX.md`.

### B13 — User-assisted conflict resolution

- **Status / order / complexity:** DEPENDENT · 9 · L
- **Purpose:** Ask the user to confirm which true semantic recollection should
  remain active without silently discarding evidence.
- **Problem:** Reconciliation exposes conflict but lacks a complete interactive
  confirmation workflow.
- **Why deferred:** Requires UX, assent, and read-only conflict explanation;
  outside reconstruction correction.
- **Architectural impact:** Reconciliation + Policy Gate interaction; Experiences
  remain immutable and old facts retain lineage.
- **Dependencies:** B04, B08, B12, B20 patterns.
- **Behavioral example:** “I have blue and red. Which is current?” → user confirms
  red → blue retired with reconciliation record.
- **Validation:** confirm/reject/abstain, malformed answers, persistence,
  provenance, no last-write-wins loss.
- **Promotion:** Standalone interactive contract, then host UX and rollback
  certification.
- **Sources:** `MEMORY_RECONCILIATION.md`, `LEARNING_GOVERNANCE.md`.

### B14 — Memory provenance presentation

- **Status / order / complexity:** COMPLETE · 2 · M
- **Completed:** 2026-07-22
- **Implementation references:** `acm/remembering/relations.py` answer provenance; explainability tests
- **Purpose:** Convert provenance graphs into bounded, comprehensible source
  explanations.
- **Problem:** Provenance is present and certified but mostly machine-oriented.
- **Why deferred:** Operational certification required presence, not user-facing
  presentation.
- **Architectural impact:** Read-only projection; provenance remains the source
  of truth.
- **Dependencies:** Redaction contract B29.
- **Behavioral example:** “This came from an experience you provided, not an
  inference or simulation.”
- **Validation:** Every origin type, parent chains, fabricated=false, cycles,
  missing artifacts, bounded depth.
- **Promotion:** Standalone schema/rendering tests, host Trace/UI validation.
- **Sources:** `PROVENANCE_MODEL.md`, `CERTIFICATION_RESULTS.md`.

### B15 — Rich source-monitoring taxonomy

- **Status / order / complexity:** RESEARCH · 12 · L
- **Purpose:** Distinguish told, perceived, inferred, imported, reconstructed,
  reflected, and simulated sources as first-class metadata.
- **Problem:** Current origin/explanation fields are useful but not a complete
  source-monitoring model.
- **Why deferred:** Identified as scientific polish; schema and migration effects
  require research.
- **Architectural impact:** Experience/Concept/provenance schema enrichment, not
  a new organ.
- **Dependencies:** Source taxonomy proposal, persistence migration, B14.
- **Behavioral example:** “You told me this” vs “I inferred this” vs “This was a
  simulation.”
- **Validation:** Source propagation, mixed-source confidence, import/export,
  persistence migration, no fabricated source claims.
- **Promotion:** Research decision → standalone schema release → migration
  certification → explicit host promotion.
- **Sources:** `SCIENTIFIC_GAP_ANALYSIS.md`,
  `ACM_PHASE2_RECOMMENDATIONS.md`.

### B16 — Memory age explanation

- **Status / order / complexity:** COMPLETE · 6 · S
- **Completed:** 2026-07-22
- **Implementation references:** `RememberingOrgan._reconstruct_age`; `memory_age_cue`
- **Purpose:** Explain when supporting evidence was formed and how recency affects
  the answer.
- **Problem:** Timestamps exist, but users cannot ask how old a memory is.
- **Why deferred:** Presentation polish, not required for correctness.
- **Architectural impact:** Read-only temporal projection over Experiences and
  timeline.
- **Dependencies:** B03; redaction/time-format policy.
- **Behavioral example:** “The supporting experience is two weeks old; it has not
  been reconfirmed.”
- **Validation:** Clock-independent tests, multiple ages, unknown timestamps,
  timezone and privacy handling.
- **Promotion:** Standalone renderer tests, host locale validation.
- **Sources:** `COGNITIVE_TIMELINE.md`, `EXPERIENCE_MODEL.md`.

### B17 — Memory strength and accessibility explanation

- **Status / order / complexity:** COMPLETE · 7 · M
- **Completed:** 2026-07-22
- **Implementation references:** `RememberingOrgan._reconstruct_accessibility`; `accessibility_cue`
- **Purpose:** Explain strength, accessibility, attention, and forgetting without
  conflating them with truth/confidence.
- **Problem:** Users cannot tell whether recall is weak because evidence is
  doubtful or because a memory is currently hard to access.
- **Why deferred:** M9/M10 implemented mechanisms, not full explanatory UX.
- **Architectural impact:** Read-only projection across Attention, Forgetting,
  Activation, and Confidence with strict ownership labels.
- **Dependencies:** B05, B06.
- **Behavioral example:** “The memory is well-supported but currently less
  accessible because it has not been activated recently.”
- **Validation:** Orthogonal confidence/accessibility cases, dormant/reactivated
  states, no causal overclaim.
- **Promotion:** Standalone behavioral suite then host presentation.
- **Sources:** `MEMORY_PRIORITY_LIFECYCLE.md`, `FORGETTING_MODEL.md`,
  `CONFIDENCE_MODEL.md`.

### B18 — Reflection explanation improvements

- **Status / order / complexity:** COMPLETE · 10 · M
- **Completed:** 2026-07-23 (M4 AML C6)
- **Implementation references:**
  - `acm/reflection/explain.py`
  - `acm/authority/handlers.py` reflection path
  - `tests/cognitive/test_m4_aml_capabilities.py`
- **Purpose:** Render contradictions, consistencies, patterns, questions, and
  hypotheses already produced by Reflection.
- **Problem:** Generic reflection summaries discard structured explanatory
  fields.
- **Why deferred:** Explicit D045 non-goal.
- **Architectural impact:** Reflection result/handler rendering only; no chain of
  thought and no Learning-policy change.
- **Dependencies:** B04, B07, B29.
- **Behavioral example:** “I marked this contradictory because these two
  semantic values both answer the cue.”
- **Validation:** Structured-field fidelity, no hidden reasoning exposure,
  read-only mode, bounded output.
- **Promotion:** Standalone explanation release then host speech validation.
- **Sources:** `PREFERENCE_INTROSPECTION.md`, `REFLECTION_MODEL.md`,
  `METACOGNITION_FOUNDATIONS.md`.

### B19 — Identity evidence and provenance presentation

- **Status / order / complexity:** COMPLETE · 8 · M
- **Completed:** 2026-07-22
- **Implementation references:** provenance speech for identity facts; D043/D044 isolation preserved
- **Purpose:** Explain which user or assistant schema attribute supports an
  identity answer while preserving D043/D044 isolation.
- **Problem:** Identity answers are correctly isolated but offer no safe evidence
  view.
- **Why deferred:** Identity certification prioritized separation and leakage
  prevention.
- **Architectural impact:** Target-scoped renderer over identity attributes and
  provenance; relationship data only on explicit relationship requests.
- **Dependencies:** B03, B14, D044 filtering invariants.
- **Behavioral example:** “I know your preferred name from your explicit ‘Call me
  Jeffrey’ statement”; assistant evidence never includes user facts.
- **Validation:** user/assistant/relationship matrices, foreign-value stripping,
  absent evidence, persistence.
- **Promotion:** Standalone Identity behavioral certification, then host
  promotion.
- **Sources:** `IDENTITY_CONTEXT_FILTERING.md`,
  `IDENTITY_SEPARATION.md`, D043/D044 tests.

### B20 — Identity correction and assent UX

- **Status / order / complexity:** DEPENDENT · 11 · L
- **Purpose:** Make identity changes explicit, reviewable, and reversible under
  the existing Policy Gate.
- **Problem:** Schema update/assent mechanisms exist, but conversational
  correction UX is incomplete.
- **Why deferred:** D042–D044 corrected implementation fidelity, not identity
  management UX.
- **Architectural impact:** Identity + Policy Gate presentation; no weakening of
  user/assistant separation.
- **Dependencies:** B01, B19; existing assent policy.
- **Behavioral example:** “My legal name changed…” → preview impact → explicit
  assent → lineage-preserving update.
- **Validation:** approve/reject/cancel, collision prevention, user/assistant
  isolation, restart and rollback.
- **Promotion:** Separate standalone Identity release and recertification before
  host promotion.
- **Sources:** `IDENTITY_MODEL.md`, `IDENTITY_SEPARATION.md`,
  `LEARNING_GOVERNANCE.md`.

### B21 — Explicit relationship-memory presentation

- **Status / order / complexity:** DEFERRED · 15 · M
- **Purpose:** Safely answer explicit “how do we know each other?” requests using
  relationship evidence.
- **Problem:** D044 permits relationship context only for explicit requests, but
  presentation depth is intentionally narrow.
- **Why deferred:** Relationship reasoning was outside Identity isolation fixes.
- **Architectural impact:** Existing relationship detection plus evidence
  renderer; must never leak into simple identity answers.
- **Dependencies:** B19, B29; relationship behavioral contract.
- **Behavioral example:** `Who are you?` remains assistant-only; `How do we know
  each other?` may cite shared project experiences.
- **Validation:** strict simple-vs-relationship query matrix, foreign identity
  filtering, provenance.
- **Promotion:** Identity recertification and explicit host UX approval.
- **Sources:** `IDENTITY_CONTEXT_FILTERING.md`, `identity/rendering.py`.

### B22 — Longitudinal confidence calibration

- **Status / order / complexity:** RESEARCH · 13 · L
- **Purpose:** Measure whether numeric confidence corresponds to observed
  correctness over time.
- **Problem:** Current confidence values are principled heuristics, not calibrated
  psychometrics.
- **Why deferred:** Not a blocker for honest status gating; requires datasets and
  longitudinal evaluation.
- **Architectural impact:** Evaluation harness first; policy changes only after
  evidence and separate approval.
- **Dependencies:** Ground-truth corpus, B27, stable explanation metrics.
- **Behavioral example:** Memories reported near 0.8 should be correct near the
  expected empirical rate for the tested domain.
- **Validation:** reliability diagrams, Brier/ECE metrics, drift across
  reconsolidation/sleep/conflict.
- **Promotion:** Research report → proposed constants/policy → standalone
  recertification; never tune directly in Aria.
- **Sources:** `CONFIDENCE_MODEL.md`, `SCIENTIFIC_GAP_ANALYSIS.md`,
  `ACM_MATURITY_REVIEW_v1.md`.

### B23 — Working-memory interference depth

- **Status / order / complexity:** FUTURE · 18 · L
- **Purpose:** Improve focus refresh, interference, and concurrent-dialogue
  behavior within the existing WorkingBuffer.
- **Problem:** Capacity/displacement exist, but interference mechanics are
  shallow.
- **Why deferred:** Scientific polish, not required for D045 or initial memory
  correctness.
- **Architectural impact:** Deepen existing peer mechanism; no new activation
  engine.
- **Dependencies:** Research specification and concurrency corpus.
- **Behavioral example:** A new high-priority thread displaces a weaker active
  item without erasing long-term memory.
- **Validation:** proactive/retroactive interference, capacity, recovery,
  multi-thread dialogue.
- **Promotion:** Standalone milestone and long-session validation.
- **Sources:** `SCIENTIFIC_GAP_ANALYSIS.md`,
  `ACM_PHASE2_RECOMMENDATIONS.md`.

### B24 — Goal and prospective-memory depth

- **Status / order / complexity:** FUTURE · 19 · L
- **Purpose:** Improve cue-driven prospective recall and goal lifecycle within
  existing Goal Space.
- **Problem:** Goals bias cognition, but completion/trigger continuity remains
  shallow.
- **Why deferred:** Polish, not a missing foundational organ.
- **Architectural impact:** Deepen Goal Space; must remain memory, not planning or
  executive action.
- **Dependencies:** Prospective-memory research contract and boundary tests.
- **Behavioral example:** Context cue recalls an existing intention without
  autonomously scheduling or acting.
- **Validation:** cue trigger, completion, stale goals, context changes, hard
  no-planning assertions.
- **Promotion:** Standalone milestone before host project-continuity adoption.
- **Sources:** `SCIENTIFIC_GAP_ANALYSIS.md`,
  `ACM_MATURITY_REVIEW_v1.md`.

### B25 — Richer contextual and state-dependent binding

- **Status / order / complexity:** RESEARCH · 20 · L
- **Purpose:** Represent stronger context-dependent recall without embedding host
  state inside ACM.
- **Problem:** Context tags influence recall, but deep state-dependent binding is
  incomplete.
- **Why deferred:** Requires science-to-engineering mapping and host sensor
  contracts.
- **Architectural impact:** ContextFrame/attributes and optional plugins; no host
  imports.
- **Dependencies:** Research design, privacy policy, plugin interface.
- **Behavioral example:** A place/activity cue changes accessibility while the
  underlying memory remains available.
- **Validation:** context-match/mismatch, state removal, privacy, deterministic
  replay.
- **Promotion:** Research prototype as plugin before any core schema change.
- **Sources:** `SCIENTIFIC_GAP_ANALYSIS.md`, `ARCHITECTURE.md`.

### B26 — Retrieval-failure explanation taxonomy

- **Status / order / complexity:** RESEARCH · 14 · M
- **Purpose:** Distinguish absent memory, weak cue, dormant memory, interference,
  and tip-of-the-tongue-like partial activation.
- **Problem:** Retrieval failures are observable but explanations remain coarse.
- **Why deferred:** Needs empirical definitions and must not overclaim human
  mechanisms.
- **Architectural impact:** Remembering/Activation observability and uncertainty
  labels; no new organ.
- **Dependencies:** B06, B22 research methods.
- **Behavioral example:** “I may have related evidence, but this cue did not
  activate an answerable concept.”
- **Validation:** synthetic ground-truth scenarios, dormant/reactivated cases,
  no false-known responses.
- **Promotion:** Research report, then bounded standalone implementation.
- **Sources:** `SCIENTIFIC_GAP_ANALYSIS.md`,
  `REMEMBERING_MODEL.md`.

### B27 — Organ-scoped observability views

- **Status / order / complexity:** COMPLETE · 3 · M
- **Completed:** 2026-07-22
- **Purpose:** Provide stable per-organ report views without splitting the
  ValidationHarness.
- **Problem:** Rich observability exists, but consumers must interpret a broad
  aggregate schema.
- **Why deferred:** Readiness review classified this as maintainability polish.
- **Architectural impact:** Views only; singular harness and organ ownership stay
  intact.
- **Dependencies:** Schema versioning; privacy redaction remains B29.
- **Behavioral example:** Preference trace shows classify, owner, semantic
  candidates, admissibility, gate, and provenance without unrelated organ data.
- **Validation:** schema contracts, backward compatibility, redaction, empty
  organs.
- **Promotion:** Standalone observability release; host consumers migrate behind
  versioned contracts.
- **Implementation references:**
  - `acm/validation/organ_views.py` — `organ_view` / `organ_views`
  - `CognitiveEngine.organ_view` / `organ_views`
  - `tests/cognitive/test_organ_views.py`
  - Redaction applied via B29 (`redaction: "strict"` default on organ views)
- **Sources:** `ACM_V1_READINESS_REVIEW.md`,
  `OBSERVABILITY.md`.

### B28 — Long-duration, scaling, and memory profiling

- **Status / order / complexity:** COMPLETE · 16 · L
- **Completed:** 2026-07-22
- **Implementation references:** `tests/cognitive/test_memory_profiling.py` soak harness (`acm.memory_profile.v1`)
- **Purpose:** Establish performance and resource behavior beyond toy concept
  counts.
- **Problem:** Long-run smoke passes, but memory leaks and large-scale retrieval
  are not instrumented deeply.
- **Why deferred:** Operational validation condition, not a D045 correctness
  requirement.
- **Architectural impact:** Test/benchmark tooling only unless evidence later
  justifies optimization.
- **Dependencies:** Representative datasets and profiling budget.
- **Behavioral example:** Stable latency/memory over multi-day mixed workloads
  and restart cycles.
- **Validation:** soak, heap/CPU profiling, persistence growth, latency
  percentiles, no semantic regression.
- **Promotion:** Publish benchmark report before optimization releases.
- **Sources:** `LONG_DURATION_VALIDATION.md`,
  `BENCHMARK_STRATEGY.md`, `ACM_V1_READINESS_REVIEW.md`.

### B29 — Diagnostic privacy and redaction

- **Status / order / complexity:** COMPLETE · 5 · M
- **Completed:** 2026-07-23 (M4 AML C1)
- **Implementation references:**
  - `acm/authority/redaction.py` — `RedactionPolicy`, inspect/organ view redactors
  - `acm/authority/inspect_api.py` — B29 projection boundary
  - `acm/validation/organ_views.py` — structural redaction
  - `docs/DIAGNOSTIC_PRIVACY_REDACTION.md`
  - `tests/cognitive/test_privacy_redaction.py`
  - `tests/behavioral/test_privacy_redaction_conversation.py`
- **Purpose:** Prevent evidence/trace surfaces from leaking unrelated identity,
  context, or sensitive content.
- **Problem:** Explainability increases exposure risk even when cognitive answers
  are correctly isolated.
- **Why deferred:** Requires final diagnostic/evidence schemas.
- **Architectural impact:** Shared rendering policy; reuse D044 target isolation,
  no raw store access.
- **Dependencies:** B03, B07–B09, B14, B19.
- **Behavioral example:** Assistant evidence never reveals a user name; preference
  evidence never includes unrelated relationship context.
- **Validation:** adversarial cross-identity/cross-context corpus, structured and
  text redaction, fail-closed behavior.
- **Promotion:** Mandatory security/privacy gate before host diagnostics.
- **Sources:** `IDENTITY_CONTEXT_FILTERING.md`,
  `HALLUCINATION_PREVENTION.md`.

### B30 — Optional embedding activation prior

- **Status / order / complexity:** FUTURE · 23 · L
- **Purpose:** Improve cue quality while keeping vectors outside cognitive
  authority.
- **Problem:** Lightweight cue NLP may miss semantic paraphrases.
- **Why deferred:** Optional polish; core must not become vector-as-memory.
- **Architectural impact:** Plugin prior feeding Activation only; never storage,
  truth, or terminal authority.
- **Dependencies:** Plugin contract, deterministic fallback, privacy/performance
  research.
- **Behavioral example:** “preferred hue” activates `favorite color` while
  semantic Concepts/Experiences still determine the answer.
- **Validation:** paraphrase recall, plugin-off equivalence, no vector-only known
  answers, latency/privacy.
- **Promotion:** Experimental plugin release; core adoption only with evidence.
- **Sources:** `ACM_PHASE2_RECOMMENDATIONS.md`,
  `ACM_COMPARATIVE_RESEARCH.md`.

### B31 — Multimodal memory plugin depth

- **Status / order / complexity:** FUTURE · 24 · XL
- **Purpose:** Strengthen multimodal envelopes without bloating core or violating
  host independence.
- **Problem:** Envelopes are referenced, but multimodal ownership is shallow.
- **Why deferred:** Requires actual modality use cases and plugin contracts.
- **Architectural impact:** Plugin pathway and envelope provenance; no modality
  framework imported into core.
- **Dependencies:** B15 source taxonomy, plugin protocol, multimodal datasets.
- **Behavioral example:** An image-derived experience is explicitly marked
  perceived and can support a Concept without embedding binary data in core.
- **Validation:** modality provenance, unavailable-plugin behavior, persistence,
  privacy, no fabricated perception.
- **Promotion:** Separate experimental plugin; core schema promotion only after
  certification.
- **Sources:** `ACM_MATURITY_REVIEW_v1.md`,
  `EXPERIENCE_MODEL.md`, `PLUGIN_ARCHITECTURE.md`.

### B32 — Packaging and plugin discovery polish

- **Status / order / complexity:** FUTURE · 25 · M
- **Purpose:** Improve reusable-library installation and extension discovery.
- **Problem:** PyPI cadence and discovery loaders remain thin.
- **Why deferred:** Repository/tag releases and direct embedding currently meet
  the reference implementation’s needs.
- **Architectural impact:** Engineering only; no cognitive behavior.
- **Dependencies:** Stable pre-1.0 API policy and supply-chain checks.
- **Behavioral example:** Hosts install a pinned package and discover explicitly
  enabled plugins without implicit imports.
- **Validation:** clean-environment installs, Python matrix, signed artifacts,
  plugin enable/disable, host-independence.
- **Promotion:** Packaging release independent of cognitive promotion.
- **Sources:** `ACM_V1_READINESS_REVIEW.md`,
  `PLUGIN_ARCHITECTURE.md`.

### B33 — Planning, decision, and executive consumers

- **Status / order / complexity:** FUTURE · 99 · XL
- **Purpose:** Record the boundary for potential systems that consume ACM memory.
- **Problem:** Roadmap discussions can mistakenly treat planning/decision making
  as missing memory organs.
- **Why deferred:** These are executive cognition, intentionally outside ACM’s
  current memory architecture.
- **Architectural impact:** Must be separate consumers with hard contracts; never
  added casually as memory organs.
- **Dependencies:** Separate architecture approval after memory roadmap work.
- **Behavioral example:** A planner may ask ACM for evidence but cannot rewrite
  Experiences or become Memory Authority.
- **Validation:** boundary/import tests, no cognitive ownership collision, no
  autonomous architecture modification.
- **Promotion:** Separate project/milestone; not bundled with ACM memory fixes.
- **Sources:** `ACM_MATURITY_REVIEW_v1.md`,
  `ACM_PHASE2_RECOMMENDATIONS.md`, `CORE_BOUNDARIES.md`.

### B34 — Semantic cue and concept-induction depth

- **Status / order / complexity:** RESEARCH · 17 · L
- **Purpose:** Improve linguistic cue formation and concept induction beyond
  lightweight token/regex heuristics.
- **Problem:** D045 exposed how lexical support concepts can dominate activation;
  current cue NLP remains intentionally lightweight.
- **Why deferred:** D045 corrected admissibility without redesigning extraction,
  cueing, or emergence.
- **Architectural impact:** Concepts/Semantic Extraction research; must preserve
  Experience-first formation and D045 answerability.
- **Dependencies:** Curated linguistic corpus, D045 regression gates, optional
  comparison with B30.
- **Behavioral example:** Paraphrased preference statements form the same
  semantic property without treating question words as memory answers.
- **Validation:** Paraphrase, negation, interrogative/declarative, multilingual
  edge cases, concept-growth and no-token-conflict invariants.
- **Promotion:** Research report before any standalone implementation proposal.
- **Sources:** `DESIGN_NOTES.md`, `ACM_MATURITY_REVIEW_v1.md`,
  D045 investigation documents.

### B35 — Knowledge adoption and meta-memory surfaces

- **Status / order / complexity:** COMPLETE · 21 · L (MVP)
- **Completed:** 2026-07-23 (M4 AML C8 bounded MVP)
- **Implementation references:**
  - `CognitiveEngine.adopt_knowledge`
  - `ProvenanceSource.ADOPTED_KNOWLEDGE`
  - `docs/LEARNING_CERTIFICATION.md` L9
  - `tests/cognitive/test_m4_aml_capabilities.py`
- **Notes:** Host meta-memory UX surfaces remain optional polish; core MVP
  enforces provenance, bulk rejection, and no auto-autobiography.
- **Purpose:** Make the Knowledge ≠ Memory boundary and explicit adoption into
  memory visible to users and hosts.
- **Problem:** Core governance distinguishes external knowledge from lived or
  adopted memory, but user-facing adoption and meta-memory surfaces are thin.
- **Why deferred:** Requires host/product semantics and was listed as optional
  memory-internal polish.
- **Architectural impact:** Adoption workflow and presentation over existing
  Experience/Concept/provenance rules; external corpora never become memory
  automatically.
- **Dependencies:** B14/B15 source monitoring, B01 utterance function.
- **Behavioral example:** “Use this reference for this answer” does not become
  autobiography; “Remember this as accepted knowledge” creates an adopted,
  sourced Experience.
- **Validation:** adopt/reject/cancel, source provenance, no bulk-corpus
  ingestion, persistence and forgetting behavior.
- **Promotion:** Separate standalone governance release before any host workflow.
- **Sources:** `ACM_MATURITY_REVIEW_v1.md`,
  `PLUGIN_ARCHITECTURE.md`, `MEMORY_DESIGN_PRINCIPLES.md`.

### B36 — Prune, forget, and erase assent UX

- **Status / order / complexity:** DEPENDENT · 22 · L
- **Purpose:** Provide explicit user governance for high-impact pruning,
  forgetting, and erasure requests.
- **Problem:** Forgetting is intentionally soft and high-impact changes are
  governed, but complete review/assent UX is postponed.
- **Why deferred:** Not part of Identity/Preference correctness and requires
  policy/security review.
- **Architectural impact:** Policy Gate + Forgetting/Identity governance; never
  delete immutable history silently.
- **Dependencies:** B07–B09 diagnostics, B14 provenance, established erase policy.
- **Behavioral example:** “Forget my old address” previews affected living
  attributes and evidence policy before assent.
- **Validation:** approve/reject/cancel, soft forget vs legal erase distinction,
  identity protection, persistence and audit lineage.
- **Promotion:** Security/privacy review and standalone governance certification.
- **Sources:** `COGNITIVE_CAPABILITY_MAP.md`,
  `FORGETTING_MODEL.md`, `LEARNING_GOVERNANCE.md`.

### B37 — Autobiographical storytelling presentation

- **Status / order / complexity:** FUTURE · 26 · L
- **Purpose:** Present coherent autobiographical narratives from existing
  Experiences/Identity without creating new historical facts.
- **Problem:** Autobiographical memory is functionally present but narrative
  presentation is partial and largely a host concern.
- **Why deferred:** Storytelling is presentation, not a missing memory organ; it
  risks blending identity/context if introduced casually.
- **Architectural impact:** Read-only presentation consumer over timeline,
  provenance, and Identity isolation.
- **Dependencies:** B03, B14, B19, B29.
- **Behavioral example:** “Summarize what you know about my coffee preferences”
  cites a bounded timeline while `Who am I?` remains schema-only.
- **Validation:** chronology, source fidelity, no fabricated transitions,
  identity/context leakage, bounded output.
- **Promotion:** Prefer host presentation prototype after standalone structured
  narrative contract.
- **Sources:** `SCIENTIFIC_GAP_ANALYSIS.md`,
  `COGNITIVE_TIMELINE.md`, `IDENTITY_CONTEXT_FILTERING.md`.

### B38 — Deferred cognitive-intent research

- **Status / order / complexity:** RESEARCH · 27 · XL
- **Purpose:** Evaluate emotion, social-model, temporal-reasoning, and creativity
  request ownership without prematurely adding organs.
- **Problem:** `DEFERRED_INTENTS` records unresolved ownership categories; some
  older entries (prediction/simulation/analogy) are now implemented, while
  others remain research questions.
- **Why deferred:** Ownership, scientific validity, and ACM-vs-host boundaries
  are unresolved.
- **Architectural impact:** Potential taxonomy/ownership clarification; no
  implementation until each category proves to be memory cognition.
- **Dependencies:** Separate research brief per intent and capability-map audit.
- **Behavioral example:** A social-context question may retrieve relationship
  memory but must not imply a new social-reasoning organ by default.
- **Validation:** Ownership corpus, boundary cases, no fallback leaks, capability
  map and taxonomy consistency.
- **Promotion:** Docs/research decision first; each approved capability becomes
  a separately scoped release.
- **Sources:** `acm/authority/taxonomy.py`,
  `COGNITIVE_CAPABILITY_MAP.md`, `CORE_BOUNDARIES.md`.

### B39 — Recognition familiarity vs recollection research

- **Status / order / complexity:** RESEARCH · 28 · L
- **Purpose:** Evaluate whether ACM should distinguish familiarity from
  evidence-rich recollection more explicitly.
- **Problem:** Recognition/familiarity exists through concept strength, but a
  formal dual-process model is absent.
- **Why deferred:** Scientific polish; no demonstrated Identity/Preference
  correctness gap.
- **Architectural impact:** Likely Confidence/Concept/Remembering reporting, not
  a new organ.
- **Dependencies:** B22 calibration, B26 retrieval-failure taxonomy.
- **Behavioral example:** “This seems familiar, but I cannot reconstruct a
  supported episode.”
- **Validation:** familiarity-only vs recollection corpora, calibration,
  unknown/insufficient-evidence gates.
- **Promotion:** Research report before implementation.
- **Sources:** `SCIENTIFIC_GAP_ANALYSIS.md`,
  `REMEMBERING_MODEL.md`.

### B40 — Safe self-improvement governance

- **Status / order / complexity:** DEFERRED · 98 · XL
- **Purpose:** Preserve the future question of user-governed changes to cognitive
  policy or architecture without conflating it with ordinary Learning.
- **Problem:** Continuous memory adaptation exists; autonomous policy/
  architecture modification is intentionally prohibited.
- **Why deferred:** High-risk governance area requiring explicit authorization
  and separate architecture.
- **Architectural impact:** Policy/governance outside ordinary Learning; must
  never silently alter Activation or organ ownership.
- **Dependencies:** Mature diagnostics, rollback, formal policy, independent
  safety review.
- **Behavioral example:** ACM may propose a policy change with evidence, but
  cannot apply it without explicit reviewed assent and rollback.
- **Validation:** proposal-only default, authorization, rollback, immutable audit,
  no self-activation path.
- **Promotion:** Separate future program; never bundled with memory fixes.
- **Sources:** `ACM_MATURITY_REVIEW_v1.md`,
  `METACOGNITION_FOUNDATIONS.md`, `REMEMBERING_DESIGN_PRINCIPLES.md`.

### B41 — Interrogative preference storage cleanup

- **Status / order / complexity:** COMPLETE · 5 · M
- **Completed:** 2026-07-22 (closed in D045 follow-on; certified)
- **Purpose:** Stop storing question text as preference attributes during cue
  extraction.
- **Problem:** `extract_cues` stores unmatched favorite-containing questions as
  `preference=<raw question>`; D045 ignores them for answerability but storage
  pollution remains.
- **Why deferred:** Explicit D045 non-goal; reconstruction admissibility was
  corrected without changing extraction.
- **Implementation references:**
  - `acm/concepts/extract.py` — interrogatives skipped for preference minting
  - `tests/cognitive/test_preference_pipeline_debug.py` —
    `test_interrogative_no_longer_stored_as_preference_fact`
- **Sources:** `PREFERENCE_PIPELINE_TRACE.md`, `acm/concepts/extract.py`.
- **Architectural impact:** Cue/extraction only; preserve genuine
  `I prefer …` fallback semantics.
- **Dependencies:** B01 helpful; cleanup/migration policy for existing stores.
- **Behavioral example:** Encoding `What is my favorite color?` creates no active
  preference attribute.
- **Validation:** Invert
  `test_deferred_question_turn_stored_as_preference_fact`; genuine prefer
  statements; persistence migration; activation regression.
- **Promotion:** Standalone cleanup release before Aria promotion of extraction
  changes.
- **Sources:** `PREFERENCE_RECONSTRUCTION_FIX.md`,
  `PREFERENCE_CONFLICT_ANALYSIS.md`, `acm/concepts/extract.py`,
  `PREFERENCE_PIPELINE_TRACE.md`.

### B42 — Preference contradiction versus correction semantics

- **Status / order / complexity:** RESEARCH · 9 · L
- **Purpose:** Decide when a new preference value is a correction, a competing
  recollection, or a context-dependent alternative.
- **Problem:** Same-key plain teaches are last-write-wins, while differently
  normalized keys can still surface as conflict.
- **Why deferred:** Explicitly called a design question outside D045.
- **Architectural impact:** Preference update policy plus Reconciliation
  interaction; no silent evidence discard.
- **Dependencies:** Key normalization research, B11–B13, provenance.
- **Behavioral example:** `blue → red` may be correction, conflict, or
  context-dependent based on explicit markers and evidence.
- **Validation:** Correction markers, plain contradictions, aliases, contextual
  preferences, reconciliation lineage, user assent.
- **Promotion:** Architectural decision, then standalone implementation and
  certification.
- **Sources:** `test_preference_pipeline_debug.py`,
  `test_preference_reconstruction_fix.py`, `MEMORY_RECONCILIATION.md`.

### B43 — Identity ownership and documentation alignment

- **Status / order / complexity:** COMPLETE · 1 · S
- **Completed:** 2026-07-22
- **Purpose:** Align routing ownership metadata, perspective docs, and the
  capability map with D043/D044 reality.
- **Problem:** Some docs still imply `kind=identity` flips first-person to
  assistant, and USER_IDENTITY ownership text still suggests remembering
  supplements biography.
- **Why deferred:** Corrective docs/metadata polish after Identity certification.
- **Architectural impact:** Docs and ownership metadata; behavioral policy already
  correct.
- **Dependencies:** None.
- **Behavioral example:** Docs and route rationales state Identity is sole speech
  authority for Who am I / Who are you; assistant self-encode requires
  `speaker="assistant"`.
- **Validation:** Doc review, routing unit asserts, capability-map consistency.
- **Promotion:** Docs-only; no runtime promotion required.
- **Implementation references:**
  - `acm/authority/routing.py` — `USER_IDENTITY` / `IDENTITY` / `ASSISTANT_IDENTITY`
    supporting organs empty; sole-speech rationales
  - `docs/PERSPECTIVE_RESOLUTION.md`, `docs/IDENTITY_EXTRACTION.md`,
    `docs/COGNITIVE_ROUTING.md`, `docs/COGNITIVE_CAPABILITY_MAP.md`,
    `docs/ARCHITECTURE.md`, `docs/REMEMBERING_MODEL.md`,
    `docs/ORGAN_OWNERSHIP_VALIDATION.md`, `docs/MEMORY_CLASSIFICATION.md`
  - `tests/cognitive/test_cognitive_intent_routing.py` —
    `test_ownership_identity_intents_have_no_supports`
- **Sources:** `PERSPECTIVE_RESOLUTION.md`, `IDENTITY_EXTRACTION.md`,
  `IDENTITY_SEPARATION.md`, `COGNITIVE_CAPABILITY_MAP.md`,
  `acm/authority/routing.py`.

### B44 — Assistant Identity pipeline diagnostics

- **Status / order / complexity:** COMPLETE · 2 · M
- **Completed:** 2026-07-22
- **Purpose:** Provide a mirrored diagnostic trace for Who are you? paths.
- **Problem:** `trace_identity_pipeline` is user-teach oriented; assistant
  diagnostics are checklist-only.
- **Why deferred:** Identity fixes prioritized behavioral isolation over
  symmetric tooling.
- **Architectural impact:** Low; diagnostics/tools only.
- **Dependencies:** Existing assistant identity path.
- **Behavioral example:** `trace_assistant_identity_pipeline(engine)` asserts
  operational name and no user bleed.
- **Validation:** Extend identity pipeline tests; isolation regression green.
- **Promotion:** Standalone tooling release; optional with Identity promotion.
- **Implementation references:**
  - `acm/identity/pipeline_trace.py` — `trace_assistant_identity_pipeline`
  - `tests/cognitive/test_assistant_identity_diagnostics.py`
- **Sources:** `IDENTITY_PIPELINE_TRACE.md`,
  `ASSISTANT_IDENTITY_PIPELINE.md`, `acm/identity/pipeline_trace.py`.

### B45 — Isolation over-filter hardening

- **Status / order / complexity:** COMPLETE · 3 · M
- **Completed:** 2026-07-22
- **Purpose:** Prevent isolation filters from wiping operational assistant
  attributes and requiring silent re-seed.
- **Problem:** Current code acknowledges over-filtering of operational speech and
  re-seeds.
- **Why deferred:** D044 prioritized blend prevention; hardening is defensive
  polish.
- **Architectural impact:** Identity rendering isolation edge cases only.
- **Dependencies:** D044 filter rules.
- **Behavioral example:** Adversarial name-collision cases preserve operational
  name/role without silent drop.
- **Validation:** Adversarial isolation corpus; no blend regressions.
- **Promotion:** Standalone Identity polish release and recertification.
- **Implementation references:**
  - `acm/identity/rendering.py` — protected operational name/role claims
  - `acm/identity/organ.py` — `reseeded_operational_name`
  - `tests/cognitive/test_assistant_identity_diagnostics.py`
- **Sources:** `acm/identity/organ.py`, `acm/authority/pipeline.py`,
  D044 isolation tests.

### B46 — Retire legacy identity extraction fallback

- **Status / order / complexity:** DEFERRED · 12 · M
- **Purpose:** Remove dual-path legacy regex identity extraction once Semantic
  Extraction covers all Daily Use patterns.
- **Problem:** Structured apply can fall back to legacy regex, risking
  perspective/subject drift.
- **Why deferred:** Requires coverage proof for all identity phrasings.
- **Architectural impact:** Encode-only cleanup; preserve extraction contracts.
- **Dependencies:** Semantic Extraction corpus parity.
- **Behavioral example:** Odd identity phrasings extract only via `acm.semantic`.
- **Validation:** Diff extract-vs-legacy corpus; no Aria promote until parity.
- **Promotion:** Standalone extraction cleanup, then explicit promotion.
- **Sources:** `IDENTITY_EXTRACTION.md`, `acm/identity/organ.py`.

### B47 — Adjacent possession and relationship fact recall

- **Status / order / complexity:** DEFERRED · 14 · M
- **Purpose:** Query and render adjacent relationship/possession facts without
  polluting user identity name speech.
- **Problem:** Facts like “My dog’s name is Zeus” may be stored as adjacent links
  but are not surfaced by identity renderers.
- **Why deferred:** Outside D043/D044 isolation scope.
- **Architectural impact:** Identity/Remembering ownership for possession
  queries; keep simple identity answers schema-only.
- **Dependencies:** B21 relationship presentation helpful; classification for
  possession cues.
- **Behavioral example:** `What's my dog's name?` → Zeus without changing
  `Who am I?`.
- **Validation:** Extract + recall suite; name-collision guards remain.
- **Promotion:** Standalone Identity enhancement and isolation recertification.
- **Sources:** `FACT_EXTRACTION_RULES.md`, `COGNITIVE_FACT_MODEL.md`,
  `acm/identity/organ.py`.

### B48 — Multi-language semantic extraction

- **Status / order / complexity:** FUTURE · 29 · L
- **Purpose:** Extend Semantic Extraction beyond English cue patterns.
- **Problem:** Pattern set is intentionally English-first and extensible.
- **Why deferred:** Requires per-language perspective and strip rules.
- **Architectural impact:** Additive extraction patterns; no organ redesign.
- **Dependencies:** Perspective/strip localization research.
- **Behavioral example:** `Je m’appelle Jeff.` → User · Name · Jeff.
- **Validation:** Per-locale extract tests; host independence preserved.
- **Promotion:** Standalone locale packs before host enablement.
- **Sources:** `SEMANTIC_EXTRACTION.md`, `FACT_EXTRACTION_RULES.md`.

### B49 — Full organ-to-substrate remapping

- **Status / order / complexity:** FUTURE · 30 · XL
- **Purpose:** Remap all organs onto a stronger abstract substrate API beyond
  D040 termination guards.
- **Problem:** Organs still couple to CognitiveStore; full remapping was deferred
  after dispatch correction.
- **Why deferred:** D040 minimal termination/sanitization was sufficient for
  cognitive ownership.
- **Architectural impact:** Large internal refactor; public verbs should remain
  stable.
- **Dependencies:** Durable store maturity; persistence compatibility.
- **Behavioral example:** Swap backends without organ code changes; diagnostics
  never name store as authority.
- **Validation:** Full suite, persistence/migration cert, independence checks.
- **Promotion:** Careful standalone major refactor release; re-cert before Aria.
- **Sources:** `INFRASTRUCTURE_ABSTRACTION.md`.

### B50 — Shadow certification conditions and ACM 1.0 evidence

- **Status / order / complexity:** DEPENDENT · 31 · L
- **Purpose:** Close Shadow certification Conditions and only then declare
  unqualified ACM 1.0.
- **Problem:** Certification remains `CERTIFIED WITH CONDITIONS`; absolute SLOs
  and real-host Shadow evidence are still required for 1.0.
- **Why deferred:** Evidence-driven governance; silent score repair forbidden.
- **Architectural impact:** Adapter scoring/ops evidence; not a new organ.
- **Dependencies:** Host Shadow access, approved scoring normalization, rollback
  drill, Trace privacy.
- **Behavioral example:** Real-host Shadow agreement meets threshold; latency
  judged against absolute ms SLOs; `certified=true` only after explicit approval.
- **Validation:** Re-run certification gates; update certified evidence docs.
- **Promotion:** Host-side evidence plus standalone certification update.
- **Sources:** `ACM_CERTIFIED_v1.md`, `SHADOW_VALIDATION_RESULTS.md`,
  `ROADMAP.md`, `ACM_V1_READINESS_REVIEW.md`.

### B51 — Explicit Aria promotion of certified Identity/Preference stack

- **Status / order / complexity:** DEPENDENT · 0 · M
- **Purpose:** Promote D038–D045 into Aria’s independent vendored ACM copy only
  after explicit approval.
- **Problem:** Standalone ACM is research/reference; Aria remains on older
  cognition until promotion.
- **Why deferred:** D036–D037 forbid auto-sync; ROADMAP awaits approval.
- **Architectural impact:** Vendoring/copy process only; no ACM redesign.
- **Dependencies:** Approval; vendored-copy diff; host `cognitive_respond` before
  LM; speaker/encode discipline.
- **Behavioral example:** In Aria, teach name / Who am I / Who are you /
  preference ask match standalone certified behavior.
- **Validation:** Vendored identity/preference suites, shadow comparison,
  rollback.
- **Promotion:** This item *is* the promotion action.
- **Sources:** `ROADMAP.md`, `PROJECT_HISTORY.md`, `DECISION_LOG.md`,
  D038–D045 notes.

### B52 — Host speaker hint and LM field forcing

- **Status / order / complexity:** FUTURE · 32 · M
- **Purpose:** Hosts pass `speaker=` on identity turns and optionally constrain
  LM output to ACM memory fields.
- **Problem:** Without host speaker discipline, conversational defaults are user;
  post-speech LM can still invent outside ACM fields.
- **Why deferred:** Host-integration concern, not standalone ACM core.
- **Architectural impact:** Host-only if ACM API already supports `speaker`.
- **Dependencies:** B51 promotion; Aria façade contracts.
- **Behavioral example:** User text never marked `speaker="assistant"`; LM cannot
  invent autobiographical fields beyond ACM speech.
- **Validation:** Host integration tests after explicit promotion approval.
- **Promotion:** Host-side after vendored ACM promotion.
- **Sources:** `SEMANTIC_EXTRACTION.md`,
  `ASSISTANT_IDENTITY_PIPELINE.md`, `HALLUCINATION_PREVENTION.md`.

### B53 — Concept hierarchy deepening (M5 Cap1)

- **Status / order / complexity:** COMPLETE · 53 · M
- **Completed:** 2026-07-23 (ACM v0.28.0 — M5 Cap1)
- **Purpose:** Evidence-stamped taxonomic hierarchies with parent/child/sibling
  queries, inheritance, specialization/generalization, and Learning/Sleep
  proposals — without inventing Experiences or relocating taxonomy ownership.
- **Problem:** Hierarchy edges lacked Experience evidence, were not persisted,
  Learning `GENERALIZE` did not deepen `is_a`, and inheritance was absent.
- **Architectural impact:** Concept organ remains sole taxonomy writer (D016);
  Associations mirror traffic; Learning coordinates Adaptations only; codec
  persists `hierarchy_edges` on the store.
- **Dependencies:** Existing Concept/Association/Learning substrate (M3/M4/M7).
- **Behavioral example:** `A labrador is a dog.` → evidenced parent link;
  siblings under dog; `concept_hierarchy("labrador")` explains evidence;
  cycle creation blocked; inherit copies parent attributes only.
- **Validation:** `tests/behavioral/test_m5_concept_hierarchies.py`,
  `tests/cognitive/test_m5_hierarchy_learning_cert.py`, full pytest + learning
  cert suite.
- **Promotion:** Standalone Cap1 certification before Aria vendor (M5 final).
- **Implementation references:**
  - `acm/concepts/model.py` — `HierarchyEdge.evidence_ids`
  - `acm/concepts/organ.py` — link/query/inherit/specialize/generalize/propose
  - `acm/learning/organ.py` — `_adapt_hierarchy_from_reflection`
  - `acm/sleep/organ.py` — `hierarchy_candidate` proposals
  - `acm/persistence/codec.py` — `hierarchy_edges` snapshot field
  - `docs/CONCEPT_HIERARCHIES.md`
- **Sources:** M5 mission Cap1; D015/D016; `COGNITIVE_ABSTRACTION.md`.

### B54 — Evidence weighting & decay (M5 Cap2)

- **Status / order / complexity:** COMPLETE · 54 · M
- **Completed:** 2026-07-23 (ACM v0.29.0 — M5 Cap2)
- **Purpose:** Evidence influence ages unless reinforced; stale/obsolete detection
  lowers confidence factors without deleting provenance or Experiences.
- **Problem:** Confidence used evidence *count* only; unreinformed old evidence
  kept full influence; STALE meant weak grounding, not temporal neglect.
- **Architectural impact:** Confidence organ owns influence weights; Sleep runs
  `age_evidence_pass`; Learning/encode refresh weights; Forgetting unchanged.
- **Dependencies:** Confidence/Sleep/Learning substrate; Cap1 optional.
- **Behavioral example:** Idle evidence weight decays; reinforce restores;
  Experience/provenance counts unchanged across sleep aging.
- **Validation:** `tests/behavioral/test_m5_evidence_weighting.py`,
  `tests/cognitive/test_m5_evidence_decay_learning_cert.py`.
- **Promotion:** Standalone Cap2 certification before Aria vendor (M5 final).
- **Implementation references:**
  - `acm/confidence/model.py` — `EvidenceInfluence`, `UncertaintyKind.STALE/OBSOLETE`
  - `acm/confidence/organ.py` — weight/age/stabilize APIs
  - `acm/sleep/organ.py` — aging during consolidate
  - `docs/EVIDENCE_WEIGHTING.md`
- **Sources:** M5 mission Cap2; `CONFIDENCE_MODEL.md`.

### B55 — Counterfactual reasoning & prediction audit (M5 Cap3)

- **Status / order / complexity:** COMPLETE · 55 · L
- **Completed:** 2026-07-23 (ACM v0.30.0 — M5 Cap3)
- **Purpose:** Competing hypotheses with lifecycle; append-only prediction audits
  (comparison → calibration → confidence → learning); belief-change explanation.
- **Problem:** Predictions could be evaluated but lacked durable hypothesis
  competition, permanent audit history, and Cap2/Cap1-integrated learning hooks.
- **Architectural impact:** Prediction organ owns Hypothesis + PredictionAudit;
  Learning applies reversible Adaptations from audits; Confidence Cap2 used on
  hits; Experiences/provenance untouched.
- **Dependencies:** Prediction/Learning/Confidence substrate; Cap1–Cap2.
- **Behavioral example:** Predict → audit observed outcome → confidence shifts;
  disproved hypotheses remain queryable; rollback undoes Adaptations only.
- **Validation:** `tests/behavioral/test_m5_prediction_audit.py`,
  `tests/cognitive/test_m5_prediction_audit_learning_cert.py`.
- **Promotion:** Standalone Cap3 certification before Cap4 / Aria vendor.
- **Implementation references:**
  - `acm/prediction/model.py` — `Hypothesis`, `PredictionAudit`
  - `acm/prediction/organ.py` — audit pipeline + explain/competing APIs
  - `acm/learning/organ.py` — `learn_from_prediction_audit`
  - `acm/persistence/codec.py` — hypotheses + prediction_audits snapshot fields
  - `docs/PREDICTION_AUDIT.md`
- **Sources:** M5 mission Cap3; `PREDICTION_MODEL.md` · `PREDICTIVE_MEMORY.md`.

### B56 — Multi-level abstraction & general principles (M5 Cap4)

- **Status / order / complexity:** COMPLETE · 56 · L
- **Completed:** 2026-07-23 (ACM v0.31.0 — M5 Cap4)
- **Purpose:** Evidence-gated multi-level abstractions (L1–L5) and probabilistic
  general principles; Cap3 audits strengthen/weaken abstractions; Cap1 hierarchy
  participates without inventing Experiences.
- **Problem:** Hierarchies existed but higher-order abstractions, principle
  statements, and lifecycle (refine/split/merge/retire) lacked durable,
  explainable records tied to prediction outcomes.
- **Architectural impact:** Concept organ owns `AbstractionRecord` +
  `GeneralPrinciple`; Learning extends prediction-audit path; Sleep may derive
  evidenced abstractions; Persistence codec stores both collections.
- **Dependencies:** Cap1–Cap3; Concept/Learning/Prediction/Sleep substrate.
- **Behavioral example:** Reject thin evidence; promote abstraction; form
  "usually" principle; audit hit raises abstraction confidence.
- **Validation:** `tests/behavioral/test_m5_multi_level_abstraction.py`,
  `tests/cognitive/test_m5_abstraction_learning_cert.py`.
- **Promotion:** Standalone Cap4 certification before Cap5 / Aria vendor.
- **Implementation references:**
  - `acm/concepts/model.py` — AbstractionRecord, GeneralPrinciple
  - `acm/concepts/organ.py` — lifecycle + explain + derive APIs
  - `acm/learning/organ.py` — audit → abstraction reinforce/weaken
  - `docs/MULTI_LEVEL_ABSTRACTION.md`
- **Sources:** M5 mission Cap4; `COGNITIVE_ABSTRACTION.md`.

## Backlog governance

1. Every implementation proposal names one or more backlog IDs.
2. Moving an item between statuses requires evidence and a decision-log entry.
3. A release candidate may bundle only items with compatible architectural and
   validation scopes.
4. “READY” is not authorization. Explicit approval is still mandatory.
5. Standalone implementation precedes any Aria/vendor promotion.
6. Completed items remain here with a completion version and superseding
   decision so historical intent is not lost.
