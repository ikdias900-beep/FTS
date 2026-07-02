# REV-TASK-004-FBT-ATLAS-001 - Independent Review of Stage 4 FBT Atlas Bundle

```text
REVIEW ID: REV-TASK-004-FBT-ATLAS-001
TASK IDS: TASK-004-FBT-ATLAS-SPEC, TASK-004-FBT-ATLAS-ORACLE, TASK-004-FBT-ATLAS-GRID-V0
COMMIT REVIEWED: f1dfe63ad2a3318490ee33fb99d6c20a26d4fd29
REVIEWER ROLE: Fresh-context AI/Codex Verifier
DATE: 2026-07-02
VERDICT: accepted
```

## Scope

Reviewed the Stage 4 FBT spec/oracle/grid-smoke bundle requested by
`REVIEW-BRIEF-TASK-004-FBT-ATLAS-001`.

The target implementation commit is `f1dfe63ad2a3318490ee33fb99d6c20a26d4fd29`
(`main`). Review execution happened on `ce8b86d66379a53e28e0db395912478faf906138`
(`codex/stage4-review-brief`), whose implementation parent is the target commit and
whose extra tracked changes are the review brief plus one-line links in README,
CHANGELOG, and `sources/source_map.md`.

This review checked:

- Theorem 4 domain/source-boundary specification for `CLM-FBT-THM-001`.
- `RDR-0004` policies for MAP ties, zero marginals, grid semantics, and primary strategy
  comparison.
- Exact finite-cell oracle behavior.
- Frozen `fbt_atlas_v0` grid enumeration and status accounting.
- CLI, manifest discipline, generated JSON/Markdown outputs, and claim boundaries.

This review did not validate a proof or production implementation of Theorem 4, a full
finite atlas, evolutionary dynamics, ML/RL, dashboards, notebooks, figures, biological
claims, or metaphysical claims.

## Commands Run

```text
py -m uv run ruff check .
```

Outcome: passed, "All checks passed!".

```text
py -m uv run ruff format --check .
```

Outcome: passed, 42 files already formatted.

```text
py -m uv run mypy src
```

Outcome: passed, no issues in 23 source files.

```text
py -m uv run pytest
```

Outcome: passed, 269 tests.

```text
py -m uv run pytest tests/exact/test_fbt_stage4_spec_gate.py
py -m uv run pytest tests/exact/test_fbt_atlas_oracle.py
py -m uv run pytest tests/exact/test_fbt_atlas_grid.py
py -m uv run pytest tests/integration/test_cli_and_smoke.py
```

Outcomes: passed, respectively 5, 7, 4, and 19 tests.

```text
py -m uv run fts doctor --release-check
```

Outcome: passed. Python 3.12.13, uv 0.11.24, required context files present, lockfile
checksum `6b81fceadcb3fe17172ce56a239b581332675e7045058459a5871f2982e609c8`,
manifest schema present, artifact directories writable, license decision resolved.

```text
py -m uv run fts fbt atlas-grid-v0-smoke
```

Outcome: passed. Fresh run:

- run ID: `EXP-TASK-004-FBT-ATLAS-GRID-V0-20260702T061419Z-EF8B4EDD`
- manifest: `experiments/manifests/ART-TASK-004-FBT-ATLAS-GRID-V0-MANIFEST-20260702T061419Z-EF8B4EDD.json`
- JSON checksum: `caba8ad12bb67f1137a7be8d6551c3234ad47768018b9634553b881bce6210b8`
- Markdown checksum: `ffbff5de5cca94bb67fb5ff702543f5006faa2cc7d2079282e6d973accfdcd6b`
- cell count: 24

```text
py -m uv run fts validate-manifest experiments/manifests/ART-TASK-004-FBT-ATLAS-GRID-V0-MANIFEST-20260702T061419Z-EF8B4EDD.json
```

Outcome: passed, manifest valid.

I also ran an independent inline Python scratch checker that imported only the standard
library (`json`, `fractions`, `itertools`, `collections`, `pathlib`) and did not import
`src/fts_lab/fbt/atlas_oracle.py` or `src/fts_lab/fbt/atlas_grid.py`.

## Primary Source And Spec Audit

Primary source consulted:

- Prakash, Stephens, Hoffman, Singh, and Fields, `Fitness Beats Truth in the Evolution
  of Perception`, Acta Biotheoretica 69, 319-341, DOI
  `https://doi.org/10.1007/s10441-020-09400-0`.
- Open author manuscript:
  `https://sites.socsci.uci.edu/~ddhoff/FitnessBeatsTruth_apa_PBR.pdf`.

The Stage 4 specs match the source-level objects needed for this scope:

- `W` is documented as the source world space, with finite restrictions marked as
  project-defined.
- `X` is finite in the source theorem domain.
- Pure perceptual maps and Markov kernels are distinguished.
- Bayesian marginalization and posterior normalization match the source appendix and
  source Bayesian-inference section.
- MAP estimates are correctly treated as potentially non-unique.
- Expected fitness is posterior-weighted fitness.
- The source Truth strategy is a MAP point-estimate strategy.
- Fitness-only ranks by expected fitness.
- Theorem 4 is recorded as a source-boundary/lower-bound transcription, not as a
  production theorem implementation.

Independent theorem-bound fixture arithmetic matched:

```text
abs_x=3:  same_best=1,   lower_bound=0
abs_x=4:  same_best=2/3, lower_bound=1/3
abs_x=5:  same_best=1/2, lower_bound=1/2
abs_x=10: same_best=2/9, lower_bound=7/9
```

I confirmed that `src/fts_lab/fbt/theorem4.py` and `src/fts_lab/fbt/finite_atlas.py` do
not exist. No production theorem module is present.

## RDR-0004 Policy Audit

`RDR-0004` is represented consistently across the assumption register, Stage 4 specs,
task briefs, fixtures, implementation, tests, generated result, and generated report.

`ASM-FBT-0001`: MAP ties are returned as full MAP sets. Primary code does not apply
lexical, insertion-order, or random tie-breaks to choose a hidden MAP winner. Cells whose
comparison can depend on tied MAP maximizer fitness are classified as
`map_tie_policy_sensitive`.

`ASM-FBT-0002`: zero-marginal observations return `zero_marginal_undefined`; dependent
cell comparisons become `blocked_zero_marginal`. No epsilon smoothing was found.

`ASM-FBT-0003`: `fbt_atlas_v0` reports `grid_frequency`, uses
`denominator_policy: all_enumerated_cells`, and keeps blocked/tie-sensitive cells in the
denominator.

`ASM-FBT-0004`: the primary comparison is `truth_map` versus
`fitness_only_expected`. Extension baselines are discussed only as future separate
baselines and are not merged into the source Truth strategy.

## Independent Oracle Derivations

The independent scratch checker recomputed all oracle fixture cases without importing
the production oracle/grid modules.

Results:

```text
same_best_observation_unique_map: same_best_observation
map_tie_same_truth_fitness: same_best_observation
map_tie_policy_sensitive: map_tie_policy_sensitive
blocked_zero_marginal: blocked_zero_marginal
fitness_only_strictly_dominates_truth: fitness_only_strictly_dominates_truth
```

Strict-dominance fixture recomputation:

```text
x1 marginal = 1/2
x1 posterior = (2/5, 3/10, 3/10)
x1 expected_fitness = 11/2
x1 truth_map best = w_high

x2 marginal = 1/2
x2 posterior = (49/100, 1/2, 1/100)
x2 expected_fitness = 37/5
x2 truth_map best = w_mid

truth_map best observation = x1
fitness_only_expected best observation = x2
status = fitness_only_strictly_dominates_truth
```

The production oracle computes these values from exact rational inputs; I did not find
hard-coded expected fixture outputs in production code.

## Independent Grid v0 Derivation

`experiments/configs/fbt_atlas_v0.json` matches the frozen grid declaration:

```text
grid_version = fbt_atlas_v0
epistemic_status = E
task_ids = [TASK-004-FBT-ATLAS-GRID-V0]
claim_ids = [CLM-FBT-ATLAS-001]
source_ids = [SRC-FBT-2021]
assumption_ids = [ASM-FBT-0001, ASM-FBT-0002, ASM-FBT-0003, ASM-FBT-0004]
observations = 2
world_states = 2
priors = 2
kernels = 4
fitness_functions = 3
offered_observation_sets = 1
total cells = 24
```

Independent enumeration reproduced deterministic cell IDs:

```text
first = fbt_atlas_v0__prior-uniform__kernel-identity__fitness-w1_high__offered-x1-x2
last  = fbt_atlas_v0__prior-w1_heavy__kernel-zero_x2__fitness-equal__offered-x1-x2
```

Independent status counts:

```text
blocked_zero_marginal = 6
map_tie_policy_sensitive = 4
same_best_observation = 6
truth_decision_tie = 8
total = 24
```

Independent grid frequencies:

```text
blocked_zero_marginal = 1/4
map_tie_policy_sensitive = 1/6
same_best_observation = 1/4
truth_decision_tie = 1/3
```

These matched the generated JSON result and production tests.

## Manifest And Checksum Audit

Fresh manifest:

```text
experiments/manifests/ART-TASK-004-FBT-ATLAS-GRID-V0-MANIFEST-20260702T061419Z-EF8B4EDD.json
```

Manifest fields audited:

```text
artifact_kind = fbt_atlas_grid_v0_smoke
epistemic_status = E
task_ids = [TASK-004-FBT-ATLAS-GRID-V0]
claim_ids = [CLM-FBT-ATLAS-001]
source_ids = [SRC-FBT-2021]
assumption_ids = [ASM-FBT-0001, ASM-FBT-0002, ASM-FBT-0003, ASM-FBT-0004]
parameters.grid_version = fbt_atlas_v0
parameters.aggregate_label = grid_frequency
parameters.denominator_policy = all_enumerated_cells
parameters.cell_count = 24
seed = null
```

The manifest includes command, git state, branch, dirty state, dependency-lock checksum,
config input path/checksum, JSON output path/checksum, and Markdown output
path/checksum.

Execution git state in the fresh manifest:

```text
commit = ce8b86d66379a53e28e0db395912478faf906138
branch = codex/stage4-review-brief
dirty = false
```

This differs from `COMMIT REVIEWED` only because the review was run on the review-brief
branch. The target implementation commit is the parent `f1dfe63...`; the extra tracked
changes do not modify Stage 4 implementation behavior.

Manual SHA-256 verification matched manifest values:

```text
fbt_atlas_v0.json      4b933097880d1e1756d62b0af04cff39131ca5e5cc85267df829d50ad17e8556
fbt_atlas_v0_smoke.json caba8ad12bb67f1137a7be8d6551c3234ad47768018b9634553b881bce6210b8
fbt_atlas_v0_smoke.md   ffbff5de5cca94bb67fb5ff702543f5006faa2cc7d2079282e6d973accfdcd6b
```

## Code And Test Audit

`bayes.py` provides exact finite Bayesian primitives with `Fraction`, strict prior and
kernel validation, zero-marginal errors for the generic posterior path, and a unique-MAP
helper that explicitly refuses ambiguous MAP ties.

`decision.py` computes expected fitness from posterior distributions and refuses
ambiguous unique-best decisions where the older unique helper is used.

`atlas_oracle.py` implements the approved Stage 4 primary finite-cell behavior:

- observation marginals and posteriors are exact rationals;
- zero marginal observations remain undefined;
- full MAP sets are recorded;
- same-fitness MAP ties remain determined;
- distinct-fitness MAP ties are policy-sensitive when they can change the comparison;
- blocked and tie-sensitive statuses are preserved.

`atlas_grid.py` validates the frozen config, enumerates deterministic cells, calls
`evaluate_primary_cell` instead of reimplementing divergent comparison semantics, writes
immutable JSON/Markdown outputs, and validates the manifest.

Test coverage includes source/spec fixture arithmetic, absence of forbidden theorem
modules, MAP tie cases, zero-marginal behavior, strict dominance, Stage 2 source-table
compatibility as a Stage 4 primary cell, grid enumeration, denominator accounting,
report wording, CLI manifest generation, and manifest checksum validation.

## Traceability And Claim Boundary Audit

Traceability is internally consistent:

- `CLM-FBT-THM-001` remains `specified_pending_review` and does not claim theorem
  implementation.
- `CLM-FBT-ATLAS-001` remains `grid_v0_smoke_implemented_pending_review` and is marked
  as an extension/design claim.
- `ASM-FBT-0001..0004` are approved in the assumption register and linked from Stage 4
  specs/config/manifest.
- `README.md` and `CHANGELOG.md` describe the Stage 4 bundle as a finite-cell oracle and
  frozen small-grid smoke-run, not a full atlas or theorem result.

Generated JSON and Markdown preserve the claim boundary:

- aggregate label is `grid_frequency`;
- `theorem_probability_claim` is false;
- the report says the smoke grid is not a full atlas run and not a source theorem
  probability calculation;
- no wording claims biological, real-perception, consciousness, spacetime, ontology,
  evolutionary-dynamics, ML/RL, or dashboard results.

## Fatal Findings

None.

## Major Findings

None.

## Minor Findings

None.

## Verdict

Accepted. I found no unresolved fatal, major, or minor findings in the reviewed Stage 4
FBT spec/oracle/grid-smoke bundle.

The project may record:

```text
REV-TASK-004-FBT-ATLAS-001_no_fatal_or_major
```

for the reviewed Stage 4 spec/oracle/grid-smoke bundle.

This review supports updating `CLM-FBT-ATLAS-001` from
`grid_v0_smoke_implemented_pending_review` to an appropriate reviewed Stage 4 bundle
status. It does not mark `CLM-FBT-THM-001` as theorem implemented or reviewed as a
theorem implementation.
