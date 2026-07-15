# Scientific Gap Analysis — ACM v0.12

**Status:** Phase Gate P1 (design only)  
**Date:** 2026-07-15  
**Scope:** Evidence-driven comparison of ACM against established human memory science  
**Companions:** [`ACM_V1_READINESS_REVIEW.md`](ACM_V1_READINESS_REVIEW.md) · [`ACM_MATURITY_REVIEW_v1.md`](ACM_MATURITY_REVIEW_v1.md) · [`BIOLOGICAL_VS_TECHNICAL_FUNCTION.md`](BIOLOGICAL_VS_TECHNICAL_FUNCTION.md)

## Method

For each capability:

| Column | Meaning |
|--------|---------|
| Status | Implemented · Partial · Missing · Deferred · Excluded |
| Science grade | Well-supported · Emerging · Speculation |
| ACM mapping | Organ / mechanism (if any) |
| Gate impact | Blocker for Aria · Polish · Optional · N/A |

Conclusions prefer **function** over anatomical imitation. Speculation is never treated as a build requirement.

---

## Capability matrix

| Capability | Status | Science | ACM mapping | Gate impact | Rationale |
|------------|--------|---------|-------------|-------------|-----------|
| **Episodic memory** | Implemented | Well-supported | Experience organ (immutable Events) | N/A | Tulving-style what/when/where episodes as Experiences |
| **Autobiographical memory** | Partial | Well-supported | Experiences + Identity + timeline + reflection | Polish | Narrative identity exists; full autobiographical *storytelling* is host/presentation |
| **Semantic memory** | Implemented | Well-supported | Concept organ | N/A | Living Concepts / attributes / hierarchy |
| **Associative memory** | Implemented | Well-supported | Association organ + Activation | N/A | Directed living edges; spreading activation |
| **Working memory** | Partial | Well-supported | WorkingBuffer (capacity ~7) | Polish | Capacity + displace exist; interference/complex WM ops shallow (Baddeley components not fully modeled — intentional simplification) |
| **Prospective memory** | Partial | Well-supported | Goals + Prediction | Polish | Intentions/goals bias encoding/recall; dedicated cue-driven PM retrieval is thin |
| **Source memory / monitoring** | Partial | Well-supported | ExplanationClass · reconciliation factors · evidence ids | Polish | Sources exist as templates/factors; rich taxonomy (told vs perceived vs inferred) not first-class |
| **Contextual memory** | Partial | Well-supported | ContextFrame · context tags on attributes | Polish | Context biases encode/recall; deep state-dependent binding incomplete |
| **Spatial memory** | Partial | Well-supported | Place tags / concepts (role PLACE) | Optional | Not a dedicated spatial map organ; sufficient for agent text memory, insufficient for navigation robots without plugins |
| **Procedural memory** | Excluded as separate organ | Well-supported (as skill systems) | Concept role `skill` / procedural residue | N/A | Architecture: Procedure ⊂ Concept (skills as living concepts). Motor programs belong outside ACM (embodiment). **Correct exclusion of a separate organ.** |
| **Recognition memory** | Partial | Well-supported | `concepts.recognize` / familiarity via strength | Polish | Familiarity signal present; dual-process recollection/familiarity not formalized |
| **Recall** | Implemented | Well-supported | Remembering + Activation Architecture | N/A | Cue-driven reconstruction, not search-as-memory |
| **Pattern completion** | Partial | Well-supported (hippocampal models) | Activation spread / remembering | Optional | Functionally present; not modeled as CA3 attractor |
| **Pattern separation** | Partial | Well-supported | Distinct Experiences; attribute contests; reconciliation | Optional | Separates episodes by immutability; no explicit DG-like encoder |
| **Consolidation** | Implemented | Well-supported / emerging mechanisms | Offline Cognition (`sleep`) | N/A | Replay, stabilize, cool proposals |
| **Reconsolidation** | Partial | Well-supported | Remembering light reconsolidation + ValidationHarness | Polish | Functional update-on-retrieval; not pharmacological/timing physiology |
| **False memory** | Partial (acknowledged) | Well-supported | Confidence ↓ + conflict + reflection; never “forbid” constructive error | Optional | Constructive memory can err; ACM observes uncertainty rather than guaranteeing truth |
| **Interference** | Partial | Well-supported | Conflicts_with · reconciliation · WM displace | Polish | Proactive/retroactive interference modeled as conflict + capacity, not full interference laws |
| **Generalization** | Partial | Well-supported | Concept abstraction · Learning · Offline proposals | Polish | Exists; not a deep schema-induction engine |
| **Transfer** | Partial | Emerging / well-supported behaviorally | Analogy + Learning | Optional | Structure-mapping supports transfer foundations |
| **Memory distortion** | Partial | Well-supported | Living Concepts change; Experiences immutable | N/A | Correct asymmetry: history fixed, meaning evolves |
| **Cue-dependent recall** | Implemented | Well-supported | Activation cues + context tags | N/A | Encoding specificity principle honored functionally |
| **State-dependent memory** | Partial | Well-supported | ContextFrame | Optional | Mood/embodied state not modeled (host sensor → context tags) |
| **Metamemory** | Implemented | Well-supported | Reflection + Confidence + metacognitive_sketch | N/A | Evaluation of memory contents without CoT |
| **Confidence** | Implemented | Well-supported | Confidence organ (M16) | N/A | Evolves with evidence; not psychometrically calibrated |
| **Uncertainty** | Implemented | Well-supported | Uncertainty kinds on snapshots | N/A | Named uncertainty taxonomy |
| **Accessibility / forgetting** | Implemented | Well-supported | Forgetting organ (soft accessibility) | N/A | Availability ≠ accessibility (Tulving/Pearlstone functional spirit) |
| **Retrieval failure** | Partial | Well-supported | Ambiguity · cool · dormant · low activation | Polish | Failures are observable; tip-of-tongue not explicit |
| **Prediction** | Implemented | Well-supported / emerging mechanisms | Prediction organ | N/A | Prospective expectation from memory — not planning |
| **Mental simulation** | Implemented | Well-supported | Simulation organ | N/A | Episodic future thinking; not executive planning |
| **Analogical reasoning** | Implemented | Well-supported | Analogy organ | N/A | Structure-mapping function |
| **Memory recombination** | Implemented | Well-supported | Recombination organ | N/A | Constructive blend; non-historical |
| **Conflict resolution (memory)** | Implemented | Well-supported | Reconciliation organ | N/A | Lineage without silent discard |
| **Identity formation** | Implemented | Well-supported / emerging self models | Identity organ + Policy Gate | N/A | Emergent schemas, assent for high-impact change |

---

## Intentional exclusions (memory science ≠ ACM)

| Item | Why excluded | Confidence |
|------|--------------|------------|
| Executive planning / decision making | Not memory organs; consumers of memory | Well-supported boundary in cognitive architectures |
| Separate procedural motor organ | Embodiment / skills engines; Procedure⊂Concept | Well-supported engineering boundary |
| Anatomical hippocampus simulation | Mechanism, not function | Design principle |
| Social/public remembering institutions | Host / society layer | — |
| LLM latent memory as ACM substrate | Violates explainability & host independence | Architecture |

---

## Scientific gaps that matter for Aria (ranked)

1. **Durable source-monitoring taxonomy** (told / perceived / inferred / reconstructed) — science well-supported; ACM partial via explanation classes.  
   **Impact:** Improve trust UI and Trace; not a new organ — enrich Experience/Concept metadata + Confidence factors.

2. **Working-memory interference depth** — science well-supported; ACM buffer is thin.  
   **Impact:** Dialogue concurrency polish; not Aria blockers if adapter rates traffic.

3. **Goal / prospective-memory completion** — science well-supported; ACM goals exist but shallow.  
   **Impact:** Project continuity for Aria; polish milestone M5b.

4. **Confidence calibration** — science well-supported that humans miscalibrate; ACM uses heuristics.  
   **Impact:** Observability / UI honesty; run longitudinal calibration offline. Not a blocker for first dual-write.

5. **Spatial / navigational memory** — only if Aria embodiments need maps.  
   **Impact:** Plugin, not core organ.

## Verdict of Part 1

ACM covers the **core scientific memory functions** required of an agent cognitive memory subsystem. Remaining gaps are **depth/polish of partial capabilities**, not absence of foundational memory systems. No well-supported *additional memory organ* is mandatory before Aria integration begins under a phased dual-write plan.

**Missing mandatory organ before Aria?** No.  
**Missing mandatory science-aligned polish before 1.0 declaration?** Yes — durable store + source taxonomy enrichment + Goal/WM polish schedule (see readiness review).
