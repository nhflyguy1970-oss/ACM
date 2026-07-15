# Roadmap — ACM

Milestones are cognitive, not storage-tech. Each milestone requires: design review → implementation → behavioral + regression tests → benchmarks (where relevant) → documentation → git commit → CI green → then proceed.

| Milestone | Focus | Status |
|-----------|--------|--------|
| **Foundation** | Standalone repo, docs suite, public API scaffold, independence rules | **Done (v0.1.0)** |
| **M0** | Validation Harness + cognitive observables + CI | **Done** |
| **M1** | Identity — *Who am I?* | **Done (v0.2.0)** |
| **M2** | Experience — *What happened?* | **Done (v0.3.0)** |
| **M3** | Concept — *What is this?* | **Done (v0.4.0)** |
| **M4** | Association — *How is this related?* | **Done (v0.5.0)** |
| **M5** | Remembering — *What do I remember?* (+ Activation Architecture) | **Done (v0.6.0)** |
| **M6** | Reflection — *What do I think about what I remember?* | **Done (v0.7.0)** |
| **L0** | Learning research & architecture (**design only**) | **Done (v0.7.1)** |
| **M7** | Learning organ — *What have I learned?* | **Done (v0.8.0)** |
| **M8** | Offline Cognition (Sleep & Consolidation) — *What should become long-term memory?* | **Done (v0.8.0)** |
| **M5b** | Goal Space organ polish | Planned (stubs / bias exist) |
| **M4b** | Working memory + Attention field polish | Planned (stubs exist) |
| **M9** | Forgetting as accessibility cooling | Planned (depends on Learning + Offline) |
| **M10** | Prediction | Planned (after Learning) |
| **M11** | Planning | Planned (after Prediction) |
| **M12** | Creativity / Analogical reasoning | Planned |
| **M13** | Safe Self-Improvement governance (assent UX) | Planned — never automatic |
| **M14** | Multimodal envelopes maturity | Planned |
| **M15** | Knowledge ≠ Memory adoption paths | Planned |
| **M16** | Observability / meta-memory sketch maturity | Partial |

> **Note:** Implementation numbering above is authoritative. Older freeze-chart labels in `ARCHITECTURE.md` (e.g. Reconsolidation as “M7”) are historical. Offline Cognition landed as **M8** per adaptive-cycle mandate; Forgetting follows as **M9**. See [`ONLINE_OFFLINE_MEMORY.md`](docs/ONLINE_OFFLINE_MEMORY.md).

## Adaptive cycle (complete at v0.8.0)

```
Experience → Remembering → Reflection → Learning → Offline Cognition → Improved Memory
```

Learning depends on Reflection (Reflective Experiences as auditable evaluation). Offline Cognition depends on Learning (replay applies/proposes Adaptation Records). Future Forgetting will cool accessibility using both organs’ schedules — without rewriting history.

## Host integration

Wiring Aria (or any host) is **out of scope** until ACM demonstrates milestone maturity with independent tests and benchmarks. Adapters live outside this repository.

## Governance

Daily Use Mode: Problem Reports and measured regressions drive work. No speculative feature stacks. Architectural self-improvement remains user-governed — Offline Cognition reorganizes memory only.
