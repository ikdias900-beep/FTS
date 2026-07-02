# FBT Atlas Grid v0 Smoke Run

```text
TASK ID: TASK-004-FBT-ATLAS-GRID-V0
EPISTEMIC STATUS: E
SOURCE IDS: SRC-FBT-2021
CLAIM IDS: CLM-FBT-ATLAS-001
ASSUMPTION IDS: ASM-FBT-0001, ASM-FBT-0002, ASM-FBT-0003, ASM-FBT-0004
GRID VERSION: fbt_atlas_v0
AGGREGATE LABEL: grid_frequency
THEOREM PROBABILITY CLAIM: false
```

## Scope

This report enumerates the frozen `fbt_atlas_v0` smoke grid through the approved Stage 4 finite-cell oracle. It is not a full atlas run and not a source theorem probability calculation.

## Status Summary

Total enumerated cells: `24`.

| status | count | grid_frequency |
|---|---:|---:|
| `blocked_zero_marginal` | 6 | 1/4 |
| `map_tie_policy_sensitive` | 4 | 1/6 |
| `same_best_observation` | 6 | 1/4 |
| `truth_decision_tie` | 8 | 1/3 |

## Claim Boundary

- Allowed: this command produces exact grid_frequency values for `fbt_atlas_v0`.
- Forbidden: treating those frequencies as Theorem 4 probabilities or as a reviewed scientific conclusion.
