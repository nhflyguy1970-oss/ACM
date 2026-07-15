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
| **M7** | Learning organ — *What have I learned?* | **Blocked until L0 accepted — not started** |
| **M7b** | Sleep consolidation (apply/propose Learning) | Planned |
| **M5b** | Goal Space organ polish | Planned (stubs / bias exist) |
| **M4b** | Working memory + Attention field polish | Planned (stubs exist) |
| **M8** | Forgetting as accessibility cooling | Planned |
| **M9** | Prediction | Planned (after Learning) |
| **M10** | Planning | Planned (after Prediction) |
| **M11** | Creativity / Analogical reasoning | Planned |
| **M12** | Safe Self-Improvement governance (assent UX) | Planned — never automatic |
| **M13** | Multimodal envelopes maturity | Planned |
| **M14** | Knowledge ≠ Memory adoption paths | Planned |
| **M15** | Observability / meta-memory sketch maturity | Partial |

> **Note:** Older roadmap labels (Context as “M6”, Reconsolidation as “M7”, freeze-chart Reflection as “M11”) referred to the design-freeze phase list in `ARCHITECTURE.md`. Implementation numbering above is authoritative for this repository. See [`ACM_ARCHITECTURE_REVIEW_M6.md`](docs/ACM_ARCHITECTURE_REVIEW_M6.md).

## Host integration

Wiring Aria (or any host) is **out of scope** until ACM demonstrates milestone maturity with independent tests and benchmarks. Adapters live outside this repository.

## Governance

Daily Use Mode: Problem Reports and measured regressions drive work. No speculative feature stacks. **L0 produces architecture only — no Learning code until M7 is explicitly authorized.**
