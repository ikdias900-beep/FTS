"""Manifest-backed finite sweeps for FFF Stage 1 tables."""

from __future__ import annotations

import csv
import io
import platform
import sys
import uuid
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path
from typing import Any

from fts_lab import __version__
from fts_lab.doctor import find_project_root, git_state
from fts_lab.fff.admissibility import admissible_count
from fts_lab.fff.cyclic_groups import (
    count_admissible_cyclic_homomorphisms_by_enumeration,
    cyclic_homomorphism_count_formula,
)
from fts_lab.fff.formulas import (
    source_cyclic_homomorphism_ratio,
    source_total_order_witness_ratio,
    unique_total_order_homomorphism_ratio,
)
from fts_lab.fff.total_orders import (
    source_total_order_witness_count,
    unique_total_order_homomorphism_count,
)
from fts_lab.manifests import (
    read_json_object,
    sha256_bytes,
    sha256_file,
    validate_manifest_file,
    write_immutable_bytes,
    write_immutable_json,
)

SWEEP_ARTIFACT_KIND = "fff_stage1_finite_count_sweep"
EXPECTED_TASK_IDS = ("TASK-001-SWEEP",)
EXPECTED_CLAIM_IDS = (
    "CLM-FFF-ADM-001",
    "CLM-FFF-ORD-001",
    "CLM-FFF-CYC-001",
    "CLM-FFF-CYC-002",
)
EXPECTED_SOURCE_IDS = ("SRC-FFF-2020",)
EXPECTED_ASSUMPTION_IDS = ("ASM-FFF-0001",)
CSV_FILENAME = "fff_stage1_counts.csv"
CSV_FIELDNAMES = (
    "schema_version",
    "task_id",
    "row_epistemic_status",
    "claim_id",
    "source_id",
    "assumption_ids",
    "structure",
    "metric",
    "count_object",
    "domain_size",
    "codomain_size",
    "numerator",
    "denominator",
    "value_label",
    "notes",
)


@dataclass(frozen=True)
class SweepConfig:
    """Validated Stage 1 sweep configuration."""

    path: Path
    artifact_kind: str
    epistemic_status: str
    task_ids: tuple[str, ...]
    claim_ids: tuple[str, ...]
    source_ids: tuple[str, ...]
    assumption_ids: tuple[str, ...]
    domain_sizes: tuple[int, ...]
    codomain_sizes: tuple[int, ...]
    include_admissible_cyclic_audit: bool
    notes: str


def run_stage1_sweep(
    config_path: Path | None = None, *, command: str | None = None
) -> dict[str, str]:
    """Run the deterministic Stage 1 finite count sweep."""
    root = find_project_root()
    config_file = (config_path or root / "experiments/configs/fff_stage1_small.json").resolve()
    config = load_sweep_config(config_file)
    rows = build_stage1_sweep_rows(config)
    csv_bytes = render_sweep_csv(rows)
    csv_checksum = sha256_bytes(csv_bytes)

    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    suffix = uuid.uuid4().hex[:8].upper()
    run_id = f"EXP-TASK-001-SWEEP-{timestamp}-{suffix}"
    manifest_id = f"ART-TASK-001-SWEEP-MANIFEST-{timestamp}-{suffix}"
    output_dir = root / "results/raw" / run_id
    csv_path = output_dir / CSV_FILENAME
    manifest_path = root / "experiments/manifests" / f"{manifest_id}.json"

    write_immutable_bytes(csv_path, csv_bytes)

    lockfile = root / "uv.lock"
    if not lockfile.is_file():
        raise FileNotFoundError("uv.lock is required before writing a sweep manifest")

    manifest: dict[str, Any] = {
        "schema_version": "1.0",
        "manifest_id": manifest_id,
        "run_id": run_id,
        "artifact_kind": config.artifact_kind,
        "epistemic_status": config.epistemic_status,
        "task_ids": list(config.task_ids),
        "claim_ids": list(config.claim_ids),
        "source_ids": list(config.source_ids),
        "assumption_ids": list(config.assumption_ids),
        "created_at_utc": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "command": command or " ".join(sys.argv),
        "parameters": {
            "config_path": str(config_file),
            "domain_sizes": list(config.domain_sizes),
            "codomain_sizes": list(config.codomain_sizes),
            "include_admissible_cyclic_audit": config.include_admissible_cyclic_audit,
            "row_count": len(rows),
        },
        "seed": None,
        "git": git_state(root),
        "environment": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "dependency_lock_sha256": sha256_file(lockfile),
        },
        "inputs": [{"path": str(config_file), "sha256": sha256_file(config_file)}],
        "outputs": [{"path": str(csv_path), "sha256": csv_checksum}],
        "status": "completed",
        "error": None,
        "implementation": {"package": "fts-lab", "version": __version__},
    }
    write_immutable_json(manifest_path, manifest)
    validate_manifest_file(manifest_path, project_root=root)

    return {
        "csv_checksum": csv_checksum,
        "csv_path": str(csv_path),
        "manifest_path": str(manifest_path),
        "run_id": run_id,
        "row_count": str(len(rows)),
    }


def load_sweep_config(path: Path) -> SweepConfig:
    """Load and validate a Stage 1 sweep config."""
    data = read_json_object(path)
    artifact_kind = _string_value(data, "artifact_kind")
    if artifact_kind != SWEEP_ARTIFACT_KIND:
        raise ValueError(f"artifact_kind must be {SWEEP_ARTIFACT_KIND!r}")
    epistemic_status = _string_value(data, "epistemic_status")
    if epistemic_status != "C":
        raise ValueError("Stage 1 sweep artifact must use epistemic_status 'C'")

    task_ids = _string_tuple(data, "task_ids", min_items=1)
    claim_ids = _string_tuple(data, "claim_ids", min_items=1)
    source_ids = _string_tuple(data, "source_ids", min_items=1)
    assumption_ids = _string_tuple(data, "assumption_ids", min_items=1)
    _require_exact_tuple("task_ids", task_ids, EXPECTED_TASK_IDS)
    _require_exact_tuple("claim_ids", claim_ids, EXPECTED_CLAIM_IDS)
    _require_exact_tuple("source_ids", source_ids, EXPECTED_SOURCE_IDS)
    _require_exact_tuple("assumption_ids", assumption_ids, EXPECTED_ASSUMPTION_IDS)

    return SweepConfig(
        path=path,
        artifact_kind=artifact_kind,
        epistemic_status=epistemic_status,
        task_ids=task_ids,
        claim_ids=claim_ids,
        source_ids=source_ids,
        assumption_ids=assumption_ids,
        domain_sizes=_positive_int_tuple(data, "domain_sizes"),
        codomain_sizes=_positive_int_tuple(data, "codomain_sizes"),
        include_admissible_cyclic_audit=_bool_value(data, "include_admissible_cyclic_audit"),
        notes=_string_value(data, "notes"),
    )


def build_stage1_sweep_rows(config: SweepConfig) -> list[dict[str, str]]:
    """Build deterministic long-form Stage 1 count rows."""
    rows: list[dict[str, str]] = []
    for domain_size in config.domain_sizes:
        for codomain_size in config.codomain_sizes:
            rows.extend(_rows_for_pair(config, domain_size, codomain_size))
    return rows


def render_sweep_csv(rows: Iterable[dict[str, str]]) -> bytes:
    """Render deterministic UTF-8 CSV bytes."""
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=CSV_FIELDNAMES, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    return buffer.getvalue().encode("utf-8")


def _rows_for_pair(
    config: SweepConfig,
    domain_size: int,
    codomain_size: int,
) -> list[dict[str, str]]:
    admissible = admissible_count(domain_size, codomain_size)
    source_order_count = source_total_order_witness_count(domain_size, codomain_size)
    unique_order_count = unique_total_order_homomorphism_count(domain_size, codomain_size)
    cyclic_count = cyclic_homomorphism_count_formula(domain_size, codomain_size)
    rows = [
        _row(
            config,
            row_epistemic_status="R",
            claim_id="CLM-FFF-ADM-001",
            structure="admissibility",
            metric="count",
            count_object="admissible_payoff_functions",
            domain_size=domain_size,
            codomain_size=codomain_size,
            value=Fraction(admissible, 1),
            notes="source admissible payoff-function count",
        ),
        _row(
            config,
            row_epistemic_status="R",
            claim_id="CLM-FFF-ORD-001",
            structure="total_order",
            metric="count",
            count_object="source_orientation_witnesses",
            domain_size=domain_size,
            codomain_size=codomain_size,
            value=Fraction(source_order_count, 1),
            notes="source formula 2 * binom(n + m - 2, m - 1)",
        ),
        _row(
            config,
            row_epistemic_status="R",
            claim_id="CLM-FFF-ORD-001",
            structure="total_order",
            metric="ratio",
            count_object="source_orientation_witnesses_over_admissible",
            domain_size=domain_size,
            codomain_size=codomain_size,
            value=source_total_order_witness_ratio(domain_size, codomain_size),
            notes="source orientation-witness count divided by admissible payoff functions",
        ),
        _row(
            config,
            row_epistemic_status="C",
            claim_id="CLM-FFF-ORD-001",
            structure="total_order",
            metric="count",
            count_object="distinct_unique_functions",
            domain_size=domain_size,
            codomain_size=codomain_size,
            value=Fraction(unique_order_count, 1),
            notes="RDR-0002 presentation companion; not the source formula",
        ),
        _row(
            config,
            row_epistemic_status="C",
            claim_id="CLM-FFF-ORD-001",
            structure="total_order",
            metric="ratio",
            count_object="distinct_unique_functions_over_admissible",
            domain_size=domain_size,
            codomain_size=codomain_size,
            value=unique_total_order_homomorphism_ratio(domain_size, codomain_size),
            notes="RDR-0002 presentation companion; not the source formula",
        ),
        _row(
            config,
            row_epistemic_status="R",
            claim_id="CLM-FFF-CYC-001",
            structure="cyclic_group",
            metric="count",
            count_object="source_cyclic_homomorphisms",
            domain_size=domain_size,
            codomain_size=codomain_size,
            value=Fraction(cyclic_count, 1),
            notes="source formula gcd(n, m)",
        ),
        _row(
            config,
            row_epistemic_status="R",
            claim_id="CLM-FFF-CYC-002",
            structure="cyclic_group",
            metric="ratio",
            count_object="source_cyclic_homomorphisms_over_admissible",
            domain_size=domain_size,
            codomain_size=codomain_size,
            value=source_cyclic_homomorphism_ratio(domain_size, codomain_size),
            notes="source cyclic count divided by admissible payoff functions",
        ),
    ]
    if config.include_admissible_cyclic_audit:
        audit_count = count_admissible_cyclic_homomorphisms_by_enumeration(
            domain_size,
            codomain_size,
        )
        rows.append(
            _row(
                config,
                row_epistemic_status="C",
                claim_id="CLM-FFF-CYC-001",
                structure="cyclic_group",
                metric="count",
                count_object="admissible_cyclic_homomorphisms_audit",
                domain_size=domain_size,
                codomain_size=codomain_size,
                value=Fraction(audit_count, 1),
                notes="audit aid after admissibility filtering; not the source numerator",
            )
        )
    return rows


def _row(
    config: SweepConfig,
    *,
    row_epistemic_status: str,
    claim_id: str,
    structure: str,
    metric: str,
    count_object: str,
    domain_size: int,
    codomain_size: int,
    value: Fraction,
    notes: str,
) -> dict[str, str]:
    return {
        "schema_version": "1.0",
        "task_id": config.task_ids[0],
        "row_epistemic_status": row_epistemic_status,
        "claim_id": claim_id,
        "source_id": config.source_ids[0],
        "assumption_ids": ";".join(config.assumption_ids) if row_epistemic_status == "C" else "",
        "structure": structure,
        "metric": metric,
        "count_object": count_object,
        "domain_size": str(domain_size),
        "codomain_size": str(codomain_size),
        "numerator": str(value.numerator),
        "denominator": str(value.denominator),
        "value_label": _value_label(value),
        "notes": notes,
    }


def _value_label(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _string_value(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be a non-empty string")
    return value


def _bool_value(data: dict[str, Any], key: str) -> bool:
    value = data.get(key)
    if not isinstance(value, bool):
        raise ValueError(f"{key} must be a boolean")
    return value


def _string_tuple(data: dict[str, Any], key: str, *, min_items: int) -> tuple[str, ...]:
    value = data.get(key)
    if not isinstance(value, list) or len(value) < min_items:
        raise ValueError(f"{key} must be a non-empty list")
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


def _positive_int_tuple(data: dict[str, Any], key: str) -> tuple[int, ...]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        raise ValueError(f"{key} must be a non-empty list")
    integers: list[int] = []
    for item in value:
        if not isinstance(item, int) or item <= 0:
            raise ValueError(f"{key} must contain positive integers")
        integers.append(item)
    if len(set(integers)) != len(integers):
        raise ValueError(f"{key} must not contain duplicates")
    return tuple(integers)
