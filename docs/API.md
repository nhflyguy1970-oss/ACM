# API — ACM v0.1

Public surface is intentionally small. Hosts integrate through `CognitiveEngine`; adapters and storage backends may evolve underneath without expanding the verb set casually.

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

#### `encode(text, *, kind="experience", pin=False, context_tags=None) -> dict`

Encodes an experience into lasting structure when attention / kind warrants durability.

Typical `kind` values: `experience`, `preference`, `identity`.

Returns at least: `encoded`, and on success `experience_id`, `concept_id`, `attention`, `importance`.

#### `remember(query) -> RememberResult`

Retrieves and lightly reconsolidates. Fields:

| Field | Meaning |
|-------|---------|
| `answer` | User-facing recollection text |
| `explanation` | Template-class explanation only (no CoT) |
| `explanation_class` | Enum class (`preference`, `experience`, …) |
| `activated_concept_ids` | What activated |
| `confidence` | Recalled confidence |
| `trace` | Public cognitive-state metadata |

#### `sleep(*, apply_low_impact=True) -> dict`

Consolidation pass: prune weak edges (optional); record merge *proposals* without auto-applying high-impact structure changes.

#### `metacognitive_sketch() -> dict`

Foundations for self-modeling: counts of known / uncertain concepts, experiences, goals, identity labels, encode/remember counts, buffer occupancy, context. **Not** consciousness.

### Observability

| Attribute | Purpose |
|-----------|---------|
| `engine.validation` | `ValidationHarness` — milestone observables |
| `engine.trace` | `TraceLog` of `CognitiveTraceEvent` |
| `engine.validation.snapshot()` | JSON-safe cognitive validation report |

## Non-goals (public API)

- No Aria / Mission Control types
- No prompt logging
- No chain-of-thought fields
- No host policy enforcement (hosts may wrap ACM)
