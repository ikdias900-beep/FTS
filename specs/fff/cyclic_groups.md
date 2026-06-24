# FFF Cyclic Groups

```text
SPEC ID: SPEC-FFF-CYCLIC-GROUPS-001
TASK IDS: TASK-001
SOURCE IDS: SRC-FFF-2020
CLAIM IDS: CLM-FFF-CYC-001, CLM-FFF-CYC-002
ASSUMPTION IDS: []
EPISTEMIC STATUS: R
```

## Source Locator

- `SRC-FFF-2020`; version of record / publisher page; Section 4, Cyclic Groups Theorem.
- `SRC-FFF-2020`; publisher PDF; Section 4, page 8.
- `SRC-FFF-2020`; Appendix A.4, "Cyclic Groups Theorem: Counting Functions Preserving Cyclicity on a Finite Group; or Periodic Functions on a Lattice".

## Source Formula

The source identifies finite cyclic groups with additive modular groups and states that the number of homomorphisms:

```text
Z_n -> Z_m
```

is:

```text
gcd(n, m)
```

It then compares this count to the admissible payoff-function denominator:

```text
m^n - (m - 1)^n
```

and states that the ratio goes to zero as `n -> infinity` and `m <= n`.

## Code Convention

Use additive cyclic groups:

```text
Z_n = {0, ..., n - 1}, operation (a + b) mod n
Z_m = {0, ..., m - 1}, operation (a + b) mod m
```

A function tuple `f` of length `n` represents:

```text
f(i) = tuple[i]
```

## Homomorphism Check

`f` is a cyclic-group homomorphism when:

```text
f((a + b) mod n) == (f(a) + f(b)) mod m
```

for all `a, b in Z_n`.

## Admissibility Note

The source numerator `gcd(n, m)` counts all cyclic-group homomorphisms. Some such homomorphisms may not attain the maximum payoff value `m - 1`.

The implementation therefore exposes:

- the source count `gcd(n, m)`;
- the source ratio `gcd(n, m) / (m^n - (m - 1)^n)`;
- an optional brute-force count of admissible cyclic homomorphisms, used as an audit aid rather than as a replacement for the source formula.

Example:

```text
n = 2, m = 2
source cyclic homomorphisms: 2
admissible cyclic homomorphisms: 1
```

## Required Checks

- Brute-force homomorphism enumeration equals `gcd(n, m)` over the declared small grid.
- Identity maps `Z_n -> Z_n` are accepted.
- Known non-homomorphisms are rejected.
- Invalid non-positive sizes raise `ValueError`.

## Forbidden Interpretation

The source ratio is a counting-measure theorem. It must not be presented as a measured biological distribution over payoff functions.
