# TASK-000 — Bootstrap the Research Repository

```text
TASK ID: TASK-000
STAGE: 0 — Research infrastructure and reproducibility contract
EPISTEMIC STATUS: N/A — infrastructure only; no scientific claim
OWNER: Codex Implementer
REVIEWER: Fresh-context AI/Codex Verifier
STATUS: READY
```

## 1. Objective

Create the initial repository for **Fitness, Truth & Structure Lab** so later AI-generated scientific code can be audited, reproduced, and reviewed.

This task is successful when a clean checkout can install the project, run quality gates, execute one deterministic infrastructure smoke run, validate its manifest, and reproduce the same payload checksum.

This task does **not** implement or test FBT, FFF, evolutionary dynamics, or ML.

## 2. Required input files

Read and preserve:

- `AGENTS.md`;
- `01_research_strategy.md`;
- `02_stage_tasks_roles.md`;
- `tasks/TASK-000_bootstrap_repo.md`;
- `sources/source_map.md`;
- `sources/claim_matrix.csv`;
- `assumptions/register.md`.

If the two strategy files were imported with `(1)` suffixes, create canonical copies without the suffix and do not alter their content.

## 3. Human decisions that must not be invented

Do not choose on behalf of the Human Principal Investigator:

- the final software license;
- whether the repository is public or private;
- whether complete AI conversation/review logs will be published;
- the final project URL or archival service.

If no license decision exists, create `docs/decisions/RDR-0001-license.md` with status `PENDING` and state that public release remains blocked. Do not insert an arbitrary license.

## 4. Required repository structure

Create at least:

```text
fitness-truth-structure-lab/
├── AGENTS.md
├── 01_research_strategy.md
├── 02_stage_tasks_roles.md
├── README.md
├── CHANGELOG.md
├── pyproject.toml
├── uv.lock
├── .gitignore
├── .editorconfig
├── .pre-commit-config.yaml
├── tasks/
│   └── TASK-000_bootstrap_repo.md
├── sources/
│   ├── source_map.md
│   ├── claim_matrix.csv
│   └── bibliography.bib
├── specs/
│   ├── epistemic_status.md
│   └── notation.md
├── assumptions/
│   ├── register.md
│   └── decisions/
├── docs/
│   ├── decisions/
│   ├── templates/
│   │   ├── claim_card.md
│   │   ├── assumption_record.md
│   │   ├── research_decision_record.md
│   │   ├── independent_review.md
│   │   └── publication_checklist.md
│   └── reproducibility.md
├── src/fts_lab/
│   ├── __init__.py
│   ├── cli.py
│   ├── doctor.py
│   ├── manifests.py
│   └── smoke.py
├── tests/
│   ├── unit/
│   ├── properties/
│   └── integration/
├── experiments/
│   ├── configs/
│   │   └── smoke.json
│   ├── schemas/
│   │   └── experiment_manifest.schema.json
│   └── manifests/
├── results/
│   ├── raw/
│   ├── derived/
│   └── reports/
├── .github/
│   ├── workflows/ci.yml
│   ├── ISSUE_TEMPLATE/
│   └── pull_request_template.md
└── Makefile
```

Empty data directories may contain `.gitkeep`. Do not create `notebooks/`, `web/`, `ml/`, or scientific implementation modules during this task.

## 5. Tooling baseline

Use:

- Python `>=3.12,<3.13` for the initial reference environment;
- `uv` for environment management and locking;
- `pytest` and `hypothesis`;
- `ruff`;
- `mypy`;
- `pre-commit`;
- a minimal JSON Schema validator for experiment manifests.

Implement the CLI through the standard library (`argparse`) unless a runtime dependency has a clear documented benefit. Expose:

```bash
fts doctor
fts reproduce-smoke
fts validate-manifest PATH
```

## 6. Infrastructure smoke run

Implement a deterministic, scientifically content-free smoke operation.

Suggested behavior:

1. Read `experiments/configs/smoke.json` containing a small integer list.
2. Compute a deterministic payload such as count, sum, and SHA-256 of canonical input bytes.
3. Write a raw result under a run-specific directory in `results/raw/`.
4. Write a manifest under `experiments/manifests/`.
5. Validate the manifest against the JSON Schema.
6. Print the payload checksum and artifact paths.

The smoke run must use:

```json
{
  "artifact_kind": "infrastructure_smoke",
  "epistemic_status": null,
  "claim_ids": [],
  "source_ids": [],
  "assumption_ids": [],
  "task_ids": ["TASK-000"]
}
```

It must not mention FBT, FFF, perception, fitness, truth, evolution, or consciousness in its result payload.

## 7. Manifest requirements

The machine-readable manifest must include at least:

- `schema_version`;
- `manifest_id` and `run_id`;
- `artifact_kind`;
- nullable `epistemic_status`;
- `task_ids`, `claim_ids`, `source_ids`, `assumption_ids`;
- UTC creation time;
- exact command;
- parameters and explicit seed field (`null` for deterministic smoke);
- Git commit, branch/detached status, and dirty flag;
- Python version, platform, and dependency-lock SHA-256;
- input and output paths with SHA-256 checksums;
- completion status and error field;
- implementation/package version.

Canonical JSON serialization must be deterministic. The scientific/data payload must reproduce byte-for-byte; the run manifest may differ in timestamp, run ID, absolute paths, and environment metadata.

## 8. `fts doctor`

`fts doctor` must report, in human-readable form and optionally JSON:

- project root;
- Python and uv availability/version;
- package version;
- Git commit and dirty state;
- presence of every required context file;
- lockfile presence and checksum;
- write access to artifact directories;
- manifest schema availability;
- active task (`TASK-000`);
- unresolved release blocker if the license is pending.

Exit non-zero for a broken required condition. A pending license is a warning for development and an error only for a release-check mode.

## 9. Quality commands

Provide working commands, directly and through `Makefile`:

```bash
uv sync --all-groups
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
uv run fts doctor
uv run fts reproduce-smoke
```

CI must run from a clean checkout without network access during tests after dependencies are installed.

## 10. Required tests

At minimum:

### Unit

- canonical JSON serialization is stable;
- SHA-256 helper returns known digests;
- manifest model rejects unknown epistemic values;
- infrastructure manifest accepts `epistemic_status: null` only with no claims;
- scientific manifest rejects missing claim/source linkage;
- output overwrite is refused by default.

### Property-based

- canonical serialization is invariant to input dictionary insertion order;
- equivalent relative path representations normalize consistently;
- checksum validation detects any payload mutation.

### Integration

- `fts doctor` succeeds in a valid checkout;
- smoke run writes payload and valid manifest;
- two smoke runs from the same config yield identical payload checksums;
- manifest validation fails after deliberate artifact corruption;
- context-file checker detects a missing required file.

## 11. Templates and registries

Create templates consistent with the two strategy documents:

- Claim Card;
- Assumption Record;
- Research Decision Record;
- Independent Review Report with `fatal`, `major`, and `minor` findings;
- Publication Checklist.

Validate on CI that:

- `sources/claim_matrix.csv` is parseable UTF-8 CSV;
- all `source_id` values used by claims exist in `sources/source_map.md`;
- all non-empty `assumption_ids` used by claims exist in `assumptions/register.md`;
- IDs are unique.

Do not modify the initial scientific claims merely to make validation convenient.

## 12. Documentation requirements

`README.md` must explain:

- the project mission in restrained terms;
- current status: Stage 0 only;
- installation and quality commands;
- how to run and verify the smoke artifact;
- epistemic statuses R/C/E/A;
- that the project does not prove Hoffman's metaphysical proposals;
- links to the strategy, roles, source map, claim matrix, assumptions, and current task.

`docs/reproducibility.md` must describe artifact immutability, checksums, manifests, exact oracles, independent review, and clean-room reproduction.

## 13. Explicitly out of scope

Do not:

- implement any formula from FBT or FFF;
- download or commit paper PDFs;
- add notebooks, plotting libraries, web frameworks, ML libraries, or GPU dependencies;
- implement evolutionary algorithms or agent simulations;
- create scientific figures or datasets;
- claim that any theorem has been reproduced;
- edit `01_research_strategy.md` or `02_stage_tasks_roles.md`;
- select a license without human approval;
- publish or push to a remote unless explicitly requested.

## 14. Acceptance criteria

`TASK-000` is complete only when:

1. all required context files exist at canonical paths;
2. `uv sync --all-groups` succeeds;
3. lint, format check, typing, and all tests pass;
4. `fts doctor` reports a healthy development checkout;
5. `fts reproduce-smoke` creates an immutable payload and valid manifest;
6. a second run reproduces the same payload checksum;
7. corrupting an artifact causes validation failure;
8. CI is green from a clean checkout;
9. no scientific implementation or claim was introduced;
10. a fresh-context reviewer produces `REV-TASK-000-001` with no unresolved fatal or major findings.

## 15. Completion report

Return a concise report containing:

- repository tree summary;
- files created/changed;
- commands and results;
- smoke payload checksum and manifest path;
- Git/lock metadata captured;
- context/registry validation results;
- pending RDRs and assumptions;
- review status;
- confirmation that scientific claims produced = none.
