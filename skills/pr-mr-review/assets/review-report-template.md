# Review report template

Choose the applicable target fields below; omit the other target block. Do not
invent remote metadata for a local review. Keep identifiers free of credentials.

```markdown
# Change Review: <reference> — <title>

## Review target
Remote: <provider, repository, PR/MR, base/head SHAs, exact diff range/identity>
Local context: <checkout, HEAD, dirty state, revision matches/mismatches>

Local: <directory, worktree-snapshot or base-ref comparison, HEAD/resolved base>
Scope: <selected paths; staged, unstaged, untracked layers; exclusions>
Snapshot: <content fingerprint, method, context coverage, captured time>

## Target freshness
- Initial target: <reviewed revision or snapshot>
- Final observation: <revision/snapshot or retrieval failure; time>
- Status: <unchanged / changed / unavailable>
- Applicability: <original snapshot only; newer content unreviewed if changed;
  freshness unknown if unavailable>
- Checks: <observed checks, associated revision/snapshot and time; unrun checks>

## Verdict
<pass / changes required / cannot complete + reason, explicitly scoped to reviewed snapshot>

## Findings
### <P0-P3> — <specific defect>
- Location: <file:line or diff hunk>
- Evidence: <observed behavior and surrounding context at identified revision/snapshot>
- Impact: <user/system consequence>
- Recommendation: <smallest safe correction>

## Acceptance criteria coverage
| ID | Criterion | Status | Implementation evidence | Test evidence |

## Verification gaps
| Gap | Why it matters | Recovery step |

## Positive observations
- <specific evidence-backed strength>

## Source coverage
| Source | Status | Notes |
```
