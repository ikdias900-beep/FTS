"""Manifest-backed Stage 4 FBT finite-atlas grid v0 smoke-run."""

from __future__ import annotations

import platform
import re
import sys
import uuid
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from fractions import Fraction
from itertools import product
from pathlib import Path
from typing import Any, Final, cast

from fts_lab import __version__
from fts_lab.doctor import find_project_root, git_state
from fts_lab.fbt.atlas_oracle import CellOracleResult, evaluate_primary_cell
from fts_lab.fbt.bayes import FBTModelError, FiniteBayesianDecisionProblem, WorldStateRow
from fts_lab.fbt.numerical_example import parse_fraction
from fts_lab.manifests import (
    canonical_json_bytes,
    read_json_object,
    sha256_bytes,
    sha256_file,
    validate_manifest_file,
    write_immutable_bytes,
    write_immutable_json,
)

TASK_ID: Final = "TASK-004-FBT-ATLAS-GRID-V0"
ARTIFACT_KIND: Final = "fbt_atlas_grid_v0_smoke"
CONFIG_ARTIFACT_KIND: Final = "fbt_atlas_grid_config"
DEFAULT_CONFIG_PATH: Final = Path("experiments/configs/fbt_atlas_v0.json")
JSON_REPORT_FILENAME: Final = "fbt_atlas_v0_smoke.json"
MARKDOWN_REPORT_FILENAME: Final = "fbt_atlas_v0_smoke.md"
EXPECTED_TASK_IDS: Final = (TASK_ID,)
EXPECTED_CLAIM_IDS: Final = ("CLM-FBT-ATLAS-001",)
EXPECTED_SOURCE_IDS: Final = ("SRC-FBT-2021",)
EXPECTED_ASSUMPTION_IDS: Final = (
    "ASM-FBT-0001",
    "ASM-FBT-0002",
    "ASM-FBT-0003",
    "ASM-FBT-0004",
)
EXPECTED_GRID_VERSION: Final = "fbt_atlas_v0"
EXPECTED_AGGREGATE_LABEL: Final = "grid_frequency"
EXPECTED_DENOMINATOR_POLICY: Final = "all_enumerated_cells"
ID_PATTERN: Final = re.compile(r"^[A-Za-z0-9_-]+$")

type JsonObject = dict[str, Any]


@dataclass(frozen=True)
class NamedPrior:
    """One exact prior distribution in the frozen smoke grid."""

    id: str
    values: Mapping[str, Fraction]


@dataclass(frozen=True)
class NamedKernel:
    """One exact observation kernel in the frozen smoke grid."""

    id: str
    values: Mapping[str, Mapping[str, Fraction]]


@dataclass(frozen=True)
class NamedFitnessFunction:
    """One exact nonnegative fitness function in the frozen smoke grid."""

    id: str
    values: Mapping[str, Fraction]


@dataclass(frozen=True)
class AtlasGridConfig:
    """Validated Stage 4 FBT grid v0 smoke configuration."""

    path: Path
    artifact_kind: str
    epistemic_status: str
    task_ids: tuple[str, ...]
    claim_ids: tuple[str, ...]
    source_ids: tuple[str, ...]
    assumption_ids: tuple[str, ...]
    grid_version: str
    observations: tuple[str, ...]
    world_states: tuple[str, ...]
    offered_observations: tuple[tuple[str, ...], ...]
    priors: tuple[NamedPrior, ...]
    kernels: tuple[NamedKernel, ...]
    fitness_functions: tuple[NamedFitnessFunction, ...]
    aggregate_label: str
    denominator_policy: str
    theorem_probability_claim: bool
    notes: str


@dataclass(frozen=True)
class AtlasGridCell:
    """One deterministic cell in the frozen Stage 4 smoke grid."""

    cell_id: str
    prior: NamedPrior
    kernel: NamedKernel
    fitness_function: NamedFitnessFunction
    offered_observations: tuple[str, ...]
    problem: FiniteBayesianDecisionProblem


def run_fbt_atlas_grid_v0(
    config_path: Path | None = None, *, command: str | None = None
) -> dict[str, str]:
    """Run the exact Stage 4 FBT grid v0 smoke enumeration and write a manifest."""
    root = find_project_root()
    config_file = (config_path or root / DEFAULT_CONFIG_PATH).resolve()
    config = load_atlas_grid_config(config_file)
    result = build_grid_result(config)
    json_bytes = canonical_json_bytes(result)
    report_bytes = render_grid_report(result).encode("utf-8")

    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    suffix = uuid.uuid4().hex[:8].upper()
    run_id = f"EXP-TASK-004-FBT-ATLAS-GRID-V0-{timestamp}-{suffix}"
    manifest_id = f"ART-TASK-004-FBT-ATLAS-GRID-V0-MANIFEST-{timestamp}-{suffix}"
    derived_dir = root / "results/derived" / run_id
    reports_dir = root / "results/reports" / run_id
    json_report_path = derived_dir / JSON_REPORT_FILENAME
    markdown_report_path = reports_dir / MARKDOWN_REPORT_FILENAME
    manifest_path = root / "experiments/manifests" / f"{manifest_id}.json"

    write_immutable_bytes(json_report_path, json_bytes)
    write_immutable_bytes(markdown_report_path, report_bytes)

    lockfile = root / "uv.lock"
    if not lockfile.is_file():
        raise FileNotFoundError("uv.lock is required before writing an FBT atlas manifest")

    json_checksum = sha256_bytes(json_bytes)
    report_checksum = sha256_bytes(report_bytes)
    summary = _mapping_value(result, "summary")
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
            "aggregate_label": config.aggregate_label,
            "denominator_policy": config.denominator_policy,
            "cell_count": summary["total_cells"],
            "json_report_filename": JSON_REPORT_FILENAME,
            "markdown_report_filename": MARKDOWN_REPORT_FILENAME,
        },
        "seed": None,
        "git": git_state(root),
        "environment": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "dependency_lock_sha256": sha256_file(lockfile),
        },
        "inputs": [{"path": str(config_file), "sha256": sha256_file(config_file)}],
        "outputs": [
            {"path": str(json_report_path), "sha256": json_checksum},
            {"path": str(markdown_report_path), "sha256": report_checksum},
        ],
        "status": "completed",
        "error": None,
        "implementation": {"package": "fts-lab", "version": __version__},
    }
    write_immutable_json(manifest_path, manifest)
    validate_manifest_file(manifest_path, project_root=root)

    return {
        "json_report_checksum": json_checksum,
        "json_report_path": str(json_report_path),
        "manifest_path": str(manifest_path),
        "markdown_report_checksum": report_checksum,
        "markdown_report_path": str(markdown_report_path),
        "run_id": run_id,
        "cell_count": str(summary["total_cells"]),
    }


def load_atlas_grid_config(path: Path) -> AtlasGridConfig:
    """Load and validate the frozen Stage 4 FBT atlas grid v0 config."""
    data = read_json_object(path)
    if _string_value(data, "schema_version") != "1.0":
        raise ValueError("schema_version must be '1.0'")
    artifact_kind = _string_value(data, "artifact_kind")
    if artifact_kind != CONFIG_ARTIFACT_KIND:
        raise ValueError(f"artifact_kind must be {CONFIG_ARTIFACT_KIND!r}")
    epistemic_status = _string_value(data, "epistemic_status")
    if epistemic_status != "E":
        raise ValueError("Stage 4 atlas grid v0 config must use epistemic_status 'E'")

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
    observations = _string_tuple(data, "observations", min_items=1)
    world_states = _string_tuple(data, "world_states", min_items=1)
    _validate_ids(("observations", observations), ("world_states", world_states))

    reporting = _mapping_value(data, "reporting")
    aggregate_label = _string_value(reporting, "aggregate_label")
    denominator_policy = _string_value(reporting, "denominator_policy")
    theorem_probability_claim = _bool_value(reporting, "theorem_probability_claim")
    if aggregate_label != EXPECTED_AGGREGATE_LABEL:
        raise ValueError(f"aggregate_label must be {EXPECTED_AGGREGATE_LABEL!r}")
    if denominator_policy != EXPECTED_DENOMINATOR_POLICY:
        raise ValueError(f"denominator_policy must be {EXPECTED_DENOMINATOR_POLICY!r}")
    if theorem_probability_claim:
        raise ValueError("theorem_probability_claim must be false for finite grid smoke runs")

    config = AtlasGridConfig(
        path=path,
        artifact_kind=artifact_kind,
        epistemic_status=epistemic_status,
        task_ids=task_ids,
        claim_ids=claim_ids,
        source_ids=source_ids,
        assumption_ids=assumption_ids,
        grid_version=grid_version,
        observations=observations,
        world_states=world_states,
        offered_observations=_offered_observation_sets(data, observations),
        priors=_named_prior_tuple(data, world_states),
        kernels=_named_kernel_tuple(data, world_states, observations),
        fitness_functions=_named_fitness_tuple(data, world_states),
        aggregate_label=aggregate_label,
        denominator_policy=denominator_policy,
        theorem_probability_claim=theorem_probability_claim,
        notes=_string_value(data, "notes"),
    )
    if not config.priors or not config.kernels or not config.fitness_functions:
        raise ValueError("priors, kernels, and fitness_functions must be non-empty")
    return config


def enumerate_grid_cells(config: AtlasGridConfig) -> tuple[AtlasGridCell, ...]:
    """Enumerate deterministic finite cells for the frozen smoke grid."""
    cells: list[AtlasGridCell] = []
    for prior, kernel, fitness_function, offered in product(
        config.priors,
        config.kernels,
        config.fitness_functions,
        config.offered_observations,
    ):
        cell_id = _cell_id(config, prior, kernel, fitness_function, offered)
        cells.append(
            AtlasGridCell(
                cell_id=cell_id,
                prior=prior,
                kernel=kernel,
                fitness_function=fitness_function,
                offered_observations=offered,
                problem=_problem_for_cell(config, prior, kernel, fitness_function),
            )
        )
    return tuple(cells)


def build_grid_result(config: AtlasGridConfig) -> JsonObject:
    """Build the exact grid v0 smoke result without writing artifacts."""
    cells = enumerate_grid_cells(config)
    cell_results = [
        _serialize_cell(cell, evaluate_primary_cell(cell.problem, cell.offered_observations))
        for cell in cells
    ]
    status_counts = Counter(_string_value(cell, "status") for cell in cell_results)
    total_cells = len(cell_results)
    return {
        "schema_version": "1.0",
        "artifact_kind": ARTIFACT_KIND,
        "epistemic_status": "E",
        "task_ids": list(config.task_ids),
        "claim_ids": list(config.claim_ids),
        "source_ids": list(config.source_ids),
        "assumption_ids": list(config.assumption_ids),
        "grid_version": config.grid_version,
        "grid_semantics": {
            "aggregate_label": config.aggregate_label,
            "denominator_policy": config.denominator_policy,
            "theorem_probability_claim": config.theorem_probability_claim,
            "notes": config.notes,
        },
        "summary": {
            "total_cells": total_cells,
            "status_counts": dict(sorted(status_counts.items())),
            "grid_frequencies_by_status": {
                status: _fraction_object(Fraction(count, total_cells))
                for status, count in sorted(status_counts.items())
            },
        },
        "cells": cell_results,
        "claim_boundary": {
            "allowed": [
                "This run enumerates the frozen fbt_atlas_v0 smoke grid through the "
                "approved finite-cell oracle.",
                "The reported aggregates are grid_frequency values for this project grid only.",
            ],
            "forbidden": [
                "The full finite atlas has been run.",
                "Theorem 4 has been implemented, proved, or reproduced.",
                "A project grid_frequency is a source theorem probability.",
                "The result says anything about real perception, consciousness, spacetime, "
                "ontology, biology, ML/RL, or evolutionary dynamics.",
            ],
        },
        "limitations": [
            "This is a small frozen smoke grid, not a full finite atlas.",
            "The output is an extension artifact with epistemic_status E.",
            "Grid frequencies are denominator counts over fbt_atlas_v0 cells only.",
            "Independent review is deferred until the Stage 4 spec/oracle/grid-smoke bundle.",
        ],
    }


def render_grid_report(result: Mapping[str, Any]) -> str:
    """Render a compact human-readable report for the grid v0 smoke result."""
    summary = _mapping_value(result, "summary")
    semantics = _mapping_value(result, "grid_semantics")
    status_counts = _mapping_value(summary, "status_counts")
    frequencies = _mapping_value(summary, "grid_frequencies_by_status")
    total_cells = summary["total_cells"]
    if not isinstance(total_cells, int):
        raise FBTModelError("summary.total_cells must be an integer")

    lines = [
        "# FBT Atlas Grid v0 Smoke Run",
        "",
        "```text",
        f"TASK ID: {TASK_ID}",
        "EPISTEMIC STATUS: E",
        "SOURCE IDS: SRC-FBT-2021",
        "CLAIM IDS: CLM-FBT-ATLAS-001",
        "ASSUMPTION IDS: ASM-FBT-0001, ASM-FBT-0002, ASM-FBT-0003, ASM-FBT-0004",
        f"GRID VERSION: {result['grid_version']}",
        f"AGGREGATE LABEL: {semantics['aggregate_label']}",
        "THEOREM PROBABILITY CLAIM: false",
        "```",
        "",
        "## Scope",
        "",
        "This report enumerates the frozen `fbt_atlas_v0` smoke grid through the approved "
        "Stage 4 finite-cell oracle. It is not a full atlas run and not a source theorem "
        "probability calculation.",
        "",
        "## Status Summary",
        "",
        f"Total enumerated cells: `{total_cells}`.",
        "",
        "| status | count | grid_frequency |",
        "|---|---:|---:|",
    ]
    for status in sorted(status_counts):
        count = status_counts[status]
        frequency = _mapping_value(frequencies, status)
        lines.append(f"| `{status}` | {count} | {frequency['label']} |")
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            "- Allowed: this command produces exact grid_frequency values for `fbt_atlas_v0`.",
            "- Forbidden: treating those frequencies as Theorem 4 probabilities or as a reviewed "
            "scientific conclusion.",
            "",
        ]
    )
    return "\n".join(lines)


def _serialize_cell(cell: AtlasGridCell, oracle_result: CellOracleResult) -> JsonObject:
    return {
        "cell_id": cell.cell_id,
        "grid_version": cell.cell_id.split("__", maxsplit=1)[0],
        "prior_id": cell.prior.id,
        "kernel_id": cell.kernel.id,
        "fitness_function_id": cell.fitness_function.id,
        "offered_observations": list(cell.offered_observations),
        "status": oracle_result.status,
        "fitness_only_best_observations": list(oracle_result.fitness_only_best_observations),
        "truth_map_best_observations": list(oracle_result.truth_map_best_observations),
        "possible_truth_map_best_observation_sets": [
            list(observations)
            for observations in oracle_result.possible_truth_map_best_observation_sets
        ],
        "possible_comparison_statuses": list(oracle_result.possible_comparison_statuses),
        "input": {
            "observations": list(cell.problem.observations),
            "world_states": [
                {
                    "id": row.world_state,
                    "prior": _fraction_object(row.prior),
                    "fitness": _fraction_object(row.fitness),
                    "likelihoods": {
                        observation: _fraction_object(row.likelihood_for(observation))
                        for observation in cell.problem.observations
                    },
                }
                for row in cell.problem.world_rows
            ],
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


def _problem_for_cell(
    config: AtlasGridConfig,
    prior: NamedPrior,
    kernel: NamedKernel,
    fitness_function: NamedFitnessFunction,
) -> FiniteBayesianDecisionProblem:
    rows = [
        WorldStateRow(
            world_state=world_state,
            prior=prior.values[world_state],
            likelihoods=tuple(
                (observation, kernel.values[world_state][observation])
                for observation in config.observations
            ),
            fitness=fitness_function.values[world_state],
        )
        for world_state in config.world_states
    ]
    return FiniteBayesianDecisionProblem(
        observations=config.observations,
        world_rows=tuple(rows),
    )


def _cell_id(
    config: AtlasGridConfig,
    prior: NamedPrior,
    kernel: NamedKernel,
    fitness_function: NamedFitnessFunction,
    offered_observations: Sequence[str],
) -> str:
    offered_label = "-".join(offered_observations)
    return (
        f"{config.grid_version}__prior-{prior.id}__kernel-{kernel.id}"
        f"__fitness-{fitness_function.id}__offered-{offered_label}"
    )


def _named_prior_tuple(
    data: Mapping[str, Any],
    world_states: tuple[str, ...],
) -> tuple[NamedPrior, ...]:
    raw_items = _list_value(data, "priors")
    priors: list[NamedPrior] = []
    for raw_item in raw_items:
        item = _mapping_item(raw_item, "priors")
        prior_id = _safe_id(_string_value(item, "id"), "prior id")
        values = _fraction_mapping_for_keys(_mapping_value(item, "values"), world_states, "prior")
        _require_probability_distribution(values.values(), f"prior {prior_id}")
        priors.append(NamedPrior(id=prior_id, values=values))
    _require_unique_ids("priors", tuple(prior.id for prior in priors))
    return tuple(priors)


def _named_kernel_tuple(
    data: Mapping[str, Any],
    world_states: tuple[str, ...],
    observations: tuple[str, ...],
) -> tuple[NamedKernel, ...]:
    raw_items = _list_value(data, "kernels")
    kernels: list[NamedKernel] = []
    for raw_item in raw_items:
        item = _mapping_item(raw_item, "kernels")
        kernel_id = _safe_id(_string_value(item, "id"), "kernel id")
        raw_values = _mapping_value(item, "values")
        _require_exact_keyset(raw_values, world_states, f"kernel {kernel_id} world states")
        rows: dict[str, dict[str, Fraction]] = {}
        for world_state in world_states:
            row = _fraction_mapping_for_keys(
                _mapping_value(raw_values, world_state),
                observations,
                f"kernel {kernel_id} row {world_state}",
            )
            _require_probability_distribution(row.values(), f"kernel {kernel_id} row {world_state}")
            rows[world_state] = row
        kernels.append(NamedKernel(id=kernel_id, values=rows))
    _require_unique_ids("kernels", tuple(kernel.id for kernel in kernels))
    return tuple(kernels)


def _named_fitness_tuple(
    data: Mapping[str, Any],
    world_states: tuple[str, ...],
) -> tuple[NamedFitnessFunction, ...]:
    raw_items = _list_value(data, "fitness_functions")
    fitness_functions: list[NamedFitnessFunction] = []
    for raw_item in raw_items:
        item = _mapping_item(raw_item, "fitness_functions")
        fitness_id = _safe_id(_string_value(item, "id"), "fitness function id")
        values = _fraction_mapping_for_keys(
            _mapping_value(item, "values"),
            world_states,
            f"fitness function {fitness_id}",
        )
        for value in values.values():
            if value < 0:
                raise ValueError(f"fitness function {fitness_id} must be nonnegative")
        fitness_functions.append(NamedFitnessFunction(id=fitness_id, values=values))
    _require_unique_ids(
        "fitness_functions",
        tuple(fitness_function.id for fitness_function in fitness_functions),
    )
    return tuple(fitness_functions)


def _offered_observation_sets(
    data: Mapping[str, Any],
    observations: tuple[str, ...],
) -> tuple[tuple[str, ...], ...]:
    raw_value = data.get("offered_observations")
    if not isinstance(raw_value, list) or not raw_value:
        raise ValueError("offered_observations must be a non-empty list")
    offered_sets: list[tuple[str, ...]] = []
    observation_set = set(observations)
    for raw_set in raw_value:
        if not isinstance(raw_set, list) or not raw_set:
            raise ValueError("offered_observations must contain non-empty lists")
        offered = tuple(_safe_id(cast(str, item), "offered observation") for item in raw_set)
        if len(set(offered)) != len(offered):
            raise ValueError("offered observation sets must not contain duplicates")
        unknown = sorted(set(offered) - observation_set)
        if unknown:
            raise ValueError(f"offered observation set contains unknown observations: {unknown}")
        offered_sets.append(offered)
    if len(set(offered_sets)) != len(offered_sets):
        raise ValueError("offered_observations must not contain duplicate sets")
    return tuple(offered_sets)


def _fraction_mapping_for_keys(
    raw_values: Mapping[str, Any],
    expected_keys: tuple[str, ...],
    context: str,
) -> dict[str, Fraction]:
    _require_exact_keyset(raw_values, expected_keys, context)
    return {key: parse_fraction(_string_value(raw_values, key)) for key in expected_keys}


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


def _require_probability_distribution(values: Iterable[Fraction], context: str) -> None:
    value_tuple = tuple(values)
    for value in value_tuple:
        if value < 0:
            raise ValueError(f"{context} probabilities must be nonnegative")
    total = sum(value_tuple, Fraction(0, 1))
    if total != 1:
        raise ValueError(f"{context} probabilities must sum to 1, got {total}")


def _validate_ids(*items: tuple[str, tuple[str, ...]]) -> None:
    for context, values in items:
        for value in values:
            _safe_id(value, context)


def _safe_id(value: str, context: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{context} must be a non-empty string")
    if ID_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{context} must contain only letters, numbers, '_' or '-'")
    return value


def _require_unique_ids(context: str, values: tuple[str, ...]) -> None:
    if len(set(values)) != len(values):
        raise ValueError(f"{context} must not contain duplicate ids")


def _require_exact_keyset(
    data: Mapping[str, Any],
    expected_keys: tuple[str, ...],
    context: str,
) -> None:
    actual = set(data)
    expected = set(expected_keys)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise ValueError(f"{context} keys mismatch; missing={missing}, extra={extra}")


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


def _mapping_item(value: Any, context: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{context} must contain objects")
    return cast(Mapping[str, Any], value)


def _list_value(data: Mapping[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        raise ValueError(f"{key} must be a non-empty list")
    return value


def _require_exact_tuple(key: str, actual: tuple[str, ...], expected: tuple[str, ...]) -> None:
    if actual != expected:
        raise ValueError(f"{key} must be exactly {expected!r}")
