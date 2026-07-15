# Rollback Strategy — ACM Phase 2

## Shadow phase rollback

Set `FeatureFlags.rollback_to_legacy=True` or disable shadow flags. User path remains legacy.

## Persistence rollback

1. Stop ACM writes.  
2. `DurableCognitiveStore.restore(backup_path)`.  
3. Verify checksum / integrity.  
4. Resume.

## Non-negotiable

Never delete Legacy while Shadow is active. Never auto-merge competing ACM/Legacy truths into user-visible answers during P2.
