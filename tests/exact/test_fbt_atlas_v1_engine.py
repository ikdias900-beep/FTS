from __future__ import annotations

from collections import Counter
from pathlib import Path

from fts_lab.doctor import find_project_root
from fts_lab.fbt.atlas_oracle import (
    STATUS_BLOCKED_ZERO_MARGINAL,
    STATUS_MAP_TIE_POLICY_SENSITIVE,
    STATUS_SAME_BEST_OBSERVATION,
)
from fts_lab.fbt.atlas_v1 import (
    build_raw_cell_table,
    build_raw_cells,
    enumerate_axis_cells,
    load_atlas_v1_config,
)

CONFIG_PATH = Path("experiments/configs/fbt_atlas_v1_draft.json")


def test_atlas_v1_config_loads_engine_contract() -> None:
    config = _load_config()

    assert config.grid_version == "fbt_atlas_v1_draft"
    assert config.task_ids == (
        "TASK-004-FBT-ATLAS-V1-SPEC",
        "TASK-004-FBT-ATLAS-V1-ENGINE",
    )
    assert config.claim_ids == ("CLM-FBT-ATLAS-001",)
    assert config.source_ids == ("SRC-FBT-2021",)
    assert config.assumption_ids == (
        "ASM-FBT-0001",
        "ASM-FBT-0002",
        "ASM-FBT-0003",
        "ASM-FBT-0004",
    )
    assert config.phase == "raw_cell_engine"
    assert config.runner_command == "fts fbt atlas-v1-raw-cells"
    assert config.full_grid_run is False
    assert config.theorem_probability_claim is False


def test_atlas_v1_axis_enumeration_is_deterministic() -> None:
    axes = enumerate_axis_cells(_load_config())

    assert len(axes) == 144
    assert axes[0].world_state_count == 2
    assert axes[0].perceptual_state_count == 2
    assert axes[0].prior_family_id == "uniform"
    assert axes[0].kernel_family_id == "pure_map"
    assert axes[0].fitness_family_id == "single_peak"
    assert axes[-1].world_state_count == 3
    assert axes[-1].perceptual_state_count == 3
    assert axes[-1].prior_family_id == "rational_simplex_small"
    assert axes[-1].kernel_family_id == "zero_marginal_probe"
    assert axes[-1].fitness_family_id == "multi_peak"


def test_atlas_v1_raw_cells_have_stable_identity_and_exact_inputs() -> None:
    cells = build_raw_cells(_load_config())

    assert len(cells) == 144
    assert (
        cells[0].cell_id == "fbt_atlas_v1_draft__w2__x2__prior-uniform__kernel-pure_map"
        "__fitness-single_peak__offered-all_observations"
        "__cmp-truth_map_vs_fitness_only_expected__edge-rdr0004_stage4_edge_policies"
    )
    assert (
        cells[-1].cell_id == "fbt_atlas_v1_draft__w3__x3__prior-rational_simplex_small"
        "__kernel-zero_marginal_probe__fitness-multi_peak__offered-all_observations"
        "__cmp-truth_map_vs_fitness_only_expected__edge-rdr0004_stage4_edge_policies"
    )
    assert cells[0].prior["w1"].numerator == 1
    assert cells[0].prior["w1"].denominator == 2
    assert cells[0].kernel["w1"]["x1"] == 1
    assert cells[0].kernel["w1"]["x2"] == 0
    assert cells[0].fitness["w1"] == 10
    assert cells[0].fitness["w2"] == 0


def test_atlas_v1_raw_cell_table_preserves_raw_scope_and_statuses() -> None:
    table = build_raw_cell_table(_load_config())

    assert table["artifact_kind"] == "fbt_atlas_v1_raw_cell_table"
    assert table["epistemic_status"] == "E"
    assert table["raw_cell_count"] == 144
    assert table["engine_scope"] == {
        "result_level": "raw_cells_only",
        "aggregate_report": False,
        "full_grid_run": False,
        "runner_command": "fts fbt atlas-v1-raw-cells",
    }
    assert "summary" not in table
    assert "grid_frequencies_by_status" not in table

    cells = table["cells"]
    assert isinstance(cells, list)
    status_counts = Counter(cell["status"] for cell in cells)
    assert status_counts[STATUS_BLOCKED_ZERO_MARGINAL] == 45
    assert status_counts[STATUS_MAP_TIE_POLICY_SENSITIVE] > 0
    assert status_counts[STATUS_SAME_BEST_OBSERVATION] > 0


def test_atlas_v1_raw_cell_records_zero_marginal_as_blocked_without_smoothing() -> None:
    table = build_raw_cell_table(_load_config())
    cells = table["cells"]
    assert isinstance(cells, list)
    blocked_cell = next(
        cell
        for cell in cells
        if cell["axis"]["kernel_family_id"] == "zero_marginal_probe"
        and cell["axis"]["perceptual_state_count"] == 3
    )

    assert blocked_cell["status"] == STATUS_BLOCKED_ZERO_MARGINAL
    observation_results = blocked_cell["observation_results"]
    assert observation_results[-1]["observation"] == "x3"
    assert observation_results[-1]["status"] == "zero_marginal_undefined"
    assert observation_results[-1]["marginal"]["label"] == "0"
    assert observation_results[-1]["posterior"] == {}


def _load_config():
    return load_atlas_v1_config(find_project_root() / CONFIG_PATH)
