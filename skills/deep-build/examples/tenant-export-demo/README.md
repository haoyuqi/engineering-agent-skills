# Tenant export demo

This is a complete, fictional Python demonstration of the `deep-build`
workflow. It is intentionally small enough to inspect in one sitting while
still spanning an API function, a retrying worker, tests, an acceptance ledger,
and an implementation handoff.

No package installation, network access, Git action, or external system is
needed. Run the verified implementation with:

```bash
cd after
python3 -m unittest discover -s tests -v
```

The `before/` directory contains the unsafe starting point. The `after/`
directory is the accepted implementation. `implementation-ledger.md` shows how
requirements map to edits and observable tests; `handoff.md` is the resulting
build handoff. The example does not tell an Agent to copy files blindly into a
user repository: it demonstrates the evidence expected after inspecting that
repository's actual conventions.
