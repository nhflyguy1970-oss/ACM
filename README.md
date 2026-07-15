# ACM — Aria Cognitive Memory

**Reusable cognitive memory engine for AI agents.**

ACM is **not** Aria. Aria (and any other agent) may become a *consumer* of ACM through external adapters. This repository has zero dependency on Aria, Mission Control, Capability Bus, or AI-Platform.

> Memory is not storage. Memory is cognition.

## Status

**v0.6.0 — M5 Remembering Organ + Cognitive Activation Architecture**

| Layer | State |
|-------|--------|
| Design constitution | Complete (`docs/MEMORY_DESIGN_PRINCIPLES.md`) |
| Architecture | Complete (`docs/ARCHITECTURE.md`) |
| Validation strategy | Complete (`docs/COGNITIVE_MEMORY_TEST_STRATEGY.md`) |
| Activation Architecture | Complete (`docs/COGNITIVE_ACTIVATION_ARCHITECTURE.md`) |
| Plugin / core boundaries | Complete |
| Experience / Concept / Association models | Complete |
| Remembering model | Complete (`docs/REMEMBERING_MODEL.md` + companions) |
| M0 Validation Harness | Implemented |
| M1 Identity | Implemented — *Who am I?* |
| M2 Experience | Implemented — *What happened?* |
| M3 Concept | Implemented — *What is this?* |
| M4 Association | Implemented — *How is this related?* |
| M5 Remembering | **Implemented** — *What do I remember?* |
| M6+ Reflection / Learning / … | Roadmapped — not started |
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
engine.encode("A husky is a dog.", pin=True)
print(engine.who_am_i()["answer"])
print(engine.what_happened())
print(engine.what_is_this("coffee"))
print(engine.how_related("husky", "dog"))
print(engine.what_do_i_remember("What is my favorite coffee?"))
result = engine.remember("What is my favorite coffee?")
print(result.answer, result.ambiguous)
report = engine.validation.snapshot()
print(report["remembering"])
```

No host framework required. See `examples/hello_acm.py`.

## Document map

| Document | Purpose |
|----------|---------|
| [VISION.md](VISION.md) | Why ACM exists |
| [ROADMAP.md](ROADMAP.md) | Cognitive milestones |
| [docs/MEMORY_DESIGN_PRINCIPLES.md](docs/MEMORY_DESIGN_PRINCIPLES.md) | Constitution (*why*) |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Architecture (*how*) |
| [docs/COGNITIVE_ACTIVATION_ARCHITECTURE.md](docs/COGNITIVE_ACTIVATION_ARCHITECTURE.md) | Shared activation model |
| [docs/REMEMBERING_MODEL.md](docs/REMEMBERING_MODEL.md) | Remembering organ |
| [docs/REMEMBERING_DESIGN_PRINCIPLES.md](docs/REMEMBERING_DESIGN_PRINCIPLES.md) | Reconstruction principles |
| [docs/SPREADING_ACTIVATION.md](docs/SPREADING_ACTIVATION.md) | Propagation mechanics |
| [docs/COGNITIVE_RECONSTRUCTION.md](docs/COGNITIVE_RECONSTRUCTION.md) | Why reconstruct |
| [docs/ASSOCIATION_MODEL.md](docs/ASSOCIATION_MODEL.md) | Living Associations |
| [docs/CONCEPT_ARCHITECTURE.md](docs/CONCEPT_ARCHITECTURE.md) | Concepts |
| [docs/API.md](docs/API.md) | Public API |
| [docs/DECISION_LOG.md](docs/DECISION_LOG.md) | Decisions |
| [CHANGELOG.md](CHANGELOG.md) | Releases |

## Non-negotiables

1. **Host-agnostic** — no Aria/MC/CapBus imports; adapters live *outside* this repo.  
2. **Cognition before storage** — databases are informative, never the design center.  
3. **Observable cognitive state** — no prompt dumps or chain-of-thought as “memory.”  
4. **Daily Use Mode** — measured regressions and Problem Reports drive work.  
5. **Assent for architecture change** — self-modification of cognitive policy requires explicit user authorization (future).
