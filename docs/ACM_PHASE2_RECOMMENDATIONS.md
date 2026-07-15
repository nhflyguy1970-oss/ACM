# ACM Phase 2 Recommendations — After P1 Gate

**Status:** Phase Gate P1 (design only)  
**Date:** 2026-07-15  
**Companions:** [`ACM_V1_READINESS_REVIEW.md`](ACM_V1_READINESS_REVIEW.md) · [`SCIENTIFIC_GAP_ANALYSIS.md`](SCIENTIFIC_GAP_ANALYSIS.md) · [`ARIA_INTEGRATION_ARCHITECTURE.md`](ARIA_INTEGRATION_ARCHITECTURE.md)

## Posture

Phase 2 is **not** automatic. It starts only after you approve a track. This document ranks work by evidence, not by idle roadmap ambition.

---

## Track A — Required minor changes before Aria dual-write (engineering)

| ID | Work | Why | Science / eng grade | New organ? |
|----|------|-----|---------------------|------------|
| A1 | **Durable CognitiveStore interface** + first SQLite (or file) backend | In-process RAM cannot be Aria SoT | Engineering well-supported | No |
| A2 | **Export/import snapshots** of Experiences/Concepts/Associations | Migration + rollback | Engineering | No |
| A3 | **Source provenance fields** on Experience/Concept evidence (told/perceived/inferred/legacy_import) | Source monitoring science | Well-supported science; small schema | No |
| A4 | **Adapter design certification tests** in Aria (contract tests against ACM engines) | Integration safety | Eng | Lives in Aria |
| A5 | Document **SLO + feature flags** exactly as integration architecture | Ops | Eng | No |

**Gate:** Track A complete (or A1+A2+A4 minimum) before Phase A Shadow writes in Aria.

---

## Track B — Strongly recommended polish (still memory; parallel OK)

| ID | Work | Why | New organ? |
|----|------|-----|------------|
| B1 | Working buffer interference / focus refresh (M4b) | Baddeley-capacity faithfulness | No — deepen mechanism |
| B2 | Goal Space lifecycle polish (M5b) | Prospective memory / project continuity | No — deepen peer system |
| B3 | Confidence longitudinal calibration harness | Metamemory honesty | No — tooling |
| B4 | Optional embedding Activation prior via plugin | Cue quality without vector-as-memory | Plugin, not core organ |
| B5 | Observability doc bump to schema `0.12` everywhere hosts read | DX | Docs |

Track B may run **in parallel** with Aria Shadow if Track A is green.

---

## Track C — Explicitly deferred (do **not** start without new approval)

| Item | Reason |
|------|--------|
| Planning organ | Executive; consumes Goals — not memory gate |
| Decision Making / Executive Reasoning | Outside ACM |
| Creativity orchestration organ | Foundations exist in M13/M14 |
| Safe Self-Improvement | User-governed later |
| Aria UI Mission Control panels | Host work after adapter |
| Spatial map organ | Only if robotics requires; prefer plugin |

---

## Track D — Intentionally never (unless principles change)

| Item | Why |
|------|-----|
| Replace Experiences with vectors | Violates autobiography |
| Silent last-write-wins conflict | Violates M15 |
| ACM imports Aria / MC / Cap Bus | Violates host independence |
| Sleep births fabricated Experiences | Offline Cognition rule |

---

## Suggested versioning after Track A

| Version | Meaning |
|---------|---------|
| **0.12.x** | P1 docs + any tiny schema provenance without API break |
| **0.13.0** | Durable store interface + SQLite backend (still pre-1.0) |
| **1.0.0** | After Track A certified + dual-write Shadow green in Aria for an agreed period |

Declaring ACM **1.0** before durable store + Shadow evidence would overclaim.

---

## Scientific note

No Track A item invents a new cognitive *question*. They make existing cognitive functions **safe to host** and **truer to source monitoring**. That is the evidence-driven Phase 2 boundary.
