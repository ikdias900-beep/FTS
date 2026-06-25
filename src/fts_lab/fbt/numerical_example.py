"""Manifest-backed exact reproduction of the FBT numerical appendix."""

from __future__ import annotations

import platform
import sys
import uuid
from collections.abc import Mapping
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path
from typing import Any, Final, cast

from fts_lab import __version__
from fts_lab.doctor import find_project_root, git_state
from fts_lab.fbt.bayes import (
    FBTModelError,
    FiniteBayesianDecisionProblem,
    WorldStateRow,
    observation_marginal,
    posterior,
    unique_map_estimate,
)
from fts_lab.fbt.decision import expected_fitness, unique_best_observation
from fts_lab.manifests import (
    canonical_json_bytes,
    read_json_object,
    sha256_bytes,
    sha256_file,
    validate_manifest_file,
    write_immutable_bytes,
    write_immutable_json,
)

TASK_ID: Final = "TASK-002-FBT-NUMERICAL"
ARTIFACT_KIND: Final = "fbt_numerical_appendix_reproduction"
DEFAULT_CONFIG_PATH: Final = Path("experiments/configs/fbt_numerical_example.json")
JSON_REPORT_FILENAME: Final = "fbt_numerical_appendix.json"
MARKDOWN_REPORT_FILENAME: Final = "fbt_numerical_appendix.md"
EXPECTED_TASK_IDS: Final = (TASK_ID,)
EXPECTED_CLAIM_IDS: Final = (
    "CLM-FBT-APP-001",
    "CLM-FBT-APP-002",
    "CLM-FBT-APP-003",
    "CLM-FBT-APP-004",
)
EXPECTED_SOURCE_IDS: Final = ("SRC-FBT-2021",)
EXPECTED_ASSUMPTION_IDS: Final = ()

type JsonObject = dict[str, Any]


def run_fbt_numerical_example(
    config_path: Path | None = None, *, command: str | None = None
) -> dict[str, str]:
    """Run the exact Stage 2 FBT numerical reproduction and write a manifest."""
    root = find_project_root()
    config_file = (config_path or root / DEFAULT_CONFIG_PATH).resolve()
    config = load_numerical_example_config(config_file)
    problem = problem_from_config(config)
    result = build_reproduction_result(config, problem)
    json_bytes = canonical_json_bytes(result)
    report_bytes = render_derivation_report(result).encode("utf-8")

    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    suffix = uuid.uuid4().hex[:8].upper()
    run_id = f"EXP-TASK-002-FBT-NUMERICAL-{timestamp}-{suffix}"
    manifest_id = f"ART-TASK-002-FBT-NUMERICAL-MANIFEST-{timestamp}-{suffix}"
    derived_dir = root / "results/derived" / run_id
    reports_dir = root / "results/reports" / run_id
    json_report_path = derived_dir / JSON_REPORT_FILENAME
    markdown_report_path = reports_dir / MARKDOWN_REPORT_FILENAME
    manifest_path = root / "experiments/manifests" / f"{manifest_id}.json"

    write_immutable_bytes(json_report_path, json_bytes)
    write_immutable_bytes(markdown_report_path, report_bytes)

    lockfile = root / "uv.lock"
    if not lockfile.is_file():
        raise FileNotFoundError("uv.lock is required before writing an FBT manifest")

    json_checksum = sha256_bytes(json_bytes)
    report_checksum = sha256_bytes(report_bytes)
    manifest: dict[str, Any] = {
        "schema_version": "1.0",
        "manifest_id": manifest_id,
        "run_id": run_id,
        "artifact_kind": ARTIFACT_KIND,
        "epistemic_status": "R",
        "task_ids": list(EXPECTED_TASK_IDS),
        "claim_ids": list(EXPECTED_CLAIM_IDS),
        "source_ids": list(EXPECTED_SOURCE_IDS),
        "assumption_ids": list(EXPECTED_ASSUMPTION_IDS),
        "created_at_utc": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "command": command or " ".join(sys.argv),
        "parameters": {
            "config_path": str(config_file),
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
    }


def load_numerical_example_config(path: Path) -> JsonObject:
    """Load and validate the canonical source input table."""
    data = read_json_object(path)
    if _string_value(data, "schema_version") != "1.0":
        raise ValueError("schema_version must be '1.0'")
    if _string_value(data, "artifact_kind") != "fbt_numerical_appendix_source_table":
        raise ValueError("artifact_kind must be 'fbt_numerical_appendix_source_table'")
    _require_exact_tuple("task_ids", _string_tuple(data, "task_ids"), EXPECTED_TASK_IDS)
    _require_exact_tuple("claim_ids", _string_tuple(data, "claim_ids"), EXPECTED_CLAIM_IDS)
    _require_exact_tuple("source_ids", _string_tuple(data, "source_ids"), EXPECTED_SOURCE_IDS)
    _require_exact_tuple(
        "assumption_ids",
        _string_tuple(data, "assumption_ids", allow_empty=True),
        EXPECTED_ASSUMPTION_IDS,
    )
    _string_value(data, "source_locator")
    _string_tuple(data, "observations")
    world_states = data.get("world_states")
    if not isinstance(world_states, list) or not world_states:
        raise ValueError("world_states must be a non-empty list")
    return data


def problem_from_config(config: Mapping[str, Any]) -> FiniteBayesianDecisionProblem:
    """Build an exact immutable problem from a validated source config."""
    observations = _string_tuple(config, "observations")
    rows: list[WorldStateRow] = []
    world_states = config.get("world_states")
    if not isinstance(world_states, list):
        raise ValueError("world_states must be a list")
    for raw_row in world_states:
        if not isinstance(raw_row, dict):
            raise ValueError("world_states must contain objects")
        row = cast(dict[str, Any], raw_row)
        likelihoods = row.get("likelihoods")
        if not isinstance(likelihoods, dict):
            raise ValueError("likelihoods must be an object")
        likelihood_pairs = tuple(
            (observation, parse_fraction(_string_mapping_value(likelihoods, observation)))
            for observation in observations
        )
        rows.append(
            WorldStateRow(
                world_state=_string_value(row, "id"),
                prior=parse_fraction(_string_value(row, "prior")),
                fitness=parse_fraction(_string_value(row, "fitness")),
                likelihoods=likelihood_pairs,
            )
        )
    return FiniteBayesianDecisionProblem(observations=observations, world_rows=tuple(rows))


def parse_fraction(value: str) -> Fraction:
    """Parse a source-table rational value."""
    try:
        return Fraction(value)
    except ValueError as exc:
        raise ValueError(f"Invalid rational value: {value!r}") from exc


def build_reproduction_result(
    config: Mapping[str, Any],
    problem: FiniteBayesianDecisionProblem,
) -> JsonObject:
    """Compute the exact appendix reproduction result."""
    source_locator = _string_value(config, "source_locator")
    marginals = {
        observation: observation_marginal(problem, observation)
        for observation in problem.observations
    }
    posteriors = {
        observation: posterior(problem, observation) for observation in problem.observations
    }
    map_estimates = {
        observation: unique_map_estimate(posteriors[observation])
        for observation in problem.observations
    }
    fitness_by_world_state = problem.fitness_by_world_state()
    expected_fitness_values = {
        observation: expected_fitness(posteriors[observation], fitness_by_world_state)
        for observation in problem.observations
    }
    fitness_winner = unique_best_observation(expected_fitness_values)

    return {
        "schema_version": "1.0",
        "artifact_kind": ARTIFACT_KIND,
        "epistemic_status": "R",
        "task_ids": list(EXPECTED_TASK_IDS),
        "claim_ids": list(EXPECTED_CLAIM_IDS),
        "source_ids": list(EXPECTED_SOURCE_IDS),
        "assumption_ids": list(EXPECTED_ASSUMPTION_IDS),
        "source_locator": source_locator,
        "source_input": _source_input_dict(problem),
        "results": {
            "marginals": _fraction_mapping(marginals),
            "posteriors": {
                observation: _fraction_mapping(posteriors[observation])
                for observation in problem.observations
            },
            "map_estimates": map_estimates,
            "expected_fitness": _fraction_mapping(expected_fitness_values),
            "fitness_winner": fitness_winner,
        },
        "claim_trace": {
            "CLM-FBT-APP-001": ["results.marginals"],
            "CLM-FBT-APP-002": ["results.posteriors.x1", "results.map_estimates.x1"],
            "CLM-FBT-APP-003": ["results.posteriors.x2", "results.map_estimates.x2"],
            "CLM-FBT-APP-004": ["results.expected_fitness", "results.fitness_winner"],
        },
        "limitations": [
            "This reproduces one numerical appendix example only.",
            "No evolutionary simulation or general FBT theorem implementation is included.",
            "No claim about real perception, consciousness, spacetime, or ontology is made.",
        ],
    }


def render_derivation_report(result: Mapping[str, Any]) -> str:
    """Render a compact human-readable derivation report from the computed result."""
    source_input = _mapping_value(result, "source_input")
    results = _mapping_value(result, "results")
    lines = [
        "# FBT Numerical Appendix Exact Reproduction",
        "",
        "```text",
        f"TASK ID: {TASK_ID}",
        "EPISTEMIC STATUS: R",
        "SOURCE IDS: SRC-FBT-2021",
        "CLAIM IDS: CLM-FBT-APP-001, CLM-FBT-APP-002, CLM-FBT-APP-003, CLM-FBT-APP-004",
        "ASSUMPTION IDS: none",
        "```",
        "",
        "## Scope",
        "",
        "This report reproduces the Bayesian and expected-fitness arithmetic in the FBT "
        "numerical appendix. It does not implement evolutionary dynamics or the general FBT "
        "theorem.",
        "",
        "## Source Input",
        "",
        "| world state | p(x1 | w) | p(x2 | w) | prior mu(w) | fitness f(w) |",
        "|---|---:|---:|---:|---:|",
    ]
    rows = source_input.get("world_states")
    if not isinstance(rows, list):
        raise FBTModelError("result source_input.world_states must be a list")
    for row in rows:
        if not isinstance(row, dict):
            raise FBTModelError("source input rows must be objects")
        likelihoods = row.get("likelihoods")
        if not isinstance(likelihoods, dict):
            raise FBTModelError("source input likelihoods must be objects")
        lines.append(
            "| "
            f"{row['id']} | "
            f"{likelihoods['x1']} | "
            f"{likelihoods['x2']} | "
            f"{row['prior']} | "
            f"{row['fitness']} |"
        )

    marginals = _mapping_value(results, "marginals")
    posteriors = _mapping_value(results, "posteriors")
    map_estimates = _mapping_value(results, "map_estimates")
    expected_fitness_values = _mapping_value(results, "expected_fitness")
    lines.extend(
        [
            "",
            "## Exact Results",
            "",
            "| observation | P(x) | posterior over (w1, w2, w3) | MAP | expected fitness |",
            "|---|---:|---:|---|---:|",
        ]
    )
    for observation in ("x1", "x2"):
        posterior_for_observation = _mapping_value(posteriors, observation)
        posterior_label = (
            f"({_fraction_label(posterior_for_observation, 'w1')}, "
            f"{_fraction_label(posterior_for_observation, 'w2')}, "
            f"{_fraction_label(posterior_for_observation, 'w3')})"
        )
        lines.append(
            "| "
            f"{observation} | "
            f"{_fraction_label(marginals, observation)} | "
            f"{posterior_label} | "
            f"{map_estimates[observation]} | "
            f"{_fraction_label(expected_fitness_values, observation)} |"
        )
    lines.extend(
        [
            "",
            f"Unique expected-fitness winner: `{results['fitness_winner']}`.",
            "",
            "## Claim Boundary",
            "",
            "- Allowed: the executable companion reproduces the linked appendix arithmetic.",
            "- Forbidden: this single example proves the general FBT theorem or any claim about "
            "real perception.",
            "",
        ]
    )
    return "\n".join(lines)


def _source_input_dict(problem: FiniteBayesianDecisionProblem) -> JsonObject:
    return {
        "observations": list(problem.observations),
        "world_states": [
            {
                "id": row.world_state,
                "prior": _fraction_label_from_value(row.prior),
                "fitness": _fraction_label_from_value(row.fitness),
                "likelihoods": {
                    observation: _fraction_label_from_value(row.likelihood_for(observation))
                    for observation in problem.observations
                },
            }
            for row in problem.world_rows
        ],
    }


def _fraction_mapping(values: Mapping[str, Fraction]) -> JsonObject:
    return {
        key: {
            "numerator": value.numerator,
            "denominator": value.denominator,
            "label": _fraction_label_from_value(value),
        }
        for key, value in values.items()
    }


def _fraction_label_from_value(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _fraction_label(container: Mapping[str, Any], key: str) -> str:
    value = container.get(key)
    if not isinstance(value, dict):
        raise FBTModelError(f"Expected fraction object at key {key!r}")
    label = value.get("label")
    if not isinstance(label, str):
        raise FBTModelError(f"Expected fraction label at key {key!r}")
    return label


def _mapping_value(container: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = container.get(key)
    if not isinstance(value, dict):
        raise FBTModelError(f"Expected object at key {key!r}")
    return cast(Mapping[str, Any], value)


def _string_value(data: Mapping[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be a non-empty string")
    return value


def _string_mapping_value(data: Mapping[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be a non-empty string")
    return value


def _string_tuple(
    data: Mapping[str, Any],
    key: str,
    *,
    allow_empty: bool = False,
) -> tuple[str, ...]:
    value = data.get(key)
    if not isinstance(value, list):
        raise ValueError(f"{key} must be a list")
    if not value and not allow_empty:
        raise ValueError(f"{key} must be non-empty")
    strings: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item:
            raise ValueError(f"{key} must contain non-empty strings")
        strings.append(item)
    if len(set(strings)) != len(strings):
        raise ValueError(f"{key} must not contain duplicates")
    return tuple(strings)


def _require_exact_tuple(key: str, actual: tuple[str, ...], expected: tuple[str, ...]) -> None:
    if actual != expected:
        raise ValueError(f"{key} must be exactly {expected!r}")
