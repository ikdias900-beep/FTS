# TASK-001-PUBTABLES Independent Review Brief

```text
REVIEW BRIEF ID: REVIEW-BRIEF-TASK-001-PUBTABLES-001
TARGET TASK ID: TASK-001-PUBTABLES
EXPECTED REVIEW ID: REV-TASK-001-PUBTABLES-001
TARGET IMPLEMENTATION COMMIT: d6ff498a2e526b21374825c831a8a10eb7405708
TARGET PR: https://github.com/ikdias900-beep/FTS/pull/5
REVIEWER ROLE: Fresh-context AI/Codex Verifier
REVIEW MODE: audit first; do not edit implementation before reporting findings
EXPECTED OUTPUT: docs/reviews/REV-TASK-001-PUBTABLES-001.md
```

## Purpose

Review `TASK-001-PUBTABLES`, the manifest-backed derived publication table package for Stage 1 FFF finite counts.

Verify that the implementation builds a derived publication package only from a validated `TASK-001-SWEEP` manifest/CSV, preserves exact values, traceability, checksums, and per-column `R/C` statuses, and adds no new scientific claims.

This review does not validate new mathematical theorems. It validates derived artifact provenance, status preservation, documentation boundaries, and release readiness for this publication-table block.

## Context Boundary

The reviewer must start in a separate session or worktree with fresh context. Use only public repository files, task/spec/code/tests, generated artifacts from commands, and this brief. Do not use private implementer rationale as evidence.

Previous reports `REV-TASK-001-001` and `REV-TASK-001-SWEEP-001` may be read as historical context, but they are not an oracle for `TASK-001-PUBTABLES`.

## Required Read Order

1. `AGENTS.md`
2. `01_research_strategy.md`
3. `02_stage_tasks_roles.md`
4. `tasks/TASK-001_publication_tables_docs.md`
5. `sources/source_map.md`
6. `sources/claim_matrix.csv`
7. `assumptions/register.md`
8. `docs/decisions/RDR-0002-total-order-count-presentation.md`
9. `docs/reviews/REV-TASK-001-SWEEP-001.md`
10. `docs/research_notes/stage1_publication_tables.md`

## Scope

Review these files, plus nearby code if needed for traceability:

- `src/fts_lab/fff/publication_tables.py`
- `src/fts_lab/fff/sweeps.py`
- `src/fts_lab/cli.py`
- `src/fts_lab/manifests.py`
- `src/fts_lab/doctor.py`
- `tests/exact/test_fff_publication_tables.py`
- `tests/exact/test_fff_sweeps.py`
- `tests/integration/test_cli_and_smoke.py`
- `tasks/TASK-001_publication_tables_docs.md`
- `docs/research_notes/stage1_publication_tables.md`
- `README.md`
- `CHANGELOG.md`
- `sources/source_map.md`

Out of scope: plots, notebooks, web demo, FBT, evolution, ML/RL, permutation groups, measurable spaces, new assumptions, new mathematical definitions, and philosophical claims.

## Independent Checks Required

Before using `src/fts_lab/fff/publication_tables.py` as evidence, independently state what a correct transformation must do:

- read one validated `TASK-001-SWEEP` manifest;
- use the sweep CSV listed in that manifest output;
- group 112 long-form sweep rows into 16 wide rows for the default `4 x 4` grid;
- preserve source sweep manifest ID and run ID in every wide row;
- preserve exact integer and rational string values without floats;
- preserve per-column statuses instead of flattening the table to `C`;
- keep total-order source orientation-witness values separate from distinct unique-function companion values;
- keep cyclic source homomorphism values separate from admissible-filtered audit values;
- write a derived manifest whose inputs include both the source sweep manifest and source sweep CSV;
- write outputs for both the derived CSV and generated Markdown report.

Verify at least these generated-artifact cases without importing `fts_lab.fff.publication_tables` as the oracle:

- derived CSV has exactly 16 data rows plus header;
- generated Markdown report has the same 16 `(n,m)` table rows;
- `(n,m)=(2,2)`: admissible `3`, order witness count `4`, order witness ratio `4/3`, unique order count `3`, unique order ratio `1`, cyclic count `2`, cyclic ratio `2/3`;
- `(n,m)=(4,4)`: admissible `175`, order witness count `40`, order witness ratio `8/35`, unique order count `39`, unique order ratio `39/175`, cyclic count `4`, cyclic ratio `4/175`.

## Audit Questions

Answer explicitly:

- Does the package depend only on reviewed `TASK-001-SWEEP` outputs, not hidden hand-edited data?
- Does the publication command fail on non-sweep manifests?
- Does the derived manifest use `artifact_kind: fff_stage1_publication_tables` and artifact-level `epistemic_status: C`?
- Does the derived manifest list exactly `TASK-001-PUBTABLES`, `SRC-FFF-2020`, `ASM-FFF-0001`, and the four expected claim IDs?
- Do manifest inputs include both the source sweep manifest and source sweep CSV?
- Do manifest outputs include both the derived CSV and generated Markdown report?
- Does the derived CSV preserve source sweep manifest/run IDs in every row?
- Does the derived CSV have one row per declared `(n,m)` pair for the default `4 x 4` grid?
- Does the derived CSV preserve per-column statuses for source reproduction columns and `RDR-0002` companion columns?
- Does the generated report explain provenance, status legend, allowed claims, and forbidden claims?
- Does the generated report avoid biological-probability, human-perception, and metaphysical overclaims?
- Does checksum validation fail if a derived output copy is mutated?
- Does `fts doctor` report `TASK-001-PUBTABLES` and all required context files?
- Does PR #5 remain draft/blocked from merge until this review has no fatal or major findings?

## Required Commands

Run from a clean checkout of PR #5 or a branch at/after the target implementation commit.

```bash
git rev-parse HEAD
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
uv run fts doctor
uv run fts fff sweep --config experiments/configs/fff_stage1_small.json
```

From the sweep output, capture `manifest_path`, then run:

```bash
uv run fts validate-manifest <sweep-manifest-path>
uv run fts fff publication-tables --sweep-manifest <sweep-manifest-path>
```

From the publication output, capture `manifest_path`, then run:

```bash
uv run fts validate-manifest <publication-manifest-path>
```

If bare `uv` is unavailable, use `py -m uv run ...` and record that environment detail.

For checksum-corruption behavior, run:

```bash
uv run pytest tests/integration/test_cli_and_smoke.py::test_stage1_publication_tables_manifest_validation_fails_after_output_corruption
```

or copy generated outputs and manifest to a temp directory, rewrite the copied manifest output path, mutate only the copy, and verify checksum failure.

## Finding Severity

- `fatal`: derived publication artifacts cannot be trusted, manifest integrity is broken, or implementation fabricates/hand-edits scientific values.
- `major`: acceptance criteria fail, status/provenance is misleading, source and companion counts are conflated, or documentation makes an invalid scientific claim.
- `minor`: documentation, ergonomics, naming, or coverage gap that does not change scientific meaning or artifact integrity.

`TASK-001-PUBTABLES` is blocked if any `fatal` or `major` finding remains unresolved.

## Required Review Report Format

Create `docs/reviews/REV-TASK-001-PUBTABLES-001.md` with:

````markdown
# REV-TASK-001-PUBTABLES-001 - Independent Review of Stage 1 Publication Tables

```text
REVIEW ID: REV-TASK-001-PUBTABLES-001
TASK ID: TASK-001-PUBTABLES
COMMIT REVIEWED: <commit>
TARGET IMPLEMENTATION COMMIT: d6ff498a2e526b21374825c831a8a10eb7405708
REVIEWER ROLE: Fresh-context AI/Codex Verifier
DATE: <YYYY-MM-DD>
VERDICT: accepted / accepted_with_minor_findings / blocked
```

## Context Boundary

## Scope

## Independent Transformation Expectations

## Generated Artifact Audit

## Source-To-Code Audit

## CSV And Report Audit

## Manifest And Checksum Audit

## Reproducibility Checks

## Fatal Findings

## Major Findings

## Minor Findings

## Overclaim Audit

## Verdict
````

The report must summarize command outcomes, the sweep manifest used, the publication manifest validated, and produced checksums.

## Paste Prompt For The Separate Session

```text
You are the Fresh-context AI/Codex Verifier for Fitness, Truth & Structure Lab.

Review TASK-001-PUBTABLES at target implementation commit d6ff498a2e526b21374825c831a8a10eb7405708 using docs/reviews/PUBTABLES-review-brief.md.

Do not assume the implementation is correct. Do not use src/fts_lab/fff/publication_tables.py as your oracle for the required transformation checks. Do not edit implementation before you have written the review findings. If you find fatal or major issues, report them and stop; fixes belong to a later implementer pass.

Read the required context files in the order specified by the review brief. Then perform the independent transformation expectations, generated artifact audit, source-to-code audit, CSV/report audit, manifest/checksum audit, required commands, and overclaim audit. Write the result to docs/reviews/REV-TASK-001-PUBTABLES-001.md.
```
