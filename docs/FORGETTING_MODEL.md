# Forgetting Model — ACM

**Status:** Canonical for M10 (implemented)  
**Cognitive question:** *What should become harder to remember?*  
**Companions:** [`MEMORY_ACCESSIBILITY.md`](MEMORY_ACCESSIBILITY.md) · [`ONLINE_OFFLINE_MEMORY.md`](ONLINE_OFFLINE_MEMORY.md)

## Definition

Forgetting owns **accessibility policy**. It never owns deletion of Experiences or silent history rewrite (P17).

## Owns

- Accessibility stage evolution
- Dormancy / cool schedules
- Activation threshold effects (via accessibility multipliers into Activation)
- Recovery / reactivation
- Proposals for prune-eligibility (never auto hard-erase)

## Does not own

- Experience content mutation
- Architectural self-modification
- Planning which goals to pursue
- Concept meaning / Association relation kinds (may cool strength/accessibility only)

## Offline Cognition

Offline may **request** cools during consolidation. Forgetting **applies** accessibility policy. Ownership does not merge.

## Scientific notes

| Claim | Grade |
|-------|-------|
| Retrieval failure often accessibility, not erasure | Well-supported |
| Cue/context restores dormant traces | Well-supported |
| Sleep-related reorganization affects accessibility | Emerging → implemented as functional cool |
| Default physical DELETE as forget | Rejected |
