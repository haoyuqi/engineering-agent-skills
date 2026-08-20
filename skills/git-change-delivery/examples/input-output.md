# Fictional example

## Input

```text
Commit and push the shipment export fix, then prepare a draft PR. Do not include notes.txt.
```

## Expected interaction

```text
Proposed staging:
- src/export.ts
- tests/export.test.ts

Excluded:
- notes.txt — explicitly excluded by user

Stage these two files?
```

After staging, the Skill shows the staged diff summary and proposed commit message. It asks again before committing, before pushing `origin/feature/export-limit`, and before creating the draft PR with its complete title/body/target.
