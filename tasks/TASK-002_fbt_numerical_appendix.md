# TASK-002-FBT-NUMERICAL: FBT Numerical Appendix Exact Reproduction

TASK ID: TASK-002-FBT-NUMERICAL
EPISTEMIC STATUS: R

## Research Question

Can the numerical Bayesian and expected-fitness calculations in the appendix of
`SRC-FBT-2021` be reproduced exactly from the published Table 1 inputs?

## Primary Source

- `SRC-FBT-2021`
- Version of record: https://doi.org/10.1007/s10441-020-09400-0
- Source locator: `SRC-FBT-2021; version of record; Appendix: Calculations for the Numerical Example in Table 1`
- Table-input access note: the publisher appendix is the canonical locator; the author
  manuscript PDF was used to verify the Table 1 input rows.

## Formal Definitions

The task is limited to a finite Bayesian decision problem with:

- world states `w1`, `w2`, `w3`;
- observations `x1`, `x2`;
- prior probabilities `mu(w)`;
- likelihoods `p(x | w)`;
- scalar fitness values `f(w)`;
- exact rational arithmetic.

The implementation computes:

- observation marginals by summing `p(x | w) * mu(w)` over world states;
- posteriors by Bayes' rule;
- unique MAP estimates for the source example;
- expected fitness per observation by summing `p(w | x) * f(w)`.

## Input Domain

The canonical machine-readable source input is
`experiments/configs/fbt_numerical_example.json`.

## Expected Output

- exact marginals for `x1` and `x2`;
- exact posteriors over `(w1, w2, w3)` for each observation;
- unique MAP estimates for each observation;
- exact expected-fitness values for each observation;
- a manifest-backed JSON result and human-readable derivation report from
  `fts fbt reproduce-numerical-example`.

## Known Small Cases

The regression fixture is `tests/fixtures/fbt/numerical_appendix_expected.json`.
It contains only expected source targets and source citation metadata; production code
does not import it.

## Invariants

- priors sum to exactly `1`;
- each likelihood row over observations sums to exactly `1`;
- all probabilities are non-negative exact `Fraction` values;
- every posterior distribution sums to exactly `1`;
- MAP estimates are unique for the source example;
- no target result is hard-coded in implementation logic.

## Assumptions

No project-added scientific assumption is used by this task.

Open assumptions acknowledged but not invoked:

- `ASM-FBT-0001`: general MAP tie handling remains open; the source example has
  unique MAP estimates, and reusable helpers raise an explicit error on ties.
- `ASM-FBT-0002`: zero-probability observations remain open; the source example has
  nonzero marginals, and reusable helpers raise an explicit error on zero marginals.

## Tests Required Before Merge

- exact unit tests for marginals, posteriors, MAP estimates, and expected fitness;
- input-perturbation test showing changed source table inputs change computed results;
- explicit tests for ambiguous MAP and zero-marginal rejection;
- CLI integration test that writes outputs and validates the manifest;
- `ruff`, `mypy`, `pytest`, and `fts doctor --release-check`.

## Artifacts To Save

Generated run artifacts are immutable and not committed by default:

- `results/derived/EXP-TASK-002-FBT-NUMERICAL-*/fbt_numerical_appendix.json`;
- `results/reports/EXP-TASK-002-FBT-NUMERICAL-*/fbt_numerical_appendix.md`;
- `experiments/manifests/ART-TASK-002-FBT-NUMERICAL-MANIFEST-*.json`.

## Claims Allowed

- `CLM-FBT-APP-001`: the executable companion reproduces the two published
  stimulus marginals exactly.
- `CLM-FBT-APP-002`: the exact posterior and MAP estimate for `x1` match the
  published example.
- `CLM-FBT-APP-003`: the exact posterior and MAP estimate for `x2` match the
  published example.
- `CLM-FBT-APP-004`: the exact expected-fitness values match the published example.

## Claims Forbidden

- Do not claim this example proves the general FBT theorem.
- Do not claim anything about real human perception, consciousness, spacetime, or
  ontology.
- Do not claim MAP is the only possible truth-oriented decision rule in future models.
- Do not silently choose a tie rule or zero-marginal behavior for general FBT modules.

## Out Of Scope

- evolutionary simulation;
- genetic algorithms;
- proof or implementation of the FBT theorem;
- finite FBT atlas;
- ML/RL models;
- dashboards or UI.
