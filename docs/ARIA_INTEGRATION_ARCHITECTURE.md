# Aria Integration Architecture — Design Only

**Status:** Phase Gate P1 (design freeze for migration *plan*)  
**Date:** 2026-07-15  
**Implementation:** **FORBIDDEN** until explicit approval after readiness verdict.  
**Companions:** [`ACM_V1_READINESS_REVIEW.md`](ACM_V1_READINESS_REVIEW.md) · [`CORE_BOUNDARIES.md`](CORE_BOUNDARIES.md) · [`PLUGIN_ARCHITECTURE.md`](PLUGIN_ARCHITECTURE.md)

## Placement

ACM remains an **external dependency**. Aria never becomes an import inside ACM.

```text
┌─────────────────────────────────────────────────────────────┐
│ Aria / Jarvis UI · Router · REST · Cap Bus · Mission Control│
└────────────────────────────┬────────────────────────────────┘
                             │ compatibility façade
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ aria_core.memory_manager  (stable events + MC panel API)    │
│        └── AcmMemoryAdapter (NEW — lives in Aria, not ACM)  │
└───────────────┬─────────────────────────────┬───────────────┘
                │                             │ dual-write / cutover
                ▼                             ▼
        acm.CognitiveEngine            legacy MemoryStore
        (Experiences/Concepts/…)       (SQLite/JSON + embeddings)
```

**Rule:** Adapter code ships in the Aria/Jarvis tree (or a thin `aria-acm-adapter` package). ACM core stays host-free.

---

## Verb mapping

| Aria / Cap Bus / Behavior today | ACM cognitive verb | Notes |
|---------------------------------|--------------------|-------|
| `remember` / `MemoryStore.add` | `encode` | Birth Experience + Concept residue |
| `recall` / `search_memory` / `prepare_context` | `remember` / `what_do_i_remember` | Activation reconstruction; optional light reconsolidation |
| `memory_correct` / supersede | `revise_experience` + Learning/Reflection path | Never silent overwrite of Experience |
| `memory_forget` / soft delete | `cool_memory` / Forgetting organ | Hard erase remains Policy Gate + rare |
| `run_consolidation` / nightly distill | `sleep` | Offline Cognition; LLM distill becomes *optional proposer* outside ACM |
| `propose_memory` / commit / rollback | Learning `assent` / `reject` / `rollback` | Align Learning Manager |
| Profile / “about user” | `who_am_i` + Identity / Concepts | Emergent, not static bio blob |
| Confidence UI (future) | `how_certain_am_i` | Metamemory |
| Conflict / contested facts | `how_should_memory_reconcile` | Lineage |

Cap Bus **external** names (`remember`/`recall`) may remain stable; adapter translates.

---

## Migration strategy (phased)

### Phase A — Shadow (dual-write)

1. Aria writes continue to legacy store (authoritative reads).  
2. Adapter also calls `encode` into ACM CognitiveEngine (durable backend required).  
3. ValidationHarness metrics exported alongside Trace (no content leakage).  
4. Mission Control shows “ACM shadow” health: encode counts, activation latency, conflict rates.

**Exit criteria:** Shadow encode success ≥ threshold; no Identity corruption; harness stable.

### Phase B — Read parallel (harvest)

1. For selected namespaces (e.g., preferences, identity facts), dual-read ACM vs legacy; log disagreement via Reconciliation.  
2. Harvest script maps legacy entries → `encode` Experiences with provenance tags (`source=legacy_import`).  
3. User-visible recall still legacy unless feature flag.

**Exit criteria:** Reconciliation competing rate understood; user can assent Identity diffs.

### Phase C — Remembering primary

1. Feature flag: Cap Bus `recall` / chat `prepare_context` use ACM `remember`.  
2. Legacy search becomes fallback on ACM miss / error.  
3. Contested answers show ExplanationClass + confidence (templates only).

**Exit criteria:** Latency SLO met; Trace organs.memory filled with ACM classes; fallback < threshold.

### Phase D — Legacy soft-retire

1. Writes ACM-only; legacy become export archive.  
2. Platform DualWriteMemoryAdapter taught to mirror **projections** (optional Experiences/Concept public views), not flat facts only — or retired.  
3. Nightly LLM consolidation demoted to optional extension proposing Reflective Experiences / Learning adaptations — never silent Experience rewrite.

---

## Rollback strategy

| Trigger | Action |
|---------|--------|
| Encode/shadow error spike | Disable ACM write; keep legacy |
| Read-primary quality regression | Flip flag to legacy recall |
| Identity assent incidents | Freeze Identity integrate; require host assent review |
| Latency SLO breach | Fall back prepare_context to hierarchical_search |
| Data integrity suspicion | Freeze; export ACM + legacy snapshots; do not auto-merge |

Rollback never *deletes* ACM Experiences already encoded; cut write path only. Keep dual snapshots for audit.

---

## Compatibility layer

**Package (conceptual):** `AcmMemoryAdapter` implementing the current `aria_core.memory_manager` method surface (or a subset behind the same façade).

Responsibilities:

- Map CRUD → cognitive verbs  
- Preserve events: `MemoryWritten`, `MemorySearch`, … (ids/counts/latency only)  
- Extend Trace `memory_operation` with ACM classes: verb, attention_class, reconsolidation class, policy outcomes, confidence deltas (no CoT / no prompts)  
- Translate Policy Gate ↔ Aria assent UX  
- Namespace mapping: legacy layers ↔ context tags / Concept roles  

Non-responsibilities:

- Mission Control UI rendering (host)  
- LLM prompt construction (host)  
- Planning / Cap Bus orchestration policy (host)

---

## Mission Control integration

| Panel need | Source |
|------------|--------|
| Health / counters | Adapter mirrors `validation.snapshot()` aggregates + legacy stats during A–C |
| Latency | CognitiveTraceEvent.latency_ms |
| Confidence viz | M16 snapshots / confidence organ events (aggregated) |
| Conflict / reconciliation | M15 status histogram |
| Content | **Never** shown in MC events — same as today’s privacy rule |

ACM must not import Mission Control. MC pulls via Aria aggregator as today (`mission_control_panel`).

---

## Conversation Trace integration

Extend Trace organ slot without breaking schema majors:

```json
"organs": {
  "memory": {
    "used": true,
    "read": true,
    "write": false,
    "latency_ms": 12,
    "acm_verb": "remember",
    "attention_class": "goal",
    "reconsolidation": "light",
    "confidence": 0.72,
    "ambiguous": false
  }
}
```

Values are observables only.

---

## Learning integration

| Today | Target |
|-------|--------|
| Learning Manager propose/commit | Map to Learning organ adaptations + assent |
| Document/observation learners | `encode` with context tags + envelopes |
| Nightly distill | Propose Reflective Experience text → Reflection/Learning — host LLM is proposer, ACM owns durable adaptation |

---

## Memory & confidence visualization

Host widgets (not ACM):

- Timeline (`what_happened` / timeline API)  
- Identity snapshot  
- Confidence histograms over time  
- Reconciliation lineage tree (record statuses)

ACM supplies **public JSON** only.

---

## Observability & error handling

| Class | Handling |
|-------|----------|
| Soft ACM failure | Log + legacy path; emit Memory* error counts |
| Policy Gate block | Return proposed status; UI assent — do not raise as hard crash |
| Persist failure | Fail encode; do not half-write Experiences |
| Ambiguous remember | Set `ambiguous=true`; host may ask clarifying question (host logic) |

---

## Performance expectations (design targets)

| Operation | Design target (local durable) |
|-----------|-------------------------------|
| encode | p95 < 50 ms (text) |
| remember (active field) | p95 < 100 ms for ≤10k concepts |
| sleep batch | async / scheduled; not on chat hot path |
| harness snapshot | < 20 ms |

Scale path: swappable CognitiveStore (SQLite → later DB). In-process dict is **not** Aria production SoT.

---

## Failure modes

1. Dual-write divergence → Reconciliation competing spike  
2. Cue tokenizer too weak → recall misses (mitigate embeddings as Activation prior plugin)  
3. Over-trust of high heuristic confidence → UI calibration banner  
4. Plugin LLM inventing sleep facts → blocked if Experience birth from Sleep forbidden (already Offline rule)

---

## Version compatibility

| Rule | Detail |
|------|--------|
| ACM dependency | Pin `aria-cognitive-memory>=0.12,<1.0` during dual-write; reassess at ACM 1.0 |
| Cap Bus | Keep remember/recall names through Phases A–C |
| Events | Additive fields only in minor Aria releases |
| ACM major | Host upgrades after adapter certification |

---

## Public interfaces (frozen for design)

**ACM (already shipped):** `CognitiveEngine` verbs listed in `API.md`.  

**Aria (to implement later):** `AcmMemoryAdapter` + feature flags `ACM_SHADOW_WRITE`, `ACM_READ_PRIMARY`, `ACM_WRITES_ONLY`.

**Do not** publish ACM Identity labels using Aria-specific schema names (agent/user/project already host-agnostic — D008).

---

## Success of this document

This file is sufficient to implement migration **after approval**. It does not authorize coding.
