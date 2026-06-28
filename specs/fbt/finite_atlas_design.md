# FBT Finite Atlas Design Specification

TASK ID: `TASK-004-FBT-ATLAS-SPEC`  
EPISTEMIC STATUS: `R` for source-derived definitions; future atlas runs must label
their own results separately.  
SOURCE ID: `SRC-FBT-2021`  
CLAIM IDS: `CLM-FBT-THM-001`, `CLM-FBT-ATLAS-001`  
ASSUMPTION IDS: `ASM-FBT-0001`, `ASM-FBT-0002`, `ASM-FBT-0003`, `ASM-FBT-0004`

## Purpose

This document designs the future Stage 4 finite atlas without running it. The atlas is a
project-defined finite restriction of FBT-style Bayesian decision problems. It is useful
only if it keeps source-derived definitions separate from extension choices.

## Source-Derived Core

A finite FBT decision problem must specify:

- finite world states `W`;
- finite perceptual states `X`;
- a prior `mu(w)`;
- a perceptual kernel `p(x | w)` or explicitly pure perceptual map;
- a nonnegative fitness function over world states or a declared payoff object;
- one or more offered perceptual states/territories for comparison;
- a Truth strategy using source MAP estimates;
- a Fitness-only strategy using expected fitness.

The Stage 2 numerical appendix is one source example of this shape. Stage 4 must not
hard-code that example as the atlas.

## Project-Defined Extension Layer

The finite atlas will later define a grid over:

- cardinalities of `W` and `X`;
- rational priors;
- rational perceptual kernels;
- rational nonnegative fitness/payoff values;
- offered-choice sets;
- optional action sets only after a separate action-model specification.

The grid is a project object. Its cell counts and aggregate frequencies are not source
theorem probabilities.

## Strategy Families

### Source Strategy Family

The source-derived primary comparison is:

- `truth_map`: MAP point estimate followed by fitness ranking of the MAP world state;
- `fitness_only_expected`: posterior expected fitness ranking.

### Future Extension Baselines

The Stage 4 strategy document may later include extension baselines, each marked as
extension and reported separately:

- posterior sampling;
- posterior mean, only when `W` has an approved metric or vector structure;
- full-posterior decision baseline;
- regret-minimizing variants.

These variants must not be described as the source Truth strategy.

## Cell Identity

Every future atlas cell must have a stable ID derived from:

- grid version;
- `W` and `X` cardinalities;
- prior grid ID;
- kernel grid ID;
- fitness/payoff grid ID;
- offered-choice-set ID;
- strategy family ID;
- tie/zero-marginal policy ID.

The ID scheme must be deterministic before the first atlas run.

## Required Raw Outputs For Future Runs

Each evaluated cell must record:

- task IDs;
- source IDs;
- claim IDs;
- assumption IDs;
- grid version and cell ID;
- exact rational inputs;
- exact rational outputs;
- strategy decisions;
- tie flags;
- zero-marginal flags;
- strict dominance, reverse dominance, equality, or blocked status;
- command, commit, dependency-lock checksum, and manifest checksum.

## Aggregate Statistics

Aggregate statistics may be reported only after raw cell results are saved. Aggregates
must keep separate:

- source MAP Truth versus extension truth baselines;
- pure maps versus noisy kernels;
- grid frequencies versus theorem probabilities;
- ties and blocked cells;
- confirmatory metrics versus exploratory summaries.

## Blockers Before Production Implementation

- Human PI decision for `ASM-FBT-0001`.
- Human PI decision for `ASM-FBT-0002`.
- Human PI decision for `ASM-FBT-0003`.
- Human PI decision for `ASM-FBT-0004`.
- Independent review of this specification bundle.

## Out Of Scope For This Spec Gate

- atlas engine;
- grid enumeration;
- manifests for atlas runs;
- figures;
- UI;
- evolutionary dynamics;
- ML/RL.

