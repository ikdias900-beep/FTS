# FFF Admissible Payoff Functions

```text
SPEC ID: SPEC-FFF-ADMISSIBILITY-001
TASK IDS: TASK-001
SOURCE IDS: SRC-FFF-2020
CLAIM IDS: CLM-FFF-ADM-001
ASSUMPTION IDS: []
EPISTEMIC STATUS: R
```

## Source Locator

- `SRC-FFF-2020`; version of record / publisher page; Section 4, "Four Theorems".
- `SRC-FFF-2020`; publisher PDF; Section 4, pages 6-7, admissible payoff-function count.

## Source Definition

For `n` world states and `m` payoff values, the source counts all payoff functions as `m^n`.

The source then restricts attention to admissible payoff functions: those that attain the maximum payoff value for at least one world state.

The number of non-admissible functions is `(m - 1)^n`, because such functions avoid the maximum payoff value.

Therefore the admissible count is:

```text
m^n - (m - 1)^n
```

## Code Convention

The source writes payoff values as `1, ..., m`. The implementation uses Python-friendly values:

```text
0, ..., m - 1
```

Thus the source's maximum payoff value `m` is represented by code value `m - 1`.

## Domain

- `n >= 1`
- `m >= 1`
- functions are tuples of length `n`
- every tuple value is an integer in `0..m-1`

The empty-domain case is out of scope for Stage 1.

## Required Checks

- Reject non-positive `n` or `m`.
- Reject function tuples with wrong length or values outside `0..m-1`.
- Verify the formula by brute-force enumeration over the declared small test grid.

## Forbidden Interpretation

The counting measure over this finite set is the source's mathematical device. It must not be described as an empirically established distribution over biological fitness functions.
