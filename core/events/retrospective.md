# Sprint Retrospective

## Purpose

The Sprint Retrospective is the team's session for raising its own quality and
effectiveness. The Scrum Team examines how the last Sprint went across its people,
interactions, processes, tools, and Definition of Done, then commits to the changes that
will help most and acts on them as soon as possible, adding them to the next Sprint where
useful.

## Participants

- **The whole Scrum Team**: Product Owner, Scrum Master, and Developers, as equal
  members. The Retrospective is team-only; nobody outside the team participates.
- **Scrum Master (SM)** facilitates, encourages every member to contribute, and takes
  part as a team member.
- The **human stakeholder does not attend.** The Retrospective inspects the team, and its
  candor depends on being closed to outsiders.

## Inputs

- `sprints/sprint-NNN/sprint.md`: the Sprint Goal, the forecast versus what passed the
  gate, and the task log including every escalation-ladder rung climbed.
- `sprints/sprint-NNN/review.md`: what the Review surfaced, including any stakeholder
  surprise.
- `.scrum/metrics.md`: DoD pass rate, rework count, escaped defects, throughput.
- `impediments.md`: what blocked the team and how long it stayed open.
- `.scrum/decisions.md`: the knowledge the Sprint's checkpoints swept in, read here for
  maintenance as well as for findings.
- `core/anti-patterns.md`: the scrum health checks, a set of process-decay symptoms to
  test the team against.

## AI-adapted procedure

**Adaptation: the Retrospective inspects the AI team itself.** The subjects official
Scrum names, individuals, interactions, processes, tools, and the Definition of Done, map
onto the machinery of an AI Scrum organization. The team inspects the quality of its
delegation briefs, the gate failures, the rework, and the escalations, and it improves
that machinery. The intent is preserved: a blame-free inspection of the whole Sprint that
ends in a committed improvement.

Work through five inspection areas, grounded in the recorded evidence, not in
impressions:

1. **Brief quality.** Read the escalations in the task log. How many failures traced to a
   thin or wrong delegation brief (missing files, unclear acceptance criteria, absent
   context)? Brief-caused rework is the most fixable failure. Name the specific brief
   defects.
2. **Gate failures.** How many PBIs failed the Definition of Done gate, and why? A high
   failure rate points to weak acceptance criteria, an unclear DoD, or forecasting work
   the team could not make Done. Distinguish honest gate catches (the gate working) from
   repeated failures on the same cause (a process defect).
3. **Rework count.** How many items were built, failed verification, and rebuilt? Track
   the count in `metrics.md` across Sprints. Rising rework is a signal to change the brief
   template, the DoD, or the forecasting.
4. **Interactions and role integrity.** Did the roles stay separate? Did the Orchestrator
   hold the no-coding rule, or intervene early? Were decisions labeled by role? Blurred
   accountability is a process defect to fix.
5. **Definition of Done and process decay.** Did the DoD hold, or was it quietly weakened
   under time pressure? Run the team against `core/anti-patterns.md`: check for
   process-decay symptoms such as feedback that changes nothing, a DoD that is a checkbox,
   or work presented as done without evidence.

For each area, ask what went well to keep, and what to change. Ground every finding in a
number or a specific event from the inputs, so the Retrospective adapts from evidence
rather than opinion.

**Sweep `decisions.md`.** The Retrospective is where the team's knowledge file is
maintained, not only added to. Prune entries the work has made stale, and resolve
entries that now contradict each other so the next Sprint's briefs carry one answer
rather than two. Then read the gotchas that appeared more than once: a recurring gotcha
is a candidate for promotion, into a `team.md` norm when it is about how the team works,
or into a Tier 3 rule of `.scrum/DEFINITION_OF_DONE.md` when it is a project-specific
quality bar the gate should enforce. A decisions file nobody prunes stops being read,
and a file nobody reads stops preventing rework.

**Mandatory output: at least one improvement item.** The Retrospective does not end
without at least one concrete improvement, and that improvement goes into effect. Route
each improvement to one of two destinations:

- **Into the next Sprint.** A process change the team will apply immediately becomes a PBI
  or a task in the next Sprint's plan (for example, "add a files-in-scope section to every
  delegation brief"). Add it to the top of the backlog so it is acted on, not filed away.
- **Into `team.md`.** A durable norm, standard, or template change amends `.scrum/team.md`
  (for example, "the DoD gate re-runs the full test suite, never only the new tests"). This
  changes the team's standing behavior for every future Sprint.

An improvement with no destination is not an improvement. The SM confirms each item lands
in the next Sprint or in `team.md` before the event closes.

Decision rules for the Retrospective:

- **Do not drop the Retrospective**, even if the team declares it unnecessary or a
  stakeholder wants to skip it for time. It is required in Scrum. If it feels unproductive,
  improve how it is run rather than remove it.
- **Keep it blame-free.** The Retrospective inspects processes, interactions, and tools,
  not individual fault. For agents this is natural; keep the focus on the machinery.
- **Prefer one or two changes the team will actually make** over a long list it will not. A
  Retrospective that generates ten items and acts on none has failed.
- **Feed recurring impediments back here.** An impediment that reappears Sprint after Sprint
  is a process defect for the Retrospective, not a one-off to clear again.

## Outputs (`.scrum/` file changes)

- `sprints/sprint-NNN/retrospective.md`: the findings per inspection area, and the
  improvement items with their destinations.
- `team.md`: amended with any durable norm, standard, or template change (required if an
  improvement targets standing behavior).
- The next Sprint's plan or `product/backlog.md`: the immediate improvement added as a task
  or PBI (required if an improvement targets the next Sprint).
- `decisions.md`: stale entries pruned, contradictions resolved, promoted entries marked
  or removed.
- `metrics.md`: rework count, gate pass rate, and brief-caused failures recorded for trend
  tracking.
- `state.md`: `Stage` set to `2 REFINEMENT` or `3 PLANNING` for the next Sprint, `Updated`
  set. A new Sprint starts immediately, with no gap.

## SM facilitation notes

- **Guarantee the improvement item lands.** The event's one non-negotiable output is at
  least one improvement that enters the next Sprint or amends `team.md`. Do not close the
  Retrospective until it is written to its destination.
- **Anchor findings in the evidence.** Bring the numbers: gate pass rate, rework count,
  escalation rungs climbed. Coach the team away from vague impressions toward specific,
  recorded causes.
- **Encourage every role to contribute**, and take part as a member yourself. Surface what
  went well to keep, not only what failed.
- **Run the health check every Retrospective.** A standing pass against
  `core/anti-patterns.md` catches process decay before it sets in.
- **Close the loop next Sprint.** At the next Retrospective, check whether the last
  improvement was applied and whether it helped. Improvement that is never verified is
  improvement in name only.

## Timebox

Official Scrum bounds the Sprint Retrospective at a maximum of three hours for a one-month
Sprint, and proportionally shorter for a shorter Sprint. It concludes the Sprint.

**Adaptation.** For a Sprint of hours the Retrospective is a short session proportional to
the Sprint, long enough to inspect the five areas and commit at least one improvement. The
purpose and the team-only, blame-free character are unchanged; only the duration scales
down. A new Sprint starts immediately after, with no gap.
