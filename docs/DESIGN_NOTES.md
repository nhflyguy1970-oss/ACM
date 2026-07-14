# Design Notes

Working implementation notes that do not override the constitution or architecture freeze.

## M0 substrate

The in-memory store is an engineering convenience. Cognitive verbs must remain valid when a durable backend is introduced.

## Preference parsing

M0 uses lightweight regex extraction for preference statements to enable early behavioral tests. This is **not** the long-term concept-formation organ; M3 should grow concept induction beyond keyword patterns.

## Default attention

Unmarked experiences may fail the durability gate (`encode_weight(DEFAULT) < 0.5`) unless `pin=True` or `kind` is `preference` / `identity`. This intentionally rejects encoding everything.

## Host adapters

Skeleton package `acm.adapters` exists for future *generic* adapter interfaces. Concrete Aria / FlyTying / robotics adapters belong outside this repository until governance opens that boundary.

## M1 Identity

Schema nuclei (`agent` / `user` / `project`) are organizational anchors. Attribute content is experience-driven. High-impact conflicts become proposals (D009). Preference encodes may create **adjacent** links without rewriting schema statements.

Architecture freeze still mentions “Aria-self”; ACM interprets this as host-agnostic **agent-self** (D008).

## M2 Experience

Encode always births Experiences through `ExperienceOrgan` when durable. Lifecycle/salience overlays preserve immutability (D012). Roadmap renumber: Experience before Working-memory depth (D011).

## M3 Concept

Encode cues → `ConceptOrgan.ingest_from_encode` → Experience birth → `bind_experience` evidence. Hierarchy `is_a` is Concept-owned (D016). Preference `favorite_*` keys are the only global attribute-key upserts (prevents token collapse). Merge/split are proposals only.
