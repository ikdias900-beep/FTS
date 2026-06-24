# AGENTS.md — Fitness, Truth & Structure Lab

**Project:** Fitness, Truth & Structure Lab  
**Instruction version:** 0.1  
**Human-facing strategy language:** Russian  
**Code, identifiers, schemas, and public API language:** English

## 1. Mission

Build an open, auditable computational research program around:

- **FBT:** `Fitness Beats Truth in the Evolution of Perception`;
- **FFF:** `Fact, Fiction, and Fitness`;
- later extensions connecting reward optimization, structure preservation, robustness, transfer, and learned representations.

The goal is to test explicit mathematical and computational claims—not to confirm a preferred metaphysics. A negative, null, discrepancy, or assumption-sensitive result is a valid result.

## 2. Required context and read order

Before changing the repository, read these files in this order:

1. `AGENTS.md` — non-negotiable repository rules.
2. `01_research_strategy.md` — program mission, stages, publication gates, and Definition of Done.
3. `02_stage_tasks_roles.md` — participant responsibilities, stage-specific acceptance criteria, and review protocol.
4. The current task brief, initially `tasks/TASK-000_bootstrap_repo.md`.
5. `sources/source_map.md` — canonical source IDs, editions, and links.
6. `sources/claim_matrix.csv` — claim IDs, source locators, allowed claims, and forbidden overclaims.
7. `assumptions/register.md` — approved, proposed, unresolved, and superseded assumptions.

Canonical filenames do **not** contain duplicate suffixes such as `(1)`. If imported copies are named `01_research_strategy(1).md` or `02_stage_tasks_roles(1).md`, copy them to the canonical names above without changing their contents.

Codex automatically reads `AGENTS.md`, but it does not automatically treat the strategy documents as instructions. Read them explicitly at the start of each new task.

## 3. Instruction priority

Use this order when instructions conflict:

1. a direct decision from the Human Principal Investigator;
2. an approved Research Decision Record (`RDR-...`);
3. the current task brief (`TASK-...`);
4. an approved formal specification in `specs/`;
5. `01_research_strategy.md` and `02_stage_tasks_roles.md`;
6. this file for repository-wide defaults.

A task may narrow scope but may not silently relax scientific-integrity, traceability, testing, or source requirements. Any deliberate exception requires a human-approved RDR.

## 4. Current scope

The initial active task is `TASK-000`: repository bootstrap and reproducibility infrastructure only.

Until `TASK-000` is accepted, do **not** implement:

- FBT or FFF mathematical results;
- evolutionary simulations;
- ML/RL models;
- dashboards or web applications;
- GPU code;
- claims about perception, evolution, consciousness, or reality.

Do not implement future stages merely because they appear in the strategy.

## 5. Roles

- **H — Human Principal Investigator:** intention, scope, approval of assumptions, admissible public claims, release decisions.
- **R — Research AI:** source analysis, formalization, experiment design, explanation, interpretation.
- **C — Codex Implementer:** code, tests, CI, manifests, documentation, release artifacts.
- **V — Independent Verifier:** fresh-context derivation, counterexample search, source-to-code audit.
- **O — Automated Oracles:** exact arithmetic, brute-force checks, property tests, regression tests, CI.

The same AI product may perform R, C, and V only in separate sessions. The verifier must not inherit the implementer's private reasoning or justification narrative.

## 6. Epistemic status

Every **scientific** claim, result, figure, dataset, or experiment must use exactly one status:

- **R — Reproduction:** follows a published definition, formula, theorem, or numerical example.
- **C — Computational reconstruction:** fills source gaps using explicitly registered assumptions.
- **E — Extension:** new model, metric, experiment, or theorem not claimed in the source.
- **A — Analogy:** transfers an idea to ML/AI or another domain; it is not a test of the original biological or philosophical claim.

Infrastructure smoke artifacts have no scientific status: use `epistemic_status: null`, `claim_ids: []`, and `artifact_kind: infrastructure_smoke`. Never mislabel infrastructure as R/C/E/A.

Never aggregate different epistemic statuses into one result without preserving per-row/per-run status and explaining the mixture.

## 7. Mandatory traceability IDs

Use stable IDs:

- `SRC-...` — source;
- `CLM-...` — claim;
- `ASM-...` — assumption;
- `RDR-...` — human-approved research decision;
- `TASK-...` — implementation task;
- `EXP-...` — experiment/run family;
- `ART-...` — saved artifact;
- `REV-...` — independent review.

Every scientific implementation and artifact must link to:

- at least one `TASK`;
- at least one `CLM`;
- at least one `SRC`;
- all relevant `ASM` IDs, or an explicit empty list;
- the Git commit and dirty/clean state;
- dependency-lock checksum;
- command, parameters, inputs, outputs, and checksums.

A public claim without a `CLM` row is not publishable.

## 8. Source rules

1. Use primary papers for definitions, formulas, theorem statements, and reproduction targets.
2. Do not implement scientific definitions from memory, podcasts, blogs, videos, repository READMEs, or AI summaries when a primary source exists.
3. Record the exact source edition and locator: section, theorem/definition number, table, appendix, and page when available.
4. Page numbers may differ between an author manuscript and the version of record. State which edition supplied the locator.
5. Do not silently repair apparent source errors. Open a discrepancy issue and register the decision.
6. Do not commit copyrighted PDFs unless redistribution is clearly permitted. Prefer DOI/full-text links plus locally recorded checksums and access notes.
7. Third-party code is a comparison target, not an oracle, unless independently validated against the primary source.

## 9. Scientific-integrity rules

- Reproduction precedes reconstruction; reconstruction precedes extension; exact checks precede stochastic simulation; simple finite models precede ML.
- Never invent a missing parameter or tie rule. Add an `ASM` entry and wait for human approval when the choice can change a scientific result.
- Do not tune definitions, payoff functions, costs, measures, grids, seeds, or plots after seeing results without marking the analysis exploratory.
- Do not create an advantage by assigning unequal information, action access, compute, parameter count, or cost unless that inequality is the registered object of study.
- Do not interpret a finite grid frequency as a probability without an explicit measure.
- Do not interpret correlation as causation.
- Publish counterexamples, failed runs, null results, and discrepancies under the same artifact discipline as positive results.
- Never claim that FBT/FFF results prove that spacetime is an interface, consciousness is fundamental, or conscious agents are the ontology of reality.

## 10. Code and repository conventions

Unless an approved RDR says otherwise:

- Python reference runtime: **3.12**.
- Environment and lockfile: **uv** and `uv.lock`.
- Package layout: `src/fts_lab/`.
- Tests: `pytest`; property tests: `hypothesis`.
- Lint/format: `ruff`; static typing: `mypy`.
- CLI executable: `fts`, implemented from importable library code.
- UTF-8, LF line endings, deterministic serialization, UTC timestamps, SHA-256 checksums.
- Prefer the standard library; every new runtime dependency needs a short rationale in the PR or an RDR if it affects architecture.
- Mathematical core must be independent of notebooks, plotting, UI, and network access.
- Notebooks may analyze stable APIs; they may not contain the only implementation of a result.
- Randomness must be injected through an explicit seed or RNG object. Never hide a seed inside a function.
- Raw artifacts are immutable. Derived artifacts must name their inputs and may not overwrite raw data.
- CPU reference implementations are required before accelerators.
- Tests must not require internet access.

## 11. Required validation order

For a scientific module, validate in this order:

1. source transcription and formal specification;
2. hand-derived or independently derived small cases;
3. exact/rational oracle where possible;
4. unit tests and invariants;
5. property-based tests;
6. optimized implementation;
7. stochastic or large-scale experiments;
8. figures and UI;
9. independent fresh-context review.

A faster implementation may not replace the reference oracle.

## 12. File ownership and modification rules

- `01_research_strategy.md` and `02_stage_tasks_roles.md` are human-approved context. Do not edit them unless a task explicitly requests a revision.
- `sources/source_map.md` may be extended only with verified bibliographic information and stable source IDs.
- `sources/claim_matrix.csv` must remain valid UTF-8 CSV. Preserve existing IDs; never recycle a retired ID.
- `assumptions/register.md` records uncertainty and decisions. Never delete an assumption; mark it `REJECTED` or `SUPERSEDED`.
- A source definition belongs in a specification/claim record, not disguised as an assumption.
- An infrastructure choice belongs in an RDR when consequential; scientific assumptions belong in the assumption register.

## 13. Git, worktrees, and review

For substantial scientific work, prefer separate branches/worktrees for:

- specification and tests;
- implementation;
- independent oracle/review;
- documentation/demo after API stabilization.

The implementation branch must not weaken tests without explicit review. The independent checker must not import the production implementation. Do not merge with unresolved `fatal` or `major` review findings.

## 14. Start-of-task protocol

Before coding:

1. verify all required context files exist;
2. state the active `TASK` and its epistemic status;
3. summarize required outputs and explicit out-of-scope items;
4. list source, claim, and assumption IDs involved;
5. identify blockers or unresolved scientific decisions;
6. inspect existing code and tests before proposing changes.

If the task is fully specified, proceed without asking redundant questions. If a missing scientific decision could change the result, mark the task `BLOCKED: AMBIGUOUS`, record the issue, and do not choose the convenient answer silently.

## 15. Completion report

At task completion, report:

- files created or changed;
- commands run and their outcomes;
- tests, lint, typing, and reproducibility checks;
- artifacts and checksums;
- linked `TASK`, `CLM`, `SRC`, and `ASM` IDs;
- assumptions introduced or resolved;
- deviations from the task;
- remaining blockers and review findings;
- scientific claims produced—normally none for `TASK-000`.
