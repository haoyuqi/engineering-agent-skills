# Requirement document template

Use this structure after the selected external workflow completes.

```markdown
# <Feature Title> Requirements

Status: <Pending confirmation / Final — user-approved>
Material blockers: <explicit list or none>

## Problem and Goal

Describe the user or business problem, intended outcome, and success signal.

## Scope

State included behavior and boundaries.

## Actors and Permissions

| Actor | Allowed actions | Restrictions |
| --- | --- | --- |

## Functional Requirements

1. FR-001: <testable behavior>
2. FR-002: <testable behavior>

## Acceptance Criteria

- AC-001 → FR-001: Given <context>, when <action>, then <observable result>.
- AC-002 → FR-002: Given <context>, when <action>, then <observable result>.

## Non-functional Requirements

Cover only applicable performance, reliability, accessibility, observability, privacy, or security constraints.

## Data and Integration Boundaries

Identify data handled, ownership, retention or privacy constraints, and external systems or APIs.

## Approaches and Trade-offs

Summarize the selected approach and material alternatives considered.

## Decisions and Assumptions

| Item | Status | Rationale or evidence |
| --- | --- | --- |
| <decision, suggestion, or assumption> | User-confirmed / External suggestion / Assumption / Open | <source and explicit user approval evidence, if confirmed> |

## Risks and Failure Modes

| Risk or failure | Expected behavior or mitigation |
| --- | --- |

## Out of Scope

List explicitly excluded work.

## Open Questions

List unresolved items, owner if known, and why each blocks or affects delivery.

## Context Sources

List only user-provided sources that informed the draft.
```

Rules:

- Use IDs only where they improve traceability: `FR-001`, `AC-001`.
- Make each acceptance criterion independently observable or testable.
- Link each AC to one or more existing requirement IDs. Give applicable
  non-functional requirements stable NFR IDs when ACs cover them. Identify
  requirements without acceptance coverage; do not fabricate a user decision
  or renumber existing IDs merely to close a gap.
- External workflow completion does not confirm individual suggestions. A
  pending draft may show newly discovered material blockers after that workflow
  completes, but is not final or ready for implementation. Finalization needs
  resolved blockers, reconciled coverage, and approval of the exact content.
- Omit sections that genuinely do not apply only when doing so does not hide a risk.
- Do not include tokens, private URLs, personal data, or raw sensitive logs.
