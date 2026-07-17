# ACM Future Enhancements Roadmap

**Status:** Authoritative roadmap  
**Established:** 2026-07-17, after D045 Preference Reconstruction  
**Detailed backlog:** [`ENGINEERING_BACKLOG.md`](ENGINEERING_BACKLOG.md)  
**Candidate releases:** [`FUTURE_RELEASE_CANDIDATES.md`](FUTURE_RELEASE_CANDIDATES.md)

## Purpose

Identity certification (D038–D044) and Preference investigation/correction
(D045) proved that ACM’s architecture is sound while exposing presentation,
diagnostic, usability, and research opportunities. Those opportunities were
intentionally not added to narrowly scoped implementation corrections.

This roadmap preserves them without turning them into approved work. It
supersedes scattered “future”, “deferred”, and “polish” lists as the
authoritative index. Historical documents remain evidence.

## Architectural guardrails

All future work must preserve:

1. Memory Authority: language and hosts never invent memory answers.
2. Cognitive Ownership: organs own distinct cognitive questions.
3. Semantic Reconstruction: retrieval is reconstruction, not database search
   presented as cognition.
4. Immutable Experiences with living semantic structures and explainable
   lineage.
5. One Activation Architecture; no parallel retrieval authority.
6. Host independence: ACM never imports Aria, Mission Control, Cap Bus, or an
   LLM.
7. No raw storage dump as cognitive speech.
8. User and Assistant Identity remain isolated except on explicit relationship
   requests.
9. Normal recall may reconsolidate; diagnostic inspection must be explicitly
   read-only rather than silently changing normal cognition.
10. Standalone validation and release always precede explicit vendored
    promotion.

## Inventory

The detailed backlog contains **52 items**:

- **READY:** 16
- **DEPENDENT:** 13
- **DEFERRED:** 5
- **RESEARCH:** 8
- **FUTURE:** 10

Items B01–B21, B29, B34–B36, and B41–B48 arose from Identity/Preference
behavioral validation or their explainability implications. B22–B28,
B30–B33, B37–B40, and B49–B52 consolidate readiness, maturity,
scientific-gap, operational, capability-map, infrastructure, and
promotion recommendations.

## Recommended implementation phases

### Phase F1 — Safe observation foundation

**Goal:** Make future debugging and explainability non-mutating and safe before
adding more user-facing introspection.

Recommended order:

0. **B51** Explicit Aria promotion of D038–D045 remains a separate governance
   gate and is not part of F1 implementation work.
1. **B43** Identity ownership/documentation alignment (docs-only, can land early)
2. **B07** Read-only diagnostic mode
3. **B27** Organ-scoped observability views
4. **B08** Non-mutating inspection APIs
5. **B09** Diagnostic safety policy
6. **B29** Diagnostic privacy and redaction
7. **B10** Conversation-safe debugging
8. **B44** Assistant Identity pipeline diagnostics
9. **B45** Isolation over-filter hardening

Why first: D045 demonstrated that observing cognition through normal recall can
change activation, confidence, reflection, and learning state. Building
presentation before safe inspection would make tests and operator conclusions
state-dependent.

Exit criteria:

- Deep store snapshot unchanged by inspection.
- Normal mode retains intended reconsolidation.
- No user/assistant, context, relationship, or raw-record leakage.
- Replay produces stable diagnostics.

### Phase F2 — Utterance function and evidence access

**Goal:** Distinguish teaching, retrieval, and evidence inspection while keeping
existing organ ownership intact.

Recommended order:

1. **B01** Declarative teach vs query recognition
2. **B41** Interrogative preference storage cleanup
3. **B02** Evidence introspection intent
4. **B14** Memory provenance presentation
5. **B03** Memory evidence presentation

Exit criteria:

- Declarative teach never accidentally becomes retrieval.
- Evidence requests never collapse into the subject intent.
- Evidence presentation is bounded, source-faithful, and redacted.
- Unknown evidence remains honest unknown.
- Question turns no longer pollute preference attributes.

### Phase F3 — Explainability

**Goal:** Explain status without exposing chain of thought or inventing causes.

Recommended order:

1. **B04** Conflict explanation
2. **B05** Explainable confidence
3. **B06** Explainable uncertainty
4. **B16** Memory age explanation
5. **B17** Memory strength/accessibility explanation
6. **B18** Reflection explanation improvements
7. **B19** Identity evidence/provenance presentation

Exit criteria:

- Every explanation maps to structured evidence or events.
- Conflict answers name only admissible semantic competitors.
- Confidence, uncertainty, age, strength, and accessibility remain distinct.
- Identity evidence passes D043/D044 isolation certification.

### Phase F4 — User-governed memory management

**Goal:** Make corrections and conflict resolution explicit, reversible, and
lineage-preserving.

Recommended order:

1. **B11** Preference editing UX
2. **B12** Preference correction UX
3. **B42** Preference contradiction vs correction semantics (research → implement)
4. **B13** User-assisted conflict resolution
5. **B20** Identity correction and assent UX
6. **B21** Explicit relationship-memory presentation
7. **B47** Adjacent possession/relationship fact recall

Exit criteria:

- No silent last-write-wins evidence loss.
- Approve/reject/cancel and restart are tested.
- Corrections preserve immutable Experiences and provenance.
- Identity changes retain Policy Gate and collision protections.

### Phase F5 — Empirical depth and operational evidence

**Goal:** Improve measurement before changing cognitive constants or deeper
mechanisms.

Recommended order:

1. **B28** Long-duration/scaling/memory profiling
2. **B22** Longitudinal confidence calibration
3. **B26** Retrieval-failure explanation taxonomy
4. **B15** Rich source-monitoring taxonomy
5. **B25** Contextual/state-dependent binding research
6. **B34** Semantic cue/concept-induction research
7. **B38** Deferred cognitive-intent research
8. **B39** Recognition familiarity/recollection research
9. **B50** Shadow certification conditions / ACM 1.0 evidence

Exit criteria:

- Published datasets, protocols, and baseline measurements.
- Policy changes are justified by evidence, not anecdote.
- Schema migrations include export/import and persistence compatibility.

### Phase F6 — Optional depth and ecosystem work

**Goal:** Deepen partial capabilities or extension ergonomics only when concrete
use cases justify them.

- **B23** Working-memory interference depth
- **B24** Goal/prospective-memory depth
- **B30** Optional embedding Activation prior
- **B31** Multimodal memory plugin depth
- **B32** Packaging/plugin discovery polish
- **B35** Knowledge-adoption/meta-memory surfaces
- **B36** Prune/forget/erase assent UX
- **B37** Autobiographical storytelling presentation
- **B46** Retire legacy identity extraction fallback
- **B48** Multi-language semantic extraction
- **B49** Full organ-to-substrate remapping
- **B52** Host speaker hint and LM field forcing

These are not prerequisites for Identity/Preference correctness.

### Boundary-only future

**B33** Planning, decision, and executive consumers and **B40** safe
self-improvement governance remain separate
architecture questions. They are not missing ACM memory organs and must not be
smuggled into an explainability or usability release.

**B51** Aria promotion of the certified Identity/Preference stack is a
governance action, not an ACM architecture change.

## Priority recommendations

1. **Highest process priority:** B51 explicit Aria promotion of certified
   D038–D045 when approved.
2. **Highest implementation priority after promotion/or next standalone work:**
   F1 safe, non-mutating diagnostics.
3. **Next:** B01/B41/B02 utterance-function, interrogative storage cleanup, and
   evidence intent.
4. **Then:** provenance/evidence/conflict/confidence/uncertainty presentation.
5. **After safe introspection:** preference and identity correction UX.
6. **Measure before tuning:** confidence calibration, retrieval-failure
   taxonomy, context binding, Shadow/1.0 evidence.
7. **Keep optional:** embeddings, multimodal depth, packaging, planning,
   self-improvement.

## Validation policy for every phase

Every implementation must include:

- focused unit tests;
- end-to-end behavioral examples;
- full regression and performance checks;
- persistence/restart checks where state is involved;
- host-independence validation;
- no raw-storage or foreign-identity leakage;
- before/after traces demonstrating only approved behavior changed;
- annotated standalone tag and release when behavior changes;
- explicit approval before Aria/vendor promotion.

## Audit sources

This roadmap consolidates:

- D038–D045 decision and implementation documents;
- Identity separation/rendering/context-filtering certification;
- Preference pipeline, conflict, introspection, and reconstruction documents;
- `ACM_V1_READINESS_REVIEW.md`;
- `ACM_MATURITY_REVIEW_v1.md`;
- `SCIENTIFIC_GAP_ANALYSIS.md`;
- `ACM_PHASE2_RECOMMENDATIONS.md`;
- `LONG_DURATION_VALIDATION.md`;
- confidence, uncertainty, provenance, reflection, remembering, context,
  plugin, and observability documents;
- deferred intent/code comments and diagnostic tests.

## Current authorization

No roadmap item is authorized. D045 is complete in standalone ACM v0.18.4.
The next permitted implementation step remains subject to explicit approval.
Promotion of D045 into Aria is also separately approval-gated.
