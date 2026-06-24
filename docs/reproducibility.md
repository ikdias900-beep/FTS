# Reproducibility Contract

This repository treats reproducibility as infrastructure before scientific implementation.

## Artifact Immutability

Raw artifacts are written once and are not overwritten by default. Derived artifacts must name their inputs and checksums.

## Checksums

All persisted payloads and manifests use SHA-256 checksums over exact bytes. A manifest is valid only while all referenced artifacts match their recorded checksums.

## Manifests

Every run manifest records:

- task, claim, source, and assumption IDs;
- UTC creation time;
- exact command and parameters;
- explicit seed field, using `null` when deterministic;
- Git commit, branch, detached state, and dirty flag;
- Python, platform, package version, and lockfile checksum;
- input and output paths with SHA-256 checksums;
- completion status and error field.

Infrastructure smoke manifests use `artifact_kind: infrastructure_smoke`, `epistemic_status: null`, and empty claim/source/assumption lists.

## Exact Oracles

Future scientific modules must prefer exact arithmetic and brute-force small-case oracles before optimized or stochastic implementations. `TASK-000` contains no scientific oracle.

## Independent Review

Scientific releases require a fresh-context verifier. `TASK-000` also requires `REV-TASK-000-001` with no unresolved `fatal` or `major` findings before acceptance.

## Clean-Room Reproduction

A clean checkout should run:

```bash
uv sync --all-groups
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
uv run fts doctor
uv run fts reproduce-smoke
```

The smoke payload checksum should match across repeated runs from the same config.
