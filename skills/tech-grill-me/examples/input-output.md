# Fictional example

The scenario and answers below are fictional.

## Input

```text
Use tech-grill-me to quiz me on transaction isolation in a beginner PostgreSQL course.
```

## Expected interaction

1. The Skill proposes isolation levels, anomalies, and retry behavior as the
   scope, then begins after the user accepts it.
2. It asks one question about dirty reads and waits for the answer.
3. If the answer omits that PostgreSQL does not permit dirty reads, including at
   `READ UNCOMMITTED`, it gives one hint about database-specific behavior,
   accepts one retry, then explains the missing point if needed.
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

Question 1: Why is receipt creation kept in the service rather than the request handler?
```

The Skill continues with the remaining visible batch rather than silently
truncating the confirmed repository.
