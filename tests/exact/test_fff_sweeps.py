from __future__ import annotations

import csv
from io import StringIO

from fts_lab.doctor import find_project_root
from fts_lab.fff.sweeps import (
    build_stage1_sweep_rows,
    load_sweep_config,
    render_sweep_csv,
)


def test_stage1_sweep_rows_include_dual_total_order_counts() -> None:
    config = load_sweep_config(find_project_root() / "experiments/configs/fff_stage1_small.json")
    rows = build_stage1_sweep_rows(config)
    pair_rows = [
        row
        for row in rows
        if row["domain_size"] == "2"
        and row["codomain_size"] == "2"
        and row["structure"] == "total_order"
    ]

    by_object = {row["count_object"]: row for row in pair_rows}
    assert by_object["source_orientation_witnesses"]["numerator"] == "4"
    assert by_object["source_orientation_witnesses"]["row_epistemic_status"] == "R"
    assert by_object["distinct_unique_functions"]["numerator"] == "3"
    assert by_object["distinct_unique_functions"]["row_epistemic_status"] == "C"
    assert by_object["distinct_unique_functions"]["assumption_ids"] == "ASM-FFF-0001"


def test_stage1_sweep_csv_is_deterministic_long_form() -> None:
    config = load_sweep_config(find_project_root() / "experiments/configs/fff_stage1_small.json")
    rows = build_stage1_sweep_rows(config)
    first = render_sweep_csv(rows)
    second = render_sweep_csv(rows)

    assert first == second
    decoded = first.decode("utf-8")
    parsed = list(csv.DictReader(StringIO(decoded)))
    assert len(parsed) == 112
    assert "source_orientation_witnesses" in decoded
    assert "distinct_unique_functions" in decoded
    assert all("." not in row["value_label"] for row in parsed)
