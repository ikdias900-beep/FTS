from __future__ import annotations

import json
from collections.abc import Mapping
from fractions import Fraction
from pathlib import Path
from typing import Any, cast

from fts_lab.doctor import find_project_root
from fts_lab.fbt.atlas_oracle import (
    MAP_TIE_DISTINCT_TRUTH_FITNESS,
    MAP_TIE_SAME_TRUTH_FITNESS,
    STATUS_BLOCKED_ZERO_MARGINAL,
    STATUS_FITNESS_ONLY_STRICTLY_DOMINATES_TRUTH,
    STATUS_MAP_TIE_POLICY_SENSITIVE,
    STATUS_SAME_BEST_OBSERVATION,
    ZERO_MARGINAL_UNDEFINED,
    evaluate_primary_cell,
)
from fts_lab.fbt.bayes import FiniteBayesianDecisionProblem, WorldStateRow
from fts_lab.fbt.numerical_example import (
    load_numerical_example_config,
    parse_fraction,
    problem_from_config,
)

FIXTURE_PATH = Path("tests/fixtures/fbt/stage4_fbt_oracle_cases.json")


def test_stage4_oracle_fixture_metadata_links_required_ids() -> None:
    fixture = _load_fixture()
    metadata = cast(dict[str, Any], fixture["metadata"])

    assert metadata["task_id"] == "TASK-004-FBT-ATLAS-ORACLE"
    assert metadata["source_ids"] == ["SRC-FBT-2021"]
    assert metadata["claim_ids"] == ["CLM-FBT-ATLAS-001"]
    assert metadata["assumption_ids"] == [
        "ASM-FBT-0001",
        "ASM-FBT-0002",
        "ASM-FBT-0003",
        "ASM-FBT-0004",
    ]
    assert metadata["epistemic_status"] == "E"


def test_primary_cell_same_best_observation_unique_map() -> None:
    case = _case("same_best_observation_unique_map")
    result = _evaluate_case(case)

    assert result.status == STATUS_SAME_BEST_OBSERVATION
    assert result.fitness_only_best_observations == ("x2",)
    assert result.truth_map_best_observations == ("x2",)
    assert result.possible_comparison_statuses == (STATUS_SAME_BEST_OBSERVATION,)


def test_map_tie_with_same_truth_fitness_is_determined_not_policy_sensitive() -> None:
    case = _case("map_tie_same_truth_fitness")
    result = _evaluate_case(case)
    observation = result.observation_result("x")

    assert result.status == STATUS_SAME_BEST_OBSERVATION
    assert observation.map_estimates == ("w1", "w2")
    assert observation.map_tie_kind == MAP_TIE_SAME_TRUTH_FITNESS
    assert observation.truth_score_values == (Fraction(3, 1),)


def test_map_tie_with_distinct_truth_fitness_is_policy_sensitive() -> None:
    case = _case("map_tie_policy_sensitive")
    result = _evaluate_case(case)
    observation = result.observation_result("x1")

    assert result.status == STATUS_MAP_TIE_POLICY_SENSITIVE
    assert observation.map_tie_kind == MAP_TIE_DISTINCT_TRUTH_FITNESS
    assert observation.map_estimates == ("w_high", "w_low")
    assert result.possible_truth_map_best_observation_sets == (("x1",), ("x2",))


def test_zero_marginal_observation_blocks_dependent_comparison_without_smoothing() -> None:
    case = _case("blocked_zero_marginal")
    result = _evaluate_case(case)
    observation = result.observation_result("x2")

    assert result.status == STATUS_BLOCKED_ZERO_MARGINAL
    assert observation.status == ZERO_MARGINAL_UNDEFINED
    assert observation.marginal == 0
    assert observation.posterior == ()
    assert observation.expected_fitness is None


def test_fixture_case_where_fitness_only_strictly_dominates_truth() -> None:
    case = _case("fitness_only_strictly_dominates_truth")
    result = _evaluate_case(case)

    assert result.status == STATUS_FITNESS_ONLY_STRICTLY_DOMINATES_TRUTH
    assert result.fitness_only_best_observations == ("x2",)
    assert result.truth_map_best_observations == ("x1",)
    assert result.observation_result("x1").expected_fitness == Fraction(11, 2)
    assert result.observation_result("x2").expected_fitness == Fraction(37, 5)


def test_stage2_source_table_is_a_valid_stage4_primary_cell_input() -> None:
    root = find_project_root()
    config = load_numerical_example_config(root / "experiments/configs/fbt_numerical_example.json")
    problem = problem_from_config(config)
    result = evaluate_primary_cell(problem, ("x1", "x2"))

    assert result.status == STATUS_FITNESS_ONLY_STRICTLY_DOMINATES_TRUTH
    assert result.fitness_only_best_observations == ("x2",)
    assert result.truth_map_best_observations == ("x1",)


def _load_fixture() -> dict[str, Any]:
    root = find_project_root()
    return cast(
        dict[str, Any],
        json.loads((root / FIXTURE_PATH).read_text(encoding="utf-8")),
    )


def _case(case_id: str) -> Mapping[str, Any]:
    fixture = _load_fixture()
    cases = fixture["cases"]
    assert isinstance(cases, list)
    for raw_case in cases:
        assert isinstance(raw_case, dict)
        if raw_case["case_id"] == case_id:
            return cast(Mapping[str, Any], raw_case)
    raise AssertionError(f"fixture case not found: {case_id}")


def _evaluate_case(case: Mapping[str, Any]):
    problem = _problem_from_case(case)
    offered = _string_tuple(case, "offered_observations")
    return evaluate_primary_cell(problem, offered)


def _problem_from_case(case: Mapping[str, Any]) -> FiniteBayesianDecisionProblem:
    observations = _string_tuple(case, "observations")
    raw_rows = case["world_states"]
    assert isinstance(raw_rows, list)
    rows: list[WorldStateRow] = []
    for raw_row in raw_rows:
        assert isinstance(raw_row, dict)
        row = cast(Mapping[str, Any], raw_row)
        likelihoods = row["likelihoods"]
        assert isinstance(likelihoods, dict)
        likelihood_mapping = cast(Mapping[str, Any], likelihoods)
        rows.append(
            WorldStateRow(
                world_state=_string_value(row, "id"),
                prior=parse_fraction(_string_value(row, "prior")),
                fitness=parse_fraction(_string_value(row, "fitness")),
                likelihoods=tuple(
                    (
                        observation,
                        parse_fraction(_string_value(likelihood_mapping, observation)),
                    )
                    for observation in observations
                ),
            )
        )
    return FiniteBayesianDecisionProblem(observations=observations, world_rows=tuple(rows))


def _string_tuple(data: Mapping[str, Any], key: str) -> tuple[str, ...]:
    value = data[key]
    assert isinstance(value, list)
    return tuple(cast(str, item) for item in value)


def _string_value(data: Mapping[str, Any], key: str) -> str:
    value = data[key]
    assert isinstance(value, str)
    return value
