# RDR-0002: Total-Order Count Presentation

## Status

APPROVED

## Intent

Resolve the Stage 1 presentation decision for `CLM-FFF-ORD-001` after discovering that the total-order source formula counts preserving/reversing orientation witnesses, while distinct payoff functions are counted differently in finite cases.

## Scope

This decision applies to:

- `TASK-001`;
- `SRC-FFF-2020`;
- `CLM-FFF-ORD-001`;
- `ASM-FFF-0001`;
- Stage 1 public tables, CLI output, documentation, and future demo labels for total orders.

## Options

1. Show only the source orientation-witness count.
2. Show only the distinct unique-function count.
3. Show both counts side by side.

## AI Explanation in Plain Language

For total orders, a payoff function can preserve order, reverse order, or in one special case do both. The maximum constant function is both preserving and reversing. If we count "ways this function is witnessed as monotone", that function is counted twice. If we count distinct payoff functions, it is counted once.

For example, when `n = 2` and `m = 2`:

- admissible payoff functions are `(0, 1)`, `(1, 0)`, and `(1, 1)`;
- `(0, 1)` is preserving;
- `(1, 0)` is reversing;
- `(1, 1)` is both preserving and reversing.

Therefore:

- source orientation-witness count is `4`;
- distinct unique-function count is `3`.

## Risks Of Each Option

Showing only the source orientation-witness count reproduces the paper's formula directly, but finite ratios can exceed `1`, which is confusing if readers interpret the count as a probability over unique functions.

Showing only the unique-function count is easier to interpret as distinct payoff functions, but it hides the exact source formula and could look like a silent correction.

Showing both counts is more verbose, but it preserves source traceability and makes the finite-size double-counting effect explicit.

## Human Decision

Show both counts.

Use these labels:

- `source orientation-witness count`;
- `distinct unique-function count`.

Every Stage 1 public total-order table, explanation, or demo must preserve this distinction. Do not collapse the two counts into one unnamed value.

Decision made by Human Principal Investigator on 2026-06-25.

## What This Does Not Mean

This does not claim that the source paper is wrong.

This does not replace the source formula.

This does not make witness counts biological probabilities.

This does not allow a public claim that the source formula is a unique-function count.

## When To Revisit

Revisit if a later source audit or author clarification shows that Appendix A.2 intended a different object than orientation witnesses, or if Stage 1 publication requires a more formal mathematical note on quotienting orientation witnesses by underlying functions.
