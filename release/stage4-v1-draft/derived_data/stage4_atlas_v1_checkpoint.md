# Stage 4 Atlas v1 Checkpoint Summary

```text
CAPSULE ID: STAGE4-V1-DRAFT
TASK ID: TASK-004-ATLAS-V1-CAPSULE
CLAIM ID: CLM-FBT-ATLAS-001
EPISTEMIC STATUS: E
REVIEW STATUS: REV-TASK-004-FBT-ATLAS-V1-001_no_fatal_or_major
```

## What This Checkpoint Packages

This checkpoint packages the reviewed atlas v1 pipeline:

```text
draft config -> exact raw-cell engine -> manifest-backed raw-cell JSON
             -> aggregate/report layer reading that raw JSON
             -> manifest-backed derived JSON/Markdown summary
```

The aggregate layer reads `raw_data/fbt_atlas_v1_raw_cells.json`. It does not read the
draft config or regenerate cells.

## Packaged Summary

| status | count | grid_frequency |
|---|---:|---:|
| `blocked_zero_marginal` | 45 | 5/16 |
| `map_tie_policy_sensitive` | 11 | 11/144 |
| `same_best_observation` | 17 | 17/144 |
| `truth_decision_tie` | 71 | 71/144 |

Total raw cells: `144`.

## Boundary

The checkpoint does not claim a full atlas run, Theorem 4 implementation, source
theorem probability, biological result, metaphysical result, ML/RL result, UI,
notebook, figure, or evolutionary-dynamics result.
