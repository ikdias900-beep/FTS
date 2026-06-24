"""Development environment checks for the FTS Lab repository."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from fts_lab import __version__
from fts_lab.manifests import SCHEMA_PATH, canonical_json_text, sha256_file

ACTIVE_TASK = "TASK-001-SWEEP"

REQUIRED_CONTEXT_FILES = (
    "AGENTS.md",
    "01_research_strategy.md",
    "02_stage_tasks_roles.md",
    "tasks/TASK-000_bootstrap_repo.md",
    "tasks/TASK-001_fff_core_orders_cyclic.md",
    "tasks/TASK-001_stage1_sweeps_tables.md",
    "sources/source_map.md",
    "sources/claim_matrix.csv",
    "assumptions/register.md",
)

ARTIFACT_DIRECTORIES = (
    "experiments/manifests",
    "results/raw",
    "results/derived",
    "results/reports",
)


@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    detail: str
    severity: str = "error"


def find_project_root(start: Path | None = None) -> Path:
    """Find the repository root by walking up to AGENTS.md and pyproject.toml."""
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "AGENTS.md").is_file() and (candidate / "pyproject.toml").is_file():
            return candidate
    raise FileNotFoundError("Could not find project root containing AGENTS.md and pyproject.toml")


def check_required_context_files(root: Path) -> dict[str, bool]:
    """Return presence for every required context file."""
    return {path: (root / path).is_file() for path in REQUIRED_CONTEXT_FILES}


def git_state(root: Path) -> dict[str, str | bool | None]:
    """Return commit, branch, detached, and dirty status."""
    commit = _git_output(root, "rev-parse", "HEAD")
    branch = _git_output(root, "rev-parse", "--abbrev-ref", "HEAD")
    detached = branch == "HEAD"
    status = _git_output(root, "status", "--short")
    return {
        "commit": commit,
        "branch": None if branch is None else branch,
        "detached": detached,
        "dirty": bool(status),
    }


def run_doctor(*, json_output: bool = False, release_check: bool = False) -> int:
    """Run repository health checks and return a process exit code."""
    root = find_project_root()
    checks = collect_checks(root, release_check=release_check)
    status = {
        "project_root": str(root),
        "package_version": __version__,
        "active_task": ACTIVE_TASK,
        "git": git_state(root),
        "checks": [check.__dict__ for check in checks],
    }

    if json_output:
        print(canonical_json_text(status))
    else:
        print(f"Project root: {root}")
        print(f"Package version: {__version__}")
        print(f"Active task: {ACTIVE_TASK}")
        git = status["git"]
        if isinstance(git, Mapping):
            print(
                "Git: "
                f"commit={git.get('commit') or 'unavailable'} "
                f"branch={git.get('branch') or 'unavailable'} "
                f"dirty={git.get('dirty')}"
            )
        for check in checks:
            marker = "OK" if check.ok else ("WARN" if check.severity == "warning" else "FAIL")
            print(f"[{marker}] {check.name}: {check.detail}")

    return 0 if all(check.ok or check.severity == "warning" for check in checks) else 1


def collect_checks(root: Path, *, release_check: bool) -> list[Check]:
    """Collect all doctor checks."""
    checks: list[Check] = []

    version = sys.version_info
    python_ok = version.major == 3 and version.minor == 12
    checks.append(
        Check(
            "python",
            python_ok,
            f"{version.major}.{version.minor}.{version.micro}; required >=3.12,<3.13",
        )
    )

    uv_ok, uv_detail = _uv_availability()
    checks.append(
        Check(
            "uv",
            uv_ok,
            uv_detail,
        )
    )

    context = check_required_context_files(root)
    for path, exists in context.items():
        checks.append(Check(f"context:{path}", exists, "present" if exists else "missing"))

    lockfile = root / "uv.lock"
    lock_ok = lockfile.is_file()
    lock_detail = sha256_file(lockfile) if lock_ok else "missing"
    checks.append(Check("lockfile", lock_ok, lock_detail))

    schema = root / SCHEMA_PATH
    checks.append(Check("manifest_schema", schema.is_file(), str(schema)))

    for directory in ARTIFACT_DIRECTORIES:
        artifact_dir = root / directory
        writable = artifact_dir.is_dir() and os.access(artifact_dir, os.W_OK)
        checks.append(
            Check(
                f"writable:{directory}",
                writable,
                "writable" if writable else "not writable",
            )
        )

    rdr = root / "docs/decisions/RDR-0001-license.md"
    pending_license = rdr.is_file() and "PENDING" in rdr.read_text(encoding="utf-8")
    checks.append(
        Check(
            "license_decision",
            not pending_license if release_check else True,
            "pending; public release blocked" if pending_license else "resolved",
            "error" if release_check else "warning",
        )
    )

    return checks


def _git_output(root: Path, *args: str) -> str | None:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def _command_output(executable: str, *args: str) -> str | None:
    result = subprocess.run(
        [executable, *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def _uv_availability() -> tuple[bool, str]:
    uv_path = shutil.which("uv")
    if uv_path is not None:
        uv_version = _command_output(uv_path, "--version")
        if uv_version is not None:
            return True, f"{uv_version} at {uv_path}"

    for candidate in _uv_candidate_paths():
        if candidate.is_file():
            uv_version = _command_output(str(candidate), "--version")
            if uv_version is not None:
                return True, f"{uv_version} at {candidate}"

    for args in (("-m", "uv", "--version"), ("-3.13", "-m", "uv", "--version")):
        uv_version = _command_output("py", *args)
        if uv_version is not None:
            return True, f"{uv_version} via py {' '.join(args)}"

    return False, "uv not found in PATH, user scripts, or Python launcher modules"


def _uv_candidate_paths() -> list[Path]:
    candidates: list[Path] = []
    appdata = os.environ.get("APPDATA")
    if appdata:
        base = Path(appdata) / "Python"
        candidates.extend(
            [
                base / "Python313" / "Scripts" / "uv.exe",
                base / "Python312" / "Scripts" / "uv.exe",
                base / "Python311" / "Scripts" / "uv.exe",
            ]
        )
    local_appdata = os.environ.get("LOCALAPPDATA")
    if local_appdata:
        candidates.extend(
            [
                Path(local_appdata) / "Programs" / "Python" / "Python313" / "Scripts" / "uv.exe",
                Path(local_appdata) / "Programs" / "Python" / "Python312" / "Scripts" / "uv.exe",
            ]
        )
    return candidates


def doctor_json() -> dict[str, Any]:
    """Return doctor data for callers that need a Python object."""
    root = find_project_root()
    return {
        "project_root": str(root),
        "package_version": __version__,
        "active_task": ACTIVE_TASK,
        "git": git_state(root),
        "checks": [check.__dict__ for check in collect_checks(root, release_check=False)],
    }
