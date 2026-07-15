# Spreading Activation — ACM

**Status:** Canonical mechanics for M5 (implements the Activation Architecture)  
**Companions:** [`COGNITIVE_ACTIVATION_ARCHITECTURE.md`](COGNITIVE_ACTIVATION_ARCHITECTURE.md) · [`ASSOCIATION_MODEL.md`](ASSOCIATION_MODEL.md) · [`REMEMBERING_MODEL.md`](REMEMBERING_MODEL.md)

## Activation

An **activation** is a transient cognitive energy attached to a Concept (or, secondarily, to participating Experience evidence). It is not a database hit and not a vector score masquerading as cognition.

## Propagation

From activated Concepts, energy flows along Associations using **directional** strength (`strength_forward` / `strength_backward` toward the neighbor). Propagation prefers active, non-retired Associations with sufficient distance band (immediate / near / far).

## Decay

Each hop multiplies remaining energy by a decay factor (default ≈ 0.55–0.7, tunable later under assent for architecture changes). Energy below a floor is dropped.

## Thresholds

| Gate | Role |
|------|------|
| Seed threshold | Cue must excite Concept enough to enter the field |
| Spread threshold | Neighbor must receive enough residual energy |
| Reconstruct threshold | Energy needed to join a recollection |
| Compete threshold | Ratio/distance between top candidates → ambiguity |

## Neighborhood traversal

Bounded breadth (hop limit, fan-out cap) preserves Working Memory realism. Traversal records path steps for observability (types + ids — not chain-of-thought).

## Association influence

Stronger / more confident Associations transmit more. Asymmetry matters: Dog → Animal may activate Animal more than the reverse activates Dog.

## Concept influence

Mature, high-strength, high-confidence Concepts seed and hold activation better. Identity Concepts receive Identity organ bias.

## Future optimization

Caching of hot neighborhoods, parallel wavefronts, and learned decay schedules may arrive via Learning — **architecture/policy changes remain assent-gated**.
