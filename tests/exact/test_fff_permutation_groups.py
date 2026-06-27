from __future__ import annotations

import json
from pathlib import Path

import pytest

from fts_lab.fff.permutation_groups import (
    compose_permutations,
    conjugate_permutation,
    constant_function,
    identity_permutation,
    inverse_permutation,
    is_second_order_homomorphism,
    is_second_order_respectful,
    iter_symmetric_group,
    source_permutation_ratio,
    source_permutation_respectful_count,
    validate_permutation,
)

FIXTURE_PATH = Path("tests/fixtures/fff/stage3_structure_spec_cases.json")


def test_validate_permutation_canonicalizes_tuple() -> None:
    assert validate_permutation([2, 0, 1]) == (2, 0, 1)


@pytest.mark.parametrize(
    "permutation",
    [
        (),
        (0, 0),
        (0, 2),
        (0, -1),
    ],
)
def test_validate_permutation_rejects_invalid_values(permutation: tuple[int, ...]) -> None:
    with pytest.raises(ValueError):
        validate_permutation(permutation)


def test_permutation_composition_and_inverse() -> None:
    permutation = (2, 0, 1)
    inverse = inverse_permutation(permutation)

    assert compose_permutations(permutation, inverse) == identity_permutation(3)
    assert compose_permutations(inverse, permutation) == identity_permutation(3)


def test_iter_symmetric_group_yields_factorial_many_elements() -> None:
    assert len(list(iter_symmetric_group(3))) == 6


def test_inner_conjugation_satisfies_second_order_action_law() -> None:
    conjugator = (1, 2, 0)
    group_element = (1, 0, 2)
    phi_image = conjugate_permutation(conjugator, group_element)

    assert is_second_order_respectful(conjugator, group_element, phi_image)


def test_second_order_homomorphism_accepts_inner_conjugation_on_small_group() -> None:
    conjugator = (1, 2, 0)
    group_elements = tuple(iter_symmetric_group(3))
    phi_images = {
        group_element: conjugate_permutation(conjugator, group_element)
        for group_element in group_elements
    }

    assert is_second_order_homomorphism(conjugator, group_elements, phi_images)


def test_constant_function_respects_trivial_target_action() -> None:
    function = constant_function(domain_size=3, value=1, codomain_size=2)
    group_element = (1, 2, 0)
    trivial_phi_image = identity_permutation(2)

    assert is_second_order_respectful(function, group_element, trivial_phi_image)


def test_nonrespectful_function_is_rejected() -> None:
    function = (0, 1, 1)
    group_element = (1, 0, 2)
    phi_image = identity_permutation(2)

    assert not is_second_order_respectful(function, group_element, phi_image)


def test_source_permutation_formula_matches_stage3_fixtures() -> None:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    for case in fixture["permutation_groups"]["cases"]:
        n = case["n"]
        ratio = source_permutation_ratio(n)
        assert source_permutation_respectful_count(n) == case["respectful_function_count"]
        assert ratio.numerator == case["respectful_function_count"]
        assert ratio.denominator == case["admissible_denominator"]


@pytest.mark.parametrize("degree", [1, 2, 3, 4])
def test_source_permutation_formula_rejects_pre_theorem_scope(degree: int) -> None:
    with pytest.raises(ValueError, match="n >= 5"):
        source_permutation_respectful_count(degree)
