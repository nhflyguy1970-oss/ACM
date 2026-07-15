# Migration Rehearsal

**Executed:** 2026-07-15  
**Scope:** ACM → ACM snapshot migration rehearsal only. **Aria not migrated.**

## Procedure

1. Source engine with durable SQLite; encode 15 experiences.  
2. Export versioned snapshot JSON (checksummed).  
3. Destination engine imports snapshot and flushes.  

## Measurements

| Metric | Value |
|--------|------:|
| Migration wall time | ≈40.3 ms |
| Experiences exported | 15 |
| Experiences imported | 15 |
| Provenance exported | 30 |
| Provenance imported | 30 |
| Completeness | **True** |
| Aria migrated | **False** |

## Rollback point

Source DB + export JSON retained as rehearsal rollback points (see Rollback Rehearsal).

## Category result

**PASS**
