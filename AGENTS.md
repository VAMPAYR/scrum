# AGENTS.md

This folder is the `scrum` package, a runtime-neutral Scrum software organization
that AI agents run for a human stakeholder, filling the Product Owner, Scrum
Master, and Developers accountabilities under a tiered, evidence-gated Definition
of Done. Every rule here and every project's state is plain markdown, so any agent
in any tool can resume any project.

## When to follow it

Follow `SKILL.md` when the user asks to start, plan, run, review, or retro a
product or a sprint, asks to build something as a software team would, or types a
`/scrum` command. `SKILL.md` is the router: it detects the stage from
`.scrum/state.md`, maps the subcommand onto a stage, and names the files it needs.

## Pick an adapter

Adapters map the Scrum roles onto what a runtime can actually do. They are named
for runtime capability, never for a vendor, and none is a default. Read the one
that matches, then record the choice in the `Adapter` field of `.scrum/state.md`
as one of `parallel-agents`, `terminal-agent`, or `single-model`.

- `adapters/parallel-agents.md`: the runtime spawns worker agents, meaning child
  runs that take a brief and report back, and discovers a skill folder from the
  frontmatter in `SKILL.md`. Developers map to concurrent worker agents, and the
  verifier is a distinct agent.
- `adapters/terminal-agent.md`: the runtime reads a project instruction file, an
  `AGENTS.md` or a rules file, and starts separate runs or background agents as
  Developers.
- `adapters/single-model.md`: one model in one conversation with no worker
  primitive. Roles become labeled hats and verification a distinct labeled pass.
- `adapters/bootstrap-prompt.md`: copy-paste prompts that boot any agent,
  including a chat-only model with no file access.

## Read on demand

Load nothing beyond this file and `SKILL.md` by default. At each stage read only
the files its row in the `SKILL.md` stage table names: a role playbook from
`core/roles/` before speaking as that role, an event file from `core/events/`
before that event, and `core/dod/definition-of-done.md` before any gate.

## Two rules that hold before any code is written

1. **The Orchestrator does not write production code while worker agents are
   available.** The Orchestrator is the main loop that facilitates, delegates, and
   arbitrates. It writes Scrum artifacts, delegation briefs, and arbitration
   decisions; Developer agents write the code. The single exception is the
   escalation rung in `core/orchestrator.md`, logged in the sprint file when used.
2. **No item is done until a verifier distinct from the implementer records
   evidence.** The verifier walks `.scrum/DEFINITION_OF_DONE.md` item by item and
   writes the evidence, meaning command output, test summaries, and file paths,
   into the item's "DoD evidence" field. Mark an unverifiable item `n/a` with a
   reason. A self-reported "done" is not done.

## State

Keep all project state in `.scrum/` in the target repository as plain markdown:
`state.md`, `team.md`, `DEFINITION_OF_DONE.md`, `product/`, and `sprints/`. Commit
it with the increment, so any runtime can read `state.md` and resume the project
at the exact stage it paused.
