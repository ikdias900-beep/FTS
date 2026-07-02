"""Manifest-backed Stage 4 FBT atlas v1 raw-cell engine."""

from __future__ import annotations

import platform
import re
import sys
import uuid
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from fractions import Fraction
from itertools import product
from pathlib import Path
from typing import Any, Final, cast

from fts_lab import __version__
from fts_lab.doctor import find_project_root, git_state
from fts_lab.fbt.atlas_oracle import CellOracleResult, evaluate_primary_cell
from fts_lab.fbt.bayes import FiniteBayesianDecisionProblem, WorldStateRow
from fts_lab.manifests import (
    canonical_json_bytes,
    read_json_object,
    sha256_bytes,
    sha256_file,
    validate_manifest_file,
    write_immutable_bytes,
    write_immutable_json,
)

TASK_ID: Final = "TASK-004-FBT-ATLAS-V1-ENGINE"
SPEC_TASK_ID: Final = "TASK-004-FBT-ATLAS-V1-SPEC"
ARTIFACT_KIND: Final = "fbt_atlas_v1_raw_cell_table"
CONFIG_ARTIFACT_KIND: Final = "fbt_atlas_v1_draft_config"
DEFAULT_CONFIG_PATH: Final = Path("experiments/configs/fbt_atlas_v1_draft.json")
RAW_CELL_TABLE_FILENAME: Final = "fbt_atlas_v1_raw_cells.json"
EXPECTED_TASK_IDS: Final = (SPEC_TASK_ID, TASK_ID)
EXPECTED_CLAIM_IDS: Final = ("CLM-FBT-ATLAS-001",)
EXPECTED_SOURCE_IDS: Final = ("SRC-FBT-2021",)
EXPECTED_ASSUMPTION_IDS: Final = (
    "ASM-FBT-0001",
    "ASM-FBT-0002",
    "ASM-FBT-0003",
    "ASM-FBT-0004",
)
EXPECTED_GRID_VERSION: Final = "fbt_atlas_v1_draft"
EXPECTED_COMPARISON_ID: Final = "truth_map_vs_fitness_only_expected"
EXPECTED_EDGE_POLICY_ID: Final = "rdr0004_stage4_edge_policies"
EXPECTED_AGGREGATE_LABEL: Final = "grid_frequency"
EXPECTED_DENOMINATOR_POLICY: Final = "all_enumerated_cells"
EXPECTED_PRIOR_FAMILIES: Final = (
    "uniform",
    "single_state_heavy",
    "rational_simplex_small",
)
EXPECTED_KERNEL_FAMILIES: Final = (
    "pure_map",
    "noisy_map",
    "uninformative",
    "zero_marginal_probe",
)
EXPECTED_FITNESS_FAMILIES: Final = ("single_peak", "equal", "multi_peak")
EXPECTED_OFFERED_SETS: Final = ("all_observations",)
ID_PATTERN: Final = re.compile(r"^[A-Za-z0-9_-]+$")

type JsonObject = dict[str, Any]


@dataclass(frozen=True)
class AtlasV1Config:
    """Validated atlas v1 draft config used by the raw-cell engine."""

    path: Path
    artifact_kind: str
    epistemic_status: str
    task_ids: tuple[str, ...]
    claim_ids: tuple[str, ...]
    source_ids: tuple[str, ...]
    assumption_ids: tuple[str, ...]
    grid_version: str
    phase: str
    engine_status: str
    runner_command: str
    full_grid_run: bool
    primary_comparison_id: str
    truth_strategy: str
    fitness_strategy: str
    extension_baselines_in_primary_results: bool
    edge_policy_id: str
    world_state_counts: tuple[int, ...]
    perceptual_state_counts: tuple[int, ...]
    prior_families: tuple[str, ...]
    kernel_families: tuple[str, ...]
    fitness_families: tuple[str, ...]
    offered_observation_sets: tuple[str, ...]
    aggregate_label: str
    denominator_policy: str
    theorem_probability_claim: bool
    notes: str


@dataclass(frozen=True)
class AtlasV1AxisCell:
    """One deterministic atlas v1 axis combination."""

    world_state_count: int
    perceptual_state_count: int
    prior_family_id: str
    kernel_family_id: str
    fitness_family_id: str
    offered_observation_set_id: str
    primary_comparison_id: str
    edge_policy_id: str


@dataclass(frozen=True)
class AtlasV1RawCell:
    """One exact finite raw cell generated from the atlas v1 draft config."""

    cell_id: str
    axis: AtlasV1AxisCell
    observations: tuple[str, ...]
    world_states: tuple[str, ...]
    prior: Mapping[str, Fraction]
    kernel: Mapping[str, Mapping[str, Fraction]]
    fitness: Mapping[str, Fraction]
    offered_observations: tuple[str, ...]
    problem: FiniteBayesianDecisionProblem


def run_fbt_atlas_v1_raw_cells(
    config_path: Path | None = None, *, command: str | None = None
) -> dict[str, str]:
    """Run the exact atlas v1 raw-cell engine and write a manifest-backed table."""
    root = find_project_root()
    config_file = (config_path or root / DEFAULT_CONFIG_PATH).resolve()
    config = load_atlas_v1_config(config_file)
    result = build_raw_cell_table(config)
    raw_bytes = canonical_json_bytes(result)

    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    suffix = uuid.uuid4().hex[:8].upper()
    run_id = f"EXP-TASK-004-FBT-ATLAS-V1-RAW-CELLS-{timestamp}-{suffix}"
    manifest_id = f"ART-TASK-004-FBT-ATLAS-V1-RAW-CELLS-MANIFEST-{timestamp}-{suffix}"
    raw_dir = root / "results/raw" / run_id
    raw_table_path = raw_dir / RAW_CELL_TABLE_FILENAME
    manifest_path = root / "experiments/manifests" / f"{manifest_id}.json"

    write_immutable_bytes(raw_table_path, raw_bytes)

    lockfile = root / "uv.lock"
    if not lockfile.is_file():
        raise FileNotFoundError("uv.lock is required before writing an atlas v1 manifest")

    raw_checksum = sha256_bytes(raw_bytes)
    raw_cell_count = result["raw_cell_count"]
    if not isinstance(raw_cell_count, int):
        raise ValueError("raw_cell_count must be an integer")

    manifest: dict[str, Any] = {
        "schema_version": "1.0",
        "manifest_id": manifest_id,
        "run_id": run_id,
        "artifact_kind": ARTIFACT_KIND,
        "epistemic_status": "E",
        "task_ids": list(config.task_ids),
        "claim_ids": list(config.claim_ids),
        "source_ids": list(config.source_ids),
        "assumption_ids": list(config.assumption_ids),
        "created_at_utc": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "command": command or " ".join(sys.argv),
        "parameters": {
            "config_path": str(config_file),
            "grid_version": config.grid_version,
            "result_level": "raw_cells_only",
            "primary_comparison_id": config.primary_comparison_id,
            "edge_policy_id": config.edge_policy_id,
            "raw_cell_count": raw_cell_count,
            "raw_cell_table_filename": RAW_CELL_TABLE_FILENAME,
            "aggregate_report": False,
        },
        "seed": None,
        "git": git_state(root),
        "environment": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "dependency_lock_sha256": sha256_file(lockfile),
        },
        "inputs": [{"path": str(config_file), "sha256": sha256_file(config_file)}],
        "outputs": [{"path": str(raw_table_path), "sha256": raw_checksum}],
        "status": "completed",
        "error": None,
        "implementation": {"package": "fts-lab", "version": __version__},
    }
    write_immutable_json(manifest_path, manifest)
    validate_manifest_file(manifest_path, project_root=root)

    return {
        "raw_cell_table_checksum": raw_checksum,
        "raw_cell_table_path": str(raw_table_path),
        "manifest_path": str(manifest_path),
        "run_id": run_id,
        "cell_count": str(raw_cell_count),
    }


def load_atlas_v1_config(path: Path) -> AtlasV1Config:
    """Load and validate the atlas v1 draft config for raw-cell execution."""
    data = read_json_object(path)
    if _string_value(data, "schema_version") != "1.0":
        raise ValueError("schema_version must be '1.0'")
    artifact_kind = _string_value(data, "artifact_kind")
    if artifact_kind != CONFIG_ARTIFACT_KIND:
        raise ValueError(f"artifact_kind must be {CONFIG_ARTIFACT_KIND!r}")
    epistemic_status = _string_value(data, "epistemic_status")
    if epistemic_status != "E":
        raise ValueError("atlas v1 config must use epistemic_status 'E'")

    task_ids = _string_tuple(data, "task_ids", min_items=1)
    claim_ids = _string_tuple(data, "claim_ids", min_items=1)
    source_ids = _string_tuple(data, "source_ids", min_items=1)
    assumption_ids = _string_tuple(data, "assumption_ids", min_items=1)
    _require_exact_tuple("task_ids", task_ids, EXPECTED_TASK_IDS)
    _require_exact_tuple("claim_ids", claim_ids, EXPECTED_CLAIM_IDS)
    _require_exact_tuple("source_ids", source_ids, EXPECTED_SOURCE_IDS)
    _require_exact_tuple("assumption_ids", assumption_ids, EXPECTED_ASSUMPTION_IDS)

    grid_version = _string_value(data, "grid_version")
    if grid_version != EXPECTED_GRID_VERSION:
        raise ValueError(f"grid_version must be {EXPECTED_GRID_VERSION!r}")

    execution = _mapping_value(data, "execution")
    phase = _string_value(execution, "phase")
    engine_status = _string_value(execution, "engine_status")
    runner_command = _string_value(execution, "runner_command")
    full_grid_run = _bool_value(execution, "full_grid_run")
    if phase != "raw_cell_engine":
        raise ValueError("execution.phase must be 'raw_cell_engine'")
    if engine_status != "raw_cell_table_implemented_pending_review":
        raise ValueError("execution.engine_status must be raw-cell pending-review status")
    if runner_command != "fts fbt atlas-v1-raw-cells":
        raise ValueError("execution.runner_command must be the atlas v1 raw-cell CLI command")
    if full_grid_run:
        raise ValueError("execution.full_grid_run must be false")

    primary = _mapping_value(data, "primary_comparison")
    primary_comparison_id = _string_value(primary, "comparison_id")
    if primary_comparison_id != EXPECTED_COMPARISON_ID:
        raise ValueError(f"primary comparison must be {EXPECTED_COMPARISON_ID!r}")
    if _string_value(primary, "truth_strategy") != "truth_map":
        raise ValueError("truth_strategy must be 'truth_map'")
    if _string_value(primary, "fitness_strategy") != "fitness_only_expected":
        raise ValueError("fitness_strategy must be 'fitness_only_expected'")
    extension_baselines_in_primary_results = _bool_value(
        primary, "extension_baselines_in_primary_results"
    )
    if extension_baselines_in_primary_results:
        raise ValueError("extension baselines must not be included in primary results")

    edge_policies = _mapping_value(data, "edge_case_policies")
    edge_policy_id = _string_value(edge_policies, "edge_policy_id")
    if edge_policy_id != EXPECTED_EDGE_POLICY_ID:
        raise ValueError(f"edge_policy_id must be {EXPECTED_EDGE_POLICY_ID!r}")

    axes = _mapping_value(_mapping_value(data, "grid_identity"), "draft_axes")
    world_state_counts = _positive_int_tuple(axes, "world_state_counts")
    perceptual_state_counts = _positive_int_tuple(axes, "perceptual_state_counts")
    prior_families = _string_tuple(axes, "prior_families", min_items=1)
    kernel_families = _string_tuple(axes, "kernel_families", min_items=1)
    fitness_families = _string_tuple(axes, "fitness_families", min_items=1)
    offered_sets = _string_tuple(axes, "offered_observation_sets", min_items=1)
    _require_exact_tuple("prior_families", prior_families, EXPECTED_PRIOR_FAMILIES)
    _require_exact_tuple("kernel_families", kernel_families, EXPECTED_KERNEL_FAMILIES)
    _require_exact_tuple("fitness_families", fitness_families, EXPECTED_FITNESS_FAMILIES)
    _require_exact_tuple("offered_observation_sets", offered_sets, EXPECTED_OFFERED_SETS)
    _validate_family_definitions(data)

    enumeration = _mapping_value(data, "enumeration")
    if _string_value(enumeration, "arithmetic") != "exact_rational":
        raise ValueError("enumeration.arithmetic must be 'exact_rational'")
    if _string_value(enumeration, "randomness") != "none":
        raise ValueError("enumeration.randomness must be 'none'")
    if _bool_value(enumeration, "stochastic_simulation"):
        raise ValueError("stochastic_simulation must be false")
    if not _bool_value(enumeration, "raw_cell_artifacts_required_before_aggregates"):
        raise ValueError("raw cell artifacts must be required before aggregates")
    if not _bool_value(enumeration, "manifest_required"):
        raise ValueError("manifest_required must be true")

    reporting = _mapping_value(data, "reporting")
    aggregate_label = _string_value(reporting, "aggregate_label")
    denominator_policy = _string_value(reporting, "denominator_policy")
    theorem_probability_claim = _bool_value(reporting, "theorem_probability_claim")
    if aggregate_label != EXPECTED_AGGREGATE_LABEL:
        raise ValueError(f"aggregate_label must be {EXPECTED_AGGREGATE_LABEL!r}")
    if denominator_policy != EXPECTED_DENOMINATOR_POLICY:
        raise ValueError(f"denominator_policy must be {EXPECTED_DENOMINATOR_POLICY!r}")
    if theorem_probability_claim:
        raise ValueError("theorem_probability_claim must be false")

    return AtlasV1Config(
        path=path,
        artifact_kind=artifact_kind,
        epistemic_status=epistemic_status,
        task_ids=task_ids,
        claim_ids=claim_ids,
        source_ids=source_ids,
        assumption_ids=assumption_ids,
        grid_version=grid_version,
        phase=phase,
        engine_status=engine_status,
        runner_command=runner_command,
        full_grid_run=full_grid_run,
        primary_comparison_id=primary_comparison_id,
        truth_strategy="truth_map",
        fitness_strategy="fitness_only_expected",
        extension_baselines_in_primary_results=extension_baselines_in_primary_results,
        edge_policy_id=edge_policy_id,
        world_state_counts=world_state_counts,
        perceptual_state_counts=perceptual_state_counts,
        prior_families=prior_families,
        kernel_families=kernel_families,
        fitness_families=fitness_families,
        offered_observation_sets=offered_sets,
        aggregate_label=aggregate_label,
        denominator_policy=denominator_policy,
        theorem_probability_claim=theorem_probability_claim,
        notes=_string_value(data, "notes"),
    )


def enumerate_axis_cells(config: AtlasV1Config) -> tuple[AtlasV1AxisCell, ...]:
    """Enumerate deterministic atlas v1 axis combinations from the draft config."""
    return tuple(
        AtlasV1AxisCell(
            world_state_count=world_count,
            perceptual_state_count=observation_count,
            prior_family_id=prior_family,
            kernel_family_id=kernel_family,
            fitness_family_id=fitness_family,
            offered_observation_set_id=offered_set,
            primary_comparison_id=config.primary_comparison_id,
            edge_policy_id=config.edge_policy_id,
        )
        for (
            world_count,
            observation_count,
            prior_family,
            kernel_family,
            fitness_family,
            offered_set,
        ) in product(
            config.world_state_counts,
            config.perceptual_state_counts,
            config.prior_families,
            config.kernel_families,
            config.fitness_families,
            config.offered_observation_sets,
        )
    )


def build_raw_cells(config: AtlasV1Config) -> tuple[AtlasV1RawCell, ...]:
    """Build exact raw cells without writing artifacts."""
    cells: list[AtlasV1RawCell] = []
    for axis in enumerate_axis_cells(config):
        world_states = _world_state_ids(axis.world_state_count)
        observations = _observation_ids(axis.perceptual_state_count)
        prior = _prior_values(axis.prior_family_id, world_states)
        kernel = _kernel_values(axis.kernel_family_id, world_states, observations)
        fitness = _fitness_values(axis.fitness_family_id, world_states)
        offered_observations = _offered_observations(
            axis.offered_observation_set_id,
            observations,
        )
        problem = _problem_from_values(observations, world_states, prior, kernel, fitness)
        cells.append(
            AtlasV1RawCell(
                cell_id=_cell_id(config.grid_version, axis),
                axis=axis,
                observations=observations,
                world_states=world_states,
                prior=prior,
                kernel=kernel,
                fitness=fitness,
                offered_observations=offered_observations,
                problem=problem,
            )
        )
    return tuple(cells)


def build_raw_cell_table(config: AtlasV1Config) -> JsonObject:
    """Build the exact atlas v1 raw-cell table without writing artifacts."""
    raw_cells = build_raw_cells(config)
    return {
        "schema_version": "1.0",
        "artifact_kind": ARTIFACT_KIND,
        "epistemic_status": "E",
        "task_ids": list(config.task_ids),
        "claim_ids": list(config.claim_ids),
        "source_ids": list(config.source_ids),
        "assumption_ids": list(config.assumption_ids),
        "grid_version": config.grid_version,
        "engine_scope": {
            "result_level": "raw_cells_only",
            "aggregate_report": False,
            "full_grid_run": config.full_grid_run,
            "runner_command": config.runner_command,
        },
        "primary_comparison": {
            "comparison_id": config.primary_comparison_id,
            "truth_strategy": config.truth_strategy,
            "fitness_strategy": config.fitness_strategy,
            "extension_baselines_in_primary_results": (
                config.extension_baselines_in_primary_results
            ),
        },
        "grid_semantics": {
            "aggregate_label_reserved_for_future_summaries": config.aggregate_label,
            "denominator_policy": config.denominator_policy,
            "theorem_probability_claim": config.theorem_probability_claim,
            "notes": config.notes,
        },
        "raw_cell_count": len(raw_cells),
        "cells": [
            _serialize_raw_cell(
                cell, evaluate_primary_cell(cell.problem, cell.offered_observations)
            )
            for cell in raw_cells
        ],
        "claim_boundary": {
            "allowed": [
                "This artifact is an exact raw-cell table for the atlas v1 draft config.",
                "Each cell records the approved primary comparison and edge-case statuses.",
            ],
            "forbidden": [
                "The full finite atlas has been run.",
                "Theorem 4 has been implemented, proved, or reproduced.",
                "Raw cells are a source-level theorem result.",
                "The artifact says anything about real perception, consciousness, spacetime, "
                "ontology, biology, ML/RL, or evolutionary dynamics.",
            ],
        },
    }


def _serialize_raw_cell(cell: AtlasV1RawCell, oracle_result: CellOracleResult) -> JsonObject:
    return {
        "cell_id": cell.cell_id,
        "task_ids": [TASK_ID],
        "claim_ids": list(EXPECTED_CLAIM_IDS),
        "source_ids": list(EXPECTED_SOURCE_IDS),
        "assumption_ids": list(EXPECTED_ASSUMPTION_IDS),
        "grid_version": cell.cell_id.split("__", maxsplit=1)[0],
        "axis": {
            "world_state_count": cell.axis.world_state_count,
            "perceptual_state_count": cell.axis.perceptual_state_count,
            "prior_family_id": cell.axis.prior_family_id,
            "kernel_family_id": cell.axis.kernel_family_id,
            "fitness_family_id": cell.axis.fitness_family_id,
            "offered_observation_set_id": cell.axis.offered_observation_set_id,
            "primary_comparison_id": cell.axis.primary_comparison_id,
            "edge_policy_id": cell.axis.edge_policy_id,
        },
        "status": oracle_result.status,
        "fitness_only_best_observations": list(oracle_result.fitness_only_best_observations),
        "truth_map_best_observations": list(oracle_result.truth_map_best_observations),
        "possible_truth_map_best_observation_sets": [
            list(observations)
            for observations in oracle_result.possible_truth_map_best_observation_sets
        ],
        "possible_comparison_statuses": list(oracle_result.possible_comparison_statuses),
        "input": {
            "world_states": list(cell.world_states),
            "observations": list(cell.observations),
            "offered_observations": list(cell.offered_observations),
            "prior": {
                world_state: _fraction_object(probability)
                for world_state, probability in cell.prior.items()
            },
            "kernel": {
                world_state: {
                    observation: _fraction_object(probability)
                    for observation, probability in row.items()
                }
                for world_state, row in cell.kernel.items()
            },
            "fitness": {
                world_state: _fraction_object(fitness)
                for world_state, fitness in cell.fitness.items()
            },
        },
        "observation_results": [
            {
                "observation": result.observation,
                "status": result.status,
                "marginal": _fraction_object(result.marginal),
                "posterior": {
                    world_state: _fraction_object(probability)
                    for world_state, probability in result.posterior
                },
                "map_estimates": list(result.map_estimates),
                "map_fitness_values": {
                    world_state: _fraction_object(fitness)
                    for world_state, fitness in result.map_fitness_values
                },
                "truth_score_values": [
                    _fraction_object(value) for value in result.truth_score_values
                ],
                "expected_fitness": None
                if result.expected_fitness is None
                else _fraction_object(result.expected_fitness),
                "map_tie_kind": result.map_tie_kind,
            }
            for result in oracle_result.observation_results
        ],
    }


def _world_state_ids(count: int) -> tuple[str, ...]:
    return tuple(f"w{index}" for index in range(1, count + 1))


def _observation_ids(count: int) -> tuple[str, ...]:
    return tuple(f"x{index}" for index in range(1, count + 1))


def _prior_values(family_id: str, world_states: tuple[str, ...]) -> dict[str, Fraction]:
    count = len(world_states)
    if family_id == "uniform":
        return {world_state: Fraction(1, count) for world_state in world_states}
    if family_id == "single_state_heavy":
        denominator = count + 1
        return {
            world_state: Fraction(2 if index == 0 else 1, denominator)
            for index, world_state in enumerate(world_states)
        }
    if family_id == "rational_simplex_small":
        denominator = count * (count + 1) // 2
        return {
            world_state: Fraction(index + 1, denominator)
            for index, world_state in enumerate(world_states)
        }
    raise ValueError(f"Unknown prior family: {family_id}")


def _kernel_values(
    family_id: str,
    world_states: tuple[str, ...],
    observations: tuple[str, ...],
) -> dict[str, dict[str, Fraction]]:
    if family_id == "pure_map":
        return {
            world_state: {
                observation: Fraction(1, 1)
                if observation == _mapped_observation(index, observations)
                else Fraction(0, 1)
                for observation in observations
            }
            for index, world_state in enumerate(world_states)
        }
    if family_id == "noisy_map":
        off_target = Fraction(1, 4 * (len(observations) - 1))
        return {
            world_state: {
                observation: Fraction(3, 4)
                if observation == _mapped_observation(index, observations)
                else off_target
                for observation in observations
            }
            for index, world_state in enumerate(world_states)
        }
    if family_id == "uninformative":
        return {
            world_state: {
                observation: Fraction(1, len(observations)) for observation in observations
            }
            for world_state in world_states
        }
    if family_id == "zero_marginal_probe":
        nonzero_observations = observations[:-1]
        nonzero_probability = Fraction(1, len(nonzero_observations))
        return {
            world_state: {
                observation: nonzero_probability
                if observation in nonzero_observations
                else Fraction(0, 1)
                for observation in observations
            }
            for world_state in world_states
        }
    raise ValueError(f"Unknown kernel family: {family_id}")


def _fitness_values(family_id: str, world_states: tuple[str, ...]) -> dict[str, Fraction]:
    if family_id == "single_peak":
        return {
            world_state: Fraction(10 if index == 0 else 0, 1)
            for index, world_state in enumerate(world_states)
        }
    if family_id == "equal":
        return {world_state: Fraction(5, 1) for world_state in world_states}
    if family_id == "multi_peak":
        return {
            world_state: Fraction(10 if index < 2 else 0, 1)
            for index, world_state in enumerate(world_states)
        }
    raise ValueError(f"Unknown fitness family: {family_id}")


def _offered_observations(family_id: str, observations: tuple[str, ...]) -> tuple[str, ...]:
    if family_id == "all_observations":
        return observations
    raise ValueError(f"Unknown offered observation set: {family_id}")


def _mapped_observation(world_index: int, observations: tuple[str, ...]) -> str:
    return observations[world_index % len(observations)]


def _problem_from_values(
    observations: tuple[str, ...],
    world_states: tuple[str, ...],
    prior: Mapping[str, Fraction],
    kernel: Mapping[str, Mapping[str, Fraction]],
    fitness: Mapping[str, Fraction],
) -> FiniteBayesianDecisionProblem:
    return FiniteBayesianDecisionProblem(
        observations=observations,
        world_rows=tuple(
            WorldStateRow(
                world_state=world_state,
                prior=prior[world_state],
                likelihoods=tuple(
                    (observation, kernel[world_state][observation]) for observation in observations
                ),
                fitness=fitness[world_state],
            )
            for world_state in world_states
        ),
    )


def _cell_id(grid_version: str, axis: AtlasV1AxisCell) -> str:
    return (
        f"{grid_version}__w{axis.world_state_count}__x{axis.perceptual_state_count}"
        f"__prior-{axis.prior_family_id}__kernel-{axis.kernel_family_id}"
        f"__fitness-{axis.fitness_family_id}"
        f"__offered-{axis.offered_observation_set_id}"
        f"__cmp-{axis.primary_comparison_id}__edge-{axis.edge_policy_id}"
    )


def _fraction_object(value: Fraction) -> JsonObject:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "label": _fraction_label(value),
    }


def _fraction_label(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _validate_family_definitions(data: Mapping[str, Any]) -> None:
    definitions = _mapping_value(data, "family_definitions")
    _require_exact_tuple(
        "family_definitions.priors",
        tuple(_mapping_value(definitions, "priors")),
        EXPECTED_PRIOR_FAMILIES,
    )
    _require_exact_tuple(
        "family_definitions.kernels",
        tuple(_mapping_value(definitions, "kernels")),
        EXPECTED_KERNEL_FAMILIES,
    )
    _require_exact_tuple(
        "family_definitions.fitness_functions",
        tuple(_mapping_value(definitions, "fitness_functions")),
        EXPECTED_FITNESS_FAMILIES,
    )


def _positive_int_tuple(data: Mapping[str, Any], key: str) -> tuple[int, ...]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        raise ValueError(f"{key} must be a non-empty list")
    integers: list[int] = []
    for item in value:
        if not isinstance(item, int) or item < 2:
            raise ValueError(f"{key} must contain integers >= 2")
        integers.append(item)
    if len(set(integers)) != len(integers):
        raise ValueError(f"{key} must not contain duplicates")
    return tuple(integers)


def _string_value(data: Mapping[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be a non-empty string")
    return value


def _string_tuple(
    data: Mapping[str, Any],
    key: str,
    *,
    min_items: int,
) -> tuple[str, ...]:
    value = data.get(key)
    if not isinstance(value, list) or len(value) < min_items:
        raise ValueError(f"{key} must contain at least {min_items} item(s)")
    strings: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item:
            raise ValueError(f"{key} must contain non-empty strings")
        _safe_id(item, key)
        strings.append(item)
    if len(set(strings)) != len(strings):
        raise ValueError(f"{key} must not contain duplicates")
    return tuple(strings)


def _bool_value(data: Mapping[str, Any], key: str) -> bool:
    value = data.get(key)
    if not isinstance(value, bool):
        raise ValueError(f"{key} must be a boolean")
    return value


def _mapping_value(data: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"{key} must be an object")
    return cast(Mapping[str, Any], value)


def _require_exact_tuple(key: str, actual: tuple[str, ...], expected: tuple[str, ...]) -> None:
    if actual != expected:
        raise ValueError(f"{key} must be exactly {expected!r}")


def _safe_id(value: str, context: str) -> None:
    if ID_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{context} must contain only letters, numbers, '_' or '-'")
