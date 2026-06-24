"""Cyclic-group helpers for FFF Stage 1."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from fractions import Fraction
from math import gcd

from fts_lab.fff.admissibility import admissible_count, is_admissible
from fts_lab.fff.functions import (
    FunctionTuple,
    iter_functions,
    require_positive_size,
    require_positive_sizes,
    validate_function,
)


def cyclic_add(left: int, right: int, order: int) -> int:
    """Add elements in the canonical additive cyclic group Z_order."""
    require_positive_size("order", order)
    return (left + right) % order


def is_cyclic_homomorphism(
    function: Sequence[int],
    domain_order: int,
    codomain_order: int,
) -> bool:
    """Return true when f: Z_n -> Z_m preserves modular addition."""
    require_positive_sizes(domain_order, codomain_order)
    values = validate_function(function, codomain_order, domain_size=domain_order)
    for left in range(domain_order):
        for right in range(domain_order):
            domain_sum = cyclic_add(left, right, domain_order)
            codomain_sum = cyclic_add(values[left], values[right], codomain_order)
            if values[domain_sum] != codomain_sum:
                return False
    return True


def cyclic_homomorphism_count_formula(domain_order: int, codomain_order: int) -> int:
    """Return the source count gcd(n, m)."""
    require_positive_sizes(domain_order, codomain_order)
    return gcd(domain_order, codomain_order)


def iter_cyclic_homomorphisms(
    domain_order: int,
    codomain_order: int,
) -> Iterator[FunctionTuple]:
    """Yield all cyclic-group homomorphisms for small finite carriers."""
    require_positive_sizes(domain_order, codomain_order)
    for function in iter_functions(domain_order, codomain_order):
        if is_cyclic_homomorphism(function, domain_order, codomain_order):
            yield function


def count_cyclic_homomorphisms_by_enumeration(
    domain_order: int,
    codomain_order: int,
) -> int:
    """Return brute-force cyclic homomorphism count."""
    return sum(1 for _ in iter_cyclic_homomorphisms(domain_order, codomain_order))


def count_admissible_cyclic_homomorphisms_by_enumeration(
    domain_order: int,
    codomain_order: int,
) -> int:
    """Return brute-force cyclic homomorphism count after admissibility filtering."""
    return sum(
        1
        for function in iter_cyclic_homomorphisms(domain_order, codomain_order)
        if is_admissible(function, codomain_order)
    )


def source_cyclic_ratio(domain_order: int, codomain_order: int) -> Fraction:
    """Return gcd(n, m) over the source admissible payoff-function denominator."""
    return Fraction(
        cyclic_homomorphism_count_formula(domain_order, codomain_order),
        admissible_count(domain_order, codomain_order),
    )


def admissible_cyclic_ratio_by_enumeration(
    domain_order: int,
    codomain_order: int,
) -> Fraction:
    """Return the audit ratio after filtering cyclic homomorphisms by admissibility."""
    return Fraction(
        count_admissible_cyclic_homomorphisms_by_enumeration(domain_order, codomain_order),
        admissible_count(domain_order, codomain_order),
    )
