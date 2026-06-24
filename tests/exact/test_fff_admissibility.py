from __future__ import annotations

import pytest

from fts_lab.fff.admissibility import (
    admissible_count,
    count_admissible_by_enumeration,
    is_admissible,
    iter_admissible_functions,
)
from fts_lab.fff.functions import count_all_functions, iter_functions, validate_function


@pytest.mark.parametrize(
    ("domain_size", "codomain_size", "expected"),
    [
        (1, 1, 1),
        (1, 2, 1),
        (2, 2, 3),
        (3, 2, 7),
        (2, 3, 5),
    ],
)
def test_admissible_formula_known_cases(
    domain_size: int,
    codomain_size: int,
    expected: int,
) -> None:
    assert admissible_count(domain_size, codomain_size) == expected


@pytest.mark.parametrize("domain_size", range(1, 5))
@pytest.mark.parametrize("codomain_size", range(1, 5))
def test_admissible_formula_matches_bruteforce(
    domain_size: int,
    codomain_size: int,
) -> None:
    assert count_admissible_by_enumeration(domain_size, codomain_size) == admissible_count(
        domain_size,
        codomain_size,
    )


def test_iter_functions_is_lazy_tuple_enumerator() -> None:
    iterator = iter_functions(2, 2)
    assert next(iterator) == (0, 0)
    assert next(iterator) == (0, 1)


def test_count_all_functions() -> None:
    assert count_all_functions(3, 2) == 8


def test_is_admissible_uses_zero_based_maximum() -> None:
    assert is_admissible((0, 2, 1), 3)
    assert not is_admissible((0, 1, 1), 3)


def test_iter_admissible_functions_contains_only_maximum_attainers() -> None:
    assert list(iter_admissible_functions(2, 2)) == [(0, 1), (1, 0), (1, 1)]


@pytest.mark.parametrize(
    ("function", "codomain_size", "domain_size"),
    [
        ((0, 2), 2, 2),
        ((0,), 2, 2),
        ((), 2, None),
    ],
)
def test_validate_function_rejects_invalid_values_or_lengths(
    function: tuple[int, ...],
    codomain_size: int,
    domain_size: int | None,
) -> None:
    with pytest.raises(ValueError):
        validate_function(function, codomain_size, domain_size=domain_size)


@pytest.mark.parametrize(("domain_size", "codomain_size"), [(0, 1), (1, 0), (-1, 2)])
def test_admissible_count_rejects_invalid_sizes(domain_size: int, codomain_size: int) -> None:
    with pytest.raises(ValueError):
        admissible_count(domain_size, codomain_size)
