# Fictional input/output example

All names, systems, and data below are invented for demonstration. They do not represent a real organization, customer, product, or workflow.

## Input

```text
Use requirements-clarification in grill-me mode.

Northstar Parcel Lab needs a retry queue for delivery-status webhooks that fail to reach a partner endpoint. The first draft says: retry three times.
```

## Expected interaction outline

1. The Skill labels the stated retry count as confirmed and identifies gaps such as retry timing, idempotency, ordering, observability, partner opt-out behavior, and terminal failure handling.
2. It invokes `mattpocock/skills:grill-me` because the user selected `grill-me` mode.
3. After the user resolves the material decisions, it produces a requirement draft. It does not claim unanswered choices are confirmed.
4. It asks whether the final draft should be saved in the current directory. Without an explicit yes, no file is created.

## Illustrative output excerpt

```markdown
# Partner Webhook Retry Requirements

## Functional Requirements

1. FR-001: The system retries a failed delivery-status webhook according to the user-confirmed retry schedule.
2. FR-002: The system records each delivery attempt and its outcome for the configured retention period.

## Acceptance Criteria

- AC-001: Given a webhook attempt fails with a retryable error, when the configured retry delay elapses, then the system creates one subsequent delivery attempt.
- AC-002: Given an event has already been accepted by a partner, when a duplicate delivery is received, then the partner can identify the event using a stable event identifier.

## Decisions and Assumptions

| Item | Status | Rationale or evidence |
| --- | --- | --- |
| Retry schedule | Assumption | The input only states three retries; timing remains unresolved. |

## Open Questions

- Which failures are retryable, and what is the terminal behavior after the final attempt?
```

This excerpt is illustrative, not a substitute for the selected external workflow or user confirmation.
