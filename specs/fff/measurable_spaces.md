# FFF Measurable Spaces

```text
SPEC ID: SPEC-FFF-MEASURABLE-SPACES-001
TASK IDS: TASK-003-FFF-STRUCTURE-SPEC
SOURCE IDS: SRC-FFF-2020
CLAIM IDS: CLM-FFF-MEAS-001
ASSUMPTION IDS: ASM-FFF-0003
EPISTEMIC STATUS: R draft specification, blocked until independent review
```

## Source Locator

- `SRC-FFF-2020`; version of record / publisher page; Section 4, Measurable Structures
  Theorem.
- `SRC-FFF-2020`; Appendix A.1, Definitions A1-A4.
- `SRC-FFF-2020`; Appendix A.5, "Measurable Structure Theorem: Counting Measurable
  Functions, that is, (Backward) Homomorphisms Preserving Algebra or Partition
  Structure".

## Source Definitions To Preserve

For a finite set `X`, an event algebra is a collection of subsets of `X` that contains
`X` and is closed under union and complement.

The source uses finite algebras through their partition bases:

- each algebra corresponds to a partition of the underlying finite set;
- every event is a disjoint union of base blocks;
- the order `k` of an algebra is the number of base blocks;
- the characteristic of an algebra is the multiset of base-block sizes.

The source treats measurable functions as backward homomorphisms. For measurable
spaces on `W` and `V`, a function:

```text
f: W -> V
```

is measurable exactly when every measurable event in `V` has a measurable inverse
image in `W`.

For finite partition bases this is equivalent to:

```text
for every base block B of V, f^{-1}(B) is a union of base blocks of W
```

## Canonical Representation

Future implementation should represent a finite algebra by a canonical partition:

```text
((block_0), ..., (block_{k-1}))
```

where:

- each block is sorted;
- blocks are sorted by their first element, then lexicographically;
- blocks are nonempty and disjoint;
- the union of all blocks is the whole underlying set;
- labels are zero-based in code: `{0, ..., n - 1}`.

This canonical representation is an implementation convention. It must not be used to
claim the source theorem quotients algebras by isomorphism unless an RDR or later spec
explicitly says so.

## Source Special Cases

The source identifies cases in which all functions are measurable:

- the algebra on `W` is discrete;
- the algebra on `V` is trivial.

The main measurable-structures theorem excludes these easy cases by requiring:

```text
2 <= k <= n - 1
the algebra on W is neither trivial nor discrete
the algebra on V is not trivial
```

where `n = |W|`, `m = |V|`, and `k` is the order of the algebra on `W`.

## Source Bound

For the theorem scope above, Appendix A.5 gives an upper bound on the number of
measurable functions:

```text
m^(k - 1) + (m / (m - 1))^(k - 1) * (m - 1)^n
```

For integer implementation, use the equivalent exact-integer form:

```text
m^(k - 1) + m^(k - 1) * (m - 1)^(n - k + 1)
```

This is a bound, not an exact count for every measurable-structure pair.

## Ratio Scope

The admissible payoff-function denominator remains:

```text
m^n - (m - 1)^n
```

The source proves the fixed-`m`, `m >= 2`, ratio bound goes to zero as `n -> infinity`.
The source also notes that if `m` grows fast enough, for example `m = n`, the limiting
behavior can be different and need not go to zero.

Therefore public Stage 3 outputs must name the growth path and must not turn the
fixed-`m` corollary into a universal all-growth-rates statement.

## Small-Case Oracle Design

This spec gate commits fixture cases in:

```text
tests/fixtures/fff/stage3_structure_spec_cases.json
```

The test-local oracle checks:

- exact inverse-image measurability for small partitions;
- special cases where all functions are measurable;
- a concrete non-measurable witness;
- source bound arithmetic for declared `(n, m, k)` cases.

The test-local oracle is intentionally not a production implementation.

## Required Future Checks

- partition validation: nonempty blocks, no overlap, full coverage;
- event algebra construction from partitions;
- closure under union and complement for generated events;
- inverse-image measurability;
- exact enumeration for declared small spaces;
- special-case tests for `W` discrete and `V` trivial;
- bound comparison for nontrivial/nondiscrete `W` and nontrivial `V`;
- explicit separation of exact count, upper bound, and asymptotic corollary;
- independent fresh-context review before changing `CLM-FFF-MEAS-001` out of
  spec-gate status.

## Forbidden Interpretation

Do not call the Appendix A.5 bound an exact count. Do not omit the trivial/discrete
special cases. Do not interpret a finite counting-measure result as an empirical
biological probability distribution. Do not publish a measurable-structure ratio without
naming the growth path for `n`, `m`, and `k`.
