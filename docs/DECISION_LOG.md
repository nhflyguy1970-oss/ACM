# Decision Log

Significant architectural and implementation decisions. Deviations from the design freeze must appear here.

## D001 — Standalone repository (2026-07-14)

**Decision:** ACM lives in its own git repository with independent versioning, CI, docs, and release cycle.

**Why:** Host independence is non-negotiable; Aria imports would conflate product boundaries.

**Status:** Accepted.

## D002 — Design freeze remains normative (2026-07-14)

**Decision:** `MEMORY_DESIGN_PRINCIPLES.md`, `ARCHITECTURE.md` (v2.1), and `COGNITIVE_MEMORY_TEST_STRATEGY.md` remain canonical. Implementation may not silently rewrite them.

**Why:** Cognition before implementation; contradictions must be explicit proposals.

**Status:** Accepted. Architecture banner updated only to note implementation authorization in this repo.

## D003 — In-memory CognitiveStore for M0 (2026-07-14)

**Decision:** M0 substrate is process-local in-memory storage.

**Why:** Informative technology choice; cognition API must not couple to a particular database. Swappable later without changing cognitive verbs.

**Status:** Accepted (temporary substrate).

## D004 — Explanation template classes only (2026-07-14)

**Decision:** Public explanations map to closed `ExplanationClass` templates (P22).

**Why:** Avoid fabricating chain-of-thought; keep observability cognitive and auditable.

**Status:** Accepted.

## D005 — Sleep does not auto-merge concepts (2026-07-14)

**Decision:** Sleep may prune very weak edges; concept merge candidates are **proposals only** at M0.

**Why:** High-impact structural change requires stronger validation (architecture sleep organ).

**Status:** Accepted for M0; revisit at M8.

## D006 — No Aria wiring in this phase (2026-07-14)

**Decision:** No host adapter in-repo that imports Aria; migration deferred until ACM maturity.

**Why:** Project mission for Foundation Build.

**Status:** Accepted.
