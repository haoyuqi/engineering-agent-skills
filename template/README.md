# Skill template

Copy this directory to `skills/<name>`, rename `SKILL.template.md` to `SKILL.md`, and replace every placeholder. Keeping the template filename prevents Skill installers from publishing `replace-me` as a real Skill.

The finished README should explain the independent capability, a realistic quick-start prompt, prerequisites, safety boundary, and links to its fictional example and evaluations. If it needs an external Skill, add an `external-dependencies.json` contract naming the upstream repository, runtime name, transitive dependencies, invocation limits, handoff, and failure behavior.

Expand `evals/triggers.json` toward 20 reviewed, realistic positive and near-neighbor negative cases before claiming the description is optimized.

Before adding the Skill to the public catalog, update these repository-level
contracts:

- [`docs/configuration-contract.json`](../docs/configuration-contract.json):
  add the Skill name, exact top-level `config.example.yaml` keys, and whether
  it is an Agent workflow policy or an agent-policy-only template. Configuration
  remains explicit input; unknown keys and tracked secrets are unsupported.
- [`docs/compatibility.json`](../docs/compatibility.json): do not add a
  runtime-specific copy of the Skill. The portable directory is packaged into
  the already-verified layouts unless a new Agent layout is deliberately added
  and tested.
