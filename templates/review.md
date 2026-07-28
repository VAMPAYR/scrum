<!--
  TEMPLATE: review.md
  Instantiate to .scrum/sprints/sprint-NNN/review.md at stage 5 REVIEW.
  The Sprint Review inspects the Increment with the stakeholder and adapts the
  Product Backlog (core/events/sprint-review.md). It demonstrates evidence, hands
  the stakeholder the product to use, and gathers feedback. It is NOT a release
  gate: items meeting the Definition of Done can be released any time. Keep it
  plain markdown, committed to the repo.
-->

# Sprint NNN Review

- Date: <YYYY-MM-DD>
- Sprint Goal (recap): <the Goal from sprint.md>
- Sprint Goal met: <yes | partially | no>

## Increment demonstrated
<!--
  Only PBIs that passed the DoD gate are demonstrated (the Increment). Undone work
  is not shown. Present in value-first order (the outcome, then detail).
-->
- PBI-NNN: <title> (outcome: <one-line outcome delivered>)
- PBI-NNN: <title> (outcome: <one-line outcome delivered>)

## Evidence
<!--
  Per PBI, the evidence the stakeholder asked for in team.md > Review evidence:
  runnable result, test output, screenshots, command output, or walkthrough. Where
  possible the stakeholder drives the running product rather than watching a
  presentation (the Review is a hands-on working session, not a slideshow).
-->
### PBI-NNN
- Runnable result: <how to run it, or the link/path the stakeholder drove>
- Test output: <summary or path>
- Screenshots / artifacts: <paths>

<!-- Repeat one block per demonstrated PBI. -->

## Stakeholder feedback
<!--
  What the stakeholder said and did with the Increment. Real engagement, not
  "presented, no comment" (health checks S1.6, S1.10). Capture requests and
  reactions in their words.
-->
- <feedback item>
- <feedback item>

## Decisions
- Acceptance: <which PBIs the stakeholder accepts; any rejected and why>
- Release decision (PO): <release now | defer, with reason>
- Product Goal still valid: <yes | revise; note change in product-goal.md>

## Backlog changes
<!-- Feedback adapts the Product Backlog. Record new, reordered, and dropped items. -->
- New items: <PBI ids added>
- Reordered: <what moved and why>
- Dropped: <PBI ids dropped and why>

## Metrics update
<!--
  Append a row to .scrum/metrics.md for this Sprint. There is no separate metrics
  template; use this shape so the health check (core/anti-patterns.md) can read it.
  Cover all four families: responsiveness, quality, improving, value.
-->
```markdown
## sprint-NNN (YYYY-MM-DD)
- Throughput: <PBIs done>
- DoD pass rate: <passed / attempted>  |  Rework count: <n>
- Cycle time: <arrival-to-release, if tracked>
- Escaped defects: <found after "done">
- Value note: <outcome/satisfaction signal, not just output>
```
