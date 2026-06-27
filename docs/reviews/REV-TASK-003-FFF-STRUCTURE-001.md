# REV-TASK-003-FFF-STRUCTURE-001 - Independent Review of Stage 3 FFF Structure Bundle

```text
REVIEW ID: REV-TASK-003-FFF-STRUCTURE-001
TASK IDS: TASK-003-FFF-STRUCTURE-SPEC, TASK-003-FFF-STRUCTURE-IMPL
COMMIT REVIEWED: 54305921630116b475ac56bfb713e604a4d96cdb
TARGET IMPLEMENTATION COMMIT: 154241c57504cc7d4b6d593ea42f9360878a151a
REVIEWER ROLE: Fresh-context AI/Codex Verifier
DATE: 2026-06-28
VERDICT: accepted_with_minor_findings
```

## Scope

I reviewed the Stage 3 FFF structure bundle for `CLM-FFF-PERM-001` and
`CLM-FFF-MEAS-001`, covering:

- source transcription for permutation-group and measurable-space definitions;
- formal specs and small oracle fixtures;
- finite helper implementation and tests;
- traceability, assumption status, and public claim boundaries.

The target implementation commit in the brief is
`154241c57504cc7d4b6d593ea42f9360878a151a`. The reviewed checkout is
`54305921630116b475ac56bfb713e604a4d96cdb`, which adds the review brief,
`CHANGELOG.md`, and `sources/source_map.md` on top of the target implementation. The
Stage 3 implementation files are from the target implementation commit. The worktree was
clean before and after review commands.

Out of scope:

- Stage 1 total orders and cyclic groups, except as imported helpers;
- Stage 2 FBT;
- future FBT theorem work, evolutionary dynamics, ML/RL, dashboards, release capsules,
  or public figures;
- claims about real perception, consciousness, spacetime, ontology, biology, or
  metaphysics.

I read the required review brief order:

1. `AGENTS.md`
2. `01_research_strategy.md`
3. `02_stage_tasks_roles.md`
4. `tasks/TASK-003_fff_structure_spec.md`
5. `tasks/TASK-003_fff_structure_impl.md`
6. `sources/source_map.md`
7. `sources/claim_matrix.csv`
8. `assumptions/register.md`
9. `specs/fff/permutation_groups.md`
10. `specs/fff/measurable_spaces.md`
11. `tests/fixtures/fff/stage3_structure_spec_cases.json`
12. `src/fts_lab/fff/permutation_groups.py`
13. `src/fts_lab/fff/measurable_spaces.py`
14. `tests/exact/test_fff_stage3_spec_gate.py`
15. `tests/exact/test_fff_permutation_groups.py`
16. `tests/exact/test_fff_measurable_spaces.py`
17. `tests/properties/test_fff_properties.py`

I also inspected `src/fts_lab/fff/functions.py`, `src/fts_lab/fff/admissibility.py`,
`src/fts_lab/fff/formulas.py`, `src/fts_lab/fff/__init__.py`, `README.md`,
`CHANGELOG.md`, `src/fts_lab/doctor.py`, and
`tests/integration/test_cli_and_smoke.py`.

## Commands Run

Required quality checks:

```text
py -m uv run ruff check .
PASS - All checks passed.

py -m uv run ruff format --check .
PASS - 37 files already formatted.

py -m uv run mypy src
PASS - Success: no issues found in 21 source files.

py -m uv run pytest
PASS - 250 passed in 6.97s.

py -m uv run fts doctor --release-check
PASS - active task TASK-003-FFF-STRUCTURE-IMPL; current git commit
54305921630116b475ac56bfb713e604a4d96cdb; branch main; dirty=False;
Python 3.12.13; uv 0.11.24; lockfile SHA-256
6b81fceadcb3fe17172ce56a239b581332675e7045058459a5871f2982e609c8.
```

Focused Stage 3 checks:

```text
py -m uv run pytest tests/exact/test_fff_stage3_spec_gate.py
PASS - 5 passed in 0.26s.

py -m uv run pytest tests/exact/test_fff_permutation_groups.py
PASS - 16 passed in 0.26s.

py -m uv run pytest tests/exact/test_fff_measurable_spaces.py
PASS - 18 passed in 0.32s.

py -m uv run pytest tests/properties/test_fff_properties.py
PASS - 8 passed in 0.49s.
```

Additional audit commands:

```text
git log --oneline --decorate -n 8
PASS - target implementation commit 154241c is an ancestor of reviewed HEAD 5430592.

git diff --name-only 154241c57504cc7d4b6d593ea42f9360878a151a..HEAD
PASS - only CHANGELOG.md, source_map.md, and the review brief changed after the target
implementation commit.

Independent scratch derivations without importing production Stage 3 modules
PASS - outputs listed in the derivation sections below.

rg claim-boundary searches over README, CHANGELOG, source/assumption registries, specs,
tasks, tests, and Stage 3 source modules
PASS - no Stage 3 reviewed-status, metaphysical, biological, ML/RL, or exact-bound
overclaim found.
```

One attempted direct `Invoke-WebRequest` fetch of the MDPI page from PowerShell was
blocked by the publisher CDN. The browser/web fetch of the MDPI open full text and
version-notes page was available and used for the source audit.

## Primary Source Audit

Primary source used:

- `SRC-FFF-2020`: Prakash, Fields, Hoffman, Prentner, and Singh, "Fact, Fiction, and
  Fitness", Entropy 22(5), 514, version of record / open full text:
  https://www.mdpi.com/1099-4300/22/5/514

The source locators in the Stage 3 task briefs and specs are the required locators:

- Section 4, Permutation Groups Theorem;
- Appendix A.1, Definitions A1-A4;
- Appendix A.3, "Permutation Groups Theorem";
- Section 4, Measurable Structures Theorem;
- Appendix A.5, "Measurable Structure Theorem".

Permutation-group source audit:

- The source uses second-order action compatibility: a pair `(phi, f)` where `G` acts
  on source and target sets, with law `f(g.x) = phi(g).f(x)`.
- The repository spec preserves the distinction between first-order group
  homomorphisms, group actions, and the source second-order construction.
- The committed formula helper uses the source count object `2*n + n!` and the
  admissible denominator `n^n - (n - 1)^n`.
- The code enforces the source theorem's `n >= 5` scope for the formula helper.
- The `S_6` outer-automorphism caveat is not silently resolved. The spec flags it as
  review-sensitive, and the implementation only exposes source formula arithmetic and
  finite action-law validators.

Measurable-space source audit:

- Appendix A.5 represents finite algebras through partition bases and defines
  measurability by inverse images of measurable codomain events.
- The spec preserves algebra order `k`, characteristic as a multiset of base-block
  sizes, and the partition-base criterion for finite inverse-image measurability.
- The source special cases are preserved: discrete `W` and trivial `V` make every
  function measurable.
- The Appendix A.5 expression is represented as an upper bound, not an exact count in
  every case.
- The fixed-`m` asymptotic caveat is preserved; repo wording does not turn it into an
  all-growth-path claim.

I found no primary-source transcription error in the reviewed Stage 3 scope.

## Independent Permutation Derivations

I recomputed the required small cases without importing
`src/fts_lab/fff/permutation_groups.py`.

Source formula cases:

```text
n = 5:
2*n + n! = 10 + 120 = 130
n^n - (n - 1)^n = 5^5 - 4^5 = 3125 - 1024 = 2101

n = 6:
2*n + n! = 12 + 720 = 732
n^n - (n - 1)^n = 6^6 - 5^6 = 46656 - 15625 = 31031
```

Action-law examples:

```text
inner_conjugation_all_S3 = True
constant_trivial_all_S3 = True
negative_action_law = False
```

The positive inner-conjugation derivation used `f = h` and
`phi(g) = h * g * h^-1` for all elements of `S_3`. The constant-function derivation
used a constant `f` and the identity action on a two-element target. The negative case
used `f = (0, 1, 1)`, a transposition of domain labels `0` and `1`, and trivial target
action; it fails because the two sides of `f(g.x) = phi(g).f(x)` differ at `x = 0`.

These derivations match `tests/fixtures/fff/stage3_structure_spec_cases.json` and the
production tests.

## Independent Measurable-Space Derivations

I recomputed the required finite partition cases without importing
`src/fts_lab/fff/measurable_spaces.py`.

For:

```text
W base = [[0, 1], [2]]
V base = [[0], [1]]
```

measurable functions must be constant on the `W` block `[0, 1]`, while element `2` is
free. Therefore:

```text
total measurable functions = 2 * 2 = 4
admissible measurable functions = 3
```

Special cases:

```text
W discrete, |W| = 3, |V| = 2:
total measurable functions = 2^3 = 8
admissible measurable functions = 7

V trivial, |W| = 3, |V| = 2:
total measurable functions = 2^3 = 8
admissible measurable functions = 7
```

Non-measurable witness:

```text
f = [0, 1, 1]
inverse image of V block [0] = [0]
```

The preimage `[0]` splits the `W` block `[0, 1]`, so it is not a union of source base
blocks and `f` is not measurable.

Bound cases using the integer form
`m^(k - 1) + m^(k - 1) * (m - 1)^(n - k + 1)`:

```text
n=3, m=2, k=2: 2^1 + 2^1 * 1^2 = 4
n=4, m=3, k=2: 3^1 + 3^1 * 2^3 = 27
n=5, m=3, k=3: 3^2 + 3^2 * 2^3 = 81
```

These derivations match the fixture and tests.

## Specification Audit

`specs/fff/permutation_groups.md`:

- correctly distinguishes ordinary group homomorphisms from the source second-order
  `(phi, f)` construction;
- records the action-compatibility law;
- scopes the source formula to `n >= 5`;
- warns against ordinary `S_n -> S_n` homomorphism counting;
- preserves the count-object caveat and `S_6` outer-automorphism caveat as open audit
  points rather than silently resolving them.

`specs/fff/measurable_spaces.md`:

- correctly represents finite algebras by partition bases;
- defines order `k` as the number of base blocks;
- defines characteristic as a multiset of block sizes;
- states inverse-image measurability and the finite base-block sufficiency check;
- preserves discrete-`W` and trivial-`V` special cases;
- treats the Appendix A.5 expression as a bound, not a universal exact count;
- warns that fixed-`m` asymptotics cannot be converted into all-growth-path claims.

The fixture metadata links `TASK-003-FFF-STRUCTURE-SPEC`, `SRC-FFF-2020`,
`CLM-FFF-PERM-001`, `CLM-FFF-MEAS-001`, `ASM-FFF-0002`, and `ASM-FFF-0003`.

I found no fatal or major specification issue.

## Code And Test Audit

Permutation implementation:

- `validate_permutation`, composition, inverse, identity, and symmetric-group iterator
  use canonical zero-based labels.
- `is_second_order_respectful` directly checks `f(g.x) = phi(g).f(x)`.
- `is_second_order_homomorphism` checks the same law over a supplied finite group and
  supplied `phi` images.
- `source_permutation_respectful_count` returns `2*n + n!` only after
  `require_source_permutation_degree` enforces `n >= 5`.
- The implementation does not enumerate ordinary group homomorphisms as a substitute
  for the source construction.

Permutation tests:

- validate canonical permutation behavior and invalid inputs;
- test composition and inverse;
- test inner-conjugation positive cases;
- test a constant-function positive case with trivial target action;
- test a concrete negative action-law example;
- compare `n=5` and `n=6` formula arithmetic against fixtures;
- verify the pre-theorem-scope guard for `n=1..4`.

Measurable-space implementation:

- validates partitions for nonempty blocks, no duplicates, no overlap, nonnegative
  labels, and full coverage of `0..carrier_size-1`;
- canonicalizes blocks and partitions deterministically;
- constructs event algebras from partition bases;
- checks union-of-blocks membership;
- computes inverse images in the correct direction from codomain events to domain
  events;
- enumerates exact measurable functions for small finite spaces;
- separates exact enumeration from `source_measurable_upper_bound`;
- exposes `measurable_bound_applies_to_partitions` for concrete theorem-scope checks.

Measurable tests:

- verify partition validation and canonicalization;
- verify event algebra unions and inverse images;
- verify exact fixture counts;
- verify the non-measurable witness that splits `[0, 1]`;
- verify discrete `W` and trivial `V` special cases;
- verify bound arithmetic and out-of-scope input rejection;
- property-test discrete-domain and trivial-codomain "all functions measurable" cases.

I found no production hard-coding of fixture outputs and no test-only implementation
path replacing the production helpers.

## Traceability And Claim Boundary Audit

`sources/claim_matrix.csv` keeps Stage 3 claim rows in:

```text
status=implemented_pending_review
review_status=pending_stage3_implementation_review
```

`assumptions/register.md` keeps:

```text
ASM-FFF-0002 status=OPEN
ASM-FFF-0003 status=OPEN
```

The README states that Stage 3 has pending-review finite validators and does not provide
reviewed Stage 3 theorem claims. The Stage 3 task briefs explicitly forbid claims about
real perception, consciousness, spacetime, ontology, biology, ML/RL, or evolutionary
dynamics.

I found no public wording that:

- claims Stage 3 theorem reproduction is reviewed before this review;
- approves `ASM-FFF-0002` or `ASM-FFF-0003`;
- treats ordinary group-homomorphism counting as the source permutation theorem;
- treats the measurable-space bound as an exact count in every case;
- expands Stage 3 into real-perception, biological, metaphysical, ML/RL, or evolutionary
  claims.

Because there are no unresolved fatal or major findings, the project may record review
status `REV-TASK-003-FFF-STRUCTURE-001_no_fatal_or_major` for `CLM-FFF-PERM-001` and
`CLM-FFF-MEAS-001` through the normal status-update process.

This review does not approve `ASM-FFF-0002` or `ASM-FFF-0003`. Human PI acceptance is
still required before either assumption can be marked `APPROVED` or `SOURCE_RESOLVED`,
or before any public Stage 3 release claim is upgraded.

## Fatal Findings

None.

## Major Findings

None.

## Minor Findings

1. `src/fts_lab/fff/__init__.py` has a stale module docstring: it still says "Exact
   finite companions for Stage 1 FFF structures" while exporting Stage 3 permutation and
   measurable-space helpers. This does not affect behavior or claim boundaries, but it
   should be updated in a follow-up cleanup.

2. `source_measurable_upper_bound(domain_size, codomain_size, domain_order)` can enforce
   only the numeric part of the Appendix A.5 scope. It cannot know whether a concrete
   codomain partition is trivial. The code already provides
   `measurable_bound_applies_to_partitions` for concrete partition pairs, so this is not
   a correctness issue in the reviewed tests, but the integer helper's docstring could
   be clearer that it is not a complete concrete-space scope validator.

## Verdict

`accepted_with_minor_findings`.

There are no unresolved fatal or major findings. The Stage 3 FFF structure bundle
preserves the primary-source distinctions required by the review brief, implements finite
validators and formula helpers within the declared scope, passes all required quality and
focused tests, and maintains pending-review claim and assumption boundaries.
