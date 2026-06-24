# FFF Total Orders

```text
SPEC ID: SPEC-FFF-TOTAL-ORDERS-001
TASK IDS: TASK-001
SOURCE IDS: SRC-FFF-2020
CLAIM IDS: CLM-FFF-ORD-001
ASSUMPTION IDS: ASM-FFF-0001
EPISTEMIC STATUS: R, assumption-sensitive
```

## Source Locator

- `SRC-FFF-2020`; version of record / publisher page; Section 4, Total Orders Theorem.
- `SRC-FFF-2020`; publisher PDF; Section 4, page 7.
- `SRC-FFF-2020`; Appendix A.2, "Total Orders Theorem: Counting Functions that are Monotonic, i.e., First-Order Homomorphisms Preserving (or Reversing) Order".

## Source Formula

The source states that the number of admissible payoff functions that are homomorphisms of total orders is:

```text
2 * binom(n + m - 2, m - 1)
```

The Appendix A.2 title identifies the counted functions as monotonic maps preserving or reversing order.

## Code Convention

The implementation uses canonical finite chains:

```text
domain:   0 < 1 < ... < n - 1
codomain: 0 < 1 < ... < m - 1
```

The source's maximum payoff value `m` is represented by code value `m - 1`.

## Preserving And Reversing Checks

A function `f` is order-preserving when:

```text
i <= j implies f(i) <= f(j)
```

On the canonical chain, this is equivalent to adjacent non-decreasing values.

A function `f` is order-reversing when:

```text
i <= j implies f(i) >= f(j)
```

On the canonical chain, this is equivalent to adjacent non-increasing values.

For Stage 1 enumeration, only admissible functions are counted for total-order ratios.

## Double-Counting Note

`ASM-FFF-0001` remains open because preserving/reversing/constant-map treatment affects whether the source formula is interpreted as:

- an orientation-witness count; or
- a count of unique payoff functions.

GitHub issue #1 tracks this discrepancy/interpretation risk for independent source transcription and Human PI decision.

The implementation therefore exposes both quantities:

```text
source_total_order_witness_count(n, m) = 2 * binom(n + m - 2, m - 1)
unique_total_order_homomorphism_count(n, m) = source_total_order_witness_count(n, m) - 1
```

The subtraction is for the single admissible constant maximum function, which is both preserving and reversing.

Example:

```text
n = 2, m = 2
admissible functions: (1, 0), (0, 1), (1, 1)
source orientation witnesses: 4
unique admissible monotone functions: 3
```

This distinction must be reported before any public Stage 1 total-order claim.

## Required Checks

- Brute-force witness enumeration equals the source formula over the declared small grid.
- Brute-force unique-function enumeration equals the unique-function formula over the declared small grid.
- The maximum constant function has both preserving and reversing witnesses.
- Non-admissible constants do not enter admissible total-order counts.

## Forbidden Interpretation

Do not claim that the source formula is the unique-function count without the double-counting note and independent review.
