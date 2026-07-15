# Migration Guide — ACM Phase 2

**Status:** Engineering guide (design + tooling)  
**Companions:** [`ARIA_INTEGRATION_ARCHITECTURE.md`](ARIA_INTEGRATION_ARCHITECTURE.md) · [`ROLLBACK_STRATEGY.md`](ROLLBACK_STRATEGY.md)

## Current authorized step

**Shadow dual-write via `AcmMemoryAdapter`** with legacy authoritative. ACM encodes in parallel. No user-visible cutover.

## Steps (host-side later)

1. Install `aria-cognitive-memory` with `aria_memory_adapter`.  
2. Inject legacy backend implementing `remember`/`recall`/`health`.  
3. Enable `FeatureFlags(shadow_write=True, shadow_read=True)`.  
4. Monitor `shadow_report()` / MC metrics.  
5. Do **not** set `acm_read_primary` until certification + approval.

## Data import

Use `CognitiveEngine.export_snapshot` / `import_snapshot` for ACM↔ACM moves.  
Legacy harvest remains an Aria-side job (not executed here).
