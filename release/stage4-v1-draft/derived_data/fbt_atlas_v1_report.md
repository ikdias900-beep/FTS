# FBT Atlas v1 Aggregate Report

```text
TASK IDS: TASK-004-FBT-ATLAS-V1-SPEC, TASK-004-FBT-ATLAS-V1-ENGINE, TASK-004-FBT-ATLAS-V1-AGGREGATE
EPISTEMIC STATUS: E
SOURCE IDS: SRC-FBT-2021
CLAIM IDS: CLM-FBT-ATLAS-001
ASSUMPTION IDS: ASM-FBT-0001, ASM-FBT-0002, ASM-FBT-0003, ASM-FBT-0004
GRID VERSION: fbt_atlas_v1_draft
AGGREGATE LABEL: grid_frequency
DENOMINATOR POLICY: all_enumerated_cells
DENOMINATOR BASIS: all_raw_cells
RECOMPUTES CELLS: false
```

## Scope

This report reads one saved `fbt_atlas_v1_raw_cell_table` artifact and summarizes its cell statuses. It does not read the draft config, regenerate cells, launch a full atlas run, or implement Theorem 4.

## Input Artifact

- artifact_kind: `fbt_atlas_v1_raw_cell_table`
- raw_cell_count: `144`
- path: `C:\Users\user\Fitness, Truth & Structure Lab\results\raw\EXP-TASK-004-FBT-ATLAS-V1-RAW-CELLS-20260702T080919Z-0AE3BB9C\fbt_atlas_v1_raw_cells.json`
- sha256: `582e7e50fd8b1bfab149feab6e00d80cd95bda29268ff6fec99e0a5ed4748613`

## Status Summary

Total raw cells: `144`.

| status | count | grid_frequency |
|---|---:|---:|
| `blocked_zero_marginal` | 45 | 5/16 |
| `map_tie_policy_sensitive` | 11 | 11/144 |
| `same_best_observation` | 17 | 17/144 |
| `truth_decision_tie` | 71 | 71/144 |

## Claim Boundary

- Allowed: status-count and grid_frequency summaries over the input raw cells.
- Forbidden: treating this as a full atlas, theorem implementation, or biological or metaphysical result.
