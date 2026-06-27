# TASK-003-FFF-STRUCTURE-IMPL: Stage 3 FFF Structure Implementation Bundle

TASK ID: TASK-003-FFF-STRUCTURE-IMPL
EPISTEMIC STATUS: R

## Research Question

Can the draft Stage 3 FFF permutation-group and measurable-space specifications be
turned into source-explicit finite validators and exact helper formulas without
upgrading public claims before independent review?

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

This task implements only the definitions and formulas already transcribed in:

- `specs/fff/permutation_groups.md`
- `specs/fff/measurable_spaces.md`

The implementation must keep these distinctions explicit:

- source second-order action compatibility is not ordinary group-homomorphism
  enumeration;
- the source symmetric-group formula is scoped to `n >= 5`;
- finite partition measurability is checked by inverse images of codomain base blocks;
- the Appendix A.5 measurable-function expression is an upper bound, not a universal
  exact count.

## Input Domain

Small finite canonical carriers:

- permutations over `{0, ..., n - 1}`;
- functions represented as tuples of zero-based codomain labels;
- finite event algebras represented by canonical partition bases.

This task does not enumerate all finite algebra isomorphism classes and does not run
large symmetric-group searches.

## Expected Output

- `src/fts_lab/fff/permutation_groups.py`
- `src/fts_lab/fff/measurable_spaces.py`
- exact tests for permutation actions, source formula arithmetic, measurable partitions,
  inverse-image measurability, special cases, and bound arithmetic;
- property tests for selected invariants;
- registry and documentation updates marking Stage 3 as implemented pending review.

## Known Small Cases

Permutation groups:

- `S_n` source formula fixtures for `n = 5` and `n = 6`;
- inner-conjugation examples satisfying the second-order action law;
- constant-function examples satisfying a trivial action target;
- concrete negative examples that fail action compatibility.

Measurable spaces:

- the committed nontrivial `W` partition with discrete `V`;
- `W` discrete and `V` trivial special cases where every function is measurable;
- a non-measurable witness whose inverse image splits a `W` base block.

## Invariants

- The implementation must not mark `CLM-FFF-PERM-001` or `CLM-FFF-MEAS-001` as
  reviewed.
- The implementation must not resolve `ASM-FFF-0002` or `ASM-FFF-0003`.
- Public-facing wording must remain `implemented_pending_review`.
- Tests may compare production code with the committed Stage 3 fixtures, but the fixture
  file remains the oracle source for this bundle.
- No release capsule, public figures, sweeps, or CLI commands are introduced in this
  task.

## Assumptions

No new approved scientific assumption is introduced.

Open assumptions acknowledged and not resolved:

- `ASM-FFF-0002`: source second-order symmetric-group morphism formalization and
  count-object interpretation remain pending independent review.
- `ASM-FFF-0003`: finite algebra canonicalization and bound/exact-count treatment remain
  pending independent review.

## Tests Required Before Merge

- exact Stage 3 tests for permutation and measurable helpers;
- property tests for permutation inverse/composition and measurable special cases;
- existing Stage 3 spec-gate fixture tests;
- `ruff`, `mypy`, `pytest`, and `fts doctor --release-check`.

## Artifacts To Save

No generated scientific result artifacts are saved in this task.

Committed files are:

- task brief;
- source modules;
- tests;
- registry/documentation updates.

## Claims Allowed

- `CLM-FFF-PERM-001` and `CLM-FFF-MEAS-001` have source-explicit finite helper
  implementations and tests pending independent review.
- The implementation reproduces declared formula arithmetic and small finite
  source-definition checks within the test scope.

## Claims Forbidden

- Do not claim the Stage 3 permutation-group or measurable-space theorem reproduction is
  reviewed.
- Do not claim the Appendix A.5 measurable upper bound is an exact count.
- Do not claim an ordinary `S_n -> S_n` group-homomorphism count implements the source
  theorem.
- Do not claim any result about real perception, consciousness, spacetime, ontology,
  biology, ML/RL, or evolutionary dynamics.

## Out Of Scope

- independent review in this same implementation session;
- public release capsule;
- exhaustive large symmetric-group enumeration;
- algebra-isomorphism sweeps;
- approximate homomorphism metrics;
- CLI commands, notebooks, figures, dashboards, or ML.

## Review Cadence

Following the Human PI decision to review less frequently, independent review is
deferred until the Stage 3 implementation bundle is ready for a fresh-context source,
spec, code, and oracle audit.
