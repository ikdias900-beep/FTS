"""Release capsule checksum validation helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from string import hexdigits

from fts_lab.manifests import sha256_file


class ReleaseCapsuleError(ValueError):
    """Raised when a release capsule is incomplete or has invalid checksums."""


@dataclass(frozen=True)
class ReleaseCapsuleValidation:
    """Summary of a successful release capsule validation."""

    capsule_root: Path
    checksum_file: Path
    checked_files: tuple[str, ...]


def validate_release_capsule(capsule_root: Path) -> ReleaseCapsuleValidation:
    """Validate a release capsule using its local checksums.txt inventory."""
    resolved_root = capsule_root.resolve()
    checksum_file = resolved_root / "checksums.txt"
    if not checksum_file.is_file():
        raise ReleaseCapsuleError(f"Missing release checksum file: {checksum_file}")

    rows = read_release_checksum_rows(checksum_file)
    if not rows:
        raise ReleaseCapsuleError(f"No checksum rows found in {checksum_file}")

    actual_files = _capsule_file_inventory(resolved_root, checksum_file=checksum_file)
    missing_from_checksums = sorted(actual_files - rows.keys())
    if missing_from_checksums:
        raise ReleaseCapsuleError(
            "Files are present in capsule but not listed in checksums.txt: "
            + ", ".join(missing_from_checksums)
        )

    for relative_path, expected_hash in rows.items():
        artifact_path = _resolve_capsule_file(resolved_root, relative_path)
        if not artifact_path.is_file():
            raise ReleaseCapsuleError(f"Listed capsule file is missing: {relative_path}")
        actual_hash = sha256_file(artifact_path)
        if actual_hash != expected_hash:
            raise ReleaseCapsuleError(
                f"Checksum mismatch for {relative_path}: "
                f"expected {expected_hash}, got {actual_hash}"
            )

    return ReleaseCapsuleValidation(
        capsule_root=resolved_root,
        checksum_file=checksum_file,
        checked_files=tuple(sorted(rows)),
    )


def read_release_checksum_rows(path: Path) -> dict[str, str]:
    """Read a release checksums.txt file keyed by normalized POSIX relative path."""
    rows: dict[str, str] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line:
            continue
        if "  " not in line:
            raise ReleaseCapsuleError(
                f"Invalid checksum row {line_number} in {path}: expected '<sha256>  <path>'"
            )
        expected_hash, relative_path = line.split("  ", maxsplit=1)
        _validate_sha256(expected_hash, path=path, line_number=line_number)
        normalized_path = _normalize_capsule_relative_path(
            relative_path,
            checksum_file=path,
            line_number=line_number,
        )
        if normalized_path in rows:
            raise ReleaseCapsuleError(
                f"Duplicate checksum path {normalized_path!r} in {path} at line {line_number}"
            )
        rows[normalized_path] = expected_hash
    return rows


def _validate_sha256(value: str, *, path: Path, line_number: int) -> None:
    if len(value) != 64 or any(character not in hexdigits for character in value):
        raise ReleaseCapsuleError(f"Invalid SHA-256 at {path}:{line_number}")
    if value.lower() != value:
        raise ReleaseCapsuleError(f"SHA-256 must be lowercase at {path}:{line_number}")


def _normalize_capsule_relative_path(
    value: str,
    *,
    checksum_file: Path,
    line_number: int,
) -> str:
    if not value or value == "." or "\\" in value:
        raise ReleaseCapsuleError(
            f"Invalid capsule path at {checksum_file}:{line_number}: {value!r}"
        )
    path = PurePosixPath(value)
    if path.is_absolute() or PureWindowsPath(value).is_absolute() or ".." in path.parts:
        raise ReleaseCapsuleError(
            f"Checksum path must stay inside the capsule at {checksum_file}:{line_number}: "
            f"{value!r}"
        )
    normalized = path.as_posix()
    if normalized != value:
        raise ReleaseCapsuleError(
            f"Checksum path must be normalized POSIX at {checksum_file}:{line_number}: {value!r}"
        )
    return normalized


def _resolve_capsule_file(capsule_root: Path, relative_path: str) -> Path:
    return capsule_root.joinpath(*PurePosixPath(relative_path).parts)


def _capsule_file_inventory(capsule_root: Path, *, checksum_file: Path) -> set[str]:
    return {
        path.relative_to(capsule_root).as_posix()
        for path in capsule_root.rglob("*")
        if path.is_file() and path.resolve() != checksum_file
    }
