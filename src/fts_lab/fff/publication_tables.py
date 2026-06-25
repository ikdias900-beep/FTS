"""Derived publication tables for FFF Stage 1 finite counts."""

from __future__ import annotations

import csv
import io
import platform
import sys
import uuid
from collections.abc import Iterable, Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fts_lab import __version__
from fts_lab.doctor import find_project_root, git_state
from fts_lab.fff.sweeps import (
    CSV_FIELDNAMES,
    EXPECTED_ASSUMPTION_IDS,
    EXPECTED_CLAIM_IDS,
    EXPECTED_SOURCE_IDS,
    SWEEP_ARTIFACT_KIND,
)
from fts_lab.manifests import (
    ManifestError,
    sha256_bytes,
    sha256_file,
    validate_manifest_file,
    write_immutable_bytes,
    write_immutable_json,
)

PUBLICATION_TABLES_TASK_ID = "TASK-001-PUBTABLES"
PUBLICATION_TABLES_ARTIFACT_KIND = "fff_stage1_publication_tables"
SUMMARY_CSV_FILENAME = "stage1_fff_publication_counts.csv"
REPORT_FILENAME = "stage1_fff_publication_tables.md"

REQUIRED_COUNT_OBJECTS = (
    "admissible_payoff_functions",
    "source_orientation_witnesses",
    "source_orientation_witnesses_over_admissible",
    "distinct_unique_functions",
    "distinct_unique_functions_over_admissible",
    "source_cyclic_homomorphisms",
    "source_cyclic_homomorphisms_over_admissible",
)

SUMMARY_FIELDNAMES = (
    "schema_version",
    "task_id",
    "source_sweep_run_id",
    "source_sweep_manifest_id",
    "domain_size",
    "codomain_size",
    "admissible_count",
    "admissible_status",
    "total_order_source_orientation_witness_count",
    "total_order_source_orientation_witness_ratio",
    "total_order_source_orientation_witness_status",
    "total_order_distinct_unique_function_count",
    "total_order_distinct_unique_function_ratio",
    "total_order_distinct_unique_function_status",
    "cyclic_source_homomorphism_count",
    "cyclic_source_homomorphism_ratio",
    "cyclic_source_homomorphism_status",
    "claim_ids",
    "source_ids",
    "assumption_ids",
    "notes",
)


def run_stage1_publication_tables(
    sweep_manifest_path: Path, *, command: str | None = None
) -> dict[str, str]:
    """Build derived publication-ready Stage 1 tables from a sweep manifest."""
    root = find_project_root()
    resolved_manifest_path = sweep_manifest_path.resolve()
    sweep_manifest = validate_manifest_file(resolved_manifest_path, project_root=root)
    _validate_sweep_manifest(sweep_manifest)

    sweep_csv_path = _resolve_artifact_path(_first_output_path(sweep_manifest), root)
    sweep_rows = read_sweep_csv(sweep_csv_path)
    summary_rows = build_publication_summary_rows(sweep_rows, sweep_manifest)
    summary_csv_bytes = render_summary_csv(summary_rows)
    report_bytes = render_publication_report(
        summary_rows,
        sweep_manifest=sweep_manifest,
        sweep_manifest_path=resolved_manifest_path,
        sweep_csv_path=sweep_csv_path,
    ).encode("utf-8")

    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    suffix = uuid.uuid4().hex[:8].upper()
    run_id = f"EXP-TASK-001-PUBTABLES-{timestamp}-{suffix}"
    manifest_id = f"ART-TASK-001-PUBTABLES-MANIFEST-{timestamp}-{suffix}"
    derived_dir = root / "results/derived" / run_id
    reports_dir = root / "results/reports" / run_id
    summary_csv_path = derived_dir / SUMMARY_CSV_FILENAME
    report_path = reports_dir / REPORT_FILENAME
    manifest_path = root / "experiments/manifests" / f"{manifest_id}.json"

    write_immutable_bytes(summary_csv_path, summary_csv_bytes)
    write_immutable_bytes(report_path, report_bytes)

    lockfile = root / "uv.lock"
    if not lockfile.is_file():
        raise FileNotFoundError("uv.lock is required before writing a publication manifest")

    summary_checksum = sha256_bytes(summary_csv_bytes)
    report_checksum = sha256_bytes(report_bytes)
    manifest: dict[str, Any] = {
        "schema_version": "1.0",
        "manifest_id": manifest_id,
        "run_id": run_id,
        "artifact_kind": PUBLICATION_TABLES_ARTIFACT_KIND,
        "epistemic_status": "C",
        "task_ids": [PUBLICATION_TABLES_TASK_ID],
        "claim_ids": list(EXPECTED_CLAIM_IDS),
        "source_ids": list(EXPECTED_SOURCE_IDS),
        "assumption_ids": list(EXPECTED_ASSUMPTION_IDS),
        "created_at_utc": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "command": command or " ".join(sys.argv),
        "parameters": {
            "sweep_manifest_path": str(resolved_manifest_path),
            "source_sweep_manifest_id": _manifest_string(sweep_manifest, "manifest_id"),
            "source_sweep_run_id": _manifest_string(sweep_manifest, "run_id"),
            "input_row_count": len(sweep_rows),
            "output_row_count": len(summary_rows),
            "summary_csv_filename": SUMMARY_CSV_FILENAME,
            "report_filename": REPORT_FILENAME,
        },
        "seed": None,
        "git": git_state(root),
        "environment": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "dependency_lock_sha256": sha256_file(lockfile),
        },
        "inputs": [
            {"path": str(resolved_manifest_path), "sha256": sha256_file(resolved_manifest_path)},
            {"path": str(sweep_csv_path), "sha256": sha256_file(sweep_csv_path)},
        ],
        "outputs": [
            {"path": str(summary_csv_path), "sha256": summary_checksum},
            {"path": str(report_path), "sha256": report_checksum},
        ],
        "status": "completed",
        "error": None,
        "implementation": {"package": "fts-lab", "version": __version__},
    }
    write_immutable_json(manifest_path, manifest)
    validate_manifest_file(manifest_path, project_root=root)

    return {
        "manifest_path": str(manifest_path),
        "report_checksum": report_checksum,
        "report_path": str(report_path),
        "row_count": str(len(summary_rows)),
        "run_id": run_id,
        "summary_csv_checksum": summary_checksum,
        "summary_csv_path": str(summary_csv_path),
    }


def read_sweep_csv(path: Path) -> list[dict[str, str]]:
    """Read a Stage 1 sweep CSV and validate its header."""
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != list(CSV_FIELDNAMES):
            raise ValueError(f"Unexpected sweep CSV fieldnames: {reader.fieldnames!r}")
        return [dict(row) for row in reader]


def build_publication_summary_rows(
    sweep_rows: Iterable[Mapping[str, str]],
    sweep_manifest: Mapping[str, Any],
) -> list[dict[str, str]]:
    """Build wide exact table rows while preserving per-column epistemic statuses."""
    source_run_id = _manifest_string(sweep_manifest, "run_id")
    source_manifest_id = _manifest_string(sweep_manifest, "manifest_id")
    grouped: dict[tuple[int, int], dict[str, Mapping[str, str]]] = {}
    order: list[tuple[int, int]] = []

    for row in sweep_rows:
        count_object = _row_value(row, "count_object")
        if count_object not in REQUIRED_COUNT_OBJECTS:
            raise ValueError(f"Unexpected count_object in canonical sweep: {count_object!r}")
        key = (int(_row_value(row, "domain_size")), int(_row_value(row, "codomain_size")))
        if key not in grouped:
            grouped[key] = {}
            order.append(key)
        if count_object in grouped[key]:
            raise ValueError(f"Duplicate count_object {count_object!r} for n,m={key!r}")
        grouped[key][count_object] = row

    summary_rows: list[dict[str, str]] = []
    for domain_size, codomain_size in order:
        rows_for_pair = grouped[(domain_size, codomain_size)]
        missing = sorted(set(REQUIRED_COUNT_OBJECTS) - set(rows_for_pair))
        if missing:
            raise ValueError(
                f"Missing count objects for n,m={(domain_size, codomain_size)!r}: {missing}"
            )

        admissible = rows_for_pair["admissible_payoff_functions"]
        order_source_count = rows_for_pair["source_orientation_witnesses"]
        order_source_ratio = rows_for_pair["source_orientation_witnesses_over_admissible"]
        order_unique_count = rows_for_pair["distinct_unique_functions"]
        order_unique_ratio = rows_for_pair["distinct_unique_functions_over_admissible"]
        cyclic_count = rows_for_pair["source_cyclic_homomorphisms"]
        cyclic_ratio = rows_for_pair["source_cyclic_homomorphisms_over_admissible"]

        summary_rows.append(
            {
                "schema_version": "1.0",
                "task_id": PUBLICATION_TABLES_TASK_ID,
                "source_sweep_run_id": source_run_id,
                "source_sweep_manifest_id": source_manifest_id,
                "domain_size": str(domain_size),
                "codomain_size": str(codomain_size),
                "admissible_count": _row_value(admissible, "value_label"),
                "admissible_status": _row_value(admissible, "row_epistemic_status"),
                "total_order_source_orientation_witness_count": _row_value(
                    order_source_count,
                    "value_label",
                ),
                "total_order_source_orientation_witness_ratio": _row_value(
                    order_source_ratio,
                    "value_label",
                ),
                "total_order_source_orientation_witness_status": _row_value(
                    order_source_count,
                    "row_epistemic_status",
                ),
                "total_order_distinct_unique_function_count": _row_value(
                    order_unique_count,
                    "value_label",
                ),
                "total_order_distinct_unique_function_ratio": _row_value(
                    order_unique_ratio,
                    "value_label",
                ),
                "total_order_distinct_unique_function_status": _row_value(
                    order_unique_count,
                    "row_epistemic_status",
                ),
                "cyclic_source_homomorphism_count": _row_value(cyclic_count, "value_label"),
                "cyclic_source_homomorphism_ratio": _row_value(cyclic_ratio, "value_label"),
                "cyclic_source_homomorphism_status": _row_value(
                    cyclic_count,
                    "row_epistemic_status",
                ),
                "claim_ids": ";".join(EXPECTED_CLAIM_IDS),
                "source_ids": ";".join(EXPECTED_SOURCE_IDS),
                "assumption_ids": ";".join(EXPECTED_ASSUMPTION_IDS),
                "notes": (
                    "finite grid row; per-column statuses preserve the R/C mixture; "
                    "not a biological probability distribution"
                ),
            }
        )
    return summary_rows


def render_summary_csv(rows: Iterable[dict[str, str]]) -> bytes:
    """Render deterministic UTF-8 CSV bytes for publication tables."""
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=SUMMARY_FIELDNAMES, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    return buffer.getvalue().encode("utf-8")


def render_publication_report(
    summary_rows: list[dict[str, str]],
    *,
    sweep_manifest: Mapping[str, Any],
    sweep_manifest_path: Path,
    sweep_csv_path: Path,
) -> str:
    """Render a human-readable exact table report."""
    manifest_id = _manifest_string(sweep_manifest, "manifest_id")
    run_id = _manifest_string(sweep_manifest, "run_id")
    lines = [
        "# Stage 1 FFF Publication Tables",
        "",
        "```text",
        f"TASK ID: {PUBLICATION_TABLES_TASK_ID}",
        "EPISTEMIC STATUS: C for this derived table package; per-column statuses preserved",
        "SOURCE IDS: SRC-FFF-2020",
        "CLAIM IDS: CLM-FFF-ADM-001, CLM-FFF-ORD-001, CLM-FFF-CYC-001, CLM-FFF-CYC-002",
        "ASSUMPTION IDS: ASM-FFF-0001",
        f"SOURCE SWEEP MANIFEST: {manifest_id}",
        f"SOURCE SWEEP RUN: {run_id}",
        "```",
        "",
        "## Scope",
        "",
        "This report formats the reviewed Stage 1 finite-count sweep for publication use. It "
        "does not add new mathematical definitions, new experiments, plots, web demos, or "
        "claims beyond the linked claim records.",
        "",
        "The table is a finite grid summary. It must not be interpreted as an empirical "
        "probability distribution over biological payoff functions.",
        "",
        "## Provenance",
        "",
        f"- Sweep manifest: `{sweep_manifest_path}`",
        f"- Sweep CSV: `{sweep_csv_path}`",
        "- Derived from exact integer counts and exact rational ratios; no floating-point "
        "values are used.",
        "",
        "## Status Legend",
        "",
        "- `R`: source reproduction column.",
        "- `C`: computational reconstruction/presentation companion column required by "
        "`ASM-FFF-0001` and `RDR-0002`.",
        "",
        "## Table",
        "",
        "| n | m | admissible count (R) | order witnesses (R) | order witness ratio (R) | "
        "unique order functions (C) | unique order ratio (C) | cyclic homomorphisms (R) | "
        "cyclic ratio (R) |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary_rows:
        lines.append(
            "| "
            f"{row['domain_size']} | "
            f"{row['codomain_size']} | "
            f"{row['admissible_count']} | "
            f"{row['total_order_source_orientation_witness_count']} | "
            f"{row['total_order_source_orientation_witness_ratio']} | "
            f"{row['total_order_distinct_unique_function_count']} | "
            f"{row['total_order_distinct_unique_function_ratio']} | "
            f"{row['cyclic_source_homomorphism_count']} | "
            f"{row['cyclic_source_homomorphism_ratio']} |"
        )
    lines.extend(
        [
            "",
            "## Allowed Claims",
            "",
            "- For the declared finite grid, this table reports exact source counts and exact "
            "ratios for admissible payoff functions, total-order source orientation witnesses, "
            "and cyclic-group homomorphisms.",
            "- Total-order distinct unique-function counts are shown beside the source "
            "orientation-witness counts as the approved `RDR-0002` presentation companion.",
            "",
            "## Forbidden Claims",
            "",
            "- Do not claim this table proves anything about human perception, consciousness, "
            "spacetime, or biological distributions of real payoff functions.",
            "- Do not describe finite grid frequencies as probabilities without an explicit "
            "measure.",
            "- Do not present the source total-order witness count as the distinct unique-function "
            "count.",
            "",
        ]
    )
    return "\n".join(lines)


def _validate_sweep_manifest(manifest: Mapping[str, Any]) -> None:
    if manifest.get("artifact_kind") != SWEEP_ARTIFACT_KIND:
        raise ManifestError(f"Expected sweep artifact kind {SWEEP_ARTIFACT_KIND!r}")
    if manifest.get("epistemic_status") != "C":
        raise ManifestError("Stage 1 sweep manifest must use epistemic_status 'C'")
    _require_manifest_list("claim_ids", manifest, EXPECTED_CLAIM_IDS)
    _require_manifest_list("source_ids", manifest, EXPECTED_SOURCE_IDS)
    _require_manifest_list("assumption_ids", manifest, EXPECTED_ASSUMPTION_IDS)


def _require_manifest_list(
    key: str,
    manifest: Mapping[str, Any],
    expected: tuple[str, ...],
) -> None:
    value = manifest.get(key)
    if value != list(expected):
        raise ManifestError(f"{key} must be exactly {list(expected)!r}")


def _first_output_path(manifest: Mapping[str, Any]) -> str:
    outputs = manifest.get("outputs")
    if not isinstance(outputs, list) or not outputs:
        raise ManifestError("sweep manifest must include at least one output")
    first = outputs[0]
    if not isinstance(first, dict):
        raise ManifestError("first sweep output must be an object")
    path = first.get("path")
    if not isinstance(path, str) or not path:
        raise ManifestError("first sweep output must include a path")
    return path


def _manifest_string(manifest: Mapping[str, Any], key: str) -> str:
    value = manifest.get(key)
    if not isinstance(value, str) or not value:
        raise ManifestError(f"manifest field {key!r} must be a non-empty string")
    return value


def _row_value(row: Mapping[str, str], key: str) -> str:
    value = row.get(key)
    if value is None:
        raise ValueError(f"row is missing {key!r}")
    return value


def _resolve_artifact_path(path: str, project_root: Path) -> Path:
    artifact_path = Path(path)
    if artifact_path.is_absolute():
        return artifact_path
    return project_root / artifact_path
