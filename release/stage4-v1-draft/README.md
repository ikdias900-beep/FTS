# Stage 4 Atlas v1 Draft Checkpoint Capsule

```text
CAPSULE ID: STAGE4-V1-DRAFT
TASK ID: TASK-004-ATLAS-V1-CAPSULE
STATUS: draft checkpoint capsule, based on independently reviewed atlas v1 bundle
LICENSE: MIT for project-authored repository contents
SCIENTIFIC CLAIMS ADDED: none
SCIENTIFIC CLAIMS PACKAGED: CLM-FBT-ATLAS-001
```

## Scope

This capsule packages the reviewed Stage 4 atlas v1 design/engine/raw/aggregate
bundle. It is a repository-local checkpoint package, not a GitHub release, DOI
archive, external publication, or final public Stage 4 paper.

It includes:

- the frozen atlas v1 draft config copied from
  `experiments/configs/fbt_atlas_v1_draft.json`;
- one deterministic exact raw-cell JSON artifact;
- one aggregate JSON and Markdown report derived from the saved raw-cell artifact;
- raw and aggregate manifests;
- a machine-readable checkpoint summary;
- claims, limitations, assumptions, review status, environment notes, reproduction
  commands, and checksums.

The package references the reviewed specs, source modules, and tests in the
repository. It does not introduce a full atlas, Theorem 4 implementation, theorem
probability, biological claim, metaphysical claim, figure, notebook, dashboard, ML/RL
work, or stochastic simulation.

## Packaging State

The packaged artifacts were produced from a clean repository state:

```text
git_commit=4a015ca85aed88cecab0c4cda82a384b530ff3a9
git_branch=codex/stage4-atlas-v1-capsule
git_dirty=false
dependency_lock_sha256=6b81fceadcb3fe17172ce56a239b581332675e7045058459a5871f2982e609c8
```

The implementation bundle reviewed by the independent verifier was commit:

```text
reviewed_commit=8e7399a32029a5726420df82318ae0b141e96e7b
review_id=REV-TASK-004-FBT-ATLAS-V1-001
review_status_token=REV-TASK-004-FBT-ATLAS-V1-001_no_fatal_or_major
```

## Included Artifact IDs

- raw-cell run:
  `EXP-TASK-004-FBT-ATLAS-V1-RAW-CELLS-20260702T080919Z-0AE3BB9C`
- raw-cell manifest:
  `ART-TASK-004-FBT-ATLAS-V1-RAW-CELLS-MANIFEST-20260702T080919Z-0AE3BB9C`
- aggregate run:
  `EXP-TASK-004-FBT-ATLAS-V1-AGGREGATE-20260702T080924Z-1A6A67BF`
- aggregate manifest:
  `ART-TASK-004-FBT-ATLAS-V1-AGGREGATE-MANIFEST-20260702T080924Z-1A6A67BF`

The copied manifests are the original run records and retain their original absolute
paths. The archived copies in this capsule are verified by `checksums.txt`.

## Included Review IDs

- Stage 4 atlas v1 independent review: `REV-TASK-004-FBT-ATLAS-V1-001`

`REV-TASK-004-FBT-ATLAS-V1-001` accepted the atlas v1 design, raw-cell engine, raw
artifacts, aggregate/report layer, tests, and manifest discipline with no fatal,
major, or minor findings.

## Directory Map

```text
release/stage4-v1-draft/
|-- README.md
|-- CLAIMS.md
|-- LIMITATIONS.md
|-- ASSUMPTIONS.md
|-- REVIEW_REPORT.md
|-- environment/
|-- manifests/
|-- raw_data/
|-- derived_data/
|-- figures/
|-- reproduction_commands.md
`-- checksums.txt
```

## Local Validation

Validate the committed capsule archive with:

```bash
py -m uv run fts validate-release-capsule release/stage4-v1-draft
```

Or, in the local Windows virtual environment used by this repository:

```powershell
.\.venv\Scripts\python.exe -m fts_lab.cli validate-release-capsule release/stage4-v1-draft
```

The validator checks the local `checksums.txt` inventory and does not require internet
access.
