# FBT Theorem 4 Domain Specification

TASK ID: `TASK-004-FBT-ATLAS-SPEC`  
EPISTEMIC STATUS: `R`  
SOURCE ID: `SRC-FBT-2021`  
CLAIM ID: `CLM-FBT-THM-001`  
ASSUMPTION IDS: `ASM-FBT-0001`, `ASM-FBT-0002`

## Source Locator

`SRC-FBT-2021; author manuscript; Mathematical Background for the Main Theorem;
General Perceptual Mappings and Bayesian Inference; Expected Fitness; Two Perceptual
Strategies; Theorem 4, “The Fitness Beats Truth” Theorem`

Canonical bibliographic locator:
Prakash, C., Stephens, K. D., Hoffman, D. D., Singh, M., & Fields, C. (2021).
*Fitness Beats Truth in the Evolution of Perception*. Acta Biotheoretica, 69,
319-341. https://doi.org/10.1007/s10441-020-09400-0

The open author manuscript was used for this spec-gate transcription because it exposes
the theorem-domain paragraphs and proof sketch in accessible text. Page numbers may
differ from the version of record.

## Source-Derived Objects

### World Space

The source theorem is stated for a world space `W` with measurable structure. The
author manuscript presents the general case as a compact regular Borel space with a
measurable event algebra and a prior probability measure. For finite computational
design work, `W` may later be restricted to a finite set, but that finite restriction is not
the theorem's full domain.

### Prior

The theorem-domain prior is a probability measure on `W`. In the manuscript, priors
under discussion are absolutely continuous with respect to a base Borel/uniform measure
and are represented by nonnegative continuous densities that integrate to one.

Finite atlas priors must therefore be explicitly labeled as a project-defined finite
restriction, not as the source's full prior space.

### Perceptual Space

`X` is the finite perceptual-state space. The source theorem lower-bound expression is
written in terms of `abs(X)`, the number of perceptual states.

The fixture checks the arithmetic expression:

```text
strict_domination_lower_bound = (abs(X) - 3) / (abs(X) - 1)
```

This expression is nonnegative for `abs(X) >= 3` and approaches `1` as `abs(X)` grows.

### Perceptual Map Or Kernel

The source distinguishes:

- a pure perceptual map, where a world state yields one sensory state; and
- a general perceptual mapping with dispersion/noise, represented as a Markov kernel
  from world states to probability distributions on `X`.

Stage 4 implementation must choose and label its mode. A pure finite map and a
stochastic kernel are not interchangeable artifacts.

## Bayesian Inference

For a perception `x`, Bayesian inference computes a posterior distribution over world
states. In a finite implementation this has the same shape as the Stage 2 appendix
calculation:

```text
P(x) = sum_w p(x | w) * mu(w)
p(w | x) = p(x | w) * mu(w) / P(x)
```

If `P(x) = 0`, the posterior is undefined. `RDR-0004` approves the Stage 4 policy:
primary exact paths do not smooth with epsilon; the observation-level result is
`zero_marginal_undefined`, and dependent comparisons are `blocked_zero_marginal`.

## MAP Estimate

The source Truth strategy uses a maximum-a-posteriori world estimate for each
perception. MAP estimates may be non-unique. The source theorem discussion treats
generic uniqueness separately from possible ties.

Stage 4 production implementation must not silently choose among MAP ties. `RDR-0004`
approves the Stage 4 policy: represent ties as full MAP sets; classify cases whose
outcome depends on the tied maximizer as `map_tie_policy_sensitive`; do not use lexical
or random tie-breaks in primary results.

## Expected Fitness

Given a nonnegative fitness function over world states, the expected fitness of a
perception is the posterior-weighted average of fitness over world states.

For a finite implementation:

```text
expected_fitness(x) = sum_w p(w | x) * fitness(w)
```

This is the same computation shape as `TASK-002-FBT-NUMERICAL`, but Stage 4 must handle
families of finite problems rather than the single appendix table.

## Source Strategies

### Truth Strategy

The source Truth strategy ranks perceptual states by taking the MAP world estimate for
each perceptual state and then evaluating the fitness associated with that estimated
world state.

This is a point-estimate strategy. It is not the same as full-posterior expected utility.

### Fitness-Only Strategy

The source Fitness-only strategy ranks perceptual states by expected fitness directly,
using the posterior distribution over world states and the fitness function.

It does not first estimate the true world state.

## Theorem 4 Claim Boundary

The source theorem states a lower bound for the probability that Fitness-only strictly
dominates Truth over the theorem's stated space of fitness functions and priors:

```text
(abs(X) - 3) / (abs(X) - 1)
```

This spec records the theorem statement and arithmetic fixture checks only. It does not
implement the theorem, reconstruct the theorem's full measure over functions and priors,
or run a finite atlas.

## Critical Separation From Future Atlas Counts

The source theorem probability is not a count of cells in a project-defined finite grid.

Future finite atlas grids may be useful extensions, but their frequencies must be labeled
as grid frequencies under an explicit project measure. They must not be reported as the
source theorem probability without a separate proof or approved reconstruction.

## Approved Stage 4 Policies

`RDR-0004` approves the policy boundary for `ASM-FBT-0001`, `ASM-FBT-0002`,
`ASM-FBT-0003`, and `ASM-FBT-0004`:

- MAP ties are represented as full MAP sets; tie-sensitive outcomes are reported
  separately.
- Zero-marginal observations remain undefined and block dependent comparisons; no
  primary exact path uses smoothing.
- Finite atlas aggregates are `grid_frequency` under frozen project grid versions, not
  source theorem probabilities.
- The primary source-aligned comparison is `truth_map` versus
  `fitness_only_expected`; extension truth-like baselines are reported separately.

These approvals unblock Stage 4 oracle/design implementation. They do not implement or
prove Theorem 4, run a finite atlas, or upgrade any claim to reviewed status.

## Forbidden Interpretations

- Do not claim this spec implements or proves Theorem 4.
- Do not claim a finite grid frequency is the theorem probability.
- Do not claim the theorem covers arbitrary strategy architectures, arbitrary measures,
  or ML agents.
- Do not use the theorem statement to claim that real perception, consciousness,
  spacetime, ontology, or conscious agents have been established.
