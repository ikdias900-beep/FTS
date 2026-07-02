from __future__ import annotations

from fractions import Fraction
from pathlib import Path

import pytest

from fts_lab.doctor import find_project_root
from fts_lab.fbt.atlas_oracle import (
    STATUS_BLOCKED_ZERO_MARGINAL,
    STATUS_MAP_TIE_POLICY_SENSITIVE,
    STATUS_SAME_BEST_OBSERVATION,
)
from fts_lab.fbt.atlas_v1 import build_raw_cell_table, load_atlas_v1_config
from fts_lab.fbt.atlas_v1_aggregate import (
    build_aggregate_report,
    render_aggregate_markdown,
)

CONFIG_PATH = Path("experiments/configs/fbt_atlas_v1_draft.json")
AGGREGATE_MODULE_PATH = Path("src/fts_lab/fbt/atlas_v1_aggregate.py")


def test_atlas_v1_aggregate_counts_statuses_from_raw_cells_only() -> None:
    raw_table = _raw_table()
    aggregate = build_aggregate_report(raw_table)

    assert aggregate["artifact_kind"] == "fbt_atlas_v1_aggregate_report"
    assert aggregate["epistemic_status"] == "E"
    assert aggregate["task_ids"] == [
        "TASK-004-FBT-ATLAS-V1-SPEC",
        "TASK-004-FBT-ATLAS-V1-ENGINE",
        "TASK-004-FBT-ATLAS-V1-AGGREGATE",
    ]
    assert aggregate["claim_ids"] == ["CLM-FBT-ATLAS-001"]
    assert aggregate["source_ids"] == ["SRC-FBT-2021"]
    assert aggregate["assumption_ids"] == [
        "ASM-FBT-0001",
        "ASM-FBT-0002",
        "ASM-FBT-0003",
        "ASM-FBT-0004",
    ]
    assert "cells" not in aggregate

    scope = aggregate["aggregate_scope"]
    assert scope["source"] == "raw_cell_artifact_only"
    assert scope["recomputes_cells"] is False
    assert scope["reads_config"] is False
    assert scope["aggregate_label"] == "grid_frequency"
    assert scope["denominator_policy"] == "all_enumerated_cells"
    assert scope["denominator_basis"] == "all_raw_cells"
    assert scope["blocked_cells_in_denominator"] is True
    assert scope["tie_sensitive_cells_in_denominator"] is True
    assert scope["full_grid_run"] is False


def test_atlas_v1_aggregate_status_counts_and_grid_frequencies_are_exact() -> None:
    aggregate = build_aggregate_report(_raw_table())
    summary = aggregate["summary"]
    status_counts = summary["status_counts"]
    frequencies = summary["grid_frequencies_by_status"]

    assert summary["total_raw_cells"] == 144
    assert sum(status_counts.values()) == 144
    assert status_counts[STATUS_BLOCKED_ZERO_MARGINAL] == 45
    assert status_counts[STATUS_MAP_TIE_POLICY_SENSITIVE] > 0
    assert status_counts[STATUS_SAME_BEST_OBSERVATION] > 0

    blocked_frequency = frequencies[STATUS_BLOCKED_ZERO_MARGINAL]
    assert blocked_frequency == {
        "numerator": 5,
        "denominator": 16,
        "label": "5/16",
    }
    total_frequency = sum(
        Fraction(item["numerator"], item["denominator"]) for item in frequencies.values()
    )
    assert total_frequency == 1


def test_atlas_v1_aggregate_rejects_raw_count_mismatch() -> None:
    raw_table = dict(_raw_table())
    raw_table["raw_cell_count"] = 999

    with pytest.raises(ValueError, match="raw_cell_count must match"):
        build_aggregate_report(raw_table)


def test_atlas_v1_report_renders_raw_artifact_boundary() -> None:
    aggregate = build_aggregate_report(
        _raw_table(),
        raw_cells_path=Path("results/raw/example/fbt_atlas_v1_raw_cells.json"),
        raw_cell_table_sha256="0" * 64,
    )
    report = render_aggregate_markdown(aggregate)

    assert "fbt_atlas_v1_raw_cell_table" in report
    assert "RECOMPUTES CELLS: false" in report
    assert "Total raw cells: `144`." in report
    assert "`blocked_zero_marginal` | 45 | 5/16" in report
    assert "does not read the draft config" in report
    assert "full atlas run" in report
    assert "biological or metaphysical result" in report


def test_atlas_v1_aggregate_module_does_not_import_raw_engine() -> None:
    source = (find_project_root() / AGGREGATE_MODULE_PATH).read_text(encoding="utf-8")

    assert "from fts_lab.fbt.atlas_v1 import" not in source
    assert "build_raw_cells" not in source
    assert "build_raw_cell_table" not in source
    assert "load_atlas_v1_config" not in source


def _raw_table():
    return build_raw_cell_table(load_atlas_v1_config(find_project_root() / CONFIG_PATH))
