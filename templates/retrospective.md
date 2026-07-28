<!--
  TEMPLATE: retrospective.md
  Instantiate to .scrum/sprints/sprint-NNN/retrospective.md at stage 6 RETRO.
  The Retrospective inspects the AI team itself: brief quality, gate failures,
  rework, and interactions (core/events/retrospective.md). It must produce at
  least one concrete improvement that enters the next Sprint or amends team.md.
  Read core/anti-patterns.md if a health check ran. Keep it plain markdown,
  committed to the repo.
-->

# Sprint NNN Retrospective

- Date: <YYYY-MM-DD>
- Participants: the AI Scrum Team (PO, SM, Developers). Stakeholder not present.

## Data inspected
<!--
  Ground the Retro in objective data, not impressions (health check S3.3). Pull
  from metrics.md and the sprint task log.
-->
- Metrics (from metrics.md): throughput, DoD pass rate, rework count, cycle time, escaped defects
- Delegation-brief quality: <briefs that were clear vs those that caused rework>
- Gate failures: <false "done" caught by the verifier; what caused them>
- Impediments: <from impediments.md: what blocked, how it resolved>
- Health check (if run): <area scores and flags from core/anti-patterns.md>

## What went well
<!-- Acknowledge success; do not jump straight to fixes (health check S3.7). -->
- <what worked, worth keeping>

## What to improve
<!-- Name the real problems, including the big ones, not only easy tweaks. -->
- <problem observed, with the data that shows it>

## decisions.md sweep
<!--
  Maintenance of the team's shared memory, a required output of this event
  (core/events/retrospective.md). Prune what the work made stale, resolve entries
  that now contradict each other so the next Sprint's briefs carry one answer, and
  promote a gotcha that appeared more than once into a standing rule. A file nobody
  prunes stops being read.
-->
- Pruned as stale: <entries removed and why, or none>
- Contradictions resolved: <which entries disagreed, and the single answer kept, or none>
- Promoted: <recurring gotcha, and where it landed: a team.md norm for how the team
  works, or a Tier 3 rule in DEFINITION_OF_DONE.md for a project quality bar the gate
  should enforce; or none>

## Improvement items
<!--
  At least one. Each must be specific, owned by a team role, with a first step and
  a success measure, sized to fit one Sprint (health checks S3.1, S3.2, S3.8). If a
  health check flagged an area, turn its recommended recovery experiment into one
  of these. Vague intentions do not count.
-->
### Improvement 1
- Action: <the specific change>
- Owner: <PO | SM | Developers>
- First step: <what happens first>
- Success measure: <how the team will know it worked>
- Lands in: <next sprint plan | team.md amendment | DEFINITION_OF_DONE.md>

<!-- Repeat if more than one improvement is committed; keep the set small. -->

## Carry-forward check
<!--
  Health check S3.5: confirm the PRIOR Sprint's improvement items were acted on.
  An improvement that left no downstream trace is Retro theater.
-->
- Prior improvement(s): <from sprint-(NNN-1)/retrospective.md>
- Acted on: <yes, where the change shows | no; escalate as a finding>

## Metrics update
<!-- Append the improving-family notes to .scrum/metrics.md for this Sprint. -->
```markdown
## sprint-NNN retro
- Improvement committed: <one line>
- Prior improvement landed: <yes | no>
- Double-loop note (if any belief/rule was challenged): <...>
```

<!--
  A new Sprint starts immediately after, with no gap. Carry the improvement item
  into the next Sprint plan (templates/sprint.md) or amend team.md now
  (templates/team.md, Amendments log).
-->
