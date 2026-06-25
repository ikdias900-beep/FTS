# REV-TASK-001-SWEEP-001 - Independent Review of Stage 1 Sweep

```text
REVIEW ID: REV-TASK-001-SWEEP-001
TASK ID: TASK-001-SWEEP
COMMIT REVIEWED: 85c2c00bd2f9c2fc874b3a0c5d7e38f0f74642f8
TARGET IMPLEMENTATION COMMIT: 799e51b71627db2521d0d97c9a5a124a0cee3338
REVIEWER ROLE: Fresh-context AI/Codex Verifier
DATE: 2026-06-25
VERDICT: accepted_with_minor_findings
```

## Context Boundary

This review used only repository files, task/spec/code/tests, and the review brief. I did not use private implementer rationale as evidence. I read `docs/reviews/REV-TASK-001-001.md` only after completing independent small-case derivations and the sweep audit, as historical context for the previously accepted Stage 1 exact helpers.

`HEAD` was `85c2c00bd2f9c2fc874b3a0c5d7e38f0f74642f8`; the target implementation commit `799e51b71627db2521d0d97c9a5a124a0cee3338` is an ancestor of `HEAD`. The worktree was clean before command execution and after the review commands.

## Scope

Reviewed the files required by `docs/reviews/TASK-001-SWEEP-independent-review-brief.md`, with focused supporting inspection of the Stage 1 FFF helper modules used by `src/fts_lab/fff/sweeps.py`.

Out-of-scope items were not reviewed or implemented: plots, notebooks, web demo, permutation groups, measurable spaces, FBT, evolution, ML/RL, new assumptions, and philosophical claims.

## Independent Derivations

I derived these small cases with a scratch script that did not import `fts_lab.fff`.

Admissible payoff functions are functions that attain the maximum payoff value at least once:

- `n=1,m=1`: admissible count `1`; functions `(0,)`; formula `1^1 - 0^1 = 1`.
- `n=2,m=2`: admissible count `3`; functions `(0,1)`, `(1,0)`, `(1,1)`; formula `2^2 - 1^2 = 3`.
- `n=2,m=3`: admissible count `5`; formula `3^2 - 2^2 = 5`.
- `n=3,m=2`: admissible count `7`; formula `2^3 - 1^3 = 7`.

For total orders at `n=2,m=2`, the admissible functions are `(0,1)`, `(1,0)`, and `(1,1)`. `(0,1)` is preserving, `(1,0)` is reversing, and the maximum constant `(1,1)` is both preserving and reversing. Therefore the source orientation-witness count is `4`, while the distinct unique-function count is `3`. The corresponding ratios over the admissible denominator are `4/3` and `1/1`.

For cyclic groups:

- `Z_2 -> Z_2`: source homomorphism count `gcd(2,2)=2`, admissible denominator `3`, source ratio `2/3`; admissible-filtered audit count `1`.
- `Z_3 -> Z_2`: source homomorphism count `gcd(3,2)=1`, admissible denominator `7`, source ratio `1/7`; admissible-filtered audit count `0`.
- `Z_4 -> Z_2`: source homomorphism count `gcd(4,2)=2`, admissible denominator `15`, source ratio `2/15`; admissible-filtered audit count `1`.

## Source-To-Code Audit

The default config declares exactly the expected traceability set:

- `task_ids`: `["TASK-001-SWEEP"]`
- `source_ids`: `["SRC-FFF-2020"]`
- `assumption_ids`: `["ASM-FFF-0001"]`
- `claim_ids`: `CLM-FFF-ADM-001`, `CLM-FFF-ORD-001`, `CLM-FFF-CYC-001`, `CLM-FFF-CYC-002`

`src/fts_lab/fff/sweeps.py` builds rows from the already-reviewed Stage 1 exact helpers rather than introducing new mathematical definitions. For every `(domain_size, codomain_size)` pair it writes:

- one admissibility count row;
- two total-order source rows for orientation-witness count and ratio;
- two total-order `RDR-0002` companion rows for distinct unique-function count and ratio;
- two cyclic source rows for `gcd(n,m)` count and source ratio.

The total-order source and companion rows are distinguishable by `count_object`, `row_epistemic_status`, `assumption_ids`, and `notes`. Source rows remain `R` with empty `assumption_ids`; `RDR-0002` companion rows are `C` with `ASM-FFF-0001`.

The cyclic source numerator `gcd(n,m)` is kept separate from the optional admissible-filtered cyclic audit count. The default config has `include_admissible_cyclic_audit: false`, so the canonical sweep does not include audit rows.

## CSV And Manifest Audit

Generated manifest:

```text
C:\Users\user\Fitness, Truth & Structure Lab\experiments\manifests\ART-TASK-001-SWEEP-MANIFEST-20260625T004315Z-F1CBA118.json
```

Generated CSV:

```text
C:\Users\user\Fitness, Truth & Structure Lab\results\raw\EXP-TASK-001-SWEEP-20260625T004315Z-F1CBA118\fff_stage1_counts.csv
```

The manifest uses `artifact_kind: fff_stage1_finite_count_sweep` and artifact-level `epistemic_status: C`.

The `4 x 4` grid produced `112` data rows plus the CSV header: 16 rows for each of the 7 default count objects. Every pair contains both total-order count objects: `source_orientation_witnesses` and `distinct_unique_functions`.

Machine audit of the generated CSV found:

- row statuses: `80` rows with `R`, `32` rows with `C`;
- `R` rows have empty `assumption_ids`;
- `C` rows have `assumption_ids=ASM-FFF-0001`;
- no floating-point decimal values in `numerator`, `denominator`, or `value_label`;
- deterministic row order: nested `domain_sizes`, `codomain_sizes`, then fixed row order per pair.

For `(n,m)=(2,2)`, the generated rows match the independent derivation:

```text
admissible_payoff_functions: 3
source_orientation_witnesses: 4
source_orientation_witnesses_over_admissible: 4/3
distinct_unique_functions: 3
distinct_unique_functions_over_admissible: 1
source_cyclic_homomorphisms: 2
source_cyclic_homomorphisms_over_admissible: 2/3
```

The manifest records command, parameters, input checksum, output checksum, git state, and `uv.lock` checksum. The manifest output checksum is:

```text
6f391a2891e1274d2e1b8240cbc35329bbe6a40326f71ba20b04f642263d5bab
```

## Reproducibility Checks

The literal first required command failed in this verifier shell because `uv` was not on the PowerShell `PATH`:

```text
uv run ruff check .
uv : The term 'uv' is not recognized as the name of a cmdlet, function, script file, or operable program.
```

`uv` was available through the Python launcher and at `C:\Users\user\AppData\Roaming\Python\Python313\Scripts\uv.exe`; running the checks through `py -m uv run ...` and the absolute `uv.exe` path succeeded.

Command summary:

```text
git rev-parse HEAD
85c2c00bd2f9c2fc874b3a0c5d7e38f0f74642f8

py -m uv run ruff check .
All checks passed!

py -m uv run ruff format --check .
23 files already formatted

py -m uv run mypy src
Success: no issues found in 13 source files

py -m uv run pytest
189 passed in 5.44s

py -m uv run fts doctor
Active task: TASK-001-SWEEP
python: 3.12.13
uv: uv 0.11.24
all required context files present
license_decision: pending; public release blocked

py -m uv run fts fff sweep --config experiments/configs/fff_stage1_small.json
row_count=112
manifest_path=C:\Users\user\Fitness, Truth & Structure Lab\experiments\manifests\ART-TASK-001-SWEEP-MANIFEST-20260625T004315Z-F1CBA118.json

py -m uv run fts validate-manifest <manifest_path>
manifest valid

py -m uv run pytest tests/integration/test_cli_and_smoke.py::test_stage1_sweep_manifest_validation_fails_after_csv_corruption
1 passed
```

The checksum-corruption test copies the generated CSV and manifest to a temporary directory, mutates only the copy, and verifies that manifest validation fails with a checksum mismatch.

## Fatal Findings

None.

## Major Findings

None.

## Minor Findings

1. Bare `uv` is not resolvable in this verifier PowerShell session, although the same `uv` installation works through `py -m uv` and its absolute executable path. This is an environment/ergonomics issue for the documented commands, not a sweep correctness issue.

2. `src/fts_lab/fff/sweeps.py:149` validates the config shape and artifact-level status, but lines 163-166 accept any non-empty, non-duplicate `task_ids`, `claim_ids`, `source_ids`, and `assumption_ids`. The default checked-in config is correct, and the generated artifact is traceable. A future hardening pass could reject configs whose ID sets do not exactly match `TASK-001-SWEEP`, `SRC-FFF-2020`, `ASM-FFF-0001`, and the four expected claim IDs.

## Overclaim Audit

No overclaims were found in `README.md`, `tasks/TASK-001_stage1_sweeps_tables.md`, the sweep config, specs, or review notes. The public-facing language stays within finite Stage 1 exact counts and explicitly rejects metaphysical, biological-probability, and human-perception overclaims.

## Verdict

`TASK-001-SWEEP` passes the independent review gate with minor findings only. The task is not blocked: there are no unresolved `fatal` or `major` findings.

The generated sweep preserves the required per-row epistemic statuses, separates source counts from `RDR-0002` presentation companion rows, keeps cyclic source counts distinct from admissible-filtered audit counts, writes deterministic non-float result values, and produces a manifest whose checksums validate and fail on CSV corruption.
