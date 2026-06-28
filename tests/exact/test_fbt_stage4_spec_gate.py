from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_PATH = PROJECT_ROOT / "tests/fixtures/fbt/stage4_fbt_spec_cases.json"
THEOREM_SPEC_PATH = PROJECT_ROOT / "specs/fbt/theorem4_domain.md"
ATLAS_SPEC_PATH = PROJECT_ROOT / "specs/fbt/finite_atlas_design.md"


def test_stage4_fixture_metadata_links_required_ids() -> None:
    fixture = _load_fixture()
    metadata = fixture["metadata"]

    assert metadata["task_id"] == "TASK-004-FBT-ATLAS-SPEC"
    assert metadata["source_id"] == "SRC-FBT-2021"
    assert metadata["epistemic_status"] == "R"
    assert metadata["claim_ids"] == ["CLM-FBT-THM-001", "CLM-FBT-ATLAS-001"]
    assert metadata["assumption_ids"] == [
        "ASM-FBT-0001",
        "ASM-FBT-0002",
        "ASM-FBT-0003",
        "ASM-FBT-0004",
    ]


def test_theorem4_bound_fixture_matches_declared_formula() -> None:
    fixture = _load_fixture()
    for case in fixture["theorem4_bound"]["cases"]:
        abs_x = case["abs_x"]
        same_best = Fraction(case["same_best_territory_probability"])
        lower_bound = Fraction(case["strict_domination_lower_bound"])

        assert same_best == Fraction(2, abs_x - 1)
        assert lower_bound == Fraction(abs_x - 3, abs_x - 1)
        assert same_best + lower_bound == 1
        assert (lower_bound >= 0) is case["nonnegative_lower_bound"]


def test_atlas_design_keeps_grid_counts_distinct_from_theorem_probability() -> None:
    fixture = _load_fixture()
    boundaries = fixture["atlas_design_boundaries"]

    assert (
        boundaries["grid_count_semantics"]
        == "project_defined_grid_frequency_not_source_theorem_probability"
    )
    assert boundaries["primary_source_strategy_family"] == [
        "truth_map",
        "fitness_only_expected",
    ]
    assert "posterior_mean_requires_metric" in boundaries["extension_strategy_families"]


def test_stage4_spec_gate_does_not_add_production_modules() -> None:
    fixture = _load_fixture()
    forbidden_paths = fixture["atlas_design_boundaries"][
        "production_modules_forbidden_in_spec_gate"
    ]

    for relative_path in forbidden_paths:
        assert not (PROJECT_ROOT / relative_path).exists()


def test_stage4_specs_record_open_blockers_and_forbidden_interpretations() -> None:
    theorem_spec = THEOREM_SPEC_PATH.read_text(encoding="utf-8")
    atlas_spec = ATLAS_SPEC_PATH.read_text(encoding="utf-8")

    for required in (
        "ASM-FBT-0001",
        "ASM-FBT-0002",
        "ASM-FBT-0003",
        "ASM-FBT-0004",
        "(abs(X) - 3) / (abs(X) - 1)",
        "finite grid frequency is the theorem probability",
    ):
        assert required in theorem_spec

    for required in (
        "CLM-FBT-ATLAS-001",
        "truth_map",
        "fitness_only_expected",
        "grid frequencies versus theorem probabilities",
    ):
        assert required in atlas_spec


def _load_fixture() -> dict[str, object]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
