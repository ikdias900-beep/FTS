# TASK-001-SWEEP Independent Review Brief

```text
REVIEW BRIEF ID: REVIEW-BRIEF-TASK-001-SWEEP-001
TARGET TASK ID: TASK-001-SWEEP
EXPECTED REVIEW ID: REV-TASK-001-SWEEP-001
TARGET IMPLEMENTATION COMMIT: 799e51b71627db2521d0d97c9a5a124a0cee3338
REVIEWER ROLE: Fresh-context AI/Codex Verifier
REVIEW MODE: audit first; do not edit implementation before reporting findings
EXPECTED OUTPUT: docs/reviews/REV-TASK-001-SWEEP-001.md
```

## 1. Purpose

Сформировать независимую проверку `TASK-001-SWEEP`: manifest-backed finite-size sweep для Stage 1 FFF counts.

Reviewer должен проверить, что sweep корректно превращает уже реализованные Stage 1 exact helpers в детерминированную long-form CSV таблицу и валидный experiment manifest. Это review не должно заново расширять математическую модель и не должно исправлять код до завершения отчета.

## 2. Context Boundary

Reviewer должен начинать в отдельной сессии или отдельном worktree с новым контекстом.

Reviewer получает только публичные файлы репозитория, первичные источники, task/spec/code/tests и это ТЗ. Reviewer не должен использовать приватную аргументацию implementer-сессии как доказательство корректности.

Разрешено читать `docs/reviews/REV-TASK-001-001.md` только после собственных малых derivations, как исторический контекст по уже принятому `TASK-001`. Нельзя ссылаться на этот review как на oracle для `TASK-001-SWEEP`.

## 3. Required Read Order

1. `AGENTS.md`
2. `01_research_strategy.md`
3. `02_stage_tasks_roles.md`
4. `tasks/TASK-001_stage1_sweeps_tables.md`
5. `sources/source_map.md`
6. `sources/claim_matrix.csv`
7. `assumptions/register.md`
8. `docs/decisions/RDR-0002-total-order-count-presentation.md`
9. `specs/fff/admissibility.md`
10. `specs/fff/total_orders.md`
11. `specs/fff/cyclic_groups.md`
12. Review target code and tests listed below.

## 4. Scope

Review these files:

- `experiments/configs/fff_stage1_small.json`
- `src/fts_lab/fff/sweeps.py`
- `src/fts_lab/cli.py`
- `src/fts_lab/manifests.py`
- `src/fts_lab/doctor.py`
- `experiments/schemas/experiment_manifest.schema.json`
- `tests/exact/test_fff_sweeps.py`
- `tests/integration/test_cli_and_smoke.py`
- `tests/exact/test_fff_admissibility.py`
- `tests/exact/test_fff_total_orders.py`
- `tests/exact/test_fff_cyclic_groups.py`
- `tests/exact/test_fff_formulas_reports.py`
- `tests/properties/test_fff_properties.py`
- `tests/properties/test_manifest_properties.py`

Review may inspect other repository files if needed for traceability, but findings should stay focused on `TASK-001-SWEEP`.

## 5. Out Of Scope

Do not implement or review as part of this task:

- plots, heatmaps, notebooks, reports, or web demo;
- permutation groups;
- measurable spaces;
- FBT;
- evolutionary simulation;
- ML/RL;
- new assumptions or new mathematical definitions;
- philosophical claims about perception, consciousness, spacetime, or reality.

## 6. Independent Derivations Required

Before inspecting `src/fts_lab/fff/sweeps.py` in detail, independently derive at least these small cases without importing production FFF modules:

- admissible payoff-function counts for selected `n,m`, including `n=1,m=1`, `n=2,m=2`, and one asymmetric case such as `n=2,m=3` or `n=3,m=2`;
- total-order source orientation-witness count and distinct unique-function count for `n=2,m=2`;
- why the admissible maximum constant function is counted once as a unique function but twice as preserving/reversing orientation witnesses;
- cyclic homomorphism count for at least `Z_2 -> Z_2`, `Z_3 -> Z_2`, and `Z_4 -> Z_2`;
- the corresponding source ratios over the admissible denominator.

These derivations may be done by hand or with a scratch script that does not import `fts_lab.fff`.

## 7. Audit Questions

Answer these questions explicitly in the review report:

- Does the config declare exactly `TASK-001-SWEEP`, `SRC-FFF-2020`, `ASM-FFF-0001`, and the four expected claim IDs?
- Does the artifact manifest use `artifact_kind: fff_stage1_finite_count_sweep` and artifact-level `epistemic_status: C`?
- Does the CSV preserve per-row `row_epistemic_status` instead of flattening all rows to `C`?
- Are source rows and reconstruction/presentation companion rows distinguishable by `count_object`, `row_epistemic_status`, `assumption_ids`, and `notes`?
- Are both total-order count objects present for every declared `n,m`: `source_orientation_witnesses` and `distinct_unique_functions`?
- Is the cyclic source numerator `gcd(n,m)` kept separate from any admissible-filtered cyclic audit count?
- Does the default config keep `include_admissible_cyclic_audit` false?
- Does the canonical CSV avoid floating-point decimal values?
- Is row ordering deterministic?
- Does the expected 4 by 4 grid produce 112 data rows plus the CSV header?
- Does the manifest record command, parameters, input checksum, output checksum, git state, and `uv.lock` checksum?
- Does checksum validation fail if the CSV bytes are changed?
- Does the CLI command `fts fff sweep --config experiments/configs/fff_stage1_small.json` emit usable artifact paths?
- Does `fts doctor` report the active task and required context consistently?
- Are there any overclaims in README/task/config/notes that go beyond finite count tables?

## 8. Required Commands

Run from a clean checkout of `main` at or after the target implementation commit. If `HEAD` is newer only because it contains this review brief, record both `HEAD` and the target implementation commit in the review report.

```bash
git rev-parse HEAD
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
uv run fts doctor
uv run fts fff sweep --config experiments/configs/fff_stage1_small.json
```

From the sweep command output, capture `manifest_path`, then run:

```bash
uv run fts validate-manifest <manifest_path>
```

For checksum-corruption behavior, do not mutate canonical raw artifacts in place. Either run the existing targeted test:

```bash
uv run pytest tests/integration/test_cli_and_smoke.py::test_stage1_sweep_manifest_validation_fails_after_csv_corruption
```

or copy the generated CSV and manifest to a temporary directory, rewrite the manifest output path to the copy, mutate only the copy, and validate that checksum verification fails.

## 9. Finding Severity

Use these severities:

- `fatal`: implementation cannot be trusted for the task, or traceability/manifest integrity is broken.
- `major`: acceptance criteria fail, row statuses/count objects are misleading, or a public claim would be invalid.
- `minor`: documentation, ergonomics, naming, or coverage gap that does not change scientific meaning.

`TASK-001-SWEEP` is blocked if any `fatal` or `major` finding remains unresolved.

## 10. Required Review Report Format

Create `docs/reviews/REV-TASK-001-SWEEP-001.md` with:

````markdown
# REV-TASK-001-SWEEP-001 - Independent Review of Stage 1 Sweep

```text
REVIEW ID: REV-TASK-001-SWEEP-001
TASK ID: TASK-001-SWEEP
COMMIT REVIEWED: <commit>
REVIEWER ROLE: Fresh-context AI/Codex Verifier
DATE: <YYYY-MM-DD>
VERDICT: accepted / accepted_with_minor_findings / blocked
```

## Context Boundary

## Scope

## Independent Derivations

## Source-To-Code Audit

## CSV And Manifest Audit

## Reproducibility Checks

## Fatal Findings

## Major Findings

## Minor Findings

## Overclaim Audit

## Verdict
````

The report must include enough command output summary for a third party to see what passed, what failed, and which generated manifest was validated.

## 11. Paste Prompt For The Separate Session

```text
You are the Fresh-context AI/Codex Verifier for Fitness, Truth & Structure Lab.

Review TASK-001-SWEEP at target implementation commit 799e51b71627db2521d0d97c9a5a124a0cee3338 using docs/reviews/TASK-001-SWEEP-independent-review-brief.md.

Do not assume the implementation is correct. Do not use production fts_lab.fff modules as your oracle for the required small derivations. Do not edit implementation before you have written the review findings. If you find fatal or major issues, report them and stop; fixes belong to a later implementer pass.

Read the required context files in the order specified by the review brief. Then perform the independent derivations, source-to-code audit, CSV/manifest audit, commands, and overclaim audit. Write the result to docs/reviews/REV-TASK-001-SWEEP-001.md.
```
