from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from fts_lab.doctor import check_required_context_files, find_project_root
from fts_lab.manifests import (
    ManifestError,
    read_json_object,
    validate_manifest_file,
    write_immutable_json,
)
from fts_lab.smoke import run_smoke


def test_doctor_succeeds_in_valid_checkout() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "fts_lab.cli", "doctor"],
        cwd=find_project_root(),
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Active task: TASK-000" in result.stdout


def test_smoke_run_writes_payload_and_valid_manifest() -> None:
    root = find_project_root()
    result = run_smoke(command="test smoke")
    payload_path = Path(result["payload_path"])
    manifest_path = Path(result["manifest_path"])

    assert payload_path.is_file()
    assert manifest_path.is_file()
    manifest = validate_manifest_file(manifest_path, project_root=root)
    assert manifest["artifact_kind"] == "infrastructure_smoke"
    assert manifest["epistemic_status"] is None
    assert manifest["claim_ids"] == []
    assert result["payload_checksum"] == manifest["outputs"][0]["sha256"]


def test_two_smoke_runs_have_identical_payload_checksums() -> None:
    first = run_smoke(command="test smoke one")
    second = run_smoke(command="test smoke two")

    assert first["payload_checksum"] == second["payload_checksum"]


def test_cli_records_documented_smoke_command() -> None:
    root = find_project_root()
    result = subprocess.run(
        [sys.executable, "-m", "fts_lab.cli", "reproduce-smoke"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    manifest_path = _manifest_path_from_output(result.stdout)
    manifest = read_json_object(manifest_path)

    assert result.returncode == 0, result.stdout + result.stderr
    assert manifest["command"] == "uv run fts reproduce-smoke"


def test_manifest_validation_fails_after_artifact_corruption(tmp_path: Path) -> None:
    root = find_project_root()
    result = run_smoke(command="test smoke corrupt")
    manifest_path = Path(result["manifest_path"])
    manifest = read_json_object(manifest_path)
    payload_path = tmp_path / "payload-copy.json"
    copied_manifest_path = tmp_path / "manifest-copy.json"
    shutil.copy2(Path(manifest["outputs"][0]["path"]), payload_path)
    manifest["outputs"][0]["path"] = str(payload_path)
    write_immutable_json(copied_manifest_path, manifest)
    payload_path.write_bytes(payload_path.read_bytes() + b"\n")

    with pytest.raises(ManifestError, match="Checksum mismatch"):
        validate_manifest_file(copied_manifest_path, project_root=root)


def test_context_file_checker_detects_missing_required_file(tmp_path: Path) -> None:
    context = check_required_context_files(tmp_path)

    assert context["AGENTS.md"] is False
    assert any(not exists for exists in context.values())


def _manifest_path_from_output(output: str) -> Path:
    for line in output.splitlines():
        if line.startswith("manifest_path="):
            return Path(line.removeprefix("manifest_path="))
    raise AssertionError(f"manifest path not found in output: {output}")
