# ACM — Aria Cognitive Memory

**Reusable cognitive memory engine for AI agents.**

ACM is **not** Aria. Aria (and any other agent) may become a *consumer* of ACM through external adapters. This repository has zero dependency on Aria, Mission Control, Capability Bus, or AI-Platform.

> Memory is not storage. Memory is cognition.

## Status

**v0.4.0 — M3 Concept Organ**

| Layer | State |
|-------|--------|
| Design constitution | Complete (`docs/MEMORY_DESIGN_PRINCIPLES.md`) |
| Architecture | Complete (`docs/ARCHITECTURE.md`) |
| Validation strategy | Complete (`docs/COGNITIVE_MEMORY_TEST_STRATEGY.md`) |
| Plugin / core boundaries | Complete (`docs/PLUGIN_ARCHITECTURE.md`, `CORE_BOUNDARIES.md`) |
| Experience model / timeline | Complete (`docs/EXPERIENCE_MODEL.md`, `COGNITIVE_TIMELINE.md`) |
| Concept architecture | Complete (`docs/CONCEPT_ARCHITECTURE.md`, abstraction + lifecycle) |
| M0 Validation Harness | Implemented |
| M1 Identity | Implemented — *Who am I?* |
| M2 Experience | Implemented — *What happened?* |
| M3 Concept | **Implemented** — *What is this?* |
| M4+ Associations / … | Roadmapped — not started |
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
engine.encode("I am a research assistant.", kind="identity")
engine.encode("My favorite coffee is dark roast.", kind="preference")
print(engine.who_am_i()["answer"])
print(engine.what_happened())
print(engine.what_is_this("coffee"))
result = engine.remember("What is my favorite coffee?")
print(result.answer)
report = engine.validation.snapshot()
print(report["concept"])
```

No host framework required. See `examples/hello_acm.py`.

## Document map

| Document | Purpose |
|----------|---------|
| [VISION.md](VISION.md) | Why ACM exists |
| [ROADMAP.md](ROADMAP.md) | Cognitive milestones M0–M15 |
| [docs/MEMORY_DESIGN_PRINCIPLES.md](docs/MEMORY_DESIGN_PRINCIPLES.md) | Constitution (*why*) |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Architecture (*how*) — design freeze also known as Aria Cognitive Memory |
| [docs/COGNITIVE_MEMORY_TEST_STRATEGY.md](docs/COGNITIVE_MEMORY_TEST_STRATEGY.md) | Validation (*proof*) |
| [docs/EXPERIENCE_MODEL.md](docs/EXPERIENCE_MODEL.md) | What an Experience is |
| [docs/COGNITIVE_TIMELINE.md](docs/COGNITIVE_TIMELINE.md) | Time as cognitive organizer |
| [docs/CONCEPT_ARCHITECTURE.md](docs/CONCEPT_ARCHITECTURE.md) | Concept emergence & meaning |
| [docs/COGNITIVE_ABSTRACTION.md](docs/COGNITIVE_ABSTRACTION.md) | Hierarchy / prototypes |
| [docs/CONCEPT_LIFECYCLE.md](docs/CONCEPT_LIFECYCLE.md) | Nucleus → mature → dormancy |
| [docs/PLUGIN_ARCHITECTURE.md](docs/PLUGIN_ARCHITECTURE.md) | Extension points |
| [docs/CORE_BOUNDARIES.md](docs/CORE_BOUNDARIES.md) | What stays in/out of ACM |
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
