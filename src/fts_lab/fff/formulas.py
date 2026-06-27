"""Exact ratio formulas for FFF Stage 1."""

from __future__ import annotations

from fractions import Fraction

from fts_lab.fff.admissibility import admissible_count
from fts_lab.fff.cyclic_groups import cyclic_homomorphism_count_formula
from fts_lab.fff.measurable_spaces import source_measurable_upper_bound
from fts_lab.fff.permutation_groups import source_permutation_respectful_count
from fts_lab.fff.total_orders import (
    source_total_order_witness_count,
    unique_total_order_homomorphism_count,
)


def exact_ratio(numerator: int, denominator: int) -> Fraction:
    """Return an exact ratio and reject impossible denominators."""
    if denominator <= 0:
        raise ValueError(f"denominator must be positive, got {denominator}")
    if numerator < 0:
        raise ValueError(f"numerator must be non-negative, got {numerator}")
    return Fraction(numerator, denominator)


def admissible_denominator(domain_size: int, codomain_size: int) -> int:
    """Return the shared admissible payoff-function denominator."""
    return admissible_count(domain_size, codomain_size)


def source_total_order_witness_ratio(domain_size: int, codomain_size: int) -> Fraction:
    """Return the source total-order witness ratio."""
    return exact_ratio(
        source_total_order_witness_count(domain_size, codomain_size),
        admissible_denominator(domain_size, codomain_size),
    )


def unique_total_order_homomorphism_ratio(domain_size: int, codomain_size: int) -> Fraction:
    """Return the unique total-order homomorphism ratio."""
    return exact_ratio(
        unique_total_order_homomorphism_count(domain_size, codomain_size),
        admissible_denominator(domain_size, codomain_size),
    )


def source_cyclic_homomorphism_ratio(domain_size: int, codomain_size: int) -> Fraction:
    """Return the source cyclic-group homomorphism ratio."""
    return exact_ratio(
        cyclic_homomorphism_count_formula(domain_size, codomain_size),
        admissible_denominator(domain_size, codomain_size),
    )


def source_permutation_group_ratio(degree: int) -> Fraction:
    """Return the source permutation-group ratio for the theorem scope ``n >= 5``."""
    return exact_ratio(
        source_permutation_respectful_count(degree),
        admissible_denominator(degree, degree),
    )


def source_measurable_structure_bound_ratio(
    domain_size: int,
    codomain_size: int,
    domain_order: int,
) -> Fraction:
    """Return the source measurable-structure upper-bound ratio."""
    return exact_ratio(
        source_measurable_upper_bound(domain_size, codomain_size, domain_order),
        admissible_denominator(domain_size, codomain_size),
    )
