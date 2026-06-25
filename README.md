# Fitness, Truth & Structure Lab

Auditable computational research program around FBT, FFF, and later structure/reward/robustness questions.

Current status: `TASK-001-PUBTABLES` is accepted with minor findings after independent review. `TASK-000` bootstrap, `TASK-001` exact core, `TASK-001-SWEEP`, and Stage 1 publication-table documentation are complete through independent review. The repository now provides infrastructure plus Stage 1 exact finite helpers for FFF admissible payoff counts, total orders, cyclic groups, and manifest-backed publication table generation. It does not implement FBT, evolutionary dynamics, ML, dashboards, notebooks, or scientific figures.

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
- [Current Stage 1 publication tables task](tasks/TASK-001_publication_tables_docs.md)
- [Stage 1 publication table note](docs/research_notes/stage1_publication_tables.md)
- [Source map](sources/source_map.md)
- [Claim matrix](sources/claim_matrix.csv)
- [Assumption register](assumptions/register.md)
- [Reproducibility contract](docs/reproducibility.md)

## Release Blockers

No final software license has been selected. See [RDR-0001-license](docs/decisions/RDR-0001-license.md). Public release remains blocked until the Human Principal Investigator approves a license.
