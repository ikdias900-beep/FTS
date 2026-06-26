"""Exact finite Bayesian calculations for FBT appendix reproduction."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from fractions import Fraction


class FBTModelError(ValueError):
    """Raised when an FBT finite decision problem is ill-formed."""


class ZeroMarginalProbabilityError(FBTModelError):
    """Raised when Bayes normalization would divide by zero."""


class AmbiguousMapEstimateError(FBTModelError):
    """Raised when a posterior has no unique MAP estimate."""


@dataclass(frozen=True)
class WorldStateRow:
    """One immutable source-table row for a finite Bayesian decision problem."""

    world_state: str
    prior: Fraction
    likelihoods: tuple[tuple[str, Fraction], ...]
    fitness: Fraction

    def likelihood_for(self, observation: str) -> Fraction:
        """Return p(observation | world_state)."""
        for candidate, value in self.likelihoods:
            if candidate == observation:
                return value
        raise FBTModelError(
            f"World state {self.world_state!r} has no likelihood for {observation!r}"
        )


@dataclass(frozen=True)
class FiniteBayesianDecisionProblem:
    """Immutable exact finite Bayesian decision problem."""

    observations: tuple[str, ...]
    world_rows: tuple[WorldStateRow, ...]

    def __post_init__(self) -> None:
        _require_unique_nonempty("observations", self.observations)
        world_states = tuple(row.world_state for row in self.world_rows)
        _require_unique_nonempty("world_states", world_states)

        prior_sum = sum((row.prior for row in self.world_rows), Fraction(0, 1))
        if prior_sum != 1:
            raise FBTModelError(f"Prior probabilities must sum to 1, got {prior_sum}")

        observation_set = set(self.observations)
        for row in self.world_rows:
            if row.prior < 0:
                raise FBTModelError(f"Prior for {row.world_state!r} must be non-negative")
            likelihood_observations = tuple(observation for observation, _ in row.likelihoods)
            _require_unique_nonempty(f"likelihoods for {row.world_state}", likelihood_observations)
            if set(likelihood_observations) != observation_set:
                raise FBTModelError(
                    f"Likelihood observations for {row.world_state!r} must match "
                    f"{self.observations!r}"
                )
            for observation, likelihood in row.likelihoods:
                if likelihood < 0:
                    raise FBTModelError(
                        f"Likelihood p({observation!r} | {row.world_state!r}) must be non-negative"
                    )
            likelihood_sum = sum((value for _, value in row.likelihoods), Fraction(0, 1))
            if likelihood_sum != 1:
                raise FBTModelError(
                    f"Likelihoods for {row.world_state!r} must sum to 1, got {likelihood_sum}"
                )
            if row.fitness < 0:
                raise FBTModelError(f"Fitness for {row.world_state!r} must be non-negative")

    def world_states(self) -> tuple[str, ...]:
        """Return world-state IDs in source-table order."""
        return tuple(row.world_state for row in self.world_rows)

    def fitness_by_world_state(self) -> dict[str, Fraction]:
        """Return exact fitness values keyed by world-state ID."""
        return {row.world_state: row.fitness for row in self.world_rows}


def observation_marginal(
    problem: FiniteBayesianDecisionProblem,
    observation: str,
) -> Fraction:
    """Compute P(observation) by marginalizing over world states."""
    _require_observation(problem, observation)
    return sum(
        (row.likelihood_for(observation) * row.prior for row in problem.world_rows),
        Fraction(0, 1),
    )


def posterior(
    problem: FiniteBayesianDecisionProblem,
    observation: str,
) -> dict[str, Fraction]:
    """Compute p(world_state | observation) by exact Bayes normalization."""
    marginal = observation_marginal(problem, observation)
    if marginal == 0:
        raise ZeroMarginalProbabilityError(
            f"Observation {observation!r} has zero marginal probability"
        )
    return {
        row.world_state: (row.likelihood_for(observation) * row.prior) / marginal
        for row in problem.world_rows
    }


def unique_map_estimate(posterior_distribution: Mapping[str, Fraction]) -> str:
    """Return the unique MAP estimate, raising if the posterior has a tie."""
    if not posterior_distribution:
        raise FBTModelError("Cannot compute a MAP estimate for an empty posterior")
    max_probability = max(posterior_distribution.values())
    winners = tuple(
        world_state
        for world_state, probability in posterior_distribution.items()
        if probability == max_probability
    )
    if len(winners) != 1:
        raise AmbiguousMapEstimateError(
            "MAP estimate is ambiguous; unresolved ASM-FBT-0001 forbids tie-breaking"
        )
    return winners[0]


def _require_observation(problem: FiniteBayesianDecisionProblem, observation: str) -> None:
    if observation not in problem.observations:
        raise FBTModelError(f"Unknown observation {observation!r}")


def _require_unique_nonempty(name: str, values: tuple[str, ...]) -> None:
    if not values:
        raise FBTModelError(f"{name} must be non-empty")
    if any(not value for value in values):
        raise FBTModelError(f"{name} must not contain empty IDs")
    if len(set(values)) != len(values):
        raise FBTModelError(f"{name} must not contain duplicates")
