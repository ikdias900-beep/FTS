from __future__ import annotations

from pathlib import Path

from fts_lab.doctor import find_project_root
from fts_lab.fbt.atlas_grid import (
    build_grid_result,
    enumerate_grid_cells,
    load_atlas_grid_config,
    render_grid_report,
)
from fts_lab.fbt.atlas_oracle import (
    STATUS_BLOCKED_ZERO_MARGINAL,
    STATUS_MAP_TIE_POLICY_SENSITIVE,
)

CONFIG_PATH = Path("experiments/configs/fbt_atlas_v0.json")


def test_atlas_grid_v0_config_links_required_traceability_ids() -> None:
    config = _load_config()

    assert config.grid_version == "fbt_atlas_v0"
    assert config.epistemic_status == "E"
    assert config.task_ids == ("TASK-004-FBT-ATLAS-GRID-V0",)
    assert config.claim_ids == ("CLM-FBT-ATLAS-001",)
    assert config.source_ids == ("SRC-FBT-2021",)
    assert config.assumption_ids == (
        "ASM-FBT-0001",
        "ASM-FBT-0002",
        "ASM-FBT-0003",
        "ASM-FBT-0004",
    )
    assert config.aggregate_label == "grid_frequency"
    assert config.denominator_policy == "all_enumerated_cells"
    assert config.theorem_probability_claim is False


def test_atlas_grid_v0_cell_enumeration_is_deterministic() -> None:
    cells = enumerate_grid_cells(_load_config())

    assert len(cells) == 24
    assert (
        cells[0].cell_id
        == "fbt_atlas_v0__prior-uniform__kernel-identity__fitness-w1_high__offered-x1-x2"
    )
    assert (
        cells[-1].cell_id
        == "fbt_atlas_v0__prior-w1_heavy__kernel-zero_x2__fitness-equal__offered-x1-x2"
    )


def test_atlas_grid_v0_result_preserves_denominator_accounting() -> None:
    result = build_grid_result(_load_config())
    summary = result["summary"]
    assert isinstance(summary, dict)
    status_counts = summary["status_counts"]
    assert isinstance(status_counts, dict)

    assert summary["total_cells"] == 24
    assert sum(status_counts.values()) == 24
    assert status_counts[STATUS_BLOCKED_ZERO_MARGINAL] == 6
    assert status_counts[STATUS_MAP_TIE_POLICY_SENSITIVE] >= 1

    frequencies = summary["grid_frequencies_by_status"]
    assert isinstance(frequencies, dict)
    blocked_frequency = frequencies[STATUS_BLOCKED_ZERO_MARGINAL]
    assert isinstance(blocked_frequency, dict)
    assert blocked_frequency["label"] == "1/4"


def test_atlas_grid_v0_result_language_forbids_theorem_probability_claim() -> None:
    result = build_grid_result(_load_config())

    semantics = result["grid_semantics"]
    assert isinstance(semantics, dict)
    assert semantics["aggregate_label"] == "grid_frequency"
    assert semantics["theorem_probability_claim"] is False

    report = render_grid_report(result)
    assert "grid_frequency" in report
    assert "THEOREM PROBABILITY CLAIM: false" in report
    assert "not a source theorem probability calculation" in report


def _load_config():
    return load_atlas_grid_config(find_project_root() / CONFIG_PATH)
