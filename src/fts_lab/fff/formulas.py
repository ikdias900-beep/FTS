"""Exact ratio formulas for FFF Stage 1."""

from __future__ import annotations

from fractions import Fraction

from fts_lab.fff.admissibility import admissible_count
from fts_lab.fff.cyclic_groups import cyclic_homomorphism_count_formula
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
