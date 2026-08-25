<!--
  TEMPLATE: sprint.md
  Instantiate to .scrum/sprints/sprint-NNN/sprint.md at stage 3 PLANNING.
  The Sprint Backlog: the Sprint Goal (Why), the forecast (What), the plan (How),
  a task log with delegation-brief references, and checkpoint entries (the adapted
  Daily Scrum). The Developers own this file. Keep it plain markdown, committed to
  the repo. Sprint numbers are zero-padded: sprint-001, sprint-002, ...
-->

# Sprint NNN

- Started: <YYYY-MM-DD>
- Cadence: <from team.md: a few hours | a day | ...>

## Sprint Goal (Why)
<!--
  One objective that gives the Sprint focus and binds the Developers. State a
  stakeholder outcome or a hypothesis, not a list of tasks (health checks S1.3,
  S4.1, S4.2). The Sprint Goal is a commitment, not a forecast. Functionality may
  flex to meet it; the Goal does not.
-->
<The single Sprint Goal, traceable to product-goal.md.>

## Forecast (What)
<!--
  The PBIs the Developers forecast they can bring to Done this Sprint. Reference
  them by id from product/backlog.md. No Size: L item may be forecast; split it
  first. Keep the forecast small enough to finish (health check S2.6).
-->
- PBI-NNN: <title> (Size: <XS|S|M>)
- PBI-NNN: <title> (Size: <XS|S|M>)

## Plan (How)
<!--
  How the Developers intend to build the forecast: sequencing, the riskiest
  assumption to test first (from team.md risk appetite), dependencies, and which
  work can run in parallel. Adjusted at checkpoints as the team learns.
-->
<The plan. Note the order of attack and any dependencies between PBIs.>

- Material risks and assumptions: <risk ids, consequence, owner, or none with reason>
- Threat-model route: <update/create path | existing model sufficient | n/a with reason>
- Test routes by PBI: <TDD, regression-first, characterization, property, fuzz, contract, integration, end-to-end, static/formal, exploratory/visual, eval, or spike; reason>
- UX routes by PBI: <ux-fit + evidence path | fallback | n/a with reason>
- High-impact assurance cases: <PBI ids and path | none>

## Task log
<!--
  One entry per delegated task. Each references its delegation brief so the work
  is traceable. A delegation brief (core/orchestrator.md) includes: Type
  (build | scout), PBI id, the Sprint Goal, acceptance criteria, the DoD tier
  checklist, risk and threat route, test strategy, UX route, exact authority,
  private-data boundary, files in scope, constraints, writing standard, and what
  evidence to return. Store the brief inline or as a file under this sprint dir
  and reference it here.

  Status: assigned | in-progress | in-review | done | blocked | reworked
  Keep WIP low: few tasks in-progress at once (health check S2.10).
-->

### Task: <short name> (PBI-NNN)
- Brief: <path to delegation brief, e.g. briefs/PBI-NNN.md, or "inline below">
- Agent: <worker agent id, or [DEV] hat in single-model mode>
- Status: assigned | in-progress | in-review | done | blocked | reworked
- Evidence returned: <commands, test and analysis results, red-then-green result when selected, risk/design evidence, diff, file paths; feeds the DoD gate>
- Verification: <verifier agent id or [ORCH]; PASS | FAIL with reason>
- Diagnosis (retries only): <root-cause hypothesis for the failed attempt and the
  recommended direction, per core/orchestrator.md section 3>
- Notes: <rework count, escalation-ladder rung used, links>

<!-- Repeat one Task block per delegated task. -->

## Checkpoints
<!--
  The adapted Daily Scrum. Adaptation: a checkpoint sync the Developers run
  between task batches, same purpose as the Daily Scrum in a compressed cadence
  (core/events/daily-scrum.md). Each checkpoint inspects progress toward the
  Sprint Goal, adapts the plan, and surfaces impediments.
-->

### Checkpoint <n> (<timestamp>)
- Progress toward the Sprint Goal: <where the work stands against the Goal>
- Plan adaptation: <what changed in the plan and why>
- Impediments surfaced: <blocker + owner; logged in ../../impediments.md>
- Knowledge swept: <durable decisions, interfaces, and gotchas this batch returned,
  appended to ../../decisions.md; or none>

<!-- Repeat one Checkpoint block per sync. -->

## Sprint outcome
<!-- Filled at the end of the Sprint, before the Review. -->
- PBIs that passed the DoD gate (the Increment): <PBI ids>
- Carryover (not Done, returned to the backlog): <PBI ids + remaining work>
- Sprint Goal met: <yes | partially | no; one line on what was learned>
- Ended: <YYYY-MM-DD>

<!--
  A Sprint may be cancelled only by the Product Owner, and only when the Sprint
  Goal becomes obsolete (core/roles/product-owner.md). Record a cancellation here
  with the reason. The Increment is the set of PBIs that passed the gate; only
  those are demonstrated at the Review (templates/review.md).
-->
