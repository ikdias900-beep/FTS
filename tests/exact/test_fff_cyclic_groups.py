from __future__ import annotations

import pytest

from fts_lab.fff.cyclic_groups import (
    admissible_cyclic_ratio_by_enumeration,
    count_admissible_cyclic_homomorphisms_by_enumeration,
    count_cyclic_homomorphisms_by_enumeration,
    cyclic_add,
    cyclic_homomorphism_count_formula,
    is_cyclic_homomorphism,
    iter_cyclic_homomorphisms,
    source_cyclic_ratio,
)


def test_cyclic_addition_uses_modular_operation() -> None:
    assert cyclic_add(2, 3, 4) == 1


@pytest.mark.parametrize("domain_order", range(1, 7))
@pytest.mark.parametrize("codomain_order", range(1, 7))
def test_cyclic_formula_matches_bruteforce(
    domain_order: int,
    codomain_order: int,
) -> None:
    assert count_cyclic_homomorphisms_by_enumeration(
        domain_order,
        codomain_order,
    ) == cyclic_homomorphism_count_formula(domain_order, codomain_order)


@pytest.mark.parametrize("order", range(1, 7))
def test_identity_map_preserves_cyclic_structure(order: int) -> None:
    assert is_cyclic_homomorphism(tuple(range(order)), order, order)


def test_known_non_homomorphism_is_rejected() -> None:
    assert not is_cyclic_homomorphism((0, 1, 1), 3, 3)


def test_cyclic_homomorphisms_are_lazily_enumerated() -> None:
    assert list(iter_cyclic_homomorphisms(2, 2)) == [(0, 0), (0, 1)]


def test_source_cyclic_count_is_separate_from_admissible_filtered_count() -> None:
    assert cyclic_homomorphism_count_formula(2, 2) == 2
    assert count_admissible_cyclic_homomorphisms_by_enumeration(2, 2) == 1
    assert source_cyclic_ratio(2, 2).numerator == 2
    assert source_cyclic_ratio(2, 2).denominator == 3
    assert admissible_cyclic_ratio_by_enumeration(2, 2).numerator == 1
    assert admissible_cyclic_ratio_by_enumeration(2, 2).denominator == 3


@pytest.mark.parametrize(
    ("function", "domain_order", "codomain_order"),
    [
        ((0, 1), 0, 2),
        ((0, 1), 2, 0),
        ((0, 2), 2, 2),
        ((0,), 2, 2),
    ],
)
def test_cyclic_homomorphism_rejects_invalid_inputs(
    function: tuple[int, ...],
    domain_order: int,
    codomain_order: int,
) -> None:
    with pytest.raises(ValueError):
        is_cyclic_homomorphism(function, domain_order, codomain_order)
