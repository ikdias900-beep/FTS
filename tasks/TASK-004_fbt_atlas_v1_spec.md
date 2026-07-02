# TASK-004-FBT-ATLAS-V1-SPEC: Stage 4 FBT Atlas v1 Spec Gate

TASK ID: TASK-004-FBT-ATLAS-V1-SPEC
EPISTEMIC STATUS: E

## Research Question

Can the project define a draft `atlas v1` design and config contract for future finite
FBT atlas work before implementing a reusable engine or launching a full run?

## Primary Source

- `SRC-FBT-2021`
- Version of record: https://doi.org/10.1007/s10441-020-09400-0
- Source-derived concepts reused from the Stage 4 specs:
  - finite world states `W`;
  - finite perceptual states `X`;
  - priors;
  - perceptual kernels;
  - MAP Truth strategy;
  - expected-fitness Fitness-only strategy.

## Prior Reviewed Stage 4 Inputs

This spec gate builds on the reviewed Stage 4 bundle:

- `TASK-004-FBT-ATLAS-SPEC`
- `TASK-004-FBT-ATLAS-ORACLE`
- `TASK-004-FBT-ATLAS-GRID-V0`
- `TASK-004-P4-CAPSULE`
- review status `REV-TASK-004-FBT-ATLAS-001_no_fatal_or_major`

## Expected Output

- `specs/fbt/atlas_v1_design.md`;
- `experiments/configs/fbt_atlas_v1_draft.json`;
- tests validating the draft config shape, grid identity, denominator semantics, and
  claim wording boundaries;
- registry and documentation updates showing this is a spec gate only.

## Required Design Defaults

- Primary comparison remains `truth_map` versus `fitness_only_expected`.
- Extension baselines stay outside primary results.
- Exact rational enumeration is required before any stochastic or approximate path.
- Blocked and tie-sensitive cells remain included in denominator accounting.
- Raw cell artifacts and manifests are required before aggregate reporting.
- No stochastic simulation, ML/RL, UI, dashboard, notebook, or figure work is started.

## Claims Allowed

- The project has started a draft atlas v1 spec gate.
- The draft config records intended traceability, grid identity, primary comparison,
  exact arithmetic, and denominator semantics for future engine work.

## Claims Forbidden

- Do not claim atlas v1 has run.
- Do not claim a reusable atlas engine exists.
- Do not claim Theorem 4 has been implemented, proved, reproduced, or reviewed as a
  theorem implementation.
- Do not convert finite grid frequencies into source-level probabilities.
- Do not claim biological, real-perception, consciousness, spacetime, ontology, ML/RL,
  dashboard, figure, or evolutionary-dynamics results.

## Out Of Scope

- production atlas v1 engine;
- manifest-backed v1 raw cell table;
- full finite atlas run;
- aggregate result publication;
- figures, UI, dashboards, notebooks;
- independent review in this same implementation session.

## Tests Required Before Merge

- `git diff --check`
- `py -m uv run fts doctor --release-check`
- `py -m uv run pytest`
- `py -m uv run ruff check .`
- `py -m uv run ruff format --check .`
- `py -m uv run mypy src`
