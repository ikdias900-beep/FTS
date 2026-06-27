# TASK-003-P3-CAPSULE: Stage 3 FFF Structure Checkpoint Capsule

TASK ID: TASK-003-P3-CAPSULE
EPISTEMIC STATUS: R

## Research Question

Can the reviewed Stage 3 FFF permutation-group and measurable-space bundle be
packaged into a repository-local checkpoint capsule without adding new scientific
claims, calculations, figures, or implementation scope?

## Primary Source

- `SRC-FFF-2020`
- Version of record / open full text: https://www.mdpi.com/1099-4300/22/5/514
- Source locators:
  - `SRC-FFF-2020; version of record; Section 4, Permutation Groups Theorem`
  - `SRC-FFF-2020; version of record; Appendix A.1, Definitions A1-A4`
  - `SRC-FFF-2020; version of record; Appendix A.3, Permutation Groups Theorem`
  - `SRC-FFF-2020; version of record; Section 4, Measurable Structures Theorem`
  - `SRC-FFF-2020; version of record; Appendix A.5, Measurable Structure Theorem`

## Formal Definitions

This task packages definitions and implementation already completed by:

- `TASK-003-FFF-STRUCTURE-SPEC`
- `TASK-003-FFF-STRUCTURE-IMPL`

Canonical formal specs:

- `specs/fff/permutation_groups.md`
- `specs/fff/measurable_spaces.md`

## Input Domain

The capsule input domain is limited to the reviewed Stage 3 finite-helper scope:

- committed small-case fixtures in `tests/fixtures/fff/stage3_structure_spec_cases.json`;
- finite permutation/action-law helper examples covered by exact and property tests;
- finite partition-based measurable-space helper examples covered by exact and property
  tests.

No large symmetric-group enumeration, algebra-isomorphism sweep, stochastic run, figure,
or new experiment artifact is introduced.

## Expected Output

Create `release/stage3-p3-draft/` with:

- `README.md`;
- `CLAIMS.md`;
- `LIMITATIONS.md`;
- `ASSUMPTIONS.md`;
- `REVIEW_REPORT.md`;
- `environment/README.md`;
- `manifests/README.md`;
- `raw_data/stage3_structure_spec_cases.json`;
- `derived_data/stage3_fff_structure_checkpoint.json`;
- `derived_data/stage3_fff_structure_checkpoint.md`;
- `figures/README.md`;
- `reproduction_commands.md`;
- `checksums.txt`.

Update repository documentation and tests so the capsule is discoverable and validated
by `fts validate-release-capsule release/stage3-p3-draft`.

## Known Small Cases

Inherited from `TASK-003-FFF-STRUCTURE-SPEC` and
`TASK-003-FFF-STRUCTURE-IMPL`:

- source formula cases for `n = 5` and `n = 6`;
- action-law positive and negative permutation examples;
- nontrivial measurable partition examples;
- discrete/trivial measurable-space special cases;
- inverse-image non-measurability witness.

## Invariants

- The capsule must not change Stage 3 production code or scientific definitions.
- The capsule must not claim new theorem coverage beyond `CLM-FFF-PERM-001` and
  `CLM-FFF-MEAS-001`.
- The measurable-space source upper bound remains a bound, not a universal exact count.
- The permutation-group source construction remains distinct from ordinary group
  homomorphism enumeration.
- The capsule checksum inventory must list every committed capsule file except
  `checksums.txt`.

## Assumptions

No new approved scientific assumption is introduced.

Resolved assumptions used for the reviewed finite-helper scope:

- `ASM-FFF-0002`: `SOURCE_RESOLVED`
- `ASM-FFF-0003`: `SOURCE_RESOLVED`

## Tests Required Before Merge

- `py -m uv run ruff check .`
- `py -m uv run ruff format --check .`
- `py -m uv run mypy src`
- `py -m uv run pytest`
- `py -m uv run fts doctor --release-check`
- `py -m uv run fts validate-release-capsule release/stage3-p3-draft`

## Artifacts To Save

This task saves a checkpoint capsule, not a new generated scientific run.

Committed capsule files are:

- copied fixture input;
- release-local checkpoint summary JSON and Markdown;
- claims, limitations, assumptions, review summary, environment notes, reproduction
  commands, and checksum inventory.

## Claims Allowed

- The Stage 3 FFF permutation-group and measurable-space bundle has been packaged as a
  repository-local checkpoint capsule.
- The capsule links the reviewed Stage 3 finite-helper scope to source, claim,
  assumption, task, review, and checksum records.
- `CLM-FFF-PERM-001` and `CLM-FFF-MEAS-001` are already
  `implemented_reviewed` with no fatal or major review findings.

## Claims Forbidden

- Do not claim the capsule is a GitHub release, DOI archive, external publication, or
  final public P3 paper.
- Do not claim new scientific results beyond the already reviewed Stage 3 finite-helper
  scope.
- Do not claim the Appendix A.5 measurable upper bound is an exact count in all cases.
- Do not claim ordinary group-homomorphism enumeration implements the source
  permutation theorem.
- Do not claim anything about real perception, consciousness, spacetime, ontology,
  biology, ML/RL, or evolutionary dynamics.

## Out Of Scope

- new implementation modules;
- new FFF theorem families;
- FBT theorem/domain work;
- sweeps, generated figures, notebooks, UI, dashboards;
- GitHub release, tag, DOI, or archival deposit;
- independent review in this same implementation session.

