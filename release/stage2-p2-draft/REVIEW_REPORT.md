# Review Report

## Review Summary

This capsule received independent review in `REV-TASK-002-FBT-NUMERICAL-001`.
The review verdict was `accepted_with_minor_findings`.

| Review ID | Scope | Verdict | Unresolved fatal | Unresolved major |
|---|---|---|---:|---:|
| `REV-TASK-002-FBT-NUMERICAL-001` | Stage 2 FBT numerical appendix reproduction and checkpoint capsule | `accepted_with_minor_findings` | 0 | 0 |

## Automated Checks Already Run

- `py -m uv run ruff check .`
- `py -m uv run ruff format --check .`
- `py -m uv run mypy src`
- `py -m uv run pytest`
- `py -m uv run fts doctor --release-check`
- `py -m uv run fts fbt reproduce-numerical-example`
- `py -m uv run fts validate-manifest experiments/manifests/ART-TASK-002-FBT-NUMERICAL-MANIFEST-20260625T222000Z-2A277325.json`
- `py -m uv run fts validate-manifest release/stage2-p2-draft/manifests/ART-TASK-002-FBT-NUMERICAL-MANIFEST-20260625T222000Z-2A277325.json`
- `py -m uv run fts validate-release-capsule release/stage2-p2-draft`

## Independent Review Findings

The reviewer independently confirmed:

- source transcription from `SRC-FBT-2021` into `specs/fbt/numerical_appendix.md`;
- likelihood-table orientation;
- exact Bayes calculations for marginals and posteriors;
- expected-fitness calculations from the same source input objects;
- absence of hard-coded target results in production implementation;
- explicit rejection of unresolved MAP-tie and zero-marginal edge cases;
- generated and copied manifests validate;
- copied raw and derived data checksums match `checksums.txt`;
- claims and limitations stay inside the Stage 2 numerical appendix boundary.

The review found no fatal findings and no major findings.

## Minor Findings

1. The copied release manifest under `release/stage2-p2-draft/manifests/`
   preserves original absolute input/output paths outside the release capsule.
   The capsule remains independently verifiable through committed raw/derived
   files and `checksums.txt`. A future release-local manifest or
   archive-validation mode would make this more portable.

Follow-up: archive-validation mode has been added as
`fts validate-release-capsule release/stage2-p2-draft`. It validates the committed
capsule files directly from local relative paths and `checksums.txt`, so capsule
verification no longer depends on the original absolute run paths.

## Known Non-Blocking Gaps

- No figures or browser demo are included.
- No GitHub release, tag, DOI, or archival deposit has been created.
