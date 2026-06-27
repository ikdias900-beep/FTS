# Stage 2 FBT Numerical Appendix Note

```text
TASK ID: TASK-002-FBT-NUMERICAL
STAGE: 2 - FBT numerical appendix exact reproduction
EPISTEMIC STATUS: R
SOURCE ID: SRC-FBT-2021
CLAIM IDS: CLM-FBT-APP-001, CLM-FBT-APP-002, CLM-FBT-APP-003, CLM-FBT-APP-004
ASSUMPTION IDS: none for the source example
REVIEW STATUS: accepted_with_minor_findings in REV-TASK-002-FBT-NUMERICAL-001
```

## Purpose

This note explains the exact FBT numerical-appendix reproduction in human-facing
terms. It does not introduce a new model, theorem proof, simulation, biological
interpretation, or public claim beyond the claim rows listed above.

The implemented reproduction reads the source-table inputs from
`experiments/configs/fbt_numerical_example.json`, computes exact rational
marginals, posteriors, unique MAP estimates, and expected-fitness values, then
writes manifest-backed JSON and Markdown artifacts.

## Source Objects

The source example uses:

- world states `w1`, `w2`, and `w3`;
- observations `x1` and `x2`;
- a prior distribution `mu(w)`;
- likelihoods `p(x | w)`;
- source fitness values `f(w)`.

For each observation `x`, the implementation computes:

```text
P(x) = sum_w p(x | w) * mu(w)
p(w | x) = p(x | w) * mu(w) / P(x)
F(x) = sum_w p(w | x) * f(w)
```

All arithmetic is done with exact `Fraction` values.

## Reproduced Values

| Observation | Marginal | Posterior over `(w1,w2,w3)` | MAP estimate | Expected fitness |
|---|---:|---|---|---:|
| `x1` | `13/28` | `(1/13, 9/13, 3/13)` | `w2` | `5` |
| `x2` | `15/28` | `(1/5, 1/5, 3/5)` | `w3` | `33/5` |

The expected-fitness winner in this appendix example is `x2`.

## MAP Versus Expected Fitness

MAP and expected fitness answer different questions.

MAP asks which world state has the largest posterior probability after an
observation. In the source example, `x1` maps to `w2`, while `x2` maps to `w3`.

Expected fitness weights source fitness values by the full posterior
distribution. In the same example, `x1` has expected fitness `5`, and `x2` has
expected fitness `33/5`.

The difference matters because the most probable world state is not necessarily
the one that maximizes posterior-weighted fitness. This appendix example
demonstrates that distinction for one fixed table. It is not a proof of the
general FBT theorem and is not evidence about arbitrary perceptual systems.

## Traceability

Implementation and validation are linked to:

- `TASK-002-FBT-NUMERICAL`;
- `SRC-FBT-2021`;
- `CLM-FBT-APP-001`;
- `CLM-FBT-APP-002`;
- `CLM-FBT-APP-003`;
- `CLM-FBT-APP-004`;
- `RDR-0003` for Stage 2 batched review cadence.

No new scientific assumption is used by the source example. The general edge
cases remain open in `ASM-FBT-0001` and `ASM-FBT-0002`, but the reproduced source
table has unique MAP estimates and nonzero observation marginals.

## Reproduction Commands

```bash
uv run fts fbt reproduce-numerical-example
uv run fts validate-manifest experiments/manifests/<manifest>.json
```

On Windows, if bare `uv` is not available on `PATH`, use:

```bash
py -m uv run fts fbt reproduce-numerical-example
py -m uv run fts validate-manifest experiments/manifests/<manifest>.json
```

The current committed checkpoint capsule is under `release/stage2-p2-draft/`.

## Allowed Claims

- The executable companion reproduces the published appendix marginals exactly.
- The executable companion reproduces the published appendix posteriors and MAP
  estimates for `x1` and `x2` exactly.
- The executable companion reproduces the published expected-fitness values `5`
  and `33/5` exactly.

## Forbidden Claims

- Do not claim this single example proves the general FBT theorem.
- Do not claim this is an evolutionary simulation.
- Do not claim this establishes biological universality, metaphysics,
  consciousness claims, spacetime-interface claims, or ontology claims.
- Do not treat unresolved MAP tie handling or zero-marginal behavior as settled
  for future general FBT work.

## Review State

`REV-TASK-002-FBT-NUMERICAL-001` accepted this Stage 2 reproduction with minor
findings only. There are no unresolved fatal or major findings.

The minor finding is packaging-related: the copied release manifest preserves
the original absolute generated-artifact paths. The capsule remains verifiable
through committed raw/derived files and `checksums.txt`.
