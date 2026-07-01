# TASK-004-FBT-ATLAS-GRID-V0: Stage 4 FBT finite-atlas grid v0 smoke-run

TASK ID: TASK-004-FBT-ATLAS-GRID-V0
EPISTEMIC STATUS: E

## Research Question

Can the project freeze a minimal exact finite grid version for Stage 4 FBT-style
decision cells and run it through the approved finite-cell oracle with a reproducible
manifest, without treating the resulting grid frequencies as source theorem
probabilities?

## Primary Source

- `SRC-FBT-2021`
- Source-derived objects reused through Stage 2 and Stage 4 primitives:
  - Bayesian marginalization;
  - posterior normalization;
  - MAP estimates;
  - expected fitness.

This task is a project-defined extension around source-derived objects. It is not an
implementation or proof of Theorem 4.

## Formal Definitions

The frozen smoke grid is identified by:

- `grid_version: fbt_atlas_v0`
- exact rational priors;
- exact rational observation kernels;
- exact rational nonnegative fitness values;
- offered observation sets;
- primary comparison `truth_map` versus `fitness_only_expected`;
- approved `RDR-0004` policies for MAP ties, zero-marginal observations, finite-grid
  reporting, and primary strategy separation.

Aggregate labels must use `grid_frequency`, not theorem probability.

## Input Domain

Committed configuration:

- `experiments/configs/fbt_atlas_v0.json`

The grid intentionally stays small enough to serve as a smoke-run fixture:

- two world states;
- two observations;
- a small set of priors, kernels, and fitness functions;
- one offered observation set.

## Expected Output

- `src/fts_lab/fbt/atlas_grid.py`;
- CLI command `fts fbt atlas-grid-v0-smoke`;
- exact tests for config validation, enumeration, status accounting, and report language;
- manifest-backed JSON and Markdown outputs when the command is run;
- registry and documentation updates showing that Stage 4 has a frozen smoke grid, but
  no full atlas result or reviewed public claim upgrade.

## Known Small Cases

The grid must include cells exercising:

- ordinary evaluated cells;
- zero-marginal blocked cells;
- MAP-tie-sensitive cells;
- deterministic exact rational serialization.

The existing oracle fixtures remain the detailed edge-case oracle tests. This smoke grid
tests end-to-end enumeration and manifest discipline.

## Invariants

- Results are exact rational values.
- Cell IDs are deterministic before execution.
- Every generated manifest links `TASK-004-FBT-ATLAS-GRID-V0`, `CLM-FBT-ATLAS-001`,
  `SRC-FBT-2021`, and `ASM-FBT-0001..0004`.
- Grid summaries use `grid_frequency` labels and preserve denominator accounting for
  blocked and tie-sensitive cells.
- No finite-grid frequency is described as a source theorem probability.
- No smoothing, lexical tie-break, random tie-break, stochastic simulation, ML/RL,
  figure generation, UI, or evolutionary dynamics is introduced.

## Assumptions

Approved assumptions used:

- `ASM-FBT-0001`;
- `ASM-FBT-0002`;
- `ASM-FBT-0003`;
- `ASM-FBT-0004`.

Approval source:

- `RDR-0004`.

## Tests Required Before Merge

- exact atlas grid tests;
- Stage 4 oracle tests;
- Stage 4 spec-gate tests;
- FBT numerical appendix regression tests;
- manifest/CLI integration tests;
- registry tests;
- `ruff`, `mypy`, `pytest`, and `fts doctor --release-check`.

## Artifacts To Save

When executed, the CLI saves:

- `results/derived/<run_id>/fbt_atlas_v0_smoke.json`;
- `results/reports/<run_id>/fbt_atlas_v0_smoke.md`;
- `experiments/manifests/<manifest_id>.json`.

Generated result artifacts are reproducible outputs, not committed release artifacts in
this task.

## Claims Allowed

- The project defines a frozen small exact grid `fbt_atlas_v0` for Stage 4 smoke-run
  testing.
- The command `fts fbt atlas-grid-v0-smoke` enumerates that grid through the approved
  finite-cell oracle and writes a validated manifest.
- The resulting aggregate values are project `grid_frequency` values for this frozen
  grid only.

## Claims Forbidden

- Do not claim the full finite atlas has been run.
- Do not claim any grid frequency is a source theorem probability.
- Do not claim Theorem 4 has been implemented, proved, or reproduced.
- Do not claim a reviewed Stage 4 public result.
- Do not claim any result about real perception, consciousness, spacetime, ontology,
  biology, ML/RL, or evolutionary dynamics.

## Out Of Scope

- full atlas sweeps;
- theorem implementation;
- extension truth baselines beyond the approved primary comparison;
- figures;
- UI;
- public release capsule;
- independent review in this same implementation session.

## Review Cadence

Independent review remains deferred until the Stage 4 spec/oracle/grid-smoke bundle is
ready for a fresh-context reviewer, unless the Human PI requests earlier review.
