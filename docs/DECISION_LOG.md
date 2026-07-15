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

## D017 — Associations are directed and may be asymmetric (2026-07-15)

**Decision:** Association organ stores independent `strength_forward` and `strength_backward`. Relation kinds may default toward symmetry (co-activation, resembles) or strong asymmetry (`is_a_traffic`, part_of, caused_by, depends_on, …). Taxonomic `is_a` remains owned by the Concept organ (D016); Associations may mirror hierarchy as `is_a_traffic` for cognitive traversal without relocating taxonomy.

**Why:** Human activation is often directional (Dog → Animal stronger than Animal → Dog). Symmetric-only edges would erase cognitively meaningful asymmetry and would underprepare analogical / retrieval traversal.

**Status:** Accepted.

## D018 — Remembering reconstructs via shared Activation Architecture (2026-07-15)

**Decision:** M5 introduces a single canonical **Cognitive Activation Architecture** (`acm/activation`) consumed first by the **Remembering organ**. Remembering answers *What do I remember?* by reconstructing from activated Concepts/Associations with Experience participation as evidence. Experiences remain immutable. Competing activations may yield ambiguity rather than forced certainty. Forgetting is not implemented; accessibility may later cool without deletion.

**Organ map for this decision:**

| Item | Content |
|------|---------|
| Depends upon | Identity, Experiences, Concepts, Associations, Goals, Attention, WM, Context |
| Future dependents | Reflection, Learning, Prediction, Planning, Creativity, Analogy, Metacognition |
| Owns alone | Recall-time activation + reconstruction |
| Never assumes | History rewrite, Concept meaning, Association typology, Reflection/Learning |

**Why:** Retrieval/search/RAG are insufficient for human-like cognition; one shared activation model prevents each future organ inventing a parallel mechanism.

**Status:** Accepted.

## D019 — Reflection evaluates; Reflective Experiences record history (2026-07-15)

**Decision:** M6 Reflection organ answers *What do I think about what I remember?* by evaluating Remembering reconstructions and birthing immutable **Reflective Experiences** (`CognitiveKind.REFLECTION`, `reflects_on` lineage). Reflection reuses the Cognitive Activation Architecture through Remembering — it does not invent a second activation model. Confidence assessment is evaluative metadata / artifact content, not silent overwrite of Concept confidence. Intellectual honesty outcomes (`insufficient_evidence`, contradictions, questions, hypotheses) are first-class.

**Organ map for this decision:**

| Item | Content |
|------|---------|
| Depends upon | Identity, Experiences, Concepts, Associations, Remembering |
| Future dependents | Learning, Prediction, Planning, Creativity, Metacognition |
| Owns alone | Evaluation of reconstructions + Reflective Experience birth |
| Never assumes | Learning/adaptation, planning, history rewrite, Concept meaning |

**Why:** Metacognition requires observable evaluation that leaves auditable history for future Learning without secretly mutating prior cognition.

**Status:** Accepted.

## D020 — L0 Learning design before M7 implementation (2026-07-15)

**Decision:** Before implementing the Learning organ, ACM completes **L0**: research-graded foundations, Learning Architecture, Governance (automatic vs assent vs never), Lifecycle, permanent `COGNITIVE_RESEARCH_FOUNDATIONS.md`, and post-M6 Architecture Review. Learning is defined as *governed durable adaptation of living structures* answering *What have I learned?* — distinct from Remembering, Reflection, Concept nucleation, knowledge import, and architectural self-improvement. M7 Learning code is **not authorized** until L0 is merged and accepted. No Learning prototypes in L0.

**Why:** Learning is the first organ that permanently changes other organs; trust requires lineage, gates, and scientific/engineering clarity before code.

**Status:** Accepted (design). Implementation authorized and shipped as M7 (v0.8.0).

## D021 — M7 Learning + M8 Offline Cognition as separate organs (2026-07-15)

**Decision:** Implement Learning and Offline Cognition as **two organs** sharing one cognitive lifecycle. Learning answers *What have I learned?* via Adaptation Records consumed from Reflective Experiences. Offline Cognition answers *What should become long-term memory?* via functional consolidation (replay, stabilize, cool, propose) without inventing Experiences or talking to the outside world. They share Adaptation lineage (`sleep_batch_id`) but never merge responsibilities. Forgetting / Prediction / Planning / Creativity / Aria remain out of scope.

**Why:** Human cognitive memory separates online adaptation from offline consolidation; ACM must not collapse sleep into Learning or treat Learning as an offline-only batch job.

**Status:** Accepted.

## D022 — Adaptive confidence triad (2026-07-15)

**Decision:** Confidence evolves as Reflection evaluates → Learning adjusts (capped) → Offline Cognition stabilizes through replay. Experience content remains immutable; confidence lives on living structures and Adaptation before/after vectors.

**Why:** Matches functional consolidation evidence without simulating neural overnight processes.

**Status:** Accepted.

## D023 — Attention allocates; never plans (2026-07-15)

**Decision:** M9 Attention & Memory Priority owns allocation and evolving investment on living structures. Goals bias Attention; Goals do not own priority. Attention modulates the singular Activation Architecture and never becomes planning, prediction, or executive decision making.

**Why:** Human attention is a memory resource gate, not a planner.

**Status:** Accepted.

## D024 — Forgetting is accessibility policy; Offline requests cools (2026-07-15)

**Decision:** M10 owns accessibility stages, cool, and reactivation. Offline Cognition may request weak-association cools; Forgetting applies them. Experiences remain immutable; prune-eligibility is proposal-only. Strong cues can restore dormant accessibility through Activation + reactivation.

**Why:** P17 — most forgetting is deactivation, not deletion; ownership must not collapse Offline into Forgetting.

**Status:** Accepted.

## D025 — Prediction estimates; never plans (2026-07-15)

**Decision:** M11 Prediction owns probabilistic anticipated memory outcomes via Activation + Associations. It never selects actions, plans goal sequences, or makes decisions. Confidence evolves from feedback / Learning / Offline residue.

**Why:** Prospective memory is not executive control.

**Status:** Accepted.

## D026 — Simulation is hypothetical memory; never history or planning (2026-07-15)

**Decision:** M12 Mental Simulation owns temporary Hypothetical Sequences clearly tagged non-historical. It may reuse Prediction for anchors but never births Experiences, never plans, never decides. Planning remains a later consumer organ.

**Why:** Episodic future thinking must not corrupt autobiography or become a planner.

**Status:** Accepted.

## D027 — Recombination blends; never plans or invents history (2026-07-15)

**Decision:** M13 Memory Recombination owns temporary novel blends of existing fragments. Prediction/Simulation may supply hints. Never births Experiences; never plans or decides. Distinct from M12 Simulation (prospective paths).

**Why:** Constructive memory creativity without executive control.

**Status:** Accepted.

## D028 — Analogy maps structure; never executive reasoning (2026-07-15)

**Decision:** M14 Analogical Reasoning owns explainable structure-mapping across domains. Why-codes only. Never decisions, planning, or theorem-proving. Builds on M4 Association foundations.

**Why:** Analogy is memory correspondence, not an executive reasoner.

**Status:** Accepted.

## D029 — Reconciliation never rewrites history (2026-07-15)

**Decision:** M15 Memory Reconciliation owns conflict/corroboration classification and creates new `ReconciliationRecord` lineage. It never deletes Experiences, never edits immutable artifacts, and never silently discards competing traces. Statuses include reinforce, unresolved, context_dependent, competing, and revised (artifact only).

**Why:** Human memory retains conflicting evidence; reconciliation updates living summaries with explainable lineage.

**Status:** Accepted.

## D030 — Confidence/Uncertainty is a memory organ, not executive cognition (2026-07-15)

**Decision:** M16 Uncertainty & Confidence owns estimation, evolution, propagation, and recalibration of living memory confidence (and uncertainty kinds). It recalibrates from Reconciliation but does not own reconciliation lineage. Never plans or decides. Every significant evolution is observable via harness events.

**Why:** Certainty about memory accuracy is metamemory — not planning, decision making, or Aria policy.

**Status:** Accepted.

## D031 — Phase Gate P1 verdict: READY WITH MINOR CHANGES (2026-07-15)

**Decision:** After scientific, architectural, engineering, and comparative review of ACM v0.12, the official readiness verdict is **READY WITH MINOR CHANGES**. ACM may proceed toward Aria dual-write only after Track A (durable store, provenance, adapter contract tests). Declaring ACM 1.0 as Aria’s sole SoT before Shadow certification is rejected.

**Why:** Core cognitive memory lifecycle is scientifically adequate; production host readiness still lacks durable substrate and migration evidence.

**Status:** Accepted. Evidence: `ACM_V1_READINESS_REVIEW.md`, `SCIENTIFIC_GAP_ANALYSIS.md`.

## D032 — No new cognitive organs before Aria Shadow (2026-07-15)

**Decision:** Do not invent Planning, Decision Making, Creativity orchestration, or other new organs as prerequisites for Aria memory integration. Adapter code lives in Aria (or host package), not inside ACM. Vector/RAG must not become ACM’s cognitive model.

**Why:** Integration risk is engineering/host boundary, not missing memory organs; feature-copying AI frameworks would regress cognition.

**Status:** Accepted. See `ACM_PHASE2_RECOMMENDATIONS.md`, `ACM_COMPARATIVE_RESEARCH.md`, `ARIA_INTEGRATION_ARCHITECTURE.md`.
