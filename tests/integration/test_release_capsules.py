from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from fts_lab.doctor import find_project_root
from fts_lab.release_capsules import (
    ReleaseCapsuleError,
    validate_release_capsule,
)


def test_stage2_p2_draft_capsule_checksums_match_files() -> None:
    capsule_root = find_project_root() / "release/stage2-p2-draft"
    result = validate_release_capsule(capsule_root)

    assert result.checksum_file == capsule_root.resolve() / "checksums.txt"
    assert "derived_data/fbt_numerical_appendix.json" in result.checked_files
    assert "derived_data/fbt_numerical_appendix.md" in result.checked_files
    assert "raw_data/fbt_numerical_example_source_table.json" in result.checked_files


def test_stage2_p2_draft_capsule_cli_validates_local_archive() -> None:
    root = find_project_root()
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "fts_lab.cli",
            "validate-release-capsule",
            "release/stage2-p2-draft",
        ],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "release_capsule_valid=" in result.stdout
    assert "checked_files=12" in result.stdout


def test_stage3_p3_draft_capsule_checksums_match_files() -> None:
    capsule_root = find_project_root() / "release/stage3-p3-draft"
    result = validate_release_capsule(capsule_root)

    assert result.checksum_file == capsule_root.resolve() / "checksums.txt"
    assert "raw_data/stage3_structure_spec_cases.json" in result.checked_files
    assert "derived_data/stage3_fff_structure_checkpoint.json" in result.checked_files
    assert "derived_data/stage3_fff_structure_checkpoint.md" in result.checked_files


def test_stage3_p3_draft_capsule_cli_validates_local_archive() -> None:
    root = find_project_root()
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "fts_lab.cli",
            "validate-release-capsule",
            "release/stage3-p3-draft",
        ],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "release_capsule_valid=" in result.stdout
    assert "checked_files=12" in result.stdout


def test_stage4_p4_draft_capsule_checksums_match_files() -> None:
    capsule_root = find_project_root() / "release/stage4-p4-draft"
    result = validate_release_capsule(capsule_root)

    assert result.checksum_file == capsule_root.resolve() / "checksums.txt"
    assert "raw_data/fbt_atlas_v0.json" in result.checked_files
    assert "raw_data/stage4_fbt_spec_cases.json" in result.checked_files
    assert "raw_data/stage4_fbt_oracle_cases.json" in result.checked_files
    assert "derived_data/fbt_atlas_v0_smoke.json" in result.checked_files
    assert "derived_data/fbt_atlas_v0_smoke.md" in result.checked_files
    assert "derived_data/stage4_fbt_atlas_checkpoint.json" in result.checked_files


def test_stage4_p4_draft_capsule_cli_validates_local_archive() -> None:
    root = find_project_root()
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "fts_lab.cli",
            "validate-release-capsule",
            "release/stage4-p4-draft",
        ],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "release_capsule_valid=" in result.stdout
    assert "checked_files=17" in result.stdout


def test_stage4_v1_draft_capsule_checksums_match_files() -> None:
    capsule_root = find_project_root() / "release/stage4-v1-draft"
    result = validate_release_capsule(capsule_root)

    assert result.checksum_file == capsule_root.resolve() / "checksums.txt"
    assert "raw_data/fbt_atlas_v1_draft.json" in result.checked_files
    assert "raw_data/fbt_atlas_v1_raw_cells.json" in result.checked_files
    assert "derived_data/fbt_atlas_v1_aggregate.json" in result.checked_files
    assert "derived_data/fbt_atlas_v1_report.md" in result.checked_files
    assert "derived_data/stage4_atlas_v1_checkpoint.json" in result.checked_files


def test_stage4_v1_draft_capsule_cli_validates_local_archive() -> None:
    root = find_project_root()
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "fts_lab.cli",
            "validate-release-capsule",
            "release/stage4-v1-draft",
        ],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "release_capsule_valid=" in result.stdout
    assert "checked_files=17" in result.stdout


def test_release_capsule_validation_rejects_unlisted_files(tmp_path: Path) -> None:
    source_root = find_project_root() / "release/stage2-p2-draft"
    capsule_copy = tmp_path / "stage2-p2-draft"
    shutil.copytree(source_root, capsule_copy)
    (capsule_copy / "unexpected.txt").write_text("not in checksums\n", encoding="utf-8")

    with pytest.raises(ReleaseCapsuleError, match=r"not listed in checksums\.txt"):
        validate_release_capsule(capsule_copy)
