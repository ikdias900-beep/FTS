# Stage 3 P3 Draft Checkpoint Capsule

```text
CAPSULE ID: STAGE3-P3-DRAFT
TASK ID: TASK-003-P3-CAPSULE
STATUS: draft checkpoint capsule, based on independently reviewed Stage 3 bundle
LICENSE: MIT for project-authored repository contents
SCIENTIFIC CLAIMS ADDED: none
SCIENTIFIC CLAIMS PACKAGED: CLM-FFF-PERM-001; CLM-FFF-MEAS-001
```

## Scope

This capsule packages the reviewed Stage 3 FFF structure bundle for permutation groups
and measurable spaces. It is a repository-local checkpoint package, not a GitHub
release, DOI archive, external publication, or final public P3 paper.

It includes:

- the reviewed Stage 3 small-case fixture copied from
  `tests/fixtures/fff/stage3_structure_spec_cases.json`;
- a machine-readable checkpoint summary;
- a human-readable checkpoint summary;
- claims, limitations, assumptions, review status, environment notes, reproduction
  commands, and checksums.

The package references the already reviewed specs, source modules, and tests in the
repository. It does not introduce new calculations, new scientific claims, new figures,
new sweeps, notebooks, dashboards, ML/RL work, evolutionary dynamics, or FBT theorem
work.

## Packaging State

The capsule was assembled from the reviewed Stage 3 closeout commit:

```text
git_commit=e917ce0c63435316d12fedfd7bc48332cf016689
git_branch=main
git_dirty=false
dependency_lock_sha256=6b81fceadcb3fe17172ce56a239b581332675e7045058459a5871f2982e609c8
```

## Included Review IDs

- Stage 3 independent review: `REV-TASK-003-FFF-STRUCTURE-001`
- Stage 3 follow-up: `REV-TASK-003-FFF-STRUCTURE-001-followup`

`REV-TASK-003-FFF-STRUCTURE-001` accepted the Stage 3 specs, fixtures,
implementation, and tests with minor findings only. There are no unresolved fatal or
major findings.

## Directory Map

```text
release/stage3-p3-draft/
├── README.md
├── CLAIMS.md
├── LIMITATIONS.md
├── ASSUMPTIONS.md
├── REVIEW_REPORT.md
├── environment/
├── manifests/
├── raw_data/
├── derived_data/
├── figures/
├── reproduction_commands.md
└── checksums.txt
```

## Local Validation

Validate the committed capsule archive with:

```bash
py -m uv run fts validate-release-capsule release/stage3-p3-draft
```

The validator checks the local `checksums.txt` inventory and does not require internet
access.

