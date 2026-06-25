# TASK-001-SWEEP - Stage 1 Finite Count Sweeps and Tables

```text
TASK ID: TASK-001-SWEEP
STAGE: 1 - FFF total orders and cyclic groups
EPISTEMIC STATUS: C for the sweep artifact; per-row status is preserved in CSV
OWNER: Codex Implementer
REVIEWER: Fresh-context AI/Codex Verifier
STATUS: ACCEPTED_WITH_MINOR_FINDINGS
```

## 1. Objective

Create a manifest-backed finite-size sweep for Stage 1 exact counts. The sweep writes a deterministic long-form CSV table for declared small `n, m` grids and a reproducibility manifest with checksums.

This task prepares P1 tables. It does not create plots, web demos, notebooks, or new mathematical definitions.

## 2. Primary Source

`SRC-FFF-2020`:

- Section 4;
- Appendix A.2, Total Orders Theorem;
- Appendix A.4, Cyclic Groups Theorem.

## 3. Linked Claims

- `CLM-FFF-ADM-001`
- `CLM-FFF-ORD-001`
- `CLM-FFF-CYC-001`
- `CLM-FFF-CYC-002`

## 4. Linked Assumptions and Decisions

- `ASM-FFF-0001`
- `RDR-0002`

The output table must show both total-order count objects:

- source orientation-witness count;
- distinct unique-function count.

## 5. Expected Output

Implement:

- `experiments/configs/fff_stage1_small.json`;
- `src/fts_lab/fff/sweeps.py`;
- CLI command `fts fff sweep --config PATH`;
- tests for deterministic CSV rows and manifest validation.

The sweep writes:

- raw CSV under `results/raw/<run_id>/fff_stage1_counts.csv`;
- manifest under `experiments/manifests/<manifest_id>.json`.

## 6. CSV Contract

The CSV is long-form. Each row records:

- `schema_version`;
- `task_id`;
- `row_epistemic_status`;
- `claim_id`;
- `source_id`;
- `assumption_ids`;
- `structure`;
- `metric`;
- `count_object`;
- `domain_size`;
- `codomain_size`;
- `numerator`;
- `denominator`;
- `value_label`;
- `notes`.

Do not use floating-point decimal values in the canonical CSV.

## 7. Manifest Contract

The sweep manifest uses:

```json
{
  "artifact_kind": "fff_stage1_finite_count_sweep",
  "epistemic_status": "C",
  "task_ids": ["TASK-001-SWEEP"],
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

The artifact-level status is `C` because the table includes the approved dual-count presentation for total orders. Each row also preserves its own `row_epistemic_status`.

## 8. Out Of Scope

- plots;
- web demo;
- notebooks;
- permutation groups;
- measurable spaces;
- FBT;
- stochastic simulation;
- new assumptions.

## 9. Acceptance Criteria

1. `fts fff sweep --config experiments/configs/fff_stage1_small.json` writes CSV and valid manifest.
2. CSV includes both total-order count objects for every declared `n,m`.
3. CSV contains no floats.
4. Manifest validates and checksum validation fails if the CSV is mutated.
5. Existing Stage 0 and Stage 1 tests remain green.

## 10. Review Outcome

`REV-TASK-001-SWEEP-001` reported `accepted_with_minor_findings` with no unresolved fatal or major findings. The task is not blocked.
