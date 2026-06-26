# Review Report

## Review Summary

This capsule has not yet received an independent review.

The current project cadence is to review Stage 2 in a larger batch rather than opening a
separate independent review for every small PR or checkpoint.

| Review ID | Scope | Verdict | Unresolved fatal | Unresolved major |
|---|---|---|---:|---:|
| pending | Stage 2 FBT numerical checkpoint batch | not reviewed yet | n/a | n/a |

## Automated Checks Already Run

- `py -m uv run ruff check .`
- `py -m uv run ruff format --check .`
- `py -m uv run mypy src`
- `py -m uv run pytest`
- `py -m uv run fts doctor --release-check`
- `py -m uv run fts fbt reproduce-numerical-example`
- `py -m uv run fts validate-manifest experiments/manifests/ART-TASK-002-FBT-NUMERICAL-MANIFEST-20260625T222000Z-2A277325.json`

## Future Batched Review Should Verify

- source transcription from `SRC-FBT-2021` into `specs/fbt/numerical_appendix.md`;
- orientation of the likelihood table;
- exact Bayes calculations for marginals and posteriors;
- expected-fitness calculation from the same source input objects;
- absence of hard-coded target results in production implementation;
- behavior for MAP ties and zero marginals does not silently depend on unresolved
  assumptions;
- copied manifest validates;
- copied raw and derived data checksums match `checksums.txt`;
- claims and limitations stay inside the Stage 2 numerical appendix boundary.

## Known Non-Blocking Gaps

- Independent review is pending by design.
- No figures or browser demo are included.
- No GitHub release, tag, DOI, or archival deposit has been created.
