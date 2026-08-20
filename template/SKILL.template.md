---
name: replace-me
description: Use when [specific situations and near-boundaries that should activate this Skill].
license: Apache-2.0
---

# Replace Me

State the reusable capability and the non-obvious principle that makes this Skill valuable.

## Configuration

Use an optional configuration matching [config.example.yaml](config.example.yaml). State defaults and required external prerequisites here.

Configuration is explicit Agent input, never an implicit loader, credential
store, or write authorization. Report unknown settings rather than assuming
their effect.

## Safety boundary

State what is read-only, what requires exact confirmation, what is forbidden, and how results are verified.

## Workflow

1. Resolve inputs. Completion: every target is explicit or recorded as missing.
2. Gather evidence. Completion: every source is accounted for, including failures.
3. Produce the result using the documented default. Completion: output matches its template and unknowns remain visible.
4. Verify. Completion: evidence, counts, and safety boundaries reconcile.

## Conditional resources

- Read a file in `references/` only when its stated branch applies.
- Use an `assets/` template only when producing that artifact.
- Run a tested `scripts/` helper only for deterministic repeated work.

## Failure behavior

Describe actionable recovery without inventing missing evidence or silently broadening scope.
