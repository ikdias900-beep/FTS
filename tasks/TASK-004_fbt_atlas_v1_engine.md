# TASK-004-FBT-ATLAS-V1-ENGINE: Stage 4 FBT Atlas v1 Raw-Cell Engine

TASK ID: TASK-004-FBT-ATLAS-V1-ENGINE
EPISTEMIC STATUS: E

## Research Question

Can the project implement a reusable atlas v1 engine that reads the draft v1 config,
enumerates exact finite raw cells, and writes a manifest-backed raw-cell table before
any aggregate result, full atlas claim, or public claim upgrade?

## Primary Source

- `SRC-FBT-2021`
- Version of record: https://doi.org/10.1007/s10441-020-09400-0
- Source-derived concepts reused through the reviewed Stage 4 bundle:
  - finite world states `W`;
  - finite perceptual states `X`;
  - priors;
  - perceptual kernels;
  - MAP Truth strategy;
  - expected-fitness Fitness-only strategy.

## Prior Reviewed Stage 4 Inputs

This implementation builds on:

- `TASK-004-FBT-ATLAS-SPEC`
- `TASK-004-FBT-ATLAS-ORACLE`
- `TASK-004-FBT-ATLAS-GRID-V0`
- `TASK-004-P4-CAPSULE`
- `TASK-004-FBT-ATLAS-V1-SPEC`
- review status `REV-TASK-004-FBT-ATLAS-001_no_fatal_or_major` for the earlier
  spec/oracle/grid-smoke bundle.

## Expected Output

- reusable engine module `src/fts_lab/fbt/atlas_v1.py`;
- CLI command `fts fbt atlas-v1-raw-cells`;
- manifest-backed raw-cell JSON output under `results/raw/`;
- tests for config validation, deterministic cell identity, exact raw-cell contents,
  denominator-policy preservation, and CLI manifest discipline;
- registry and documentation updates showing this is pending review and not a full
  atlas result.

## Input Domain

The first v1 engine path uses `experiments/configs/fbt_atlas_v1_draft.json`.

The draft grid expands deterministic representative families for:

- world-state counts `2, 3`;
- perceptual-state counts `2, 3`;
- prior families `uniform`, `single_state_heavy`, `rational_simplex_small`;
- kernel families `pure_map`, `noisy_map`, `uninformative`, `zero_marginal_probe`;
- fitness families `single_peak`, `equal`, `multi_peak`;
- offered-observation set `all_observations`.

These are project-defined representative grid families, not the source theorem domain.

## Invariants

- Use exact rational arithmetic only.
- Use the reviewed finite-cell oracle for the primary comparison.
- Do not add stochastic simulation, approximate arithmetic, ML/RL, UI, notebooks, or
  figures.
- Do not compute or publish aggregate frequencies in this task.
- Preserve blocked and tie-sensitive statuses in raw cells.
- Write a manifest recording command, config checksum, output checksum, git state,
  dependency-lock checksum, task IDs, claim IDs, source IDs, and assumption IDs.

## Assumptions

No new scientific assumption is introduced.

Approved Stage 4 assumptions used:

- `ASM-FBT-0001`: MAP ties are represented as full MAP sets.
- `ASM-FBT-0002`: zero-marginal observations remain undefined.
- `ASM-FBT-0003`: finite-grid semantics are project `grid_frequency` semantics when
  aggregates are later added; this task writes raw cells only.
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

- The project has a reusable atlas v1 raw-cell engine over the draft v1 config.
- The engine writes exact manifest-backed raw cell tables for the declared draft
  representative families.
- Raw cells preserve traceability and edge-case statuses needed for later aggregate
  design and review.

## Claims Forbidden

- Do not claim a full finite atlas has been run.
- Do not publish aggregate frequencies from this task as a scientific result.
- Do not claim Theorem 4 has been implemented, proved, reproduced, or reviewed as a
  theorem implementation.
- Do not treat project raw cells or future grid frequencies as source-level theorem
  probabilities.
- Do not claim biological, real-perception, consciousness, spacetime, ontology, ML/RL,
  dashboard, figure, or evolutionary-dynamics results.

## Out Of Scope

- full atlas result;
- aggregate result table or report;
- release capsule;
- independent review in this same implementation session;
- figures, UI, dashboards, notebooks;
- stochastic simulation, ML/RL, or evolutionary dynamics.
