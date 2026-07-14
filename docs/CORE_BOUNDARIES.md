# Core Boundaries — ACM

**Status:** Governance (M1)  
**Purpose:** Keep ACM a reusable cognitive engine — not a host monolith.  
**Companions:** [`PLUGIN_ARCHITECTURE.md`](PLUGIN_ARCHITECTURE.md) · [`ARCHITECTURE.md`](ARCHITECTURE.md)

## What MUST remain inside ACM

These are cognitive organs or irreducible platform mechanics:

| Inside | Why |
|--------|-----|
| Identity schemas | Privileged self/user/project continuity (P10) |
| Experiences | Immutable cognitive events (*What happened?*) |
| Concepts & attributes | Emergent meaning (*What is this?*) |
| Associations | Relational understanding |
| Remembering | Cue-driven activation + reconsolidation |
| Attention & context | Meaning and durability gates |
| Working memory | Capacity-limited focus / interference |
| Goal Space | Future-directed bias |
| Sleep / consolidation | Offline reorganization |
| Policy Gate (thin) | Assent for high-impact identity/erase/sleep |
| Validation harness & cognitive traces | Observable cognitive state |
| Extension registry | Attach future senses without redesign |
| Multimodal *envelope refs* | Modality-agnostic links (bytes may live outside) |

## What MUST remain outside ACM

| Outside | Why |
|---------|-----|
| GUIs / Mission Control panels | Presentation is host concern |
| LLMs / prompt stacks | Generation is not cognition ownership |
| Speech I/O, TTS, ASR pipelines | Sensors/effectors; feed envelopes in |
| Robotics middleware | Embodiment adapters |
| AI-Platform / Capability Bus | Host infrastructure |
| Conversation Trace products | Host diagnostics productization |
| Aria application logic | Aria is a *consumer*, not a dependency |
| Business / product workflows | Agents apply ACM; they are not ACM |
| Vector DBs, blob stores (as requirements) | Optional backends behind store interfaces |
| Scraped personas / bios as identity | Violates experience-first identity |

## Boundary tests

1. Can a new agent integrate with `pip install` + `CognitiveEngine` and no Aria imports?  
2. Does a proposed feature answer “closer to practical human cognition?” rather than host convenience?  
3. If the feature is a modality or host UI, does it fit as an **extension** or **external adapter**?

If the answer to (1) is no, or (3) points inside the core for a GUI/LLM, reject the change.

## Identity-specific boundary

Identity content is **not** a manually maintained profile blob in host config. Hosts may *assent* to proposed high-impact changes; they should not ship a static persona file that silently overwrites emergent schemas.
