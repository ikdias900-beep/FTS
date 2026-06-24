from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from fts_lab.doctor import check_required_context_files, find_project_root
from fts_lab.manifests import ManifestError, read_json_object, validate_manifest_file
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


def test_manifest_validation_fails_after_artifact_corruption() -> None:
    root = find_project_root()
    result = run_smoke(command="test smoke corrupt")
    manifest_path = Path(result["manifest_path"])
    manifest = read_json_object(manifest_path)
    payload_path = Path(manifest["outputs"][0]["path"])
    payload_path.write_bytes(payload_path.read_bytes() + b"\n")

    with pytest.raises(ManifestError, match="Checksum mismatch"):
        validate_manifest_file(manifest_path, project_root=root)


def test_context_file_checker_detects_missing_required_file(tmp_path: Path) -> None:
    context = check_required_context_files(tmp_path)

    assert context["AGENTS.md"] is False
    assert any(not exists for exists in context.values())
