# Stage 4 P4 Draft Checkpoint Capsule

```text
CAPSULE ID: STAGE4-P4-DRAFT
TASK ID: TASK-004-P4-CAPSULE
STATUS: draft checkpoint capsule, based on independently reviewed Stage 4 bundle
LICENSE: MIT for project-authored repository contents
SCIENTIFIC CLAIMS ADDED: none
SCIENTIFIC CLAIMS PACKAGED: CLM-FBT-ATLAS-001
```

## Scope

This capsule packages the reviewed Stage 4 FBT finite-atlas spec/oracle/grid-smoke
bundle. It is a repository-local checkpoint package, not a GitHub release, DOI archive,
external publication, or final public Stage 4 paper.

It includes:

- Stage 4 source/spec fixture cases copied from
  `tests/fixtures/fbt/stage4_fbt_spec_cases.json`;
- Stage 4 oracle fixture cases copied from
  `tests/fixtures/fbt/stage4_fbt_oracle_cases.json`;
- the frozen `fbt_atlas_v0` config copied from `experiments/configs/fbt_atlas_v0.json`;
- a deterministic generated `fbt_atlas_v0` smoke JSON result and Markdown report;
- the original smoke-run manifest;
- a machine-readable checkpoint summary;
- claims, limitations, assumptions, review status, environment notes, reproduction
  commands, and checksums.

The package references the already reviewed specs, source modules, and tests in the
repository. It does not introduce a full atlas, Theorem 4 implementation, theorem
probability, biological claim, metaphysical claim, figure, notebook, dashboard, ML/RL
work, or stochastic simulation.

## Packaging State

The grid-smoke artifacts were produced from a clean repository state:

```text
git_commit=ed55ba337b8d3f03f80b12bfd7c566ce47ae57a6
git_branch=codex/stage4-p4-capsule
git_dirty=false
dependency_lock_sha256=6b81fceadcb3fe17172ce56a239b581332675e7045058459a5871f2982e609c8
```

## Included Artifact IDs

- FBT atlas grid v0 manifest:
  `ART-TASK-004-FBT-ATLAS-GRID-V0-MANIFEST-20260702T063659Z-58A56618`
- FBT atlas grid v0 run:
  `EXP-TASK-004-FBT-ATLAS-GRID-V0-20260702T063659Z-58A56618`

The copied manifest is the original run record and retains its original absolute paths.
The archived copies in this capsule are verified by `checksums.txt`.

## Included Review IDs

- Stage 4 independent review: `REV-TASK-004-FBT-ATLAS-001`

`REV-TASK-004-FBT-ATLAS-001` accepted the Stage 4 specs, finite-cell oracle,
grid-smoke runner, tests, and manifest discipline with no fatal, major, or minor
findings.

## Directory Map

```text
release/stage4-p4-draft/
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
py -m uv run fts validate-release-capsule release/stage4-p4-draft
```

The validator checks the local `checksums.txt` inventory and does not require internet
access.
