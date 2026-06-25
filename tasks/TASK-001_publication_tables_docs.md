# TASK-001-PUBTABLES - Stage 1 Publication Tables and Result Documentation

```text
TASK ID: TASK-001-PUBTABLES
STAGE: 1 - FFF total orders and cyclic groups
EPISTEMIC STATUS: C for the derived publication table package; per-column status is preserved
OWNER: Codex Implementer
REVIEWER: Fresh-context AI/Codex Verifier for publication package before P1 release
STATUS: ACCEPTED_WITH_MINOR_FINDINGS
```

## 1. Objective

Create publication-oriented tables and documentation from the reviewed `TASK-001-SWEEP` artifact without adding new scientific claims.

The output must be derived from a validated Stage 1 sweep manifest. It must preserve exact values, provenance, checksums, claim IDs, source IDs, and the `R/C` distinction between source reproduction columns and `RDR-0002` presentation companion columns.

## 2. Precondition

`TASK-001-SWEEP` passed independent review:

- `REV-TASK-001-SWEEP-001`
- verdict: `accepted_with_minor_findings`
- unresolved fatal findings: none
- unresolved major findings: none

`TASK-001-PUBTABLES` passed independent review:

- `REV-TASK-001-PUBTABLES-001`
- verdict: `accepted_with_minor_findings`
- unresolved fatal findings: none
- unresolved major findings: none
- source sweep `task_ids` lineage validation fix committed in `446eb187775ad2c5f327d06c0efcaf5b1201ef19`
- remaining minor finding: bare `uv` is not on the local PowerShell `PATH`; use the documented `py -m uv ...` fallback on that machine

## 3. Primary Source

`SRC-FFF-2020`:

- Section 4;
- Appendix A.2, Total Orders Theorem;
- Appendix A.4, Cyclic Groups Theorem.

No new source definitions are introduced by this task.

## 4. Linked Claims

- `CLM-FFF-ADM-001`
- `CLM-FFF-ORD-001`
- `CLM-FFF-CYC-001`
- `CLM-FFF-CYC-002`

## 5. Linked Assumptions and Decisions

- `ASM-FFF-0001`
- `RDR-0002`

The publication table must show both total-order count objects:

- source orientation-witness count;
- distinct unique-function count.

## 6. Expected Output

Implement:

- CLI command `fts fff publication-tables --sweep-manifest PATH`;
- derived wide CSV under `results/derived/<run_id>/stage1_fff_publication_counts.csv`;
- human-readable Markdown report under `results/reports/<run_id>/stage1_fff_publication_tables.md`;
- manifest under `experiments/manifests/<manifest_id>.json`;
- docs explaining how to reproduce the publication table package.

The generated report may contain formatted result tables, but committed documentation must not hard-code unreproducible scientific result tables outside the manifest-backed pipeline.

## 7. Derived CSV Contract

The derived CSV is wide-form and publication-oriented. Each row records one `(n,m)` pair and includes:

- task ID;
- source sweep run and manifest IDs;
- exact admissible count;
- exact total-order source orientation-witness count and ratio;
- exact total-order distinct unique-function count and ratio;
- exact cyclic source homomorphism count and ratio;
- per-column epistemic statuses;
- claim, source, and assumption IDs;
- notes warning that the finite grid is not a biological probability distribution.

Do not use floating-point decimal values in the canonical derived CSV.

## 8. Manifest Contract

The publication table manifest uses:

```json
{
  "artifact_kind": "fff_stage1_publication_tables",
  "epistemic_status": "C",
  "task_ids": ["TASK-001-PUBTABLES"],
  "claim_ids": [
    "CLM-FFF-ADM-001",
    "CLM-FFF-ORD-001",
    "CLM-FFF-CYC-001",
    "CLM-FFF-CYC-002"
  ],
  "source_ids": ["SRC-FFF-2020"],
  "assumption_ids": ["ASM-FFF-0001"]
}
```

Inputs must include the source sweep manifest and sweep CSV. Outputs must include the derived CSV and Markdown report.

## 9. Claims Allowed

- The derived table formats the reviewed Stage 1 finite-count sweep for publication use.
- Values are exact integers or exact rational ratios.
- The table preserves source reproduction columns separately from the `RDR-0002` presentation companion columns.

## 10. Claims Forbidden

- Do not claim any result about human perception, consciousness, spacetime, or ontology.
- Do not claim that the finite grid is an empirical or biological probability distribution.
- Do not claim that source total-order orientation-witness counts are distinct unique-function counts.
- Do not add permutation groups, measurable spaces, FBT, evolution, ML/RL, plots, web demo, or notebooks.

## 11. Acceptance Criteria

1. `fts fff publication-tables --sweep-manifest PATH` reads a valid `TASK-001-SWEEP` manifest and writes derived CSV, report, and valid manifest.
2. The derived CSV contains one row per declared `(n,m)` pair for the default `4 x 4` grid.
3. The derived CSV contains no floating-point decimal values.
4. The generated report includes provenance, status legend, allowed claims, and forbidden claims.
5. The derived manifest validates and checksum validation fails if an output is mutated.
6. Existing Stage 0 and Stage 1 tests remain green.
