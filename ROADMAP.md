# Roadmap — ACM

Milestones are cognitive, not storage-tech. Each milestone requires: design review → implementation → behavioral + regression tests → benchmarks (where relevant) → documentation → git commit → CI green → then proceed.

| Milestone | Focus | Status |
|-----------|--------|--------|
| **Foundation** | Standalone repo, docs suite, public API scaffold, independence rules | **Done (v0.1.0)** |
| **M0** | Validation Harness + cognitive observables + CI | **Done (minimal stubs)** |
| **M1** | Identity schemas — *Who am I?* | **Done (v0.2.0)** |
| **M2** | Experience organ — *What happened?* | **Done (v0.3.0)** |
| **M3** | Concept organ — *What is this?* | **Done (v0.4.0)** |
| **M4** | Association organ — *How is this related?* | **Done (v0.5.0)** |
| **M5** | Remembering organ — *What do I remember?* (+ shared Activation Architecture) | **Done (v0.6.0)** |
| **M5b** | Goal Space bias refinement on encode/remember | Planned (M0 stubs exist; goals already bias activation) |
| **M4b** | Working memory interference + attention field | Planned (M0 stubs exist) |
| **M6** | Context frames & contextual recall | Planned (M0 stubs exist) |
| **M7** | Reconsolidation (supersede / contest / strengthen) | Partial stub |
| **M8** | Sleep consolidation (proposals + low-impact apply) | Partial stub |
| **M9** | Multimodal envelopes (non-text first-class) | Planned |
| **M10** | Knowledge ≠ Memory boundary + policy gate hooks | Planned |
| **M11** | Lifelong strengthening / weakening / forgetting curves | Planned |
| **M12** | Prediction & reflection loops | Planned |
| **M13** | Abstraction / generalization | Planned |
| **M14** | Observability completeness (cognitive state dashboard exports) | Planned |
| **M15** | Meta-memory self-sketch maturity | Sketch only |

## Host integration

Wiring Aria (or any host) is **out of scope** until ACM demonstrates milestone maturity with independent tests and benchmarks. Adapters live outside this repository.

## Governance

Daily Use Mode: Problem Reports and measured regressions drive work. No speculative feature stacks.
