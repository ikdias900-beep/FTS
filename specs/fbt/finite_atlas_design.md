# FBT Finite Atlas Design Specification

TASK ID: `TASK-004-FBT-ATLAS-SPEC`  
EPISTEMIC STATUS: `R` for source-derived definitions; future atlas runs must label
their own results separately.  
SOURCE ID: `SRC-FBT-2021`  
CLAIM IDS: `CLM-FBT-THM-001`, `CLM-FBT-ATLAS-001`  
ASSUMPTION IDS: `ASM-FBT-0001`, `ASM-FBT-0002`, `ASM-FBT-0003`, `ASM-FBT-0004`

## Purpose

This document designs the future Stage 4 finite atlas without running it. The atlas is a
project-defined finite restriction of FBT-style Bayesian decision problems. It is useful
only if it keeps source-derived definitions separate from extension choices.

## Source-Derived Core

A finite FBT decision problem must specify:

- finite world states `W`;
- finite perceptual states `X`;
- a prior `mu(w)`;
- a perceptual kernel `p(x | w)` or explicitly pure perceptual map;
- a nonnegative fitness function over world states or a declared payoff object;
- one or more offered perceptual states/territories for comparison;
- a Truth strategy using source MAP estimates;
- a Fitness-only strategy using expected fitness.

The Stage 2 numerical appendix is one source example of this shape. Stage 4 must not
hard-code that example as the atlas.

## Project-Defined Extension Layer

The finite atlas will later define a grid over:

- cardinalities of `W` and `X`;
- rational priors;
- rational perceptual kernels;
- rational nonnegative fitness/payoff values;
- offered-choice sets;
- optional action sets only after a separate action-model specification.

The grid is a project object. Its cell counts and aggregate frequencies are not source
theorem probabilities.

`RDR-0004` approves the Stage 4 reporting semantics: every atlas run must name a frozen
`grid_version`, aggregates must use `grid_frequency` labels, and blocked or
tie-sensitive cells must remain visible in denominator accounting.

## Strategy Families

### Source Strategy Family

The source-derived primary comparison is:

- `truth_map`: MAP point estimate followed by fitness ranking of the MAP world state;
- `fitness_only_expected`: posterior expected fitness ranking.

`RDR-0004` approves this as the primary Stage 4 comparison.

### Future Extension Baselines

The Stage 4 strategy document may later include extension baselines, each marked as
extension and reported separately:

- posterior sampling;
- posterior mean, only when `W` has an approved metric or vector structure;
- full-posterior decision baseline;
- regret-minimizing variants.

These variants must not be described as the source Truth strategy.

`truth_posterior_mean` remains unavailable until a separate metric or vector semantics
for `W` is approved.

## Approved Edge-Case Policies

`RDR-0004` approves these Stage 4 policies:

- MAP ties are represented as full MAP sets. If tied maximizers imply different
  comparison outcomes, the cell is `map_tie_policy_sensitive`; primary results must not
  use lexical or random tie-breaks.
- Observations with `P(x) = 0` produce `zero_marginal_undefined`. Comparisons depending
  on such observations are `blocked_zero_marginal`; primary exact paths must not use
  epsilon smoothing.
- Finite-grid summaries are project `grid_frequency` values under the declared
  `grid_version`, not source theorem probabilities.
- Extension baselines are reported separately from the primary `truth_map` versus
  `fitness_only_expected` comparison.

## Cell Identity

Every future atlas cell must have a stable ID derived from:

- grid version;
- `W` and `X` cardinalities;
- prior grid ID;
- kernel grid ID;
- fitness/payoff grid ID;
- offered-choice-set ID;
- strategy family ID;
- tie/zero-marginal policy ID.

The ID scheme must be deterministic before the first atlas run.

## Required Raw Outputs For Future Runs

Each evaluated cell must record:

- task IDs;
- source IDs;
- claim IDs;
- assumption IDs;
- grid version and cell ID;
- exact rational inputs;
- exact rational outputs;
- strategy decisions;
- tie flags;
- zero-marginal flags;
- strict dominance, reverse dominance, equality, or blocked status;
- command, commit, dependency-lock checksum, and manifest checksum.

## Finite-Cell Oracle

`TASK-004-FBT-ATLAS-ORACLE` implements the exact finite-cell oracle in:

- `src/fts_lab/fbt/atlas_oracle.py`

The oracle evaluates the approved primary comparison for one finite cell and records:

- observation marginals;
- posteriors for nonzero-marginal observations;
- full MAP sets;
- MAP-tie kind;
- expected fitness;
- Fitness-only best observations;
- possible Truth best observations;
- comparison status.

The oracle is not a grid enumerator, does not freeze a `grid_version`, does not write
manifests, and does not produce atlas aggregates.

## Grid v0 Smoke-Run

`TASK-004-FBT-ATLAS-GRID-V0` freezes the first small smoke grid:

- `grid_version: fbt_atlas_v0`
- config: `experiments/configs/fbt_atlas_v0.json`
- runner: `src/fts_lab/fbt/atlas_grid.py`
- command: `fts fbt atlas-grid-v0-smoke`

The smoke grid enumerates exact cells through the approved finite-cell oracle and writes
manifest-backed JSON and Markdown outputs. Its aggregate values are labeled
`grid_frequency` under `grid_version: fbt_atlas_v0`. They are not source theorem
probabilities and must not be used as full-atlas results.

## Aggregate Statistics

Aggregate statistics may be reported only after raw cell results are saved. Aggregates
must keep separate:

- source MAP Truth versus extension truth baselines;
- pure maps versus noisy kernels;
- grid frequencies versus theorem probabilities;
- ties and blocked cells;
- confirmatory metrics versus exploratory summaries.

## Remaining Gates Before Production Implementation

- independent review of the Stage 4 spec/oracle/grid-smoke bundle before public claim
  upgrade or full atlas production work.

## Out Of Scope For This Spec Gate

- full atlas engine;
- full grid enumeration beyond `fbt_atlas_v0` smoke-run;
- production atlas manifests beyond the smoke-run manifest;
- figures;
- UI;
- evolutionary dynamics;
- ML/RL.
