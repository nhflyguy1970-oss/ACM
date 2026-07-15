# Biological vs Technical Function — ACM

**Status:** Permanent reference (from M11/M12 onward)  
**Rule:** Every future organ document MUST include both sections.

## Purpose

Separate what human cognition appears to do (science) from what ACM implements (engineering). Speculation must never be labeled as fact. Biology never dictates code shape.

## Template for every organ

### Biological function
- What function does this process serve in human cognition?
- Why might it exist (adaptive role)?
- How does it interact with memory?
- Evidence grade: well-supported / emerging / speculation
- Uncertainties

### Technical function
- Responsible ACM organ
- Inputs / outputs / artifacts / APIs
- Validation & observability
- Engineering tradeoffs
- Intentional omissions (what ACM does **not** model)

## Applied: Prediction (M11)

| Layer | Content |
|-------|---------|
| Biological | Anticipate likely upcoming cues/outcomes from experience (**well-supported** behaviorally) |
| Technical | `PredictionOrgan` scoring likely memory outcomes via Activation + Associations |
| Omissions | Neural predictive coding; action policies |

## Applied: Mental Simulation (M12)

| Layer | Content |
|-------|---------|
| Biological | Episodic future / counterfactual recombination (**well-supported**) distinct from executive planning |
| Technical | `SimulationOrgan` temporary hypothetical sequences, never Experience chronology |
| Omissions | World simulators; unconstrained story generation; planners |

## Applied ledger (completed organs — short)

| Organ | Biological (grade) | Technical |
|-------|--------------------|-----------|
| Experience | Episodic events (well-supported) | Immutable Experience records |
| Concept / Association | Semantic / relational memory (well-supported) | Living Concept/Association graphs |
| Remembering | Cue-driven reconstruction (well-supported) | Activation → Reconstruction |
| Reflection | Metacognitive evaluation (emerging–well-supported) | Reflective Experiences |
| Learning | Durable adaptation (well-supported) | Adaptation Records |
| Offline Cognition | Consolidation / replay (emerging–well-supported) | Sleep consolidate/replay |
| Attention / Priority | Resource gating (well-supported) | Allocation + importance investment |
| Forgetting | Accessibility change (well-supported) | Accessibility stages; no default delete |
| Prediction | Prospective expectation (well-supported / emerging mechanisms) | Probabilistic memory outcomes |
| Mental Simulation | Episodic future thinking (well-supported) | Hypothetical sequences |
| Memory Recombination | Constructive / generative episodic blend (well-supported) | Temporary RecombinedMemory artifacts |
| Analogical Reasoning | Structure-mapping across domains (well-supported) | Explainable AnalogyMapping artifacts |
| Memory Reconciliation | Conflict retention + corroboration / revision with lineage (well-supported) | ReconciliationRecord artifacts |
| Uncertainty & Confidence | Metamemory certainty evolves with evidence (well-supported) | ConfidenceOrgan snapshots + events |

## Applied: Memory Recombination (M13)

| Layer | Content |
|-------|---------|
| Biological | Novel blends from existing memory fragments (**well-supported**) |
| Technical | `RecombinationOrgan` temporary recombined structures; never Experiences |
| Omissions | Free generative art/LLM creativity; planning |

## Applied: Analogical Reasoning (M14)

| Layer | Content |
|-------|---------|
| Biological | Relational alignment across domains (**well-supported**) |
| Technical | `AnalogyOrgan` source↔target structure maps with observable why-codes |
| Omissions | Executive inference, decision making, theorem proving |

## Applied: Memory Reconciliation (M15)

| Layer | Content |
|-------|---------|
| Biological | Competing traces + corroboration without silent erasure (**well-supported**) |
| Technical | `ReconciliationOrgan` lineage records; Experience history immutable |
| Omissions | Forced unique truth; executive action choice |

## Applied: Uncertainty & Confidence (M16)

| Layer | Content |
|-------|---------|
| Biological | Feeling-of-knowing / confidence calibration (**well-supported**) |
| Technical | `ConfidenceOrgan` evolvable estimates + uncertainty kinds |
| Omissions | Action policies; Bayesian network mandates |
