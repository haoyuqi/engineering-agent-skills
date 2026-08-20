# Compatibility and installation

Every `skills/<name>/` directory is portable Agent Skills content: `SKILL.md`
plus its referenced resources travel together. The catalog does not publish
Agent-specific copies or require a particular model.

## Verified packaging targets

The source of truth is
[`compatibility.json`](compatibility.json). CI uses its four project layouts to
install every Skill with the pinned `skills` CLI and byte-compare all bundled
files. This verifies discovery and resource packaging; it does **not** claim
that every Agent version has identical triggering, tool, permission, or UI
behavior.

| Agent | Installer identifier | Project location | CLI installation |
| --- | --- | --- | --- |
| Codex | `codex` | `.agents/skills/<skill-name>/` | `npx skills@1.5.20 add haoyuqi/engineering-agent-skills --skill <skill-name> --agent codex` |
| Claude Code | `claude-code` | `.claude/skills/<skill-name>/` | `npx skills@1.5.20 add haoyuqi/engineering-agent-skills --skill <skill-name> --agent claude-code` |
| OpenCode | `opencode` | `.agents/skills/<skill-name>/` | `npx skills@1.5.20 add haoyuqi/engineering-agent-skills --skill <skill-name> --agent opencode` |
| GitHub Copilot | `github-copilot` | `.agents/skills/<skill-name>/` | `npx skills@1.5.20 add haoyuqi/engineering-agent-skills --skill <skill-name> --agent github-copilot` |

When the CLI is unavailable, copy the complete `skills/<skill-name>/` directory
to the listed project location. Do not copy only `SKILL.md`: templates,
fixtures, references, and deterministic scripts are part of the Skill's
contract. Check the selected Agent's current documentation before installing to
a global location or a different runtime-specific path.

## What remains portable

- Portable frontmatter and the Skill directory structure are the interface.
- `agents/openai.yaml` is optional Codex UI metadata; compatible runtimes can
  ignore it without losing the portable workflow.
- Provider access, adapters, names, and credentials are not bundled. Configure
  them through user input or the Skill's `config.example.yaml` without placing
  secrets in tracked files.
- External Skill dependencies are exceptional and explicitly declared only by
  `requirements-clarification`.
