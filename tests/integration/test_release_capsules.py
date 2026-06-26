from __future__ import annotations

import hashlib
from pathlib import Path, PurePosixPath

from fts_lab.doctor import find_project_root


def test_stage2_p2_draft_capsule_checksums_match_files() -> None:
    capsule_root = find_project_root() / "release/stage2-p2-draft"
    checksum_file = capsule_root / "checksums.txt"

    assert checksum_file.is_file()
    rows = _read_checksum_rows(checksum_file)
    assert rows
    assert "derived_data/fbt_numerical_appendix.json" in rows
    assert "derived_data/fbt_numerical_appendix.md" in rows
    assert "raw_data/fbt_numerical_example_source_table.json" in rows

    for relative_path, expected_hash in rows.items():
        path = capsule_root.joinpath(*PurePosixPath(relative_path).parts)
        assert path.is_file(), relative_path
        assert _sha256_file(path) == expected_hash


def _read_checksum_rows(path: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        expected_hash, relative_path = line.split("  ", maxsplit=1)
        rows[relative_path] = expected_hash
    return rows


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
