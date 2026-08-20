# Review report template

```markdown
# Change Review: <reference> — <title>

## Review target
| Provider | Repository | PR/MR | Base SHA | Head SHA | Diff range | Retrieved | Checks snapshot |

## Verdict
<pass / changes required / cannot complete + reason>

## Findings
### <P0-P3> — <specific defect>
- Location: <file:line or diff hunk>
- Evidence: <observed behavior and surrounding context>
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
