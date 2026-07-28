<!--
  TEMPLATE: decisions.md
  Instantiate to .scrum/decisions.md at stage 4 EXECUTION, at the first checkpoint
  that has something durable to record.
  This file is the team's shared memory: the decisions, interfaces, and gotchas
  that every Developer brief must carry, so a fresh agent neither rediscovers them
  nor contradicts them. Written at the checkpoint sync
  (core/events/daily-scrum.md), pruned at the Retrospective
  (core/events/retrospective.md). Keep it plain markdown, committed to the repo.
-->

# Team decisions

<!--
  What belongs here:
  - a decision later work must respect (a chosen library, a naming rule, a
    pattern the code now follows)
  - an interface another agent has to call correctly (a signature, a file
    contract, an environment variable)
  - a gotcha that cost one agent time and would cost the next one the same

  What does not belong here: task state (that is the sprint task log), product
  scope (that is the backlog), or process problems (those are impediments.md).

  Entry shape, one line each, oldest first:

  - <YYYY-MM-DD> <area>: <one-line decision or gotcha> (source: PBI-NNN)

  Keep the file short enough to paste into every delegation brief. At the
  Retrospective, prune entries that no longer bind: a decision the code now
  enforces on its own, an interface that was deleted, a gotcha a fix made
  obsolete. Record each removal below so the history stays transparent.
-->

## Entries

<!--
  Two illustrative entries; delete before use.

  - 2026-07-20 auth: Sessions are validated in middleware only; no route checks
    its own token. (source: PBI-012)
  - 2026-07-21 test runner: The suite needs the fixture server started first; a
    bare test command fails with a connection error, not a test failure.
    (source: PBI-015)
-->

- <YYYY-MM-DD> <area>: <one-line decision or gotcha> (source: PBI-NNN)

## Pruned
<!-- Entries removed at a Retrospective, with the Sprint that removed them. -->
- <YYYY-MM-DD, sprint-NNN>: removed <entry summary> because <reason>
