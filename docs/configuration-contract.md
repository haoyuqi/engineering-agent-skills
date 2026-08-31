# Configuration contract

Every `config.example.yaml` is a portable, **explicit** policy input for its
own Skill. It is not a discovery mechanism, a credential store, or an automatic
runtime loader. Supply it through the selected Agent's normal context or
configuration mechanism, or paste only the relevant settings into the request.

[`configuration-contract.json`](configuration-contract.json) is the
machine-readable source of truth for the supported top-level keys of all six
templates. It distinguishes a general `agent_workflow_policy` from the
`repository-vulnerabilities` `agent_policy_only` template: its bundled runner
accepts documented CLI flags and never silently reads YAML.

## Rules

1. Treat a supplied template as policy, not permission. It can narrow scope,
   choose adapters, set limits, or prohibit operations, but never authorizes a
   write by itself.
2. Do not invent support for an unknown key, adapter type, or value. Report it
   as unsupported and ask for a supported replacement.
3. Keep secrets, tokens, cookies, private endpoints, and credential-bearing
   URLs out of tracked YAML. Use the adapter or Agent's normal authentication
   flow instead.
4. Resolve and display the effective target before using an adapter. A path,
   host, project, repository, or cluster from configuration is still subject to
   the Skill's read-only boundary and exact confirmation gate.
5. For a state change, show the exact action and target, obtain fresh user
   confirmation, execute only that scope, then verify. A `true` setting can
   enable a proposal; it cannot replace confirmation.

The contract checks top-level interface drift, not a universal YAML schema:
individual adapter values remain intentionally provider-neutral. Refer to the
specific Skill README and `SKILL.md` for accepted variants and failure behavior.
