# Association Model — ACM

**Status:** Canonical for M4  
**Cognitive question answered:** *How is this related?*  
**Companions:** [`COGNITIVE_NETWORKS.md`](COGNITIVE_NETWORKS.md) · [`ANALOGICAL_FOUNDATIONS.md`](ANALOGICAL_FOUNDATIONS.md) · [`CONCEPT_ARCHITECTURE.md`](CONCEPT_ARCHITECTURE.md) · [`ARCHITECTURE.md`](ARCHITECTURE.md)

## What is an Association?

An Association is a **cognitive relationship** — not a database edge, not a graph-tech primitive.

| Concepts | Associations |
|----------|--------------|
| Meaning — *what is this?* | Relationship — *how is this related?* |
| Nuclei → mature stages | Living links with strength, distance, context |

Concepts become useful because they are connected. Future Remembering will travel Associations; Reflection will traverse them; Creativity will lean on distant ones.

Taxonomic `is_a` remains owned by the **Concept organ** (D016). The Association organ holds relational fabric among Concepts (and, optionally, mirrors hierarchy as directed cognitive traffic without replacing taxonomy).

## Birth

Associations emerge from:

- Co-activation of Concepts within the same Experience  
- Temporal proximity of Experiences (precedes / follows hints)  
- Shared context tags / goal binding  
- Identity adjacency (`owned_by`, belongs-with)  
- Explicit relational language when present (supports, contradicts, …)  
- Sibling / neighborhood pressure under shared parents (resembles)

Nothing requires a hand-authored ontology of thousands of link types. Relation kinds are an **open, evolvable vocabulary**.

## Lifecycle

```
birth (nascent)
  → active
  → strong
  ⇄ dormant
  → retired
  ↑ reactivation / resurrection via new evidence
```

Plus evolution: strengthen, weaken, merge *proposal*, split *candidate* (high-impact merges are not silent).

## Strength model (cognitive, not arbitrary)

Forward and reverse strengths are distinct scores shaped by:

| Factor | Role |
|--------|------|
| Supporting Experiences (evidence count) | Practice mass |
| Co-activation / reinforcement events | Use |
| Goal relevance | Future-directed bias |
| Identity relevance | Privileged continuity |
| Temporal proximity | Chronology |
| Shared context | Situational binding |
| Concept maturity of endpoints | Stable meanings support stronger links |

Composite strength is informative; cognition owns the factors.

## Distance

| Band | Meaning |
|------|---------|
| **Immediate** | Strong, frequently co-activated |
| **Near** | Clear neighborhood member |
| **Far** | Weak but traversable |
| **Weak** | Barely held |
| **Dormant** | Circulating status cool |
| **Unexpected** | Low prior + sudden support (creative seam) |

## Directionality (decision)

**Associations are directed and may be asymmetric.** Humans often activate Dog → Animal more readily than Animal → Dog. M4 stores `strength_forward` and `strength_backward` independently (D017). Symmetric relations (e.g., pure co-activation) can keep both sides similar without forcing ontology-wide symmetry.

## Confidence & context

Confidence moves with congruent evidence and contestation. Context tags condition when a relationship is salient. Goal and identity influence are first-class stamps, not afterthoughts.

## Relationship to Remembering

M4 does **not** implement Remembering. It ensures traversable neighborhoods, distances, and directional strengths so future activation can walk meaning-relations instead of scanning raw Experiences.
