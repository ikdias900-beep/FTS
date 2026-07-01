# TASK-004-FBT-ATLAS-ORACLE: Stage 4 FBT finite-cell exact oracle

TASK ID: TASK-004-FBT-ATLAS-ORACLE
EPISTEMIC STATUS: E

## Research Question

Can the approved Stage 4 FBT finite-atlas policies from `RDR-0004` be implemented as
an exact finite-cell oracle without running a full atlas, creating aggregate results, or
upgrading public claims?

## Primary Source

- `SRC-FBT-2021`
- Source-derived formulas used through existing Stage 2 primitives:
  - Bayesian marginalization;
  - posterior normalization;
  - MAP estimates;
  - expected fitness.

The oracle is a project-defined finite-cell extension around source-derived objects. It
is not an implementation or proof of Theorem 4.

## Formal Definitions

The oracle evaluates one finite decision cell:

- finite world states `W`;
- finite observations/perceptual states `X`;
- exact rational priors;
- exact rational observation kernels;
- exact rational nonnegative fitness values;
- an offered observation set;
- primary comparison `truth_map` versus `fitness_only_expected`.

Approved `RDR-0004` policies:

- MAP ties are represented as full MAP sets.
- MAP ties with distinct Truth fitness that can change the decision are
  `map_tie_policy_sensitive`.
- `P(x) = 0` produces `zero_marginal_undefined`.
- Comparisons depending on a zero-marginal observation are `blocked_zero_marginal`.
- Primary exact paths do not use smoothing, random tie-breaking, or lexical tie-breaking.
- Finite-cell outcomes are not theorem probabilities or atlas aggregate frequencies.

## Input Domain

Committed fixture cases live in:

- `tests/fixtures/fbt/stage4_fbt_oracle_cases.json`

These are exact small-cell oracle fixtures, not generated atlas results.

## Expected Output

- `src/fts_lab/fbt/atlas_oracle.py`;
- exact fixture-backed tests for approved edge-case policies;
- registry and documentation updates showing that Stage 4 has an oracle, but no atlas
  run or reviewed result.

## Known Small Cases

The fixture covers:

- unique MAP where `truth_map` and `fitness_only_expected` choose the same observation;
- MAP tie with same Truth fitness, determined without tie-breaking;
- MAP tie with distinct Truth fitness, classified as `map_tie_policy_sensitive`;
- zero-marginal observation, classified as `blocked_zero_marginal` at cell level;
- a strict-dominance finite cell where Fitness-only chooses a higher expected-fitness
  observation than Truth.

The Stage 2 numerical appendix source table is also checked as a valid Stage 4 primary
cell input.

## Invariants

- No full finite-atlas grid enumeration.
- No `grid_version` freeze in this task.
- No manifests, generated atlas artifacts, reports, figures, UI, notebooks, or release
  capsule.
- No stochastic simulation.
- No theorem implementation.
- No random, lexical, or hidden tie-break.
- No finite grid frequency or theorem-probability claim.

## Assumptions

Approved assumptions used:

- `ASM-FBT-0001`;
- `ASM-FBT-0002`;
- `ASM-FBT-0003`;
- `ASM-FBT-0004`.

Approval source:

- `RDR-0004`.

## Tests Required Before Merge

- exact oracle fixture tests;
- Stage 4 spec-gate tests;
- FBT numerical appendix regression tests;
- registry tests;
- `ruff`, `mypy`, `pytest`, and `fts doctor --release-check`.

## Artifacts To Save

No generated experiment artifacts are saved by this task.

Committed files are:

- task brief;
- oracle implementation;
- fixture JSON;
- exact tests;
- registry/documentation updates.

## Claims Allowed

- The project has an exact finite-cell oracle for the approved Stage 4 primary
  comparison policy.
- The oracle handles the approved MAP-tie and zero-marginal policies on small exact
  fixture cases.
- `CLM-FBT-ATLAS-001` has an implementation component pending independent review.

## Claims Forbidden

- Do not claim the finite atlas has been run.
- Do not claim any aggregate grid frequency.
- Do not claim a theorem probability has been reproduced.
- Do not claim Theorem 4 has been implemented or proved.
- Do not claim any result about real perception, consciousness, spacetime, ontology,
  biology, ML/RL, or evolutionary dynamics.

## Out Of Scope

- frozen `grid_version`;
- atlas sweeps;
- manifest-backed atlas run;
- aggregate statistics;
- public release capsule;
- independent review in this same implementation session.

## Review Cadence

Independent review remains deferred until the Stage 4 spec/oracle/grid-smoke bundle is
ready for a fresh-context reviewer, unless the Human PI requests earlier review.
