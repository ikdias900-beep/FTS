"""Command-line interface for FTS Lab infrastructure."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from fts_lab.doctor import find_project_root, run_doctor
from fts_lab.manifests import ManifestError, validate_manifest_file
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
    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
