# Concept Architecture — ACM

**Status:** Canonical for M3  
**Cognitive question answered:** *What is this?*  
**Companions:** [`COGNITIVE_ABSTRACTION.md`](COGNITIVE_ABSTRACTION.md) · [`CONCEPT_LIFECYCLE.md`](CONCEPT_LIFECYCLE.md) · [`EXPERIENCE_MODEL.md`](EXPERIENCE_MODEL.md) · [`ARCHITECTURE.md`](ARCHITECTURE.md)

## What is a Concept?

A Concept is **emergent meaning** — not a manually maintained object, not an Experience, not a document.

| Experiences | Concepts |
|-------------|---------|
| History — what happened | Meaning — what this *is* |
| Immutable events | Living structures that strengthen/weaken |
| Chronology | Categories, prototypes, hierarchies |

Experiences create Concepts. Concepts create understanding. Future Associations and Remembering should increasingly operate over Concepts, not raw Experience streams.

## Emergence

```
Experiences accumulate
  → patterns / labels / attributes recur
  → Concept Nuclei appear (provisional)
  → reinforcement raises strength & confidence
  → Concepts stabilize and mature
  → neglect / contradiction weakens or dormants them
```

Avoid hand-authored taxonomies as the source of truth. Lightweight structure (e.g., “X is a Y”) may *seed* hierarchy candidates; maturation still requires experience evidence.

## Concept Nuclei

A **nucleus** is an emerging understanding — not yet a mature Concept.

- Born from first supporting Experience(s)  
- Low strength / confidence; `provisional=True`  
- Repeated congruent Experiences transform nuclei → growing → stable → mature  
- Unsupported nuclei weaken and may retire naturally  

## Reinforcement

Each supporting Experience may:

- Increase strength and confidence  
- Append evidence (Experience ids)  
- Update prototype features  
- Register exemplars  
- Advance lifecycle stage  

Contradictory evidence can supersede attributes (with lineage on attributes) and may *weaken* confidence without erasing Experience history.

## Confidence & maturity

| Signal | Role |
|--------|------|
| Confidence | How strongly the meaning is held |
| Strength | Practice / reinforcement mass |
| Evidence count | Number of supporting Experiences |
| Stage | Nucleus → … → Mature (see lifecycle doc) |

## Abstraction & specialization

Hierarchy edges (`is_a` / specialization) live in the **Concept organ** (not the future Association organ). Abstraction structures enable future reasoning; M3 does not implement reasoning.

## Prototypes & exemplars (decision)

**Decision:** Concepts maintain both a **prototype** (central tendency of features) and a capped list of **exemplars** (specific Experiences or instance Concepts).

| Representation | Why |
|----------------|-----|
| Prototype | Supports “typical X” and family resemblance |
| Exemplars | Anchors lived instances (Zeus, that PDF, that failure) |

This is more cognitively appropriate than prototype-only or exemplar-only for an experience-grounded engine. Documented as D015.

## Merge / split

- **Merge:** high-similarity labels may create *proposals*; mature merges are not silent.  
- **Split:** clustered contradictory attributes may create split *candidates*.  
M3 records proposals; high-impact application waits for stronger policy (compatible with future self-improvement assent).

## Retirement / resurrection

Weak nuclei/dormant Concepts may retire from default recognition. New Experiences can resurrect dormant Concepts by reinforcement (lifecycle overlay).

## Future Associations

Associations (M4+) will connect Concepts (and Experiences/envelopes). Hierarchy/prototype structures here must remain usable as association endpoints. M3 does **not** implement spreading activation or associative remembering.
