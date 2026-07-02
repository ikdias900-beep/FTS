# Manifests

This directory contains archived copies of the original manifest records:

- `ART-TASK-004-FBT-ATLAS-V1-RAW-CELLS-MANIFEST-20260702T080919Z-0AE3BB9C.json`
- `ART-TASK-004-FBT-ATLAS-V1-AGGREGATE-MANIFEST-20260702T080924Z-1A6A67BF.json`

The raw-cell manifest records:

- input: `experiments/configs/fbt_atlas_v1_draft.json`;
- output: `results/raw/.../fbt_atlas_v1_raw_cells.json`;
- `artifact_kind=fbt_atlas_v1_raw_cell_table`.

The aggregate manifest records:

- input: the raw-cell JSON artifact;
- outputs: aggregate JSON and Markdown report;
- `artifact_kind=fbt_atlas_v1_aggregate_report`.

The manifests retain original absolute paths. The capsule-local archived copies are
covered by `release/stage4-v1-draft/checksums.txt`.
