from __future__ import annotations

import csv
import json
from io import StringIO
from pathlib import Path

import pytest

from fts_lab.doctor import find_project_root
from fts_lab.fff.publication_tables import (
    build_publication_summary_rows,
    render_publication_report,
    render_summary_csv,
)
from fts_lab.fff.sweeps import (
    build_stage1_sweep_rows,
    load_sweep_config,
)


def test_publication_summary_preserves_statuses_and_exact_values() -> None:
    config = load_sweep_config(find_project_root() / "experiments/configs/fff_stage1_small.json")
    sweep_rows = build_stage1_sweep_rows(config)
    summary_rows = build_publication_summary_rows(
        sweep_rows,
        {"manifest_id": "ART-TEST", "run_id": "EXP-TEST"},
    )

    assert len(summary_rows) == 16
    pair = next(
        row for row in summary_rows if row["domain_size"] == "2" and row["codomain_size"] == "2"
    )
    assert pair["admissible_count"] == "3"
    assert pair["admissible_status"] == "R"
    assert pair["total_order_source_orientation_witness_count"] == "4"
    assert pair["total_order_source_orientation_witness_ratio"] == "4/3"
    assert pair["total_order_source_orientation_witness_status"] == "R"
    assert pair["total_order_distinct_unique_function_count"] == "3"
    assert pair["total_order_distinct_unique_function_ratio"] == "1"
    assert pair["total_order_distinct_unique_function_status"] == "C"
    assert pair["cyclic_source_homomorphism_count"] == "2"
    assert pair["cyclic_source_homomorphism_ratio"] == "2/3"
    assert pair["cyclic_source_homomorphism_status"] == "R"
    assert pair["assumption_ids"] == "ASM-FFF-0001"


def test_publication_summary_csv_is_deterministic_and_non_float() -> None:
    config = load_sweep_config(find_project_root() / "experiments/configs/fff_stage1_small.json")
    sweep_rows = build_stage1_sweep_rows(config)
    summary_rows = build_publication_summary_rows(
        sweep_rows,
        {"manifest_id": "ART-TEST", "run_id": "EXP-TEST"},
    )
    first = render_summary_csv(summary_rows)
    second = render_summary_csv(summary_rows)

    assert first == second
    decoded = first.decode("utf-8")
    parsed = list(csv.DictReader(StringIO(decoded)))
    assert len(parsed) == 16
    value_columns = [
        key
        for key in parsed[0]
        if key.endswith("_count") or key.endswith("_ratio") or key == "admissible_count"
    ]
    assert all("." not in row[column] for row in parsed for column in value_columns)


def test_publication_report_includes_provenance_and_boundaries() -> None:
    config = load_sweep_config(find_project_root() / "experiments/configs/fff_stage1_small.json")
    summary_rows = build_publication_summary_rows(
        build_stage1_sweep_rows(config),
        {"manifest_id": "ART-TEST", "run_id": "EXP-TEST"},
    )

    report = render_publication_report(
        summary_rows,
        sweep_manifest={"manifest_id": "ART-TEST", "run_id": "EXP-TEST"},
        sweep_manifest_path=find_project_root() / "experiments/manifests/example.json",
        sweep_csv_path=find_project_root() / "results/raw/example/fff_stage1_counts.csv",
    )

    assert "TASK-001-PUBTABLES" in report
    assert "SOURCE SWEEP MANIFEST: ART-TEST" in report
    assert "unique order functions (C)" in report
    assert "Forbidden Claims" in report
    assert "human perception" in report


def test_publication_summary_rejects_unexpected_count_objects() -> None:
    config = load_sweep_config(find_project_root() / "experiments/configs/fff_stage1_small.json")
    rows = build_stage1_sweep_rows(config)
    rows[0] = {**rows[0], "count_object": "unexpected"}

    with pytest.raises(ValueError, match="Unexpected count_object"):
        build_publication_summary_rows(rows, {"manifest_id": "ART-TEST", "run_id": "EXP-TEST"})


def test_sweep_config_requires_exact_traceability_ids(tmp_path: Path) -> None:
    root = find_project_root()
    source = root / "experiments/configs/fff_stage1_small.json"
    data = json.loads(source.read_text(encoding="utf-8"))
    data["claim_ids"] = ["CLM-FFF-ADM-001"]
    config_path = tmp_path / "bad_sweep_config.json"
    config_path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="claim_ids must be exactly"):
        load_sweep_config(config_path)
