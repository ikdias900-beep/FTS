from __future__ import annotations

import csv
import re

from fts_lab.doctor import find_project_root


def test_claim_matrix_is_parseable_and_ids_are_unique() -> None:
    root = find_project_root()
    with (root / "sources/claim_matrix.csv").open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    claim_ids = [row["claim_id"] for row in rows]

    assert rows
    assert len(claim_ids) == len(set(claim_ids))


def test_claim_source_and_assumption_references_exist() -> None:
    root = find_project_root()
    source_text = (root / "sources/source_map.md").read_text(encoding="utf-8")
    assumption_text = (root / "assumptions/register.md").read_text(encoding="utf-8")
    source_ids = set(re.findall(r"SRC-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{4}", source_text))
    assumption_ids = set(re.findall(r"ASM-[A-Z]+-\d{4}", assumption_text))

    with (root / "sources/claim_matrix.csv").open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    for row in rows:
        assert row["source_id"] in source_ids
        for assumption_id in re.findall(r"ASM-[A-Z]+-\d{4}", row["assumption_ids"]):
            assert assumption_id in assumption_ids
