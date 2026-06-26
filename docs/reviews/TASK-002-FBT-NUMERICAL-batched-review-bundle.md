# TASK-002-FBT-NUMERICAL Batched Review Bundle

```text
TASK ID: TASK-002-FBT-NUMERICAL
REVIEW TYPE: deferred independent Stage 2 batch review input
CURRENT VERDICT: none; not yet independently reviewed
SOURCE ID: SRC-FBT-2021
CLAIM IDS: CLM-FBT-APP-001, CLM-FBT-APP-002, CLM-FBT-APP-003, CLM-FBT-APP-004
ASSUMPTION IDS: none for the source example
```

## Purpose

This file is a review bundle for the later batched Stage 2 independent review.
It is not a review result and does not change any claim to accepted/reviewed
status.

Per `RDR-0003`, intermediate Stage 2 work may merge before independent review
when local checks and CI pass. The end-of-Stage 2 independent review must still
verify this block before any reviewed-release claim is made.

## Review Scope

The reviewer should verify that the repository exactly reproduces the numerical
appendix example from `SRC-FBT-2021`, without expanding the claim to the general
FBT theorem or evolutionary dynamics.

Primary files:

- `tasks/TASK-002_fbt_numerical_appendix.md`;
- `specs/fbt/numerical_appendix.md`;
- `experiments/configs/fbt_numerical_example.json`;
- `tests/fixtures/fbt/numerical_appendix_expected.json`;
- `src/fts_lab/fbt/bayes.py`;
- `src/fts_lab/fbt/decision.py`;
- `src/fts_lab/fbt/numerical_example.py`;
- `src/fts_lab/cli.py`;
- `tests/unit/fbt/test_bayes.py`;
- `tests/unit/fbt/test_decision.py`;
- `tests/unit/fbt/test_numerical_example.py`;
- `tests/integration/test_cli_and_smoke.py`;
- `release/stage2-p2-draft/`;
- `docs/research_notes/stage2_fbt_numerical_appendix.md`;
- `sources/claim_matrix.csv`;
- `assumptions/register.md`.

## Expected Source Values

The reviewer should independently recompute:

- `P(x1) = 13/28`;
- `P(x2) = 15/28`;
- `p(w | x1) = (1/13, 9/13, 3/13)`;
- `p(w | x2) = (1/5, 1/5, 3/5)`;
- `MAP(x1) = w2`;
- `MAP(x2) = w3`;
- `F(x1) = 5`;
- `F(x2) = 33/5`;
- expected-fitness winner: `x2`.

## Commands To Run

Quality checks:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
uv run fts doctor --release-check
```

Stage 2 reproduction:

```bash
uv run fts fbt reproduce-numerical-example
uv run fts validate-manifest experiments/manifests/<manifest>.json
```

Windows fallback if bare `uv` is unavailable:

```bash
py -m uv run ruff check .
py -m uv run ruff format --check .
py -m uv run mypy src
py -m uv run pytest
py -m uv run fts doctor --release-check
py -m uv run fts fbt reproduce-numerical-example
py -m uv run fts validate-manifest experiments/manifests/<manifest>.json
```

## Acceptance Criteria To Check

- Source-table values are transcribed from `SRC-FBT-2021` into a config, not
  hidden as detached production constants.
- The same implementation objects drive CLI output, report generation, and
  tests.
- Regression fixtures encode expected source results, while production code
  recomputes them from inputs.
- Exact arithmetic is preserved as rational values.
- Changing the source config changes the computed result in tests.
- Manifest metadata records task IDs, claim IDs, source IDs, git state, command,
  dependency-lock checksum, input checksums, output checksums, and artifact
  checksums.
- The release capsule checksum test validates the committed Stage 2 checkpoint
  package.

## Edge Cases And Open Decisions

`ASM-FBT-0001` remains open for general MAP tie handling. The source example has
unique MAP estimates, so no tie rule is introduced here. The current reusable
helper raises an explicit ambiguity error instead of choosing a silent tie rule.

`ASM-FBT-0002` remains open for zero-probability observations. The source example
has nonzero marginals, so no zero-marginal convention is introduced here. The
current reusable helper raises an explicit zero-marginal error.

The reviewer should confirm that these edge behaviors are not presented as
settled source claims for later general FBT work.

## Overclaim Checks

The reviewer should reject or flag any wording that claims:

- this appendix reproduction proves the general FBT theorem;
- the implementation simulates evolution;
- this example establishes biological universality;
- this example proves metaphysical, consciousness, spacetime-interface, or
  ontology claims;
- MAP inference and expected-fitness maximization are the same criterion.

## Review Output Expected Later

The later independent review should produce a `REV-...` file that records:

- verdict: `accepted`, `accepted_with_minor_findings`, `blocked_major`, or
  `blocked_fatal`;
- source transcription findings;
- independent arithmetic recomputation;
- code/test/manifest findings;
- overclaim findings;
- any required fixes before Stage 2 can be called independently reviewed.
