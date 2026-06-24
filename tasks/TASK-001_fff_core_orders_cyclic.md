# TASK-001 - FFF Core Orders and Cyclic Groups

```text
TASK ID: TASK-001
STAGE: 1 - FFF total orders and cyclic groups
EPISTEMIC STATUS: R, with explicit assumption-sensitive total-order notes
OWNER: Codex Implementer
REVIEWER: Fresh-context AI/Codex Verifier
STATUS: IN_PROGRESS
```

## 1. Objective

Implement exact, small-finite companions for the first Stage 1 FFF structures:

- admissible payoff-function counting;
- total-order monotonicity counts;
- cyclic-group homomorphism counts;
- exact ratios against admissible payoff functions.

The implementation must be source-traceable, deterministic, independent of UI/notebooks/network access, and backed by brute-force oracles for declared small cases.

## 2. Primary Source

`SRC-FFF-2020`:

Prakash, C., Fields, C., Hoffman, D. D., Prentner, R., & Singh, M. (2020). *Fact, Fiction, and Fitness*. Entropy, 22(5), 514.

Implementation locators:

- version of record / publisher page, Section 4;
- publisher PDF, Section 4, pages 7-8;
- Appendix A.2, Total Orders Theorem;
- Appendix A.4, Cyclic Groups Theorem.

## 3. Linked Claims

- `CLM-FFF-ADM-001`
- `CLM-FFF-ORD-001`
- `CLM-FFF-CYC-001`
- `CLM-FFF-CYC-002`

## 4. Linked Assumptions

- `ASM-FFF-0001` remains `OPEN` for public R-status claims about the exact source interpretation of total-order homomorphisms.

No new approved scientific assumptions are introduced by this task.

## 4.1 Linked Issues

- GitHub issue #1: total-order witness count vs unique functions discrepancy/interpretation risk.

## 5. Formal Definitions

Use `specs/fff/admissibility.md`, `specs/fff/total_orders.md`, and `specs/fff/cyclic_groups.md`.

Code uses zero-based finite carriers:

- world states: `0, ..., n-1`;
- payoff values: `0, ..., m-1`;
- the source's maximum payoff value `m` corresponds to code value `m - 1`.

## 6. Expected Output

Create:

```text
src/fts_lab/fff/
├── __init__.py
├── functions.py
├── admissibility.py
├── total_orders.py
├── cyclic_groups.py
├── formulas.py
└── reports.py
```

Implement:

- lazy enumeration of all functions for small `n, m`;
- admissibility filter and formula `m^n - (m - 1)^n`;
- order-preserving and order-reversing checks on finite total orders;
- total-order source witness count `2 * binom(n + m - 2, m - 1)`;
- a separate unique-function total-order count to expose preserving/reversing double counting;
- cyclic group homomorphism checker for additive `Z_n -> Z_m`;
- cyclic source count `gcd(n, m)`;
- exact ratios as `fractions.Fraction`;
- small CLI helpers under `fts fff ...`.

## 7. Known Small Cases

- `n=1, m=1`: admissible count is `1`.
- `n=1, m=2`: admissible count is `1`.
- `n=2, m=2`: admissible count is `3`.
- `n=2, m=2`: total-order source witness count is `4`, but unique admissible monotone functions are `3`.
- `n=2, m=2`: cyclic source homomorphism count is `2`, but admissible cyclic homomorphisms are `1`.
- `n=3, m=2`: cyclic source homomorphism count is `1`.

## 8. Invariants

- Every yielded function is a tuple of length `n` with values in `0..m-1`.
- Brute-force admissible count equals `m^n - (m - 1)^n`.
- Total-order source witness enumeration equals `2 * binom(n + m - 2, m - 1)`.
- Total-order unique enumeration equals source witness count minus the single admissible constant maximum function.
- Cyclic homomorphism enumeration equals `gcd(n, m)`.
- Invalid non-positive sizes raise `ValueError`.

## 9. Tests Required Before Merge

- exact brute-force grid tests for admissibility, total orders, and cyclic groups;
- edge-case tests for `n=1`, `m=1`, constants, and invalid inputs;
- property tests over bounded small domains;
- CLI smoke tests for the new `fts fff` subcommands;
- existing Stage 0 tests must remain green.

## 10. Artifacts To Save

No scientific result artifacts are saved in this task. This task creates reusable code, specs, and tests only.

## 11. Claims Allowed

- For declared finite cases, brute-force enumeration matches the admissible payoff count formula.
- For declared finite cases, cyclic homomorphism enumeration matches `gcd(n, m)`.
- The implementation exposes the source total-order witness count and separately exposes the unique-function count.

## 12. Claims Forbidden

- This code proves a claim about human perception, consciousness, spacetime, or biology.
- The source total-order witness count is the same thing as the count of unique payoff functions without noting the preserving/reversing overlap.
- Counting-measure ratios are biological probability distributions.
- Stage 1 results settle permutation groups, measurable spaces, FBT, evolution, ML, or UI/dashboard claims.

## 13. Out Of Scope

- permutation groups;
- measurable spaces;
- FBT appendix arithmetic;
- stochastic simulations;
- plotting libraries;
- web dashboards;
- notebooks;
- ML/RL code.

## 14. Acceptance Criteria

`TASK-001` is implementation-complete when:

1. required specs exist and cite `SRC-FFF-2020` locators;
2. the `fts_lab.fff` package implements all files listed above;
3. exact and property tests pass for the declared small grids;
4. `ruff`, `ruff format --check`, `mypy`, and `pytest` pass;
5. the total-order double-counting issue is documented, not hidden;
6. no saved result artifact or public scientific conclusion is produced without manifest/review;
7. an independent review is still required before treating Stage 1 as accepted.
