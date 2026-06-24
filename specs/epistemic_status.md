# Epistemic Status

Scientific artifacts must use exactly one of these statuses:

| Status | Meaning |
|---|---|
| `R` | Reproduction from a published definition, formula, theorem, or numerical example. |
| `C` | Computational reconstruction using explicitly registered assumptions. |
| `E` | Extension not claimed in the source. |
| `A` | Analogy to another domain; not a test of the original biological or philosophical claim. |

Infrastructure smoke artifacts are not scientific artifacts. They must use:

```json
{
  "artifact_kind": "infrastructure_smoke",
  "epistemic_status": null,
  "claim_ids": []
}
```

Mixed-status scientific results must preserve per-row or per-run status.
