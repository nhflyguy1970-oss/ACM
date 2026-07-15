# Remembering Model — ACM

**Status:** Canonical for M5  
**Cognitive question answered:** *What do I remember?*  
**Companions:** [`REMEMBERING_DESIGN_PRINCIPLES.md`](REMEMBERING_DESIGN_PRINCIPLES.md) · [`SPREADING_ACTIVATION.md`](SPREADING_ACTIVATION.md) · [`COGNITIVE_RECONSTRUCTION.md`](COGNITIVE_RECONSTRUCTION.md) · [`COGNITIVE_ACTIVATION_ARCHITECTURE.md`](COGNITIVE_ACTIVATION_ARCHITECTURE.md)

## Ownership

| Owns | Must never assume |
|------|-------------------|
| Cue-driven remembering | Experience history rewriting |
| Activation + reconstruction for recall | Concept meaning formation |
| Competing recollections / confidence surface | Association typology as ontology owner |
| Light reconsolidation on recall (accessibility) | Reflection / Learning / Prediction |

### Depends upon

Identity · Experiences (immutable evidence) · Concepts · Associations · Goals · Attention · Working Memory · Context · shared Activation Architecture

### Future organs that depend upon Remembering

Reflection · Learning · Prediction · Planning · Creativity · Analogical Reasoning · Metacognition · assent-gated self-improvement

## Cue-driven remembering

Cues (questions, concepts, goals, places, times, internal thoughts, observations) enter the shared **Activation Architecture**. Seeds activate Concepts; Associations propagate; Experiences **participate as evidence** — they are not scanned as a primary search index when Concepts/Associations suffice.

## Spreading activation

See [`SPREADING_ACTIVATION.md`](SPREADING_ACTIVATION.md). Path sketch:

```
Cue
  → Identity / Goals / Working Memory bias
  → Concept seeds
  → Association traversal (directional strengths)
  → Neighbor Concept activation + decay
  → Experience participation (evidence / exemplars)
  → Reconstruction(s)
```

## Reconstruction

A recollection packages:

- Primary Concept(s) + attributes  
- Supporting Associations activated  
- Participating Experiences (ids / public summaries — content unchanged)  
- Context / Identity / Goal influence stamps  
- Confidence + ambiguity flags  
- Competing candidates when close

## Competing memories

When multiple reconstructions exceed a competing threshold, ACM reports ambiguity rather than forced certainty. Future Reflection may resolve.

## Confidence

Emerges from Concept/Attribute confidence, Association confidence, evidence mass, goal congruence, and context match — not from opaque LLM scores.

## Context & Identity

Context retags emphasis; Identity biases self-relevant reconstructions and owns `Who am I?` reconstruction (Identity organ) while still participating in activation observables.

## Temporal influence

Recent activations and Experience timestamps bias accessibility for reconstruction without rewriting history.

## Future Reflection → M6 delivered

Remembering produces reconstructions. **Reflection** evaluates them and births Reflective Experiences. See [`REFLECTION_MODEL.md`](REFLECTION_MODEL.md). M5/M6 still do **not** implement Learning.
