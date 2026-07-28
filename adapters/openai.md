# Adapter: OpenAI Codex CLI and GPT

Map the Scrum organization onto OpenAI runtimes. Read this alongside `SKILL.md`
and `core/orchestrator.md`. Set `Adapter: openai` in `.scrum/state.md` when this
runtime is detected.

## Codex CLI via AGENTS.md

Codex reads `AGENTS.md` from the project root. Copy the package to
`<project>/scrum/` and add an include that points Codex at the core:

```markdown
# AGENTS.md
## Scrum organization
When asked to build, plan, run, review, or retro a product as a software team,
follow scrum/SKILL.md. Read scrum/adapters/openai.md for the role mapping.
Load scrum/core files by progressive disclosure per the stage table in
scrum/SKILL.md. Keep all project state in .scrum/ as plain markdown and commit
it with each increment.
```

Codex then discovers the skill from `AGENTS.md` on any relevant request. The
Orchestrator is the Codex main loop and holds the no-coding rule while worker
runs are available.

### Role to primitive mapping (Codex CLI)

| Scrum role | Codex primitive |
|---|---|
| Orchestrator | the main Codex session |
| Product Owner | the session wearing a labeled `[PO]` turn |
| Scrum Master | the session wearing a labeled `[SM]` turn |
| Developers | a separate Codex worker run per task, where the setup allows spawning one; otherwise a sequential `[DEV]` turn |
| Verifier (DoD gate) | a separate run, or a labeled `[VERIFY]` pass distinct from the implementing turn |

### Worker runs and sequencing

Where the environment can start a distinct Codex run (a separate invocation,
process, or worktree), treat each as a Developer with a full delegation brief:
PBI id, Sprint Goal, acceptance criteria, applicable DoD tiers, files in scope,
constraints, and the evidence to return. Reconcile results in the main session
and run the full test suite before the gate.

Where no worker run is available, switch roles sequentially in one session. The
Orchestrator writes the brief, then takes a labeled `[DEV]` turn to implement,
then a distinct `[VERIFY]` turn to walk `.scrum/DEFINITION_OF_DONE.md`. Keep the
turns visibly separated so PO, SM, DEV, and verification decisions stay traceable.
This matches the single-model protocol in `adapters/generic.md`; use its
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
in `adapters/generic.md` substitutes.

## GPT and Assistants via system-prompt composition

When there is no CLI or filesystem, compose the roles into the system prompt.

1. Put the Orchestrator protocol in the system prompt: the no-coding rule (or its
   relaxation in single-model mode), the escalation ladder, and role-label
   discipline from `core/orchestrator.md`.
2. Load the role playbook for the active hat from `core/roles/` into the system
   prompt or the thread when that role acts.
3. Load `core/dod/definition-of-done.md` before any DoD gate and
   `core/events/*.md` before each event.
4. Use function/tool calling for any real actions (running tests, reading files).
   A tool result is the evidence the DoD gate records; never accept a "done"
   claim without it.

### Threads and state

Keep `.scrum/` state as fenced markdown blocks in the thread. On each stage
transition, emit the updated `state.md`, `backlog.md`, or `sprint.md` block so
the state is recoverable. On resume, paste the last known blocks back so the
Orchestrator can read the stage and continue. If the runtime has file access,
prefer writing `.scrum/` to disk and committing it.

### Parallel Assistants

If the setup runs multiple Assistants or parallel tool calls, assign each a
Developer brief and fan out independent PBIs, then reconcile in the Orchestrator
thread. If not, sequence the briefs. The protocol is identical either way.

## Escalation ladder

Follow `core/orchestrator.md` rungs: rebrief the same worker, spawn a fresh
worker with the failure trace, split or pair two approaches, let the Orchestrator
intervene directly as the sole exception to the no-coding rule (logged in the
sprint file), then escalate to the stakeholder with batched options and a
recommendation.
