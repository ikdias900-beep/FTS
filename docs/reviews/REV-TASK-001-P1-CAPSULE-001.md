# REV-TASK-001-P1-CAPSULE-001 - Independent Review of Stage 1 Draft Release Capsule

```text
REVIEW ID: REV-TASK-001-P1-CAPSULE-001
TASK ID: TASK-001-P1-CAPSULE
COMMIT REVIEWED: c077593ed8565ba727a4658738e021be741d8ed6
REVIEWER ROLE: Fresh-context AI/Codex Verifier
DATE: 2026-06-26
VERDICT: accepted_with_minor_findings
```

## Scope

Reviewed the Stage 1 P1 draft release capsule for packaging, provenance, checksums, license state, manifest validity, and claim boundaries. This review did not validate new mathematical theorems, add scientific claims, or review out-of-scope work such as FBT, evolution, ML/RL, permutation groups, measurable spaces, browser demos, DOI archiving, or figures.

The target implementation commit from the brief is `c077593ed8565ba727a4658738e021be741d8ed6`. The current command context at review time was `da7598b61afae732f1751579320eda2fd892ce0c`, whose only committed difference from the target was the independent review brief file.

## Commands Run

```text
git rev-parse HEAD
da7598b61afae732f1751579320eda2fd892ce0c

git merge-base --is-ancestor c077593ed8565ba727a4658738e021be741d8ed6 HEAD
exit code 0

git diff --stat c077593ed8565ba727a4658738e021be741d8ed6..HEAD
docs/reviews/TASK-001-P1-CAPSULE-independent-review-brief.md | 144 +++++++++++++++++++++

py -m uv run fts doctor --release-check
passed; Active task: TASK-001-P1-CAPSULE; license_decision: resolved

py -m uv run fts validate-manifest release/stage1-p1-draft/manifests/ART-TASK-001-SWEEP-MANIFEST-20260625T192538Z-FBD5EA2B.json
manifest valid

py -m uv run fts validate-manifest release/stage1-p1-draft/manifests/ART-TASK-001-PUBTABLES-MANIFEST-20260625T192546Z-D763EFE3.json
manifest valid

py -m uv run ruff check .
All checks passed!

py -m uv run ruff format --check .
25 files already formatted

py -m uv run mypy src
Success: no issues found in 14 source files

py -m uv run pytest
197 passed in 8.29s

git status --short
clean before this report was created
```

Additional audit commands checked `git ls-files release/stage1-p1-draft`, independently hashed every `checksums.txt` entry, compared capsule copies with the original manifest output paths, scanned forbidden-claim terms, and read PR #6 metadata through the public GitHub API because `gh` is not installed in this PowerShell environment.

## License And Provenance Audit

`RDR-0001-license` is `APPROVED` and explicitly selects the MIT License for project-authored repository contents. The root `LICENSE` contains the standard MIT text and the approved copyright notice:

```text
Copyright (c) 2026 Fitness, Truth & Structure Lab contributors
```

The capsule documents correctly state that external primary sources, publisher content, third-party packages, and other non-project-authored materials are not relicensed.

The PR #6 body at `https://github.com/ikdias900-beep/FTS/pull/6` records the same generated artifact checksums as the capsule:

```text
raw sweep CSV: 6f391a2891e1274d2e1b8240cbc35329bbe6a40326f71ba20b04f642263d5bab
derived publication CSV: a0295ae0a52fb558c2116481da46fa449c622ea83e86c4f989b0b958479a9d51
generated report: 2e349b9c299d81ee261da929738e5c98fb743a0bdc021057b2b02f4ae8253877
```

## Manifest And Checksum Audit

Both copied manifests validate successfully. They retain the original absolute paths for generated artifacts, and `release/stage1-p1-draft/README.md` explicitly tells reviewers that capsule copies are verified by `checksums.txt`.

Independent checksum verification found:

```text
listed_count=13
committed_excluding_checksums=13
mismatch_count=0
unlisted_committed_count=0
listed_not_committed_count=0
```

Direct manifest-output-to-capsule-copy comparisons also matched:

```text
raw sweep csv: match=True
derived publication csv: match=True
generated publication report: match=True
sweep manifest copy: match=True
publication manifest copy: match=True
```

The archived raw CSV has the expected 112 data rows for the `4 x 4` grid and preserves row-level `R` and `C` statuses. The derived publication CSV has 16 data rows and preserves per-column status distinctions. Total-order source orientation-witness counts remain separate from `RDR-0002` distinct unique-function companion counts.

## Claim Boundary Audit

`CLAIMS.md`, `LIMITATIONS.md`, `REVIEW_REPORT.md`, the release README, and the generated Markdown table stay within the approved Stage 1 boundary:

- linked source: `SRC-FFF-2020`;
- linked claims: `CLM-FFF-ADM-001`, `CLM-FFF-ORD-001`, `CLM-FFF-CYC-001`, `CLM-FFF-CYC-002`;
- linked assumption: `ASM-FFF-0001`;
- linked decisions: `RDR-0001-license`, `RDR-0002`.

The capsule preserves the `R/C` distinction and explicitly states that the draft is not a GitHub release, DOI archive, archival deposit, browser demo, figure package, or final public P1 publication. Searches for forbidden sensitive topics found them only in limitations or forbidden-claim language, not as positive claims.

## Fatal Findings

None.

## Major Findings

None.

## Minor Findings

1. The command context was `da7598b61afae732f1751579320eda2fd892ce0c`, while the brief's target implementation commit is `c077593ed8565ba727a4658738e021be741d8ed6`. The only committed difference before this report was the review brief itself, so this does not affect the release-capsule artifact audit.

2. The GitHub CLI `gh` is not installed in this shell. PR metadata and PR body checks were performed through the public GitHub API instead.

## Verdict

`TASK-001-P1-CAPSULE` is accepted with minor findings. There are no unresolved fatal or major findings.

The draft release capsule has the required files, validates both archived manifests, matches all capsule checksums, preserves raw and derived artifact provenance, keeps the `R/C` and `RDR-0002` total-order count distinctions visible, records the approved MIT license state, and avoids overclaims outside the approved Stage 1 claim boundary. The capsule is sufficient for draft release-capsule review even though it is not yet a GitHub release, DOI archive, browser demo, figure package, or full P1 publication.
