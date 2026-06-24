# Source Map

**Project:** Fitness, Truth & Structure Lab  
**Version:** 0.1  
**Last verified:** 2026-06-24  
**Purpose:** canonical source IDs, editions, links, stage usage, and source-handling rules.

## 1. Source policy

- Use the DOI/version of record as the canonical bibliographic reference.
- Use an openly accessible publisher page or author manuscript for implementation work when available.
- Record the exact edition used for a formula or page locator. Pagination can differ between editions.
- A repository, blog, podcast, video, or AI summary may suggest a question but may not define an R-status implementation when a primary paper exists.
- Do not commit copyrighted PDFs unless redistribution rights are explicit. Store links, access dates, and local checksums instead.
- Before implementing a theorem, transcribe its definitions and formula into `specs/` and have a fresh-context verifier compare the transcription with the source.

## 2. Internal governing documents

| Path | Role |
|---|---|
| `01_research_strategy.md` | Program mission, stages, publication gates, scientific boundaries. |
| `02_stage_tasks_roles.md` | Participant roles, stage tasks, acceptance criteria, review process. |
| `AGENTS.md` | Repository-wide Codex instructions and integrity rules. |
| `tasks/TASK-000_bootstrap_repo.md` | Completed bootstrap task. |
| `tasks/TASK-001_fff_core_orders_cyclic.md` | Completed Stage 1 exact-count core task. |
| `tasks/TASK-001_stage1_sweeps_tables.md` | Current Stage 1 manifest-backed sweep/table task. |
| `sources/claim_matrix.csv` | Claim-to-source-to-test traceability. |
| `assumptions/register.md` | Scientific assumptions and unresolved decision points. |

## 3. Core primary scientific sources

### SRC-FBT-2021

**Citation**  
Prakash, C., Stephens, K. D., Hoffman, D. D., Singh, M., & Fields, C. (2021). *Fitness Beats Truth in the Evolution of Perception*. Acta Biotheoretica, 69, 319–341.

**Canonical DOI**  
https://doi.org/10.1007/s10441-020-09400-0

**Version of record / publisher page**  
https://link.springer.com/article/10.1007/s10441-020-09400-0

**Author manuscript / open PDF**  
https://sites.socsci.uci.edu/~ddhoff/FitnessBeatsTruth_apa_PBR

**Primary use**

- Stage 2 exact reproduction of the numerical appendix;
- Stage 4 finite FBT decision problems;
- Stage 5 evolutionary interpretation and theorem-domain checks.

**Key implementation targets**

- definitions of Truth and Fitness-only strategies;
- priors, likelihoods, posteriors, MAP estimates, and expected fitness in the numerical example;
- Theorem 4 and its stated domain;
- distinctions among infinite populations, finite populations with full selection, and sufficiently large finite populations with weak selection.

**High-risk interpretation points**

- tie handling for non-unique MAP estimates;
- the measure over fitness functions and priors;
- what “probability” means in the theorem;
- whether a later simulation faithfully instantiates the theorem's strategy definitions;
- avoiding the claim that a toy implementation establishes biological universality.

---

### SRC-FFF-2020

**Citation**  
Prakash, C., Fields, C., Hoffman, D. D., Prentner, R., & Singh, M. (2020). *Fact, Fiction, and Fitness*. Entropy, 22(5), 514.

**Canonical DOI**  
https://doi.org/10.3390/e22050514

**Open full text / publisher page**  
https://www.mdpi.com/1099-4300/22/5/514

**Primary use**

- Stage 1 total orders and cyclic groups;
- Stage 3 permutation groups and measurable spaces;
- Stage 6 structure-preservation metrics, with extensions explicitly marked E.

**Key implementation targets**

- definition and count of admissible payoff functions;
- Total Orders Theorem and Appendix A.2;
- Permutation Groups Theorem and Appendix A.3;
- Cyclic Groups Theorem and Appendix A.4;
- Measurable Structures Theorem and Appendix A.5;
- use of counting measure and the paper's asymptotic limits.

**High-risk interpretation points**

- ordinary group homomorphism versus the paper's second-order morphism construction for symmetric groups;
- exact meaning of order homomorphism and treatment of constant/order-reversing maps;
- reverse-homomorphism character of measurability;
- exceptional trivial/discrete measurable structures;
- not presenting a bound as an exact count;
- not converting a counting-measure theorem into a claim about all plausible biological payoff distributions.

---

### SRC-ITP-2015

**Citation**  
Hoffman, D. D., Singh, M., & Prakash, C. (2015). *The Interface Theory of Perception*. Psychonomic Bulletin & Review, 22, 1480–1506.

**Canonical DOI**  
https://doi.org/10.3758/s13423-015-0890-8

**Publisher page**  
https://link.springer.com/article/10.3758/s13423-015-0890-8

**Primary use**

- conceptual context for why FBT and FFF matter;
- definitions and claims about interface strategies;
- historical comparison with evolutionary games and genetic algorithms.

**Not a direct oracle for**

- the exact Stage 2 FBT appendix arithmetic;
- the four FFF counting theorems;
- the claim that conscious-agent ontology has been established.

---

### SRC-OOC-2014

**Citation**  
Hoffman, D. D., & Prakash, C. (2014). *Objects of Consciousness*. Frontiers in Psychology, 5, 577.

**Canonical DOI**  
https://doi.org/10.3389/fpsyg.2014.00577

**Open full text**  
https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2014.00577/full

**Author PDF**  
https://sites.socsci.uci.edu/~ddhoff/Objects_of_Consciousness.pdf

**Primary use**

- boundary/context document separating the negative evolutionary argument from the positive conscious-agent proposal;
- possible future companion project on finite Markov-kernel dynamics.

**Scope warning**

FBT and FFF can challenge assumptions about veridical perception. They do not by themselves establish the conscious-agent formalism or its physical interpretations.

## 4. Primary predecessor sources for later evolutionary work

These are not required for `TASK-000`, but they should be consulted before reconstructing earlier simulations.

### SRC-NSVP-2010

Mark, J. T., Marion, B. B., & Hoffman, D. D. (2010). *Natural Selection and Veridical Perception*. Journal of Theoretical Biology, 266, 504–515.  
DOI: https://doi.org/10.1016/j.jtbi.2010.07.020

**Use:** predecessor evolutionary-game models and strategy comparisons.  
**Status:** bibliographic identity verified; exact implementation locators must be pinned before use.

### SRC-CEP-2012

Hoffman, D. D., & Singh, M. (2012). *Computational Evolutionary Perception*. Perception, 41, 1073–1091.

**Use:** genetic-algorithm and computational-evolutionary-perception background.  
**Status:** add a verified DOI/full-text link before using this source for an R-status implementation.

### SRC-TRUE-2013

Hoffman, D. D., Singh, M., & Mark, J. T. (2013). *Does Natural Selection Favor True Perceptions?* Proceedings of SPIE 8651, 865104.  
DOI: https://doi.org/10.1117/12.2011609

**Use:** predecessor argument and simulation context.  
**Status:** exact model details must be transcribed and independently checked before implementation.

## 5. Independent adversarial source

This source is not a primary source for Hoffman's definitions. It is included to design falsification and robustness tests.

### SRC-CRIT-2021

Charan, A. R., Gharibzadeh, S., & Firouzabadi, S. M. (2021). *Realism is Almost True: A Critique of the Interface Theory of Perception*.  
Preprint: https://arxiv.org/abs/2111.03864

**Use:** environment-shift and extinction counter-scenarios; adversarial review of interface strategies.  
**Epistemic use:** extension/review context, not an oracle for FBT or FFF reproduction.

## 6. Operational primary sources for Codex workflow

### SRC-CODEX-AGENTS-2026

OpenAI Developers. *Custom instructions with AGENTS.md*.  
https://developers.openai.com/codex/guides/agents-md

**Use:** project instruction discovery and size/precedence behavior.

### SRC-CODEX-WORKTREES-2026

OpenAI Developers. *Worktrees — Codex app*.  
https://developers.openai.com/codex/app/worktrees

**Use:** isolated implementation, independent checking, and documentation branches/worktrees.

## 7. Stage-to-source matrix

| Stage | Required sources | Optional/adversarial sources |
|---|---|---|
| 0 | Internal governing documents; Codex operational sources | None |
| 1 | `SRC-FFF-2020` | `SRC-ITP-2015` for context only |
| 2 | `SRC-FBT-2021` | `SRC-ITP-2015` for context only |
| 3 | `SRC-FFF-2020` | Standard algebra/measure references added later |
| 4 | `SRC-FBT-2021` | `SRC-NSVP-2010`, `SRC-TRUE-2013` |
| 5 | `SRC-FBT-2021`, verified evolutionary-dynamics references | `SRC-CRIT-2021`, predecessors |
| 6 | `SRC-FBT-2021`, `SRC-FFF-2020` | representation-learning literature added later |
| 7 | Stage 6 sources plus primary ML/RL sources | critical robustness literature |
| 8 | All sources used by published claims | archival/reproducibility standards |

## 8. Locator format

Use this format in specs and claim records:

```text
SOURCE_ID; edition; section/theorem/definition/table/appendix; page if stable
```

Examples:

```text
SRC-FBT-2021; version of record; Appendix: Calculations for the Numerical Example in Table 1
SRC-FBT-2021; author manuscript; Theorem 4, “The Fitness Beats Truth Theorem”
SRC-FFF-2020; version of record; Section 4 and Appendix A.4, Cyclic Groups Theorem
```
