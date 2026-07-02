# REV-TASK-004-FBT-ATLAS-V1-001 - Independent Review of Atlas v1 Bundle

```text
REVIEW ID: REV-TASK-004-FBT-ATLAS-V1-001
TASK IDS: TASK-004-FBT-ATLAS-V1-SPEC, TASK-004-FBT-ATLAS-V1-ENGINE, TASK-004-FBT-ATLAS-V1-AGGREGATE
COMMIT REVIEWED: 8e7399a32029a5726420df82318ae0b141e96e7b
REVIEWER ROLE: Fresh-context AI/Codex Verifier
DATE: 2026-07-02
VERDICT: accepted
```

## Scope

Reviewed the atlas v1 bundle requested by
`docs/reviews/TASK-004-FBT-ATLAS-V1-independent-review-brief.md`.

This review checked the limited pipeline:

```text
draft config -> exact raw-cell engine -> manifest-backed raw-cell JSON
             -> aggregate/report layer reading that raw JSON
             -> manifest-backed derived JSON/Markdown summary
```

This review did not validate a full finite atlas run, production implementation of
Theorem 4, source-level theorem result, evolutionary dynamics, ML/RL, UI, figures,
biological claims, or metaphysical claims.

No production code was changed as part of this review.

## Commands Run

`py -m uv` was not available in this Windows environment:

```text
py -m uv run fts doctor --release-check
```

Outcome: failed before project execution with `No installed Python found!`.

Used the local project environment instead:

```text
.\.venv\Scripts\python.exe -m fts_lab.cli doctor --release-check
```

Outcome: passed. Python `3.12.13`, package version `0.1.0`, active task
`TASK-004-FBT-ATLAS-V1-AGGREGATE`, git commit
`8e7399a32029a5726420df82318ae0b141e96e7b`, git dirty state `false`, lockfile checksum
`6b81fceadcb3fe17172ce56a239b581332675e7045058459a5871f2982e609c8`.

```text
.\.venv\Scripts\python.exe -m pytest
```

Outcome: initial sandboxed run could not complete because Windows denied creation of
test artifact/cache paths. Re-running the same command outside the sandbox passed:
`290 passed in 9.97s`.

```text
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m mypy src
```

Outcome: sandboxed `ruff` could not create `.ruff_cache` temp files, and sandboxed
`mypy` failed during type checking. Re-running the same checks outside the sandbox
passed:

```text
ruff check: All checks passed!
ruff format --check: 47 files already formatted
mypy src: Success, no issues found in 25 source files
```

```text
git diff --check
```

Outcome: passed.

```text
.\.venv\Scripts\python.exe -m fts_lab.cli fbt atlas-v1-raw-cells
```

Outcome: passed. Fresh raw-cell run:

```text
raw_cell_table_checksum=582e7e50fd8b1bfab149feab6e00d80cd95bda29268ff6fec99e0a5ed4748613
raw_cell_table_path=C:\Users\user\Fitness, Truth & Structure Lab\results\raw\EXP-TASK-004-FBT-ATLAS-V1-RAW-CELLS-20260702T075259Z-9FA13D1D\fbt_atlas_v1_raw_cells.json
manifest_path=C:\Users\user\Fitness, Truth & Structure Lab\experiments\manifests\ART-TASK-004-FBT-ATLAS-V1-RAW-CELLS-MANIFEST-20260702T075259Z-9FA13D1D.json
cell_count=144
```

```text
.\.venv\Scripts\python.exe -m fts_lab.cli fbt atlas-v1-aggregate --raw-cells <fresh raw-cell JSON>
```

Outcome: passed. Fresh aggregate run:

```text
json_report_checksum=5bca8c33d900c5441b5a275ebb6ad5602b10591c7475b6fb035369cb625fa558
json_report_path=C:\Users\user\Fitness, Truth & Structure Lab\results\derived\EXP-TASK-004-FBT-ATLAS-V1-AGGREGATE-20260702T075308Z-E3AD0E8C\fbt_atlas_v1_aggregate.json
markdown_report_checksum=2c69b2254e446b9b628b86673fa4f233e292af1a86610e9447580eb1a801c969
markdown_report_path=C:\Users\user\Fitness, Truth & Structure Lab\results\reports\EXP-TASK-004-FBT-ATLAS-V1-AGGREGATE-20260702T075308Z-E3AD0E8C\fbt_atlas_v1_report.md
manifest_path=C:\Users\user\Fitness, Truth & Structure Lab\experiments\manifests\ART-TASK-004-FBT-ATLAS-V1-AGGREGATE-MANIFEST-20260702T075308Z-E3AD0E8C.json
cell_count=144
```

```text
.\.venv\Scripts\python.exe -m fts_lab.cli validate-manifest <raw manifest>
.\.venv\Scripts\python.exe -m fts_lab.cli validate-manifest <aggregate manifest>
```

Outcome: both manifests valid.

## Source And Claim Boundary

The v1 bundle is correctly marked as `E`, not `R`.

Traceability is consistent:

```text
source_ids = SRC-FBT-2021
claim_ids = CLM-FBT-ATLAS-001
assumption_ids = ASM-FBT-0001, ASM-FBT-0002, ASM-FBT-0003, ASM-FBT-0004
```

`CLM-FBT-THM-001` remains a theorem/source-boundary claim with no production theorem
implementation. The v1 engine and aggregate are linked to `CLM-FBT-ATLAS-001`, not to a
reviewed implementation of Theorem 4.

README, CHANGELOG, `sources/source_map.md`, and `sources/claim_matrix.csv` keep the v1
public claim limited to pending-review design/engine/raw/aggregate work. I found no
claim that v1 is a full atlas run, theorem implementation, source-level probability,
biological result, metaphysical result, ML/RL result, dashboard, or figure.

## Draft Config Audit

`experiments/configs/fbt_atlas_v1_draft.json` preserves the required boundaries:

```text
primary comparison = truth_map vs fitness_only_expected
extension_baselines.enabled = false
extension_baselines_in_primary_results = false
arithmetic = exact_rational
randomness = none
stochastic_simulation = false
disabled = full_atlas_run, stochastic_simulation, ml_rl, ui_dashboard, notebooks, figures
aggregate_label = grid_frequency
denominator_policy = all_enumerated_cells
theorem_probability_claim = false
```

Independent axis count from the config:

```text
axis_lengths = [2, 2, 3, 4, 3, 1]
axis_count = 2 * 2 * 3 * 4 * 3 * 1 = 144
```

## Raw-Cell Engine Audit

`src/fts_lab/fbt/atlas_v1.py` reads the draft config, expands deterministic axis
families, constructs exact rational finite decision problems, evaluates each cell
through the reviewed finite-cell oracle, and writes a raw-cell artifact plus manifest.

The raw artifact preserves raw scope:

```text
artifact_kind = fbt_atlas_v1_raw_cell_table
epistemic_status = E
raw_cell_count = 144
engine_scope.result_level = raw_cells_only
engine_scope.aggregate_report = false
engine_scope.full_grid_run = false
```

The raw JSON does not contain an aggregate `summary` or
`grid_frequencies_by_status`.

Zero-marginal observations remain undefined and are not smoothed with epsilon. MAP ties
are represented through full MAP sets and policy-sensitive cells are kept as explicit
statuses.

## Aggregate/Report Audit

`src/fts_lab/fbt/atlas_v1_aggregate.py` does not import `src/fts_lab/fbt/atlas_v1.py`
or raw-cell enumeration helpers. Its scientific input is one saved raw-cell JSON
artifact supplied through `--raw-cells`.

The aggregate is computed from `cells[*].status`, keeps all raw cells in the
denominator, and writes derived JSON plus Markdown. The derived JSON does not embed the
full raw `cells` table.

The aggregate scope records:

```text
source = raw_cell_artifact_only
recomputes_cells = false
reads_config = false
aggregate_label = grid_frequency
denominator_policy = all_enumerated_cells
denominator_basis = all_raw_cells
blocked_cells_in_denominator = true
tie_sensitive_cells_in_denominator = true
full_grid_run = false
source_theorem_result_claim = false
```

## Independent Data Checks

I recomputed the required data checks from the generated JSON using only the Python
standard library (`json`, `collections.Counter`, `fractions.Fraction`, `pathlib`), with
no import from `fts_lab`.

Results:

```text
raw_cell_count = 144
len(cells) = 144
raw_counts = {
  blocked_zero_marginal: 45,
  map_tie_policy_sensitive: 11,
  same_best_observation: 17,
  truth_decision_tie: 71
}
aggregate_counts = {
  blocked_zero_marginal: 45,
  map_tie_policy_sensitive: 11,
  same_best_observation: 17,
  truth_decision_tie: 71
}
blocked_zero_marginal grid_frequency = 5/16
sum(grid_frequency) = 1
raw_has_summary = false
aggregate_has_cells = false
markdown_has_blocked_row = true
markdown_mentions_no_config = true
```

The required `blocked_zero_marginal = 45` and `45/144 = 5/16` checks passed.

## Manifest Audit

The fresh raw manifest records the config as input and the raw JSON as output:

```text
artifact_kind = fbt_atlas_v1_raw_cell_table
task_ids = TASK-004-FBT-ATLAS-V1-SPEC, TASK-004-FBT-ATLAS-V1-ENGINE
claim_ids = CLM-FBT-ATLAS-001
source_ids = SRC-FBT-2021
assumption_ids = ASM-FBT-0001, ASM-FBT-0002, ASM-FBT-0003, ASM-FBT-0004
git.commit = 8e7399a32029a5726420df82318ae0b141e96e7b
git.dirty = false
dependency_lock_sha256 = 6b81fceadcb3fe17172ce56a239b581332675e7045058459a5871f2982e609c8
inputs = experiments/configs/fbt_atlas_v1_draft.json
outputs = results/raw/.../fbt_atlas_v1_raw_cells.json
```

The fresh aggregate manifest records the raw JSON as input and derived JSON/Markdown as
outputs:

```text
artifact_kind = fbt_atlas_v1_aggregate_report
task_ids = TASK-004-FBT-ATLAS-V1-SPEC, TASK-004-FBT-ATLAS-V1-ENGINE, TASK-004-FBT-ATLAS-V1-AGGREGATE
claim_ids = CLM-FBT-ATLAS-001
source_ids = SRC-FBT-2021
assumption_ids = ASM-FBT-0001, ASM-FBT-0002, ASM-FBT-0003, ASM-FBT-0004
git.commit = 8e7399a32029a5726420df82318ae0b141e96e7b
git.dirty = false
dependency_lock_sha256 = 6b81fceadcb3fe17172ce56a239b581332675e7045058459a5871f2982e609c8
inputs = results/raw/.../fbt_atlas_v1_raw_cells.json
outputs = results/derived/.../fbt_atlas_v1_aggregate.json, results/reports/.../fbt_atlas_v1_report.md
```

Both manifests passed `fts validate-manifest`.

## Fatal Findings

None.

## Major Findings

None.

## Minor Findings

None.

## Verdict

```text
verdict: accepted
fatal_findings: none
major_findings: none
minor_findings: none
review_status_token: REV-TASK-004-FBT-ATLAS-V1-001_no_fatal_or_major
```

The atlas v1 bundle is accepted for the limited reviewed scope: manifest-backed exact
raw-cell tables plus derived status-count/grid_frequency summaries from raw artifacts
only. This verdict does not mark Theorem 4 as implemented or reviewed as a theorem
implementation, and it does not authorize full-atlas, biological, metaphysical, ML/RL,
UI, dashboard, notebook, or figure claims.
