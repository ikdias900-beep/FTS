from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st

from fts_lab.fff.admissibility import admissible_count, count_admissible_by_enumeration
from fts_lab.fff.cyclic_groups import (
    count_cyclic_homomorphisms_by_enumeration,
    cyclic_homomorphism_count_formula,
)
from fts_lab.fff.total_orders import (
    count_total_order_witnesses_by_enumeration,
    count_unique_total_order_homomorphisms_by_enumeration,
    source_total_order_witness_count,
    unique_total_order_homomorphism_count,
)

small_size = st.integers(min_value=1, max_value=4)


@given(domain_size=small_size, codomain_size=small_size)
@settings(max_examples=24)
def test_admissible_formula_property(domain_size: int, codomain_size: int) -> None:
    assert count_admissible_by_enumeration(domain_size, codomain_size) == admissible_count(
        domain_size,
        codomain_size,
    )


@given(domain_size=small_size, codomain_size=small_size)
@settings(max_examples=24)
def test_total_order_witness_formula_property(domain_size: int, codomain_size: int) -> None:
    assert count_total_order_witnesses_by_enumeration(
        domain_size,
        codomain_size,
    ) == source_total_order_witness_count(domain_size, codomain_size)


@given(domain_size=small_size, codomain_size=small_size)
@settings(max_examples=24)
def test_total_order_unique_formula_property(domain_size: int, codomain_size: int) -> None:
    assert count_unique_total_order_homomorphisms_by_enumeration(
        domain_size,
        codomain_size,
    ) == unique_total_order_homomorphism_count(domain_size, codomain_size)


@given(domain_order=small_size, codomain_order=small_size)
@settings(max_examples=24)
def test_cyclic_formula_property(domain_order: int, codomain_order: int) -> None:
    assert count_cyclic_homomorphisms_by_enumeration(
        domain_order,
        codomain_order,
    ) == cyclic_homomorphism_count_formula(domain_order, codomain_order)
