# FFF Permutation Groups

```text
SPEC ID: SPEC-FFF-PERMUTATION-GROUPS-001
TASK IDS: TASK-003-FFF-STRUCTURE-SPEC
SOURCE IDS: SRC-FFF-2020
CLAIM IDS: CLM-FFF-PERM-001
ASSUMPTION IDS: ASM-FFF-0002
EPISTEMIC STATUS: R draft specification, blocked until independent review
```

## Source Locator

- `SRC-FFF-2020`; version of record / publisher page; Section 4, Permutation Groups
  Theorem.
- `SRC-FFF-2020`; Appendix A.1, Definitions A1-A4.
- `SRC-FFF-2020`; Appendix A.3, "Permutation Groups Theorem: Counting Functions
  Preserving Symmetry under the Symmetric Group S_n".

## Source Definitions To Preserve

The source distinguishes first-order and second-order homomorphisms.

A first-order group homomorphism is a map between groups that preserves the group
operation.

A group action lets each element of an acting semigroup, monoid, or group `G` act as
an operation on another set `X`, compatibly with multiplication in `G`.

The Stage 3 permutation theorem uses the source's second-order construction. If `G`
acts on sets `X` and `Y`, a second-order `G`-homomorphism from `X` to `Y` is a pair:

```text
(phi, f)
```

where:

```text
phi: G -> G
f: X -> Y
```

and the action-compatibility law holds:

```text
f(g . x) = phi(g) . f(x)
```

for every `g in G` and `x in X`.

The source abbreviates this condition as `f` respecting `phi`.

## Stage 3 Canonical Objects

For the source symmetric-group theorem:

```text
G = S_n
X = {1, ..., n}
Y = {1, ..., n}
```

The source uses the natural action of `S_n` on the `n` symbols. Production code will
use zero-based labels:

```text
{0, ..., n - 1}
```

with the same permutation/action structure.

## Source Theorem Statement

For `n >= 5`, the source Appendix A.3 states that the number of respectful functions
is:

```text
2*n + n!
```

The corresponding ratio to all admissible payoff functions is:

```text
(2*n + n!) / (n^n - (n - 1)^n)
```

and the source proves this ratio tends to zero as `n -> infinity`.

## Count-Object Warning

The theorem must not be implemented as ordinary group homomorphism enumeration.
The source count is tied to the second-order pair `(phi, f)` and the action-compatibility
law above.

There is a count-object risk similar in shape to the Stage 1 total-order witness issue:
source Appendix A.3 decomposes the count into respectful functions for several classes
of `phi`. A future implementation must explicitly decide, after independent review,
whether public outputs display:

- the source respectful-witness count;
- distinct unique payoff functions `f`;
- or both, if these differ in finite cases.

Until that review, `ASM-FFF-0002` remains open.

## Source Count Components To Audit

The future checker must separately audit the source's cases:

- trivial homomorphism: constant `f` values;
- inner automorphisms of `S_n`: one respectful `f` per inner automorphism;
- homomorphism onto an order-2 subgroup: constant `f` values;
- source restriction/statement for `n >= 5`.

The checker must also explicitly document how the source's treatment handles the
exceptional outer automorphism of `S_6`, rather than silently relying on generic
`Aut(S_n)` facts from memory.

## Small-Case Oracle Design

This spec gate commits source-formula fixture cases in:

```text
tests/fixtures/fff/stage3_structure_spec_cases.json
```

For this task, tests only verify fixture consistency:

```text
count = 2*n + factorial(n)
denominator = n^n - (n - 1)^n
```

No production exhaustive `S_n` checker is introduced here.

The future production task should add an independent checker that:

- constructs `S_n` as permutations over canonical labels;
- validates closure, identity, inverse, and associativity by composition;
- evaluates the second-order law for candidate `(phi, f)` pairs;
- measures and reports any difference between respectful-witness and unique-function
  counts;
- refuses to run exhaustive enumeration above a measured threshold.

## Required Future Checks

- source transcription against Appendix A.1/A.3;
- `S_n` group operation tests;
- action law tests;
- examples of functions that respect trivial, inner, and order-2 quotient cases;
- known negative examples that fail the second-order law;
- formula comparison for reviewed finite cases;
- independent fresh-context review before changing `CLM-FFF-PERM-001` out of
  spec-gate status.

## Forbidden Interpretation

Do not claim that an ordinary homomorphism count from `S_n` to `S_n` is the source
permutation theorem. Do not claim this spec implements the theorem. Do not publish
the asymptotic statement without preserving the source's count object and `n >= 5`
scope.
