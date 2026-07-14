# ACM — Aria Cognitive Memory

**Reusable cognitive memory engine for AI agents.**

ACM is **not** Aria. Aria (and any other agent) may become a *consumer* of ACM through external adapters. This repository has zero dependency on Aria, Mission Control, Capability Bus, or AI-Platform.

> Memory is not storage. Memory is cognition.

## Status

**v0.1.0 — Foundation Build / M0 Validation Harness**

| Layer | State |
|-------|--------|
| Design constitution | Complete (`docs/MEMORY_DESIGN_PRINCIPLES.md`) |
| Architecture | Complete (`docs/ARCHITECTURE.md`) |
| Validation strategy | Complete (`docs/COGNITIVE_MEMORY_TEST_STRATEGY.md`) |
| M0 Validation Harness | Implemented (in-repo) |
| M1+ Identity / Concepts / … | Roadmapped — not yet implemented |
| Host migration (Aria, etc.) | **Not started** — ACM must mature first |

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## 60-second integration

```python
from acm import CognitiveEngine

engine = CognitiveEngine(agent_id="demo-agent")
engine.encode("My favorite coffee is dark roast.", kind="preference")
result = engine.remember("What is my favorite coffee?")
print(result.answer)
print(result.explanation)  # template class only — no chain-of-thought
report = engine.validation.snapshot()
print(report["activations"][-1])
```

No host framework required. See `examples/hello_acm.py`.

## Document map

| Document | Purpose |
|----------|---------|
| [VISION.md](VISION.md) | Why ACM exists |
| [ROADMAP.md](ROADMAP.md) | Cognitive milestones M0–M15 |
| [docs/MEMORY_DESIGN_PRINCIPLES.md](docs/MEMORY_DESIGN_PRINCIPLES.md) | Constitution (*why*) |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Architecture (*how*) |
| [docs/COGNITIVE_MEMORY_TEST_STRATEGY.md](docs/COGNITIVE_MEMORY_TEST_STRATEGY.md) | Validation (*proof*) |
| [docs/API.md](docs/API.md) | Public API |
| [docs/DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md) | Develop here |
| [docs/OBSERVABILITY.md](docs/OBSERVABILITY.md) | Cognitive state visibility |
| [docs/DECISION_LOG.md](docs/DECISION_LOG.md) | Significant decisions |
| [CHANGELOG.md](CHANGELOG.md) | Releases |

## Non-negotiables

1. **Host-agnostic** — no Aria/MC/CapBus imports; adapters live *outside* this repo.  
2. **Cognition first** — every change must move toward practical human-like memory.  
3. **Emergence over scripts** — identity, patterns, confidence grow from interacting systems.  
4. **Plug-and-play** — minimal deps, clean API, installable by any agent.

## Governance

**Daily Use Mode** remains in force: Problem Reports → measure → minimal change → regressions → observables. No speculative features.

## License

Apache-2.0 — see [LICENSE](LICENSE).
