# Fitness, Truth & Structure Lab

Auditable computational research program around FBT, FFF, and later structure/reward/robustness questions.

Current status: `TASK-003-FFF-STRUCTURE-IMPL` is complete as a Stage 3 implementation
bundle for FFF permutation groups and measurable spaces, with independent review
accepted with minor findings and follow-up cleanup completed. A repository-local Stage
3 P3 draft checkpoint capsule is available under `release/stage3-p3-draft/`.
`TASK-004-FBT-ATLAS-SPEC` has started as a Stage 4 spec gate only.
`TASK-002-FBT-NUMERICAL` is complete
through independent review with minor findings only; `TASK-000` bootstrap,
`TASK-001` exact core, `TASK-001-SWEEP`, `TASK-001-PUBTABLES`, and the Stage 1 draft
release capsule are also complete through independent review. The repository now
provides infrastructure, Stage 1 exact finite helpers for FFF admissible payoff counts,
total orders, cyclic groups, manifest-backed publication table generation, a draft Stage
1 release capsule, exact FBT numerical appendix reproduction, an independently reviewed
draft Stage 2 checkpoint capsule, draft Stage 3 source-transcription specs, and
reviewed Stage 3 finite validators for permutation/measurable structures. It also
includes a draft Stage 3 checkpoint capsule. It does not
provide FBT evolutionary dynamics, the general FBT
theorem implementation, finite FBT atlas runs, ML, dashboards, notebooks, or scientific
figures.

This project does not prove Hoffman's metaphysical proposals. Future scientific claims must be tied to source IDs, claim IDs, assumptions, manifests, tests, and independent review.

## Install

The reference runtime is Python `>=3.12,<3.13` managed by `uv`.

```bash
uv sync --all-groups
```

On Windows, if `uv` is installed but not on `PATH`, the same commands can usually be run as `py -m uv ...`.

`jsonschema` is the only runtime dependency because `fts validate-manifest` validates machine-readable experiment manifests against `experiments/schemas/experiment_manifest.schema.json`. Test, lint, typing, and pre-commit tools are development dependencies.

## Quality Commands

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
uv run fts doctor
uv run fts reproduce-smoke
uv run fts fbt reproduce-numerical-example
uv run fts validate-release-capsule release/stage2-p2-draft
uv run fts validate-release-capsule release/stage3-p3-draft
```

Equivalent Make targets are available:

```bash
make install
make quality
```

## Smoke Reproduction

Run:

```bash
uv run fts reproduce-smoke
```

The command reads `experiments/configs/smoke.json`, writes an immutable payload under `results/raw/`, writes a manifest under `experiments/manifests/`, validates the manifest, and prints the payload checksum.

Validate a manifest later:

```bash
uv run fts validate-manifest experiments/manifests/<manifest>.json
```

Two runs from the same config should produce the same payload checksum. Manifest timestamps, run IDs, absolute paths, and environment metadata may differ.

## Stage 1 Exact Helpers

Run small exact FFF counts:

```bash
uv run fts fff admissible-count 2 2
uv run fts fff total-order-count 2 2
uv run fts fff total-order-count 2 2 --mode unique
uv run fts fff cyclic-count 2 2
uv run fts fff cyclic-count 2 2 --admissible-only
uv run fts fff sweep --config experiments/configs/fff_stage1_small.json
```

The total-order helper intentionally separates the source orientation-witness count from the distinct unique-function count. `RDR-0002` records the Human PI decision to show both values in Stage 1 outputs.

Build derived publication tables after a sweep:

```bash
uv run fts fff publication-tables --sweep-manifest experiments/manifests/<sweep-manifest>.json
```

The derived package writes a wide CSV under `results/derived/`, a Markdown report under `results/reports/`, and a manifest under `experiments/manifests/`.

## Stage 2 FBT Numerical Appendix

Reproduce the FBT numerical appendix with exact rational arithmetic:

```bash
uv run fts fbt reproduce-numerical-example
```

The command reads `experiments/configs/fbt_numerical_example.json`, computes
marginals, posteriors, unique MAP estimates, expected-fitness values, writes a JSON
result and Markdown derivation report, then validates a scientific manifest with
`epistemic_status: R`. This is a reproduction of one appendix example only; it is not an
evolutionary simulation or a proof of the general FBT theorem.

The current checkpoint package is under `release/stage2-p2-draft/`. Validate the
committed archive contents with:

```bash
uv run fts validate-release-capsule release/stage2-p2-draft
```

`REV-TASK-002-FBT-NUMERICAL-001` accepted the Stage 2 reproduction with minor
findings only. No fatal or major findings block the Stage 2 checkpoint. The
packaging portability follow-up is the release-capsule checksum validator above;
it verifies the archived files without depending on original absolute manifest paths.

## Stage 3 FFF Structure Implementation

Stage 3 has moved from a specification gate into an independently reviewed implementation
bundle:

```text
TASK-003-FFF-STRUCTURE-IMPL
```

The draft specs are:

- `specs/fff/permutation_groups.md`
- `specs/fff/measurable_spaces.md`

The implementation helpers are:

- `src/fts_lab/fff/permutation_groups.py`
- `src/fts_lab/fff/measurable_spaces.py`

The fixture and tests are:

- `tests/fixtures/fff/stage3_structure_spec_cases.json`
- `tests/exact/test_fff_stage3_spec_gate.py`
- `tests/exact/test_fff_permutation_groups.py`
- `tests/exact/test_fff_measurable_spaces.py`

`CLM-FFF-PERM-001` and `CLM-FFF-MEAS-001` are `implemented_reviewed`, with review
status `REV-TASK-003-FFF-STRUCTURE-001_no_fatal_or_major`. `ASM-FFF-0002` and
`ASM-FFF-0003` are `SOURCE_RESOLVED` for the reviewed Stage 3 finite-helper scope after
Human PI status acceptance. The measurable-space bound is not treated as an exact count.

The Stage 3 checkpoint package is under `release/stage3-p3-draft/`. Validate the
committed archive contents with:

```bash
uv run fts validate-release-capsule release/stage3-p3-draft
```

This capsule packages the already reviewed Stage 3 bundle. It adds no new scientific
claims, generated figures, sweeps, or public release status.

## Stage 4 FBT Finite Atlas Spec Gate

Stage 4 has started as a spec gate:

```text
TASK-004-FBT-ATLAS-SPEC
```

The current Stage 4 outputs are draft specs and fixture checks only:

- `specs/fbt/theorem4_domain.md`
- `specs/fbt/finite_atlas_design.md`
- `tests/fixtures/fbt/stage4_fbt_spec_cases.json`
- `tests/exact/test_fbt_stage4_spec_gate.py`

No finite atlas engine, sweeps, generated atlas artifacts, figures, or theorem
implementation have been added.

## Epistemic Status

Scientific artifacts must use exactly one status:

- `R` - reproduction from a published source;
- `C` - computational reconstruction with registered assumptions;
- `E` - extension beyond the source;
- `A` - analogy to another domain.

Infrastructure smoke artifacts use `epistemic_status: null`, `claim_ids: []`, and `artifact_kind: infrastructure_smoke`.

## Project Context

- [Research strategy](01_research_strategy.md)
- [Stage tasks and roles](02_stage_tasks_roles.md)
- [Repository instructions](AGENTS.md)
- [Bootstrap task](tasks/TASK-000_bootstrap_repo.md)
- [Stage 1 core task](tasks/TASK-001_fff_core_orders_cyclic.md)
- [Stage 1 sweep task](tasks/TASK-001_stage1_sweeps_tables.md)
- [Stage 1 publication tables task](tasks/TASK-001_publication_tables_docs.md)
- [Stage 1 draft release capsule task](tasks/TASK-001_p1_release_capsule.md)
- [Stage 2 FBT numerical appendix task](tasks/TASK-002_fbt_numerical_appendix.md)
- [Stage 3 FFF structure spec task](tasks/TASK-003_fff_structure_spec.md)
- [Stage 3 FFF structure implementation task](tasks/TASK-003_fff_structure_impl.md)
- [Stage 3 P3 checkpoint capsule task](tasks/TASK-003_p3_release_capsule.md)
- [Stage 4 FBT finite atlas spec task](tasks/TASK-004_fbt_finite_atlas_spec.md)
- [Stage 2 FBT numerical appendix spec](specs/fbt/numerical_appendix.md)
- [Stage 4 FBT theorem-domain spec](specs/fbt/theorem4_domain.md)
- [Stage 4 FBT finite-atlas design spec](specs/fbt/finite_atlas_design.md)
- [Stage 3 permutation-group spec](specs/fff/permutation_groups.md)
- [Stage 3 measurable-space spec](specs/fff/measurable_spaces.md)
- [Stage 2 draft checkpoint capsule](release/stage2-p2-draft/README.md)
- [Stage 3 draft checkpoint capsule](release/stage3-p3-draft/README.md)
- [Stage 1 publication table note](docs/research_notes/stage1_publication_tables.md)
- [Stage 2 FBT numerical appendix note](docs/research_notes/stage2_fbt_numerical_appendix.md)
- [Stage 2 batched review bundle](docs/reviews/TASK-002-FBT-NUMERICAL-batched-review-bundle.md)
- [Stage 2 independent review brief](docs/reviews/TASK-002-FBT-NUMERICAL-independent-review-brief.md)
- [Stage 2 independent review report](docs/reviews/REV-TASK-002-FBT-NUMERICAL-001.md)
- [Stage 2 review follow-up](docs/reviews/REV-TASK-002-FBT-NUMERICAL-001-followup.md)
- [Source map](sources/source_map.md)
- [Claim matrix](sources/claim_matrix.csv)
- [Assumption register](assumptions/register.md)
- [Reproducibility contract](docs/reproducibility.md)

## License

Project-authored repository contents are released under the MIT License. See [LICENSE](LICENSE) and [RDR-0001-license](docs/decisions/RDR-0001-license.md). External sources and third-party dependencies keep their own terms.
