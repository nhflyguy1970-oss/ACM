# ACM — Aria Cognitive Memory

**Reusable cognitive memory engine for AI agents.**

ACM is **not** Aria. Aria (and any other agent) may become a *consumer* of ACM through external adapters. This repository has zero dependency on Aria, Mission Control, Capability Bus, or AI-Platform.

> Memory is not storage. Memory is cognition.

## Status

**v0.7.1 — L0 Learning Research & Architecture (design only)**

Implemented organs: M1–M6. **Learning organ is not implemented.** L0 documents define canonical Learning design, governance, and research foundations for future M7.

| Layer | State |
|-------|--------|
| M1–M6 organs | Implemented (through Reflection) |
| Cognitive Capability Map | Complete |
| Cognitive Research Foundations | Complete (permanent ledger) |
| L0 Learning design package | **Complete — no code** |
| M7 Learning organ | **Not started / not authorized** |
| Host migration (Aria, etc.) | **Not started** |

## Design canon (L0)

| Document | Purpose |
|----------|---------|
| [docs/LEARNING_ARCHITECTURE.md](docs/LEARNING_ARCHITECTURE.md) | Future Learning organ architecture |
| [docs/LEARNING_RESEARCH_FOUNDATIONS.md](docs/LEARNING_RESEARCH_FOUNDATIONS.md) | Graded scientific foundations |
| [docs/COGNITIVE_RESEARCH_FOUNDATIONS.md](docs/COGNITIVE_RESEARCH_FOUNDATIONS.md) | Per-organ research ledger |
| [docs/LEARNING_GOVERNANCE.md](docs/LEARNING_GOVERNANCE.md) | Automatic vs assent boundaries |
| [docs/LEARNING_LIFECYCLE.md](docs/LEARNING_LIFECYCLE.md) | Adaptation lifecycle |
| [docs/ACM_ARCHITECTURE_REVIEW_M6.md](docs/ACM_ARCHITECTURE_REVIEW_M6.md) | Post-M6 architecture & roadmap review |

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Non-negotiables

1. **Host-agnostic**  
2. **Cognition before storage**  
3. **Observable cognitive state** — no prompt/CoT dumps  
4. **Daily Use Mode**  
5. **Assent for architecture change** — Learning ≠ self-improvement  
