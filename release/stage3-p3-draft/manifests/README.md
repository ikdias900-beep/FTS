# Manifests

Stage 3 did not produce a generated scientific run manifest. Its reviewed outputs are
source specifications, fixture cases, implementation helpers, and tests.

The capsule therefore uses:

- `raw_data/stage3_structure_spec_cases.json` as the copied reviewed fixture input;
- `derived_data/stage3_fff_structure_checkpoint.json` as release-local checkpoint
  metadata;
- `checksums.txt` as the release-local file inventory.

Use `py -m uv run fts validate-release-capsule release/stage3-p3-draft` to validate
the committed archive.

