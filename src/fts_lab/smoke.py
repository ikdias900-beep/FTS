"""Deterministic infrastructure smoke run for TASK-000."""

from __future__ import annotations

import platform
import sys
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fts_lab import __version__
from fts_lab.doctor import find_project_root, git_state
from fts_lab.manifests import (
    INFRASTRUCTURE_SMOKE_KIND,
    canonical_json_bytes,
    read_json_object,
    sha256_bytes,
    sha256_file,
    validate_manifest_file,
    write_immutable_json,
)


def run_smoke(config_path: Path | None = None, *, command: str | None = None) -> dict[str, str]:
    """Run the deterministic infrastructure smoke operation."""
    root = find_project_root()
    config = (config_path or root / "experiments/configs/smoke.json").resolve()
    config_data = read_json_object(config)
    values = _read_integer_values(config_data)

    payload = {
        "schema_version": "1.0",
        "count": len(values),
        "total": sum(values),
        "minimum": min(values),
        "maximum": max(values),
        "input_sha256": sha256_file(config),
        "values_sha256": sha256_bytes(canonical_json_bytes(values)),
    }
    payload_checksum = sha256_bytes(canonical_json_bytes(payload))

    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    suffix = uuid.uuid4().hex[:8].upper()
    run_id = f"EXP-TASK-000-SMOKE-{timestamp}-{suffix}"
    manifest_id = f"ART-TASK-000-SMOKE-MANIFEST-{timestamp}-{suffix}"
    output_dir = root / "results/raw" / run_id
    payload_path = output_dir / "payload.json"
    manifest_path = root / "experiments/manifests" / f"{manifest_id}.json"

    write_immutable_json(payload_path, payload)

    lockfile = root / "uv.lock"
    if not lockfile.is_file():
        raise FileNotFoundError("uv.lock is required before writing a smoke manifest")

    manifest: dict[str, Any] = {
        "schema_version": "1.0",
        "manifest_id": manifest_id,
        "run_id": run_id,
        "artifact_kind": INFRASTRUCTURE_SMOKE_KIND,
        "epistemic_status": None,
        "task_ids": ["TASK-000"],
        "claim_ids": [],
        "source_ids": [],
        "assumption_ids": [],
        "created_at_utc": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "command": command or " ".join(sys.argv),
        "parameters": {
            "config_path": str(config),
            "value_count": len(values),
        },
        "seed": None,
        "git": git_state(root),
        "environment": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "dependency_lock_sha256": sha256_file(lockfile),
        },
        "inputs": [{"path": str(config), "sha256": sha256_file(config)}],
        "outputs": [{"path": str(payload_path), "sha256": payload_checksum}],
        "status": "completed",
        "error": None,
        "implementation": {"package": "fts-lab", "version": __version__},
    }
    write_immutable_json(manifest_path, manifest)
    validate_manifest_file(manifest_path, project_root=root)

    return {
        "payload_checksum": payload_checksum,
        "payload_path": str(payload_path),
        "manifest_path": str(manifest_path),
        "run_id": run_id,
    }


def _read_integer_values(config_data: dict[str, Any]) -> list[int]:
    values = config_data.get("values")
    if not isinstance(values, list) or not values:
        raise ValueError("smoke config must contain a non-empty values list")
    integers: list[int] = []
    for value in values:
        if not isinstance(value, int):
            raise ValueError("smoke config values must be integers")
        integers.append(value)
    return integers
