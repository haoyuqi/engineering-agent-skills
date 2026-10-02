# Fictional example

## Input

```text
Commit and push the shipment export fix, then open a draft PR. Do not include notes.txt.
```

## Expected interaction

```text
Authorized scope (confirmed by the request):
- src/export.ts
- tests/export.test.ts

Excluded:
- notes.txt — explicitly excluded by user

Commit: fix: scope shipment export to tenant
Push: origin/feature/export-limit
Draft PR: feature/export-limit → main, using the repository template.

Proceeding with these operations; notes.txt stays untouched.
```

Assume the two files are the whole intended change, the index has no unrelated content, and the target is established by repository evidence. The Skill verifies staging, runs checks/hooks, commits, pushes, shows the full PR title/body and creates it without another approval question. It then verifies and reports the actual results.

## Boundaries

- “Commit the already staged export fix; do not push”: inspect and commit only.
- “Prepare a draft PR description”: return the proposal without publishing.
- “Do each step only after I confirm”: pause at each requested step.
- An unrelated pre-staged document is discovered: ask how to isolate it before committing; neither include nor unstage it silently.
- A push is rejected and would need force: report the remote state and request specific approval; ordinary push authorization is insufficient.
