from __future__ import annotations

from pathlib import Path

from hypothesis import given
from hypothesis import strategies as st

from fts_lab.manifests import canonical_json_bytes, normalize_relative_path, sha256_bytes


@given(st.dictionaries(st.text(min_size=1), st.integers(), min_size=1, max_size=20))
def test_canonical_serialization_is_invariant_to_insertion_order(data: dict[str, int]) -> None:
    items = list(data.items())
    reversed_data = dict(reversed(items))

    assert canonical_json_bytes(data) == canonical_json_bytes(reversed_data)


@given(st.lists(st.from_regex(r"[A-Za-z0-9_]+", fullmatch=True), min_size=1, max_size=5))
def test_equivalent_relative_paths_normalize_consistently(segments: list[str]) -> None:
    base = Path.cwd()
    relative = Path(*segments)
    equivalent = Path(".") / relative

    assert normalize_relative_path(relative, base) == normalize_relative_path(equivalent, base)


@given(st.binary(min_size=1, max_size=1024))
def test_checksum_detects_payload_mutation(data: bytes) -> None:
    mutated = data + b"x"

    assert sha256_bytes(data) != sha256_bytes(mutated)
