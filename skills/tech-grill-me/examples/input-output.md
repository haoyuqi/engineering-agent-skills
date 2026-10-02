# Fictional example

The scenario and answers below are fictional.

## Input

```text
Use tech-grill-me to quiz me on transaction isolation in a beginner PostgreSQL course.
```

## Expected interaction

1. The Skill proposes isolation levels, anomalies, and retry behavior as the
   scope, then begins after the user accepts it.
2. It asks: "What is a dirty read?" and waits. "Reading another transaction's
   uncommitted changes" is complete; omitting database-specific behavior is not
   a weakness.
3. It can ask separately: "Does PostgreSQL allow dirty reads at READ UNCOMMITTED?"
   Only an incomplete or incorrect answer to this explicit follow-up receives
   one non-revealing hint and one retry, then a correction if needed. Ambiguous
   wording is clarified without recording a learner weakness.
4. On `stop`, it reports demonstrated concepts, remaining gaps, and concrete
   next-study suggestions. It proposes a weak-points file but does not write it
   until the user confirms both its content and path.

## Code-answer variation

For a suitable question, the Skill may ask the user to submit a small function.
It assesses only its static correctness for that question, explicitly does not
run it, and does not turn the exchange into a general code review.

## Codebase-familiarization variation

Input:

```text
Use tech-grill-me to help me learn the fictional-service repository. Read the whole repository, then ask me questions.
```

Expected first response:

```text
Confirmed scope: fictional-service/ (entire repository). First map batch: payment/; reporting/ remains.

- Observation — payment/handler.py:create_payment delegates receipt creation to payment/service.py:create_receipt.
- Inference — keeping receipt creation in the service separates transport from persistence.
- Unknown — this batch does not establish the retry policy.

Reading continues with reporting/ before questions begin.
```

After reading the remaining batch, it reports the combined map, including:

```text
Coverage: payment/ and reporting/ reviewed; no batches pending.
- Observation — reporting/summary.py:receipt_summary reads receipts through payment/store.py:list_receipts.
- Inference — receipt storage is shared by payment and reporting.
- Unknown — the available code does not establish the operational retry policy.
Excluded: credentials, ignored/private directories, and non-readable binary assets.

Question 1: Why might receipt creation live in a service rather than the request handler?
```

The question asks for reasoning, not an undocumented author's intent. If the
remaining batch is unreadable, report the gap and ask whether to continue with
payment/ alone; do not question before that scope decision. An explicit entire-
repository request needs no repeated confirmation; an ambiguous scope does.
