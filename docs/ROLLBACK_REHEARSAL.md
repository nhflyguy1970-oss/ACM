# Rollback Rehearsal

**Executed:** 2026-07-15

## Persistence rollback

1. Encode baseline → flush → backup.  
2. Encode additional candidate → flush.  
3. Restore backup.  

| Check | Result |
|-------|--------|
| Baseline experiences preserved | **PASS** |
| Orphan experience refs in provenance | **0** |
| Corruption indicators | None |
| Rollback wall time | ≈ included in section (~ms scale) |

## Adapter rollback flag

`FeatureFlags(rollback_to_legacy=True)`:

| Check | Result |
|-------|--------|
| Authoritative remains legacy | **PASS** |
| ACM shadow suppressed | **PASS** (`acm_shadow is None`) |

## Category result

**PASS**
