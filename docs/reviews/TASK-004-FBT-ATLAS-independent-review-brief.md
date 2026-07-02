# TASK-004-FBT-ATLAS Independent Review Brief

```text
REVIEW BRIEF ID: REVIEW-BRIEF-TASK-004-FBT-ATLAS-001
TARGET TASK IDS: TASK-004-FBT-ATLAS-SPEC, TASK-004-FBT-ATLAS-ORACLE, TASK-004-FBT-ATLAS-GRID-V0
EXPECTED REVIEW ID: REV-TASK-004-FBT-ATLAS-001
TARGET BRANCH: main after PR #18
TARGET IMPLEMENTATION COMMIT: f1dfe63ad2a3318490ee33fb99d6c20a26d4fd29
EXPECTED OUTPUT: docs/reviews/REV-TASK-004-FBT-ATLAS-001.md
```

## Роль reviewer

Вы независимый verifier вычислительного исследовательского репозитория. Начните с
файлов репозитория, первоисточника и этого brief. Не предполагайте, что спецификации,
fixtures, production code, tests, manifests или wording claims корректны только потому,
что implementer считает их корректными.

Это review проверяет Stage 4 FBT bundle:

- source/spec gate для Theorem 4 domain и finite-atlas boundary;
- approved `RDR-0004` policies для MAP ties, zero-marginal observations, grid
  semantics и primary comparison;
- exact finite-cell oracle;
- frozen small grid `fbt_atlas_v0`;
- grid-smoke runner, CLI, tests, generated manifest discipline;
- traceability и claim boundaries.

Это review не валидирует:

- proof или implementation of Theorem 4;
- full finite FBT atlas;
- evolutionary dynamics;
- ML/RL;
- dashboards, notebooks, figures;
- claims about real perception, consciousness, spacetime, ontology, biology, or
  metaphysics.

## Обязательный порядок чтения

1. `AGENTS.md`
2. `01_research_strategy.md`
3. `02_stage_tasks_roles.md`
4. `tasks/TASK-004_fbt_finite_atlas_spec.md`
5. `tasks/TASK-004_fbt_atlas_oracle.md`
6. `tasks/TASK-004_fbt_atlas_grid_v0.md`
7. `sources/source_map.md`
8. `sources/claim_matrix.csv`
9. `assumptions/register.md`
10. `docs/decisions/RDR-0004-stage4-fbt-blockers.md`
11. `specs/fbt/theorem4_domain.md`
12. `specs/fbt/finite_atlas_design.md`
13. `tests/fixtures/fbt/stage4_fbt_spec_cases.json`
14. `tests/fixtures/fbt/stage4_fbt_oracle_cases.json`
15. `experiments/configs/fbt_atlas_v0.json`
16. `src/fts_lab/fbt/bayes.py`
17. `src/fts_lab/fbt/decision.py`
18. `src/fts_lab/fbt/atlas_oracle.py`
19. `src/fts_lab/fbt/atlas_grid.py`
20. `src/fts_lab/cli.py`
21. `src/fts_lab/manifests.py`
22. `tests/exact/test_fbt_stage4_spec_gate.py`
23. `tests/exact/test_fbt_atlas_oracle.py`
24. `tests/exact/test_fbt_atlas_grid.py`
25. `tests/integration/test_cli_and_smoke.py`
26. `README.md`
27. `CHANGELOG.md`

Treat Stage 1, Stage 2, and Stage 3 reviews as process history only. They are not
oracles for this Stage 4 result.

## Primary source to audit

Use the version of record or author manuscript for `SRC-FBT-2021`:

```text
Prakash, C., Stephens, K. D., Hoffman, D. D., Singh, M., & Fields, C. (2021).
Fitness Beats Truth in the Evolution of Perception. Acta Biotheoretica, 69, 319-341.
https://doi.org/10.1007/s10441-020-09400-0
```

Audit the source-derived objects used by Stage 4:

- finite world/perceptual states;
- priors and perceptual kernels;
- Bayesian marginalization and posterior normalization;
- MAP estimates used by the source Truth strategy;
- expected fitness used by the Fitness-only strategy;
- Theorem 4 statement and lower-bound arithmetic as a source-transcription object.

Do not use AI summaries, blogs, podcasts, videos, repository prose, or third-party code
as the source oracle when the primary paper is available.

## Files to inspect

Task and decision files:

- `tasks/TASK-004_fbt_finite_atlas_spec.md`
- `tasks/TASK-004_fbt_atlas_oracle.md`
- `tasks/TASK-004_fbt_atlas_grid_v0.md`
- `docs/decisions/RDR-0004-stage4-fbt-blockers.md`

Specs and configs:

- `specs/fbt/theorem4_domain.md`
- `specs/fbt/finite_atlas_design.md`
- `experiments/configs/fbt_atlas_v0.json`

Fixtures and tests:

- `tests/fixtures/fbt/stage4_fbt_spec_cases.json`
- `tests/fixtures/fbt/stage4_fbt_oracle_cases.json`
- `tests/exact/test_fbt_stage4_spec_gate.py`
- `tests/exact/test_fbt_atlas_oracle.py`
- `tests/exact/test_fbt_atlas_grid.py`
- `tests/integration/test_cli_and_smoke.py`

Implementation and manifest infrastructure:

- `src/fts_lab/fbt/bayes.py`
- `src/fts_lab/fbt/decision.py`
- `src/fts_lab/fbt/atlas_oracle.py`
- `src/fts_lab/fbt/atlas_grid.py`
- `src/fts_lab/fbt/__init__.py`
- `src/fts_lab/cli.py`
- `src/fts_lab/manifests.py`
- `experiments/schemas/experiment_manifest.schema.json`

Traceability and public wording:

- `sources/source_map.md`
- `sources/claim_matrix.csv`
- `assumptions/register.md`
- `README.md`
- `CHANGELOG.md`
- `src/fts_lab/doctor.py`

Generated local files under `results/` and `experiments/manifests/` are not committed
release artifacts for this task. Reviewer should generate fresh artifacts with the CLI.

## Required independent derivations

Do these derivations without importing `src/fts_lab/fbt/atlas_oracle.py` or
`src/fts_lab/fbt/atlas_grid.py`. Small scratch scripts are allowed, but they must be
independent of the production implementation. Running the production tests is a separate
step after the independent derivation.

### 1. Theorem 4 domain/spec arithmetic

Verify that Stage 4 only transcribes source-domain and boundary information for
`CLM-FBT-THM-001`; it does not implement or prove Theorem 4.

Independently recompute fixture arithmetic:

```text
strict_domination_lower_bound = (abs_x - 3) / (abs_x - 1)
same_best_territory_probability = 2 / (abs_x - 1)

abs_x = 3:
same_best = 1
lower_bound = 0

abs_x = 4:
same_best = 2/3
lower_bound = 1/3

abs_x = 5:
same_best = 1/2
lower_bound = 1/2

abs_x = 10:
same_best = 2/9
lower_bound = 7/9
```

Confirm that:

- no `src/fts_lab/fbt/theorem4.py` production theorem module exists;
- no full finite-atlas theorem probability is claimed;
- `CLM-FBT-THM-001` remains source-spec/transcription work, not theorem
  implementation.

### 2. Approved edge-case policies from RDR-0004

Audit that `RDR-0004` decisions are faithfully implemented:

- `ASM-FBT-0001`: MAP ties are full MAP sets; no lexical/random tie-break in primary
  results.
- `ASM-FBT-0002`: `P(x) = 0` is undefined; no epsilon smoothing; dependent cell
  comparison becomes `blocked_zero_marginal`.
- `ASM-FBT-0003`: frozen grid versions report `grid_frequency`, not source theorem
  probability.
- `ASM-FBT-0004`: primary comparison is `truth_map` versus
  `fitness_only_expected`; extension baselines are separate and not merged into the
  source Truth strategy.

### 3. Oracle fixture cases

Independently recompute the expected statuses and exact values for
`tests/fixtures/fbt/stage4_fbt_oracle_cases.json`.

Required checks:

```text
same_best_observation_unique_map:
truth_map best = x2
fitness_only_expected best = x2
status = same_best_observation

map_tie_same_truth_fitness:
posterior tie = {w1, w2}
fitness(w1) = fitness(w2) = 3
map_tie_kind = same_truth_fitness
status = same_best_observation

map_tie_policy_sensitive:
x1 has MAP tie with distinct Truth fitness values
possible truth best observation sets = [[x1], [x2]]
status = map_tie_policy_sensitive

blocked_zero_marginal:
P(x2) = 0
posterior(x2) undefined
cell status = blocked_zero_marginal
```

For the strict-dominance fixture, independently recompute:

```text
x1 joint weights:
w_high: (89/200) * (40/89) = 1/5
w_mid:  (2/5)    * (3/8)   = 3/20
w_low:  (31/200) * (30/31) = 3/20
P(x1) = 1/2
posterior(x1) = (2/5, 3/10, 3/10)
truth_map(x1) = w_high
expected_fitness(x1) = 11/2

x2 joint weights:
w_high: (89/200) * (49/89) = 49/200
w_mid:  (2/5)    * (5/8)   = 1/4
w_low:  (31/200) * (1/31)  = 1/200
P(x2) = 1/2
posterior(x2) = (49/100, 1/2, 1/100)
truth_map(x2) = w_mid
expected_fitness(x2) = 37/5

truth_map best = x1
fitness_only_expected best = x2
status = fitness_only_strictly_dominates_truth
```

### 4. Frozen grid v0 enumeration

Independently inspect `experiments/configs/fbt_atlas_v0.json` and verify:

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
total cells = 2 * 4 * 3 * 1 = 24
```

Independently verify deterministic cell IDs:

```text
first expected cell id:
fbt_atlas_v0__prior-uniform__kernel-identity__fitness-w1_high__offered-x1-x2

last expected cell id:
fbt_atlas_v0__prior-w1_heavy__kernel-zero_x2__fitness-equal__offered-x1-x2
```

Independently recompute status counts for this frozen grid:

```text
blocked_zero_marginal: 6
map_tie_policy_sensitive: 4
same_best_observation: 6
truth_decision_tie: 8
total: 24
```

Expected `grid_frequency` values:

```text
blocked_zero_marginal: 1/4
map_tie_policy_sensitive: 1/6
same_best_observation: 1/4
truth_decision_tie: 1/3
```

Confirm that all aggregate wording says `grid_frequency`, never source theorem
probability.

### 5. Manifest discipline

Run the CLI and validate a fresh manifest:

```bash
py -m uv run fts fbt atlas-grid-v0-smoke
py -m uv run fts validate-manifest experiments/manifests/<generated-manifest>.json
```

If bare `uv` is available, equivalent `uv run ...` commands are acceptable.

Verify the generated manifest contains:

- `artifact_kind: fbt_atlas_grid_v0_smoke`;
- `epistemic_status: E`;
- `task_ids: [TASK-004-FBT-ATLAS-GRID-V0]`;
- `claim_ids: [CLM-FBT-ATLAS-001]`;
- `source_ids: [SRC-FBT-2021]`;
- `assumption_ids: [ASM-FBT-0001, ASM-FBT-0002, ASM-FBT-0003, ASM-FBT-0004]`;
- `parameters.grid_version: fbt_atlas_v0`;
- `parameters.aggregate_label: grid_frequency`;
- `parameters.denominator_policy: all_enumerated_cells`;
- `parameters.cell_count: 24`;
- `seed: null`;
- git commit, branch, dirty state;
- dependency-lock checksum;
- config input path and checksum;
- JSON and Markdown output paths and checksums.

Independently hash the generated JSON and Markdown outputs and confirm the manifest
checksums match.

## Required commands

Run or independently reproduce equivalent checks:

```bash
py -m uv run ruff check .
py -m uv run ruff format --check .
py -m uv run mypy src
py -m uv run pytest
py -m uv run fts doctor --release-check
py -m uv run fts fbt atlas-grid-v0-smoke
py -m uv run fts validate-manifest experiments/manifests/<generated-manifest>.json
```

Also run focused Stage 4 checks:

```bash
py -m uv run pytest tests/exact/test_fbt_stage4_spec_gate.py
py -m uv run pytest tests/exact/test_fbt_atlas_oracle.py
py -m uv run pytest tests/exact/test_fbt_atlas_grid.py
py -m uv run pytest tests/integration/test_cli_and_smoke.py
```

Tests must not require internet access.

## Audit questions

1. Do the Stage 4 specs match the primary source objects, or do they import
   definitions from memory or secondary explanations?
2. Is Theorem 4 kept as source transcription/domain-boundary work rather than a
   production theorem implementation?
3. Does the code ever silently choose a MAP tie by lexical order, insertion order, or
   randomness?
4. Does the code ever smooth zero-marginal observations with epsilon or fabricate a
   posterior?
5. Are blocked and tie-sensitive cells preserved in denominator accounting?
6. Is `truth_map` kept separate from extension truth-like baselines?
7. Does `atlas_grid.py` use the approved finite-cell oracle instead of reimplementing
   divergent comparison logic?
8. Does `fbt_atlas_v0.json` validate as a frozen project grid with exact rational
   priors, kernels, and nonnegative fitness values?
9. Are all grid rows exact rational calculations end to end?
10. Are grid cell IDs deterministic and derived from grid version, prior, kernel,
    fitness, and offered observations?
11. Does the generated JSON result include enough exact input/output detail to audit
    every cell?
12. Does the generated Markdown report preserve the claim boundary?
13. Does the manifest include command, parameters, git state, lock checksum, inputs,
    outputs, and checksums?
14. Do tests verify both ordinary cells and edge cases: MAP tie, zero marginal, strict
    dominance, deterministic grid enumeration, and theorem-probability wording?
15. Are `sources/source_map.md`, `sources/claim_matrix.csv`, `assumptions/register.md`,
    README, and CHANGELOG mutually consistent?
16. Does any wording imply that Stage 4 has a full atlas result, Theorem 4 proof, or
    source theorem probability?
17. Does any wording overclaim into real perception, consciousness, spacetime,
    ontology, biology, ML/RL, or evolutionary dynamics?

## Blocking criteria

Mark the review `blocked` if any unresolved `fatal` or `major` finding remains.

Fatal examples:

- a source definition or theorem-bound expression is transcribed incorrectly;
- production code claims or implements Theorem 4 while task scope says it does not;
- MAP ties are silently resolved by hidden deterministic or random tie-breaks;
- zero-marginal observations are smoothed or normalized into fabricated posteriors;
- grid frequencies are described as source theorem probabilities;
- manifest validation fails;
- generated output checksums do not match the manifest;
- production code hard-codes fixture expected outputs rather than computing them;
- public wording claims a full atlas run, biological result, real-perception result,
  consciousness result, spacetime/ontology result, ML/RL result, or evolutionary result.

Major examples:

- source locators are too vague to audit the Stage 4 definitions;
- approved `ASM-FBT-0001..0004` decisions are inconsistently represented across specs,
  code, tests, and docs;
- oracle and grid runner use inconsistent comparison semantics;
- status accounting drops blocked or policy-sensitive cells from denominators;
- `fbt_atlas_v0` can change without changing `grid_version`;
- generated reports and tests use different computation paths;
- claim rows imply independent review has already accepted Stage 4;
- CLI command cannot reproduce the smoke result from a clean checkout.

Minor examples:

- wording can be clearer without changing claim boundaries;
- local environment uses `py -m uv` instead of bare `uv`;
- non-blocking documentation or organization issue;
- useful extra edge cases are suggested but current claims remain valid.

## Expected review report

Create `docs/reviews/REV-TASK-004-FBT-ATLAS-001.md` with:

````markdown
# REV-TASK-004-FBT-ATLAS-001 - Independent Review of Stage 4 FBT Atlas Bundle

```text
REVIEW ID: REV-TASK-004-FBT-ATLAS-001
TASK IDS: TASK-004-FBT-ATLAS-SPEC, TASK-004-FBT-ATLAS-ORACLE, TASK-004-FBT-ATLAS-GRID-V0
COMMIT REVIEWED: <commit>
REVIEWER ROLE: Fresh-context AI/Codex Verifier
DATE: <YYYY-MM-DD>
VERDICT: accepted | accepted_with_minor_findings | blocked
```

## Scope

## Commands Run

## Primary Source And Spec Audit

## RDR-0004 Policy Audit

## Independent Oracle Derivations

## Independent Grid v0 Derivation

## Manifest And Checksum Audit

## Code And Test Audit

## Traceability And Claim Boundary Audit

## Fatal Findings

## Major Findings

## Minor Findings

## Verdict
````

If the verdict is `accepted` or `accepted_with_minor_findings` and there are no
unresolved fatal or major findings, the project may record:

```text
REV-TASK-004-FBT-ATLAS-001_no_fatal_or_major
```

for the reviewed Stage 4 spec/oracle/grid-smoke bundle.

This review may support a status update for `CLM-FBT-ATLAS-001` from
`grid_v0_smoke_implemented_pending_review` to a reviewed Stage 4 bundle status. It must
not mark `CLM-FBT-THM-001` as theorem implemented or reviewed as a theorem
implementation. Theorem 4 remains unimplemented unless a separate theorem task is
created, implemented, and reviewed.
