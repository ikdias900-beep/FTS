# RDR-0003: Stage 2 Batched Review Cadence

## Status

APPROVED

## Intent

Record the Human Principal Investigator decision that intermediate Stage 2 pull
requests may merge before independent review, while preserving independent review
as a required end-of-Stage 2 gate before any reviewed-release claim.

## Scope

This decision applies to:

- Stage 2 work on `SRC-FBT-2021`;
- `TASK-002-FBT-NUMERICAL`;
- intermediate Stage 2 implementation pull requests;
- Stage 2 review briefs, release notes, and claim-status language.

This decision does not apply to Stage 1 retroactively, later Stage 3+ work, or
public release claims that say a result has passed independent review.

## Options

1. Require independent review before every intermediate Stage 2 merge.
2. Merge intermediate Stage 2 pull requests after local and CI checks, then run
   one batched independent review at the end of Stage 2.
3. Skip independent review for Stage 2 entirely.

## AI Explanation In Plain Language

Per-PR independent review catches issues earlier, but it is expensive when the
work is small and tightly scoped. Batched review keeps the independent reviewer
fresh and reduces repeated review overhead, while still requiring a separate
verification pass before Stage 2 can be described as independently reviewed.

The tradeoff is timing. With batched review, an intermediate merge can contain an
unreviewed defect for longer. To control that risk, claim records and release
notes must keep the status `pending_independent_review`, and intermediate PRs
must still pass local quality checks, tests, manifest validation, and CI.

## Risks

Requiring review before every merge improves early defect detection, but slows
small implementation increments and creates repeated review setup cost.

Batched end-of-stage review improves throughput and review coherence, but can
delay discovery of a defect until several Stage 2 changes have accumulated.

Skipping review entirely would violate the repository's scientific-integrity
model and would make reviewed publication claims inadmissible.

## Human Decision

Use batched independent review for Stage 2.

Intermediate Stage 2 PRs may merge without independent review when:

- the Human Principal Investigator explicitly allows the merge;
- no known fatal or major finding is unresolved;
- local quality checks and relevant reproduction commands pass;
- GitHub CI passes, or a failed check is investigated and explicitly waived by
  the Human Principal Investigator;
- claim rows and release notes continue to mark the work as pending independent
  review.

Run independent review at the end of Stage 2 before converting any Stage 2 result
from `pending_independent_review` to reviewed/accepted status.

Decision made by Human Principal Investigator on 2026-06-26.

## What This Does Not Mean

This does not remove the independent-review requirement for Stage 2.

This does not allow reviewed-release wording before the batched Stage 2 review
has accepted the relevant claims.

This does not allow unresolved fatal or major review findings to be ignored.

This does not broaden `TASK-002-FBT-NUMERICAL` beyond exact appendix arithmetic.

## When To Revisit

Revisit this decision if Stage 2 expands beyond appendix reproduction, if a
regression reaches `main`, if CI coverage becomes insufficient for a Stage 2
claim, or before starting Stage 3.
