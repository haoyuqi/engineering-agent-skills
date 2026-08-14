# Fictional example

All organizations and versions are invented.

## Input

```text
Scan the current acme-example/route-planner checkout for Composer and npm vulnerabilities. Do not change dependencies.
```

## Illustrative output

```markdown
## Scan Inventory
| Project | Ecosystem | Lockfile | Audit status |
| --- | --- | --- | --- |
| `.` | npm | `package-lock.json` | Completed |

### GHSA-xxxx-example — map-parser
- Advisory range: `>=4.0.0, <4.2.7`
- Installed evidence: `acme-example/route-planner`, `package-lock.json`, version `4.2.9`
- Verdict: False positive
- Reason: the resolved version is above the patched boundary.
- Suggested dismissal rationale: "Lockfile resolves 4.2.9; advisory affects versions below 4.2.7."
```

No dependency file is changed by the Skill.
