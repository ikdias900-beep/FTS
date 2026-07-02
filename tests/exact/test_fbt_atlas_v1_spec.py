from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fts_lab.doctor import find_project_root

CONFIG_PATH = Path("experiments/configs/fbt_atlas_v1_draft.json")


def test_atlas_v1_draft_config_links_required_traceability_ids() -> None:
    config = _load_config()

    assert config["schema_version"] == "1.0"
    assert config["artifact_kind"] == "fbt_atlas_v1_draft_config"
    assert config["epistemic_status"] == "E"
    assert config["task_ids"] == [
        "TASK-004-FBT-ATLAS-V1-SPEC",
        "TASK-004-FBT-ATLAS-V1-ENGINE",
    ]
    assert config["claim_ids"] == ["CLM-FBT-ATLAS-001"]
    assert config["source_ids"] == ["SRC-FBT-2021"]
    assert config["assumption_ids"] == [
        "ASM-FBT-0001",
        "ASM-FBT-0002",
        "ASM-FBT-0003",
        "ASM-FBT-0004",
    ]


def test_atlas_v1_draft_config_is_raw_cell_engine_only() -> None:
    config = _load_config()
    execution = _object(config, "execution")

    assert config["grid_version"] == "fbt_atlas_v1_draft"
    assert execution["phase"] == "raw_cell_engine"
    assert execution["engine_status"] == "raw_cell_table_implemented_pending_review"
    assert execution["runner_command"] == "fts fbt atlas-v1-raw-cells"
    assert execution["full_grid_run"] is False

    disabled = set(_list(config, "disabled_features"))
    assert {
        "full_atlas_run",
        "stochastic_simulation",
        "ml_rl",
        "ui_dashboard",
        "notebooks",
        "figures",
    } <= disabled


def test_atlas_v1_primary_comparison_excludes_extension_baselines() -> None:
    config = _load_config()
    comparison = _object(config, "primary_comparison")
    baselines = _object(config, "extension_baselines")

    assert comparison["comparison_id"] == "truth_map_vs_fitness_only_expected"
    assert comparison["truth_strategy"] == "truth_map"
    assert comparison["fitness_strategy"] == "fitness_only_expected"
    assert comparison["extension_baselines_in_primary_results"] is False
    assert baselines["enabled"] is False
    assert baselines["activation_requires_new_task"] is True


def test_atlas_v1_grid_identity_contract_is_stable_and_draft() -> None:
    config = _load_config()
    identity = _object(config, "grid_identity")

    assert identity["freeze_status"] == "draft_not_frozen"
    assert identity["cell_id_components"] == [
        "grid_version",
        "world_state_count",
        "perceptual_state_count",
        "prior_family_id",
        "kernel_family_id",
        "fitness_family_id",
        "offered_observation_set_id",
        "primary_comparison_id",
        "edge_policy_id",
    ]

    axes = _object(identity, "draft_axes")
    assert axes["world_state_counts"] == [2, 3]
    assert axes["perceptual_state_counts"] == [2, 3]
    assert "zero_marginal_probe" in axes["kernel_families"]


def test_atlas_v1_denominator_semantics_preserve_blocked_and_tie_sensitive_cells() -> None:
    config = _load_config()
    enumeration = _object(config, "enumeration")
    policies = _object(config, "edge_case_policies")
    reporting = _object(config, "reporting")

    assert policies["edge_policy_id"] == "rdr0004_stage4_edge_policies"
    assert enumeration["arithmetic"] == "exact_rational"
    assert enumeration["randomness"] == "none"
    assert enumeration["stochastic_simulation"] is False
    assert enumeration["raw_cell_artifacts_required_before_aggregates"] is True
    assert enumeration["manifest_required"] is True

    assert policies["map_ties"] == "full_map_sets"
    assert policies["map_tie_sensitive_status"] == "map_tie_policy_sensitive"
    assert policies["zero_marginal"] == "zero_marginal_undefined"
    assert policies["blocked_status"] == "blocked_zero_marginal"

    assert reporting["aggregate_label"] == "grid_frequency"
    assert reporting["denominator_policy"] == "all_enumerated_cells"
    assert reporting["include_blocked_zero_marginal_in_denominator"] is True
    assert reporting["include_map_tie_policy_sensitive_in_denominator"] is True
    assert reporting["theorem_probability_claim"] is False


def test_atlas_v1_family_definitions_are_explicit() -> None:
    config = _load_config()
    definitions = _object(config, "family_definitions")

    priors = _object(definitions, "priors")
    kernels = _object(definitions, "kernels")
    fitness_functions = _object(definitions, "fitness_functions")

    assert tuple(priors) == ("uniform", "single_state_heavy", "rational_simplex_small")
    assert tuple(kernels) == (
        "pure_map",
        "noisy_map",
        "uninformative",
        "zero_marginal_probe",
    )
    assert tuple(fitness_functions) == ("single_peak", "equal", "multi_peak")


def test_atlas_v1_draft_config_contains_no_source_probability_wording() -> None:
    config = _load_config()

    forbidden_fragments = (
        "theorem probability",
        "theorem-probability",
        "source probability",
        "source-probability",
    )
    for value in _walk_strings(config):
        lowered = value.lower()
        for fragment in forbidden_fragments:
            assert fragment not in lowered


def _load_config() -> dict[str, Any]:
    data = json.loads((find_project_root() / CONFIG_PATH).read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def _object(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data[key]
    assert isinstance(value, dict)
    return value


def _list(data: dict[str, Any], key: str) -> list[Any]:
    value = data[key]
    assert isinstance(value, list)
    return value


def _walk_strings(value: Any) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,)
    if isinstance(value, list):
        return tuple(string for item in value for string in _walk_strings(item))
    if isinstance(value, dict):
        return tuple(string for item in value.values() for string in _walk_strings(item))
    return ()
