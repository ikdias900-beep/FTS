# Claims

```text
TASK ID: TASK-003-P3-CAPSULE
EPISTEMIC STATUS: R
SOURCE IDS: SRC-FFF-2020
CLAIM IDS: CLM-FFF-PERM-001; CLM-FFF-MEAS-001
ASSUMPTION IDS: ASM-FFF-0002; ASM-FFF-0003
REVIEW STATUS: REV-TASK-003-FFF-STRUCTURE-001_no_fatal_or_major
```

## Allowed Claims In This Capsule

- The capsule packages the reviewed Stage 3 FFF permutation-group and measurable-space
  finite-helper scope.
- `CLM-FFF-PERM-001` is `implemented_reviewed`: source-explicit permutation helpers,
  action-law checks, and formula arithmetic passed independent review with no fatal or
  major findings.
- `CLM-FFF-MEAS-001` is `implemented_reviewed`: partition measurability helpers, exact
  small-case enumeration, special-case checks, and source upper-bound arithmetic passed
  independent review with no fatal or major findings.
- The Stage 3 fixture copy in `raw_data/` is the reviewed small-case fixture used by the
  Stage 3 spec-gate and implementation tests.
- The capsule is locally auditable through `checksums.txt` and
  `fts validate-release-capsule`.

## Status Boundaries

- All scientific claims packaged here are `R`: reproduction/source-transcription work
  for `SRC-FFF-2020`.
- No new scientific claim is added by the capsule.
- `ASM-FFF-0002` and `ASM-FFF-0003` are `SOURCE_RESOLVED` only for the reviewed Stage 3
  finite-helper scope.
- Future exhaustive automorphism enumeration, algebra-isomorphism sweeps, alternate
  canonicalization, approximate metrics, or extension work needs a new task or decision.

## Forbidden Claims

- This capsule is not a final public P3 publication, DOI archive, GitHub release, or
  external archival deposit.
- The Appendix A.5 measurable upper bound is not an exact count in every measurable
  space case.
- Ordinary group-homomorphism enumeration is not an implementation of the paper's
  second-order permutation-group construction.
- The Stage 3 finite-helper scope does not establish claims about real perception,
  consciousness, spacetime, ontology, biology, ML/RL, or evolutionary dynamics.

