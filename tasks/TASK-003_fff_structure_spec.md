# TASK-003-FFF-STRUCTURE-SPEC: Stage 3 FFF Structure Spec Gate

TASK ID: TASK-003-FFF-STRUCTURE-SPEC
EPISTEMIC STATUS: R

## Research Question

Can the `SRC-FFF-2020` permutation-group and measurable-structure theorem
statements be transcribed into implementation-ready specifications and small-case
oracle designs without yet implementing the production Stage 3 modules?

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

This task produces formal specifications only:

- `specs/fff/permutation_groups.md`
- `specs/fff/measurable_spaces.md`

The permutation-group spec must distinguish:

- first-order group homomorphisms;
- group actions;
- source second-order `G`-homomorphisms `(phi, f)`;
- the source `S_n` theorem count `2*n + n!` for `n >= 5`;
- the risk of replacing the source construction with ordinary group homomorphisms.

The measurable-space spec must distinguish:

- finite event algebras and their partition bases;
- algebra order `k`;
- algebra characteristic;
- inverse-image measurability;
- trivial/discrete special cases;
- exact finite counts versus the source upper bound.

## Input Domain

Committed spec fixtures are limited to small finite examples in:

- `tests/fixtures/fff/stage3_structure_spec_cases.json`

These fixtures are not generated scientific results. They are design fixtures for
future implementation and review.

## Expected Output

- Stage 3 task brief;
- two formal specs with source locators and forbidden interpretations;
- small-case fixture data for permutation and measurable-structure checks;
- test-local oracle checks that validate fixture internal consistency without importing
  future production implementation;
- registry/documentation updates showing Stage 3 is at spec-gate status only.

## Known Small Cases

Permutation groups:

- source formula cases for `n = 5` and `n = 6`;
- no exhaustive production checker is introduced in this task.

Measurable spaces:

- a nontrivial/non-discrete `W` partition with discrete `V`, where the bound is tight;
- a non-measurable example by inverse-image criterion;
- `W` discrete and `V` trivial special cases where all functions are measurable.

## Invariants

- No production module `src/fts_lab/fff/permutation_groups.py` or
  `src/fts_lab/fff/measurable_spaces.py` is created in this task.
- Tests for this task must not import future production Stage 3 code.
- The source measurable theorem bound must not be labeled an exact count.
- The source permutation theorem must not be replaced by ordinary group-homomorphism
  enumeration.
- `ASM-FFF-0002` and `ASM-FFF-0003` remain open until independent review and Human PI
  acceptance of the formalization.

## Assumptions

No new approved scientific assumption is introduced.

Open assumptions acknowledged and not resolved:

- `ASM-FFF-0002`: source second-order symmetric-group morphism formalization and
  count-object interpretation remain pending independent review.
- `ASM-FFF-0003`: finite algebra canonicalization and bound/exact-count treatment
  remain pending independent review.

## Tests Required Before Merge

- fixture-internal consistency tests for the source permutation formula cases;
- fixture-internal consistency tests for measurable-space exact small cases;
- inverse-image non-measurability witness test;
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

- `CLM-FFF-PERM-001` and `CLM-FFF-MEAS-001` have draft formal specifications and
  small-case oracle designs.
- Stage 3 remains pre-implementation and pre-independent-review.

## Claims Forbidden

- Do not claim permutation-group or measurable-space theorem reproduction is
  implemented.
- Do not claim `CLM-FFF-PERM-001` or `CLM-FFF-MEAS-001` is reviewed.
- Do not claim the source measurable upper bound is an exact count.
- Do not claim an ordinary group-homomorphism count implements the source
  permutation theorem.
- Do not claim any result about real perception, consciousness, spacetime, ontology,
  biology, ML/RL, or evolutionary dynamics.

## Out Of Scope

- production implementation of permutation groups;
- production implementation of measurable spaces;
- CLI commands;
- sweeps, manifests, release capsules, figures, UI, notebooks;
- approximate homomorphism metrics;
- independent review in this same implementation session.

## Review Cadence

Following the Human PI decision to review less frequently, independent review is
deferred until the Stage 3 spec/oracle bundle is complete enough for a fresh-context
reviewer to audit source transcription and small-case oracle design.
