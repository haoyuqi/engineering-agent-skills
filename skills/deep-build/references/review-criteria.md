# Review criteria

Use this file after implementation, against the actual diff. Read the repository's `AGENTS.md` and local conventions first; they override generic conventions. Record every selected criterion and its evidence in the Plan.

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
