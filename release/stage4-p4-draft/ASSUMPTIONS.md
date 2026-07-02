# Assumptions

No new scientific assumption is introduced by this capsule.

Approved Stage 4 assumptions:

| ID | Status | Capsule use |
|---|---|---|
| `ASM-FBT-0001` | APPROVED | MAP ties are represented as full MAP sets; tie-sensitive cells stay labeled. |
| `ASM-FBT-0002` | APPROVED | Zero-marginal observations remain undefined and can block comparisons. |
| `ASM-FBT-0003` | APPROVED | Frozen finite grids report `grid_frequency`, not theorem probability. |
| `ASM-FBT-0004` | APPROVED | The primary comparison is `truth_map` versus `fitness_only_expected`. |

These approvals are recorded in `docs/decisions/RDR-0004-stage4-fbt-blockers.md` and
`assumptions/register.md`.
