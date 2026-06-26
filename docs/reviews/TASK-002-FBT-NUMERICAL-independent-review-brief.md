# TASK-002-FBT-NUMERICAL Independent Review Brief

```text
REVIEW BRIEF ID: REVIEW-BRIEF-TASK-002-FBT-NUMERICAL-001
TARGET TASK ID: TASK-002-FBT-NUMERICAL
EXPECTED REVIEW ID: REV-TASK-002-FBT-NUMERICAL-001
TARGET BRANCH: main after the Stage 2 closeout brief is merged
EXPECTED OUTPUT: docs/reviews/REV-TASK-002-FBT-NUMERICAL-001.md
```

## Reviewer Role

You are an independent verifier for a computational research repository. Start
from the repository files and this brief. Do not assume that the implementation,
the manifest, the capsule, or the claimed arithmetic is correct because the
implementer says it is correct.

This review validates the Stage 2 exact reproduction of the FBT numerical
appendix. It does not validate the general FBT theorem, evolutionary dynamics,
finite FBT atlases, ML/RL models, or claims about real perception,
consciousness, spacetime, or ontology.

## Required Read Order

1. `AGENTS.md`
2. `01_research_strategy.md`
3. `02_stage_tasks_roles.md`
4. `tasks/TASK-002_fbt_numerical_appendix.md`
5. `sources/source_map.md`
6. `sources/claim_matrix.csv`
7. `assumptions/register.md`
8. `docs/decisions/RDR-0003-stage2-batched-review-cadence.md`
9. `specs/fbt/numerical_appendix.md`
10. `docs/research_notes/stage2_fbt_numerical_appendix.md`
11. `docs/reviews/TASK-002-FBT-NUMERICAL-batched-review-bundle.md`
12. `release/stage2-p2-draft/README.md`
13. `release/stage2-p2-draft/CLAIMS.md`
14. `release/stage2-p2-draft/LIMITATIONS.md`
15. `release/stage2-p2-draft/ASSUMPTIONS.md`
16. `release/stage2-p2-draft/REVIEW_REPORT.md`
17. `release/stage2-p2-draft/reproduction_commands.md`
18. `release/stage2-p2-draft/checksums.txt`

Treat previous Stage 1 review reports as process history only. They are not an
oracle for this Stage 2 result.

## Files To Inspect

- `experiments/configs/fbt_numerical_example.json`
- `tests/fixtures/fbt/numerical_appendix_expected.json`
- `src/fts_lab/fbt/bayes.py`
- `src/fts_lab/fbt/decision.py`
- `src/fts_lab/fbt/numerical_example.py`
- `src/fts_lab/cli.py`
- `tests/exact/test_fbt_numerical_appendix.py`
- `tests/integration/test_cli_and_smoke.py`
- `tests/integration/test_release_capsules.py`
- `sources/claim_matrix.csv`
- `assumptions/register.md`
- every committed file under `release/stage2-p2-draft/`

## Required Independent Arithmetic

Without importing the production implementation, independently recompute from the
source-table inputs:

- `P(x1) = 13/28`
- `P(x2) = 15/28`
- `p(w | x1) = (1/13, 9/13, 3/13)`
- `p(w | x2) = (1/5, 1/5, 3/5)`
- `MAP(x1) = w2`
- `MAP(x2) = w3`
- `F(x1) = 5`
- `F(x2) = 33/5`
- expected-fitness winner: `x2`

Also verify the likelihood-table orientation: likelihood rows are indexed by
world state and sum over observations.

## Required Checks

Run or independently reproduce equivalent checks:

```bash
py -m uv run ruff check .
py -m uv run ruff format --check .
py -m uv run mypy src
py -m uv run pytest
py -m uv run fts doctor --release-check
py -m uv run fts fbt reproduce-numerical-example
py -m uv run fts validate-manifest experiments/manifests/<generated-manifest>.json
py -m uv run fts validate-manifest release/stage2-p2-draft/manifests/ART-TASK-002-FBT-NUMERICAL-MANIFEST-20260625T222000Z-2A277325.json
```

Verify `release/stage2-p2-draft/checksums.txt` independently by hashing every
listed file and confirming there are no unlisted committed files under
`release/stage2-p2-draft/` except `checksums.txt`.

## Audit Questions

1. Are all source-table values transcribed into
   `experiments/configs/fbt_numerical_example.json` without hidden production
   target constants?
2. Do priors sum to exactly `1`, and does each likelihood row sum to exactly `1`?
3. Are all Bayesian calculations exact rational calculations end to end?
4. Does the implementation compute the source target values from the input table
   rather than reading them from the regression fixture?
5. Does changing the input table change the computed result in tests?
6. Does the derivation report use the same implementation objects as the CLI and
   tests?
7. Are MAP ties and zero-marginal observations rejected explicitly without
   silently choosing a project assumption?
8. Does every generated or committed scientific artifact link to
   `TASK-002-FBT-NUMERICAL`, `SRC-FBT-2021`, and
   `CLM-FBT-APP-001` through `CLM-FBT-APP-004`?
9. Does the manifest record command, parameters, git state, dependency-lock
   checksum, input checksums, output checksums, and artifact checksums?
10. Do README, research note, release capsule, and claim rows avoid saying that
    this appendix example proves the general FBT theorem?
11. Do all review-status statements preserve `pending_independent_review` until
    this review is complete?
12. Is there any wording that implies biological universality, real human
    perception claims, consciousness claims, spacetime-interface claims, or
    ontology claims?

## Blocking Criteria

Mark the review `blocked` if any `fatal` or `major` finding remains unresolved.

Fatal examples:

- a source-table value is transcribed incorrectly;
- the appendix target result is hard-coded in production code;
- exact arithmetic is replaced by floating-point arithmetic for the source
  reproduction;
- a manifest validation failure;
- a checksum mismatch in committed release-capsule files;
- a public claim outside the approved `CLM-...` rows.

Major examples:

- likelihood orientation is ambiguous or implemented inconsistently;
- edge behavior silently depends on unresolved `ASM-FBT-0001` or
  `ASM-FBT-0002`;
- generated reports and tests use different computation paths;
- claim rows or release docs imply independent review has already accepted the
  Stage 2 result;
- review cannot reproduce the CLI result from a clean checkout.

Minor examples:

- wording can be clearer without changing claim boundaries;
- local environment uses `py -m uv` instead of bare `uv`;
- non-blocking documentation or organization issue.

## Expected Review Report

Create `docs/reviews/REV-TASK-002-FBT-NUMERICAL-001.md` with:

````markdown
# REV-TASK-002-FBT-NUMERICAL-001 - Independent Review of Stage 2 FBT Numerical Appendix

```text
REVIEW ID: REV-TASK-002-FBT-NUMERICAL-001
TASK ID: TASK-002-FBT-NUMERICAL
COMMIT REVIEWED: <commit>
REVIEWER ROLE: Fresh-context AI/Codex Verifier
DATE: <YYYY-MM-DD>
VERDICT: accepted | accepted_with_minor_findings | blocked
```

## Scope

## Commands Run

## Independent Arithmetic Recalculation

## Source Transcription Audit

## Code And Test Audit

## Manifest And Checksum Audit

## Claim Boundary Audit

## Fatal Findings

## Major Findings

## Minor Findings

## Verdict
````

If the verdict is `accepted` or `accepted_with_minor_findings` and there are no
unresolved fatal or major findings, `TASK-002-FBT-NUMERICAL` may be marked
independently reviewed. Only then may the Stage 2 claim rows move out of
`pending_independent_review`.
