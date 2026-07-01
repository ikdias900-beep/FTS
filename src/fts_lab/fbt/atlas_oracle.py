"""Exact finite-cell oracle for Stage 4 FBT atlas design."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from itertools import product

from fts_lab.fbt.bayes import (
    FBTModelError,
    FiniteBayesianDecisionProblem,
    observation_marginal,
    posterior,
)
from fts_lab.fbt.decision import expected_fitness

OBSERVATION_EVALUATED = "evaluated"
ZERO_MARGINAL_UNDEFINED = "zero_marginal_undefined"

MAP_TIE_NONE = "none"
MAP_TIE_SAME_TRUTH_FITNESS = "same_truth_fitness"
MAP_TIE_DISTINCT_TRUTH_FITNESS = "distinct_truth_fitness"

STATUS_BLOCKED_ZERO_MARGINAL = "blocked_zero_marginal"
STATUS_MAP_TIE_POLICY_SENSITIVE = "map_tie_policy_sensitive"
STATUS_FITNESS_ONLY_STRICTLY_DOMINATES_TRUTH = "fitness_only_strictly_dominates_truth"
STATUS_SAME_BEST_OBSERVATION = "same_best_observation"
STATUS_TRUTH_DECISION_TIE = "truth_decision_tie"
STATUS_FITNESS_ONLY_DECISION_TIE = "fitness_only_decision_tie"
STATUS_DIFFERENT_BEST_EQUAL_EXPECTED_FITNESS = "different_best_observation_equal_expected_fitness"


@dataclass(frozen=True)
class ObservationOracleResult:
    """Exact per-observation oracle output for a finite FBT decision problem."""

    observation: str
    marginal: Fraction
    posterior: tuple[tuple[str, Fraction], ...]
    map_estimates: tuple[str, ...]
    map_fitness_values: tuple[tuple[str, Fraction], ...]
    truth_score_values: tuple[Fraction, ...]
    expected_fitness: Fraction | None
    status: str
    map_tie_kind: str

    def posterior_dict(self) -> dict[str, Fraction]:
        """Return the posterior as a deterministic mapping copy."""
        return dict(self.posterior)

    def map_fitness_dict(self) -> dict[str, Fraction]:
        """Return MAP-estimate fitness values as a deterministic mapping copy."""
        return dict(self.map_fitness_values)


@dataclass(frozen=True)
class CellOracleResult:
    """Exact finite-cell oracle output for the approved Stage 4 primary comparison."""

    offered_observations: tuple[str, ...]
    observation_results: tuple[ObservationOracleResult, ...]
    status: str
    fitness_only_best_observations: tuple[str, ...]
    truth_map_best_observations: tuple[str, ...]
    possible_truth_map_best_observation_sets: tuple[tuple[str, ...], ...]
    possible_comparison_statuses: tuple[str, ...]

    def observation_result(self, observation: str) -> ObservationOracleResult:
        """Return one per-observation result by ID."""
        for result in self.observation_results:
            if result.observation == observation:
                return result
        raise FBTModelError(f"Unknown evaluated observation {observation!r}")


def map_estimates(posterior_distribution: Mapping[str, Fraction]) -> tuple[str, ...]:
    """Return all MAP maximizers without choosing a tie-break policy."""
    if not posterior_distribution:
        raise FBTModelError("Cannot compute a MAP estimate set for an empty posterior")
    max_probability = max(posterior_distribution.values())
    return tuple(
        world_state
        for world_state, probability in posterior_distribution.items()
        if probability == max_probability
    )


def evaluate_observation(
    problem: FiniteBayesianDecisionProblem,
    observation: str,
) -> ObservationOracleResult:
    """Evaluate one observation under approved Stage 4 edge-case policies."""
    marginal = observation_marginal(problem, observation)
    if marginal == 0:
        return ObservationOracleResult(
            observation=observation,
            marginal=marginal,
            posterior=(),
            map_estimates=(),
            map_fitness_values=(),
            truth_score_values=(),
            expected_fitness=None,
            status=ZERO_MARGINAL_UNDEFINED,
            map_tie_kind=MAP_TIE_NONE,
        )

    posterior_distribution = posterior(problem, observation)
    winners = map_estimates(posterior_distribution)
    fitness_by_world_state = problem.fitness_by_world_state()
    winner_fitness_pairs = tuple(
        (world_state, fitness_by_world_state[world_state]) for world_state in winners
    )
    truth_scores = _unique_fractions(value for _, value in winner_fitness_pairs)
    return ObservationOracleResult(
        observation=observation,
        marginal=marginal,
        posterior=tuple(posterior_distribution.items()),
        map_estimates=winners,
        map_fitness_values=winner_fitness_pairs,
        truth_score_values=truth_scores,
        expected_fitness=expected_fitness(posterior_distribution, fitness_by_world_state),
        status=OBSERVATION_EVALUATED,
        map_tie_kind=_map_tie_kind(winners, truth_scores),
    )


def evaluate_primary_cell(
    problem: FiniteBayesianDecisionProblem,
    offered_observations: Sequence[str] | None = None,
) -> CellOracleResult:
    """Evaluate the approved primary comparison for one finite atlas cell."""
    offered = tuple(offered_observations or problem.observations)
    _require_offered_observations(problem, offered)
    observation_results = tuple(
        evaluate_observation(problem, observation) for observation in offered
    )

    if any(result.status == ZERO_MARGINAL_UNDEFINED for result in observation_results):
        return CellOracleResult(
            offered_observations=offered,
            observation_results=observation_results,
            status=STATUS_BLOCKED_ZERO_MARGINAL,
            fitness_only_best_observations=(),
            truth_map_best_observations=(),
            possible_truth_map_best_observation_sets=(),
            possible_comparison_statuses=(STATUS_BLOCKED_ZERO_MARGINAL,),
        )

    expected_by_observation = {
        result.observation: _require_expected_fitness(result) for result in observation_results
    }
    fitness_only_best = _best_keys(expected_by_observation)
    possible_truth_sets: list[tuple[str, ...]] = []
    possible_statuses: list[str] = []
    score_options = tuple(
        tuple((result.observation, score) for score in result.truth_score_values)
        for result in observation_results
    )

    for score_choice in product(*score_options):
        truth_scores = dict(score_choice)
        truth_best = _best_keys(truth_scores)
        possible_truth_sets.append(truth_best)
        possible_statuses.append(
            _comparison_status(
                truth_best_observations=truth_best,
                fitness_only_best_observations=fitness_only_best,
                expected_fitness_by_observation=expected_by_observation,
            )
        )

    truth_sets = _unique_tuples(possible_truth_sets)
    statuses = _unique_strings(possible_statuses)
    variable_map_tie = any(
        result.map_tie_kind == MAP_TIE_DISTINCT_TRUTH_FITNESS for result in observation_results
    )
    if variable_map_tie and (len(truth_sets) > 1 or len(statuses) > 1):
        status = STATUS_MAP_TIE_POLICY_SENSITIVE
    elif len(statuses) == 1:
        status = statuses[0]
    else:
        status = STATUS_MAP_TIE_POLICY_SENSITIVE

    return CellOracleResult(
        offered_observations=offered,
        observation_results=observation_results,
        status=status,
        fitness_only_best_observations=fitness_only_best,
        truth_map_best_observations=truth_sets[0] if len(truth_sets) == 1 else (),
        possible_truth_map_best_observation_sets=truth_sets,
        possible_comparison_statuses=statuses,
    )


def _comparison_status(
    *,
    truth_best_observations: tuple[str, ...],
    fitness_only_best_observations: tuple[str, ...],
    expected_fitness_by_observation: Mapping[str, Fraction],
) -> str:
    if len(truth_best_observations) > 1:
        return STATUS_TRUTH_DECISION_TIE
    if len(fitness_only_best_observations) > 1:
        return STATUS_FITNESS_ONLY_DECISION_TIE

    truth_best = truth_best_observations[0]
    fitness_best = fitness_only_best_observations[0]
    if truth_best == fitness_best:
        return STATUS_SAME_BEST_OBSERVATION

    fitness_expected = expected_fitness_by_observation[fitness_best]
    truth_expected = expected_fitness_by_observation[truth_best]
    if fitness_expected > truth_expected:
        return STATUS_FITNESS_ONLY_STRICTLY_DOMINATES_TRUTH
    if fitness_expected == truth_expected:
        return STATUS_DIFFERENT_BEST_EQUAL_EXPECTED_FITNESS
    raise FBTModelError("Fitness-only best observation cannot have lower expected fitness")


def _map_tie_kind(winners: tuple[str, ...], truth_scores: tuple[Fraction, ...]) -> str:
    if len(winners) == 1:
        return MAP_TIE_NONE
    if len(truth_scores) == 1:
        return MAP_TIE_SAME_TRUTH_FITNESS
    return MAP_TIE_DISTINCT_TRUTH_FITNESS


def _best_keys(values: Mapping[str, Fraction]) -> tuple[str, ...]:
    if not values:
        raise FBTModelError("Cannot choose best keys from an empty mapping")
    best_value = max(values.values())
    return tuple(key for key, value in values.items() if value == best_value)


def _require_expected_fitness(result: ObservationOracleResult) -> Fraction:
    if result.expected_fitness is None:
        raise FBTModelError(f"Observation {result.observation!r} has no expected fitness value")
    return result.expected_fitness


def _require_offered_observations(
    problem: FiniteBayesianDecisionProblem,
    offered_observations: tuple[str, ...],
) -> None:
    if not offered_observations:
        raise FBTModelError("offered_observations must be non-empty")
    if len(set(offered_observations)) != len(offered_observations):
        raise FBTModelError("offered_observations must not contain duplicates")
    unknown = sorted(set(offered_observations) - set(problem.observations))
    if unknown:
        raise FBTModelError(f"Unknown offered observations: {unknown}")


def _unique_fractions(values: Iterable[Fraction]) -> tuple[Fraction, ...]:
    unique: list[Fraction] = []
    for value in values:
        if value not in unique:
            unique.append(value)
    return tuple(unique)


def _unique_strings(values: Iterable[str]) -> tuple[str, ...]:
    unique: list[str] = []
    for value in values:
        if value not in unique:
            unique.append(value)
    return tuple(unique)


def _unique_tuples(values: Iterable[tuple[str, ...]]) -> tuple[tuple[str, ...], ...]:
    unique: list[tuple[str, ...]] = []
    for value in values:
        if value not in unique:
            unique.append(value)
    return tuple(unique)
