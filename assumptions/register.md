# Assumption Register

**Project:** Fitness, Truth & Structure Lab  
**Version:** 0.1  
**Rule:** never delete an assumption record; change status and preserve history.

## 1. Purpose

This register contains choices that are **not fully fixed by a primary source** and that can affect scientific results or their interpretation.

Do not put the following here:

- an explicit definition copied from a source—put it in a formal specification and claim record;
- an ordinary implementation detail with no scientific effect—put it in code/PR notes;
- a consequential infrastructure or publication decision—use an `RDR-...`;
- an observed result—use an experiment manifest and report.

## 2. Status vocabulary

| Status | Meaning |
|---|---|
| `OPEN` | Decision required; implementation that depends on it is blocked. |
| `PROPOSED` | A candidate choice exists but has not been approved by the Human PI. |
| `APPROVED` | Human PI approved the assumption for a declared scope. |
| `REJECTED` | Explicitly considered and not allowed. |
| `SUPERSEDED` | Replaced by another assumption ID; historical record remains. |
| `SOURCE_RESOLVED` | Further source work showed that no project assumption was needed. |

## 3. Impact vocabulary

- `LOW`: cannot change headline result, but may affect formatting or edge cases.
- `MEDIUM`: may change some cells, counts, or secondary metrics.
- `HIGH`: may change direction, dominance, asymptotic interpretation, or public conclusion.

## 4. Active and known decision points

| assumption_id | stage | category | statement / unresolved question | why needed | source_ids | claim_ids | alternatives | impact | status | approved_by | approved_at | validation plan | notes |
|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| `ASM-FBT-0001` | 2/4 | tie handling | How should a general Truth strategy act when multiple world states share the maximum posterior probability? | The numerical example has a unique MAP result, but the reusable engine must not silently choose a tie rule. | `SRC-FBT-2021` | future general FBT claims | return a set; deterministic lexical rule; randomize uniformly; preserve full posterior | HIGH | OPEN | — | — | Implement no general tie behavior until the source is re-read and the Human PI approves a rule; test all approved variants separately. | Decision brief prepared in `docs/decisions/RDR-0004-stage4-fbt-blockers.md`; not approved yet. Does not block exact Stage 2 calculations if no tie occurs. |
| `ASM-FBT-0002` | 2/4 | zero-probability observation | What should the API return when an observation has zero marginal probability? | Bayes posterior is undefined; silent normalization would fabricate information. | `SRC-FBT-2021` | future general FBT claims | explicit exception; undefined result object; exclude by domain contract | MEDIUM | OPEN | — | — | Add a failing test first; approve one behavior for production and retain alternatives in extension tests. | Decision brief prepared in `docs/decisions/RDR-0004-stage4-fbt-blockers.md`; not approved yet. Stage 2 source example has nonzero marginals. |
| `ASM-FBT-0003` | 4 | finite atlas grid measure | What finite rational grid and measure semantics may be used for the Stage 4 atlas? | A project grid frequency is not the source theorem probability; changing the grid can change headline aggregate patterns. | `SRC-FBT-2021` | `CLM-FBT-ATLAS-001` | fixed uniform rational grid; weighted grid; stratified grid with per-family reporting; no aggregate probability claim | HIGH | OPEN | — | — | Spec gate records the separation; production atlas blocked until grid version and reporting semantics are approved. | Decision brief prepared in `docs/decisions/RDR-0004-stage4-fbt-blockers.md`; not approved yet. Introduced by `TASK-004-FBT-ATLAS-SPEC`; does not block source transcription. |
| `ASM-FBT-0004` | 4 | truth strategy family | Which truth-strategy variants are part of the primary Stage 4 comparison, and how are source MAP Truth and extension baselines separated? | Posterior sampling, posterior mean, and full-posterior baselines can change the comparison and must not be mislabeled as the source Truth strategy. | `SRC-FBT-2021` | `CLM-FBT-ATLAS-001` | source MAP only; source MAP plus separately reported extension baselines; full posterior as primary baseline | HIGH | OPEN | — | — | Spec gate lists candidate families; production atlas blocked until primary and exploratory strategy families are approved. | Decision brief prepared in `docs/decisions/RDR-0004-stage4-fbt-blockers.md`; not approved yet. Posterior mean requires an approved metric or vector structure on `W`. |
| `ASM-FFF-0001` | 1 | total-order morphism transcription | Stage 1 public total-order outputs must show both the source orientation-witness count and the distinct unique-function count. | The source formula counts preserving/reversing monotonicity witnesses; finite unique-function counts differ because the admissible maximum constant function has both witnesses. | `SRC-FFF-2020` | `CLM-FFF-ORD-001` | show only source witnesses; show only unique functions; show both counts | HIGH | APPROVED | Human PI | 2026-06-25 | `REV-TASK-001-001` independently derived the small case; tests must keep both source witness and unique-function counts visible. | Approved via `RDR-0002`; GitHub issue #1 remains the discrepancy/interpretation record. |
| `ASM-FFF-0002` | 3 | symmetric-group morphism | What exact data constitute the paper's “second-order homomorphism,” and how are ordinary homomorphisms, respectful maps, and automorphisms combined? | Replacing the construction with an ordinary group-homomorphism count would test a different theorem. | `SRC-FFF-2020` | `CLM-FFF-PERM-001` | exact Appendix A.3 construction only for R; simplified variants only as E | HIGH | SOURCE_RESOLVED | Human PI | 2026-06-28 | `REV-TASK-003-FFF-STRUCTURE-001` found no fatal or major source/spec/code finding; retain tests for action-law and `n >= 5` scope. | Source/spec issue resolved for the reviewed Stage 3 finite-helper scope. Future exhaustive automorphism enumeration, alternate count-object reporting, or extensions require a new task or decision. |
| `ASM-FFF-0003` | 3 | measurable structures | How will finite algebras, their order k, exceptional trivial/discrete cases, and the theorem's bound be represented without treating the bound as an exact count? | Multiple reasonable encodings can create duplicate structures or alter counts. | `SRC-FFF-2020` | `CLM-FFF-MEAS-001` | canonical partitions; explicit event algebras; isomorphism-reduced variants | HIGH | SOURCE_RESOLVED | Human PI | 2026-06-28 | `REV-TASK-003-FFF-STRUCTURE-001` found no fatal or major source/spec/code finding; retain tests for partition validation, inverse-image measurability, special cases, and bound/exact separation. | Source/spec issue resolved for the reviewed Stage 3 finite-helper scope. Future algebra-isomorphism sweeps, alternate canonicalization, or extensions require a new task or decision. |

## 4.1 Stage 3 spec-gate notes

`TASK-003-FFF-STRUCTURE-SPEC` adds draft specifications and small-case fixture
checks for `ASM-FFF-0002` and `ASM-FFF-0003`:

- `specs/fff/permutation_groups.md`
- `specs/fff/measurable_spaces.md`
- `tests/fixtures/fff/stage3_structure_spec_cases.json`
- `tests/exact/test_fff_stage3_spec_gate.py`

These artifacts did not approve the assumptions or unblock production Stage 3
implementation by themselves. The statuses remained `OPEN` until independent review and
Human PI acceptance of the formalization.

## 4.2 Stage 3 implementation-bundle notes

`TASK-003-FFF-STRUCTURE-IMPL` adds source-explicit finite helper implementations and
tests for the Stage 3 draft specs:

- `src/fts_lab/fff/permutation_groups.py`
- `src/fts_lab/fff/measurable_spaces.py`
- `tests/exact/test_fff_permutation_groups.py`
- `tests/exact/test_fff_measurable_spaces.py`

This implementation did not by itself approve `ASM-FFF-0002` or `ASM-FFF-0003`. After
`REV-TASK-003-FFF-STRUCTURE-001` recorded no fatal or major findings and the Human PI
requested status updates on 2026-06-28, both assumptions were marked
`SOURCE_RESOLVED` for the reviewed Stage 3 finite-helper scope.

## 5. Entry template

Copy this section for each new assumption:

```markdown
### ASM-XXXX-0000 — Short title

- **Stage:**
- **Category:**
- **Status:** OPEN / PROPOSED / APPROVED / REJECTED / SUPERSEDED / SOURCE_RESOLVED
- **Impact:** LOW / MEDIUM / HIGH
- **Source IDs:**
- **Claim IDs:**
- **Problem or source gap:**
- **Proposed assumption:**
- **Alternatives considered:**
- **Why this choice is not neutral:**
- **Expected result sensitivity:**
- **Validation / ablation plan:**
- **Approved by Human PI:**
- **Approval date (UTC):**
- **Supersedes / superseded by:**
- **Notes:**
```

## 6. Approval rule

Codex may create an `OPEN` or `PROPOSED` entry. Codex may not mark a scientifically consequential assumption `APPROVED`; that status requires an explicit Human PI decision, ideally linked to an `RDR-...`.

An experiment manifest must list every approved assumption it depends on. An empty assumption list means the result uses no project-added scientific assumptions beyond explicit source definitions—it does not mean assumptions were forgotten.
