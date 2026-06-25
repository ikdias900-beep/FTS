# REV-TASK-001-PUBTABLES-001 - Independent Review of Stage 1 Publication Tables

```text
REVIEW ID: REV-TASK-001-PUBTABLES-001
TASK ID: TASK-001-PUBTABLES
COMMIT REVIEWED: fc438d130a05dbc6ed70e89dfacc5e8f425b7ca5 + local working-tree fix
TARGET IMPLEMENTATION COMMIT: d6ff498a2e526b21374825c831a8a10eb7405708
REVIEWER ROLE: Fresh-context AI/Codex Verifier
DATE: 2026-06-25
VERDICT: accepted_with_minor_findings
```

## Context Boundary

This review used repository files, task/spec/code/tests, generated artifacts from commands, the public GitHub PR page for PR #5, and the review brief. I did not use private implementer rationale as evidence. Previous report `REV-TASK-001-SWEEP-001` was read only as historical context; it was not treated as an oracle for the publication-table transformation.

`HEAD` is `fc438d130a05dbc6ed70e89dfacc5e8f425b7ca5`. The target implementation commit `d6ff498a2e526b21374825c831a8a10eb7405708` is an ancestor of `HEAD`. The current candidate is not a clean commit: the working tree contains the local fix in `src/fts_lab/fff/publication_tables.py` and its regression test in `tests/integration/test_cli_and_smoke.py`, plus this review report and the implementer-side follow-up report. Generated manifests from this review therefore record `dirty=True`.

I first reviewed clean `HEAD` in a detached worktree and confirmed the original major finding: clean `HEAD` did not validate the source sweep manifest `task_ids`. I then reviewed the current local fixed candidate in the main worktree, because the fix is not yet committed.

## Scope

Reviewed the files named in `docs/reviews/PUBTABLES-review-brief.md`, with focused supporting inspection of the publication-table command, sweep manifest producer, manifest validation helpers, doctor output, tests, README, changelog, and Stage 1 publication-table documentation.

Out-of-scope items were not reviewed or implemented: plots, notebooks, web demo, FBT, evolution, ML/RL, permutation groups, measurable spaces, new assumptions, new mathematical definitions, and philosophical claims.

## Independent Transformation Expectations

A correct `TASK-001-PUBTABLES` transformation must:

- read one validated `TASK-001-SWEEP` manifest;
- use the sweep CSV listed in that manifest output;
- group the default `112` long-form sweep rows into `16` wide rows for the `4 x 4` grid;
- preserve the source sweep manifest ID and run ID in every wide row;
- preserve exact integer and rational string values without decimal floats;
- preserve per-column `R/C` statuses instead of flattening the table to artifact-level `C`;
- keep total-order source orientation-witness counts separate from `RDR-0002` distinct unique-function companion counts;
- keep cyclic source homomorphism counts separate from admissible-filtered audit counts;
- write a derived manifest whose inputs include both the source sweep manifest and source sweep CSV;
- write outputs for both the derived CSV and generated Markdown report.

I checked generated artifacts with PowerShell CSV/JSON/Markdown inspection and direct source-CSV-to-derived-CSV comparison. These checks did not import `fts_lab.fff.publication_tables` as an oracle.

Independent expected spot checks:

```text
(n,m)=(2,2): admissible 3; order witness count 4; order witness ratio 4/3; unique order count 3; unique order ratio 1; cyclic count 2; cyclic ratio 2/3.
(n,m)=(4,4): admissible 175; order witness count 40; order witness ratio 8/35; unique order count 39; unique order ratio 39/175; cyclic count 4; cyclic ratio 4/175.
```

## Generated Artifact Audit

Generated source sweep:

```text
sweep_manifest_path=C:\Users\user\Fitness, Truth & Structure Lab\experiments\manifests\ART-TASK-001-SWEEP-MANIFEST-20260625T092012Z-BDBD3455.json
sweep_csv_path=C:\Users\user\Fitness, Truth & Structure Lab\results\raw\EXP-TASK-001-SWEEP-20260625T092012Z-BDBD3455\fff_stage1_counts.csv
sweep_csv_checksum=6f391a2891e1274d2e1b8240cbc35329bbe6a40326f71ba20b04f642263d5bab
sweep_rows=112
```

Generated publication package:

```text
publication_manifest_path=C:\Users\user\Fitness, Truth & Structure Lab\experiments\manifests\ART-TASK-001-PUBTABLES-MANIFEST-20260625T092019Z-E7710A69.json
summary_csv_path=C:\Users\user\Fitness, Truth & Structure Lab\results\derived\EXP-TASK-001-PUBTABLES-20260625T092019Z-E7710A69\stage1_fff_publication_counts.csv
summary_csv_checksum=33bf45de4b6ccdfe16b6e29d2d35e3c461cd86539024e6b3958bd81b7db82263
report_path=C:\Users\user\Fitness, Truth & Structure Lab\results\reports\EXP-TASK-001-PUBTABLES-20260625T092019Z-E7710A69\stage1_fff_publication_tables.md
report_checksum=a4a3762d2a11015da64172836866dceb6b3010c80f7cf89c758f71c0dc173fe4
publication_rows=16
```

Generated-artifact checks found:

- derived CSV has `16` data rows plus header;
- generated Markdown report has `16` `(n,m)` table rows;
- value columns contain `0` decimal-float cells;
- source sweep CSV has `112` rows and status counts `R:80;C:32`;
- source-CSV-to-derived-CSV comparison found `0` mismatches;
- per-column status pattern is consistently `R/R/C/R`.

Spot checks matched the independent expected values:

```text
pair_2_2=admissible:3;order_witness:4;order_witness_ratio:4/3;unique:3;unique_ratio:1;cyclic:2;cyclic_ratio:2/3;statuses:R/R/C/R
pair_4_4=admissible:175;order_witness:40;order_witness_ratio:8/35;unique:39;unique_ratio:39/175;cyclic:4;cyclic_ratio:4/175;statuses:R/R/C/R
```

## Source-To-Code Audit

The original major finding was valid for clean `HEAD`: the publication command validated artifact kind, artifact-level status, claims, sources, and assumptions, but not the source sweep manifest's `task_ids`.

The current fixed candidate imports `EXPECTED_TASK_IDS` from `fts_lab.fff.sweeps` and requires the source manifest `task_ids` to equal `["TASK-001-SWEEP"]`. A regression test was added:

```text
tests/integration/test_cli_and_smoke.py::test_stage1_publication_tables_rejects_manifest_with_wrong_source_task
```

The direct negative check also rejects a sweep-shaped manifest with only `task_ids` changed:

```text
fff failed: task_ids must be exactly ['TASK-001-SWEEP']
exit_code=1
```

The publication command also rejects non-sweep manifests by artifact kind:

```text
fff failed: Expected sweep artifact kind 'fff_stage1_finite_count_sweep'
exit_code=1
```

The transformation reads the source CSV from the validated source manifest output, validates the sweep CSV header against the Stage 1 sweep fieldnames, rejects unexpected count objects, rejects duplicate count objects per `(n,m)`, and rejects missing required count objects.

`sweeps.py` requires the Stage 1 sweep config ID sets exactly to `TASK-001-SWEEP`, `SRC-FFF-2020`, `ASM-FFF-0001`, and the four expected claim IDs. `manifests.py` validates JSON Schema, project traceability rules, and input/output checksums. `doctor.py` reports active task `TASK-001-PUBTABLES` and all required context files.

## CSV And Report Audit

The derived CSV preserves source and companion columns separately:

- admissible payoff-function count: `R`;
- total-order source orientation-witness count and ratio: `R`;
- total-order distinct unique-function count and ratio: `C`;
- cyclic source homomorphism count and ratio: `R`.

The generated Markdown report includes provenance, status legend, the `16` table rows, allowed claims, and forbidden claims. It explicitly states that the finite grid summary must not be interpreted as an empirical probability distribution over biological payoff functions.

## Manifest And Checksum Audit

The publication manifest validates successfully:

```text
artifact_kind=fff_stage1_publication_tables
epistemic_status=C
task_ids=TASK-001-PUBTABLES
claim_ids=CLM-FFF-ADM-001;CLM-FFF-ORD-001;CLM-FFF-CYC-001;CLM-FFF-CYC-002
source_ids=SRC-FFF-2020
assumption_ids=ASM-FFF-0001
input_count=2
output_count=2
```

Manifest inputs include both the source sweep manifest and source sweep CSV. Manifest outputs include both the derived CSV and generated Markdown report.

Checksum-corruption behavior was verified with:

```text
py -m uv run pytest tests/integration/test_cli_and_smoke.py::test_stage1_publication_tables_manifest_validation_fails_after_output_corruption
1 passed
```

## Reproducibility Checks

The literal bare `uv` command failed in this PowerShell environment:

```text
uv run ruff check .
uv : The term 'uv' is not recognized as the name of a cmdlet, function, script file, or operable program.
```

The review brief permits `py -m uv run ...` when bare `uv` is unavailable. Required command outcomes through that fallback:

```text
git rev-parse HEAD
fc438d130a05dbc6ed70e89dfacc5e8f425b7ca5

git status --short --branch
## stage1-publication-tables...origin/stage1-publication-tables
 M src/fts_lab/fff/publication_tables.py
 M tests/integration/test_cli_and_smoke.py
?? docs/reviews/REV-TASK-001-PUBTABLES-001-followup.md
?? docs/reviews/REV-TASK-001-PUBTABLES-001.md

py -m uv run ruff check .
All checks passed!

py -m uv run ruff format --check .
25 files already formatted

py -m uv run mypy src
Success: no issues found in 14 source files

py -m uv run pytest
197 passed in 6.19s

py -m uv run fts doctor
Active task: TASK-001-PUBTABLES
Git: commit=fc438d130a05dbc6ed70e89dfacc5e8f425b7ca5 branch=stage1-publication-tables dirty=True
all required context files present
license_decision: pending; public release blocked

py -m uv run fts fff sweep --config experiments/configs/fff_stage1_small.json
row_count=112
manifest_path=C:\Users\user\Fitness, Truth & Structure Lab\experiments\manifests\ART-TASK-001-SWEEP-MANIFEST-20260625T092012Z-BDBD3455.json

py -m uv run fts validate-manifest <sweep-manifest-path>
manifest valid

py -m uv run fts fff publication-tables --sweep-manifest <sweep-manifest-path>
row_count=16
manifest_path=C:\Users\user\Fitness, Truth & Structure Lab\experiments\manifests\ART-TASK-001-PUBTABLES-MANIFEST-20260625T092019Z-E7710A69.json

py -m uv run fts validate-manifest <publication-manifest-path>
manifest valid

py -m uv run pytest tests/integration/test_cli_and_smoke.py::test_stage1_publication_tables_rejects_manifest_with_wrong_source_task
1 passed
```

GitHub CLI was not available in this shell. The public PR page at `https://github.com/ikdias900-beep/FTS/pull/5` showed PR #5 as `Draft` with no reviews at review time, so the remote PR remains blocked from merge. The local fix must be committed and pushed before this accepted local-candidate review can correspond to the remote PR contents.

## Fatal Findings

None.

## Major Findings

None unresolved.

Previously observed major finding: the source sweep manifest `task_ids` were not validated. That finding is fixed in the current local candidate and covered by both regression test and direct mutated-manifest command output.

## Minor Findings

1. Bare `uv` is not resolvable in this PowerShell environment, although `fts doctor` finds `uv 0.11.24` at `C:\Users\user\AppData\Roaming\Python\Python313\Scripts\uv.exe`, and all required checks pass through the review-brief fallback `py -m uv run ...`.

2. The accepted candidate includes uncommitted working-tree changes. This does not change the local artifact audit result, but it means PR #5 is still formally blocked until the fix and review report are committed and pushed.

## Overclaim Audit

No overclaims were found in `README.md`, `tasks/TASK-001_publication_tables_docs.md`, `docs/research_notes/stage1_publication_tables.md`, the generated report, or `CHANGELOG.md`.

Sensitive terms such as human perception, consciousness, spacetime, ontology, biological distribution, probability, and metaphysical claims appear only in boundary or forbidden-claim language. The package does not claim biological probability, human-perception conclusions, metaphysical conclusions, FBT results, evolutionary results, ML/RL results, permutation-group results, or measurable-space results.

## Verdict

`TASK-001-PUBTABLES` is accepted with minor findings for the current local fixed candidate. There are no unresolved `fatal` or `major` findings in that candidate.

The derived publication package depends on a validated `TASK-001-SWEEP` manifest and its recorded sweep CSV, preserves exact integer/rational values, preserves source sweep manifest/run IDs, keeps total-order source orientation-witness values separate from `RDR-0002` distinct unique-function companion values, keeps cyclic source homomorphism values separate from admissible-filtered audit values, writes a valid derived manifest with both required inputs and outputs, rejects wrong source task IDs, and remains within the allowed claim boundary.
