# TASK-004-FBT-ATLAS-SPEC: Stage 4 FBT Finite Atlas Spec Gate

TASK ID: TASK-004-FBT-ATLAS-SPEC
EPISTEMIC STATUS: R

## Research Question

Can the `SRC-FBT-2021` theorem-domain assumptions, strategy definitions, and future
finite-atlas boundaries be transcribed into implementation-ready specifications without
yet implementing the production atlas, running sweeps, or upgrading public claims?

## Primary Source

- `SRC-FBT-2021`
- Canonical DOI: https://doi.org/10.1007/s10441-020-09400-0
- Open author manuscript used for source transcription:
  https://sites.socsci.uci.edu/~ddhoff/FitnessBeatsTruth_apa_PBR.pdf
- Source locators:
  - `SRC-FBT-2021; author manuscript; Mathematical Background for the Main Theorem`
  - `SRC-FBT-2021; author manuscript; General Perceptual Mappings and Bayesian Inference`
  - `SRC-FBT-2021; author manuscript; Expected Fitness`
  - `SRC-FBT-2021; author manuscript; Two Perceptual Strategies`
  - `SRC-FBT-2021; author manuscript; Theorem 4, “The Fitness Beats Truth” Theorem`
  - `SRC-FBT-2021; version of record; Appendix: Calculations for the Numerical Example in Table 1`

## Formal Definitions

This task creates specifications only:

- `specs/fbt/theorem4_domain.md`
- `specs/fbt/finite_atlas_design.md`

The theorem-domain spec must distinguish:

- world space `W` and perceptual space `X`;
- pure perceptual maps from general Markov kernels;
- priors and posteriors;
- MAP point estimates and non-unique MAP ties;
- expected fitness;
- source Truth strategy;
- source Fitness-only strategy;
- source lower-bound expression `(abs(X) - 3) / (abs(X) - 1)`;
- theorem probability/measure language versus future finite-grid atlas counts.

The finite-atlas design spec must distinguish:

- source-derived decision-problem definitions;
- future project-defined finite rational grids;
- grid cell counts versus source theorem probabilities;
- source MAP Truth from future extension baselines;
- exact raw cell evaluation from aggregate summary statistics.

## Input Domain

Committed spec fixtures are limited to small declaration checks in:

- `tests/fixtures/fbt/stage4_fbt_spec_cases.json`

These fixtures are not generated scientific results. They are design fixtures for future
implementation and review.

## Expected Output

- Stage 4 task brief;
- theorem-domain spec;
- finite-atlas design spec;
- small fixture data for theorem-bound arithmetic and atlas-design boundaries;
- tests that validate fixture internal consistency without importing future production
  Stage 4 implementation;
- registry/documentation updates showing Stage 4 is at spec-gate status only.

## Known Small Cases

Theorem-bound arithmetic:

- `abs(X) = 3`: lower bound `0`;
- `abs(X) = 4`: lower bound `1/3`;
- `abs(X) = 5`: lower bound `1/2`;
- `abs(X) = 10`: lower bound `7/9`.

The fixture also records that same-best-territory probability is the complement
`2 / (abs(X) - 1)` for these design checks.

## Invariants

- No production module `src/fts_lab/fbt/theorem4.py` or
  `src/fts_lab/fbt/finite_atlas.py` is created in this task.
- Tests for this task must not import future production Stage 4 code.
- The source theorem probability must not be equated with a project finite-grid count.
- `ASM-FBT-0001` and `ASM-FBT-0002` remain open and block general production behavior.
- New Stage 4 atlas design decisions remain open until Human PI approval.

## Assumptions

No new approved scientific assumption is introduced.

Open assumptions acknowledged and not resolved:

- `ASM-FBT-0001`: general MAP tie handling.
- `ASM-FBT-0002`: zero-probability observation behavior.
- `ASM-FBT-0003`: finite-atlas grid and measure semantics.
- `ASM-FBT-0004`: truth-strategy family and primary comparison policy.

## Tests Required Before Merge

- fixture-internal consistency tests for theorem-bound arithmetic;
- tests verifying the spec-gate fixture explicitly records grid-count/probability
  separation;
- tests verifying no Stage 4 production module is introduced;
- `ruff`, `mypy`, `pytest`, and `fts doctor --release-check`.

## Artifacts To Save

This spec-gate task saves no generated experiment artifacts.

Committed files are:

- task brief;
- specs;
- fixture JSON;
- tests;
- registry/documentation updates.

## Claims Allowed

- `CLM-FBT-THM-001` has a draft theorem-domain transcription and fixture-backed
  arithmetic checks for the lower-bound expression.
- `CLM-FBT-ATLAS-001` has a draft finite-atlas design protocol, but no atlas cells,
  results, or aggregate statistics have been generated.
- Stage 4 remains pre-implementation and pre-independent-review.

## Claims Forbidden

- Do not claim the FBT theorem is implemented.
- Do not claim the finite atlas has been run.
- Do not claim finite grid frequencies are source theorem probabilities.
- Do not choose a MAP tie rule or zero-marginal policy silently.
- Do not claim any result about real perception, consciousness, spacetime, ontology,
  biology, ML/RL, or evolutionary dynamics.

## Out Of Scope

- production FBT theorem implementation;
- production finite-atlas implementation;
- exhaustive grids, sweeps, manifests, figures, UI, notebooks, or release capsules;
- evolutionary dynamics;
- ML/RL;
- independent review in this same implementation session.

## Review Cadence

Independent review is deferred until the Stage 4 spec/oracle-design bundle is ready for
a fresh-context reviewer to audit source transcription, ambiguity handling, and atlas
claim boundaries.

