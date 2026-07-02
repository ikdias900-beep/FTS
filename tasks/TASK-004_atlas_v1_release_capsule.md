# TASK-004-ATLAS-V1-CAPSULE: Stage 4 Atlas v1 Reviewed Checkpoint Capsule

TASK ID: TASK-004-ATLAS-V1-CAPSULE
EPISTEMIC STATUS: E

## Research Question

Can the project package the independently reviewed Stage 4 atlas v1
design/engine/raw/aggregate bundle into a local draft checkpoint capsule without
changing the scientific scope or upgrading public claims beyond the reviewed
artifact boundary?

## Primary Source

- `SRC-FBT-2021`
- Version of record: https://doi.org/10.1007/s10441-020-09400-0

The capsule packages project extension artifacts derived from source FBT decision
concepts. It is not a source theorem reproduction.

## Prior Inputs

- `TASK-004-FBT-ATLAS-V1-SPEC`
- `TASK-004-FBT-ATLAS-V1-ENGINE`
- `TASK-004-FBT-ATLAS-V1-AGGREGATE`
- `REV-TASK-004-FBT-ATLAS-V1-001_no_fatal_or_major`

## Expected Output

- `release/stage4-v1-draft/README.md`
- `release/stage4-v1-draft/CLAIMS.md`
- `release/stage4-v1-draft/LIMITATIONS.md`
- `release/stage4-v1-draft/ASSUMPTIONS.md`
- `release/stage4-v1-draft/REVIEW_REPORT.md`
- `release/stage4-v1-draft/reproduction_commands.md`
- `release/stage4-v1-draft/checksums.txt`
- `release/stage4-v1-draft/raw_data/`
- `release/stage4-v1-draft/derived_data/`
- `release/stage4-v1-draft/manifests/`
- `release/stage4-v1-draft/environment/`
- `release/stage4-v1-draft/figures/README.md`

## Included Artifact Types

- frozen atlas v1 draft config;
- manifest-backed exact raw-cell JSON artifact;
- manifest-backed aggregate JSON and Markdown report derived from the raw-cell JSON;
- raw and aggregate manifests;
- machine-readable checkpoint summary;
- review, limitations, assumptions, reproduction commands, and local checksums.

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
- `.venv\Scripts\python.exe -m fts_lab.cli validate-release-capsule release/stage4-v1-draft`
- `.venv\Scripts\python.exe -m fts_lab.cli doctor --release-check`
- `.venv\Scripts\python.exe -m pytest -p no:cacheprovider`
- `.venv\Scripts\python.exe -m ruff check . --no-cache`
- `.venv\Scripts\python.exe -m ruff format --check . --no-cache`
- `.venv\Scripts\python.exe -m mypy src`

## Claims Allowed

- The reviewed atlas v1 bundle can produce manifest-backed exact raw-cell tables
  and manifest-backed aggregate status-count/`grid_frequency` reports from saved
  raw artifacts only.
- This capsule archives one deterministic checkpoint of that reviewed bundle.
- The packaged aggregate values describe only the included raw-cell artifact.

## Claims Forbidden

- Do not claim a full finite atlas has been run.
- Do not claim Theorem 4 has been implemented, proved, reproduced, or reviewed.
- Do not treat project `grid_frequency` values as source theorem probabilities.
- Do not claim biological, real-perception, consciousness, spacetime, ontology,
  ML/RL, dashboard, notebook, figure, or evolutionary-dynamics results.

## Out Of Scope

- new atlas grid expansion;
- theorem implementation;
- stochastic simulation;
- figures, UI, dashboards, notebooks;
- new independent review;
- GitHub release, DOI archive, or external publication.
