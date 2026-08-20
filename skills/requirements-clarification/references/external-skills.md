# External Skill integration

Load this reference only after the user selects a mode that requires an external Skill.

The checked-in [machine-readable contract](../external-dependencies.json) is the authoritative source for upstream identity, dependency relation, invocation class, and failure behavior. This reference explains how to apply it in a user conversation.

## Complete upstream names

| Role | Upstream Skill | Integration result used here |
| --- | --- | --- |
| Explore an incomplete idea | `obra/superpowers:brainstorming` | A design the user explicitly approved. |
| User-facing pressure test | `mattpocock/skills:grill-me` | A completed interview the user confirms reached shared understanding. |
| Reusable implementation behind `grill-me` | `mattpocock/skills:grilling` | The resolved decision tree produced through the wrapper. |

Install the selected dependencies with a compatible installer:

```bash
npx skills@1.5.20 add obra/superpowers --skill brainstorming
npx skills@1.5.20 add mattpocock/skills --skill grill-me --skill grilling
```

Do not install tools during a requirements session without a separate user request.

## Invocation contract

Upstream `grill-me` is a thin user-invoked wrapper and delegates its work to `grilling`. Some runtimes prevent another Skill from invoking a user-only Skill. In that case:

1. Tell the user that `mattpocock/skills:grill-me` must be invoked directly.
2. Preserve the context snapshot for that invocation.
3. Wait for the external workflow to finish.
4. Resume only after the user confirms shared understanding was reached.

Do not silently call `grilling` as a substitute for the requested wrapper, and do not reproduce its interviewing workflow locally.

For `brainstorming`, use the approved in-conversation design as the handoff. If upstream proposes saving or committing a design artifact, this repository's safety boundary applies: show the exact write and ask for confirmation. Declining that optional write does not erase an already approved in-conversation design.

## Failure contract

Stop without a final requirements draft when:

- a selected Skill or `grilling` is unavailable;
- the runtime cannot invoke it and the user has not completed the direct invocation;
- `brainstorming` has no approved design;
- `grill-me` has unresolved branches or no user confirmation of shared understanding.

State the exact failed dependency and recovery action. Never improvise a replacement workflow.
