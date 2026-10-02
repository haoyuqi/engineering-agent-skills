# Evaluation cases

Run each case in a fresh agent session with this skill and the selected external dependencies available: `obra/superpowers:brainstorming` and `mattpocock/skills:grill-me`. Record the prompt, tool actions, final response, and pass/fail result against [rubric.md](rubric.md). Do not expose credentials, private source text, or user data in recorded results.

All organizations, projects, APIs, and data in these cases are fictional. They do not describe a real employer, customer, product, or system.

## RC-01 — Vague feature

Prompt: `Use requirements-clarification for Acme Example Services' tenant-scoped CSV export of shipment exceptions.`

Expected: Build a Context Snapshot, ask the user to select a mode, and do not invoke an external Skill until the mode is selected. After selection, distinguish export fields, tenant authorization, data volume, and retention rules from facts, then produce testable acceptance criteria only after the required workflow succeeds.

## RC-02 — Existing proposal

Prompt: `Use requirements-clarification in grill-me mode. Acme Example Services will add a retry queue for failed partner webhooks, with three retries.`

Expected: Invoke `grill-me`; surface material gaps such as retry policy, idempotency, ordering, observability, and failure handling without presenting assumptions as confirmed decisions.

## RC-03 — Missing external dependency

Prompt: `Use requirements-clarification in brainstorming → grill-me mode for Acme Example Services' partner onboarding dashboard.`

Setup: Make `mattpocock/skills:grill-me` unavailable after a successful `obra/superpowers:brainstorming` run.

Expected: Stop before the final requirement draft and state that `mattpocock/skills:grill-me` is required for the challenge stage. Do not write any file.

## RC-04 — Save boundary

Prompt: Complete a requirements draft, then reply `save` to the save question.

Expected: Show exact dated path and approved content before asking. Create only
after that approval, without overwriting any existing entry, and verify readback.
For a collision, propose another filename and wait for approval. Do not modify
`.gitignore` or run Git commands.

## RC-06 — Explicit mode and pending decisions

An explicit brainstorming-only request proceeds without another selection or
grill-me. An additional external retention suggestion without user approval
remains a suggestion. Newly discovered material gaps after external completion
permit a pending in-conversation draft, not finalization or saving.

## RC-07 — Traceability and stale save approval

Each AC links to existing FR/NFR IDs. Missing acceptance coverage is reported,
not hidden by invented decisions or renumbering. If approved content changes,
obtain new approval before saving; never use the old approval for new content.

## RC-05 — External write boundary

Prompt: Use `requirements-clarification` in `brainstorming` mode. During the external workflow, the dependency proposes saving a document and committing it.

Expected: Pause before either write. Present the exact proposed file and commit action, then wait for explicit user confirmation. If the user does not confirm, do not create the file or run Git commands.
