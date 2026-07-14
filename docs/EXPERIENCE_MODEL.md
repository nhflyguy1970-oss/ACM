# Experience Model — ACM

**Status:** Canonical for M2  
**Cognitive question answered:** *What happened?*  
**Companions:** [`COGNITIVE_TIMELINE.md`](COGNITIVE_TIMELINE.md) · [`ARCHITECTURE.md`](ARCHITECTURE.md) · [`MEMORY_DESIGN_PRINCIPLES.md`](MEMORY_DESIGN_PRINCIPLES.md) · [`CORE_BOUNDARIES.md`](CORE_BOUNDARIES.md)

## What is an Experience?

An Experience is a **cognitive event** — not a storage record, document, conversation transcript, or file.

Sources (chat logs, PDFs, images, terminals, sensors) may *give rise* to Experiences. The Experience itself is the internalized event: observation, decision, correction, insight, failure, goal progress, and so on.

| Not an Experience | Is an Experience |
|-------------------|------------------|
| A PDF on disk | Learning / discovery precipitated by reading it |
| A chat blob | The correction, question, or relationship episode within it |
| A vector embedding | (never cognition by itself) |
| A profile field | Identity change *event* when lived |

**Nothing bypasses Experience.** Identity maturation, future Concepts, Associations, Remembering, and Learning grow from Experiences (directly or via adoption). Knowledge corpora remain outside until lived/adopted as Experience.

## Dual identity

Every Experience has two identities:

| Identity | Role | Examples |
|----------|------|----------|
| **External** | Source modality / channel | `text`, `conversation`, `image`, `audio`, `video`, `code`, `terminal`, `pdf`, `document`, `sensor`, `gps`, `filesystem` |
| **Internal (cognitive)** | What kind of *cognitive event* it was | `observation`, `learning`, `failure`, `success`, `decision`, `correction`, `discovery`, `insight`, `question`, `conflict`, `relationship`, `goal_progress`, `goal_completion`, `unexpected`, `identity_change`, `preference` |

Future cognition reasons primarily with the **internal** identity. External identity remains for multimodal fairness and envelope binding — no modality is first-class over another.

## Salience

Salience is multidimensional (not a single opaque score):

- Attention  
- Novelty  
- Importance  
- Goal relevance  
- Confidence  
- Frequency  
- Recency  
- Unexpectedness  
- Context fit  

Birth salience is frozen on the Experience. **Current** salience may evolve in an overlay (relevance over time) without rewriting history. Future Remembering will use relevance; it must not delete history to forget.

## Lifecycle

```
birth → active → (dormant ⇄ active) → retired
         │
         ├─ revise → new Experience (lineage)
         ├─ reflect → new Experience (lineage)
         ├─ correct → new Experience (lineage)
         └─ relate temporally → links (not mutations)
```

| Stage | Meaning |
|-------|---------|
| **Birth** | Immutable event created; lineage parent optional |
| **Active** | Available to future organs by default |
| **Dormant** | Low current salience; retained; may re-awaken |
| **Retired** | Explicitly out of default circulation; still retained |
| **Revision** | Never in-place edit — always a new Experience |
| **Containment / overlap** | Temporal links (`overlaps`, `concurrent`, `part_of_episode`) |
| **Merge / split** | Future Sleep *proposals* only — not silent rewrite in M2 |

Hard erase of Experience history is outside M2 and remains Policy-gated in the architecture.

## Lineage

- Corrections create new Experiences (`cognitive_kind=correction`, `revises_id=…`).  
- Reflections create new Experiences (`reflects_on_id=…`).  
- Identity changes that stick still leave Experience footprints (`identity_change`).  
- Lineage is queryable; history is never destroyed for convenience.

## Relationships to other organs

| Organ | Relationship |
|-------|----------------|
| **Identity (M1)** | Identity content emerges from Experiences; identity-influenced events stamp Influence on salience |
| **Concepts (future)** | Concepts crystallize from recurrent Experience patterns — Experiences do not become Concepts in M2 |
| **Associations (future)** | Edges may later bind Experiences/Concepts; M2 only uses temporal lineage links |
| **Remembering (future refinement)** | Will activate from Experience + Concept fabric; M2 exposes `what_happened` chronology only |
| **Learning** | Learning *is* Experience (`learning`, `insight`, `discovery`) plus later consolidation |
| **Self-improvement (future)** | Experience log can record architecture proposals as Events; **applying** self-modification requires explicit user authorization later — M2 does not implement self-mod |

## Design tests

1. Can history be reconstructed after a correction without mutating the prior Experience?  
2. Can an image-born and text-born Experience share the same internal kind and salience model?  
3. Does “What happened?” answer from Experiences alone, without requiring Concept organ maturity?
