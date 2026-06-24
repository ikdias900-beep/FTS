"""Finite function enumeration utilities for FFF Stage 1."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from itertools import product

type FunctionTuple = tuple[int, ...]


def require_positive_size(name: str, value: int) -> None:
    """Reject non-positive finite carrier sizes."""
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")


def require_positive_sizes(domain_size: int, codomain_size: int) -> None:
    """Reject non-positive domain or codomain sizes."""
    require_positive_size("domain_size", domain_size)
    require_positive_size("codomain_size", codomain_size)


def count_all_functions(domain_size: int, codomain_size: int) -> int:
    """Return the number of functions from an n-element set to an m-element set."""
    require_positive_sizes(domain_size, codomain_size)
    return int(codomain_size**domain_size)


def iter_functions(domain_size: int, codomain_size: int) -> Iterator[FunctionTuple]:
    """Yield all functions as tuples, lazily and in lexicographic order."""
    require_positive_sizes(domain_size, codomain_size)
    yield from product(range(codomain_size), repeat=domain_size)


def validate_function(
    function: Sequence[int],
    codomain_size: int,
    *,
    domain_size: int | None = None,
) -> FunctionTuple:
    """Validate and normalize a finite function tuple."""
    require_positive_size("codomain_size", codomain_size)
    values = tuple(function)
    if domain_size is not None:
        require_positive_size("domain_size", domain_size)
        if len(values) != domain_size:
            raise ValueError(f"function length must be {domain_size}, got {len(values)}")
    elif not values:
        raise ValueError("function must be non-empty")

    for value in values:
        if value < 0 or value >= codomain_size:
            raise ValueError(f"function values must be in 0..{codomain_size - 1}, got {value}")
    return values
