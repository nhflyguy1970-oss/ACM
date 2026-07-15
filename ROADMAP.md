# Roadmap — ACM

Milestones are cognitive, not storage-tech. Each milestone requires: design → architecture review → implementation → behavioral + cognitive + regression + performance tests → documentation → commit → push → CI → annotated tag → GitHub Release → completion report → approval before next.

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
| **M9** | Attention & Memory Priority — *What deserves cognitive attention and continued memory investment?* | **Done (v0.9.0)** |
| **M10** | Memory Accessibility & Forgetting — *What should become harder to remember?* | **Done (v0.9.0)** |
| **M5b** | Goal Space organ polish | Planned (stubs / bias exist) |
| **M4b** | Working memory polish | Planned (buffer exists; Attention organ supersedes field-only M4b attention) |
| **M11** | Prediction | Planned |
| **M12** | Planning | Planned (after Prediction) |
| **M13** | Creativity / Analogical reasoning | Planned |
| **M14** | Safe Self-Improvement governance (assent UX) | Planned — never automatic |
| **M15** | Multimodal envelopes maturity | Planned |
| **M16** | Knowledge ≠ Memory adoption paths | Planned |
| **M17** | Observability / meta-memory sketch maturity | Partial |

> **Note:** Implementation numbering above is authoritative. Attention landed as **M9** and Forgetting as **M10** per adaptive-memory mandate (Prediction deferred).

## Adaptive cycle (complete through v0.9.0)

```
Encode (Attention) → Experience → Remembering ↔ Accessibility
  → Reflection → Learning → Offline Cognition (priority-ranked replay)
  → Forgetting cools neglected paths → Reactivation via strong cues
```

## Host integration

Wiring Aria (or any host) remains **out of scope**.

## Governance

Daily Use Mode. Architectural self-improvement remains user-governed.
