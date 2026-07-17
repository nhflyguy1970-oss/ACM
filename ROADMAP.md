# Roadmap — ACM

Milestones are cognitive, not storage-tech. Each milestone requires the permanent ACM lifecycle through annotated tag, GitHub Release, and completion report before the next milestone.

| Milestone | Focus | Status |
|-----------|--------|--------|
| **Foundation** … **M16** | Core cognitive memory lifecycle | **Done (≤v0.12.0)** |
| **P1** | Integration Readiness (design) | **Done (v0.12.1)** |
| **P2** | Operational Readiness (P2.1–P2.5) | **Done (v0.13.0)** |
| **P2 Cert** | Operational Certification Execution | **Done (v0.14.0)** — **CERTIFIED WITH CONDITIONS** |
| **Aria Blueprint** | Full memory replacement design + ACM Supremacy Rules | **Done (design, v0.14.1 docs)** — Jarvis `docs/acm_integration/` |
| **Memory Authority** | LM never determines memory; Cognitive Response Pipeline | **Done (v0.15.0)** — D038; promote-to-Aria pending approval |
| **Cognitive Intent & Routing** | Classify cognitive ownership; route to owning organ | **Done (v0.16.0)** — D039; promote-to-Aria pending approval |
| **Cognitive Dispatch** | End-to-end organ termination; no infrastructure endpoints | **Done (v0.17.0)** — D040; promote-to-Aria pending approval |
| **Semantic Extraction** | NL → structured cognitive facts before organ storage | **Done (v0.18.0)** — D041; promote-to-Aria pending approval |
| **Identity Pipeline Debug** | Fix encode→retrieve confidence/pollution for user name | **Done (v0.18.1)** — D042; promote-to-Aria pending approval |
| **Assistant Identity Pipeline** | Separate operational assistant identity from user autobiography | **Done (v0.18.2)** — D043; promote-to-Aria pending approval |
| **Identity Rendering Isolation** | No cross-identity blend in Who am I / Who are you speech | **Done (v0.18.3)** — D044; promote-to-Aria pending approval |
| **Preference Reconstruction Fix** | Lexical support concepts never compete with semantic preferences | **Done (v0.18.4)** — D045; promote-to-Aria pending approval |
| **Future Enhancement Backlog** | Permanent post-D045 enhancement inventory and candidate ordering | **Captured (docs)** — 52 items; no implementation authorized |
| **Next (approval)** | Promote certified ACM into Aria vendored copy (as approved) | **Awaiting approval** |
| **Later** | Unqualified ACM 1.0 label | Evidence-driven |
| **Later** | Planning / Decision / Creativity | Deferred |

> **Certification:** [`docs/ACM_CERTIFIED_v1.md`](docs/ACM_CERTIFIED_v1.md)  
> **Memory Authority:** [`docs/MEMORY_AUTHORITY_MODEL.md`](docs/MEMORY_AUTHORITY_MODEL.md)  
> **Cognitive Intent:** [`docs/COGNITIVE_INTENT_CLASSIFICATION.md`](docs/COGNITIVE_INTENT_CLASSIFICATION.md)  
> **Cognitive Dispatch:** [`docs/COGNITIVE_DISPATCH_ENGINE.md`](docs/COGNITIVE_DISPATCH_ENGINE.md)  
> **Semantic Extraction:** [`docs/SEMANTIC_EXTRACTION.md`](docs/SEMANTIC_EXTRACTION.md)  
> **Future roadmap:** [`docs/FUTURE_ENHANCEMENTS_ROADMAP.md`](docs/FUTURE_ENHANCEMENTS_ROADMAP.md) · [`docs/ENGINEERING_BACKLOG.md`](docs/ENGINEERING_BACKLOG.md) · [`docs/FUTURE_RELEASE_CANDIDATES.md`](docs/FUTURE_RELEASE_CANDIDATES.md)
> **Integration policy:** D036 · D037 · **D038** · **D039** · **D040** · **D041** · **D042** · **D043** · **D044** · **D045**.
> Standalone ACM stays research/reference — **not** Aria’s runtime shared library. Cognition improvements: implement here → certify → **explicit promotion**.

## Host integration

- Production path: **vendored ACM copy inside Aria** with thin façades (D036).  
- Hosts handling memory questions **must** call `cognitive_respond` (or equivalent) **before** language-model generation (D038).  
- Blueprint location (Aria/Jarvis): `/media/jeff/AI/jarvis/docs/acm_integration/`.

## Governance

Daily Use Mode. Future cognition is evidence-driven only. Supremacy Rules forbid reimplementing ACM organs in Aria or regressing cognition out of ACM without re-certification.
