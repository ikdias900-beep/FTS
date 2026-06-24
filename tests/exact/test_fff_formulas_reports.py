from __future__ import annotations

from fractions import Fraction

import pytest

from fts_lab.fff.formulas import (
    admissible_denominator,
    exact_ratio,
    source_cyclic_homomorphism_ratio,
    source_total_order_witness_ratio,
    unique_total_order_homomorphism_ratio,
)
from fts_lab.fff.reports import CountReport


def test_exact_ratio_reduces_fraction() -> None:
    assert exact_ratio(2, 4) == Fraction(1, 2)


@pytest.mark.parametrize(("numerator", "denominator"), [(-1, 1), (1, 0)])
def test_exact_ratio_rejects_invalid_inputs(numerator: int, denominator: int) -> None:
    with pytest.raises(ValueError):
        exact_ratio(numerator, denominator)


def test_formula_ratios_are_directly_exposed() -> None:
    assert admissible_denominator(2, 2) == 3
    assert source_total_order_witness_ratio(2, 2) == Fraction(4, 3)
    assert unique_total_order_homomorphism_ratio(2, 2) == Fraction(1, 1)
    assert source_cyclic_homomorphism_ratio(2, 2) == Fraction(2, 3)


def test_count_report_as_dict_is_json_compatible() -> None:
    report = CountReport(
        structure="total_order",
        domain_size=2,
        codomain_size=2,
        numerator=4,
        denominator=3,
        ratio=Fraction(4, 3),
        task_ids=("TASK-001",),
        claim_ids=("CLM-FFF-ORD-001",),
        source_ids=("SRC-FFF-2020",),
        assumption_ids=("ASM-FFF-0001",),
        notes=("source orientation-witness count",),
    )

    assert report.as_dict() == {
        "structure": "total_order",
        "domain_size": 2,
        "codomain_size": 2,
        "numerator": 4,
        "denominator": 3,
        "ratio": {"numerator": 4, "denominator": 3},
        "task_ids": ["TASK-001"],
        "claim_ids": ["CLM-FFF-ORD-001"],
        "source_ids": ["SRC-FFF-2020"],
        "assumption_ids": ["ASM-FFF-0001"],
        "notes": ["source orientation-witness count"],
    }
