# Claims

```text
TASK ID: TASK-002-FBT-NUMERICAL
EPISTEMIC STATUS: R
SOURCE IDS: SRC-FBT-2021
CLAIM IDS: CLM-FBT-APP-001; CLM-FBT-APP-002; CLM-FBT-APP-003; CLM-FBT-APP-004
ASSUMPTION IDS: none
REVIEW STATUS: pending batched independent review
```

## Allowed Claims In This Capsule

- The executable companion reproduces the two published stimulus marginals exactly:
  `P(x1)=13/28` and `P(x2)=15/28`.
- The exact posterior for `x1` over `(w1, w2, w3)` is `(1/13, 9/13, 3/13)`, with
  unique MAP estimate `w2`.
- The exact posterior for `x2` over `(w1, w2, w3)` is `(1/5, 1/5, 3/5)`, with
  unique MAP estimate `w3`.
- The exact expected-fitness values are `5` for `x1` and `33/5` for `x2`; `x2` is the
  unique expected-fitness winner in this source example.
- The generated result is linked to a manifest with commit, dependency-lock checksum,
  command, parameters, input, output, and checksum metadata.

## Status Boundaries

- All scientific rows in this capsule are `R`: reproduction of the source numerical
  appendix from `SRC-FBT-2021`.
- No project-added scientific assumption is used.
- General MAP tie handling and zero-marginal behavior remain unresolved for future
  general FBT work; this source example does not invoke either case.

## Forbidden Claims

- This numerical example proves the general FBT theorem.
- This numerical example establishes any claim about real human perception,
  consciousness, spacetime, ontology, or conscious agents.
- MAP is the only possible truth-oriented inference rule in all future models.
- The expected-fitness comparison in one source example is an evolutionary simulation.
- This draft checkpoint has passed independent review.
