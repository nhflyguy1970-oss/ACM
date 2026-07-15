# Aria Memory Adapter

**Status:** Canonical for Phase 2 (P2.3)  
**Package:** `aria_memory_adapter` (separate from `acm` and from Aria)

## Separation

| Package | May import |
|---------|------------|
| `acm` | — (no Aria, no adapter) |
| `aria_memory_adapter` | `acm` only |
| Aria application | adapter + acm (future — **not in this phase**) |

## Responsibilities

Public memory interface · legacy API translation · feature flags · rollback hooks · error isolation · metrics · health · capability discovery · Shadow Mode orchestration

## Public API

```python
from aria_memory_adapter import AcmMemoryAdapter, FeatureFlags

adapter = AcmMemoryAdapter(legacy=host_legacy_backend, flags=FeatureFlags())
adapter.remember("...")   # legacy authoritative
adapter.recall("...")     # legacy authoritative + ACM shadow compare
adapter.health()
adapter.capabilities()
adapter.shadow_report()
adapter.mission_control_metrics()  # engineering visibility only
```

## Feature flags

`shadow_write` · `shadow_read` · `acm_read_primary` (reserved; false in P2) · `acm_writes_only` · `rollback_to_legacy`

## Non-goals (this phase)

No Aria repo modifications · no Cap Bus cutover · no UI · no certification execution.
