# Reproduction Commands

Install dependencies:

```bash
py -m uv sync --all-groups
```

Run repository checks:

```bash
py -m uv run fts doctor --release-check
py -m uv run pytest
py -m uv run ruff check .
py -m uv run ruff format --check .
py -m uv run mypy src
```

Regenerate the Stage 4 grid-smoke output:

```bash
py -m uv run fts fbt atlas-grid-v0-smoke
```

Validate a generated manifest:

```bash
py -m uv run fts validate-manifest experiments/manifests/<manifest>.json
```

Validate this committed capsule:

```bash
py -m uv run fts validate-release-capsule release/stage4-p4-draft
```

The committed capsule validation checks archive-local checksums. It does not require
internet access and does not depend on the original absolute paths stored in the copied
run manifest.
