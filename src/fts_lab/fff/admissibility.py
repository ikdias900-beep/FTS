"""Admissible payoff-function counts for FFF Stage 1."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from fts_lab.fff.functions import (
    FunctionTuple,
    iter_functions,
    require_positive_sizes,
    validate_function,
)


def maximum_payoff_value(codomain_size: int) -> int:
    """Return the code value corresponding to the source's maximum payoff value."""
    if codomain_size <= 0:
        raise ValueError(f"codomain_size must be positive, got {codomain_size}")
    return codomain_size - 1


def is_admissible(function: Sequence[int], codomain_size: int) -> bool:
    """Return true when a payoff function attains the maximum payoff value."""
    values = validate_function(function, codomain_size)
    return maximum_payoff_value(codomain_size) in values


def admissible_count(domain_size: int, codomain_size: int) -> int:
    """Return the source formula m^n - (m - 1)^n."""
    require_positive_sizes(domain_size, codomain_size)
    return int(codomain_size**domain_size - (codomain_size - 1) ** domain_size)


def iter_admissible_functions(
    domain_size: int,
    codomain_size: int,
) -> Iterator[FunctionTuple]:
    """Yield all admissible functions over the canonical finite carriers."""
    for function in iter_functions(domain_size, codomain_size):
        if is_admissible(function, codomain_size):
            yield function


def count_admissible_by_enumeration(domain_size: int, codomain_size: int) -> int:
    """Return the brute-force admissible count for small finite carriers."""
    return sum(1 for _ in iter_admissible_functions(domain_size, codomain_size))
