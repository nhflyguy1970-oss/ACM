# Plugin Architecture — ACM

**Status:** Architectural (M1)  
**Companions:** [`CORE_BOUNDARIES.md`](CORE_BOUNDARIES.md) · [`ARCHITECTURE.md`](ARCHITECTURE.md) · [`MEMORY_DESIGN_PRINCIPLES.md`](MEMORY_DESIGN_PRINCIPLES.md)

ACM is an extensible **cognitive platform**. The cognitive core stays small and stable. Future capabilities attach without rewriting `CognitiveEngine` verbs.

> Cognition is owned by the core. Extensions contribute experiences, concepts, envelopes, or cognitive *services*. They do not own remembering.

## 1. Core responsibilities

The core owns:

| Organ | Responsibility |
|-------|----------------|
| Experiences | Encode lived events |
| Concepts / Associations | Structure and neighborhoods |
| Identity | Privileged schemas; emergence + lineage |
| Goals | Future-directed bias |
| Attention / Context | Encoding and recall gating |
| Working buffer | Capacity-limited focus |
| Remember / Reconsolidate | Cue → activation → write |
| Sleep | Consolidation proposals / low-impact apply |
| Validation / Trace | Observable cognitive state |
| Extension registry | Attachment lifecycle |

Public cognitive verbs (`encode`, `remember`, `sleep`, …) remain stable across extensions.

## 2. Extension responsibilities

Extensions may:

- Contribute multimodal envelopes and linked experiences
- Propose concepts / associations (core decides durability via Attention + policy)
- Offer **cognitive services** (e.g., vision feature extraction → envelope + tags)
- Observe cognitive events for host dashboards (read-only hooks)

Extensions must **not**:

- Replace Identity / Remember / Sleep with host-specific logic
- Import Aria, Mission Control, AI-Platform, Capability Bus, or Conversation Trace
- Bypass Policy Gate for identity / erase / high-impact sleep
- Emit chain-of-thought as “memory”

## 3. Extension lifecycle

```
discover → register → on_register → (encode|remember|sleep hooks) → unregister
```

1. **Register** with name + semver compatible with core API major.
2. **`on_register(engine)`** — bind resources; may open no durable identity content by itself.
3. **Event hooks** (optional): `after_encode`, `after_remember`, `after_sleep`.
4. **Unregister** — detach hooks; leave store state intact (cognition persists).

M1 ships a minimal in-process registry. Discovery loaders (entry points) may arrive later without changing contracts.

## 4. Registration (M1)

```python
from acm import CognitiveEngine
from acm.plugins import CognitiveExtension

class MySense(CognitiveExtension):
    name = "example.sense"
    version = "0.1.0"

    def on_register(self, engine):
        ...

engine = CognitiveEngine(agent_id="demo")
engine.extensions.register(MySense())
```

Registration fails if `name` collides or major version is incompatible with `acm.__version__` major.

## 5. Version compatibility

| Rule | Meaning |
|------|---------|
| Core major | Extensions declare support for core major `N` |
| Backward | Minor/patch core bumps should not break hooks |
| Breaking | New required hook or verb semantics → core major bump |

Identity and other organs are **not** plugins; their versions track the ACM package.

## 6. Cognitive contracts

Extensions that write into cognition must honor:

1. **Experience-first** — structure grows from lived/adopted events (P3 / P10).
2. **Knowledge ≠ Memory** — corpora stay outside until explicit adoption (P7).
3. **Attention gates durability** — dumps are not automatic permanence.
4. **Reconsolidation / lineage** — substantive updates version; they do not silent-overwrite.
5. **Identity privilege** — identity-central writes go through Policy Gate when high-impact.
6. **Observability** — state changes record in Validation Harness / Trace (no CoT).

## 7. Future extension examples

| Extension | Contributes |
|-----------|-------------|
| Vision | Image envelopes + perceptual tags → concepts |
| Audio / voice | Utterance envelopes; prosody as attention cue |
| Robotics / spatial | Pose, maps, affordance experiences |
| Web memory | Adoption pipeline (explicit) for knowledge→memory |
| Scientific reasoning | Hypothesis buffer services; does not own Identity |
| Planning | Goal structuring helpers; Goals organ remains core |
| Embodiment | Sensor envelopes; sleep rehearsal of motor traces |

## 8. Non-goals

- Plugin marketplaces, sandboxed WASM runtimes, or heavy DI frameworks
- Host GUIs inside ACM
- LLM orchestration as a core organ

Keep the extension system minimal. Prefer hooks + registry over frameworks.
