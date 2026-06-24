"""Small structured reports for FFF exact counts."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any


@dataclass(frozen=True)
class CountReport:
    """Traceable exact count report for CLI and future manifests."""

    structure: str
    domain_size: int
    codomain_size: int
    numerator: int
    denominator: int
    ratio: Fraction
    task_ids: tuple[str, ...]
    claim_ids: tuple[str, ...]
    source_ids: tuple[str, ...]
    assumption_ids: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        """Return a deterministic JSON-compatible dictionary."""
        return {
            "structure": self.structure,
            "domain_size": self.domain_size,
            "codomain_size": self.codomain_size,
            "numerator": self.numerator,
            "denominator": self.denominator,
            "ratio": {
                "numerator": self.ratio.numerator,
                "denominator": self.ratio.denominator,
            },
            "task_ids": list(self.task_ids),
            "claim_ids": list(self.claim_ids),
            "source_ids": list(self.source_ids),
            "assumption_ids": list(self.assumption_ids),
            "notes": list(self.notes),
        }
