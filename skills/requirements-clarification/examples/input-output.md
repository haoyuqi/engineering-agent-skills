# Fictional input/output example

All names, systems, and data below are invented for demonstration. They do not represent a real organization, customer, product, or workflow.

## Input

```text
Use requirements-clarification in grill-me mode.

Northstar Parcel Lab needs a retry queue for delivery-status webhooks that fail to reach a partner endpoint. The first draft says: retry three times.
```

## Expected interaction outline

1. The Skill records three retries as a proposal in the first draft, not automatically a final decision, and identifies gaps in timing, idempotency, observability, and terminal failure handling.
2. It uses `mattpocock/skills:grill-me` without asking for the selected mode again, respecting the direct-user invocation boundary when required.
3. After the user resolves the material decisions, it produces a requirement draft. It does not claim unanswered choices are confirmed.
4. After exact content approval and resolution of material blockers, it shows the full destination path and content, then asks whether to save. A collision needs a newly approved name; without approval no file is created.

## Illustrative output excerpt

```markdown
# Partner Webhook Retry Requirements

Status: Pending confirmation — newly discovered retry-policy blockers remain.

## Functional Requirements

1. FR-001: The system retries a failed delivery-status webhook according to the user-confirmed retry schedule.
2. FR-002: The system records each delivery attempt and its outcome for the configured retention period.
3. FR-003: Proposed — retries preserve a stable event identifier for partner deduplication.

## Acceptance Criteria

- AC-001 → FR-001: Given a webhook attempt fails with a retryable error, when the configured retry delay elapses, then the system creates one subsequent delivery attempt. Pending: error classes and delay need confirmation.
- AC-002 → FR-003: Given a retried webhook, when it is sent, then its event identifier matches the initial attempt. Proposed, not user-approved.
- Coverage gap: FR-002 needs observable retention/deletion criteria after the retention period is decided.

## Decisions and Assumptions

| Item | Status | Rationale or evidence |
| --- | --- | --- |
| Retry schedule | Open | The first draft proposes three retries; timing remains unresolved. |
| Stable event identifier | External suggestion | No explicit user approval recorded. |

## Open Questions

- Which failures are retryable, and what is the terminal behavior after the final attempt?
```

This excerpt is illustrative, not a substitute for the selected external workflow or user confirmation.
