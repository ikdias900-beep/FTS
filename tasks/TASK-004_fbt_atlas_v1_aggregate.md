# TASK-004-FBT-ATLAS-V1-AGGREGATE: Stage 4 FBT Atlas v1 Aggregate/Report Layer

TASK ID: TASK-004-FBT-ATLAS-V1-AGGREGATE
EPISTEMIC STATUS: E

## Research Question

Can the project add an aggregate/report layer for atlas v1 that reads a saved raw-cell
artifact, writes manifest-backed derived outputs, and avoids hidden recomputation from
the draft config?

## Primary Source

- `SRC-FBT-2021`
- Version of record: https://doi.org/10.1007/s10441-020-09400-0
- Source-derived concepts remain those already used by the reviewed Stage 4 bundle and
  the v1 raw-cell engine:
  - finite world states `W`;
  - finite perceptual states `X`;
  - priors;
  - perceptual kernels;
  - MAP Truth strategy;
  - expected-fitness Fitness-only strategy.

## Prior Inputs

This task builds on:

- `TASK-004-FBT-ATLAS-V1-SPEC`
- `TASK-004-FBT-ATLAS-V1-ENGINE`
- `REV-TASK-004-FBT-ATLAS-001_no_fatal_or_major` for the earlier grid-v0 bundle.

## Expected Output

- module `src/fts_lab/fbt/atlas_v1_aggregate.py`;
- CLI command `fts fbt atlas-v1-aggregate --raw-cells <path>`;
- derived JSON output under `results/derived/`;
- Markdown report under `results/reports/`;
- scientific manifest under `experiments/manifests/`;
- exact tests proving the aggregate is computed from raw-cell rows only;
- integration tests proving manifest input/output discipline;
- independent-review brief for the full v1 design/engine/raw/results bundle.

## Input Domain

The command accepts one saved `fbt_atlas_v1_raw_cell_table` JSON artifact. It does not
accept a config path, enumerate a grid, or regenerate raw cells.

## Invariants

- The only aggregate input is the raw-cell artifact.
- Aggregate status counts are computed from `cells[*].status`.
- `grid_frequency` values are exact rational fractions over all input raw cells.
- Blocked and tie-sensitive cells remain in the denominator.
- The derived JSON must not embed the full raw `cells` table.
- The manifest must list the raw-cell JSON as an input and the derived JSON/Markdown
  files as outputs.
- The aggregate module must not import the raw-cell engine functions used to enumerate
  cells.

## Assumptions

No new scientific assumption is introduced.

Approved Stage 4 assumptions used:

- `ASM-FBT-0001`: MAP ties are represented as full MAP sets.
- `ASM-FBT-0002`: zero-marginal observations remain undefined.
- `ASM-FBT-0003`: finite-grid aggregates are project `grid_frequency` values.
- `ASM-FBT-0004`: primary comparison is `truth_map` versus
  `fitness_only_expected`.

## Tests Required Before Merge

- `git diff --check`
- `py -m uv run fts doctor --release-check`
- `py -m uv run pytest`
- `py -m uv run ruff check .`
- `py -m uv run ruff format --check .`
- `py -m uv run mypy src`

## Claims Allowed

- The project can derive manifest-backed atlas v1 status summaries from a saved raw-cell
  artifact.
- The aggregate report gives `grid_frequency` summaries for the input raw artifact only.
- The aggregate/report layer is ready for independent review as part of the v1 bundle.

## Claims Forbidden

- Do not claim a full finite atlas has been run.
- Do not claim Theorem 4 has been implemented, proved, reproduced, or reviewed.
- Do not treat project grid frequencies as source theorem results.
- Do not claim biological, real-perception, consciousness, spacetime, ontology, ML/RL,
  dashboard, figure, or evolutionary-dynamics results.

## Out Of Scope

- full atlas result;
- theorem implementation;
- release capsule;
- figures, UI, dashboards, notebooks;
- stochastic simulation, ML/RL, or evolutionary dynamics;
- independent review in this same implementation session.
