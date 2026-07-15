# Daily Use Validation — ACM Phase 2

**Status:** Framework support (not executed certification)

## Intent

Daily Use validation proves ACM does not disturb host behavior while Shadow runs.

## Checks (automated smoke)

- Legacy authoritative on remember/recall  
- `user_visible_changed=false`  
- Shadow metrics accumulate  
- Provenance stamped without fabrication  
- Persistence survives restart  

## Out of scope here

Live Aria fleets · user A/B · Mission Control redesign.
