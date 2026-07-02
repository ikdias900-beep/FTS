"""Command-line interface for FTS Lab infrastructure."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path

from fts_lab.doctor import find_project_root, run_doctor
from fts_lab.fbt.atlas_grid import run_fbt_atlas_grid_v0
from fts_lab.fbt.atlas_v1 import run_fbt_atlas_v1_raw_cells
from fts_lab.fbt.atlas_v1_aggregate import run_fbt_atlas_v1_aggregate
from fts_lab.fbt.numerical_example import run_fbt_numerical_example
from fts_lab.fff.admissibility import admissible_count
from fts_lab.fff.cyclic_groups import (
    count_admissible_cyclic_homomorphisms_by_enumeration,
    cyclic_homomorphism_count_formula,
    source_cyclic_ratio,
)
from fts_lab.fff.publication_tables import run_stage1_publication_tables
from fts_lab.fff.sweeps import run_stage1_sweep
from fts_lab.fff.total_orders import (
    source_total_order_ratio,
    source_total_order_witness_count,
    unique_total_order_homomorphism_count,
    unique_total_order_ratio,
)
from fts_lab.manifests import ManifestError, validate_manifest_file
from fts_lab.release_capsules import ReleaseCapsuleError, validate_release_capsule
from fts_lab.smoke import run_smoke


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fts")
    subcommands = parser.add_subparsers(dest="command", required=True)

    doctor = subcommands.add_parser("doctor", help="Check repository health")
    doctor.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    doctor.add_argument(
        "--release-check",
        action="store_true",
        help="Treat pending release decisions as errors",
    )

    smoke = subcommands.add_parser("reproduce-smoke", help="Run deterministic smoke reproduction")
    smoke.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to smoke config JSON",
    )

    validate = subcommands.add_parser("validate-manifest", help="Validate a manifest and checksums")
    validate.add_argument("path", type=Path, help="Manifest path")

    validate_capsule = subcommands.add_parser(
        "validate-release-capsule",
        help="Validate a release capsule against its local checksums.txt inventory",
    )
    validate_capsule.add_argument("path", type=Path, help="Release capsule root")

    fbt = subcommands.add_parser("fbt", help="Run exact FBT Stage 2 helpers")
    fbt_subcommands = fbt.add_subparsers(dest="fbt_command", required=True)

    reproduce_numerical = fbt_subcommands.add_parser(
        "reproduce-numerical-example",
        help="Reproduce the FBT numerical appendix with exact arithmetic",
    )
    reproduce_numerical.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to the FBT numerical example source-table JSON",
    )
    atlas_grid_v0 = fbt_subcommands.add_parser(
        "atlas-grid-v0-smoke",
        help="Run the manifest-backed Stage 4 FBT atlas grid v0 smoke enumeration",
    )
    atlas_grid_v0.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to the FBT atlas grid v0 config JSON",
    )
    atlas_v1_raw_cells = fbt_subcommands.add_parser(
        "atlas-v1-raw-cells",
        help="Run the manifest-backed Stage 4 FBT atlas v1 raw-cell engine",
    )
    atlas_v1_raw_cells.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to the FBT atlas v1 draft config JSON",
    )
    atlas_v1_aggregate = fbt_subcommands.add_parser(
        "atlas-v1-aggregate",
        help="Build Stage 4 FBT atlas v1 aggregate/report outputs from a raw-cell artifact",
    )
    atlas_v1_aggregate.add_argument(
        "--raw-cells",
        type=Path,
        required=True,
        help="Path to a manifest-backed FBT atlas v1 raw-cell JSON artifact",
    )

    fff = subcommands.add_parser("fff", help="Run exact FFF Stage 1 helpers")
    fff_subcommands = fff.add_subparsers(dest="fff_command", required=True)

    admissible = fff_subcommands.add_parser(
        "admissible-count",
        help="Count admissible payoff functions",
    )
    _add_size_arguments(admissible)

    total_order = fff_subcommands.add_parser(
        "total-order-count",
        help="Count admissible monotone total-order functions",
    )
    _add_size_arguments(total_order)
    total_order.add_argument(
        "--mode",
        choices=("source-witness", "unique"),
        default="source-witness",
        help="Use source orientation witnesses or unique functions",
    )

    cyclic = fff_subcommands.add_parser(
        "cyclic-count",
        help="Count cyclic-group homomorphisms",
    )
    _add_size_arguments(cyclic)
    cyclic.add_argument(
        "--admissible-only",
        action="store_true",
        help="Audit count after admissibility filtering",
    )

    sweep = fff_subcommands.add_parser(
        "sweep",
        help="Run manifest-backed Stage 1 finite count sweep",
    )
    sweep.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to Stage 1 sweep config JSON",
    )

    publication_tables = fff_subcommands.add_parser(
        "publication-tables",
        help="Build derived Stage 1 publication tables from a sweep manifest",
    )
    publication_tables.add_argument(
        "--sweep-manifest",
        type=Path,
        required=True,
        help="Path to a validated Stage 1 sweep manifest",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "doctor":
        return run_doctor(json_output=args.json, release_check=args.release_check)

    if args.command == "reproduce-smoke":
        try:
            result = run_smoke(
                args.config,
                command="uv run fts reproduce-smoke"
                if args.config is None
                else f"uv run fts reproduce-smoke --config {args.config}",
            )
        except (OSError, ValueError, ManifestError) as exc:
            print(f"smoke failed: {exc}")
            return 1
        print(f"payload_checksum={result['payload_checksum']}")
        print(f"payload_path={result['payload_path']}")
        print(f"manifest_path={result['manifest_path']}")
        return 0

    if args.command == "validate-manifest":
        try:
            validate_manifest_file(args.path, project_root=find_project_root())
        except ManifestError as exc:
            print(f"manifest invalid: {exc}")
            return 1
        print(f"manifest valid: {args.path}")
        return 0

    if args.command == "validate-release-capsule":
        try:
            capsule_validation = validate_release_capsule(args.path)
        except ReleaseCapsuleError as exc:
            print(f"release capsule invalid: {exc}")
            return 1
        print(f"release_capsule_valid={capsule_validation.capsule_root}")
        print(f"checksum_file={capsule_validation.checksum_file}")
        print(f"checked_files={len(capsule_validation.checked_files)}")
        return 0

    if args.command == "fff":
        try:
            return _run_fff_command(args)
        except ValueError as exc:
            print(f"fff failed: {exc}")
            return 1
    if args.command == "fbt":
        try:
            return _run_fbt_command(args)
        except (OSError, ValueError, ManifestError) as exc:
            print(f"fbt failed: {exc}")
            return 1
    raise AssertionError(f"unhandled command: {args.command}")


def _add_size_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("domain_size", type=int, help="Domain size n")
    parser.add_argument("codomain_size", type=int, help="Codomain/payoff size m")


def _run_fff_command(args: argparse.Namespace) -> int:
    if args.fff_command == "sweep":
        result = run_stage1_sweep(
            args.config,
            command="uv run fts fff sweep"
            if args.config is None
            else f"uv run fts fff sweep --config {args.config}",
        )
        print(f"csv_checksum={result['csv_checksum']}")
        print(f"csv_path={result['csv_path']}")
        print(f"manifest_path={result['manifest_path']}")
        print(f"row_count={result['row_count']}")
        return 0

    if args.fff_command == "publication-tables":
        result = run_stage1_publication_tables(
            args.sweep_manifest,
            command=f"uv run fts fff publication-tables --sweep-manifest {args.sweep_manifest}",
        )
        print(f"summary_csv_checksum={result['summary_csv_checksum']}")
        print(f"summary_csv_path={result['summary_csv_path']}")
        print(f"report_checksum={result['report_checksum']}")
        print(f"report_path={result['report_path']}")
        print(f"manifest_path={result['manifest_path']}")
        print(f"row_count={result['row_count']}")
        return 0

    domain_size = args.domain_size
    codomain_size = args.codomain_size
    denominator = admissible_count(domain_size, codomain_size)

    print("task_ids=TASK-001")
    print("source_ids=SRC-FFF-2020")

    if args.fff_command == "admissible-count":
        print("claim_ids=CLM-FFF-ADM-001")
        print(f"count={denominator}")
        return 0

    if args.fff_command == "total-order-count":
        print("claim_ids=CLM-FFF-ORD-001")
        print("assumption_ids=ASM-FFF-0001")
        if args.mode == "source-witness":
            count = source_total_order_witness_count(domain_size, codomain_size)
            ratio = source_total_order_ratio(domain_size, codomain_size)
        else:
            count = unique_total_order_homomorphism_count(domain_size, codomain_size)
            ratio = unique_total_order_ratio(domain_size, codomain_size)
        print(f"mode={args.mode}")
        print(f"count={count}")
        _print_ratio(ratio, denominator=denominator)
        return 0

    if args.fff_command == "cyclic-count":
        print("claim_ids=CLM-FFF-CYC-001,CLM-FFF-CYC-002")
        if args.admissible_only:
            count = count_admissible_cyclic_homomorphisms_by_enumeration(
                domain_size,
                codomain_size,
            )
            ratio = Fraction(count, denominator)
            print("mode=admissible-filtered-audit")
        else:
            count = cyclic_homomorphism_count_formula(domain_size, codomain_size)
            ratio = source_cyclic_ratio(domain_size, codomain_size)
            print("mode=source")
        print(f"count={count}")
        _print_ratio(ratio, denominator=denominator)
        return 0

    raise AssertionError(f"unhandled FFF command: {args.fff_command}")


def _run_fbt_command(args: argparse.Namespace) -> int:
    if args.fbt_command == "reproduce-numerical-example":
        result = run_fbt_numerical_example(
            args.config,
            command="uv run fts fbt reproduce-numerical-example"
            if args.config is None
            else f"uv run fts fbt reproduce-numerical-example --config {args.config}",
        )
        print(f"json_report_checksum={result['json_report_checksum']}")
        print(f"json_report_path={result['json_report_path']}")
        print(f"markdown_report_checksum={result['markdown_report_checksum']}")
        print(f"markdown_report_path={result['markdown_report_path']}")
        print(f"manifest_path={result['manifest_path']}")
        return 0

    if args.fbt_command == "atlas-grid-v0-smoke":
        result = run_fbt_atlas_grid_v0(
            args.config,
            command="uv run fts fbt atlas-grid-v0-smoke"
            if args.config is None
            else f"uv run fts fbt atlas-grid-v0-smoke --config {args.config}",
        )
        print(f"json_report_checksum={result['json_report_checksum']}")
        print(f"json_report_path={result['json_report_path']}")
        print(f"markdown_report_checksum={result['markdown_report_checksum']}")
        print(f"markdown_report_path={result['markdown_report_path']}")
        print(f"manifest_path={result['manifest_path']}")
        print(f"cell_count={result['cell_count']}")
        return 0

    if args.fbt_command == "atlas-v1-raw-cells":
        result = run_fbt_atlas_v1_raw_cells(
            args.config,
            command="uv run fts fbt atlas-v1-raw-cells"
            if args.config is None
            else f"uv run fts fbt atlas-v1-raw-cells --config {args.config}",
        )
        print(f"raw_cell_table_checksum={result['raw_cell_table_checksum']}")
        print(f"raw_cell_table_path={result['raw_cell_table_path']}")
        print(f"manifest_path={result['manifest_path']}")
        print(f"cell_count={result['cell_count']}")
        return 0

    if args.fbt_command == "atlas-v1-aggregate":
        result = run_fbt_atlas_v1_aggregate(
            args.raw_cells,
            command=f"uv run fts fbt atlas-v1-aggregate --raw-cells {args.raw_cells}",
        )
        print(f"json_report_checksum={result['json_report_checksum']}")
        print(f"json_report_path={result['json_report_path']}")
        print(f"markdown_report_checksum={result['markdown_report_checksum']}")
        print(f"markdown_report_path={result['markdown_report_path']}")
        print(f"manifest_path={result['manifest_path']}")
        print(f"cell_count={result['cell_count']}")
        return 0

    raise AssertionError(f"unhandled FBT command: {args.fbt_command}")


def _print_ratio(ratio: Fraction, *, denominator: int) -> None:
    print(f"admissible_denominator={denominator}")
    print(f"ratio={ratio.numerator}/{ratio.denominator}")


if __name__ == "__main__":
    raise SystemExit(main())
