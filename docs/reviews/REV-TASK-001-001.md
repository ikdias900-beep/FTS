# REV-TASK-001-001 - Independent Review of Stage 1 Exact Helpers

```text
REVIEW ID: REV-TASK-001-001
TASK ID: TASK-001
COMMIT REVIEWED: bbbb1cde50a3ed7bb2113ec191abe3d5b6f90ec1
REVIEWER ROLE: Fresh-context AI/Codex Verifier
DATE: 2026-06-24
VERDICT: accepted_as_implementation_review_with_minor_finding
```

## Scope

Review `TASK-001` on branch `stage1-fff-core` without editing files.

Required focus:

- admissible payoff-function count;
- total-order witness count versus unique-function count;
- cyclic-group homomorphism count;
- traceability to `SRC-FFF-2020`;
- `ASM-FFF-0001` preserving/reversing/constant-map ambiguity.

## Verdict

`TASK-001` can be accepted as an implementation review for Stage 1 exact helpers.

No fatal or major findings were reported.

Important boundary: `ASM-FFF-0001` remains `OPEN`, so the public R-status total-order theorem claim remains blocked until the Human PI/source-transcription decision is resolved. The implementation correctly exposes that ambiguity instead of hiding it.

## Findings

### Fatal

None.

### Major

None.

### Minor

- `src/fts_lab/fff/formulas.py` and `src/fts_lab/fff/reports.py` are not directly tested, although equivalent ratio paths are covered through total-order/cyclic modules and CLI. This is a coverage gap, not a correctness blocker.

## Independent Derivations

For `n=2, m=2`, all functions are:

```text
(0, 0), (0, 1), (1, 0), (1, 1)
```

Admissible functions hit maximum payoff `1`, so the count is `3`.

Total orders for `n=2, m=2`:

- preserving admissible witnesses: `(0, 1)`, `(1, 1)`;
- reversing admissible witnesses: `(1, 0)`, `(1, 1)`;
- witness count: `4`;
- unique admissible monotone functions: `{(0, 1), (1, 0), (1, 1)}`, count `3`;
- overlap: exactly the admissible maximum constant `(1, 1)`.

Cyclic case `Z_6 -> Z_3`:

- homomorphisms are determined by `a = f(1)`;
- all `a in {0, 1, 2}` satisfy `6a = 0 mod 3`;
- maps are `(0,0,0,0,0,0)`, `(0,1,2,0,1,2)`, `(0,2,1,0,2,1)`;
- source count is `gcd(6, 3) = 3`;
- admissible-filtered count is `2`.

## Evidence

Specs cite `SRC-FFF-2020` locators for admissibility, total orders, and cyclic groups:

- `specs/fff/admissibility.md`;
- `specs/fff/total_orders.md`;
- `specs/fff/cyclic_groups.md`.

The verifier also checked the MDPI primary source page:

- https://www.mdpi.com/1099-4300/22/5/514

Code matches the spec split:

- total-order source witnesses and unique functions are separate in `src/fts_lab/fff/total_orders.py`;
- cyclic source count and admissible-filtered audit count are separate in `src/fts_lab/fff/cyclic_groups.py`;
- CLI emits `ASM-FFF-0001` for total-order counts in `src/fts_lab/cli.py`.

## Commands Run By Verifier

Initial command:

```bash
uv run ruff check .
```

failed because `uv` was not on the verifier process `PATH`.

Using `.venv`:

```bash
python -m ruff check .
python -m ruff format --check .
python -m mypy src --cache-dir %TEMP%/...
python -m pytest <scoped FFF exact/property tests and FFF CLI smoke>
```

All scoped verifier checks passed.

The verifier did not run full pytest because smoke tests write result artifacts and this pass was requested read-only. The verifier reported that the worktree remained clean after checks.

## Acceptance Impact

Implementation review gate is passed for `TASK-001`.

Remaining blocker:

- `ASM-FFF-0001` requires Human PI decision before public total-order theorem claims are treated as accepted.
