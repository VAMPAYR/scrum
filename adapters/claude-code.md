# Adapter: Claude Code

Map the Scrum organization onto Claude Code's main loop and subagents. Read this
alongside `SKILL.md` and `core/orchestrator.md`.

## Role to primitive mapping

| Scrum role | Claude Code primitive |
|---|---|
| Orchestrator | the main conversation loop |
| Product Owner | the main loop wearing a labeled `[PO]` turn |
| Scrum Master | the main loop wearing a labeled `[SM]` turn |
| Developers | subagent / Task invocations, one per worker |
| Verifier (DoD gate) | a separate subagent, never the implementer |

The Orchestrator, PO, and SM run in the main loop because they facilitate,
decide, and arbitrate rather than write production code. Developers run as
subagents so their work is isolated and independently verifiable.

## Install path

- User-wide: `~/.claude/skills/scrum/`.
- Single project: `<project>/.claude/skills/scrum/`.

The `SKILL.md` frontmatter drives discovery. Set `Adapter: claude-code` in
`.scrum/state.md` when this runtime is detected.

## Orchestrator = main loop

The main loop holds the no-coding rule from `core/orchestrator.md`. While
subagents are available it writes Scrum artifacts, delegation briefs, and
arbitration decisions, and it dispatches all production code to Developer
subagents. It speaks as PO or SM only under an explicit `[PO]` or `[SM]` label,
keeping ordering and acceptance decisions (PO) separate from process decisions
(SM).

## Developers = subagents

Spawn one subagent per Developer task with the Task tool. Every delegation brief
carries the fields required by `core/orchestrator.md`:

- PBI id and title
- Sprint Goal
- acceptance criteria (verbatim from the PBI)
- the DoD tier checklist that applies (from `.scrum/DEFINITION_OF_DONE.md`)
- files in scope and files off-limits
- constraints (patterns to follow, libraries allowed)
- what evidence to return (command output, test summary, file paths, diffs)

The subagent implements, runs the tests and checks itself, and returns evidence.
Honest reporting is mandatory: failed test output is returned verbatim, never
smoothed over (see `core/roles/developers.md`).

## Staffing: a model tier per seat

Subagents can each run a different model, so the Staffing section of
`.scrum/team.md` maps directly onto dispatch:

- Orchestrator, PO, and SM: the strongest available model. They facilitate,
  arbitrate, and diagnose, which is where judgment pays.
- Developer briefs: a mid-tier worker model. This is where most of the token
  volume goes, and the brief already carries the thinking.
- Senior Developer, when `Staffing > Senior Developer: on`: the strongest
  available model, briefed on the hardest or highest-blast-radius task of the
  Sprint and on any task a rung of the escalation ladder has already failed.
  **Adaptation:** this is a skill distribution inside the single Developers
  accountability, not a new role or title. Official Scrum defines no sub-roles or
  titles inside Developers, and the senior Developer holds no authority the other
  Developers lack.
- Verifier: at least the implementer's tier, and the strongest available for
  security-sensitive or irreversible work. A weaker verifier cannot gate a
  stronger implementer.

Where the harness exposes git worktrees, give each parallel Developer its own
worktree so concurrent briefs cannot collide in the working tree, and reconcile
the results in the main loop before the DoD gate. Where it does not, keep
parallel briefs on disjoint files as the next section requires.

## Parallel fan-out

When PBIs or tasks are independent, dispatch subagents in parallel by issuing
their Task calls in one turn. Use fan-out when:

- multiple PBIs in the Sprint Backlog touch disjoint files, or
- escalation rung (c) runs two approaches to the same task and takes the better
  result.

Do not fan out tasks that write the same files or depend on each other's output;
sequence those. After a parallel batch returns, the Orchestrator reconciles the
results, resolves any file conflicts, and runs the full test suite once over the
combined change before the DoD gate.

Where the harness does not expose parallelism, dispatch the same briefs
sequentially; the protocol is unchanged.

## The DoD gate as a distinct subagent

When a Developer subagent reports `done`, the Orchestrator opens the gate from
`core/dod/definition-of-done.md`. Spawn a verifier subagent that did not write
the code. Its brief: walk `.scrum/DEFINITION_OF_DONE.md` item by item, run each
check, and record evidence or an `n/a` reason into the PBI's "DoD evidence"
field. The Orchestrator marks the PBI `done` only on a clean verifier pass. This
realizes "evidence, never trust" with agent independence.

## Escalation ladder on Claude Code

Follow the rungs in `core/orchestrator.md`:

1. **Rebrief**: re-invoke the same subagent role with a sharper brief and the
   failure trace.
2. **Fresh agent**: spawn a new subagent with an improved brief that includes
   the prior failure output.
3. **Split or pair**: decompose into smaller Task calls, or fan out two
   subagents with different approaches and keep the better result.
4. **Orchestrator intervenes**: the main loop edits code directly. This is the
   only exception to the no-coding rule; log it in the sprint file.
5. **Stakeholder escalation**: batch questions, present options with a
   recommendation, and wait.

## Events and state

The Orchestrator facilitates the events in `core/events/` from the main loop.
Sprint Planning, the checkpoint sync (adapted Daily Scrum), Sprint Review, and
Retrospective are conversation turns, not subagents. All state writes go to
`.scrum/` in plain markdown. Commit `.scrum/` together with the code increment so
the project resumes cleanly in any tool.

During EXECUTION, interrupt the stakeholder only for scope decisions, destructive
actions, or an exhausted escalation ladder. Everything else waits for the Sprint
Review (see `core/orchestrator.md`).
