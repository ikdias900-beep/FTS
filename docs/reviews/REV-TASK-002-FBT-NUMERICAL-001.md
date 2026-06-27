# REV-TASK-002-FBT-NUMERICAL-001 - Independent Review of Stage 2 FBT Numerical Appendix

```text
REVIEW ID: REV-TASK-002-FBT-NUMERICAL-001
TASK ID: TASK-002-FBT-NUMERICAL
COMMIT REVIEWED: a0bc6319593f78ffbad3f0eae75833ba69f7acc0
REVIEWER ROLE: Fresh-context AI/Codex Verifier
DATE: 2026-06-26
VERDICT: accepted_with_minor_findings
```

## Scope

I reviewed the Stage 2 exact reproduction of the numerical appendix from
`SRC-FBT-2021` for `TASK-002-FBT-NUMERICAL`.

In scope:

- `CLM-FBT-APP-001` through `CLM-FBT-APP-004`;
- source-table transcription into `experiments/configs/fbt_numerical_example.json`;
- exact rational marginal, posterior, MAP, and expected-fitness calculations;
- production-code hard-code audit;
- MAP tie and zero-marginal rejection behavior;
- tests, CLI path, generated manifest, draft release capsule, checksums, and claim
  boundaries.

Out of scope:

- the general FBT theorem;
- evolutionary dynamics, finite atlases, ML/RL, dashboards, or GPU code;
- claims about real perception, biological universality, consciousness, spacetime,
  ontology, or metaphysics.

I read the required review brief order:

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

I also inspected all committed files under `release/stage2-p2-draft/`.

## Commands Run

All required commands passed:

```text
py -m uv run ruff check .
PASS - All checks passed.

py -m uv run ruff format --check .
PASS - 31 files already formatted.

py -m uv run mypy src
PASS - Success: no issues found in 18 source files.

py -m uv run pytest
PASS - 205 passed in 6.49s.

py -m uv run fts doctor --release-check
PASS - active task TASK-002-FBT-NUMERICAL; current git commit
a0bc6319593f78ffbad3f0eae75833ba69f7acc0; branch main; dirty=False.

py -m uv run fts fbt reproduce-numerical-example
PASS - generated run EXP-TASK-002-FBT-NUMERICAL-20260626T002906Z-C064D557.
JSON checksum b5dabb660739de45d4d943e64b5195b7e85236cfe8ce5d0f2a3c61412abeb509.
Markdown checksum af7831b01b606eee35ced1734db1b86e93b230fd0a3262ac34a392880d07d565.

py -m uv run fts validate-manifest experiments/manifests/ART-TASK-002-FBT-NUMERICAL-MANIFEST-20260626T002906Z-C064D557.json
PASS - manifest valid.

py -m uv run fts validate-manifest release/stage2-p2-draft/manifests/ART-TASK-002-FBT-NUMERICAL-MANIFEST-20260625T222000Z-2A277325.json
PASS - manifest valid.
```

Additional independent checks:

```text
Independent Fraction recalculation from experiments/configs/fbt_numerical_example.json
PASS.

Production hard-code search:
rg -n "13/28|15/28|1/13|9/13|3/13|1/5|3/5|33/5|numerical_appendix_expected|tests/fixtures" src/fts_lab/fbt src/fts_lab/cli.py
PASS - no matches.

Release checksum inventory:
listed_count=12
tracked_count_including_checksums=13
missing=[]
mismatches=[]
unlisted_tracked_except_checksums=[]
listed_untracked=[]
```

## Independent Arithmetic Recalculation

I recomputed from the machine-readable source table without importing production
implementation code.

Source rows:

```text
w1: mu=1/7, p(x1|w1)=1/4, p(x2|w1)=3/4, f=20
w2: mu=3/7, p(x1|w2)=3/4, p(x2|w2)=1/4, f=4
w3: mu=3/7, p(x1|w3)=1/4, p(x2|w3)=3/4, f=3
```

Normalization:

```text
prior_sum = 1
likelihood row sums:
w1: 1/4 + 3/4 = 1
w2: 3/4 + 1/4 = 1
w3: 1/4 + 3/4 = 1
```

This confirms the table orientation used in the implementation: likelihood rows are
indexed by world state and sum over observations.

Marginals:

```text
P(x1) = (1/7)(1/4) + (3/7)(3/4) + (3/7)(1/4)
      = 1/28 + 9/28 + 3/28
      = 13/28

P(x2) = (1/7)(3/4) + (3/7)(1/4) + (3/7)(3/4)
      = 3/28 + 3/28 + 9/28
      = 15/28
```

Posteriors:

```text
p(w | x1) = (1/28, 9/28, 3/28) / (13/28)
          = (1/13, 9/13, 3/13)
MAP(x1) = w2

p(w | x2) = (3/28, 3/28, 9/28) / (15/28)
          = (1/5, 1/5, 3/5)
MAP(x2) = w3
```

Expected fitness:

```text
F(x1) = (1/13)(20) + (9/13)(4) + (3/13)(3)
      = 20/13 + 36/13 + 9/13
      = 65/13
      = 5

F(x2) = (1/5)(20) + (1/5)(4) + (3/5)(3)
      = 4 + 4/5 + 9/5
      = 33/5
```

Expected-fitness winner:

```text
x2, because 33/5 > 5.
```

## Source Transcription Audit

`experiments/configs/fbt_numerical_example.json` matches the table encoded in
`specs/fbt/numerical_appendix.md`:

- observations: `x1`, `x2`;
- world states: `w1`, `w2`, `w3`;
- priors: `1/7`, `3/7`, `3/7`;
- likelihood rows:
  - `w1`: `x1=1/4`, `x2=3/4`;
  - `w2`: `x1=3/4`, `x2=1/4`;
  - `w3`: `x1=1/4`, `x2=3/4`;
- fitness values: `20`, `4`, `3`;
- traceability: `TASK-002-FBT-NUMERICAL`, `SRC-FBT-2021`,
  `CLM-FBT-APP-001` through `CLM-FBT-APP-004`, and empty `assumption_ids`.

I found no source-table transcription error.

## Code And Test Audit

Production computation path:

- `src/fts_lab/fbt/numerical_example.py` parses the config into
  `FiniteBayesianDecisionProblem`;
- `src/fts_lab/fbt/bayes.py` computes marginals, posteriors, and unique MAP estimates
  with `fractions.Fraction`;
- `src/fts_lab/fbt/decision.py` computes expected fitness from posteriors and fitness
  values;
- the CLI calls the same `run_fbt_numerical_example` path used for result/report/manifest
  generation.

Hard-code audit:

- the published target values are present in the fixture, specs, release docs, and tests;
- the target fractions are not present in `src/fts_lab/fbt` or `src/fts_lab/cli.py`;
- production code does not import `tests/fixtures/fbt/numerical_appendix_expected.json`.

Exact arithmetic audit:

- source rationals are parsed through `Fraction(value)`;
- prior normalization, likelihood-row normalization, marginalization, posterior
  normalization, MAP comparison, and expected fitness use `Fraction`;
- no float path is used in the FBT production modules.

Edge behavior:

- `unique_map_estimate` raises `AmbiguousMapEstimateError` on ties and names
  unresolved `ASM-FBT-0001`;
- `posterior` raises `ZeroMarginalProbabilityError` on zero marginal observations;
- tests cover both cases.

Tests:

- `tests/exact/test_fbt_numerical_appendix.py` verifies exact marginals, posteriors, MAP
  estimates, expected fitness, fixture alignment, input perturbation, MAP tie rejection,
  zero marginal rejection, and invalid rational parsing;
- `tests/integration/test_cli_and_smoke.py` verifies the FBT CLI writes outputs and a
  valid manifest;
- `tests/integration/test_release_capsules.py` verifies release-capsule checksums.

I found no production hard-coding, no silent MAP tie policy, and no silent
zero-marginal policy.

## Manifest And Checksum Audit

Fresh generated manifest:

- path:
  `experiments/manifests/ART-TASK-002-FBT-NUMERICAL-MANIFEST-20260626T002906Z-C064D557.json`;
- validated successfully;
- records command, parameters, git branch/commit/dirty state, Python/platform metadata,
  dependency-lock SHA-256, input checksum, output checksums, task IDs, claim IDs, source
  IDs, empty assumption IDs, status, and implementation version;
- records current reviewed commit
  `a0bc6319593f78ffbad3f0eae75833ba69f7acc0` with `dirty=false` at generation time.

Archived release manifest:

- path:
  `release/stage2-p2-draft/manifests/ART-TASK-002-FBT-NUMERICAL-MANIFEST-20260625T222000Z-2A277325.json`;
- validated successfully;
- records original generation commit
  `23060471e8ade4e9d1790041ea49271f0002cd18` with `dirty=false`;
- records dependency-lock SHA-256
  `6b81fceadcb3fe17172ce56a239b581332675e7045058459a5871f2982e609c8`.

Release capsule checksums:

- I independently hashed every file listed in
  `release/stage2-p2-draft/checksums.txt`;
- all 12 listed hashes matched;
- `git ls-files release/stage2-p2-draft` reports 13 tracked files including
  `checksums.txt`;
- there are no unlisted tracked files under `release/stage2-p2-draft/` except
  `checksums.txt`.

## Claim Boundary Audit

`sources/claim_matrix.csv` keeps Stage 2 claim rows in:

```text
status=implemented_pending_review
review_status=pending_independent_review
```

The review note, task brief, spec, release README, `CLAIMS.md`, `LIMITATIONS.md`,
`ASSUMPTIONS.md`, and `REVIEW_REPORT.md` preserve the pending independent-review state
until this review is complete.

Allowed claims are limited to exact reproduction of:

- stimulus marginals;
- `x1` posterior and MAP;
- `x2` posterior and MAP;
- expected-fitness values and winner.

Forbidden and boundary language explicitly rejects:

- proving the general FBT theorem from this example;
- evolutionary simulation claims;
- biological universality claims;
- real human perception claims;
- consciousness, spacetime-interface, ontology, or metaphysical claims;
- treating MAP as the only future truth-oriented rule;
- treating general MAP tie or zero-marginal behavior as resolved.

I found no public claim outside the approved `CLM-FBT-APP-001` through
`CLM-FBT-APP-004` rows.

## Fatal Findings

None.

## Major Findings

None.

## Minor Findings

1. The copied release manifest under `release/stage2-p2-draft/manifests/` preserves
   original absolute input/output paths outside the release capsule. In this workspace
   the required `fts validate-manifest release/stage2-p2-draft/manifests/...` command
   passed because those ignored original generated artifacts are present locally. The
   capsule itself is still independently verifiable through committed raw/derived files
   and `checksums.txt`, and the README documents that the copied manifest retains
   original absolute paths. A future release-local manifest or archive-validation mode
   would make this more portable.

## Verdict

`accepted_with_minor_findings`.

There are no unresolved fatal or major findings. `TASK-002-FBT-NUMERICAL` may be
marked independently reviewed, and the Stage 2 claim rows may move out of
`pending_independent_review` after the project applies the normal status-update process.
