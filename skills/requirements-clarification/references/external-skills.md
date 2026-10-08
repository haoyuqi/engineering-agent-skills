# External Skill integration

Load this reference only after the user selects a mode that requires an external Skill.

The checked-in [machine-readable contract](../external-dependencies.json) is the authoritative source for upstream identity, dependency relation, invocation class, and failure behavior. This reference explains how to apply it in a user conversation.

## Complete upstream names

| Role | Upstream Skill | Integration result used here |
| --- | --- | --- |
| Explore an incomplete idea | `obra/superpowers:brainstorming` | User-approved in-conversation design from the requirements-stage adaptation below, not full upstream completion. |
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

## Brainstorming requirements-stage adaptation

Reviewed against [upstream brainstorming at 8ca22d](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/brainstorming/SKILL.md). This revision has no requirements-only return hook: its architectural path requires a saved and committed spec, written-spec approval, then writing-plans. Its bounded path proceeds to implementation. These are not optional steps in an otherwise complete upstream run.

This integration is a downstream adaptation, not native execution of that complete lifecycle:

1. Read the installed upstream instructions and identify their source/version when available. The recorded revision is review evidence, not an installation lock. Reconcile changed upstream instructions with this boundary; if incompatible or unreadable, stop and explain rather than assume compatibility.
2. Tell the user: "I am using brainstorming's requirements-stage adaptation: explore and approve a design here, then return to requirements drafting; no design-file save, commit, implementation plan, or implementation."
3. Use upstream's intent discovery, correction of shared understanding, read-only project exploration, focused questions, alternatives with trade-offs, and design discussion at appropriate depth. Do not relabel architectural work as bounded to escape its lifecycle. Preserve uncertainty and obtain explicit approval of the presented design.
4. At that approval, return the design, constraints, decisions, unresolved questions, and approval evidence to requirements-clarification. In combined mode, continue to grill-me; otherwise draft requirements. Report "requirements-stage adaptation complete", never "full brainstorming complete".

Do not invoke the unmodified upstream workflow when the host would enforce its entire lifecycle. Read it as source guidance for this disclosed adaptation instead; file reading is not a native Skill invocation. If the host cannot support this without violating its rules, stop at `pending compatible brainstorming adaptation` and explain the conflict. Do not silently bypass runtime invocation restrictions.

Design-file creation, commits, written-spec review and writing-plans are outside this adaptation, not completed or waived upstream steps. The only optional save here is the approved requirements document under this Skill's save gate. Implementation planning belongs to a later deep-build or user-selected workflow, with separate approval; it is not an additional installed dependency. Optional upstream companions requiring writes or extra resources are not started by this read-only adaptation.

## Failure contract

Stop without a final requirements draft when:

- a selected Skill or `grilling` is unavailable;
- the runtime cannot invoke it and the user has not completed the direct invocation;
- `brainstorming` has no approved design;
- `grill-me` has unresolved branches or no user confirmation of shared understanding.

State the exact failed dependency and recovery action. Never improvise a replacement workflow.
