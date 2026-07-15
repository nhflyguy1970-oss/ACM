# Memory Reconciliation — ACM

**Status:** Canonical for M15 (implemented)  
**Cognitive question:** *When memories disagree, how should memory reconcile them?*  
**Companions:** [`EVIDENCE_AND_CORROBORATION.md`](EVIDENCE_AND_CORROBORATION.md) · [`HUMAN_MEMORY_CONFLICTS.md`](HUMAN_MEMORY_CONFLICTS.md) · [`CONFIDENCE_MODEL.md`](CONFIDENCE_MODEL.md) · [`UNCERTAINTY_MODEL.md`](UNCERTAINTY_MODEL.md)

## Human memory reality check

| # | Question | Answer |
|---|----------|--------|
| 1 | Exists in human cognitive memory? | Yes — source monitoring, conflict retention, reconsolidation with lineage |
| 2 | Memory process (not executive)? | Yes — resolves what memory believes, does not choose actions |
| 3 | Models function not mechanism? | Yes — reconciliation artifacts, not synaptic micro-mechanics |
| 4 | ACM ≠ Aria boundary preserved? | Yes — no host planning/decision |
| 5 | Makes ACM more like human memory? | Yes — competing traces coexist; history is never silently deleted |

## Scientific foundations

| Grade | Finding |
|-------|---------|
| **Well-supported** | Multiple traces can coexist; corroboration strengthens belief; conflict raises uncertainty; revision does not erase the earlier episode (source monitoring / constructive memory) |
| **Emerging** | Precise neural reconciliation circuits; how context gates competing episodic details |
| **Speculation** | Exact weighted jury of autobiographical contests |

Never present speculation as established science.

## Biological function

Memory must stay coherent without destroying evidence. Organisms accumulate corroboration, retain contradictions, and revise living summaries while episodic history remains addressable. Reconciliation exists so remembering can remain useful under incomplete and contradictory experience.

## Technical function

| Field | Content |
|-------|---------|
| Organ | `ReconciliationOrgan` |
| Public API | `CognitiveEngine.how_should_memory_reconcile(cue)` |
| Verb | `MemoryVerb.RECONCILE` |
| Inputs | Activation field, Concept attributes, `conflicts_with` Associations, Reflective outcomes, Prediction dispersion, context tags |
| Outputs | `ReconciliationRecord` with status + explainable factors |
| Statuses | `reinforce` · `unresolved` · `context_dependent` · `competing` · `revised` |
| Validation | `acm.validation/0.12` → `reconciliation` aggregate |
| Collaboration | Calls Confidence organ for living recalibration — does not own confidence policy |

## Ownership

| Owns | Does not own |
|------|----------------|
| Conflict detection & reconciliation lineage | Deleting / rewriting Experiences |
| Corroboration vs conflict classification | Confidence estimation policy (M16) |
| Explainable reconciliation summaries | Planning, decisions, executive reasoning |
| | Second Activation Architecture |

## Intentional omissions

Belief-revision theorem engines; forced unique winners; silent discard; LLM-mediated arbitration; executive choice of which “truth” to act on (deferred to Aria / planning phases).
