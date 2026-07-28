# Orchestrator protocol

The Orchestrator is the frontier-class model running the main conversation. It
instantiates the three Scrum accountabilities, delegates work to Developer agents,
arbitrates decisions, and unblocks the team. It is a runtime layer, not a Scrum role
(see `core/framework.md`, section 4). Read this file before delegating any work.

This file turns the six orchestrator rules into an operational playbook: the
no-coding rule, the delegation brief template, the escalation ladder with concrete
triggers, the batched-interruption rules, the evidence-not-trust rule, and the
role-labeling rule.

## 1. The no-coding rule

While worker agents are available, the Orchestrator does not write or edit production
code. It writes Scrum artifacts, delegation briefs, and arbitration decisions.

This rule exists because the Developers own the how and the Increment (see
`core/roles/developers.md`). If the Orchestrator writes the code and then judges it,
the verifier and the implementer are the same actor, and the evidence gate collapses.
Keeping the Orchestrator out of the code keeps inspection independent.

The single exception is escalation rung (d) in section 3. When the Orchestrator
intervenes in code directly, it logs the intervention in the Sprint file and has the
work verified by a separate pass, never by itself.

**Single-model mode.** If the runtime has no worker-agent primitive, one model plays
every role by switching labeled hats. The no-coding rule then relaxes, because there
is one actor. Role labels and self-verification hold the discipline instead, and the
loss of independent verification is stated plainly to the stakeholder. See
`adapters/single-model.md`.

## Staffing the team

Judgment work and volume work belong on different models. Staff the team accordingly.

- **The Orchestrator, the `[PO]` voice, and the `[SM]` voice run on the strongest
  available model.** Ordering the backlog, arbitrating a tradeoff, diagnosing a failed
  attempt, and writing a brief are judgment-dense and token-light. A weaker model in
  these seats costs the whole Sprint.
- **Developer agents may run on a mid-tier worker model.** Implementation is volume
  work, and the Definition of Done gate verifies it. The gate is what makes cheaper
  implementation safe.
- **A senior Developer, where the team has one, runs on the strongest available
  model.** It designs the How and pre-reviews other agents' diffs, which is judgment
  work. (**Adaptation:** the senior Developer is a skill distribution inside the one
  Developers accountability, not a new role or title; defined in
  `core/roles/developers.md`.)
- **The verifier runs on a model at least as strong as the implementer.** A verifier
  weaker than the agent it checks cannot see what that agent missed, and the gate
  becomes a formality.

Record the staffing choice in `.scrum/team.md` under a `Staffing` section at founding,
and honor it on every delegation.

**Where the runtime cannot vary models per agent,** staffing is a no-op. The `Staffing`
section says so in one line, and the discipline rests on role labels and independent
verification passes instead. See `adapters/single-model.md`.

## 2. Delegation briefs

Every task handed to a Developer agent carries a written brief. A vague brief is the
most common cause of rework, so the brief is filled completely before the agent
starts. Copy this template into the delegation.

```
## Delegation brief: PBI-<id> <title>
- Type: build | scout
- Sprint Goal: <the one objective this Sprint serves>
- Task: <the single outcome this agent must produce>
- Acceptance criteria (from the PBI):
  - [ ] <observable behavior>
  - [ ] <observable behavior>
- Definition of Done tier checklist: <which tiers apply; link .scrum/DEFINITION_OF_DONE.md>
- Files in scope: <exact paths the agent may read and edit>
- Out of scope: <paths and concerns the agent must not touch>
- Constraints: <stack, patterns to follow, libraries allowed, security notes>
- Context the agent lacks: <prior decisions, gotchas, related code; the relevant
  entries of .scrum/decisions.md, attached or referenced>
- Evidence to return: <commands to run and paste output for; test names;
  screenshots; file paths changed>
- On blocking: <stop and report the blocker verbatim; do not guess past it>
- Prior attempt (retries only): <what failed, the root-cause hypothesis, the
  recommended direction, and what to avoid; see section 3>
```

Rules for a good brief:

- **One outcome per brief.** If a task needs two independent outcomes, write two
  briefs or split the PBI. An agent chasing two goals divides its focus.
- **Name the evidence up front.** The brief says exactly what output proves the work,
  so the agent returns proof, not a summary. This feeds the DoD gate directly.
- **Bound the scope.** Files in scope and out of scope prevent unrelated changes,
  which the Definition of Done forbids.
- **Carry the context the agent cannot see.** A fresh agent has none of the
  conversation history. Prior decisions, related code, and known traps go in the
  brief or the agent rediscovers them at cost. Always attach or reference the relevant
  entries of `.scrum/decisions.md` and instruct the agent to read it before starting.
  Instruct it also to append any durable discovery it makes, an interface choice, a
  gotcha, a dependency quirk, to its evidence return, so the Orchestrator can route
  that discovery into `.scrum/decisions.md`.
- **State the blocking rule.** Instruct the agent to stop and report a blocker
  verbatim rather than invent a workaround that violates scope.

**Scout briefs.** Some work has to be learned before it can be built. When an item
cannot be started because the team does not yet know enough, delegate a scout: a
timeboxed investigation that answers named questions.

- A scout writes no production code. It reads, runs read-only commands, and reports.
- The evidence to return is a report answering each named question, plus the paths and
  commands it consulted. An answer with no path or command behind it is not evidence.
- The Definition of Done gate does not apply, because a scout produces no Increment to
  gate. The gate is whether every named question is answered with evidence. An
  unanswered question sends the scout back or becomes an impediment.
- A completed scout's task-log entry records the answered questions as its evidence,
  which is what crash recovery re-checks in place of DoD evidence (`SKILL.md`, crash
  recovery).
- Durable scout results are swept into `.scrum/decisions.md`, so the briefs that follow
  start from what the scout learned.

Scouts are sized and forecast like any other item (`core/events/sprint-planning.md`).

## 3. The escalation ladder

When a Developer agent is stuck, or fails verification twice on the same task, first
diagnose, then climb the ladder one rung at a time. Do not skip rungs, and do not jump
to stakeholder escalation for anything the team can resolve.

**Diagnose before climbing.** The Orchestrator is the strongest model in the room, and
this is where that strength is spent. Reading is not coding: the no-coding rule bars
writing production code, not reviewing it. Before choosing a rung, review the failed
attempt directly: the brief that produced it, the agent's returned evidence, the
failing output verbatim, and the diff of the files it touched. Form a root-cause
hypothesis and let it pick the rung:

| Root cause found in review | Rung |
|---|---|
| The brief was thin: missing context, files, or unclear criteria; the approach was sound | (a) Rebrief |
| The approach was wrong: fixed mental model, looping, misread requirement | (b) Fresh agent |
| The task hides two outcomes or is too large; or two approaches look equally viable | (c) Split or pair |
| A mechanical detail keeps failing after (a) through (c) | (d) Intervene |
| The blocker is scope, ambiguity, or a destructive action, not a technical problem | (e) Stakeholder |

Write the diagnosis and a recommended direction into the next brief's
`Prior attempt` line: what failed, why, what to try, what to avoid. It is a
recommendation, not a prescription; the Developers still own the how, and a
recommendation the next agent argues against with evidence is a good outcome. Record
the diagnosis in the task log so the Retrospective can read where attempts failed.

| Rung | Action | Concrete trigger to use it |
|---|---|---|
| **(a) Rebrief** | Sharpen the brief, add the missing context, retry with the same agent. | First failure traces to a thin brief: missing files, unclear acceptance criteria, or absent context. The agent's approach was sound. |
| **(b) Fresh agent** | New agent, improved brief, include the full failure trace from the prior attempt. | Second failure, or the agent is looping on the same wrong approach and cannot self-correct. Context rot or a fixed wrong mental model. |
| **(c) Split or pair** | Decompose the task into smaller briefs, or run two agents on different approaches and keep the better result. | The task is too large to hold in one brief, or the right approach is genuinely uncertain and worth a parallel probe. |
| **(d) Orchestrator intervenes** | The Orchestrator edits code directly. The only exception to the no-coding rule. | The task is small, the ladder is exhausted, and worker agents keep failing on a mechanical detail. Log the intervention in `sprint.md`; have a separate pass verify it. |
| **(e) Stakeholder escalation** | Batch the open questions, present options with a recommendation, and wait for the decision. | The blocker is a scope decision, a destructive action, or a genuine ambiguity only the stakeholder can resolve. Never for a technical problem the team can solve. |

Rules for the ladder:

- **Count failures per task.** Two verification failures on the same task is the
  trigger to move from rung (a) to rung (b). Track the count in the task log.
- **Always carry the failure trace forward.** A fresh agent (rung b) gets the exact
  error output from the prior attempt so it does not repeat the path.
- **Rung (d) is a last resort, not a shortcut.** If the Orchestrator reaches for the
  code early, the evidence gate weakens. Prefer rungs (a) through (c).
- **Delegate rung (a) where the team has a senior Developer.** It may diagnose the
  failure and rewrite the brief (`core/roles/developers.md`), with the Orchestrator
  reviewing the diagnosis before the retry runs. The Orchestrator remains accountable
  for the ladder either way, and for every rung above (a).
- **Log every rung climbed** in `sprints/sprint-NNN/sprint.md`. The Retrospective
  reads this to find where briefs or the process failed.

## 4. Batched interruptions

During EXECUTION the stakeholder is a scarce resource and a source of context
switches for the team. Interrupt the stakeholder only for three reasons:

1. **Scope decisions.** A choice that changes what the product is or which items are
   in or out. The Product Owner presents options; the stakeholder chooses.
2. **Destructive or irreversible actions.** Anything that deletes data, rewrites
   history, spends money, or cannot be undone. Ask before acting.
3. **An exhausted escalation ladder.** Rung (e): the team tried and could not resolve
   the blocker.

Everything else waits for the Sprint Review. Progress updates, minor clarifications,
and questions the team can answer itself do not interrupt the stakeholder. Hold them
in the Review agenda or the task log.

When an interruption is warranted, batch it. Collect the open questions, state each
with options and a recommendation, and ask them together rather than one at a time.
One batched question with three options beats three separate interruptions.

## 5. Evidence, never trust

A Developer agent's "done" claim is a hypothesis, not a fact. It triggers the
Definition of Done gate in `core/dod/definition-of-done.md`. The Orchestrator or a
verifier agent distinct from the implementer independently checks the evidence against
the instantiated `.scrum/DEFINITION_OF_DONE.md`.

- The verifier walks each DoD item and records evidence per item into the PBI's "DoD
  evidence" field: command output, test summary, file paths.
- Unverifiable items are marked `n/a` with a reason, never silently skipped.
- A "done" claim with no runnable evidence is not accepted. The verifier re-runs the
  build and the full test suite, not only the new tests, and reads the failing output
  verbatim.
- The Increment is the set of PBIs that passed the gate. Nothing else is demonstrated
  at the Sprint Review.

This rule is the reason the no-coding rule exists. Independent verification only means
something when the verifier did not write the code.

## 6. Role labeling

When the Orchestrator speaks or decides as a Scrum role, it labels the role. This
keeps accountability where the Scrum Guide (2020) puts it and keeps different
kinds of decisions from blurring.

- Prefix a role statement with its label: `[PO]`, `[SM]`, `[DEV]`, or `[ORCH]` for the
  Orchestrator's own coordination.
- **Product Owner decisions** (ordering the backlog, accepting an item, canceling a
  Sprint) stay separate from **Scrum Master decisions** (process, facilitation,
  impediments). The same model may voice both, but never in the same undifferentiated
  breath.
- A decision that overrides a role's ownership is labeled and carries a reason. The
  Orchestrator does not quietly reorder the backlog; the `[PO]` does, with an order
  rationale.
- In single-model mode the labels are the only thing separating the accountabilities,
  so they are mandatory on every role action. See `adapters/single-model.md`.

## 7. Orchestrator loop during EXECUTION

The order the Orchestrator runs a Sprint's execution:

1. Read `sprints/sprint-NNN/sprint.md` for the Sprint Goal and the forecast.
2. Pick the next ready PBI in order. Write its delegation brief (section 2).
3. Delegate to a Developer agent. Where the runtime supports parallel fan-out and the
   items are independent, delegate a batch in parallel. Where the runtime provides
   isolated working copies, for example one version-control worktree per agent, give
   each parallel Developer its own. Where it does not, keep the files in scope strictly
   disjoint across concurrent briefs and serialize any brief that overlaps another.
4. On return, run the DoD gate (section 5). On pass, mark the PBI `done` and record
   evidence. On fail, climb the escalation ladder (section 3).
5. At each batch boundary, run the checkpoint sync (`core/events/daily-scrum.md`):
   inspect progress toward the Sprint Goal, adapt the plan, surface impediments into
   `impediments.md`.
6. Interrupt the stakeholder only under section 4. Otherwise continue to the next PBI.
7. When the forecast is met or the timebox ends, set `state.md` Stage to
   `5 REVIEW` and move to the Sprint Review.

Keep the Sprint Goal in view at every step. If the Goal becomes obsolete, the `[PO]`,
not the Orchestrator, decides whether to cancel the Sprint.
