# Sprint Review

## Purpose

The Sprint Review examines what the Sprint produced and decides what to adapt next. The
team presents its results to the stakeholder and discusses progress toward the Product
Goal. It runs as a working session, not a one-way presentation.

## Participants

- **Human stakeholder** is the audience and the customer. The Review exists to gather the
  stakeholder's feedback. This is the main point at which the human joins the team.
- **Product Owner (PO)** runs the Review, presents progress toward the Product Goal, and
  captures feedback into the Product Backlog. The Review is the PO's most valuable event.
- **Developers** demonstrate the Increment and answer questions about what was built.
- **Scrum Master (SM)** facilitates and keeps the session a two-way working session, not a
  one-way demo.
- **Orchestrator** assembles the evidence and records the outputs.

## Inputs

- The **Increment**: the set of PBIs that passed the Definition of Done gate this Sprint.
  Only gated work is demonstrated. Scout items are not part of the Increment and are not
  demonstrated; their findings are reported at the Review as learning that shaped or will
  shape the backlog.
- `sprints/sprint-NNN/sprint.md`: the Sprint Goal and the task log, to report what was and
  was not achieved.
- `product/product-goal.md` and `product/backlog.md`: to frame progress and to receive
  feedback.
- `.scrum/DEFINITION_OF_DONE.md`: the standard that decided what counts as done.
- Evidence gathered during execution: runnable results, test and analysis output,
  changed paths, threat and assurance records, and design evidence recorded in
  each PBI's "DoD evidence" field. Use screenshots only when they materially show
  visual or interaction evidence.

## AI-adapted procedure

**Adaptation: the stakeholder demo with evidence.** The Sprint Review is where the AI
team meets its human. It demonstrates real, verifiable output, never a claim. For each
Increment the team shows evidence a skeptical stakeholder can check: the app running, the
test suite output, a screenshot of the working behavior, or a diff of the changed files.
The intent, inspect the real outcome and adapt from it, is preserved by grounding the demo
in gated evidence rather than in assertions.

Run the Review in this order:

1. **Restate the Sprint Goal** and report honestly whether it was met. State what was
   completed and what was not.
2. **Demonstrate each Increment with evidence.** For each PBI that passed the gate, show
   the working behavior and the evidence behind it. Use the PBI's acceptance criteria as
   the demo script: show that each observable behavior holds. Prefer a runnable
   demonstration over a description.
   For security-triggered work, show mitigation closure, assumptions, and the
   residual-risk owner. For design-triggered work, compare the implemented
   experience with the accepted Design Brief or fallback intent.
3. **Show only Done work.** Items that did not meet the Definition of Done are not
   demonstrated as if complete. Name them, return them to the Product Backlog, and estimate
   the remaining work. Presenting undone work as done breaks transparency and trust.
4. **Discuss progress toward the Product Goal.** Set the Sprint's result against the
   Product Goal and the market or usage context the stakeholder brings.
5. **Gather feedback and adapt the backlog.** Capture the stakeholder's reactions,
   requests, and changes of direction directly into `product/backlog.md` as new or
   reordered PBIs. The backlog may be reordered on the spot; that is the Review doing its
   job.
6. **Record value signals.** Note the value measures the PO tracks (current value,
   unrealized value, time-to-market, and ability-to-innovate) into `metrics.md`, so trends
   are visible across Sprints.
7. **Audit the review artifact.** Apply `core/artifact-writing-standard.md` before
   saving it. Lead with the outcome, keep claims next to evidence, distinguish
   observed results from inference, and remove filler and private paths.

Decision rules for the Review:

- **The Review is not a release gate.** Items that meet the Definition of Done may be
  released at any time during the Sprint. The Review inspects the product and adapts
  the backlog; it does not authorize release.
- **Do not insert a gap after the Review.** If the stakeholder wants to react to feedback
  faster, shorten the Sprint timeboxes and fold the feedback into the backlog. A new
  Sprint starts immediately; there is no waiting period between Sprints.
- **A missed Review is a transparency loss.** If the stakeholder cannot attend, the team
  loses the feedback that adapts the product and risks drifting out of touch. Reschedule
  rather than skip, and make the evidence available for asynchronous review.
- **The whole team owns the Increment at the Review**, not one agent. The demonstration
  reflects integrated work, not separate branches shown in isolation.

## Outputs (`.scrum/` file changes)

- `sprints/sprint-NNN/review.md`: the evidence demonstrated, the stakeholder feedback, and
  the decisions taken.
- `product/backlog.md`: new PBIs from feedback added, existing items reordered, the Product
  Goal adjusted if the stakeholder redirected it.
- `metrics.md`: this Sprint's throughput, DoD pass rate, escaped defects, and value signals
  appended.
- `state.md`: `Stage` set to `6 RETRO`, `Updated` set.

## SM facilitation notes

- **Keep it a working session, not a presentation.** Draw the stakeholder into the
  Increment: let them try it, question it, and react. A one-way demo wastes the event.
- **Insist on evidence, refuse claims.** If a Developer presents an item as done with no
  runnable evidence, it does not go in the demo. Route it back through the DoD gate.
- **Protect honesty about undone work.** Coach the team to show the real state, including
  what was not finished. Hiding undone work to look complete is the failure the Review
  exists to prevent.
- **Turn feedback into ordered backlog items,** not a loose wish list. Every reaction the
  stakeholder gives should land as a PBI the PO can order.
- **Restore transparency when stakeholders are surprised.** If the stakeholder is surprised
  by cost, scope, or progress, that is a transparency failure to repair now and to raise at
  the Retrospective.

## Timebox

The Scrum Guide (2020) bounds the Sprint Review at a maximum of four hours for a one-month
Sprint, and proportionally shorter for a shorter Sprint.

**Adaptation.** For a Sprint of hours the Review is a short session proportional to the
Sprint, long enough to demonstrate the Increment with evidence and to capture feedback into
the backlog. The purpose and the working-session character are unchanged; only the duration
scales down with the Sprint length.
