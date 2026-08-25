# Adapter: terminal and IDE agents

Use this adapter when the runtime is a terminal or editor-integrated coding agent
that reads a project instruction file, an `AGENTS.md` at the repository root or a
rules file the editor loads, and that can start separate runs or background agents
to act as workers. Runtimes in this class include, for example, Codex CLI, Cursor,
or a Kimi or Llama-based terminal agent; the list is illustrative, not exhaustive,
and implies no preference among them. Read this alongside `SKILL.md` and
`core/orchestrator.md`. Set `Adapter: terminal-agent` in `.scrum/state.md` when
this runtime is detected.

## Discovery through a project instruction file

A runtime in this class does not scan a skill directory. It reads one project
instruction file on every relevant request. Copy the package to `<project>/scrum/`
and add an include that points the agent at the core. The file to edit depends on
the runtime: an `AGENTS.md` at the repository root for agents that read one, or
the rules file an editor loads for its own agent. The include text is the same in
either case:

```markdown
# AGENTS.md
## Scrum organization
When asked to build, plan, run, review, or retro a product as a software team,
follow scrum/SKILL.md. Read scrum/adapters/terminal-agent.md for the role mapping.
Load scrum/core files by progressive disclosure per the stage table in
scrum/SKILL.md. Keep all project state in .scrum/ as plain markdown and commit
it with each increment.
```

The agent then discovers the skill from that file on any relevant request. The
Orchestrator is the main agent session and holds the no-coding rule while worker
runs are available.

### Role to primitive mapping

| Scrum role | Runtime primitive |
|---|---|
| Orchestrator | the main agent session |
| Product Owner | the session wearing a labeled `[PO]` turn |
| Scrum Master | the session wearing a labeled `[SM]` turn |
| Developers | a separate agent run per task, where the setup allows starting one; otherwise a sequential `[DEV]` turn |
| Verifier (DoD gate) | a separate run, or a labeled `[VERIFY]` pass distinct from the implementing turn |

### Worker runs and sequencing

Where the environment can start a distinct run (a separate invocation, a separate
process, a background agent, or a run in its own worktree), treat each as a
Developer with a full delegation brief: PBI id, Sprint Goal, acceptance criteria,
applicable DoD tiers, risk and threat route, adaptive test strategy, UI/UX route,
files in scope, constraints, minimum authority, private-data boundary, approval
and stop limits, writing standard, and the evidence to return.
Reconcile results in the main session and run the full test suite before the gate.

Where no worker run is available, switch roles sequentially in one session. The
Orchestrator writes the brief, then takes a labeled `[DEV]` turn to implement,
then a distinct `[VERIFY]` turn to walk `.scrum/DEFINITION_OF_DONE.md`. Keep the
turns visibly separated so PO, SM, DEV, and verification decisions stay traceable.
This matches the single-model protocol in `adapters/single-model.md`; use its
self-verification rules and its honest note that self-verification is weaker than
an independent verifier.

### Staffing tiers

The Staffing section of `.scrum/team.md` maps onto separate runs wherever the
harness lets a run pick its model: start Developer runs on a mid-tier worker
model, and keep the main session, the senior Developer run, and the verifier run
on the strongest available model, with the verifier never below the implementer's
tier. **Adaptation:** the senior Developer is a skill distribution inside the
single Developers accountability, not a new role or title. Where the harness
fixes one model for every run, staffing is a no-op and the labeled-hat discipline
in `adapters/single-model.md` substitutes.

## Runtimes that compose a system prompt instead of reading a file

Some runtimes in this class expose no project instruction file and no filesystem,
and are driven through an API that sets a system prompt per run. Compose the roles
into that system prompt.

1. Put the Orchestrator protocol in the system prompt: the no-coding rule (or its
   relaxation in single-model mode), the escalation ladder, and role-label
   discipline from `core/orchestrator.md`.
2. Load the role playbook for the active hat from `core/roles/` into the system
   prompt or the thread when that role acts.
3. Load `core/dod/definition-of-done.md` before any DoD gate and
   `core/events/*.md` before each event.
4. Load `core/artifact-writing-standard.md` once per invocation,
   `core/test-strategy.md` before a build, and `core/threat-modeling.md` or
   `core/ux-integration.md` when its trigger applies.
5. Use function or tool calling for any real actions (running tests, reading
   files). A tool result is the evidence the DoD gate records; never accept a
   "done" claim without it.

### Threads and state

Keep `.scrum/` state as fenced markdown blocks in the thread. On each stage
transition, emit the updated `state.md`, `backlog.md`, or `sprint.md` block so
the state is recoverable. On resume, paste the last known blocks back so the
Orchestrator can read the stage and continue. If the runtime has file access,
prefer writing `.scrum/` to disk and committing it.

### Parallel worker threads

If the setup runs multiple agent threads or parallel tool calls, assign each a
Developer brief and fan out independent PBIs, then reconcile in the Orchestrator
thread. If not, sequence the briefs. The protocol is identical either way.

## Escalation ladder

Follow `core/orchestrator.md` rungs: rebrief the same worker, spawn a fresh
worker with the failure trace, split or pair two approaches, let the Orchestrator
intervene directly as the sole exception to the no-coding rule (logged in the
sprint file), then escalate to the stakeholder with batched options and a
recommendation.
