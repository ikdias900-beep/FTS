# Stage 1 Publication Tables

```text
TASK ID: TASK-001-PUBTABLES
STAGE: 1 - FFF total orders and cyclic groups
STATUS: documentation for manifest-backed derived tables
SCIENTIFIC CLAIMS ADDED: none
```

## Purpose

This note explains how to build publication-oriented Stage 1 tables from the reviewed finite-count sweep. It does not introduce new mathematical definitions, new assumptions, plots, notebooks, or public claims.

The publication table package is derived from a validated `TASK-001-SWEEP` manifest. The generated artifacts are:

- a wide exact CSV under `results/derived/<run_id>/stage1_fff_publication_counts.csv`;
- a human-readable Markdown report under `results/reports/<run_id>/stage1_fff_publication_tables.md`;
- a manifest under `experiments/manifests/<manifest_id>.json`.

Generated result artifacts are intentionally not committed by default. Reproduce them from the commands below.

## Reproduction Commands

First generate the reviewed sweep artifact:

```bash
uv run fts fff sweep --config experiments/configs/fff_stage1_small.json
```

Then pass the printed `manifest_path` to the publication table command:

```bash
uv run fts fff publication-tables --sweep-manifest experiments/manifests/<sweep-manifest>.json
```

Validate the derived manifest:

```bash
uv run fts validate-manifest experiments/manifests/<publication-manifest>.json
```

On Windows, if bare `uv` is not available on `PATH`, use:

```bash
py -m uv run fts fff sweep --config experiments/configs/fff_stage1_small.json
py -m uv run fts fff publication-tables --sweep-manifest experiments/manifests/<sweep-manifest>.json
py -m uv run fts validate-manifest experiments/manifests/<publication-manifest>.json
```

## Traceability

The derived publication package is linked to:

- `TASK-001-PUBTABLES`;
- `SRC-FFF-2020`;
- `CLM-FFF-ADM-001`;
- `CLM-FFF-ORD-001`;
- `CLM-FFF-CYC-001`;
- `CLM-FFF-CYC-002`;
- `ASM-FFF-0001`;
- `RDR-0002`.

The derived manifest also records the source sweep manifest path, source sweep run ID, source sweep manifest ID, input checksums, output checksums, current Git state, and `uv.lock` checksum.

## Column Statuses

The wide CSV aggregates several source rows into one row per `(n,m)` pair. To avoid mixing epistemic statuses silently, each value group has an explicit status column:

- admissible payoff-function count: `R`;
- total-order source orientation-witness count and ratio: `R`;
- total-order distinct unique-function count and ratio: `C`;
- cyclic source homomorphism count and ratio: `R`.

The `C` columns are the approved `RDR-0002` presentation companion required by `ASM-FFF-0001`; they are not a replacement for the source orientation-witness count.

## Allowed Claims

- For the declared finite grid, the package reports exact integer counts and exact rational ratios.
- The table separates source orientation-witness total-order counts from distinct unique-function companion counts.
- The table is derived from a reviewed sweep artifact and is reproducible through a manifest.

## Forbidden Claims

- Do not claim the finite grid is an empirical distribution over biological payoff functions.
- Do not claim the result proves anything about human perception, consciousness, spacetime, or ontology.
- Do not present the total-order source orientation-witness count as the distinct unique-function count.
- Do not use this package as evidence for permutation groups, measurable spaces, FBT, evolutionary dynamics, ML/RL, or any future stage.

## Review State

`REV-TASK-001-SWEEP-001` accepted the source sweep with minor findings only. No fatal or major findings block `TASK-001-SWEEP`.

`TASK-001-PUBTABLES` still requires its own fresh-context review before a P1 release package.
