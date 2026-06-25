# TASK-001-P1-CAPSULE Independent Review Brief

```text
REVIEW BRIEF ID: REVIEW-BRIEF-TASK-001-P1-CAPSULE-001
TARGET TASK ID: TASK-001-P1-CAPSULE
EXPECTED REVIEW ID: REV-TASK-001-P1-CAPSULE-001
TARGET IMPLEMENTATION COMMIT: c077593ed8565ba727a4658738e021be741d8ed6
EXPECTED OUTPUT: docs/reviews/REV-TASK-001-P1-CAPSULE-001.md
```

## Reviewer Role

You are an independent verifier for a computational research repository. Start from the repository files and this brief. Do not assume the release capsule is correct because the implementer says it is correct.

This review validates release packaging, provenance, checksums, licensing state, and claim boundaries. It does not validate new mathematical theorems and must not introduce new scientific claims.

## Required Read Order

1. `AGENTS.md`
2. `01_research_strategy.md`
3. `02_stage_tasks_roles.md`
4. `tasks/TASK-001_p1_release_capsule.md`
5. `sources/source_map.md`
6. `sources/claim_matrix.csv`
7. `assumptions/register.md`
8. `docs/decisions/RDR-0001-license.md`
9. `docs/decisions/RDR-0002-total-order-count-presentation.md`
10. `release/stage1-p1-draft/README.md`
11. `release/stage1-p1-draft/CLAIMS.md`
12. `release/stage1-p1-draft/LIMITATIONS.md`
13. `release/stage1-p1-draft/ASSUMPTIONS.md`
14. `release/stage1-p1-draft/REVIEW_REPORT.md`
15. `release/stage1-p1-draft/reproduction_commands.md`
16. `release/stage1-p1-draft/checksums.txt`

Historical review context:

- `docs/reviews/REV-TASK-001-001.md`
- `docs/reviews/REV-TASK-001-SWEEP-001.md`
- `docs/reviews/REV-TASK-001-PUBTABLES-001.md`

Treat these as review history, not as an oracle for this capsule.

## Files To Inspect

- `LICENSE`
- `README.md`
- `CHANGELOG.md`
- `sources/source_map.md`
- `src/fts_lab/doctor.py`
- `tests/integration/test_cli_and_smoke.py`
- `tasks/TASK-001_p1_release_capsule.md`
- every file under `release/stage1-p1-draft/`

## Required Checks

Run or independently reproduce equivalent checks:

```bash
py -m uv run fts doctor --release-check
py -m uv run fts validate-manifest release/stage1-p1-draft/manifests/ART-TASK-001-SWEEP-MANIFEST-20260625T192538Z-FBD5EA2B.json
py -m uv run fts validate-manifest release/stage1-p1-draft/manifests/ART-TASK-001-PUBTABLES-MANIFEST-20260625T192546Z-D763EFE3.json
py -m uv run ruff check .
py -m uv run ruff format --check .
py -m uv run mypy src
py -m uv run pytest
```

Verify `release/stage1-p1-draft/checksums.txt` independently by hashing every listed file and confirming there are no unlisted committed files under `release/stage1-p1-draft/` except `checksums.txt`.

## Audit Questions

1. Does `RDR-0001-license` approve MIT, and is the root `LICENSE` consistent with that decision?
2. Does `fts doctor --release-check` pass and report `TASK-001-P1-CAPSULE`?
3. Do both copied manifests validate?
4. Do the release-capsule checksums match every archived file?
5. Are the copied raw and derived data files the same content recorded by the manifests and the PR body?
6. Does the capsule clearly state that copied manifests retain original absolute paths while capsule copies are verified by `checksums.txt`?
7. Do `CLAIMS.md`, `LIMITATIONS.md`, and `REVIEW_REPORT.md` avoid overclaims about human perception, consciousness, spacetime, ontology, FBT, evolution, ML/RL, permutation groups, measurable spaces, browser demos, figures, DOI, or final public release?
8. Does the capsule preserve the `R/C` distinction and `RDR-0002` side-by-side total-order count decision?
9. Are there any untracked or generated files required to reproduce the capsule but absent from the PR?
10. Is the capsule sufficient for a draft release-capsule review, even though it is not yet a GitHub release, DOI archive, browser demo, or full P1 publication?

## Blocking Criteria

Mark the review `blocked` if any `fatal` or `major` finding remains unresolved.

Fatal examples:

- incorrect or missing license decision for release;
- checksum mismatch in archived release files;
- manifest validation failure;
- a public claim outside the approved `CLM-...` rows;
- missing required capsule files: `CLAIMS.md`, `LIMITATIONS.md`, or `REVIEW_REPORT.md`.

Major examples:

- capsule data not traceable to the reviewed sweep/publication manifests;
- `fts doctor --release-check` fails;
- copied data differs from recorded manifest outputs without explanation;
- release docs imply a final public release, DOI, or browser demo exists when it does not.

Minor examples:

- wording could be clearer without changing claim boundaries;
- local environment uses `py -m uv` instead of bare `uv`;
- non-blocking formatting or organization improvements.

## Expected Review Report

Create `docs/reviews/REV-TASK-001-P1-CAPSULE-001.md` with:

````markdown
# REV-TASK-001-P1-CAPSULE-001 - Independent Review of Stage 1 Draft Release Capsule

```text
REVIEW ID: REV-TASK-001-P1-CAPSULE-001
TASK ID: TASK-001-P1-CAPSULE
COMMIT REVIEWED: <commit>
REVIEWER ROLE: Fresh-context AI/Codex Verifier
DATE: <YYYY-MM-DD>
VERDICT: accepted | accepted_with_minor_findings | blocked
```

## Scope

## Commands Run

## License And Provenance Audit

## Manifest And Checksum Audit

## Claim Boundary Audit

## Fatal Findings

## Major Findings

## Minor Findings

## Verdict
````

If the verdict is accepted or accepted with minor findings and there are no unresolved fatal or major findings, `TASK-001-P1-CAPSULE` may be moved out of draft and merged.
