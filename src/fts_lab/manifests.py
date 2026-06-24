"""Manifest and checksum helpers for reproducible infrastructure runs."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Final, cast

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError as JsonSchemaValidationError

type JsonObject = dict[str, Any]

ALLOWED_EPISTEMIC_STATUSES: Final = {"R", "C", "E", "A"}
INFRASTRUCTURE_SMOKE_KIND: Final = "infrastructure_smoke"
SCHEMA_PATH: Final = Path("experiments/schemas/experiment_manifest.schema.json")


class ManifestError(ValueError):
    """Raised when a manifest violates project rules."""


def canonical_json_text(value: object) -> str:
    """Return deterministic JSON text for hashing and persisted payloads."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_json_bytes(value: object) -> bytes:
    """Return deterministic UTF-8 JSON bytes."""
    return canonical_json_text(value).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    """Return SHA-256 hex digest for exact bytes."""
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    """Return SHA-256 hex digest for a file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json_object(path: Path) -> JsonObject:
    """Read a JSON object from disk."""
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ManifestError(f"Expected JSON object in {path}")
    return cast(JsonObject, value)


def write_immutable_bytes(path: Path, data: bytes, *, overwrite: bool = False) -> None:
    """Write bytes and refuse to overwrite by default."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        raise FileExistsError(f"Refusing to overwrite existing artifact: {path}")
    path.write_bytes(data)


def write_immutable_json(path: Path, value: object, *, overwrite: bool = False) -> None:
    """Write canonical JSON bytes and refuse to overwrite by default."""
    write_immutable_bytes(path, canonical_json_bytes(value), overwrite=overwrite)


def normalize_relative_path(path: str | Path, base: str | Path) -> str:
    """Normalize equivalent paths consistently relative to a base directory when possible."""
    base_path = Path(base).resolve()
    path_value = Path(path)
    resolved = (
        path_value.resolve() if path_value.is_absolute() else (base_path / path_value).resolve()
    )
    try:
        return resolved.relative_to(base_path).as_posix()
    except ValueError:
        return resolved.as_posix()


def load_manifest_schema(project_root: Path) -> JsonObject:
    """Load the repository manifest JSON Schema."""
    return read_json_object(project_root / SCHEMA_PATH)


def validate_manifest_rules(manifest: Mapping[str, Any]) -> None:
    """Validate project-specific traceability rules not expressible enough in JSON Schema."""
    artifact_kind = manifest.get("artifact_kind")
    epistemic_status = manifest.get("epistemic_status")
    claim_ids = _list_value(manifest, "claim_ids")
    source_ids = _list_value(manifest, "source_ids")
    assumption_ids = _list_value(manifest, "assumption_ids")

    if epistemic_status is not None and epistemic_status not in ALLOWED_EPISTEMIC_STATUSES:
        raise ManifestError(f"Unknown epistemic status: {epistemic_status!r}")

    if artifact_kind == INFRASTRUCTURE_SMOKE_KIND:
        if epistemic_status is not None:
            raise ManifestError("Infrastructure smoke artifacts must use epistemic_status null")
        if claim_ids or source_ids or assumption_ids:
            raise ManifestError(
                "Infrastructure smoke artifacts must not link claims, sources, or assumptions"
            )
        return

    if epistemic_status is None:
        raise ManifestError("Only infrastructure smoke artifacts may use epistemic_status null")
    if not claim_ids:
        raise ManifestError("Scientific manifests must include at least one claim_id")
    if not source_ids:
        raise ManifestError("Scientific manifests must include at least one source_id")


def validate_manifest_data(manifest: Mapping[str, Any], project_root: Path) -> None:
    """Validate a manifest object against JSON Schema and project rules."""
    schema = load_manifest_schema(project_root)
    validator = Draft202012Validator(schema)
    try:
        validator.validate(manifest)
    except JsonSchemaValidationError as exc:
        raise ManifestError(exc.message) from exc
    validate_manifest_rules(manifest)


def validate_manifest_file(
    path: Path,
    *,
    project_root: Path,
    check_artifacts: bool = True,
) -> JsonObject:
    """Validate a manifest file and optionally verify referenced artifact checksums."""
    manifest = read_json_object(path)
    validate_manifest_data(manifest, project_root)
    if check_artifacts:
        for section in ("inputs", "outputs"):
            for item in _artifact_items(manifest, section):
                artifact_path = _resolve_artifact_path(item["path"], project_root)
                if not artifact_path.is_file():
                    raise ManifestError(f"Referenced artifact is missing: {artifact_path}")
                actual = sha256_file(artifact_path)
                expected = item["sha256"]
                if actual != expected:
                    raise ManifestError(
                        f"Checksum mismatch for {artifact_path}: expected {expected}, got {actual}"
                    )
    return manifest


def _list_value(manifest: Mapping[str, Any], key: str) -> list[Any]:
    value = manifest.get(key)
    if not isinstance(value, list):
        return []
    return value


def _artifact_items(manifest: Mapping[str, Any], section: str) -> list[dict[str, str]]:
    value = manifest.get(section)
    if not isinstance(value, list):
        raise ManifestError(f"Manifest section {section!r} must be a list")
    items: list[dict[str, str]] = []
    for item in value:
        if not isinstance(item, dict):
            raise ManifestError(f"Manifest section {section!r} contains a non-object item")
        path = item.get("path")
        checksum = item.get("sha256")
        if not isinstance(path, str) or not isinstance(checksum, str):
            raise ManifestError(f"Manifest section {section!r} contains an invalid path/checksum")
        items.append({"path": path, "sha256": checksum})
    return items


def _resolve_artifact_path(path: str, project_root: Path) -> Path:
    artifact_path = Path(path)
    if artifact_path.is_absolute():
        return artifact_path
    return project_root / artifact_path
