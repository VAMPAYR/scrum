# Sprint Planning

## Purpose

Sprint Planning starts the Sprint by laying out the work the team will take on. The
whole Scrum Team collaborates to produce the plan. Planning settles three questions: the
value this Sprint should create, the amount of work the team can finish to the agreed
standard, and the approach it will take to build that work.

## Participants

- **Product Owner (PO)** proposes how the product could increase its value this Sprint,
  and brings the ordered, refined Product Backlog. Owns the What discussion.
- **Developers** select the items they forecast they can turn into a Done Increment and
  design the plan for building them. Own the How discussion and the forecast.
- **Scrum Master (SM)** facilitates, guards the timebox, and coaches the team to a
  Sprint Goal.
- **Orchestrator** runs the event and records the outputs. The human stakeholder is not
  required, but the PO carries the stakeholder's direction into the room.

## Inputs

- `product/backlog.md`: the ordered backlog with ready items on top, each carrying
  acceptance criteria and a size.
- `product/product-goal.md`: the Product Goal the Sprint must move toward.
- `.scrum/DEFINITION_OF_DONE.md`: the standard the forecast must be feasible against.
- `.scrum/metrics.md`: past throughput and DoD pass rate, used to gauge capacity.
- `core/engineering-standards.md` and `core/test-strategy.md`: the risk-driven
  loop and verification choices the plan must make explicit.
- Existing threat models, architecture records, Design Briefs, and design-system
  evidence relevant to the forecast. Read `core/threat-modeling.md` or
  `core/ux-integration.md` when its trigger applies.
- The previous Sprint's `review.md` feedback, folded into the backlog before planning.

## AI-adapted procedure

Work the three topics in order. Do not skip the Why; a forecast with no Sprint Goal is a
list of random tasks.

**Topic 1: Why (the Sprint Goal).** The PO states the value the Sprint should create.
The team crafts a single Sprint Goal, one objective that gives the Sprint focus and
binds the Developers. The Sprint Goal is a commitment, not a forecast. Functionality may
flex during the Sprint to meet the Goal; the Goal does not change. Write the Sprint Goal
at the top of `sprint.md` before selecting any item.

**Topic 2: What (the forecast).** The Developers pull items from the top of the ordered
backlog that serve the Sprint Goal, and forecast the amount they can turn into a Done
Increment. The PO clarifies items and can trade scope, but the Developers own the
selection. Feasibility is judged against the Definition of Done: an Increment is usable
only when all its work meets the DoD, so the forecast is what the team can make Done, not
what it can start.

Capacity and forecasting for AI teams:

- **Base the forecast on recorded throughput, not optimism.** Read `metrics.md` for the
  prior Sprint's completed PBIs and DoD pass rate. A team that passed the gate on three
  of five forecast items last Sprint should forecast with that pass rate in mind.
- **Size, do not schedule.** Items are sized XS, S, M, L. An L must be split before it
  can be forecast; it is too large to finish against one Sprint Goal. Prefer several
  small items that each reach Done over one large item that reaches Done at the buzzer.
- **Forecast the most likely amount when requirements are unclear.** If the Developers
  cannot confidently forecast a full Sprint Backlog but can craft a Sprint Goal, forecast
  the most likely amount and proceed. The Sprint Goal provides the coherence; unclear
  items are refined during the Sprint.
- **Turn an unknown too large to forecast into a scout item.** Where an item cannot be
  sized because the team does not yet know enough, forecast a scout in its place: a
  timeboxed investigation brief that returns a report answering named questions, with no
  production code (`core/orchestrator.md`, section 2). Size and forecast a scout like any
  other item, and feed its findings into refinement so the work it unblocks can be sized
  in the next cycle.
- **Account for verification cost.** Every forecast item carries a DoD gate run by a
  separate verifier. Budget that verification and any expected rework into capacity, not
  only the implementation.

**Topic 3: How (the plan).** The Developers break each forecast item into tasks and
decide the approach. For AI teams this plan is the delegation order: which items are
independent and can fan out to parallel agents, which are sequential, and which files
each touches. The plan does not have to be complete; the Developers refine it through the
Sprint. Record enough for the Orchestrator to write the first delegation briefs
(`core/orchestrator.md`, section 2).

For each forecast PBI, record the material risk and assumptions, threat-model
route, selected test methods and why they fit, UI/UX route, and whether a compact
assurance case is required. TDD is preferred for deterministic behavior and
reproducible defects, but another method is required when it can test the claim
better. Also record required capabilities, the default or risk-adjusted mutating
attempt budget, evidence that would count as progress, stop conditions, a
recoverable baseline, and the capability-matched diagnostic route from
`core/stall-recovery.md`. Include verification, specialist review, diagnosis, and
likely rework in capacity rather than budgeting implementation alone.

The Sprint Goal, the forecast, and the plan together form the Sprint Backlog.

## Outputs (`.scrum/` file changes)

- `sprints/sprint-NNN/sprint.md`: created with the Sprint Goal, the forecast (the
  selected PBIs by id), and the initial plan and task-log skeleton including
  attempt and recovery fields.
- `product/backlog.md`: selected items marked `forecast`; any items split during planning
  are rewritten.
- `state.md`: `Stage` set to `4 EXECUTION`, `Sprint` incremented, `Active PBIs` listed,
  `Updated` set.

## SM facilitation notes

- **Do not let planning start without the ordered backlog.** If the PO wants to prepare
  or pre-own the Sprint Backlog before the event to make it "more effective", advise
  against it. The Sprint Backlog belongs to the Developers, and Sprint Planning is the
  whole team's collaborative work. Pre-owning it erodes Developer ownership.
- **Do not postpone planning to wait for feedback to reach the backlog.** If Review
  feedback is not yet in the Product Backlog, fold it in during the event. Adapting the
  backlog and making it transparent is part of Sprint Planning.
- **Push for one Sprint Goal, not a theme.** If the team cannot name a single objective,
  the selected items probably lack coherence. Coach the team to a goal that a stakeholder
  would recognize as valuable.
- **Guard the timebox** (see the Adaptation note below). Planning that runs long is
  usually planning that skipped refinement; note it for the Retrospective.
- **Keep the DoD in the room.** The DoD sets how much work each item needs to be Done and
  so what the team can honestly forecast.

## Timebox

The Scrum Guide (2020) bounds Sprint Planning at a maximum of eight hours for a one-month
Sprint, and proportionally shorter for a shorter Sprint.

**Adaptation.** A Sprint here is one work cycle of hours, not weeks, so Sprint Planning
is a short session measured in minutes, proportional to the Sprint length. The three
topics and their order are unchanged: the compressed cadence preserves the intent that
the team enters the Sprint with a valuable purpose, a feasible forecast, and a shared
plan. Scale the planning session down with the Sprint, never drop a topic.
