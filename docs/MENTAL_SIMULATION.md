# Mental Simulation — ACM

**Status:** Canonical for M12 (implemented)  
**Cognitive question:** *What possible futures can memory imagine?*  
**Companions:** [`HYPOTHETICAL_MEMORY.md`](HYPOTHETICAL_MEMORY.md) · [`PREDICTION_MODEL.md`](PREDICTION_MODEL.md) · [`BIOLOGICAL_VS_TECHNICAL_FUNCTION.md`](BIOLOGICAL_VS_TECHNICAL_FUNCTION.md)

## Biological function

Humans recombine past episodes into counterfactual / prospective scenes (episodic future thinking — **well-supported**). Simulation supports preparation and evaluation without acting. It is **not** the same as executive planning (**distinct**: simulation explores; planning commits).

## Technical function

Mental Simulation builds **temporary hypothetical memory structures** and sequences from existing Concepts, Associations, Experiences (read-only), Identity, Learning, and Priority — clearly tagged non-historical.

| Field | Content |
|-------|---------|
| Organ | `SimulationOrgan` |
| Inputs | Cue + Activation + Prediction hints (optional) + living structures |
| Outputs | Hypothetical sequences / branches with lineage; simulation confidence |
| Validation | No Experience birth; store.hypotheses only; marked `hypothetical=true` |

## Ownership

| Owns | Does not own |
|------|----------------|
| Hypothetical recombination / counterfactual replay | Planning, decisions, reasoning engines |
| Distinguishing imagined vs remembered | Rewriting history |

## Intentional omissions

World physics engines, unconstrained generative narrative, tool-use rehearsal, optimization of action policies.
