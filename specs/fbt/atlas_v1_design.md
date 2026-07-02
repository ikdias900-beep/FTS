# FBT Atlas v1 Design Specification

TASK ID: `TASK-004-FBT-ATLAS-V1-SPEC`  
EPISTEMIC STATUS: `E`  
SOURCE ID: `SRC-FBT-2021`  
CLAIM ID: `CLM-FBT-ATLAS-001`  
ASSUMPTION IDS: `ASM-FBT-0001`, `ASM-FBT-0002`, `ASM-FBT-0003`, `ASM-FBT-0004`

## Purpose

Atlas v1 is the next Stage 4 block after the reviewed spec/oracle/grid-smoke
checkpoint. This document freezes design expectations for a reusable raw-cell engine.
It is not a run plan for a large public result and it does not add a new public
scientific claim.

## Scope

The first v1 deliverable was a spec gate:

- a draft config contract;
- stable cell identity requirements;
- denominator and edge-case semantics;
- tests that reject claim-boundary drift.

`TASK-004-FBT-ATLAS-V1-ENGINE` implements the first production path: a
manifest-backed raw-cell table. `TASK-004-FBT-ATLAS-V1-AGGREGATE` adds a derived
aggregate/report layer that consumes those raw-cell artifacts. Public claim upgrades
still come later.

## Source-Derived Core

Atlas v1 cells remain finite FBT-style Bayesian decision problems with:

- finite world states;
- finite perceptual states;
- exact rational priors;
- exact rational perceptual kernels;
- exact rational nonnegative fitness values;
- offered perceptual states for comparison.

The source-derived primary comparison remains:

- `truth_map`: MAP point estimate followed by fitness ranking of MAP world states;
- `fitness_only_expected`: posterior expected-fitness ranking.

## Extension Boundary

Atlas v1 is a project extension. It may explore a finite rational grid, but the grid is
not the source theorem domain.

Extension baselines such as posterior sampling, posterior mean, or full-posterior
decision rules are out of the primary comparison. They require separate config fields,
separate result columns, and a later task before use.

## Draft Grid Identity

Every future v1 raw cell must have a deterministic identity derived from:

- `grid_version`;
- world-state count;
- perceptual-state count;
- prior family ID;
- kernel family ID;
- fitness family ID;
- offered-observation-set ID;
- primary-comparison ID;
- edge-policy ID.

The draft config records this identity contract and the first engine enumerates exact
raw cells over the declared representative families. This is still not a full public
atlas result.

## Draft Representative Families

The v1 draft config declares representative project families:

- priors: `uniform`, `single_state_heavy`, `rational_simplex_small`;
- kernels: `pure_map`, `noisy_map`, `uninformative`, `zero_marginal_probe`;
- fitness functions: `single_peak`, `equal`, `multi_peak`;
- offered-observation sets: `all_observations`.

These families are deterministic project grid choices. They are not claimed to exhaust
the source theorem domain.

## Arithmetic And Denominator Semantics

The reference path is exact rational enumeration. Approximate or stochastic paths are
out of scope for the spec gate.

All primary summaries must use:

- `aggregate_label: grid_frequency`;
- `denominator_policy: all_enumerated_cells`;
- blocked and tie-sensitive cells included in the denominator.

This keeps `blocked_zero_marginal` and `map_tie_policy_sensitive` visible instead of
silently removing them from the summary base.

## Manifest Discipline

The v1 raw-cell engine writes a raw cell artifact and a manifest that records:

- task IDs;
- claim IDs;
- source IDs;
- assumption IDs;
- grid version;
- config checksum;
- command;
- git commit and dirty state;
- dependency-lock checksum;
- output paths and checksums.

The raw-cell engine writes manifests. Later aggregate/report commands must consume raw
cell artifacts rather than recomputing hidden cells.

## Raw-Cell Engine

`TASK-004-FBT-ATLAS-V1-ENGINE` adds:

- module: `src/fts_lab/fbt/atlas_v1.py`;
- CLI: `fts fbt atlas-v1-raw-cells`;
- output: `results/raw/<run_id>/fbt_atlas_v1_raw_cells.json`;
- manifest: `experiments/manifests/<manifest_id>.json`.

The engine reads `experiments/configs/fbt_atlas_v1_draft.json`, expands deterministic
representative families into exact finite cells, evaluates each cell through the
reviewed Stage 4 finite-cell oracle, and saves the raw table. It does not compute
aggregate frequencies.

## Aggregate/Report Layer

`TASK-004-FBT-ATLAS-V1-AGGREGATE` adds:

- module: `src/fts_lab/fbt/atlas_v1_aggregate.py`;
- CLI: `fts fbt atlas-v1-aggregate --raw-cells <path>`;
- output: `results/derived/<run_id>/fbt_atlas_v1_aggregate.json`;
- report: `results/reports/<run_id>/fbt_atlas_v1_report.md`;
- manifest: `experiments/manifests/<manifest_id>.json`.

The aggregate command accepts a saved `fbt_atlas_v1_raw_cell_table` JSON artifact as
its only scientific input. It validates that artifact, counts `cells[*].status`, and
writes exact rational `grid_frequency` summaries over all raw cells in the input.

The aggregate command must not read `experiments/configs/fbt_atlas_v1_draft.json`,
must not regenerate cells, and must not import the raw-cell enumeration helpers. This
preserves the raw/derived boundary: raw artifacts are the auditable data source, while
reports are reproducible summaries of those artifacts.

The denominator semantics remain:

- `aggregate_label: grid_frequency`;
- `denominator_policy: all_enumerated_cells`;
- `denominator_basis: all_raw_cells`;
- blocked and tie-sensitive cells stay in the denominator.

## Forbidden For The Spec Gate

- full atlas run;
- aggregate result publication;
- Theorem 4 implementation;
- stochastic simulation;
- ML/RL;
- UI, dashboard, notebook, or figure generation;
- biological or metaphysical interpretation.

## Acceptance

This engine gate is complete when:

- `experiments/configs/fbt_atlas_v1_draft.json` links the required traceability IDs;
- tests validate primary comparison, grid identity, exact arithmetic, and denominator
  semantics;
- tests verify that draft config wording cannot be mistaken for a source-level
  probability claim;
- the raw-cell CLI writes a manifest-backed raw-cell table;
- the aggregate CLI writes derived JSON/Markdown reports from a raw-cell artifact
  without hidden recomputation.
