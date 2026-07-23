# API — ACM v0.7

Public surface is intentionally small. Hosts integrate through `CognitiveEngine`; adapters and storage backends may evolve underneath without expanding the verb set casually.

See also: [`COGNITIVE_CAPABILITY_MAP.md`](COGNITIVE_CAPABILITY_MAP.md) · [`REFLECTION_MODEL.md`](REFLECTION_MODEL.md) · [`REMEMBERING_MODEL.md`](REMEMBERING_MODEL.md) · [`COGNITIVE_ACTIVATION_ARCHITECTURE.md`](COGNITIVE_ACTIVATION_ARCHITECTURE.md)

## Install

```bash
pip install -e ".[dev]"
```

```python
from acm import CognitiveEngine, RememberResult, ValidationHarness
```

## `CognitiveEngine`

### Constructor

```python
CognitiveEngine(*, agent_id: str = "agent", buffer_capacity: int = 7)
```

- `agent_id` — opaque host label (not Aria-specific).
- `buffer_capacity` — working-memory slots (default 7).

### Context & goals

| Method | Purpose |
|--------|---------|
| `set_context(*tags, activity="", place="")` | Set active context frame |
| `open_goal(title, *, importance=0.6) -> goal_id` | Open an active goal |
| `complete_goal(goal_id)` | Mark goal completed |

### Cognitive verbs

#### `encode(text, *, kind="experience", pin=False, context_tags=None, assent=False, proposal_id=None, external_kind="text", envelope_ids=None, revises_id=None, reflects_on_id=None, t_start=None, t_end=None) -> dict`

Births an **immutable Experience** (and may update identity / provisional concept residue) when attention / kind warrants durability.

Typical encode `kind` values: `experience`, `preference`, `identity`.

Optional: `external_kind` (modality), `envelope_ids`, `revises_id` / `reflects_on_id` (lineage), temporal bounds.

Returns at least: `encoded`, and on success `experience_id`, `concept_id`, `attention`, `importance`, `identity`, `experience` (public view).

High-impact identity conflicts return `identity.status == "proposed"` with a `proposal_id` unless `assent=True`.

#### `remember(query) -> RememberResult`

Active **Remembering** — reconstructs via the shared Cognitive Activation Architecture (not search/RAG). Fields:

| Field | Meaning |
|-------|---------|
| `answer` | User-facing recollection text |
| `explanation` | Template-class explanation only (no CoT) |
| `explanation_class` | Enum class (`preference`, `experience`, …) |
| `activated_concept_ids` | What activated |
| `confidence` | Recalled confidence |
| `ambiguous` | Competing recollections nearby |
| `reconstruction` | Public reconstruction package (activation path metadata) |
| `trace` | Public cognitive-state metadata |

#### `what_do_i_remember(cue) -> dict`

Cognitive question M5 façade over `remember()` — returns the reconstruction public view.

#### `what_do_i_think(cue) -> dict`

Cognitive question M6 — evaluates the reconstruction and births a Reflective Experience. Returns outcomes, confidence assessment, questions/hypotheses, and lineage ids. Does not rewrite history.

#### `sleep(*, apply_low_impact=True) -> dict`

Consolidation pass: prune weak edges (optional); record merge *proposals* without auto-applying high-impact structure changes.

#### `metacognitive_sketch() -> dict`

Foundations for self-modeling: counts of known / uncertain concepts, experiences, goals, identity observables, extensions, encode/remember counts, buffer occupancy, context. **Not** consciousness.

### Experience

| Method | Purpose |
|--------|---------|
| `what_happened(**filters)` | Chronological answer to *What happened?* |
| `timeline()` | Events + temporal links + observables |
| `revise_experience(id, text, …)` | Correction → new Experience + lineage |
| `reflect_on(id, text, …)` | Reflection → new Experience + lineage |
| `engine.experiences` | Experience organ (envelopes, salience touch, retire/awaken) |

### Concepts

| Method | Purpose |
|--------|---------|
| `what_is_this(cue)` | Answer *What is this?* from emergent Concepts |
| `engine.concepts.recognize(cue)` | Similarity / seen-before hook (not Remembering) |
| `engine.concepts` | Nuclei, hierarchy, prototypes, weaken/resurrect |

### Associations

| Method | Purpose |
|--------|---------|
| `how_related(left, right)` | Answer *How is this related?* (direct or neighborhood path) |
| `engine.associations.neighborhood(cue)` | Cognitive neighborhood of a Concept |
| `engine.associations.clusters()` | Emergent connected communities |
| `engine.associations` | Relate / reinforce / weaken / absorb / observables |

### Remembering

| Method | Purpose |
|--------|---------|
| `remember(query)` | Reconstruct a recollection (Activation Architecture) |
| `what_do_i_remember(cue)` | *What do I remember?* public package |
| `engine.remembering` | Remembering organ |
| `engine.activation` | Shared Cognitive Activation Engine |

### Reflection

| Method | Purpose |
|--------|---------|
| `what_do_i_think(cue)` | *What do I think about what I remember?* evaluation + Reflective Experience |
| `reflect_on(experience_id, text)` | Host-supplied Reflective Experience lineage helper |
| `engine.reflection` | Reflection organ |

### Reconciliation & Confidence (M15 / M16)

| Method | Purpose |
|--------|---------|
| `how_should_memory_reconcile(cue)` | *When memories disagree…* → ReconciliationRecord lineage |
| `how_certain_am_i(cue="", *, concept_id="")` | *How certain am I…* → ConfidenceSnapshots + uncertainty |
| `engine.reconciliation` | Reconciliation organ |
| `engine.confidence` | Confidence / Uncertainty organ |

### Identity

| Method | Purpose |
|--------|---------|
| `who_am_i()` | Reconstruct agent identity from schemas + goals + central concepts |
| `identity_snapshot()` | Full derived snapshot (schemas, lineage tail, evolution metrics) |
| `assent_identity(proposal_id)` | Apply a pending high-impact identity change |
| `reject_identity(proposal_id)` | Reject a pending change; prior attribute remains |
| `cancel_identity(proposal_id)` | B20 — cancel pending proposal without applying |
| `preview_identity_change` / `propose_identity_change` | B20 — preview / propose attribute change |
| `apply_identity_change` | B20 — trusted-host commit (`assent=True`) or propose |
| `preview_identity_correction` / `apply_identity_correction` | B20 — conversational correction UX |
| `pending_identity_changes()` | B20 — read-only pending proposal list |
| `present_relationship_memory(request)` | B21 — explicit relationship presentation (D044) |
| `preview_erase_request` / `propose_erase_request` | B36 — preview / propose forget·prune·erase |
| `assent_erase_request` / `reject_erase_request` / `cancel_erase_request` | B36 — gate resolution |
| `apply_erase_request` / `pending_erase_requests` | B36 — trusted-host commit / pending list |

See [`IDENTITY_CORRECTION.md`](IDENTITY_CORRECTION.md) · [`RELATIONSHIP_PRESENTATION.md`](RELATIONSHIP_PRESENTATION.md) · [`ERASE_GOVERNANCE.md`](ERASE_GOVERNANCE.md).

### Extensions

| Attribute / API | Purpose |
|-----------------|---------|
| `engine.extensions.register(ext)` | Attach a `BaseExtension` / `CognitiveExtension` |
| Hooks | `after_encode`, `after_remember`, `after_sleep`, `after_reconcile`, `after_assess`, … |

### Observability

| Attribute | Purpose |
|-----------|---------|
| `engine.validation` | `ValidationHarness` — milestone observables |
| `engine.trace` | `TraceLog` of `CognitiveTraceEvent` |
| `engine.validation.snapshot()` | JSON-safe report (`acm.validation/0.12`) including reconciliation + confidence |
| `engine.identity` | Identity organ (advanced; prefer public methods above) |

## Non-goals (public API)

- No Aria / Mission Control types
- No prompt logging
- No chain-of-thought fields
- No host policy enforcement (hosts may wrap ACM)
- No Planning / Decision Making / Executive Reasoning APIs
