# TASK-001-P1-CAPSULE - Stage 1 Draft Release Capsule

```text
TASK ID: TASK-001-P1-CAPSULE
STAGE: 1 - FFF total orders and cyclic groups
EPISTEMIC STATUS: C for release packaging; no new scientific claims
OWNER: Codex Implementer
REVIEWER: Fresh-context AI/Codex Verifier before publication
STATUS: READY_FOR_REVIEW
```

## 1. Objective

Assemble a draft P1 release capsule from the reviewed Stage 1 core, sweep, and publication-table artifacts.

This task packages already reviewed outputs. It does not change mathematical definitions, add figures, create a browser demo, or expand the allowed scientific claims.

## 2. Preconditions

- `TASK-001` exact core passed independent review with no fatal or major findings.
- `TASK-001-SWEEP` passed independent review with verdict `accepted_with_minor_findings`.
- `TASK-001-PUBTABLES` passed independent review with verdict `accepted_with_minor_findings`.
- `RDR-0001-license` is approved as MIT for project-authored repository contents.

## 3. Linked Sources, Claims, Assumptions, and Decisions

- Source IDs: `SRC-FFF-2020`
- Claim IDs: `CLM-FFF-ADM-001`, `CLM-FFF-ORD-001`, `CLM-FFF-CYC-001`, `CLM-FFF-CYC-002`
- Assumption IDs: `ASM-FFF-0001`
- Decisions: `RDR-0001-license`, `RDR-0002`

## 4. Expected Output

Create `release/stage1-p1-draft/` with:

- `README.md`
- `CLAIMS.md`
- `LIMITATIONS.md`
- `ASSUMPTIONS.md`
- `REVIEW_REPORT.md`
- `environment/`
- `manifests/`
- `raw_data/`
- `derived_data/`
- `figures/`
- `reproduction_commands.md`
- `checksums.txt`

The capsule must include the generated Stage 1 sweep manifest, publication-table manifest, raw sweep CSV, derived publication CSV, and generated Markdown report.

## 5. Claims Allowed

- The capsule archives reviewed Stage 1 finite-count artifacts for total orders and cyclic groups.
- Included numeric artifacts are manifest-backed and checksum-recorded.
- The release package preserves source reproduction columns separately from the `RDR-0002` presentation companion columns.

## 6. Claims Forbidden

- Do not claim a final public release, DOI, or archival deposit has been created.
- Do not claim the finite grid is a biological probability distribution.
- Do not claim results about human perception, consciousness, spacetime, ontology, FBT, evolution, ML/RL, permutation groups, or measurable spaces.
- Do not include a browser demo or figures unless they are generated from manifest-backed data in a later reviewed task.

## 7. Acceptance Criteria

1. `fts doctor --release-check` passes.
2. Included manifests validate against the repository schema.
3. `checksums.txt` records every committed release-capsule file except itself.
4. Release `CLAIMS.md`, `LIMITATIONS.md`, and `REVIEW_REPORT.md` exist and remain within the approved claim boundary.
5. Full tests, lint, format check, and typing pass.
6. No new assumptions are introduced.
