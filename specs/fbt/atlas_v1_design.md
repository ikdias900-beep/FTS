# FBT Atlas v1 Design Specification

TASK ID: `TASK-004-FBT-ATLAS-V1-SPEC`  
EPISTEMIC STATUS: `E`  
SOURCE ID: `SRC-FBT-2021`  
CLAIM ID: `CLM-FBT-ATLAS-001`  
ASSUMPTION IDS: `ASM-FBT-0001`, `ASM-FBT-0002`, `ASM-FBT-0003`, `ASM-FBT-0004`

## Purpose

Atlas v1 is the next Stage 4 block after the reviewed spec/oracle/grid-smoke
checkpoint. This document freezes design expectations before a reusable engine is
implemented. It is not a run plan for a large result and it does not add a new public
scientific claim.

## Scope

The first v1 deliverable is a spec gate:

- a draft config contract;
- stable cell identity requirements;
- denominator and edge-case semantics;
- tests that reject claim-boundary drift.

Production implementation comes later only after this contract is stable.

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

The draft config records this identity contract but does not enumerate the full v1 grid.

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

Before any v1 aggregate is publishable, the engine must write raw cell artifacts and a
manifest that records:

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

The spec gate does not write v1 manifests.

## Forbidden For The Spec Gate

- full atlas run;
- reusable production engine;
- aggregate result publication;
- Theorem 4 implementation;
- stochastic simulation;
- ML/RL;
- UI, dashboard, notebook, or figure generation;
- biological or metaphysical interpretation.

## Acceptance

This spec gate is complete when:

- `experiments/configs/fbt_atlas_v1_draft.json` links the required traceability IDs;
- tests validate primary comparison, grid identity, exact arithmetic, and denominator
  semantics;
- tests verify that draft config wording cannot be mistaken for a source-level
  probability claim.
