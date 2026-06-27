from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st

from fts_lab.fff.admissibility import admissible_count, count_admissible_by_enumeration
from fts_lab.fff.cyclic_groups import (
    count_cyclic_homomorphisms_by_enumeration,
    cyclic_homomorphism_count_formula,
)
from fts_lab.fff.functions import count_all_functions
from fts_lab.fff.measurable_spaces import count_measurable_functions_by_enumeration
from fts_lab.fff.permutation_groups import (
    compose_permutations,
    conjugate_permutation,
    identity_permutation,
    inverse_permutation,
    is_second_order_respectful,
)
from fts_lab.fff.total_orders import (
    count_total_order_witnesses_by_enumeration,
    count_unique_total_order_homomorphisms_by_enumeration,
    source_total_order_witness_count,
    unique_total_order_homomorphism_count,
)

small_size = st.integers(min_value=1, max_value=4)
small_permutation = st.permutations([0, 1, 2]).map(tuple)


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


@given(permutation=small_permutation)
@settings(max_examples=12)
def test_permutation_inverse_property(permutation: tuple[int, ...]) -> None:
    inverse = inverse_permutation(permutation)

    assert compose_permutations(permutation, inverse) == identity_permutation(len(permutation))
    assert compose_permutations(inverse, permutation) == identity_permutation(len(permutation))


@given(conjugator=small_permutation, group_element=small_permutation)
@settings(max_examples=24)
def test_inner_conjugation_respects_second_order_action_property(
    conjugator: tuple[int, ...],
    group_element: tuple[int, ...],
) -> None:
    assert is_second_order_respectful(
        conjugator,
        group_element,
        conjugate_permutation(conjugator, group_element),
    )


@given(domain_size=small_size, codomain_size=small_size)
@settings(max_examples=16)
def test_discrete_domain_partition_makes_every_function_measurable(
    domain_size: int,
    codomain_size: int,
) -> None:
    w_partition = [[index] for index in range(domain_size)]
    v_partition = [[index] for index in range(codomain_size)]

    assert count_measurable_functions_by_enumeration(
        w_partition,
        v_partition,
    ) == count_all_functions(domain_size, codomain_size)


@given(domain_size=small_size, codomain_size=small_size)
@settings(max_examples=16)
def test_trivial_codomain_partition_makes_every_function_measurable(
    domain_size: int,
    codomain_size: int,
) -> None:
    w_partition = [list(range(domain_size))]
    v_partition = [list(range(codomain_size))]

    assert count_measurable_functions_by_enumeration(
        w_partition,
        v_partition,
    ) == count_all_functions(domain_size, codomain_size)
