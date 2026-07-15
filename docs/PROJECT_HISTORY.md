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
- **2026-07:** L0 Learning research & architecture — design-only foundations for M7. Released as v0.7.1. **No Learning organ code.**
- **2026-07:** M7 Learning + M8 Offline Cognition — first complete adaptive memory cycle (Adaptation Records; sleep replay/consolidation). Released as v0.8.0.

## Milestone cognitive questions

| Milestone | Question | Capability |
|-----------|----------|------------|
| M1 | Who am I? | Emergent Identity schemas |
| M2 | What happened? | Immutable Experience chronology |
| M3 | What is this? | Emergent Concepts / understanding |
| M4 | How is this related? | Living Associations / cognitive networks |
| M5 | What do I remember? | Active reconstruction + Activation Architecture |
| M6 | What do I think about what I remember? | Metacognitive Reflection + Reflective Experiences |
| L0 | (design) What have I learned? | Research + architecture authorizing M7 |
| M7 | What have I learned? | Learning organ + Adaptation Records |
| M8 | What should become long-term memory? | Offline Cognition (Sleep & Consolidation) |

### Organ dependency map (ownership)

| Organ | Depends upon | Future dependents | Owns alone | Never assumes |
|-------|--------------|-------------------|------------|---------------|
| Identity | Experiences (content) | All | Who am I? | History rewrite |
| Experience | — | Concepts+ | Immutable history | Meaning / relations / recall |
| Concept | Experiences | Associations, Remembering+ | Meaning | History / relationships / recall |
| Association | Concepts (+Experiences) | Remembering+ | Relationships | Meaning / recall evaluation |
| Remembering | Identity, Experiences, Concepts, Associations, Goals, Attention, WM, Context, **Activation Architecture** | Reflection, Learning, Prediction, Planning, Creativity, Analogy, Metacognition | Activation-for-recall + reconstruction | Reflection, Learning, history rewrite |
| Reflection | Identity, Experiences, Concepts, Associations, Remembering (+ Activation via Remembering) | Learning, Prediction, Planning, Creativity, Metacognition | Evaluation + Reflective Experiences | Learning / planning / history rewrite |
| Learning | M1–M6 + Reflective Experiences + governance | Offline Cognition, Prediction, Planning, Creativity, Forgetting | Durable governed adaptation (Adaptation Records) | History rewrite; architecture self-mod |
| Offline Cognition | Learning + living structures + Activation (read-only replay) | Forgetting (future), improved Remembering | Replay, consolidation, abstraction proposals | Inventing Experiences; external I/O; architecture change |
| Activation Architecture | Concepts, Associations, Identity, Goals, WM, Context | Every future active organ | Shared field mechanics | Organ-specific questions |

### What new cognitive capability exists today that did not exist yesterday?

**ACM now completes its first adaptive memory cycle:** Experience → Remembering → Reflection → Learning → Offline Cognition → improved living memory — without rewriting Experience history. Learning owns governed Adaptation Records; Offline Cognition owns sleep-like replay and consolidation. Forgetting, Prediction, Planning, Creativity, and Aria integration remain out of scope.

## Relationship to Aria

Aria remains the expected first consumer **after** ACM demonstrates maturity. Until then, Aria’s Memory continues under Daily Use Mode governance; ACM evolves independently.
