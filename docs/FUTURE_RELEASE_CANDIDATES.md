# ACM Future Release Candidates

**Status:** Planning only — no release is authorized or version-reserved  
**Authoritative items:** [`ENGINEERING_BACKLOG.md`](ENGINEERING_BACKLOG.md)  
**Ordering:** [`FUTURE_ENHANCEMENTS_ROADMAP.md`](FUTURE_ENHANCEMENTS_ROADMAP.md)

Candidate releases are deliberately named by capability, not assigned semantic
versions. Actual versions, decisions, and scope require approval after the
preceding candidate is certified.

## RC-A — Diagnostic Safety Foundation

- **Backlog:** B07, B08, B09, B27, B29; B10 after core gates pass
- **Candidate status:** COMPLETE (B07–B10, B27, B29 implemented through v0.36.0)
- **Purpose:** Establish read-only, non-mutating, redacted inspection before
  user-facing introspection.
- **Why first:** D045 showed that ordinary diagnostic questions can mutate the
  state being inspected.
- **Architectural review:** Confirm inspection is a mode/view over existing
  organs, not a second cognitive authority.
- **Behavioral gate:** Store/provenance/confidence/working snapshots remain
  byte-equivalent across inspection; normal recall still reconsolidates.
- **Promotion:** Standalone release only. Host exposure requires separate
  privacy/security and adapter review.

## RC-B — Teach and Evidence Intent

- **Backlog:** B01, B02
- **Candidate status:** DEPENDENT on RC-A inspection contracts
- **Purpose:** Separate declarative teaching, reconstruction queries, and
  evidence inspection.
- **Architectural review:** Preserve Cognitive Ownership and conservative Memory
  Authority fallback.
- **Behavioral gate:** Cross-domain utterance-function corpus; no host/LM intent
  override; no evidence query classified as its subject.
- **Promotion:** Standalone classification/dispatch release, then explicit
  vendored promotion.

## RC-C — Evidence and Provenance Presentation

- **Backlog:** B03, B14, B16, B19
- **Candidate status:** DEPENDENT on RC-A and RC-B
- **Purpose:** Present why a memory is known, when its evidence formed, and where
  it came from.
- **Architectural review:** Presentation is a read-only projection; no raw-store
  terminal and no invented provenance.
- **Behavioral gate:** All provenance origins, redaction, missing artifacts,
  user/assistant isolation, bounded rendering.
- **Promotion:** Standalone release, then host Trace/speech validation.

## RC-D — Conflict, Confidence, and Uncertainty Explainability

- **Backlog:** B04, B05, B06, B17, B18
- **Candidate status:** DEPENDENT on RC-A/RC-C
- **Purpose:** Explain conflicts, confidence movement, uncertainty kinds, and
  accessibility without chain-of-thought exposure.
- **Architectural review:** Reconciliation owns lineage, Confidence owns
  confidence/uncertainty, Reflection owns evaluation, Remembering owns
  reconstruction.
- **Behavioral gate:** True semantic conflict examples; no lexical competitors;
  every explanation maps to structured fields/events.
- **Promotion:** Standalone behavioral certification, then host presentation
  approval.

## RC-E — User-Governed Preference Management

- **Backlog:** B11, B12, B13
- **Candidate status:** DEPENDENT on RC-B–RC-D
- **Purpose:** Explicit preference viewing, editing, correction, and assisted
  conflict resolution.
- **Architectural review:** Immutable Experiences and reconciliation lineage
  remain intact; no direct store CRUD UX.
- **Behavioral gate:** set/replace/remove/cancel, true conflicts, confirm/reject,
  persistence/restart, provenance.
- **Promotion:** Standalone release and manual behavioral certification before
  vendored promotion.

## RC-F — User-Governed Identity Management

- **Backlog:** B20 (COMPLETE v0.40.0); B21 (COMPLETE v0.41.0)
- **Candidate status:** COMPLETE for practical identity correction + relationship presentation
- **Purpose:** Add correction/assent and explicit relationship presentation
  while preserving D043/D044 isolation.
- **Architectural review:** Re-run complete User/Assistant Identity separation,
  collision, context, and relationship boundaries.
- **Behavioral gate:** approve/reject/cancel, cross-identity leakage, persistence,
  relationship-only context.
- **Promotion:** Standalone Identity recertification required; never bundled
  casually with Preference work.

## RC-G — Source Monitoring and Calibration Research

- **Backlog:** B15, B22, B25, B26, B28
- **Candidate status:** RESEARCH
- **Purpose:** Produce datasets and evidence for source taxonomy, confidence
  calibration, context binding, and retrieval-failure explanations.
- **Architectural review:** Research first; no cognitive constants or schemas
  change without a later implementation decision.
- **Behavioral gate:** Reproducible protocol, baseline metrics, migration impact,
  and negative findings recorded.
- **Promotion:** Research report may be docs-only; implementation candidates are
  split by evidence.

## RC-H — Memory Depth Polish

- **Backlog:** B23, B24
- **Candidate status:** FUTURE
- **Purpose:** Deepen WorkingBuffer interference and Goal/prospective-memory
  behavior without adding executive cognition.
- **Architectural review:** One Activation Architecture; goals remain memory
  cues, not autonomous planning.
- **Behavioral gate:** long-conversation interference, prospective cueing,
  completion/staleness, strict no-action assertions.
- **Promotion:** Separate standalone milestone(s); not a prerequisite for D045
  promotion.

## RC-I — Optional Extension Ecosystem

- **Backlog:** B30, B31, B32
- **Candidate status:** FUTURE
- **Purpose:** Optional embedding priors, multimodal plugins, packaging, and
  plugin discovery.
- **Architectural review:** Plugins cannot become memory authority; core works
  identically when plugins are absent.
- **Behavioral gate:** plugin-off equivalence, provenance, privacy, latency,
  clean installation.
- **Promotion:** Experimental plugins/packages remain separately versioned where
  possible.

## Not an ACM memory release candidate

**B33 Planning, decision, and executive consumers** and **B40 Safe
self-improvement governance** require separate architecture and approval
processes. They must not be combined with any release candidate above or
represented as missing memory subsystems.

Additional items **B34–B52** graduate only through the matching candidate:

- B34/B38/B39/B42 → RC-G research first
- B35 → a future knowledge-adoption governance candidate
- B36 → a future privacy/governance candidate after RC-A/RC-C
- B37 → host-facing presentation candidate after RC-C and Identity isolation
  validation
- B41 → RC-B with teach/query and evidence intent
- B43–B45 → docs/tooling polish before or with Identity recertification
- B46–B48 → Identity/extraction depth candidates after coverage research
- B49 → infrastructure refactor candidate after persistence maturity
- B50 → Shadow/1.0 evidence gate
- B51 → explicit Aria promotion of D038–D045
- B52 → host-side after B51

## Candidate graduation checklist

A candidate may become an approved release only when:

1. scope and non-goals are frozen;
2. architectural ownership is documented;
3. dependencies are completed;
4. behavioral and regression plans are approved;
5. privacy/leakage implications are resolved;
6. standalone implementation is authorized;
7. release/tag policy is assigned;
8. Aria promotion remains a separate explicit decision.
