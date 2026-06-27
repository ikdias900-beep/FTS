# Stage 2 P2 Draft Checkpoint Capsule

```text
CAPSULE ID: STAGE2-P2-DRAFT
TASK ID: TASK-002-FBT-NUMERICAL
STATUS: draft checkpoint capsule, accepted with minor findings in independent review
LICENSE: MIT for project-authored repository contents
SCIENTIFIC CLAIMS ADDED: CLM-FBT-APP-001; CLM-FBT-APP-002; CLM-FBT-APP-003; CLM-FBT-APP-004
```

## Scope

This capsule packages the current Stage 2 exact reproduction of the FBT numerical
appendix. It is an independently reviewed checkpoint package, not a final public
release, DOI archive, or external publication package.

It includes:

- machine-readable source input copied from `experiments/configs/fbt_numerical_example.json`;
- exact JSON result for marginals, posteriors, MAP estimates, and expected fitness;
- generated Markdown derivation report;
- source run manifest;
- claims, limitations, assumptions, review status, reproduction commands, and checksums.

This capsule does not include evolutionary dynamics, a genetic algorithm, the general
FBT theorem, ML/RL experiments, figures, browser demo, DOI, or external publication
package.

## Artifact Generation State

The generated result artifacts were produced from a clean repository state:

```text
git_commit=23060471e8ade4e9d1790041ea49271f0002cd18
git_branch=codex/stage2-fbt-numerical-appendix
git_dirty=false
dependency_lock_sha256=6b81fceadcb3fe17172ce56a239b581332675e7045058459a5871f2982e609c8
```

## Included Artifact IDs

- FBT numerical manifest: `ART-TASK-002-FBT-NUMERICAL-MANIFEST-20260625T222000Z-2A277325`
- FBT numerical run: `EXP-TASK-002-FBT-NUMERICAL-20260625T222000Z-2A277325`

The copied manifest is the original run record and retains its original absolute paths.
The archived copies in this capsule are verified by `checksums.txt`.

## Directory Map

```text
release/stage2-p2-draft/
├── README.md
├── CLAIMS.md
├── LIMITATIONS.md
├── ASSUMPTIONS.md
├── REVIEW_REPORT.md
├── environment/
├── manifests/
├── raw_data/
├── derived_data/
├── figures/
├── reproduction_commands.md
└── checksums.txt
```

## Review Cadence

`REV-TASK-002-FBT-NUMERICAL-001` accepted this capsule and the Stage 2 FBT
numerical reproduction with minor findings only. There are no unresolved fatal or
major findings.

The minor finding is that the copied manifest retains original absolute paths
outside the release capsule. The archived capsule contents remain independently
verifiable through committed raw/derived files and `checksums.txt`.

Follow-up archive validation is now available:

```bash
py -m uv run fts validate-release-capsule release/stage2-p2-draft
```

This command validates the committed capsule files against the local checksum
inventory and does not depend on the original absolute paths retained in the
copied run manifest.
