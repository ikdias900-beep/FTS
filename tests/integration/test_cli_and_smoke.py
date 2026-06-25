from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from fts_lab.doctor import check_required_context_files, find_project_root
from fts_lab.fff.sweeps import run_stage1_sweep
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
    assert "Active task: TASK-001-PUBTABLES" in result.stdout


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
    assert result.returncode == 0, result.stdout + result.stderr
    manifest_path = _manifest_path_from_output(result.stdout)
    manifest = read_json_object(manifest_path)

    assert result.returncode == 0, result.stdout + result.stderr
    assert manifest["command"] == "uv run fts reproduce-smoke"


@pytest.mark.parametrize(
    ("args", "expected_lines"),
    [
        (
            ["fff", "admissible-count", "2", "2"],
            ["claim_ids=CLM-FFF-ADM-001", "count=3"],
        ),
        (
            ["fff", "total-order-count", "2", "2"],
            [
                "claim_ids=CLM-FFF-ORD-001",
                "assumption_ids=ASM-FFF-0001",
                "mode=source-witness",
                "count=4",
                "ratio=4/3",
            ],
        ),
        (
            ["fff", "total-order-count", "2", "2", "--mode", "unique"],
            ["mode=unique", "count=3", "ratio=1/1"],
        ),
        (
            ["fff", "cyclic-count", "2", "2"],
            ["claim_ids=CLM-FFF-CYC-001,CLM-FFF-CYC-002", "mode=source", "count=2"],
        ),
        (
            ["fff", "cyclic-count", "2", "2", "--admissible-only"],
            ["mode=admissible-filtered-audit", "count=1"],
        ),
    ],
)
def test_fff_cli_commands_emit_traceable_counts(
    args: list[str],
    expected_lines: list[str],
) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "fts_lab.cli", *args],
        cwd=find_project_root(),
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "task_ids=TASK-001" in result.stdout
    assert "source_ids=SRC-FFF-2020" in result.stdout
    for expected_line in expected_lines:
        assert expected_line in result.stdout


def test_stage1_sweep_writes_csv_and_valid_manifest() -> None:
    root = find_project_root()
    result = run_stage1_sweep(command="test fff sweep")
    csv_path = Path(result["csv_path"])
    manifest_path = Path(result["manifest_path"])

    assert csv_path.is_file()
    assert manifest_path.is_file()
    manifest = validate_manifest_file(manifest_path, project_root=root)
    assert manifest["artifact_kind"] == "fff_stage1_finite_count_sweep"
    assert manifest["epistemic_status"] == "C"
    assert manifest["task_ids"] == ["TASK-001-SWEEP"]
    assert manifest["assumption_ids"] == ["ASM-FFF-0001"]
    assert result["csv_checksum"] == manifest["outputs"][0]["sha256"]


def test_stage1_sweep_cli_emits_artifact_paths() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "fts_lab.cli", "fff", "sweep"],
        cwd=find_project_root(),
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "csv_checksum=" in result.stdout
    assert "csv_path=" in result.stdout
    assert "manifest_path=" in result.stdout
    assert "row_count=112" in result.stdout


def test_stage1_sweep_manifest_validation_fails_after_csv_corruption(tmp_path: Path) -> None:
    root = find_project_root()
    result = run_stage1_sweep(command="test fff sweep corrupt")
    manifest_path = Path(result["manifest_path"])
    manifest = read_json_object(manifest_path)
    csv_path = tmp_path / "sweep-copy.csv"
    copied_manifest_path = tmp_path / "manifest-copy.json"
    shutil.copy2(Path(manifest["outputs"][0]["path"]), csv_path)
    manifest["outputs"][0]["path"] = str(csv_path)
    write_immutable_json(copied_manifest_path, manifest)
    csv_path.write_bytes(csv_path.read_bytes() + b"\n")

    with pytest.raises(ManifestError, match="Checksum mismatch"):
        validate_manifest_file(copied_manifest_path, project_root=root)


def test_stage1_publication_tables_cli_writes_outputs_and_valid_manifest() -> None:
    root = find_project_root()
    sweep_result = run_stage1_sweep(command="test fff publication source sweep")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "fts_lab.cli",
            "fff",
            "publication-tables",
            "--sweep-manifest",
            sweep_result["manifest_path"],
        ],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "summary_csv_checksum=" in result.stdout
    assert "summary_csv_path=" in result.stdout
    assert "report_checksum=" in result.stdout
    assert "report_path=" in result.stdout
    assert "manifest_path=" in result.stdout
    assert "row_count=16" in result.stdout

    manifest_path = _manifest_path_from_output(result.stdout)
    manifest = validate_manifest_file(manifest_path, project_root=root)
    assert manifest["artifact_kind"] == "fff_stage1_publication_tables"
    assert manifest["epistemic_status"] == "C"
    assert manifest["task_ids"] == ["TASK-001-PUBTABLES"]
    assert manifest["assumption_ids"] == ["ASM-FFF-0001"]
    assert len(manifest["inputs"]) == 2
    assert len(manifest["outputs"]) == 2


def test_stage1_publication_tables_manifest_validation_fails_after_output_corruption(
    tmp_path: Path,
) -> None:
    root = find_project_root()
    sweep_result = run_stage1_sweep(command="test fff publication corrupt source sweep")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "fts_lab.cli",
            "fff",
            "publication-tables",
            "--sweep-manifest",
            sweep_result["manifest_path"],
        ],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    manifest_path = _manifest_path_from_output(result.stdout)
    manifest = read_json_object(manifest_path)
    copied_manifest_path = tmp_path / "publication-manifest-copy.json"
    copied_summary_path = tmp_path / "summary-copy.csv"
    original_summary_path = Path(manifest["outputs"][0]["path"])
    shutil.copy2(original_summary_path, copied_summary_path)
    manifest["outputs"][0]["path"] = str(copied_summary_path)
    write_immutable_json(copied_manifest_path, manifest)
    copied_summary_path.write_bytes(copied_summary_path.read_bytes() + b"\n")

    with pytest.raises(ManifestError, match="Checksum mismatch"):
        validate_manifest_file(copied_manifest_path, project_root=root)


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
