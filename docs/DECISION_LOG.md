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

## D007 — Plugin architecture before Identity (2026-07-14)

**Decision:** Document and ship a minimal `ExtensionRegistry` / hook protocol before Identity organ work; add `PLUGIN_ARCHITECTURE.md` and `CORE_BOUNDARIES.md`.

**Why:** Future modalities (vision, robotics, web) must attach without enlarging the cognitive core into a monolith.

**Status:** Accepted.

## D008 — Host-agnostic identity schema roles (2026-07-14)

**Decision:** ACM Identity uses roles `agent`, `user`, and `project` instead of Aria-named schemas. Architecture freeze text that says “Aria-self” is interpreted as **agent-self** for this host-agnostic engine (cross-ref `ARCHITECTURE.md` Identity Schema; contradiction recorded rather than silent rewrite of freeze narrative).

**Why:** ACM must never assume Aria exists (P10 still holds: identity emerges through experience under policy).

**Status:** Accepted.

## D009 — High-impact identity flips require assent (2026-07-14)

**Decision:** Conflicting identity attribute writes create pending proposals; active schema attributes change only via `assent_identity` or `encode(..., assent=True)`.

**Why:** Architecture Policy Gate / Sleep identity rules; prevents silent identity overwrite (test strategy §5.1).

**Status:** Accepted for M1.

## D010 — Schema nuclei vs content (2026-07-14)

**Decision:** Empty organizational schema concepts may exist as anchors; *content* attributes still arrive only through encode/experience (or assented proposals).

**Why:** Distinguishes structural privilege from prohibited profile-blob identity.

**Status:** Accepted.

## D011 — M2 is Experience, not Working Memory (2026-07-14)

**Decision:** Implementation milestone M2 answers *What happened?* via the Experience organ. Working-memory depth previously listed as roadmap M2 is deferred (now M3b) so Experiences become the foundation before Concepts/Associations/Remembering expansion.

**Why:** Architecture: nothing bypasses Experience; Concepts must grow from lived events.

**Status:** Accepted. Cross-ref `EXPERIENCE_MODEL.md`, `COGNITIVE_TIMELINE.md`.

## D012 — Experience content immutable; lifecycle/salience in overlays (2026-07-14)

**Decision:** Experience records are frozen. Corrections/reflections birth new Experiences with lineage links. Circulation lifecycle and current salience live in runtime overlays — never mutate birth content.

**Why:** History is never rewritten; relevance may still evolve for future remembering.

**Status:** Accepted.

## D013 — Self-improvement reserved, not implemented (2026-07-14)

**Decision:** M2 may record experiences that *describe* architectural ideas, but applying self-modification to ACM’s own cognitive architecture/policies requires future explicit user authorization. M2 does not implement self-mod.

**Why:** Learning evolves automatically; architecture change must remain assent-gated.

**Status:** Accepted (forward constraint).

## D014 — Future organs prefer Concepts over raw Experiences (2026-07-14)

**Decision:** Long-term direction is Experience → Concept → Association → Remembering → … Future organs should avoid manipulating raw Experiences when Concepts suffice. Recorded as architectural principle in Concept docs; not an M3 hard runtime ban.

**Why:** Meaning vs history separation; scalable cognition.

**Status:** Accepted (directional).

## D015 — Concepts keep prototypes and exemplars (2026-07-14)

**Decision:** Each Concept maintains a prototype (feature central tendency) and a capped exemplar list (Experience anchors). Not prototype-only or exemplar-only.

**Why:** Family resemblance plus lived instances best match experience-grounded cognition for future recognition.

**Status:** Accepted.

## D016 — Hierarchy lives in Concept organ, not Association organ (2026-07-14)

**Decision:** `is_a` / specialization edges are owned by `ConceptOrgan` in M3. M4 Association organ will add broader associative fabric without relocating taxonomy.

**Why:** Abstraction is part of meaning formation; avoids starting Associations early.

**Status:** Accepted.
