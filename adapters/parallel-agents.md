# Adapter: parallel worker agents

Use this adapter when the runtime can spawn parallel worker agents, meaning child
agent runs dispatched from a main conversation loop that execute concurrently and
return their results, and when it auto-discovers a skill folder from the
frontmatter in `SKILL.md`. Read this alongside `SKILL.md` and
`core/orchestrator.md`. Set `Adapter: parallel-agents` in `.scrum/state.md` when
this runtime is detected.

## Role to primitive mapping

| Scrum role | Runtime primitive |
|---|---|
| Orchestrator | the main conversation loop |
| Product Owner | the main loop wearing a labeled `[PO]` turn |
| Scrum Master | the main loop wearing a labeled `[SM]` turn |
| Developers | worker agents, one per task, dispatched concurrently |
| Verifier (DoD gate) | a distinct worker agent, never the implementer |

The Orchestrator, PO, and SM run in the main loop because they facilitate,
decide, and arbitrate rather than write production code. Developers run as worker
agents so their work is isolated and independently verifiable.

## Install path

Discovery is automatic in this class of runtime: the runtime scans its skill
directories and reads the `name` and `description` frontmatter in `SKILL.md` to
decide when the skill applies, so no include line is required. Install the
package with the folder name `scrum` and `SKILL.md` at its root, into a directory
the runtime scans. Two scopes are usual:

- a user-level skills directory, which makes the package available in every
  project;
- a project-level skills directory inside the repository, which scopes the
  package to one project.

Directory names differ per runtime. Take the exact path from the runtime's own
documentation.

## Orchestrator = main loop

The main loop holds the no-coding rule from `core/orchestrator.md`. While worker
agents are available it writes Scrum artifacts, delegation briefs, and arbitration
decisions, and it dispatches all production code to Developer agents. It speaks as
PO or SM only under an explicit `[PO]` or `[SM]` label, keeping ordering and
acceptance decisions (PO) separate from process decisions (SM).

## Developers = worker agents

Spawn one worker agent per Developer task, using whatever the runtime calls its
agent-spawn primitive (a task tool, a subagent call, a background agent). Every
delegation brief carries the fields required by `core/orchestrator.md`:

- PBI id and title
- Sprint Goal
- acceptance criteria (verbatim from the PBI)
- the DoD tier checklist that applies (from `.scrum/DEFINITION_OF_DONE.md`)
- material risks, threat-model route, and adaptive test strategy with its reason
- UI/UX route and design evidence when applicable
- files in scope and files off-limits
- constraints, minimum authority, approval and stop limits, and private-data boundary
- required capabilities, attempt budget, progress evidence, baseline, stop
  conditions, and diagnostic route
- the writing contract from `core/artifact-writing-standard.md`
- what evidence to return (commands, test and analysis results, risk or design
  evidence, file paths, and the full diff)

The worker implements under `core/engineering-standards.md`, follows the selected
route in `core/test-strategy.md`, runs the checks, inspects generated output, and
returns evidence.
Honest reporting is mandatory: failed test output is returned verbatim, never
smoothed over (see `core/roles/developers.md`).

## Staffing: a model tier per seat

Worker agents can each run a different model where the runtime lets a run pick
one, so the Staffing section of `.scrum/team.md` maps directly onto dispatch:

- Orchestrator, PO, and SM: the strongest available model. They facilitate,
  arbitrate, and diagnose, which is where judgment pays.
- Developer briefs: a mid-tier worker model. This is where most of the token
  volume goes, and the brief already carries the thinking.
- Senior Developer, when `Staffing > Senior Developer: on`: the strongest
  available model, briefed on the hardest or highest-blast-radius task and used
  for read-only diagnosis when its capabilities match a stalled task.
  **Adaptation:** this is a skill distribution inside the single Developers
  accountability, not a new role or title. The Scrum Guide (2020) defines no
  sub-roles or titles inside Developers, and the senior Developer holds no
  authority the other Developers lack.
- Verifier: at least the implementer's tier, and the strongest available for
  security-sensitive or irreversible work. A weaker verifier cannot gate a
  stronger implementer.

Where the harness fixes one model for every agent, staffing is a no-op: record
the single tier in `team.md` and rest the discipline on agent independence at the
gate.

Record each available specialist's domain, tools, authority, and diagnostic
strength in the `team.md` capability registry. For support, match required
authority and capability first, then diagnostic strength, model tier, and cost.

Where the harness exposes git worktrees, give each parallel Developer its own
worktree so concurrent briefs cannot collide in the working tree, and reconcile
the results in the main loop before the DoD gate. Where it does not, keep
parallel briefs on disjoint files as the next section requires.

## Parallel fan-out

When PBIs or tasks are independent, dispatch worker agents in parallel by issuing
their spawn calls in one turn. Use fan-out when:

- multiple PBIs in the Sprint Backlog touch disjoint files, or
- a diagnosed uncertainty justifies two isolated, discriminating approaches.

Do not fan out tasks that write the same files or depend on each other's output;
sequence those. After a parallel batch returns, the Orchestrator reconciles the
results, resolves any file conflicts, and runs the full test suite once over the
combined change before the DoD gate.

Where the harness dispatches workers only one at a time, dispatch the same briefs
sequentially; the protocol is unchanged. Where the runtime exposes no worker
primitive at all, follow `adapters/single-model.md` instead.

## The DoD gate as a distinct worker agent

When a Developer agent reports `done`, the Orchestrator opens the gate from
`core/dod/definition-of-done.md`. Spawn a verifier agent that did not write the
code. Its brief: walk `.scrum/DEFINITION_OF_DONE.md` item by item, run each check,
and record evidence or an `n/a` reason into the PBI's "DoD evidence" field. The
Orchestrator marks the PBI `done` only on a clean verifier pass. This realizes
"evidence, never trust" with agent independence.

## Stall recovery with worker agents

On a stall trigger, load `core/stall-recovery.md`, pause the mutating worker, and
preserve its worktree. Run `scripts/stall_router.py` when executable tools are
available. Spawn the capability-matched expert with read-only authority and the
blocker packet, original brief, actual diff, and exact failure evidence. The
expert returns one discriminating next step; it does not silently take over.

The Orchestrator then resumes or rebriefs the worker, assigns a fresh worker,
pairs, splits, opens a scout or impediment, or uses the tightly bounded mechanical
intervention route. Two mutating approaches run only in separate worktrees. The
implementer and any co-implementing expert remain ineligible for final
verification.

## Events and state

The Orchestrator facilitates the events in `core/events/` from the main loop.
Sprint Planning, the checkpoint sync (adapted Daily Scrum), Sprint Review, and
Retrospective are conversation turns, not worker agents. All state writes go to
`.scrum/` in plain markdown. Commit `.scrum/` together with the code increment so
the project resumes cleanly in any tool.

During EXECUTION, interrupt the stakeholder only for product scope or intent,
destructive authority, or an ambiguity only that person can resolve. Technical
uncertainty remains with the team (see `core/stall-recovery.md`, STALL-8).
