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

---

## Not yet organs (roadmapped)

Learning · Prediction · Planning · Creativity · Analogical Reasoning · Forgetting · Sleep consolidation maturity · Full Goal / Attention organs

## Ownership rule

No organ assumes another’s exclusive responsibility. Metacognition emerges from Reflection interacting with Remembering and future Learning — not as a silent monopoly organ.
