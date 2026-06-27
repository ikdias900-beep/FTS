"""Permutation-group helpers for FFF Stage 3.

These utilities implement source-explicit finite checks from the Stage 3 draft spec.
They do not resolve the pending independent-review questions in ``ASM-FFF-0002``.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Mapping, Sequence
from fractions import Fraction
from itertools import permutations
from math import factorial

from fts_lab.fff.admissibility import admissible_count
from fts_lab.fff.functions import FunctionTuple, require_positive_size, validate_function

type Permutation = tuple[int, ...]

MINIMUM_SOURCE_PERMUTATION_DEGREE = 5


def validate_permutation(
    permutation: Sequence[int],
    degree: int | None = None,
) -> Permutation:
    """Validate and normalize a permutation over canonical zero-based labels."""
    values = tuple(permutation)
    if degree is None:
        if not values:
            raise ValueError("permutation must be non-empty")
        degree = len(values)

    require_positive_size("degree", degree)
    if len(values) != degree:
        raise ValueError(f"permutation length must be {degree}, got {len(values)}")

    expected = set(range(degree))
    actual = set(values)
    if actual != expected:
        raise ValueError(f"permutation values must be exactly 0..{degree - 1}, got {values}")
    return values


def identity_permutation(degree: int) -> Permutation:
    """Return the identity permutation on ``degree`` labels."""
    require_positive_size("degree", degree)
    return tuple(range(degree))


def iter_symmetric_group(degree: int) -> Iterator[Permutation]:
    """Yield elements of ``S_degree`` as tuple-valued permutations."""
    require_positive_size("degree", degree)
    yield from permutations(range(degree))


def compose_permutations(left: Sequence[int], right: Sequence[int]) -> Permutation:
    """Return ``left`` after ``right`` using tuple maps ``x -> permutation[x]``."""
    left_values = validate_permutation(left)
    right_values = validate_permutation(right, degree=len(left_values))
    return tuple(left_values[right_values[index]] for index in range(len(left_values)))


def inverse_permutation(permutation: Sequence[int]) -> Permutation:
    """Return the inverse permutation."""
    values = validate_permutation(permutation)
    inverse = [0] * len(values)
    for source, target in enumerate(values):
        inverse[target] = source
    return tuple(inverse)


def apply_permutation(permutation: Sequence[int], element: int) -> int:
    """Apply a permutation to one canonical label."""
    values = validate_permutation(permutation)
    if element < 0 or element >= len(values):
        raise ValueError(f"element must be in 0..{len(values) - 1}, got {element}")
    return values[element]


def conjugate_permutation(conjugator: Sequence[int], permutation: Sequence[int]) -> Permutation:
    """Return the inner conjugate ``conjugator * permutation * conjugator^-1``."""
    conjugator_values = validate_permutation(conjugator)
    permutation_values = validate_permutation(permutation, degree=len(conjugator_values))
    return compose_permutations(
        conjugator_values,
        compose_permutations(permutation_values, inverse_permutation(conjugator_values)),
    )


def is_second_order_respectful(
    function: Sequence[int],
    group_element: Sequence[int],
    phi_image: Sequence[int],
    *,
    codomain_size: int | None = None,
) -> bool:
    """Check the source action law ``f(g.x) = phi(g).f(x)`` for one group element."""
    group_values = validate_permutation(group_element)
    phi_values = validate_permutation(phi_image, degree=codomain_size)
    values = validate_function(
        function,
        len(phi_values),
        domain_size=len(group_values),
    )

    for source in range(len(group_values)):
        left = values[group_values[source]]
        right = phi_values[values[source]]
        if left != right:
            return False
    return True


def is_second_order_homomorphism(
    function: Sequence[int],
    group_elements: Iterable[Sequence[int]],
    phi_images: Mapping[Permutation, Sequence[int]],
    *,
    codomain_size: int | None = None,
) -> bool:
    """Check the source action law for every supplied group element."""
    normalized_group = _validate_group_elements(group_elements)
    if codomain_size is None:
        first_phi = _lookup_phi_image(phi_images, normalized_group[0])
        codomain_size = len(validate_permutation(first_phi))

    validate_function(function, codomain_size, domain_size=len(normalized_group[0]))
    for group_element in normalized_group:
        phi_image = _lookup_phi_image(phi_images, group_element)
        if not is_second_order_respectful(
            function,
            group_element,
            phi_image,
            codomain_size=codomain_size,
        ):
            return False
    return True


def source_permutation_respectful_count(degree: int) -> int:
    """Return the source Appendix A.3 count ``2*n + n!`` for ``n >= 5``."""
    require_source_permutation_degree(degree)
    return int(2 * degree + factorial(degree))


def source_permutation_ratio(degree: int) -> Fraction:
    """Return the source count over the admissible payoff-function denominator."""
    return Fraction(
        source_permutation_respectful_count(degree),
        admissible_count(degree, degree),
    )


def require_source_permutation_degree(degree: int) -> None:
    """Reject degrees outside the source theorem's stated ``n >= 5`` scope."""
    require_positive_size("degree", degree)
    if degree < MINIMUM_SOURCE_PERMUTATION_DEGREE:
        raise ValueError(
            "source permutation theorem formula is specified for "
            f"n >= {MINIMUM_SOURCE_PERMUTATION_DEGREE}, got {degree}"
        )


def constant_function(domain_size: int, value: int, codomain_size: int) -> FunctionTuple:
    """Return a validated constant function over canonical finite carriers."""
    require_positive_size("domain_size", domain_size)
    validate_function((value,), codomain_size, domain_size=1)
    return tuple(value for _ in range(domain_size))


def _validate_group_elements(group_elements: Iterable[Sequence[int]]) -> tuple[Permutation, ...]:
    normalized: list[Permutation] = []
    degree: int | None = None
    for group_element in group_elements:
        if degree is None:
            values = validate_permutation(group_element)
            degree = len(values)
        else:
            values = validate_permutation(group_element, degree=degree)
        normalized.append(values)

    if not normalized:
        raise ValueError("group_elements must be non-empty")
    return tuple(normalized)


def _lookup_phi_image(
    phi_images: Mapping[Permutation, Sequence[int]],
    group_element: Permutation,
) -> Sequence[int]:
    try:
        return phi_images[group_element]
    except KeyError as exc:
        raise ValueError(f"missing phi image for group element {group_element}") from exc
