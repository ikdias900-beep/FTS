from __future__ import annotations

import json
import math
from itertools import product
from pathlib import Path
from typing import Any

FIXTURE_PATH = Path("tests/fixtures/fff/stage3_structure_spec_cases.json")


def test_stage3_fixture_metadata_is_traceable() -> None:
    fixture = _load_fixture()
    metadata = fixture["metadata"]

    assert metadata["task_id"] == "TASK-003-FFF-STRUCTURE-SPEC"
    assert metadata["source_id"] == "SRC-FFF-2020"
    assert metadata["claim_ids"] == ["CLM-FFF-PERM-001", "CLM-FFF-MEAS-001"]
    assert metadata["assumption_ids"] == ["ASM-FFF-0002", "ASM-FFF-0003"]
    assert metadata["epistemic_status"] == "R"


def test_permutation_group_source_formula_cases_are_consistent() -> None:
    permutation = _load_fixture()["permutation_groups"]
    minimum_n = permutation["formula_valid_for_n_at_least"]

    for case in permutation["cases"]:
        n = case["n"]
        assert n >= minimum_n
        assert case["respectful_function_count"] == 2 * n + math.factorial(n)
        assert case["admissible_denominator"] == n**n - (n - 1) ** n
        assert case["respectful_function_count"] < case["admissible_denominator"]


def test_measurable_bound_cases_are_consistent() -> None:
    measurable = _load_fixture()["measurable_spaces"]

    for case in measurable["bound_cases"]:
        n = case["n"]
        m = case["m"]
        k = case["k"]
        assert 2 <= k <= n - 1
        assert m >= 2
        assert case["bound"] == _measurable_bound(n=n, m=m, k=k)


def test_measurable_exact_cases_match_inverse_image_oracle() -> None:
    measurable = _load_fixture()["measurable_spaces"]

    for case in measurable["exact_cases"]:
        functions = list(product(case["v_elements"], repeat=len(case["w_elements"])))
        measured = [
            function
            for function in functions
            if _is_measurable(function, w_base=case["w_base"], v_base=case["v_base"])
        ]
        admissible_measured = [
            function for function in measured if max(case["v_elements"]) in function
        ]

        assert len(measured) == case["total_measurable_functions"], case["case_id"]
        assert len(admissible_measured) == case["admissible_measurable_functions"], case["case_id"]
        if "bound" in case:
            assert len(measured) <= case["bound"]


def test_measurable_non_measurable_witnesses_are_rejected() -> None:
    measurable = _load_fixture()["measurable_spaces"]

    for case in measurable["non_measurable_witnesses"]:
        assert (
            _is_measurable(tuple(case["function"]), w_base=case["w_base"], v_base=case["v_base"])
            is case["is_measurable"]
        ), case["case_id"]


def _load_fixture() -> dict[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _measurable_bound(*, n: int, m: int, k: int) -> int:
    return m ** (k - 1) + (m ** (k - 1)) * ((m - 1) ** (n - k + 1))


def _is_measurable(
    function: tuple[int, ...],
    *,
    w_base: list[list[int]],
    v_base: list[list[int]],
) -> bool:
    for v_block in v_base:
        preimage = {w_index for w_index, value in enumerate(function) if value in set(v_block)}
        if not _is_union_of_w_blocks(preimage, w_base=w_base):
            return False
    return True


def _is_union_of_w_blocks(candidate: set[int], *, w_base: list[list[int]]) -> bool:
    reconstructed: set[int] = set()
    for block in w_base:
        block_set = set(block)
        if block_set <= candidate:
            reconstructed.update(block_set)
        elif block_set & candidate:
            return False
    return reconstructed == candidate
