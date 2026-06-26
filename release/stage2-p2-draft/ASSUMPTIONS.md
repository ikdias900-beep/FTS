# Assumptions And Decisions

## Scientific Assumptions Used

None.

An empty assumption list means the result uses no project-added scientific assumptions
beyond explicit source definitions and table values.

## Open Assumptions Not Invoked

### ASM-FBT-0001

General MAP tie handling remains `OPEN`. The source numerical appendix has unique MAP
estimates for both observations, so no tie rule is needed for this reproduction.

The reusable helper raises an explicit ambiguity error when a tie occurs.

### ASM-FBT-0002

General zero-probability observation behavior remains `OPEN`. The source numerical
appendix has nonzero marginals for both observations, so no zero-marginal policy is
needed for this reproduction.

The reusable helper raises an explicit normalization error when a zero marginal occurs.

## Research Decisions

### RDR-0001-license

Project-authored repository contents use the MIT License. External primary-source
papers, publisher content, third-party packages, and other non-project-authored
materials are not relicensed.

## New Assumptions Introduced

None.
