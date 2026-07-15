# ACM Comparative Research — Modern AI Memory Architectures

**Status:** Phase Gate P1 (design only)  
**Date:** 2026-07-15  
**Companions:** [`ACM_V1_READINESS_REVIEW.md`](ACM_V1_READINESS_REVIEW.md) · [`SCIENTIFIC_GAP_ANALYSIS.md`](SCIENTIFIC_GAP_ANALYSIS.md)

## Purpose

Compare ACM to common AI memory approaches. Recommend **only** additions that improve cognitive memory function — never features merely because another system has them.

---

## Landscape

| Family | Typical traits | Example pattern |
|--------|----------------|-----------------|
| Vector / embedding stores | Similarity search over chunks | Pinecone-style agent memory |
| RAG | Retrieve corpus passages → prompt | Document QA pipelines |
| Graph memory | Nodes/edges as knowledge | Knowledge graphs, some agent graphs |
| Long-context | Pack history into context window | 100k–1M token models |
| Agent frameworks | Scratchpads, tools, session stores | Lang-agent memory modules |
| Classical cognitive architectures | ACT-R, SOAR productions | Symbolic WM + LTM |
| Hybrid CRM-style agent memory | Profiles + notes + vectors | Consumer “AI companion” memory |

---

## What ACM intentionally does differently

| Dimension | Typical AI memory | ACM |
|-----------|-------------------|-----|
| Unit of truth | Chunk / embedding / string fact | Immutable **Experience** + living **Concept/Association** |
| Recall | Search / top-k | Cue-driven **Activation** → reconstruction |
| Updates | Overwrite / upsert | Lineage, reconsolidation, reconciliation artifacts |
| Forgetting | Delete / TTL | Accessibility stages (soft) |
| Certainty | Often absent or static score | Evolving Confidence + Uncertainty kinds |
| Governance | App policy ad hoc | Policy Gate assent for identity/high-impact |
| Explainability | Prompt leftovers / citations | Template explanation classes + harness |
| Host coupling | Often framework-tied | Host-agnostic CognitiveEngine |
| Offline | Rare / summarizer cron | Dedicated Offline Cognition organ |
| Conflict | Last-write-wins | Competing / context-dependent / reinforce |

---

## What ACM improves (relative to common agent memory)

1. **Autobiographical integrity** — history is not silently rewritten.  
2. **Cognitive verb discipline** — encode / remember / sleep / reconcile / assess, not only CRUD.  
3. **Metamemory** — reflection + confidence as first-class memory functions.  
4. **Constructive processes** — simulation, recombination, analogy without inventing historical episodes.  
5. **Observability without CoT** — ValidationHarness metadata suitable for Mission Control.

---

## What ACM should intentionally avoid copying

| Temptation | Why avoid |
|------------|-----------|
| Pure vector store as the memory model | Similarity ≠ remembering; loses lineage/identity |
| RAG as identity | Knowledge ≠ autobiographical memory (citation wall stays) |
| Infinite transcript-as-WM | Violates capacity/interference (Principles) |
| Prompted “self-reflection” as Reflection organ | CoT is not cognitive state |
| Auto-merge truth under conflict | Violates M15 lineage |
| Framework-owned memory (Lang-only) | Host independence |
| Replacing Experiences with summaries only | Loses episodic detail needed for reconciliation |

---

## Selective borrowings (acceptable as *substrate*, not as *cognition*)

| Borrow | Role | Rule |
|--------|------|------|
| Embeddings | Informative cue → activation prior | Behind Activation; never public “memory = vector” |
| Graph DBs | Durable Association/Concept substrate | Swappable CognitiveStore backend |
| RAG indices | Knowledge corpora | Explicit encode-to-adopt; not automatic identity |
| Long context | Host dialogue packing | Outside ACM (working buffer still capacity-limited) |

Science grade for these borrowings: **engineering**: well-supported as storage/IR tools; **not** substitutes for episodic/semantic cognitive function.

---

## Recommendation

Do **not** add a VectorMemory organ or RAG organ to ACM core.  
Do keep optional embedding plugins for Activation scoring after Aria integration design approvals.  
Do not chase feature parity with agent frameworks; chase **human cognitive memory function**.
