# Learning Architecture — ACM

**Status:** Canonical architecture for the Learning organ (**implemented M7 / v0.8.0**)  
**Cognitive question (M7):** *What have I learned?*  
**Companions:** [`LEARNING_RESEARCH_FOUNDATIONS.md`](LEARNING_RESEARCH_FOUNDATIONS.md) · [`LEARNING_GOVERNANCE.md`](LEARNING_GOVERNANCE.md) · [`LEARNING_LIFECYCLE.md`](LEARNING_LIFECYCLE.md) · [`COGNITIVE_CAPABILITY_MAP.md`](COGNITIVE_CAPABILITY_MAP.md) · [`COGNITIVE_ACTIVATION_ARCHITECTURE.md`](COGNITIVE_ACTIVATION_ARCHITECTURE.md)

---

## Purpose

Learning is the first organ authorized to **permanently adapt other cognitive organs’ living structures** under governance. It answers what durable lessons ACM has drawn from Experience and Reflection — without rewriting history and without redesigning ACM’s architecture.

---

## Ownership (exclusive)

| Owns | Must never assume |
|------|-------------------|
| Durable adaptation of Concepts, Associations, preference/goal parameters, accessibility policies | Experience content mutation |
| Application of Reflection outcomes into structure change | Reflection’s evaluation role |
| Learning lineage / “what have I learned?” summaries | Remembering reconstruction |
| Automatic vs assent routing for adaptations | Silent Policy Gate bypass |
| Coordination with Sleep for consolidation proposals | Sleep as unbounded mutator |
| | Prediction, Planning, Creativity, self-mod of organs |

### Depends upon

Identity · Experiences · Concepts · Associations · Remembering · Reflection · Goals · Attention · Context · WM · Activation Architecture · Policy Gate patterns

### Future dependents

Prediction · Planning · Creativity · Forgetting · Safe Self-Improvement (governance only) · Metacognition maturity

---

## What Learning means in ACM

**Definition:** Learning produces **auditable Adaptation Records** that change living cognition (strength, confidence policies, association weights, hierarchy *proposals*, preference weighting, goal priority) so future Remembering and Reflection behave differently — with lineage back to Reflective Experiences and evidence Experiences.

Learning does **not** mean:

- Adding rows to a vector DB  
- Retraining an LLM  
- Reconstructing a memory (Remembering)  
- Judging a memory (Reflection)

---

## Cognitive lineage (canonical)

```
Experience (immutable)
    ↓ (meaning / relation growth)
Concept · Association · Identity attributes
    ↓ (cue-driven)
Remembering → Reconstruction
    ↓ (evaluate)
Reflection → Reflective Experience (immutable)
    ↓ (adapt)
Learning → Adaptation Record(s)
    ↓ (apply under governance)
Concept evolution · Association evolution · Identity proposals · Goal bias · Accessibility
    ↓
Future Remembering / Reflection / Prediction
```

### Lineage sufficiency

**Sufficient for M7** with one refinement: every Adaptation Record must cite:

1. Trigger Reflective Experience id(s) (and/or encode outcome codes)  
2. Target structure ids (Concept / Association / Identity attribute / Goal)  
3. Change vector (before → after observables)  
4. Governance class (`automatic` | `proposed` | `assented` | `rejected`)  
5. Optional Sleep batch id  

**Refinement recommended:** introduce a first-class `Adaptation` cognitive artifact (not an Experience rewrite; separate record analogous to TemporalLink metadata) so Learning outputs are queryable as *What have I learned?* without scanning raw Experiences alone.

---

## Public verbs (implemented M7)

| Verb | Intent |
|------|--------|
| `what_have_i_learned(cue?)` | Summarize adaptations / lessons relevant to cue |
| `learn(...)` / `learn_from_reflection(...)` | Apply or propose adaptations from one Reflective Experience |
| `assent_adaptation(proposal_id)` / `reject_adaptation(proposal_id)` / `rollback_adaptation(...)` | Governance |
| `learning.observables()` | Metrics only |

Internal: `propose_adaptation`, `apply_low_impact`, Offline Cognition `sleep_batch_id`.

---

## Interaction with Activation Architecture

Learning **reuses** Activation Architecture when selecting what a lesson is about (cue neighborhoods). It does **not** invent a second activation engine. Spread may bias which Associations get adapted; activation energy is not itself “the lesson.”

---

## Change surface by organ

| Target | Automatic (examples) | Assent-required (examples) |
|--------|----------------------|----------------------------|
| Association strength | Small +/- from consistent co-activation / Reflective consistency | RelationKind rewrites; mass retirement |
| Concept strength / confidence | Bounded nudges from repeated congruent Reflective `sufficient` | Mature Concept merge/split; role change |
| Prototype features | Soft weight updates from exemplars | Replacing prototype wholesale |
| Identity attributes | Slight confidence on congruent self-evidence | Conflicting identity adopt/supersede |
| Goals | Importance nudge from progress Reflective signals | Abandoning / inventing goals as policy |
| Preferences | Reinforcement within existing preference keys | High-stakes preference erase |
| Accessibility | Future Forgetting cool paths | Hard delete |

Exact thresholds = policy constants (assent if changed as architecture). See Governance.

---

## Observability (required at M7)

Harness must observe (no CoT):

- Adaptation births · applies · proposals · rejects  
- Target organ · magnitude · lineage Reflective Experience ids  
- Automatic vs assent path  
- Rollback markers  
- Sleep consolidation batches  

---

## Compatibility with constitution

| Principle | How Learning complies |
|-----------|----------------------|
| Cognition ≠ storage | Adaptations change behavior of remember/encode bias |
| Experiences primary & immutable | Never rewrite Experience summaries |
| Knowledge ≠ Memory | External facts need adoption Experiences before Learning |
| Explainability | Template explanations + lineage, not chain-of-thought |
| Host independence | No Aria hooks |
| User governance | Assent for high-impact |

---

## Non-goals (M7/M8 boundary)

- No Prediction organ  
- No Planning organ  
- No Creativity organ  
- No Forgetting organ (hooks only — Offline cools weak associations as accessibility)  
- No neuron simulation  
- No architectural self-improvement  

**M7 Learning and M8 Offline Cognition are implemented (v0.8.0).** L0 design remains the scientific/governance baseline.
