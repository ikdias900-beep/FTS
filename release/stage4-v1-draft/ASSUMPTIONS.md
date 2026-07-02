# Assumptions

No new scientific assumption is introduced by this capsule.

## Approved Stage 4 Assumptions Used

| ID | Status | Role in this capsule |
|---|---|---|
| `ASM-FBT-0001` | APPROVED | MAP ties are represented as full MAP sets; tie-sensitive cells are classified explicitly. |
| `ASM-FBT-0002` | APPROVED | Zero-marginal observations remain undefined; no epsilon smoothing is used. |
| `ASM-FBT-0003` | APPROVED | Finite-grid summaries are reported as project `grid_frequency`, not source theorem probability. |
| `ASM-FBT-0004` | APPROVED | The primary comparison is `truth_map` versus `fitness_only_expected`; extension baselines are outside primary results. |

These assumptions were approved via `RDR-0004-stage4-fbt-blockers.md`.

## Boundary

The capsule does not add a new tie rule, probability measure, grid semantics,
truth-strategy family, stochastic model, or evolutionary model.
