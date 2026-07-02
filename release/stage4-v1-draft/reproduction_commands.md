# Reproduction Commands

Run from the repository root.

## Generate Raw-Cell Artifact

```powershell
.\.venv\Scripts\python.exe -m fts_lab.cli fbt atlas-v1-raw-cells
```

Packaged run output:

```text
raw_cell_table_checksum=582e7e50fd8b1bfab149feab6e00d80cd95bda29268ff6fec99e0a5ed4748613
raw_cell_table_path=results/raw/EXP-TASK-004-FBT-ATLAS-V1-RAW-CELLS-20260702T080919Z-0AE3BB9C/fbt_atlas_v1_raw_cells.json
manifest_path=experiments/manifests/ART-TASK-004-FBT-ATLAS-V1-RAW-CELLS-MANIFEST-20260702T080919Z-0AE3BB9C.json
cell_count=144
```

## Generate Aggregate From Raw-Cell Artifact

```powershell
.\.venv\Scripts\python.exe -m fts_lab.cli fbt atlas-v1-aggregate --raw-cells "results\raw\EXP-TASK-004-FBT-ATLAS-V1-RAW-CELLS-20260702T080919Z-0AE3BB9C\fbt_atlas_v1_raw_cells.json"
```

Packaged run output:

```text
json_report_checksum=2512ab5833a2da993b31af21b1db4c529837eeb5930f7d2764de201860767328
json_report_path=results/derived/EXP-TASK-004-FBT-ATLAS-V1-AGGREGATE-20260702T080924Z-1A6A67BF/fbt_atlas_v1_aggregate.json
markdown_report_checksum=786e48e0495822828d128580fe87199a253fdff71ad7939d2b0049a0796848a6
markdown_report_path=results/reports/EXP-TASK-004-FBT-ATLAS-V1-AGGREGATE-20260702T080924Z-1A6A67BF/fbt_atlas_v1_report.md
manifest_path=experiments/manifests/ART-TASK-004-FBT-ATLAS-V1-AGGREGATE-MANIFEST-20260702T080924Z-1A6A67BF.json
cell_count=144
```

## Validate Manifests

```powershell
.\.venv\Scripts\python.exe -m fts_lab.cli validate-manifest "release\stage4-v1-draft\manifests\ART-TASK-004-FBT-ATLAS-V1-RAW-CELLS-MANIFEST-20260702T080919Z-0AE3BB9C.json"
.\.venv\Scripts\python.exe -m fts_lab.cli validate-manifest "release\stage4-v1-draft\manifests\ART-TASK-004-FBT-ATLAS-V1-AGGREGATE-MANIFEST-20260702T080924Z-1A6A67BF.json"
```

## Validate Capsule

```powershell
.\.venv\Scripts\python.exe -m fts_lab.cli validate-release-capsule release/stage4-v1-draft
```

## Full Quality Gate

```powershell
git diff --check
.\.venv\Scripts\python.exe -m fts_lab.cli doctor --release-check
.\.venv\Scripts\python.exe -m pytest -p no:cacheprovider
.\.venv\Scripts\python.exe -m ruff check . --no-cache
.\.venv\Scripts\python.exe -m ruff format --check . --no-cache
.\.venv\Scripts\python.exe -m mypy src
```
