# Shadow Mode — ACM

**Status:** Canonical for Phase 2 (P2.4)

## Rule

Shadow Mode **never** changes Aria/user-visible memory behavior.  
**Legacy remains authoritative.**

## Behavior

1. Legacy serves the answer.  
2. ACM answers in parallel (encode/remember).  
3. Compare answer overlap, confidence, latency.  
4. Record agreement / disagreement metrics.  
5. `user_visible_changed=false` always in P2.

## Compared dimensions

Recall · confidence · latency · (optional hooks for prediction/reconciliation later) · provenance counts · agreement/disagreement

## Mission Control / Trace

Engineering metrics only (`mission_control_metrics`, `trace` block). No UI redesign.
