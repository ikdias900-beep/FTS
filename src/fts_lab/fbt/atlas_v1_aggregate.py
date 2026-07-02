"""Aggregate/report layer for Stage 4 FBT atlas v1 raw-cell artifacts."""

from __future__ import annotations

import platform
import sys
import uuid
from collections import Counter
from collections.abc import Mapping
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path
from typing import Any, Final, cast

from fts_lab import __version__
from fts_lab.doctor import find_project_root, git_state
from fts_lab.manifests import (
    canonical_json_bytes,
    read_json_object,
    sha256_bytes,
    sha256_file,
    validate_manifest_file,
    write_immutable_bytes,
    write_immutable_json,
)

TASK_ID: Final = "TASK-004-FBT-ATLAS-V1-AGGREGATE"
SPEC_TASK_ID: Final = "TASK-004-FBT-ATLAS-V1-SPEC"
ENGINE_TASK_ID: Final = "TASK-004-FBT-ATLAS-V1-ENGINE"
ARTIFACT_KIND: Final = "fbt_atlas_v1_aggregate_report"
RAW_CELL_ARTIFACT_KIND: Final = "fbt_atlas_v1_raw_cell_table"
AGGREGATE_JSON_FILENAME: Final = "fbt_atlas_v1_aggregate.json"
MARKDOWN_REPORT_FILENAME: Final = "fbt_atlas_v1_report.md"
EXPECTED_TASK_IDS: Final = (SPEC_TASK_ID, ENGINE_TASK_ID, TASK_ID)
EXPECTED_RAW_TASK_IDS: Final = (SPEC_TASK_ID, ENGINE_TASK_ID)
EXPECTED_CLAIM_IDS: Final = ("CLM-FBT-ATLAS-001",)
EXPECTED_SOURCE_IDS: Final = ("SRC-FBT-2021",)
EXPECTED_ASSUMPTION_IDS: Final = (
    "ASM-FBT-0001",
    "ASM-FBT-0002",
    "ASM-FBT-0003",
    "ASM-FBT-0004",
)
EXPECTED_GRID_VERSION: Final = "fbt_atlas_v1_draft"
EXPECTED_AGGREGATE_LABEL: Final = "grid_frequency"
EXPECTED_DENOMINATOR_POLICY: Final = "all_enumerated_cells"
DENOMINATOR_BASIS: Final = "all_raw_cells"

type JsonObject = dict[str, Any]


def run_fbt_atlas_v1_aggregate(
    raw_cells_path: Path,
    *,
    command: str | None = None,
) -> dict[str, str]:
    """Build aggregate JSON and Markdown report from a saved raw-cell artifact."""
    root = find_project_root()
    raw_table_path = raw_cells_path.resolve()
    raw_table = load_raw_cell_table(raw_table_path)
    raw_checksum = sha256_file(raw_table_path)
    aggregate = build_aggregate_report(
        raw_table,
        raw_cells_path=raw_table_path,
        raw_cell_table_sha256=raw_checksum,
    )
    aggregate_bytes = canonical_json_bytes(aggregate)
    markdown_bytes = render_aggregate_markdown(aggregate).encode("utf-8")

    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    suffix = uuid.uuid4().hex[:8].upper()
    run_id = f"EXP-TASK-004-FBT-ATLAS-V1-AGGREGATE-{timestamp}-{suffix}"
    manifest_id = f"ART-TASK-004-FBT-ATLAS-V1-AGGREGATE-MANIFEST-{timestamp}-{suffix}"
    derived_dir = root / "results/derived" / run_id
    reports_dir = root / "results/reports" / run_id
    aggregate_path = derived_dir / AGGREGATE_JSON_FILENAME
    markdown_path = reports_dir / MARKDOWN_REPORT_FILENAME
    manifest_path = root / "experiments/manifests" / f"{manifest_id}.json"

    write_immutable_bytes(aggregate_path, aggregate_bytes)
    write_immutable_bytes(markdown_path, markdown_bytes)

    lockfile = root / "uv.lock"
    if not lockfile.is_file():
        raise FileNotFoundError("uv.lock is required before writing an atlas v1 manifest")

    aggregate_checksum = sha256_bytes(aggregate_bytes)
    markdown_checksum = sha256_bytes(markdown_bytes)
    summary = _mapping_value(aggregate, "summary")
    total_raw_cells = _int_value(summary, "total_raw_cells")

    manifest: dict[str, Any] = {
        "schema_version": "1.0",
        "manifest_id": manifest_id,
        "run_id": run_id,
        "artifact_kind": ARTIFACT_KIND,
        "epistemic_status": "E",
        "task_ids": list(EXPECTED_TASK_IDS),
        "claim_ids": list(EXPECTED_CLAIM_IDS),
        "source_ids": list(EXPECTED_SOURCE_IDS),
        "assumption_ids": list(EXPECTED_ASSUMPTION_IDS),
        "created_at_utc": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "command": command or " ".join(sys.argv),
        "parameters": {
            "raw_cells_path": str(raw_table_path),
            "grid_version": _string_value(aggregate, "grid_version"),
            "result_level": "aggregate_from_raw_cells",
            "aggregate_label": EXPECTED_AGGREGATE_LABEL,
            "denominator_policy": EXPECTED_DENOMINATOR_POLICY,
            "denominator_basis": DENOMINATOR_BASIS,
            "raw_cell_count": total_raw_cells,
            "recomputes_cells": False,
            "full_grid_run": False,
            "aggregate_json_filename": AGGREGATE_JSON_FILENAME,
            "markdown_report_filename": MARKDOWN_REPORT_FILENAME,
        },
        "seed": None,
        "git": git_state(root),
        "environment": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "dependency_lock_sha256": sha256_file(lockfile),
        },
        "inputs": [{"path": str(raw_table_path), "sha256": raw_checksum}],
        "outputs": [
            {"path": str(aggregate_path), "sha256": aggregate_checksum},
            {"path": str(markdown_path), "sha256": markdown_checksum},
        ],
        "status": "completed",
        "error": None,
        "implementation": {"package": "fts-lab", "version": __version__},
    }
    write_immutable_json(manifest_path, manifest)
    validate_manifest_file(manifest_path, project_root=root)

    return {
        "json_report_checksum": aggregate_checksum,
        "json_report_path": str(aggregate_path),
        "markdown_report_checksum": markdown_checksum,
        "markdown_report_path": str(markdown_path),
        "manifest_path": str(manifest_path),
        "run_id": run_id,
        "cell_count": str(total_raw_cells),
    }


def load_raw_cell_table(path: Path) -> JsonObject:
    """Read and validate an atlas v1 raw-cell artifact."""
    raw_table = read_json_object(path)
    _validate_raw_cell_table(raw_table)
    return raw_table


def build_aggregate_report(
    raw_table: Mapping[str, Any],
    *,
    raw_cells_path: Path | None = None,
    raw_cell_table_sha256: str | None = None,
) -> JsonObject:
    """Build a deterministic status aggregate from an already-materialized raw table."""
    _validate_raw_cell_table(raw_table)
    cells = _list_value(raw_table, "cells")
    total_cells = len(cells)
    status_counts = Counter(_string_value(_mapping_item(cell, "cells"), "status") for cell in cells)
    status_count_dict = dict(sorted(status_counts.items()))
    frequencies = {
        status: _fraction_object(Fraction(count, total_cells))
        for status, count in status_count_dict.items()
    }
    status_rows = [
        {
            "status": status,
            "count": count,
            "grid_frequency": frequencies[status],
        }
        for status, count in status_count_dict.items()
    ]

    input_artifact: dict[str, Any] = {
        "artifact_kind": RAW_CELL_ARTIFACT_KIND,
        "raw_cell_count": total_cells,
    }
    if raw_cells_path is not None:
        input_artifact["path"] = str(raw_cells_path)
    if raw_cell_table_sha256 is not None:
        input_artifact["sha256"] = raw_cell_table_sha256

    grid_semantics = _mapping_value(raw_table, "grid_semantics")
    denominator_policy = _string_value(grid_semantics, "denominator_policy")
    if denominator_policy != EXPECTED_DENOMINATOR_POLICY:
        raise ValueError(f"raw denominator_policy must be {EXPECTED_DENOMINATOR_POLICY!r}")

    return {
        "schema_version": "1.0",
        "artifact_kind": ARTIFACT_KIND,
        "epistemic_status": "E",
        "task_ids": list(EXPECTED_TASK_IDS),
        "claim_ids": list(EXPECTED_CLAIM_IDS),
        "source_ids": list(EXPECTED_SOURCE_IDS),
        "assumption_ids": list(EXPECTED_ASSUMPTION_IDS),
        "grid_version": _string_value(raw_table, "grid_version"),
        "input_artifact": input_artifact,
        "aggregate_scope": {
            "source": "raw_cell_artifact_only",
            "raw_cell_artifact_kind": RAW_CELL_ARTIFACT_KIND,
            "recomputes_cells": False,
            "reads_config": False,
            "aggregate_label": EXPECTED_AGGREGATE_LABEL,
            "denominator_policy": denominator_policy,
            "denominator_basis": DENOMINATOR_BASIS,
            "blocked_cells_in_denominator": True,
            "tie_sensitive_cells_in_denominator": True,
            "full_grid_run": False,
            "source_theorem_result_claim": False,
        },
        "summary": {
            "total_raw_cells": total_cells,
            "status_counts": status_count_dict,
            "grid_frequencies_by_status": frequencies,
            "status_rows": status_rows,
        },
        "claim_boundary": {
            "allowed": [
                "This artifact aggregates status counts from one atlas v1 raw-cell artifact.",
                "The reported values are grid_frequency summaries over the input raw cells only.",
            ],
            "forbidden": [
                "The full finite atlas has been run.",
                "Theorem 4 has been implemented, proved, reproduced, or reviewed.",
                "A project grid_frequency is a source theorem result.",
                "The result says anything about real perception, consciousness, spacetime, "
                "ontology, biology, ML/RL, figures, UI, or evolutionary dynamics.",
            ],
        },
        "limitations": [
            "The aggregate is derived only from the provided raw-cell JSON artifact.",
            "The command does not read the v1 config and does not regenerate cells.",
            "The output remains pending independent review as part of the atlas v1 bundle.",
        ],
    }


def render_aggregate_markdown(aggregate: Mapping[str, Any]) -> str:
    """Render the atlas v1 aggregate as a compact human-readable report."""
    summary = _mapping_value(aggregate, "summary")
    scope = _mapping_value(aggregate, "aggregate_scope")
    input_artifact = _mapping_value(aggregate, "input_artifact")
    rows = _list_value(summary, "status_rows")
    total_raw_cells = _int_value(summary, "total_raw_cells")

    lines = [
        "# FBT Atlas v1 Aggregate Report",
        "",
        "```text",
        f"TASK IDS: {', '.join(EXPECTED_TASK_IDS)}",
        "EPISTEMIC STATUS: E",
        "SOURCE IDS: SRC-FBT-2021",
        "CLAIM IDS: CLM-FBT-ATLAS-001",
        "ASSUMPTION IDS: ASM-FBT-0001, ASM-FBT-0002, ASM-FBT-0003, ASM-FBT-0004",
        f"GRID VERSION: {_string_value(aggregate, 'grid_version')}",
        f"AGGREGATE LABEL: {scope['aggregate_label']}",
        f"DENOMINATOR POLICY: {scope['denominator_policy']}",
        f"DENOMINATOR BASIS: {scope['denominator_basis']}",
        "RECOMPUTES CELLS: false",
        "```",
        "",
        "## Scope",
        "",
        "This report reads one saved `fbt_atlas_v1_raw_cell_table` artifact and summarizes "
        "its cell statuses. It does not read the draft config, regenerate cells, launch a "
        "full atlas run, or implement Theorem 4.",
        "",
        "## Input Artifact",
        "",
        f"- artifact_kind: `{input_artifact['artifact_kind']}`",
        f"- raw_cell_count: `{input_artifact['raw_cell_count']}`",
    ]
    if "path" in input_artifact:
        lines.append(f"- path: `{input_artifact['path']}`")
    if "sha256" in input_artifact:
        lines.append(f"- sha256: `{input_artifact['sha256']}`")
    lines.extend(
        [
            "",
            "## Status Summary",
            "",
            f"Total raw cells: `{total_raw_cells}`.",
            "",
            "| status | count | grid_frequency |",
            "|---|---:|---:|",
        ]
    )
    for raw_row in rows:
        row = _mapping_item(raw_row, "status_rows")
        frequency = _mapping_value(row, "grid_frequency")
        lines.append(
            f"| `{_string_value(row, 'status')}` | {_int_value(row, 'count')} | "
            f"{frequency['label']} |"
        )
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            "- Allowed: status-count and grid_frequency summaries over the input raw cells.",
            "- Forbidden: treating this as a full atlas, theorem implementation, or biological "
            "or metaphysical result.",
            "",
        ]
    )
    return "\n".join(lines)


def _validate_raw_cell_table(raw_table: Mapping[str, Any]) -> None:
    if _string_value(raw_table, "schema_version") != "1.0":
        raise ValueError("raw schema_version must be '1.0'")
    if _string_value(raw_table, "artifact_kind") != RAW_CELL_ARTIFACT_KIND:
        raise ValueError(f"raw artifact_kind must be {RAW_CELL_ARTIFACT_KIND!r}")
    if _string_value(raw_table, "epistemic_status") != "E":
        raise ValueError("raw epistemic_status must be 'E'")
    _require_exact_tuple(
        "raw task_ids", _string_tuple(raw_table, "task_ids"), EXPECTED_RAW_TASK_IDS
    )
    _require_exact_tuple("raw claim_ids", _string_tuple(raw_table, "claim_ids"), EXPECTED_CLAIM_IDS)
    _require_exact_tuple(
        "raw source_ids", _string_tuple(raw_table, "source_ids"), EXPECTED_SOURCE_IDS
    )
    _require_exact_tuple(
        "raw assumption_ids",
        _string_tuple(raw_table, "assumption_ids"),
        EXPECTED_ASSUMPTION_IDS,
    )
    if _string_value(raw_table, "grid_version") != EXPECTED_GRID_VERSION:
        raise ValueError(f"raw grid_version must be {EXPECTED_GRID_VERSION!r}")

    cells = _list_value(raw_table, "cells")
    raw_cell_count = _int_value(raw_table, "raw_cell_count")
    if raw_cell_count != len(cells):
        raise ValueError("raw_cell_count must match the number of cells")
    if raw_cell_count <= 0:
        raise ValueError("raw_cell_count must be positive")

    engine_scope = _mapping_value(raw_table, "engine_scope")
    if _string_value(engine_scope, "result_level") != "raw_cells_only":
        raise ValueError("raw engine_scope.result_level must be 'raw_cells_only'")
    if _bool_value(engine_scope, "aggregate_report"):
        raise ValueError("raw engine_scope.aggregate_report must be false")
    if _bool_value(engine_scope, "full_grid_run"):
        raise ValueError("raw engine_scope.full_grid_run must be false")

    grid_semantics = _mapping_value(raw_table, "grid_semantics")
    if (
        _string_value(grid_semantics, "aggregate_label_reserved_for_future_summaries")
        != EXPECTED_AGGREGATE_LABEL
    ):
        raise ValueError("raw aggregate label reservation is not grid_frequency")
    if _string_value(grid_semantics, "denominator_policy") != EXPECTED_DENOMINATOR_POLICY:
        raise ValueError(f"raw denominator_policy must be {EXPECTED_DENOMINATOR_POLICY!r}")
    if _bool_value(grid_semantics, "theorem_probability_claim"):
        raise ValueError("raw theorem_probability_claim must be false")

    seen_cell_ids: set[str] = set()
    for raw_cell in cells:
        cell = _mapping_item(raw_cell, "cells")
        cell_id = _string_value(cell, "cell_id")
        if cell_id in seen_cell_ids:
            raise ValueError(f"duplicate raw cell_id: {cell_id}")
        seen_cell_ids.add(cell_id)
        _string_value(cell, "status")


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


def _string_value(data: Mapping[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be a non-empty string")
    return value


def _string_tuple(data: Mapping[str, Any], key: str) -> tuple[str, ...]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        raise ValueError(f"{key} must be a non-empty list")
    strings: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item:
            raise ValueError(f"{key} must contain non-empty strings")
        strings.append(item)
    if len(set(strings)) != len(strings):
        raise ValueError(f"{key} must not contain duplicates")
    return tuple(strings)


def _int_value(data: Mapping[str, Any], key: str) -> int:
    value = data.get(key)
    if not isinstance(value, int):
        raise ValueError(f"{key} must be an integer")
    return value


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
