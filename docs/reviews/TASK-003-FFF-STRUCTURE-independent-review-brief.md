# TASK-003-FFF-STRUCTURE Independent Review Brief

```text
REVIEW BRIEF ID: REVIEW-BRIEF-TASK-003-FFF-STRUCTURE-001
TARGET TASK IDS: TASK-003-FFF-STRUCTURE-SPEC, TASK-003-FFF-STRUCTURE-IMPL
EXPECTED REVIEW ID: REV-TASK-003-FFF-STRUCTURE-001
TARGET BRANCH: main after PR #12
TARGET IMPLEMENTATION COMMIT: 154241c57504cc7d4b6d593ea42f9360878a151a
EXPECTED OUTPUT: docs/reviews/REV-TASK-003-FFF-STRUCTURE-001.md
```

## Reviewer Role

You are an independent verifier for a computational research repository. Start from
the repository files, the primary source, and this brief. Do not assume that the
specification, fixtures, implementation, tests, or claim wording are correct because
the implementer says they are correct.

This review validates the Stage 3 FFF structure bundle:

- source transcription for permutation-group and measurable-space definitions;
- formal specs;
- small oracle fixtures;
- finite helper implementation;
- exact and property tests;
- traceability and claim boundaries.

This review does not validate Stage 1 total orders/cyclic groups, Stage 2 FBT,
future FBT theorem work, evolutionary dynamics, ML/RL, dashboards, release capsules,
or claims about real perception, consciousness, spacetime, ontology, biology, or
metaphysics.

## Required Read Order

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

Treat previous Stage 1 and Stage 2 reviews as process history only. They are not
oracles for this Stage 3 result.

## Primary Source To Audit

Use the version of record / open full text for `SRC-FFF-2020`:

```text
Prakash, C., Fields, C., Hoffman, D. D., Prentner, R., & Singh, M. (2020).
Fact, Fiction, and Fitness. Entropy, 22(5), 514.
https://doi.org/10.3390/e22050514
https://www.mdpi.com/1099-4300/22/5/514
```

Required source locators:

- Section 4, Permutation Groups Theorem;
- Appendix A.1, Definitions A1-A4;
- Appendix A.3, "Permutation Groups Theorem";
- Section 4, Measurable Structures Theorem;
- Appendix A.5, "Measurable Structure Theorem".

Do not use AI summaries, blogs, podcasts, videos, or repository prose as the source
oracle when the primary paper is available.

## Files To Inspect

Core task/spec files:

- `tasks/TASK-003_fff_structure_spec.md`
- `tasks/TASK-003_fff_structure_impl.md`
- `specs/fff/permutation_groups.md`
- `specs/fff/measurable_spaces.md`

Fixture and oracle tests:

- `tests/fixtures/fff/stage3_structure_spec_cases.json`
- `tests/exact/test_fff_stage3_spec_gate.py`
- `tests/exact/test_fff_permutation_groups.py`
- `tests/exact/test_fff_measurable_spaces.py`
- `tests/properties/test_fff_properties.py`

Implementation:

- `src/fts_lab/fff/permutation_groups.py`
- `src/fts_lab/fff/measurable_spaces.py`
- `src/fts_lab/fff/functions.py`
- `src/fts_lab/fff/admissibility.py`
- `src/fts_lab/fff/formulas.py`
- `src/fts_lab/fff/__init__.py`

Traceability and docs:

- `sources/source_map.md`
- `sources/claim_matrix.csv`
- `assumptions/register.md`
- `README.md`
- `CHANGELOG.md`
- `src/fts_lab/doctor.py`
- `tests/integration/test_cli_and_smoke.py`

## Required Independent Derivations

Do these derivations without importing the production Stage 3 implementation. Small
scripts or scratch code are allowed, but they must be independent of
`src/fts_lab/fff/permutation_groups.py` and `src/fts_lab/fff/measurable_spaces.py`.

### Permutation Groups

Verify from `SRC-FFF-2020` and the specs:

- the source uses a second-order construction `(phi, f)`, not ordinary
  `S_n -> S_n` group-homomorphism counting;
- the source action law is `f(g . x) = phi(g) . f(x)`;
- the theorem formula is scoped to `n >= 5`;
- the source count used in the committed fixtures is `2*n + n!`;
- the denominator used for the source ratio is `n^n - (n - 1)^n`;
- the implementation rejects formula use below `n = 5`.

Independently recompute fixture cases:

```text
n = 5:
2*n + n! = 10 + 120 = 130
n^n - (n - 1)^n = 5^5 - 4^5 = 3125 - 1024 = 2101

n = 6:
2*n + n! = 12 + 720 = 732
n^n - (n - 1)^n = 6^6 - 5^6 = 46656 - 15625 = 31031
```

Also independently check at least one positive and one negative action-law example:

- positive inner-conjugation example where `f = h` and
  `phi(g) = h * g * h^-1`;
- positive constant-function example with trivial target action;
- negative function that fails `f(g . x) = phi(g) . f(x)`.

Pay special attention to the `S_6` outer-automorphism caveat. The implementation may
be acceptable while still deferring this as a review-sensitive source-count audit, but
it must not silently claim to have exhausted all `Aut(S_n)` issues.

### Measurable Spaces

Verify from `SRC-FFF-2020` and the specs:

- finite event algebras are represented through partition bases;
- algebra order `k` is the number of base blocks;
- algebra characteristic is a multiset of base-block sizes;
- measurability is checked by inverse images of codomain measurable events;
- for partition bases, checking inverse images of codomain base blocks is sufficient;
- all functions are measurable when the algebra on `W` is discrete;
- all functions are measurable when the algebra on `V` is trivial;
- the Appendix A.5 expression is an upper bound, not an exact count in every case;
- the fixed-`m` asymptotic caveat is not converted into an all-growth-path claim.

Independently recompute fixture cases:

```text
W base = [[0, 1], [2]]
V base = [[0], [1]]

Measurable functions must be constant on W block [0, 1], while element 2 is free:
total measurable functions = 2 * 2 = 4
admissible measurable functions = 3

W discrete, |W| = 3, |V| = 2:
all functions measurable = 2^3 = 8
admissible measurable functions = 7

V trivial, |W| = 3, |V| = 2:
all functions measurable = 2^3 = 8
admissible measurable functions = 7

Non-measurable witness f = [0, 1, 1]:
inverse image of V block [0] is [0], which splits W block [0, 1].
```

Independently recompute bound cases using the integer form:

```text
bound(n, m, k) = m^(k - 1) + m^(k - 1) * (m - 1)^(n - k + 1)

n=3, m=2, k=2:
2^1 + 2^1 * 1^2 = 4

n=4, m=3, k=2:
3^1 + 3^1 * 2^3 = 27

n=5, m=3, k=3:
3^2 + 3^2 * 2^3 = 81
```

## Required Checks

Run or independently reproduce equivalent checks:

```bash
py -m uv run ruff check .
py -m uv run ruff format --check .
py -m uv run mypy src
py -m uv run pytest
py -m uv run fts doctor --release-check
```

Also run the focused Stage 3 tests:

```bash
py -m uv run pytest tests/exact/test_fff_stage3_spec_gate.py
py -m uv run pytest tests/exact/test_fff_permutation_groups.py
py -m uv run pytest tests/exact/test_fff_measurable_spaces.py
py -m uv run pytest tests/properties/test_fff_properties.py
```

If bare `uv` is available, the equivalent `uv run ...` commands are acceptable.
Do not require internet access for tests.

## Audit Questions

1. Do the Stage 3 specs match the primary source locators, or do they import
   definitions from memory or secondary explanations?
2. Does `specs/fff/permutation_groups.md` clearly distinguish first-order group
   homomorphisms, group actions, and source second-order `(phi, f)` homomorphisms?
3. Does `src/fts_lab/fff/permutation_groups.py` implement the action-compatibility
   law without claiming ordinary homomorphism enumeration is sufficient?
4. Does the permutation formula helper enforce `n >= 5`?
5. Do tests include positive and negative second-order action-law cases?
6. Is the permutation count-object issue still represented as pending review rather
   than silently resolved?
7. Does `specs/fff/measurable_spaces.md` preserve partition-basis definitions,
   order `k`, characteristic, inverse-image measurability, and special cases?
8. Does `src/fts_lab/fff/measurable_spaces.py` validate partitions, construct event
   algebras, check inverse-image measurability, and separate exact enumeration from
   source upper bounds?
9. Do tests verify the non-measurable witness that splits a source block?
10. Do tests verify `W` discrete and `V` trivial special cases?
11. Does the code ever label the Appendix A.5 bound as an exact count?
12. Does any public wording imply that `CLM-FFF-PERM-001` or `CLM-FFF-MEAS-001` is
    reviewed before this independent review is complete?
13. Are `ASM-FFF-0002` and `ASM-FFF-0003` still open or explicitly review-sensitive,
    rather than silently approved by implementation?
14. Are claim rows, specs, tests, and implementation targets mutually consistent?
15. Does any Stage 3 wording overclaim into real perception, biological probability,
    consciousness, spacetime, ontology, ML/RL, or evolutionary dynamics?

## Blocking Criteria

Mark the review `blocked` if any `fatal` or `major` finding remains unresolved.

Fatal examples:

- a primary-source theorem formula or definition is transcribed incorrectly;
- the permutation implementation substitutes ordinary group-homomorphism counting for
  the source second-order construction;
- the measurable-space implementation treats the Appendix A.5 bound as an exact count
  in all cases;
- fixture expected values are wrong;
- production code hard-codes test fixture outputs rather than computing them;
- full quality checks cannot pass from a clean checkout;
- public claims exceed the approved `CLM-...` rows;
- metaphysical, consciousness, real-perception, biology, ML/RL, or evolutionary claims
  are presented as Stage 3 results.

Major examples:

- source locators are too vague to audit the definitions;
- `n < 5` permutation formula behavior is not guarded;
- partition canonicalization accepts invalid overlapping or incomplete partitions;
- inverse-image measurability is checked in the wrong direction;
- special cases for discrete `W` or trivial `V` are omitted or contradicted;
- code and tests use inconsistent function/partition conventions;
- claim rows imply independent review has already accepted Stage 3;
- assumptions `ASM-FFF-0002` or `ASM-FFF-0003` are effectively approved without Human PI
  decision.

Minor examples:

- wording can be clearer without changing claim boundaries;
- local environment uses `py -m uv` instead of bare `uv`;
- non-blocking documentation or organization issue;
- useful additional edge cases are suggested but current claims remain valid.

## Expected Review Report

Create `docs/reviews/REV-TASK-003-FFF-STRUCTURE-001.md` with:

````markdown
# REV-TASK-003-FFF-STRUCTURE-001 - Independent Review of Stage 3 FFF Structure Bundle

```text
REVIEW ID: REV-TASK-003-FFF-STRUCTURE-001
TASK IDS: TASK-003-FFF-STRUCTURE-SPEC, TASK-003-FFF-STRUCTURE-IMPL
COMMIT REVIEWED: <commit>
REVIEWER ROLE: Fresh-context AI/Codex Verifier
DATE: <YYYY-MM-DD>
VERDICT: accepted | accepted_with_minor_findings | blocked
```

## Scope

## Commands Run

## Primary Source Audit

## Independent Permutation Derivations

## Independent Measurable-Space Derivations

## Specification Audit

## Code And Test Audit

## Traceability And Claim Boundary Audit

## Fatal Findings

## Major Findings

## Minor Findings

## Verdict
````

If the verdict is `accepted` or `accepted_with_minor_findings` and there are no
unresolved fatal or major findings, the project may record review status
`REV-TASK-003-FFF-STRUCTURE-001_no_fatal_or_major` for
`CLM-FFF-PERM-001` and `CLM-FFF-MEAS-001`.

Independent review alone does not approve `ASM-FFF-0002` or `ASM-FFF-0003`. After an
accepted review, Human PI acceptance is still required before marking those assumptions
`APPROVED` or `SOURCE_RESOLVED`, or before making any public Stage 3 release claim.
