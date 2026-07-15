# ACM Architecture Review — Post M6 (L0)

**Status:** Design review only — **no implementation of corrections**  
**Date:** 2026-07-15  
**Scope:** Identity · Experiences · Concepts · Associations · Remembering · Reflection · Activation Architecture · Capability ownership · Dependencies · Roadmap  
**Companions:** [`COGNITIVE_CAPABILITY_MAP.md`](COGNITIVE_CAPABILITY_MAP.md) · [`LEARNING_ARCHITECTURE.md`](LEARNING_ARCHITECTURE.md) · [`ARCHITECTURE.md`](ARCHITECTURE.md)

---

## Executive verdict

ACM’s organ stack through M6 is **cognitively coherent**: history → meaning → relations → reconstruction → evaluation. The shared Activation Architecture is the correct foundation for active cognition. The largest remaining risk is **adaptation without a Learning organ**—Concept/Association/Remembering already apply mini-updates that must be reconciled when M7 lands. L0 defines Learning ownership so M7 does not fight existing organs.

---

## Strengths

1. **Clear cognitive questions per milestone** — minimizes organ sprawl.  
2. **Experience immutability** — trust and audit base.  
3. **Directed Associations + distance** — prepares analogy/creativity later.  
4. **Remembering ≠ search** — constitutionally aligned.  
5. **Reflection births history** — Learning feedstock exists (Reflective Experiences).  
6. **Host independence + harness observables** — reusable engine posture.  
7. **Policy Gate precedent on Identity** — pattern to extend for Learning assent.  
8. **Capability Map** — ownership documentation started.

---

## Weaknesses

1. **Roadmap numbering drift** — `ROADMAP.md` still lists legacy M6 Context / M7 Reconsolidation while implementation milestones used M5 Remembering / M6 Reflection; freeze `ARCHITECTURE.md` phases differ again. Confuses contributors.  
2. **Double-counting adaptation** — Concept strengthen, Association reinforce-on-recall, and future Learning overlap.  
3. **Goals / Attention / Context** — influential but not full organs; bias logic is scattered.  
4. **Sleep** — stub prune ≠ cognitive consolidation.  
5. **Adaptation artifact missing** — Reflective Experiences exist; Adaptation Records only designed in L0.  
6. **Lexical cueing** — still linguistic heuristics beneath Activation seeding (acceptable for now; limited multimodal).  
7. **Capability Map incomplete for unimplemented organs** — Learning section must be added at end of L0.

---

## Technical debt (do not fix in L0)

| Debt | Risk | Suggested future fix (not now) |
|------|------|--------------------------------|
| Duplicate roadmap numbering | Mis-ordered work | Reconcile ROADMAP to implementation IDs; footnote freeze chart |
| Remembering reconsolidation vs Learning | Policy fights | M7: classify light recall bumps vs Learning adaptations |
| `store.add_association` legacy | Mixed strength models | Route durable changes through AssociationOrgan / Learning |
| Goal edges to non-concepts | Activation graph noise | Goal organ or typed non-concept endpoints |
| Empty `acm/goals`, `sleep`, `reconsolidation` packages | False completeness | Fill or document as stubs explicitly |
| Architecture freeze M11 “Reflection” | Doc conflict | Cross-link implementation history without silent freeze rewrite |

---

## Opportunities

1. **M7 Learning** can absorb outcome-sensitive change and leave organs with clearer jobs.  
2. **Sleep + Learning** pairing matches consolidation science without neuron theater.  
3. **Forgetting-as-accessibility** preserves history while enabling human-like cool-down.  
4. **Capability Map + Research Foundations** become onboarding canon.  
5. **Partial Goal/Context milestones** (M4b/M5b) can harden bias without blocking Learning.

---

## Organ ownership check

| Organ | Ownership still clean? | Notes |
|-------|------------------------|-------|
| Experience | Yes | Guard zealously |
| Concept | Mostly | Cede cross-episode outcome policy to Learning later |
| Association | Mostly | Same |
| Remembering | Yes | Keep accessibility-only reconsolidation |
| Reflection | Yes | Must not start adapting |
| Activation | Yes | Single shared field |

**Responsibility overlap to resolve at M7:** “who strengthens a Concept after success?” → Learning applies; Concept retains formation/hierarchy APIs.

---

## Dependency flow (post-M6)

```
Identity ─────────────────────────────────────────────┐
Experiences ──► Concepts ──► Associations ──► Remembering ──► Reflection
                     │              │              │              │
                     └──────────────┴──────────────┴── Activation ┘
                                                          │
                                                     Learning (M7)
                                                          │
                                              Prediction → Planning
                                              Creativity / Analogy
                                              Forgetting / Sleep‡
```

‡ Sleep assists consolidation of Learning; not a parallel Learning.

---

## Future roadmap recommendation (post-Reflection)

Recommended **implementation** order (justified):

| Order | Milestone | Rationale |
|-------|-----------|-----------|
| 1 | **L0 Learning research** (this package) | Learning permanently changes organs — design first |
| 2 | **M7 Learning organ** | Consumes Reflective Experiences; gated adaptations |
| 3 | **M7b Sleep consolidation (real)** | Offline apply/propose Learning; matches evidence |
| 4 | **M5b Goal Space organ polish** | Goals already bias; deepen after Learning can update priorities |
| 5 | **M4b Working memory / Attention field polish** | Improves Activation quality for Prediction |
| 6 | **M8 Forgetting (accessibility)** | After Learning schedules exist so cool-down doesn’t fight lessons |
| 7 | **M9 Prediction** | Needs stable learned structure + goals |
| 8 | **M10 Planning** | Consumes Prediction + Goals; late by design freeze spirit |
| 9 | **M11 Creativity / Analogy** | Needs far Associations + Learning transfer |
| 10 | **M12 Safe Self-Improvement governance UX** | Never before Learning/Prediction maturity |
| — | Aria integration | Still **after** cognitive maturity metrics |

### Should order stay Learning → Prediction → Planning → Creativity → Self-Improvement?

**Yes, with inserts:** Sleep consolidation and Forgetting belong **adjacent to Learning**, not after Creativity. Context/Goal polish may parallelize as “b” milestones without superseding Learning.

### Why not Prediction before Learning?

Prediction without durable adaptation is brittle pattern matching. Cognitive science places prediction atop learned models (**well-supported** functionally). Reflection alone is evaluation, not model update.

### Why not Creativity earlier?

Creativity/analogy benefit from rich Association distance and learned abstractions — premature creativity becomes randomness or hallucinated links.

### Why Self-Improvement last?

Architecture change is not skill learning; trust requires Learning/Prediction auditability first.

---

## Corrections recommended (document only)

1. Update `ROADMAP.md` to L0 + M7 Learning; deprecate conflicting old M6/M7 labels or footnote them.  
2. Extend Capability Map with Learning (design).  
3. Cross-link Research Foundations from README / MEMORY_DESIGN companions.  
4. At M7, RFC for Adaptation Record schema + double-counting resolution.  

**No code changes for these corrections beyond documentation in L0.**

---

## Authorization statement

**M7 Learning implementation is not authorized until L0 documents are merged and accepted.**  
This review does not implement Learning, Prediction, Planning, Creativity, Forgetting, or Aria.
