from __future__ import annotations

import pytest

from fts_lab.fff.total_orders import (
    count_order_preserving_admissible_by_enumeration,
    count_order_reversing_admissible_by_enumeration,
    count_total_order_witnesses_by_enumeration,
    count_unique_total_order_homomorphisms_by_enumeration,
    is_order_preserving,
    is_order_reversing,
    orientation_witnesses,
    source_total_order_ratio,
    source_total_order_witness_count,
    unique_total_order_homomorphism_count,
    unique_total_order_ratio,
)


def test_order_orientation_checks() -> None:
    assert is_order_preserving((0, 1, 1), 2)
    assert not is_order_preserving((1, 0, 1), 2)
    assert is_order_reversing((2, 1, 1, 0), 3)
    assert not is_order_reversing((1, 0, 1), 2)


def test_source_formula_counts_orientation_witnesses_not_unique_functions() -> None:
    assert source_total_order_witness_count(2, 2) == 4
    assert count_total_order_witnesses_by_enumeration(2, 2) == 4
    assert unique_total_order_homomorphism_count(2, 2) == 3
    assert count_unique_total_order_homomorphisms_by_enumeration(2, 2) == 3


def test_maximum_constant_has_two_orientation_witnesses() -> None:
    assert orientation_witnesses((1, 1), 2) == ("preserving", "reversing")
    assert orientation_witnesses((0, 0), 2) == ()
    assert orientation_witnesses((0, 0), 2, require_admissible=False) == (
        "preserving",
        "reversing",
    )


@pytest.mark.parametrize("domain_size", range(1, 6))
@pytest.mark.parametrize("codomain_size", range(1, 6))
def test_total_order_source_formula_matches_witness_enumeration(
    domain_size: int,
    codomain_size: int,
) -> None:
    assert count_total_order_witnesses_by_enumeration(
        domain_size,
        codomain_size,
    ) == source_total_order_witness_count(domain_size, codomain_size)


@pytest.mark.parametrize("domain_size", range(1, 6))
@pytest.mark.parametrize("codomain_size", range(1, 6))
def test_total_order_unique_formula_matches_unique_enumeration(
    domain_size: int,
    codomain_size: int,
) -> None:
    assert count_unique_total_order_homomorphisms_by_enumeration(
        domain_size,
        codomain_size,
    ) == unique_total_order_homomorphism_count(domain_size, codomain_size)


@pytest.mark.parametrize("domain_size", range(1, 5))
@pytest.mark.parametrize("codomain_size", range(1, 5))
def test_preserving_and_reversing_counts_are_symmetric(
    domain_size: int,
    codomain_size: int,
) -> None:
    assert count_order_preserving_admissible_by_enumeration(
        domain_size,
        codomain_size,
    ) == count_order_reversing_admissible_by_enumeration(domain_size, codomain_size)


def test_ratios_are_exact() -> None:
    assert source_total_order_ratio(2, 2).numerator == 4
    assert source_total_order_ratio(2, 2).denominator == 3
    assert unique_total_order_ratio(2, 2).numerator == 1
    assert unique_total_order_ratio(2, 2).denominator == 1


@pytest.mark.parametrize(("domain_size", "codomain_size"), [(0, 1), (1, 0)])
def test_total_order_counts_reject_invalid_sizes(domain_size: int, codomain_size: int) -> None:
    with pytest.raises(ValueError):
        source_total_order_witness_count(domain_size, codomain_size)
