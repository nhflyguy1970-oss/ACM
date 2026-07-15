# Memory Priority — ACM

**Status:** Canonical for M9 (implemented)  
**Companions:** [`ATTENTION_MODEL.md`](ATTENTION_MODEL.md) · [`MEMORY_PRIORITY_LIFECYCLE.md`](MEMORY_PRIORITY_LIFECYCLE.md)

## Definition

Memory Priority is the living investment score on cognitive structures (primarily Concepts). It answers where long-term cognitive investment should continue.

Priority influences:

- Encoding durability (via Attention allocation)
- Remembering reconstruction bias
- Reflection / Learning urgency bias
- Offline replay selection
- Accessibility protection (high priority cools slower)

## Evolution

Priority evolves continuously via observable investment events:

- Successful remembering / reflection / learning → invest
- Neglect / low activation → slight disinvestment (Attention records; Forgetting cools accessibility separately)
- Goals and identity adjacency → temporary boost while goals open

Never a static priority bit stamped at birth (P14).

## Observability

Every investment records before/after priority, source organ, and factor tags. No chain-of-thought.
