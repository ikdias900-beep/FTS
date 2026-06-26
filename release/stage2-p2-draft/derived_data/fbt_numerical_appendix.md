# FBT Numerical Appendix Exact Reproduction

```text
TASK ID: TASK-002-FBT-NUMERICAL
EPISTEMIC STATUS: R
SOURCE IDS: SRC-FBT-2021
CLAIM IDS: CLM-FBT-APP-001, CLM-FBT-APP-002, CLM-FBT-APP-003, CLM-FBT-APP-004
ASSUMPTION IDS: none
```

## Scope

This report reproduces the Bayesian and expected-fitness arithmetic in the FBT numerical appendix. It does not implement evolutionary dynamics or the general FBT theorem.

## Source Input

| world state | p(x1 | w) | p(x2 | w) | prior mu(w) | fitness f(w) |
|---|---:|---:|---:|---:|
| w1 | 1/4 | 3/4 | 1/7 | 20 |
| w2 | 3/4 | 1/4 | 3/7 | 4 |
| w3 | 1/4 | 3/4 | 3/7 | 3 |

## Exact Results

| observation | P(x) | posterior over (w1, w2, w3) | MAP | expected fitness |
|---|---:|---:|---|---:|
| x1 | 13/28 | (1/13, 9/13, 3/13) | w2 | 5 |
| x2 | 15/28 | (1/5, 1/5, 3/5) | w3 | 33/5 |

Unique expected-fitness winner: `x2`.

## Claim Boundary

- Allowed: the executable companion reproduces the linked appendix arithmetic.
- Forbidden: this single example proves the general FBT theorem or any claim about real perception.
