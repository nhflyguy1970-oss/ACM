# Cognitive Capability Map — ACM

**Status:** Canonical architectural overview  
**Purpose:** One map of every cognitive organ — questions, ownership, dependencies, activation, observability.  
**Companions:** [`ARCHITECTURE.md`](ARCHITECTURE.md) · [`PROJECT_HISTORY.md`](PROJECT_HISTORY.md) · [`DECISION_LOG.md`](DECISION_LOG.md)

---

## Shared substrate

| Component | Role |
|-----------|------|
| CognitiveStore | In-process substrate (informative tech choice) |
| ValidationHarness | Observable cognitive state (no CoT / prompts) |
| Cognitive Activation Architecture | Shared cue→spread→field for active organs |
| Working Buffer · Attention · Context · Goals | Bias & capacity (owned as mechanisms, not full milestone organs yet) |

---

## Organs

### Identity — M1

| Field | Content |
|-------|---------|
| Question | Who am I? |
| Exclusive responsibility | Emergent agent/user/project schemas + Policy Gate assent |
| Inputs | Experiences (content), Goals |
| Outputs | `who_am_i`, identity snapshot, proposals |
| Artifacts | Identity Concepts / attributes + lineage |
| Dependencies | Experiences |
| Future dependents | All organs |
| Activation | Seeds / biases for self-cues |
| Observability | `identity` harness aggregate |
| Validation | Identity behavioral + cognitive suites |

### Experience — M2

| Field | Content |
|-------|---------|
| Question | What happened? |
| Exclusive responsibility | Immutable cognitive events + temporal lineage |
| Inputs | Encode stream, envelopes |
| Outputs | `what_happened`, timeline |
| Artifacts | Experiences, TemporalLinks, overlays |
| Dependencies | — |
| Future dependents | Concepts, Associations, Remembering, Reflection, … |
| Activation | Evidence participants |
| Observability | `experience` aggregate |
| Validation | Immutability + timeline tests |

### Concept — M3

| Field | Content |
|-------|---------|
| Question | What is this? |
| Exclusive responsibility | Emergent meaning (nuclei→mature), hierarchy `is_a`, prototypes |
| Inputs | Experiences |
| Outputs | `what_is_this`, recognize |
| Artifacts | Concepts, attributes, hierarchy |
| Dependencies | Experiences |
| Future dependents | Associations, Remembering, Reflection |
| Activation | Primary energy holders |
| Observability | `concept` aggregate |
| Validation | Emergence + hierarchy tests |

### Association — M4

| Field | Content |
|-------|---------|
| Question | How is this related? |
| Exclusive responsibility | Living directed relationships |
| Inputs | Concepts, Experiences (co-activation) |
| Outputs | `how_related`, neighborhoods, clusters |
| Artifacts | Associations |
| Dependencies | Concepts (+ Experiences) |
| Future dependents | Remembering, Reflection, Analogy |
| Activation | Conduits for spread |
| Observability | `association` aggregate |
| Validation | Asymmetry + neighborhood tests |

### Remembering — M5

| Field | Content |
|-------|---------|
| Question | What do I remember? |
| Exclusive responsibility | Cue-driven reconstruction |
| Inputs | Identity, Experiences, Concepts, Associations, Goals, Attention, WM, Context, Activation |
| Outputs | `remember` / `what_do_i_remember` |
| Artifacts | Reconstructions (ephemeral); light reconsolidation of accessibility |
| Dependencies | M1–M4 + Activation Architecture |
| Future dependents | Reflection, Learning, Prediction, … |
| Activation | First consumer |
| Observability | `remembering` aggregate |
| Validation | Reconstruction + integrity tests |

### Reflection — M6

| Field | Content |
|-------|---------|
| Question | What do I think about what I remember? |
| Exclusive responsibility | Evaluation of reconstructions; Reflective Experiences |
| Inputs | Remembering reconstructions (+ underlying organs via Activation) |
| Outputs | `what_do_i_think` / `reflect` |
| Artifacts | Reflective Experiences; outcome codes; questions; hypotheses |
| Dependencies | Identity, Experiences, Concepts, Associations, Remembering |
| Future dependents | Learning, Prediction, Planning, Creativity, Metacognition |
| Activation | Reuses Remembering → Activation Architecture (no second model) |
| Observability | `reflection` aggregate |
| Validation | Artifact birth + no silent history mutation |

### Learning — M7 implemented

| Field | Content |
|-------|---------|
| Question | What have I learned? |
| Exclusive responsibility | Governed durable adaptation of living structures |
| Inputs | Reflective Experiences, encode/remember outcomes, Offline batches |
| Outputs | `what_have_i_learned`, `learn`, assent/reject/rollback |
| Artifacts | Adaptation Records; never Experience rewrites |
| Dependencies | Identity, Experiences, Concepts, Associations, Remembering, Reflection |
| Future dependents | Offline Cognition, Prediction, Planning, Creativity, Forgetting |
| Activation | Reuses shared Activation Architecture (via neighborhood lessons) |
| Observability | `learning` harness aggregate |
| Validation | Adaptation lineage; history immutability; governance caps |

**Implementation status:** Implemented (v0.8.0). Docs: [`LEARNING_MODEL.md`](LEARNING_MODEL.md) · [`LEARNING_ARCHITECTURE.md`](LEARNING_ARCHITECTURE.md) · [`GENERALIZATION.md`](GENERALIZATION.md).

**Why Learning depends on Reflection:** only Reflective Experiences carry auditable evaluation outcomes (`sufficient`, `contradiction`, …) suitable for explainable adaptation. Encoding/remembering alone must not silently rewrite meaning.

### Offline Cognition — M8 implemented

| Field | Content |
|-------|---------|
| Question | What should become long-term memory? |
| Exclusive responsibility | Sleep-like replay, consolidation, abstraction proposals, confidence/salience stabilization |
| Inputs | Existing Reflective Experiences + Concepts/Associations (no external world) |
| Outputs | `sleep` / consolidate batch; proposals; cooled weak edges |
| Artifacts | Sleep batch ids; Offline observables; Learning Adaptations tagged with `sleep_batch_id` |
| Dependencies | Learning (applies/proposes adaptations); Activation for neighborhood replay |
| Future dependents | Forgetting (accessibility cooling schedules); improved Remembering |
| Observability | `offline` + `sleep_events` harness aggregates |
| Validation | No invented Experiences; prune/cool accessibility only; merge proposals never auto-applied |

**Implementation status:** Implemented (v0.8.0). Docs: [`OFFLINE_COGNITION.md`](OFFLINE_COGNITION.md) · [`CONSOLIDATION_MODEL.md`](CONSOLIDATION_MODEL.md) · [`ONLINE_OFFLINE_MEMORY.md`](ONLINE_OFFLINE_MEMORY.md).

**Why Offline Cognition depends on Learning:** consolidation strengthens memory by replaying evidence through the Adaptation pipeline — not by inventing new history or bypassing governance.

**How future Forgetting depends on both:** Forgetting cools accessibility using Learning lessons and Offline schedules so durable understanding is not erased while stale paths fade.

### Attention & Memory Priority — M9 implemented

| Field | Content |
|-------|---------|
| Question | What deserves cognitive attention and continued memory investment? |
| Exclusive responsibility | Attention allocation + evolving memory priority |
| Inputs | Cue text, Goals, Identity, living Concept importance, context |
| Outputs | `what_deserves_attention`, `allocate`, `invest`, replay ranking |
| Artifacts | PriorityEvents; AttentionAllocation factors |
| Dependencies | Concepts, Goals, Identity, Activation (modulation only) |
| Future dependents | All online verbs; Offline replay order |
| Observability | `attention` harness aggregate |
| Validation | Priority evolves; encode gate uses living factors |

**Implementation status:** Implemented (v0.9.0). Docs: [`ATTENTION_MODEL.md`](ATTENTION_MODEL.md) · [`MEMORY_PRIORITY.md`](MEMORY_PRIORITY.md).

### Accessibility & Forgetting — M10 implemented

| Field | Content |
|-------|---------|
| Question | What should become harder to remember? |
| Exclusive responsibility | Accessibility stages, cool, reactivation (never deletion) |
| Inputs | Neglect, Offline cool requests, host soft-forget, strong cues |
| Outputs | `what_should_be_harder_to_remember`, `cool_memory`, `reactivate_memory` |
| Artifacts | Accessibility levels + AccessibilityEvents |
| Dependencies | Concepts/Associations living state; Attention (cool resistance) |
| Future dependents | Remembering thresholds; prune-assent UX |
| Observability | `forgetting` harness aggregate |
| Validation | History immutable; dormant structures reactivate |

**Implementation status:** Implemented (v0.9.0). Docs: [`FORGETTING_MODEL.md`](FORGETTING_MODEL.md) · [`MEMORY_ACCESSIBILITY.md`](MEMORY_ACCESSIBILITY.md) · [`MEMORY_PRIORITY_LIFECYCLE.md`](MEMORY_PRIORITY_LIFECYCLE.md).

### Prediction — M11 implemented

| Field | Content |
|-------|---------|
| Question | Based upon memory, what is likely? |
| Exclusive responsibility | Probabilistic expected memory outcomes |
| Inputs | Activation, Associations, Priority, Accessibility, Learning residue |
| Outputs | `what_is_likely`, Prediction artifacts, `evaluate_prediction` |
| Artifacts | Predictions with outcome distributions |
| Dependencies | M1–M10 + Activation |
| Future dependents | Mental Simulation; Planning (consumer later) |
| Observability | `prediction` harness aggregate |
| Validation | Never plans/decides; confidence evolves |

**Implementation status:** Implemented (v0.10.0). Docs: [`PREDICTION_MODEL.md`](PREDICTION_MODEL.md) · [`PREDICTIVE_MEMORY.md`](PREDICTIVE_MEMORY.md) · [`BIOLOGICAL_VS_TECHNICAL_FUNCTION.md`](BIOLOGICAL_VS_TECHNICAL_FUNCTION.md).

### Mental Simulation — M12 implemented

| Field | Content |
|-------|---------|
| Question | What possible futures can memory imagine? |
| Exclusive responsibility | Hypothetical recombination / counterfactual memory sequences |
| Inputs | Activation, living structures, optional Prediction anchors |
| Outputs | `what_futures_can_memory_imagine` / `simulate` |
| Artifacts | Simulations with HypotheticalSteps (`hypothetical=true`) |
| Dependencies | Prediction (optional), Activation, Concepts/Associations/Experiences (read-only) |
| Future dependents | Planning (consumer); Creativity (later) |
| Observability | `simulation` harness aggregate |
| Validation | Never births Experiences; never plans/decides |

**Implementation status:** Implemented (v0.10.0). Docs: [`MENTAL_SIMULATION.md`](MENTAL_SIMULATION.md) · [`HYPOTHETICAL_MEMORY.md`](HYPOTHETICAL_MEMORY.md).

### Memory Recombination — M13 implemented

| Field | Content |
|-------|---------|
| Question | What new memories can emerge by recombining existing memories? |
| Exclusive responsibility | Novel temporary blends of existing fragments |
| Outputs | `what_new_memories_can_emerge` |
| Artifacts | RecombinedMemory (never Experiences) |
| Observability | `recombination` harness aggregate |

**Implementation status:** Implemented (v0.11.0). Docs: [`MEMORY_RECOMBINATION.md`](MEMORY_RECOMBINATION.md) · [`CREATIVITY_FOUNDATIONS.md`](CREATIVITY_FOUNDATIONS.md).

### Analogical Reasoning — M14 implemented

| Field | Content |
|-------|---------|
| Question | What existing memories are analogous even when they appear different? |
| Exclusive responsibility | Structural similarity / cross-domain mapping |
| Outputs | `what_is_analogous` |
| Artifacts | AnalogyMapping with alignments + why-codes |
| Observability | `analogy` harness aggregate |

**Implementation status:** Implemented (v0.11.0). Docs: [`ANALOGICAL_REASONING.md`](ANALOGICAL_REASONING.md) · [`ANALOGICAL_FOUNDATIONS.md`](ANALOGICAL_FOUNDATIONS.md).

### Memory Reconciliation — M15 implemented

| Field | Content |
|-------|---------|
| Question | When memories disagree, how should memory reconcile them? |
| Exclusive responsibility | Conflict/corroboration classification + reconciliation lineage |
| Inputs | Activation, Concept attrs, `conflicts_with`, Reflective outcomes, Predictions, context |
| Outputs | `how_should_memory_reconcile` |
| Artifacts | `ReconciliationRecord` (never rewrites Experiences) |
| Dependencies | M1–M14 + Confidence (collaboration) |
| Observability | `reconciliation` harness aggregate |
| Validation | History immutable; competing/context-dependent coexistence |

**Implementation status:** Implemented (v0.12.0). Docs: [`MEMORY_RECONCILIATION.md`](MEMORY_RECONCILIATION.md) · [`EVIDENCE_AND_CORROBORATION.md`](EVIDENCE_AND_CORROBORATION.md) · [`HUMAN_MEMORY_CONFLICTS.md`](HUMAN_MEMORY_CONFLICTS.md).

### Uncertainty & Confidence — M16 implemented

| Field | Content |
|-------|---------|
| Question | How certain am I that this memory is accurate? |
| Exclusive responsibility | Confidence estimation/evolution + uncertainty kinds |
| Inputs | Concepts, Accessibility, Priority, Learning, Reconciliation |
| Outputs | `how_certain_am_i` |
| Artifacts | `ConfidenceSnapshot`, `ConfidenceEvent` |
| Dependencies | Living memory graph; Reconciliation for corroboration/conflict deltas |
| Observability | `confidence` harness aggregate |
| Validation | Confidence evolves; explainable factors; never plans/decides |

**Implementation status:** Implemented (v0.12.0). Docs: [`CONFIDENCE_MODEL.md`](CONFIDENCE_MODEL.md) · [`UNCERTAINTY_MODEL.md`](UNCERTAINTY_MODEL.md) · [`ACM_MATURITY_REVIEW_v1.md`](ACM_MATURITY_REVIEW_v1.md).

### Phase Gate P1 — Readiness (design only)

| Field | Content |
|-------|---------|
| Question | Is ACM ready to become Aria’s memory subsystem / approach 1.0? |
| Exclusive responsibility | Scientific gap analysis, architecture/engineering review, Aria migration design |
| Outputs | Readiness verdict + recommendations (no organ code) |
| Verdict | **READY WITH MINOR CHANGES** |
| Observability | Documentation artifacts only |

**Status:** Complete (v0.12.1). Docs: [`ACM_V1_READINESS_REVIEW.md`](ACM_V1_READINESS_REVIEW.md) · [`SCIENTIFIC_GAP_ANALYSIS.md`](SCIENTIFIC_GAP_ANALYSIS.md) · [`ARIA_INTEGRATION_ARCHITECTURE.md`](ARIA_INTEGRATION_ARCHITECTURE.md) · [`ACM_COMPARATIVE_RESEARCH.md`](ACM_COMPARATIVE_RESEARCH.md) · [`ACM_PHASE2_RECOMMENDATIONS.md`](ACM_PHASE2_RECOMMENDATIONS.md).

### Phase 2 — Operational Readiness (engineering only)

| Field | Content |
|-------|---------|
| Question | Is ACM production-ready without new cognition? |
| Deliverables | Durable store · Provenance · Adapter · Shadow · Certification framework |
| Cognition change | **None** |
| Observability | `acm.validation/0.13` storage/provenance/shadow |

**Status:** Complete (v0.13.0). Docs: [`OPERATIONAL_READINESS.md`](OPERATIONAL_READINESS.md) · [`COGNITIVESTORE_ARCHITECTURE.md`](COGNITIVESTORE_ARCHITECTURE.md) · [`PROVENANCE_MODEL.md`](PROVENANCE_MODEL.md) · [`ARIA_MEMORY_ADAPTER.md`](ARIA_MEMORY_ADAPTER.md) · [`SHADOW_MODE.md`](SHADOW_MODE.md) · [`CERTIFICATION_FRAMEWORK.md`](CERTIFICATION_FRAMEWORK.md).

---

## Not yet organs (roadmapped)

Planning · Decision Making · Creativity orchestration · Full Goal organ polish · Working-memory depth

## Ownership rule

No organ assumes another’s exclusive responsibility. Metacognition emerges from Reflection interacting with Remembering and Learning — not as a silent monopoly organ. Reconciliation and Confidence cooperate without merging ownership. Phase 2 engineering layers do not become cognitive organs.
