"""Total-order helpers for FFF Stage 1."""

from __future__ import annotations

from collections.abc import Sequence
from fractions import Fraction
from itertools import pairwise
from math import comb
from typing import Literal

from fts_lab.fff.admissibility import admissible_count, is_admissible
from fts_lab.fff.functions import (
    iter_functions,
    require_positive_sizes,
    validate_function,
)

type OrderOrientation = Literal["preserving", "reversing"]


def is_order_preserving(function: Sequence[int], codomain_size: int) -> bool:
    """Return true when values are weakly non-decreasing on the canonical chain."""
    values = validate_function(function, codomain_size)
    return all(left <= right for left, right in pairwise(values))


def is_order_reversing(function: Sequence[int], codomain_size: int) -> bool:
    """Return true when values are weakly non-increasing on the canonical chain."""
    values = validate_function(function, codomain_size)
    return all(left >= right for left, right in pairwise(values))


def orientation_witnesses(
    function: Sequence[int],
    codomain_size: int,
    *,
    require_admissible: bool = True,
) -> tuple[OrderOrientation, ...]:
    """Return preserving/reversing witnesses for a finite function.

    A maximum constant function has two witnesses, which is the visible source of the
    total-order orientation double count.
    """
    values = validate_function(function, codomain_size)
    if require_admissible and not is_admissible(values, codomain_size):
        return ()

    witnesses: list[OrderOrientation] = []
    if is_order_preserving(values, codomain_size):
        witnesses.append("preserving")
    if is_order_reversing(values, codomain_size):
        witnesses.append("reversing")
    return tuple(witnesses)


def source_total_order_witness_count(domain_size: int, codomain_size: int) -> int:
    """Return the source's preserving-or-reversing orientation witness count."""
    require_positive_sizes(domain_size, codomain_size)
    return 2 * comb(domain_size + codomain_size - 2, codomain_size - 1)


def unique_total_order_homomorphism_count(domain_size: int, codomain_size: int) -> int:
    """Return unique admissible monotone functions under the Stage 1 convention."""
    return source_total_order_witness_count(domain_size, codomain_size) - 1


def count_total_order_witnesses_by_enumeration(domain_size: int, codomain_size: int) -> int:
    """Return brute-force preserving/reversing witness count for admissible functions."""
    require_positive_sizes(domain_size, codomain_size)
    return sum(
        len(orientation_witnesses(function, codomain_size))
        for function in iter_functions(domain_size, codomain_size)
    )


def count_unique_total_order_homomorphisms_by_enumeration(
    domain_size: int,
    codomain_size: int,
) -> int:
    """Return brute-force unique admissible monotone-function count."""
    require_positive_sizes(domain_size, codomain_size)
    return sum(
        1
        for function in iter_functions(domain_size, codomain_size)
        if orientation_witnesses(function, codomain_size)
    )


def count_order_preserving_admissible_by_enumeration(
    domain_size: int,
    codomain_size: int,
) -> int:
    """Return brute-force admissible order-preserving count."""
    require_positive_sizes(domain_size, codomain_size)
    return sum(
        1
        for function in iter_functions(domain_size, codomain_size)
        if is_admissible(function, codomain_size) and is_order_preserving(function, codomain_size)
    )


def count_order_reversing_admissible_by_enumeration(
    domain_size: int,
    codomain_size: int,
) -> int:
    """Return brute-force admissible order-reversing count."""
    require_positive_sizes(domain_size, codomain_size)
    return sum(
        1
        for function in iter_functions(domain_size, codomain_size)
        if is_admissible(function, codomain_size) and is_order_reversing(function, codomain_size)
    )


def source_total_order_ratio(domain_size: int, codomain_size: int) -> Fraction:
    """Return the exact source witness ratio over admissible payoff functions."""
    return Fraction(
        source_total_order_witness_count(domain_size, codomain_size),
        admissible_count(domain_size, codomain_size),
    )


def unique_total_order_ratio(domain_size: int, codomain_size: int) -> Fraction:
    """Return the exact unique-function ratio over admissible payoff functions."""
    return Fraction(
        unique_total_order_homomorphism_count(domain_size, codomain_size),
        admissible_count(domain_size, codomain_size),
    )
