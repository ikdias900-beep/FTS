"""Exact finite companions for Stage 1 FFF structures."""

from fts_lab.fff.admissibility import (
    admissible_count,
    count_admissible_by_enumeration,
    is_admissible,
    iter_admissible_functions,
)
from fts_lab.fff.cyclic_groups import (
    count_admissible_cyclic_homomorphisms_by_enumeration,
    count_cyclic_homomorphisms_by_enumeration,
    cyclic_homomorphism_count_formula,
    is_cyclic_homomorphism,
    source_cyclic_ratio,
)
from fts_lab.fff.functions import FunctionTuple, count_all_functions, iter_functions
from fts_lab.fff.total_orders import (
    count_total_order_witnesses_by_enumeration,
    count_unique_total_order_homomorphisms_by_enumeration,
    is_order_preserving,
    is_order_reversing,
    orientation_witnesses,
    source_total_order_ratio,
    source_total_order_witness_count,
    unique_total_order_homomorphism_count,
    unique_total_order_ratio,
)

__all__ = [
    "FunctionTuple",
    "admissible_count",
    "count_admissible_by_enumeration",
    "count_admissible_cyclic_homomorphisms_by_enumeration",
    "count_all_functions",
    "count_cyclic_homomorphisms_by_enumeration",
    "count_total_order_witnesses_by_enumeration",
    "count_unique_total_order_homomorphisms_by_enumeration",
    "cyclic_homomorphism_count_formula",
    "is_admissible",
    "is_cyclic_homomorphism",
    "is_order_preserving",
    "is_order_reversing",
    "iter_admissible_functions",
    "iter_functions",
    "orientation_witnesses",
    "source_cyclic_ratio",
    "source_total_order_ratio",
    "source_total_order_witness_count",
    "unique_total_order_homomorphism_count",
    "unique_total_order_ratio",
]
