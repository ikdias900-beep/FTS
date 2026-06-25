# REV-TASK-001-PUBTABLES-001 Follow-Up Verification

```text
REVIEW ID: REV-TASK-001-PUBTABLES-001-FOLLOWUP
TASK ID: TASK-001-PUBTABLES
RELATED REVIEW: REV-TASK-001-PUBTABLES-001
BASE REVIEW VERDICT: blocked
FOLLOW-UP DATE: 2026-06-25
FOLLOW-UP TYPE: implementer-side verification after fix
FOLLOW-UP VERDICT: major finding appears fixed; requires fresh-context re-review to close the formal gate
```

## Context Boundary

This follow-up was performed in the same session that implemented the fix for the major finding in `REV-TASK-001-PUBTABLES-001`. It is therefore not a fresh-context independent review. It records post-fix evidence for the later reviewer and should not by itself satisfy the project rule requiring independent verification before release.

## Original Major Finding

`src/fts_lab/fff/publication_tables.py` accepted a source sweep manifest whose `task_ids` did not equal `["TASK-001-SWEEP"]`. A manifest with correct artifact kind, claims, source IDs, assumptions, and checksums, but with `task_ids=["TASK-BOGUS"]`, could still produce a publication-table package.

This was a traceability defect: the generated numeric table could be correct, but the publication command did not enforce that the source artifact came from the reviewed `TASK-001-SWEEP` lineage.

## Fix Summary

The publication-table input validation now imports `EXPECTED_TASK_IDS` from `fts_lab.fff.sweeps` and requires the source manifest's `task_ids` to match exactly.

A regression test was added:

```text
tests/integration/test_cli_and_smoke.py::test_stage1_publication_tables_rejects_manifest_with_wrong_source_task
```

The test copies a valid sweep manifest, changes only `task_ids` to `["TASK-BOGUS"]`, and verifies that `fts fff publication-tables` exits nonzero with:

```text
task_ids must be exactly ['TASK-001-SWEEP']
```

## Commands Run

```text
py -m uv run pytest tests/integration/test_cli_and_smoke.py::test_stage1_publication_tables_rejects_manifest_with_wrong_source_task tests/integration/test_cli_and_smoke.py::test_stage1_publication_tables_cli_writes_outputs_and_valid_manifest
2 passed

py -m uv run ruff check .
All checks passed!

py -m uv run ruff format --check .
25 files already formatted

py -m uv run mypy src
Success: no issues found in 14 source files

py -m uv run pytest
197 passed

py -m uv run fts doctor
exit_code=0
active_task=TASK-001-PUBTABLES
dirty=True
license_decision=pending; public release blocked
```

Bare `uv` remains unavailable on this PowerShell `PATH`, so the documented Windows fallback `py -m uv` was used.

## Post-Fix Artifact Verification

Valid source sweep:

```text
sweep_manifest_path=C:\Users\user\Fitness, Truth & Structure Lab\experiments\manifests\ART-TASK-001-SWEEP-MANIFEST-20260625T084456Z-10426524.json
sweep_csv_path=C:\Users\user\Fitness, Truth & Structure Lab\results\raw\EXP-TASK-001-SWEEP-20260625T084456Z-10426524\fff_stage1_counts.csv
sweep_csv_checksum=6f391a2891e1274d2e1b8240cbc35329bbe6a40326f71ba20b04f642263d5bab
sweep_row_count=112
validate_sweep_manifest=passed
```

Derived publication package from that valid sweep:

```text
publication_manifest_path=C:\Users\user\Fitness, Truth & Structure Lab\experiments\manifests\ART-TASK-001-PUBTABLES-MANIFEST-20260625T084517Z-362636D5.json
summary_csv_path=C:\Users\user\Fitness, Truth & Structure Lab\results\derived\EXP-TASK-001-PUBTABLES-20260625T084517Z-362636D5\stage1_fff_publication_counts.csv
report_path=C:\Users\user\Fitness, Truth & Structure Lab\results\reports\EXP-TASK-001-PUBTABLES-20260625T084517Z-362636D5\stage1_fff_publication_tables.md
summary_csv_checksum=fc8010a476c4233720c7125e9474b6a11dbea3501a93f0a32cb940751e727742
report_checksum=72e182723b91212b6b16fc70dad103386906ac2f76398afbe56c5a6915b8ab5c
row_count=16
validate_publication_manifest=passed
```

Negative source-task check:

```text
temp_manifest=C:\Users\user\AppData\Local\Temp\fts_pubtables_bad_task_manifest_followup.json
change_applied=task_ids -> ["TASK-BOGUS"]
command=py -m uv run fts fff publication-tables --sweep-manifest <temp_manifest>
exit_code=1
stdout=fff failed: task_ids must be exactly ['TASK-001-SWEEP']
```

## Residual Findings

No residual failure was observed for the original major finding in this implementer-side verification.

This follow-up does not close the formal independent-review requirement. A fresh-context reviewer should rerun the negative source-task check and decide whether to update the final `TASK-001-PUBTABLES` review gate to accepted or accepted with minor findings.
