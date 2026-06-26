"""Exact expected-fitness calculations for FBT appendix reproduction."""

from __future__ import annotations

from collections.abc import Mapping
from fractions import Fraction

from fts_lab.fbt.bayes import FBTModelError


class AmbiguousFitnessDecisionError(FBTModelError):
    """Raised when expected fitness has no unique maximizer."""


def expected_fitness(
    posterior_distribution: Mapping[str, Fraction],
    fitness_by_world_state: Mapping[str, Fraction],
) -> Fraction:
    """Compute expected fitness by weighting fitness with posterior probabilities."""
    if not posterior_distribution:
        raise FBTModelError("Cannot compute expected fitness for an empty posterior")
    missing = sorted(set(posterior_distribution) - set(fitness_by_world_state))
    if missing:
        raise FBTModelError(f"Missing fitness values for world states: {missing}")
    return sum(
        (
            probability * fitness_by_world_state[world_state]
            for world_state, probability in posterior_distribution.items()
        ),
        Fraction(0, 1),
    )


def unique_best_observation(expected_fitness_by_observation: Mapping[str, Fraction]) -> str:
    """Return the observation with unique maximum expected fitness."""
    if not expected_fitness_by_observation:
        raise FBTModelError("Cannot choose from an empty expected-fitness mapping")
    max_fitness = max(expected_fitness_by_observation.values())
    winners = tuple(
        observation
        for observation, value in expected_fitness_by_observation.items()
        if value == max_fitness
    )
    if len(winners) != 1:
        raise AmbiguousFitnessDecisionError("Expected-fitness decision is ambiguous")
    return winners[0]
