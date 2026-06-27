# REV-TASK-002-FBT-NUMERICAL-001 Follow-Up Verification

```text
REVIEW ID: REV-TASK-002-FBT-NUMERICAL-001-FOLLOWUP
TASK ID: TASK-002-FBT-NUMERICAL
RELATED REVIEW: REV-TASK-002-FBT-NUMERICAL-001
BASE REVIEW VERDICT: accepted_with_minor_findings
FOLLOW-UP DATE: 2026-06-27
FOLLOW-UP TYPE: implementer-side verification after minor packaging fix
FOLLOW-UP VERDICT: minor finding addressed by release-capsule archive validation
```

## Context Boundary

This follow-up was performed in the same implementation session that added the
packaging fix. It is not a fresh-context independent review and does not replace
`REV-TASK-002-FBT-NUMERICAL-001`.

## Original Minor Finding

The copied release manifest under `release/stage2-p2-draft/manifests/` preserves
the original absolute input/output paths outside the release capsule. The capsule
was already independently verifiable through committed raw/derived files and
`checksums.txt`, but a release-local manifest or archive-validation mode would make
that verification more portable.

## Fix Summary

Added release-capsule archive validation:

```text
py -m uv run fts validate-release-capsule release/stage2-p2-draft
```

The validator checks `checksums.txt` using release-local relative paths. It verifies
that every listed file exists, every SHA-256 hash matches, every listed path stays
inside the capsule, and no unlisted file is present except `checksums.txt` itself.

## Scientific Scope

No source input, exact FBT computation, generated raw/derived scientific artifact,
claim row, assumption row, or copied original run manifest was changed.

## Follow-Up Evidence

Regression coverage was added in:

```text
tests/integration/test_release_capsules.py
```

The tests verify that the committed Stage 2 capsule passes the new validator and
that adding an unlisted file to a copied capsule is rejected.
