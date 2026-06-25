from __future__ import annotations

from fractions import Fraction

import pytest

from fts_lab.doctor import find_project_root
from fts_lab.fbt.bayes import (
    AmbiguousMapEstimateError,
    FiniteBayesianDecisionProblem,
    WorldStateRow,
    ZeroMarginalProbabilityError,
    observation_marginal,
    posterior,
    unique_map_estimate,
)
from fts_lab.fbt.decision import expected_fitness, unique_best_observation
from fts_lab.fbt.numerical_example import (
    build_reproduction_result,
    load_numerical_example_config,
    parse_fraction,
    problem_from_config,
)
from fts_lab.manifests import read_json_object


def test_fbt_numerical_appendix_matches_regression_fixture() -> None:
    root = find_project_root()
    config = load_numerical_example_config(root / "experiments/configs/fbt_numerical_example.json")
    expected = read_json_object(root / "tests/fixtures/fbt/numerical_appendix_expected.json")[
        "expected"
    ]
    problem = problem_from_config(config)

    marginals = {
        observation: observation_marginal(problem, observation)
        for observation in problem.observations
    }
    posteriors = {
        observation: posterior(problem, observation) for observation in problem.observations
    }
    fitness = problem.fitness_by_world_state()
    expected_fitness_values = {
        observation: expected_fitness(posteriors[observation], fitness)
        for observation in problem.observations
    }

    assert _labels(marginals) == expected["marginals"]
    assert {key: _labels(value) for key, value in posteriors.items()} == expected["posteriors"]
    assert {
        observation: unique_map_estimate(posteriors[observation])
        for observation in problem.observations
    } == expected["map_estimates"]
    assert _labels(expected_fitness_values) == expected["expected_fitness"]
    assert unique_best_observation(expected_fitness_values) == expected["fitness_winner"]


def test_reproduction_report_is_built_from_same_problem_objects() -> None:
    root = find_project_root()
    config = load_numerical_example_config(root / "experiments/configs/fbt_numerical_example.json")
    problem = problem_from_config(config)
    result = build_reproduction_result(config, problem)

    assert result["results"]["marginals"]["x1"]["label"] == "13/28"
    assert result["results"]["posteriors"]["x2"]["w3"]["label"] == "3/5"
    assert result["results"]["expected_fitness"]["x2"]["label"] == "33/5"
    assert result["results"]["fitness_winner"] == "x2"
    assert result["claim_trace"]["CLM-FBT-APP-004"] == [
        "results.expected_fitness",
        "results.fitness_winner",
    ]


def test_changing_input_table_changes_computed_results() -> None:
    root = find_project_root()
    config = load_numerical_example_config(root / "experiments/configs/fbt_numerical_example.json")
    changed_config = dict(config)
    changed_rows = [dict(row) for row in config["world_states"]]
    changed_first_likelihoods = dict(changed_rows[0]["likelihoods"])
    changed_first_likelihoods["x1"] = "1/2"
    changed_first_likelihoods["x2"] = "1/2"
    changed_rows[0]["likelihoods"] = changed_first_likelihoods
    changed_config["world_states"] = changed_rows

    baseline = problem_from_config(config)
    changed = problem_from_config(changed_config)

    assert observation_marginal(baseline, "x1") == Fraction(13, 28)
    assert observation_marginal(changed, "x1") != Fraction(13, 28)


def test_map_tie_raises_without_hidden_policy() -> None:
    with pytest.raises(AmbiguousMapEstimateError, match="ASM-FBT-0001"):
        unique_map_estimate({"w1": Fraction(1, 2), "w2": Fraction(1, 2)})


def test_zero_marginal_observation_raises_without_fabricating_posterior() -> None:
    problem = FiniteBayesianDecisionProblem(
        observations=("x1", "x2"),
        world_rows=(
            WorldStateRow(
                world_state="w1",
                prior=Fraction(1, 1),
                likelihoods=(("x1", Fraction(1, 1)), ("x2", Fraction(0, 1))),
                fitness=Fraction(1, 1),
            ),
        ),
    )

    with pytest.raises(ZeroMarginalProbabilityError):
        posterior(problem, "x2")


def test_fraction_parser_rejects_invalid_rationals() -> None:
    with pytest.raises(ValueError, match="Invalid rational"):
        parse_fraction("not-a-rational")


def _labels(values: dict[str, Fraction]) -> dict[str, str]:
    return {
        key: str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
        for key, value in values.items()
    }
