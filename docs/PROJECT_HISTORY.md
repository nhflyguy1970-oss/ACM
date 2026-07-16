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
- **2026-07:** M9 Attention & Memory Priority + M10 Accessibility & Forgetting — priority-driven cognition and human-like soft forgetting. Released as v0.9.0.
- **2026-07:** M11 Prediction + M12 Mental Simulation — memory-driven likelihood and hypothetical futures. Released as v0.10.0.
- **2026-07:** M13 Memory Recombination + M14 Analogical Reasoning — novel blends and structure-mapping. Released as v0.11.0.
- **2026-07:** M15 Memory Reconciliation + M16 Uncertainty & Confidence — conflict lineage and evolvable certainty. Released as v0.12.0. Maturity review: `docs/ACM_MATURITY_REVIEW_v1.md`.
- **2026-07:** Phase Gate P1 — Integration Readiness + Scientific Gap Analysis (**design only**). Verdict: **READY WITH MINOR CHANGES**. Released as v0.12.1. See `docs/ACM_V1_READINESS_REVIEW.md`.
- **2026-07:** Phase 2 Operational Readiness (P2.1–P2.5) — durable store, provenance, adapter, shadow, certification framework. **No new cognition.** Released as v0.13.0. See `docs/OPERATIONAL_READINESS.md`.
- **2026-07:** Phase 2 Operational Certification Execution — measured all gates. Verdict: **CERTIFIED WITH CONDITIONS**. Released as v0.14.0 (evidence docs only). See `docs/ACM_CERTIFIED_v1.md`.
- **2026-07:** Aria ACM Integration Blueprint (**design only**) — full cognitive memory **replacement** via independent Aria-embedded ACM copy; ACM Supremacy Rules (D036–D037). Docs live under Jarvis `docs/acm_integration/`. Released as ACM v0.14.1 (governance docs only). **No Aria/ACM implementation.**
- **2026-07:** **Memory Authority** architectural correction (D038) — Cognitive Response Pipeline; LM never determines memory; unknown is knowledge; speech contamination blocked; soft confabulation refused. Released as **v0.15.0**. Standalone only until promotion approval.
- **2026-07:** **Cognitive Intent Classification & Routing** architectural correction (D039) — every request classified by cognitive intent; Cognitive Routing Engine assigns organ ownership; LM never chooses the organ; assistant vs user identity; goals/projects/reflection/learning routed correctly. Released as **v0.16.0**. Standalone only until promotion approval.
- **2026-07:** **End-to-End Cognitive Dispatch** architectural correction (D040) — Cognitive Dispatch Engine; organ-only termination; multi-organ reconstruction; diagnostics; sanitize raw storage/learning dumps; user identity without assistant bleed. Released as **v0.17.0**. Standalone only until promotion approval.
- **2026-07:** **Semantic Extraction** implementation correction (D041) — NL → structured cognitive facts before organ storage; perspective resolution; instructional strip; evidence separation. Released as **v0.18.0**. Standalone only until promotion approval.
- **2026-07:** **Identity pipeline debug** (D042) — stop identity-schema cue pollution; user-identity confidence from name attributes; `Who am I?` → `Your name is Jeff.` Released as **v0.18.1**. Standalone only until promotion approval.

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
| M9 | What deserves cognitive attention and continued memory investment? | Attention & Memory Priority |
| M10 | What should become harder to remember? | Accessibility & Forgetting |
| M11 | Based upon memory, what is likely? | Prediction |
| M12 | What possible futures can memory imagine? | Mental Simulation |
| M13 | What new memories can emerge by recombining existing memories? | Memory Recombination |
| M14 | What existing memories are analogous even when they appear different? | Analogical Reasoning |
| M15 | When memories disagree, how should memory reconcile them? | Memory Reconciliation |
| M16 | How certain am I that this memory is accurate? | Uncertainty & Confidence |
| P1 | (design) Is ACM ready for Aria / 1.0? | Readiness + scientific gap gate |
| P2 | (engineering) Is ACM operationally ready? | Durable store · provenance · adapter · shadow · certification framework |

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
| Offline Cognition | Learning + living structures + Activation (read-only replay) | Forgetting (accessibility), improved Remembering | Replay, consolidation, abstraction proposals | Inventing Experiences; external I/O; architecture change |
| Attention & Priority | Goals, Identity, living Concept importance, cue context | Encode/Remember/Reflect/Learn/Offline bias | Allocation + priority investment | Planning; decision making; deletion |
| Accessibility & Forgetting | Neglect, Offline cool requests, host soft-forget | Remembering thresholds; reactivation | Accessibility stages; cool; reactivate | Experience deletion; history rewrite |
| Prediction | Activation + Associations + Priority + Accessibility + Learning residue | Simulation (optional anchors); future Planning (consumer only) | Probabilistic memory outcomes | Planning; decisions; actions |
| Mental Simulation | Activation + living structures + Prediction hints | Future Planning (consumer); Creativity (later) | Hypothetical sequences | Experience birth; planning; decisions |
| Memory Recombination | Activation + fragments + Prediction/Simulation hints | Creativity foundations; Analogy (coop) | Temporary RecombinedMemory | Experience birth; planning |
| Analogical Reasoning | Neighborhoods, resembles, hierarchy, relation patterns | Transfer / Creativity foundations | Explainable AnalogyMapping | Executive reasoning; decisions |
| Memory Reconciliation | Activation + conflicts/corroboration signals + Confidence collab | Living certainty updates via Confidence | ReconciliationRecord lineage | History rewrite; planning; decisions |
| Uncertainty & Confidence | Living graph + Reconciliation deltas + Learning/encode | All metacognitive consumers | Confidence evolution + uncertainty kinds | Planning thresholds; decisions |
| Activation Architecture | Concepts, Associations, Identity, Goals, WM, Context, Attention, Accessibility | Every future active organ | Shared field mechanics | Organ-specific questions |

### What new cognitive capability exists today that did not exist yesterday?

**Semantic Extraction (v0.18.0 / D041):** encode now forms structured cognitive facts before organ storage. Not a new organ — an implementation correction to the existing pipeline.


## Relationship to Aria

**Target architecture (D036):** Aria vendors an independent certified ACM **source copy** as its sole cognitive memory. Standalone ACM remains research/reference — not a pip/runtime shared dependency and not auto-synced. Promotion is explicit only.

**Policy (D037):** ACM Supremacy Rules — single cognitive authority; no lost functionality without mapped disposition; no legacy overrides; no duplicate cognition; migration INTO ACM only; no architectural regression without re-certification.

Reference `aria_memory_adapter` remains a Shadow/translation design aid. Implementation wiring is approval-gated. Blueprint: Jarvis `docs/acm_integration/` (also cites earlier `ARIA_INTEGRATION_ARCHITECTURE.md` · `OPERATIONAL_READINESS.md` · `ACM_CERTIFIED_v1.md`).
