# Project History

## Origin

Daily Use Mode work on Aria’s legacy Memory subsystem concluded that incremental repair had reached its limit. A full cognitive architecture was designed (Principles + Architecture v2.1 + Test Strategy) and frozen as design.

## Birth of ACM

Implementation was authorized as a **new standalone engine**, not a rename of Aria Memory and not an in-place migration.

- **2026-07:** ACM repository bootstrapped; M0 Validation Harness and `CognitiveEngine` foundation landed as v0.1.0.
- **2026-07:** M1 Identity — first true cognitive organ. Emergent schemas, lineage, Policy Gate assent, plugin/core boundary docs. Released as v0.2.0.
- **2026-07:** M2 Experience — immutable cognitive events with dual identity, salience, temporal links, and lineage. Released as v0.3.0.
- **2026-07:** M3 Concept — emergent meaning (nuclei, lifecycle, hierarchy, prototypes). Released as v0.4.0.
- **2026-07:** M4 Association — living cognitive relationships (strength, distance, neighborhoods). Released as v0.5.0.
- **2026-07:** M5 Remembering — cue-driven reconstruction via shared Cognitive Activation Architecture. Released as v0.6.0.
- **2026-07:** M6 Reflection — metacognitive evaluation producing Reflective Experiences. Released as v0.7.0. Capability map: `docs/COGNITIVE_CAPABILITY_MAP.md`.

## Milestone cognitive questions

| Milestone | Question | Capability |
|-----------|----------|------------|
| M1 | Who am I? | Emergent Identity schemas |
| M2 | What happened? | Immutable Experience chronology |
| M3 | What is this? | Emergent Concepts / understanding |
| M4 | How is this related? | Living Associations / cognitive networks |
| M5 | What do I remember? | Active reconstruction + Activation Architecture |
| M6 | What do I think about what I remember? | Metacognitive Reflection + Reflective Experiences |

### Organ dependency map (ownership)

| Organ | Depends upon | Future dependents | Owns alone | Never assumes |
|-------|--------------|-------------------|------------|---------------|
| Identity | Experiences (content) | All | Who am I? | History rewrite |
| Experience | — | Concepts+ | Immutable history | Meaning / relations / recall |
| Concept | Experiences | Associations, Remembering+ | Meaning | History / relationships / recall |
| Association | Concepts (+Experiences) | Remembering+ | Relationships | Meaning / recall evaluation |
| Remembering | Identity, Experiences, Concepts, Associations, Goals, Attention, WM, Context, **Activation Architecture** | Reflection, Learning, Prediction, Planning, Creativity, Analogy, Metacognition | Activation-for-recall + reconstruction | Reflection, Learning, history rewrite |
| Reflection | Identity, Experiences, Concepts, Associations, Remembering (+ Activation via Remembering) | Learning, Prediction, Planning, Creativity, Metacognition | Evaluation + Reflective Experiences | Learning / planning / history rewrite |
| Activation Architecture | Concepts, Associations, Identity, Goals, WM, Context | Every future active organ | Shared field mechanics | Organ-specific questions |

### What new cognitive capability exists today that did not exist yesterday?

**ACM can now answer “What do I think about what I remember?”:** Reflection evaluates reconstructions for confidence, contradiction, consistency, patterns, questions, and hypotheses — birthing immutable Reflective Experiences without altering history — preparing Learning while establishing the Cognitive Capability Map as the architectural overview of ACM’s organs.

## Relationship to Aria

Aria remains the expected first consumer **after** ACM demonstrates maturity. Until then, Aria’s Memory continues under Daily Use Mode governance; ACM evolves independently.
