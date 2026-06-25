# Stage 1 P1 Draft Release Capsule

```text
CAPSULE ID: STAGE1-P1-DRAFT
TASK ID: TASK-001-P1-CAPSULE
STATUS: draft release capsule, ready for independent review
LICENSE: MIT for project-authored repository contents
SCIENTIFIC CLAIMS ADDED: none
```

## Scope

This capsule packages the reviewed Stage 1 FFF finite-count artifacts for total orders and cyclic groups.

It includes:

- raw long-form finite-count sweep CSV;
- derived wide publication-table CSV;
- generated Markdown publication-table report;
- source sweep and derived publication-table manifests;
- claims, limitations, assumptions, review summary, reproduction commands, and checksums.

This is not a GitHub release, DOI, archival deposit, browser demo, or final public publication package. It is a reviewable draft capsule assembled inside the repository.

## Artifact Generation State

The generated raw and derived artifacts were produced from a clean repository state:

```text
git_commit=ca23c56232a1d108b675418fcb55cda883a3dc6a
git_branch=stage1-p1-release-capsule
git_dirty=false
dependency_lock_sha256=6b81fceadcb3fe17172ce56a239b581332675e7045058459a5871f2982e609c8
```

## Included Artifact IDs

- Sweep manifest: `ART-TASK-001-SWEEP-MANIFEST-20260625T192538Z-FBD5EA2B`
- Sweep run: `EXP-TASK-001-SWEEP-20260625T192538Z-FBD5EA2B`
- Publication manifest: `ART-TASK-001-PUBTABLES-MANIFEST-20260625T192546Z-D763EFE3`
- Publication run: `EXP-TASK-001-PUBTABLES-20260625T192546Z-D763EFE3`

The copied manifests are the original run records and retain their original absolute paths. The archived copies in this capsule are verified by `checksums.txt`.

## Directory Map

```text
release/stage1-p1-draft/
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

## Review Gate

This capsule should receive an independent review before being treated as a publishable P1 package. The review should verify manifest validity, checksums, claim boundaries, license/provenance, and reproduction commands.
