# FBT Numerical Appendix Specification

TASK ID: `TASK-002-FBT-NUMERICAL`  
EPISTEMIC STATUS: `R`  
SOURCE ID: `SRC-FBT-2021`  
CLAIM IDS: `CLM-FBT-APP-001`, `CLM-FBT-APP-002`, `CLM-FBT-APP-003`,
`CLM-FBT-APP-004`  
ASSUMPTION IDS: none

## Source Locator

`SRC-FBT-2021; version of record; Appendix: Calculations for the Numerical Example in Table 1`

Canonical bibliographic locator:
Prakash, C., Stephens, K. D., Hoffman, D. D., Singh, M., & Fields, C. (2021).
*Fitness Beats Truth in the Evolution of Perception*. Acta Biotheoretica, 69,
319-341. https://doi.org/10.1007/s10441-020-09400-0

The publisher page supplies the appendix formulas and DOI metadata. The open author
manuscript PDF was used to verify the Table 1 input rows.

## Machine-Readable Source Input

The source table is stored in `experiments/configs/fbt_numerical_example.json`.

| world state | p(x1 | w) | p(x2 | w) | prior mu(w) | fitness f(w) |
|---|---:|---:|---:|---:|
| `w1` | `1/4` | `3/4` | `1/7` | `20` |
| `w2` | `3/4` | `1/4` | `3/7` | `4` |
| `w3` | `1/4` | `3/4` | `3/7` | `3` |

## Required Calculations

For each observation `x`, compute:

```text
P(x) = sum_w p(x | w) * mu(w)
p(w | x) = p(x | w) * mu(w) / P(x)
F(x) = sum_w p(w | x) * f(w)
```

The truth estimate for this task is the unique MAP world state for the source example.
General tie policy is not specified here.

## Regression Targets

The target values are stored only in the test fixture
`tests/fixtures/fbt/numerical_appendix_expected.json`.

- `P(x1) = 13/28`
- `P(x2) = 15/28`
- `p(w | x1) = (1/13, 9/13, 3/13)` over `(w1, w2, w3)`, MAP `w2`
- `p(w | x2) = (1/5, 1/5, 3/5)` over `(w1, w2, w3)`, MAP `w3`
- `F(x1) = 5`
- `F(x2) = 33/5`

## Edge Policy

The exact source example has no MAP tie and no zero-probability observation.

For reusable helper functions:

- MAP ties raise an explicit ambiguity error and do not choose a winner;
- zero observation marginals raise an explicit Bayes-normalization error.

These errors avoid depending on the unresolved `ASM-FBT-0001` and `ASM-FBT-0002`
decisions.

## Public Claim Boundary

This task reproduces one numerical appendix example. It does not implement or test the
general FBT theorem, evolutionary game dynamics, or biological claims about real
perception.
