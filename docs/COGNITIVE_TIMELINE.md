# Cognitive Timeline — ACM

**Status:** Canonical for M2  
**Companions:** [`EXPERIENCE_MODEL.md`](EXPERIENCE_MODEL.md) · [`ARCHITECTURE.md`](ARCHITECTURE.md)

## Why time is a first-class cognitive organizer

Human memory is not a bag of facts. It is ordered, overlapping, causal, and recurrent. ACM treats time as **cognitive structure**, not optional metadata.

Without temporal cognition:

- Corrections cannot sit after errors  
- Goals cannot show progress episodes  
- Concurrent perceptions collapse into one blob  
- “What happened?” becomes “what strings match?”

## Chronology

Every Experience carries:

| Field | Role |
|-------|------|
| `t_start` | When the event began (cognitive clock) |
| `t_end` | Optional end (duration) |
| `t_encoded` | When ACM birthed the Experience |
| Sequence index | Stable ordering within an agent stream |

`what_happened` and `timeline` order primarily by `t_start` / encode sequence, not by retrieval rank.

## Causality & relatedness (M2 links)

Temporal links (immutable edge records among Experiences):

| Relation | Meaning |
|----------|---------|
| `precedes` / `follows` | Order |
| `overlaps` / `concurrent` | Shared interval |
| `causes` / `caused_by` | Explicit causal claim (asserted at birth or by a later Experience) |
| `revises` | Correction lineage |
| `reflects_on` | Reflection lineage |
| `near` | Temporal proximity cluster hint |

M2 records links; it does not yet run full causal inference (future Prediction / Reflection milestones).

## Experience lineage vs revision

- **Lineage** = directed history of cognitive rewrite without mutation  
- **Revision** = new Experience that supersedes relevance of a prior *for future read paths*, while the prior remains immutable  

Retired / dormant statuses affect default circulation, never bit-destruction.

## Temporal clustering

Future organs may cluster Experiences by proximity, shared context tags, shared goals, or concurrent envelopes. M2 exposes:

- ordered timeline slices  
- proximity queries (`near`)  
- lineage chains  

## Future temporal reasoning (not implemented now)

Planning, prediction, and creative synthesis should later reuse the same timeline primitives. M2 only ensures Experiences and links are rich enough that those organs will not require a redesign.
