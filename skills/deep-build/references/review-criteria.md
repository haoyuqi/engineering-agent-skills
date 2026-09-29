# Review criteria

Read the reviewer policy below before both Plan Review and Code Review. Apply the code-specific criteria after implementation, against the actual diff. Read the repository's `AGENTS.md` and local conventions first; they override generic conventions. Record every selected criterion and its evidence in the Plan.

## Independent reviewer policy — both gates

- The reviewer must not have authored the version being reviewed. Use a separate agent context, another session, an external reviewer, or a human. A role change inside the author's existing context is still self-review. Plan and Code Review may use the same reviewer if that reviewer did not write either artifact.
- Give the reviewer requirements, the Plan or actual diff, relevant repository context, and verification evidence. Reviewer conclusions must come from inspecting the artifacts, not accepting the author's summary. Keep review read-only; the author handles revisions and code fixes. Re-review the changed version and affected surrounding code before recording PASS.
- Prefer a different model only when its capabilities fit the task. Do not select a weaker or lightweight model solely to obtain a different model name. Use the user's configured reviewer when suitable; disclose a known capability mismatch rather than silently accepting it.
- When suitability of an alternative is unknown, retain the author's model and reasoning effort in a separate context. If the runtime cannot provide this, request a suitable external or human reviewer; stop at `pending external review` until one is available. No provider, tool, or model ranking is hardcoded.
- Record reviewer identity/context, reviewed version (commit or working-copy fingerprint), known model and effort, selection rationale, findings, and verdict. Report unavailable model metadata as unknown, and human model metadata as N/A; never infer independence or claim a different model from a role name alone.
- Report each review result to the user. Plan PASS still requires explicit user Plan approval. Code PASS still requires the final handoff and user acceptance. Missing independent evidence is pending, never PASS.

## Always: five-axis review

Review requirement correctness, readability/simplicity, architecture, security, and performance. Check error paths, compatibility, tests, verification evidence, and unrelated changes. Classify findings as `Critical`, `Required`, `Optional`, `Nit`, or `FYI`; Critical and Required findings require another review round.

## Add a specialist review when the diff triggers it

| Diff signal | Principle and recommended skill |
| --- | --- |
| Authentication, authorization, middleware, user input, validation, PII, encryption, tokens, or API endpoints | Threat boundaries, least privilege, validation and output encoding — `security-and-hardening` |
| Queries, schema migrations, indexes, batch jobs, unbounded loops, or large datasets | Measure before optimizing; bounded access, pagination, indexes, rollback — `performance-optimization` |
| PostgreSQL queries, indexes, JSONB, or migration performance | Analyze the real plan before/after; use `EXPLAIN (ANALYZE, BUFFERS)` where safe — `postgres-pro` |
| Refactor/extraction/consolidation, or 200+ changed lines | Preserve behavior; remove needless complexity and duplication; avoid drive-by changes — `code-simplification` |

When uncertain, include the specialist review. Missing a recommended external skill does not waive its principle: apply the concise rule above and record the limitation.

## Sources

The routing rules are a concise, independently written adaptation of the public guidance in [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) and the optional PostgreSQL specialist at [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills). Install commands and exact identifiers are in [external-dependencies.json](../external-dependencies.json).
