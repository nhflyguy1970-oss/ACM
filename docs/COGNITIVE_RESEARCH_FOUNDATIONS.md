# Cognitive Research Foundations — ACM

**Status:** Permanent scientific foundation ledger for ACM  
**Mode:** Research & architectural decisions — updated as organs are designed  
**Rule:** Separate **Well-supported** · **Emerging** · **Speculative**. Never present speculation as established science.  
**Companions:** [`LEARNING_RESEARCH_FOUNDATIONS.md`](LEARNING_RESEARCH_FOUNDATIONS.md) · [`ARCHITECTURE.md`](ARCHITECTURE.md) · [`COGNITIVE_CAPABILITY_MAP.md`](COGNITIVE_CAPABILITY_MAP.md)

This file records, for each cognitive organ (present and planned): scientific background, competing theories, evidence strength, engineering interpretation, architectural decision, and reasons for acceptance/rejection.

---

## How to use this ledger

1. Every new organ design phase starts with a section here (or a focused companion that this file indexes).  
2. Implementation may proceed only when architectural decision is **Accepted** and governance boundaries are explicit.  
3. Engineering translations pursue **functional cognition**, not biological fidelity.

---

## Identity (M1 — implemented)

| Field | Content |
|-------|---------|
| Scientific background | Self-schema / autobiographical self; identity continuity; social identity (well-supported in psychology) |
| Competing theories | Scripted persona vs emergent self; minimal vs narrative self |
| Evidence strength | Continuity + experience-shaped self-knowledge: **well-supported**; single “true self” module: **speculative** |
| Engineering interpretation | Privileged schemas (`agent`/`user`/`project`) fed by experience; Policy Gate for high-impact flips |
| Architectural decision | **Accepted** D008–D010 |
| Accepted because | Trust + continuity without hard-coded bios |
| Rejected | Static persona scrape as identity |

## Experience (M2 — implemented)

| Field | Content |
|-------|---------|
| Scientific background | Episodic memory as event memory; encoding specificity (Tulving) — **well-supported** |
| Competing theories | Pure constructive memory (no stored episode) vs store+reconstruct hybrids |
| Evidence strength | Episodes as primary units: **well-supported**; perfect tape recorder: **rejected by evidence** |
| Engineering interpretation | Immutable Experience records + overlays for lifecycle/salience; reconstruction at Remembering |
| Architectural decision | **Accepted** D012 |
| Accepted because | Trustable history + room for constructive recall |
| Rejected | In-place experience overwrite |

## Concept (M3 — implemented)

| Field | Content |
|-------|---------|
| Scientific background | Categories, prototypes, exemplars, hierarchical taxonomy (Rosch, etc.) — **well-supported** |
| Competing theories | Prototype-only vs exemplar-only vs theory-theory |
| Evidence strength | Dual prototype+exemplar utility: **well-supported** enough for engineering |
| Engineering interpretation | Nuclei→mature Concepts; prototypes + exemplars (D015); hierarchy in Concept organ (D016) |
| Architectural decision | **Accepted** |
| Rejected | Manually curated ontology as default cognition |

## Association (M4 — implemented)

| Field | Content |
|-------|---------|
| Scientific background | Associative learning; spreading activation (Collins & Loftus tradition) — **well-supported** as cognitive model |
| Competing theories | Symmetric associative links vs directed asymmetric activations |
| Evidence strength | Asymmetric accessibility (category→member vs reverse) — **well-supported** behaviorally |
| Engineering interpretation | Living directed Associations (D017); not DB graph tech |
| Architectural decision | **Accepted** |
| Rejected | Mega-ontology of link types up front |

## Remembering (M5 — implemented)

| Field | Content |
|-------|---------|
| Scientific background | Reconstructive memory; context-dependent recall — **well-supported** |
| Competing theories | Retrieval-as-lookup vs reconstruction |
| Evidence strength | Reconstruction + interference: **well-supported** |
| Engineering interpretation | Cue-driven Activation Architecture; reconstructions not RAG (D018) |
| Architectural decision | **Accepted** |
| Rejected | Keyword/vector search as Remembering |

## Reflection / Metacognition (M6 — implemented)

| Field | Content |
|-------|---------|
| Scientific background | Metacognition: monitoring & control (Flavell; Nelson & Narens) — **well-supported** |
| Competing theories | Reflection as separate system vs emergent from memory |
| Evidence strength | Humans monitor confidence/conflict: **well-supported**; perfect calibration: **false** |
| Engineering interpretation | Reflection evaluates Remembering; births Reflective Experiences; no silent mutation (D019) |
| Architectural decision | **Accepted** |
| Rejected | Hidden CoT as “metacognition”; collapsing into Learning |

## Learning (L0 designed — M7 not implemented)

| Field | Content |
|-------|---------|
| Scientific background | See [`LEARNING_RESEARCH_FOUNDATIONS.md`](LEARNING_RESEARCH_FOUNDATIONS.md) |
| Competing theories | Multi-memory; pure RL; Hebbian-only; LLM fine-tune-as-memory |
| Evidence strength | Multi-system durable change: **well-supported**; single-mechanism monopoly: **rejected** |
| Engineering interpretation | Adaptation Records under governance; lineage Reflection→Learning→structure |
| Architectural decision | **Accepted and implemented** as M7 (v0.8.0); Offline Cognition as M8 |
| Rejected | Neuron simulation; silent self-mod; Learning = Reflection |

## Activation Architecture (shared — implemented)

| Field | Content |
|-------|---------|
| Scientific background | Spreading activation; limited capacity WM — **well-supported** cognitive models |
| Evidence strength | Activation-as-search metaphor is model, not literal brain current — treat as **engineering model** |
| Engineering interpretation | One shared field for active organs |
| Architectural decision | **Accepted** D018 |
| Rejected | Per-organ private activation engines |

## Prediction (future)

| Field | Content |
|-------|---------|
| Scientific background | Prospective cognition; predictive processing (**emerging**–**well-supported** hybrid depending on claim scope) |
| Engineering interpretation | Bias encode/remember from predicted next state; consume Learning lessons |
| Architectural decision | **Deferred** — after Learning + solid Association neighborhoods |
| Rejected (for now) | Prediction as first organ before Learning |

## Planning (future)

| Field | Content |
|-------|---------|
| Scientific background | Goal-directed behavior, hierarchical plans — **well-supported** |
| Engineering interpretation | Consumer of memory + prediction; not a memory store |
| Architectural decision | **Late roadmap** after Prediction / goals maturity |

## Creativity / Analogy (future)

| Field | Content |
|-------|---------|
| Scientific background | Far associative paths; structure mapping (Gentner) — **well-supported** phenomena |
| Engineering interpretation | Distant Associations + Activation unexpected band |
| Architectural decision | After Learning strengthens transferable structure |

## Forgetting (future)

| Field | Content |
|-------|---------|
| Scientific background | Decay, interference, retrieval-induced forgetting — **well-supported**; erasure of all traces uncommon |
| Engineering interpretation | Accessibility cooling, not Experience deletion |
| Architectural decision | **Accepted principle**; organ after Learning schedules exist |

## Sleep consolidation (partial stubs)

| Field | Content |
|-------|---------|
| Scientific background | Sleep aids memory consolidation — **well-supported** behaviorally |
| Engineering interpretation | Offline apply of low-impact Learning; propose high-impact |
| Architectural decision | **Accepted**; deepen with M7+ |

## Safe Self-Improvement (future governance)

| Field | Content |
|-------|---------|
| Scientific background | Human metacognitive strategy change is slow and socially constrained |
| Engineering interpretation | Architecture/policy change requires explicit user authorization |
| Architectural decision | **Accepted hard rule** — never conflate with Learning |

---

## Cross-cutting rejections for all organs

1. Biological literalism (neurons, cortex maps as required design).  
2. Prompt / chain-of-thought as cognitive state.  
3. Host product frameworks inside ACM core.  
4. Silent high-impact belief identity changes.  
5. Storage metrics as success metrics.
