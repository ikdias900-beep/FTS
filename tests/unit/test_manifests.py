from __future__ import annotations

from pathlib import Path

import pytest

from fts_lab.manifests import (
    INFRASTRUCTURE_SMOKE_KIND,
    ManifestError,
    canonical_json_bytes,
    sha256_bytes,
    validate_manifest_rules,
    write_immutable_bytes,
)


def test_canonical_json_serialization_is_stable() -> None:
    left = {"b": [2, 1], "a": {"d": 4, "c": 3}}
    right = {"a": {"c": 3, "d": 4}, "b": [2, 1]}

    assert canonical_json_bytes(left) == canonical_json_bytes(right)
    assert canonical_json_bytes(left) == b'{"a":{"c":3,"d":4},"b":[2,1]}'


def test_sha256_helper_returns_known_digest() -> None:
    assert (
        sha256_bytes(b"abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    )


def test_manifest_rejects_unknown_epistemic_status() -> None:
    with pytest.raises(ManifestError, match="Unknown epistemic status"):
        validate_manifest_rules(
            {
                "artifact_kind": "scientific",
                "epistemic_status": "X",
                "claim_ids": ["CLM-TEST-001"],
                "source_ids": ["SRC-TEST-2026"],
                "assumption_ids": [],
            }
        )


def test_infrastructure_manifest_accepts_null_only_with_no_claims() -> None:
    validate_manifest_rules(
        {
            "artifact_kind": INFRASTRUCTURE_SMOKE_KIND,
            "epistemic_status": None,
            "claim_ids": [],
            "source_ids": [],
            "assumption_ids": [],
        }
    )

    with pytest.raises(ManifestError, match="must not link claims"):
        validate_manifest_rules(
            {
                "artifact_kind": INFRASTRUCTURE_SMOKE_KIND,
                "epistemic_status": None,
                "claim_ids": ["CLM-TEST-001"],
                "source_ids": [],
                "assumption_ids": [],
            }
        )


def test_scientific_manifest_rejects_missing_claim_source_linkage() -> None:
    with pytest.raises(ManifestError, match="claim_id"):
        validate_manifest_rules(
            {
                "artifact_kind": "scientific_result",
                "epistemic_status": "R",
                "claim_ids": [],
                "source_ids": ["SRC-TEST-2026"],
                "assumption_ids": [],
            }
        )

    with pytest.raises(ManifestError, match="source_id"):
        validate_manifest_rules(
            {
                "artifact_kind": "scientific_result",
                "epistemic_status": "R",
                "claim_ids": ["CLM-TEST-001"],
                "source_ids": [],
                "assumption_ids": [],
            }
        )


def test_output_overwrite_is_refused_by_default(tmp_path: Path) -> None:
    path = tmp_path / "artifact.bin"
    write_immutable_bytes(path, b"first")

    with pytest.raises(FileExistsError):
        write_immutable_bytes(path, b"second")

    assert path.read_bytes() == b"first"
