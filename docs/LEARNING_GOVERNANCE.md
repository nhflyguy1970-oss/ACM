# Learning Governance — ACM

**Status:** Canonical for L0 (design only)  
**Companions:** [`LEARNING_ARCHITECTURE.md`](LEARNING_ARCHITECTURE.md) · [`LEARNING_RESEARCH_FOUNDATIONS.md`](LEARNING_RESEARCH_FOUNDATIONS.md) · [`CORE_BOUNDARIES.md`](CORE_BOUNDARIES.md) · Identity Policy Gate precedents (D009)

---

## Learning ≠ self-improvement

| | Continuous Learning | Architectural self-improvement |
|--|---------------------|--------------------------------|
| Changes | Living cognitive *content* / strengths | Organs, activation policies, assent rules, core verbs |
| Cadence | Ongoing | Rare, explicit |
| Authority | Automatic or per Adaptation assent | **Always** explicit user authorization |
| Examples | Prefer coffee more; husky↔dog strong | Changing decay constants system-wide; adding organs |

Preserve **user trust** above throughput of change.

---

## Three gate classes

### A — Automatic learning (low-impact)

May apply without interactive assent when **all** hold:

1. Magnitude below organ-specific caps (to be fixed at M7).  
2. Target is Association strength, Concept strength/confidence (bounded), preference confidence within existing keys, or goal importance nudge.  
3. Triggered by Reflective Experience or repeated congruent encode evidence.  
4. Full Adaptation Record written.  
5. No Identity conflicting adopt; no Concept merge/split; no deletion.  

Rollback: always reverseable via Adaptation lineage (see below).

### B — Permission-required learning (high-impact)

Require `assent_adaptation` (host/user), mirroring Identity Policy Gate:

- Identity attribute adopt / supersede / erase  
- Mature Concept merge / split / retire  
- Association kind ontology expansion that reinterprets large neighborhoods  
- Goal abandon / create as lasting policy  
- Preference key deletion or cross-context forced unification  
- Any batch marked `sleep_high_impact`

### C — Never automatic / never Learning alone

- Experience content rewrite or delete  
- Changing Activation Architecture constants / algorithms  
- Changing Learning policy itself  
- Host-secret ingestion as identity  
- Capability Bus / Aria coupling  

These require **constitution / roadmap authorization**, not Learning assent UX.

---

## Trust model

1. **Visibility** — every adaptation is harness-observable.  
2. **Attribution** — lineage to Reflective Experiences / evidence.  
3. **Reversibility** — automatic adaptations store `before` snapshots sufficient to roll back.  
4. **Honesty** — Learning may record “I did not adapt because uncertainty remained.”  
5. **Host neutrality** — hosts may wrap assent UI; ACM defines the gate, not a product UI.

---

## Rollback philosophy

- Prefer **compensating Adaptations** over destructive erase.  
- Rolling back never invents false Experiences; it restores prior living-structure values with a new Adaptation of kind `rollback`.  
- Identity/Concept high-impact rollbacks leave lineage entries (as Identity already does).

---

## Auditability

`what_have_i_learned` must be answerable from Adaptation Records + public summaries — not from hidden optimizer state. No prompts. No chain-of-thought fields.

---

## Conflict with existing organs

| Conflict | Resolution |
|----------|------------|
| Concept organ already strengthens on bind | Learning owns *cross-episode outcome-sensitive* policy; Concept retains birth/hierarchy mechanics; M7 must avoid double-counting via single Adaptation pipeline |
| Remembering light reconsolidation | Remains accessibility-only; Learning owns durable skill/preference lessons beyond light recall bumps |
| Reflection confidence assessment | Evaluation only; Learning may later write confidence *if* gated |

---

## Assent UX (host responsibility)

ACM exposes proposal ids + public summaries. Hosts present them. ACM does not depend on Aria Mission Control.
