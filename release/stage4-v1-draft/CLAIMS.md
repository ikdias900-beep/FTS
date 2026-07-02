# Claims

## Packaged Claim

```text
CLAIM ID: CLM-FBT-ATLAS-001
EPISTEMIC STATUS: E
REVIEW STATUS: REV-TASK-004-FBT-ATLAS-V1-001_no_fatal_or_major
```

This capsule packages a reviewed Stage 4 atlas v1 extension checkpoint:

- `fbt_atlas_v1_draft` defines the reviewed draft config contract.
- The raw-cell engine writes a manifest-backed exact raw-cell table.
- The aggregate/report layer reads the saved raw-cell artifact and derives
  status-count and `grid_frequency` summaries.
- The aggregate denominator is all included raw cells.
- Blocked and tie-sensitive cells remain in the denominator.

## Concrete Packaged Values

For the included raw-cell artifact:

```text
total_raw_cells=144
blocked_zero_marginal=45
map_tie_policy_sensitive=11
same_best_observation=17
truth_decision_tie=71
blocked_zero_marginal_grid_frequency=5/16
```

These values describe only the included draft-grid artifact. They are project
`grid_frequency` summaries, not source theorem probabilities.

## Claims Not Made

This capsule does not claim:

- a full finite atlas run;
- an implementation, proof, reproduction, or review of Theorem 4;
- a source-level theorem probability;
- biological or real-perception validity;
- any claim about consciousness, spacetime, ontology, or metaphysics;
- ML/RL, dashboard, notebook, figure, or evolutionary-dynamics results.

`CLM-FBT-THM-001` remains a source/theorem-boundary claim with production theorem
implementation still not started.
