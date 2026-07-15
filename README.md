# ACM — Aria Cognitive Memory

**Reusable cognitive memory engine for AI agents.**

ACM is **not** Aria. Aria (and any other agent) may become a *consumer* of ACM through external adapters. This repository has zero dependency on Aria, Mission Control, Capability Bus, or AI-Platform.

> Memory is not storage. Memory is cognition.

## Status

**v0.7.0 — M6 Reflection Organ + Cognitive Capability Map**

| Layer | State |
|-------|--------|
| Design constitution | Complete |
| Architecture + Capability Map | Complete (`docs/COGNITIVE_CAPABILITY_MAP.md`) |
| Activation Architecture | Complete |
| M1 Identity | *Who am I?* |
| M2 Experience | *What happened?* |
| M3 Concept | *What is this?* |
| M4 Association | *How is this related?* |
| M5 Remembering | *What do I remember?* |
| M6 Reflection | **Implemented** — *What do I think about what I remember?* |
| M7+ Learning / Prediction / … | Roadmapped — not started |
| Host migration (Aria, etc.) | **Not started** |

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
print(engine.what_do_i_remember("What is my favorite coffee?"))
print(engine.what_do_i_think("What is my favorite coffee?"))
report = engine.validation.snapshot()
print(report["reflection"])
```

See `examples/hello_acm.py`.

## Document map

| Document | Purpose |
|----------|---------|
| [docs/COGNITIVE_CAPABILITY_MAP.md](docs/COGNITIVE_CAPABILITY_MAP.md) | Master organ capability map |
| [docs/REFLECTION_MODEL.md](docs/REFLECTION_MODEL.md) | Reflection organ |
| [docs/METACOGNITION_FOUNDATIONS.md](docs/METACOGNITION_FOUNDATIONS.md) | Metacognition foundations |
| [docs/REFLECTIVE_EXPERIENCES.md](docs/REFLECTIVE_EXPERIENCES.md) | Reflective Experience lineage |
| [docs/REMEMBERING_MODEL.md](docs/REMEMBERING_MODEL.md) | Remembering |
| [docs/COGNITIVE_ACTIVATION_ARCHITECTURE.md](docs/COGNITIVE_ACTIVATION_ARCHITECTURE.md) | Shared activation |
| [docs/API.md](docs/API.md) | Public API |
| [CHANGELOG.md](CHANGELOG.md) | Releases |

## Non-negotiables

1. **Host-agnostic** — no Aria/MC/CapBus imports.  
2. **Cognition before storage.**  
3. **Observable cognitive state** — no prompt/CoT dumps.  
4. **Daily Use Mode.**  
5. **Assent for architecture change.**
