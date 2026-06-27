from __future__ import annotations

import json
from pathlib import Path

import pytest

from fts_lab.fff.functions import count_all_functions
from fts_lab.fff.measurable_spaces import (
    all_functions_measurable_by_special_case,
    count_admissible_measurable_functions_by_enumeration,
    count_measurable_functions_by_enumeration,
    event_algebra,
    inverse_image,
    is_discrete_partition,
    is_measurable,
    is_trivial_partition,
    is_union_of_blocks,
    measurable_bound_applies_to_partitions,
    partition_characteristic,
    partition_order,
    source_measurable_bound_ratio,
    source_measurable_upper_bound,
    validate_partition,
)

FIXTURE_PATH = Path("tests/fixtures/fff/stage3_structure_spec_cases.json")


def test_validate_partition_canonicalizes_blocks() -> None:
    assert validate_partition([[2], [1, 0]]) == ((0, 1), (2,))


@pytest.mark.parametrize(
    "partition",
    [
        [],
        [[]],
        [[0], [0]],
        [[1]],
        [[0, -1]],
    ],
)
def test_validate_partition_rejects_invalid_partitions(
    partition: list[list[int]],
) -> None:
    with pytest.raises(ValueError):
        validate_partition(partition)


def test_partition_order_and_characteristic() -> None:
    partition = [[0, 1], [2], [3, 4, 5]]

    assert partition_order(partition) == 3
    assert partition_characteristic(partition) == (1, 2, 3)


def test_event_algebra_contains_all_unions_of_base_blocks() -> None:
    assert event_algebra([[0, 1], [2]]) == ((), (2,), (0, 1), (0, 1, 2))
    assert is_union_of_blocks([0, 1], [[0, 1], [2]])
    assert not is_union_of_blocks([0], [[0, 1], [2]])


def test_inverse_image_returns_domain_event() -> None:
    assert inverse_image((0, 1, 1), [1], codomain_size=2) == (1, 2)


def test_measurable_exact_cases_match_stage3_fixtures() -> None:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    for case in fixture["measurable_spaces"]["exact_cases"]:
        measured = count_measurable_functions_by_enumeration(case["w_base"], case["v_base"])
        admissible = count_admissible_measurable_functions_by_enumeration(
            case["w_base"],
            case["v_base"],
        )

        assert measured == case["total_measurable_functions"], case["case_id"]
        assert admissible == case["admissible_measurable_functions"], case["case_id"]
        if "special_case" in case:
            assert all_functions_measurable_by_special_case(case["w_base"], case["v_base"])
            assert measured == count_all_functions(len(case["w_elements"]), len(case["v_elements"]))
        if "bound" in case:
            assert measured <= case["bound"]


def test_measurable_non_measurable_witnesses_match_stage3_fixtures() -> None:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    for case in fixture["measurable_spaces"]["non_measurable_witnesses"]:
        assert (
            is_measurable(case["function"], case["w_base"], case["v_base"]) is case["is_measurable"]
        ), case["case_id"]


def test_partition_special_cases_are_detected() -> None:
    assert is_discrete_partition([[0], [1], [2]])
    assert not is_discrete_partition([[0, 1], [2]])
    assert is_trivial_partition([[0, 1, 2]])
    assert not is_trivial_partition([[0], [1], [2]])


def test_bound_scope_detection_for_partitions() -> None:
    assert measurable_bound_applies_to_partitions([[0, 1], [2]], [[0], [1]])
    assert not measurable_bound_applies_to_partitions([[0], [1], [2]], [[0], [1]])
    assert not measurable_bound_applies_to_partitions([[0, 1], [2]], [[0, 1]])


def test_source_measurable_bound_matches_stage3_fixtures() -> None:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    for case in fixture["measurable_spaces"]["bound_cases"]:
        ratio = source_measurable_bound_ratio(case["n"], case["m"], case["k"])
        assert source_measurable_upper_bound(case["n"], case["m"], case["k"]) == case["bound"]
        assert ratio.numerator == case["bound"]


@pytest.mark.parametrize(
    ("domain_size", "codomain_size", "domain_order"),
    [
        (1, 2, 1),
        (3, 1, 2),
        (3, 2, 1),
        (3, 2, 3),
    ],
)
def test_source_measurable_bound_rejects_out_of_scope_inputs(
    domain_size: int,
    codomain_size: int,
    domain_order: int,
) -> None:
    with pytest.raises(ValueError):
        source_measurable_upper_bound(domain_size, codomain_size, domain_order)
