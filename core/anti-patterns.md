# Process-decay health checks

This file is the health-check system behind `/scrum health`. It restates the
symptoms of process decay as concrete, automated checks an AI-run Scrum process
can evaluate against its own plain-file state in `.scrum/` and its recent process
history. Read it before running a health check and at the Retrospective (stage
6), where its findings feed at least one improvement item.

## 1. What process decay is, and why an AI team is at risk

Process decay, also called cargo-cult Scrum, looks like Scrum from a distance and
produces none of the outcomes Scrum exists to create. A team runs every event and
keeps every artifact, yet delivers no frequent releasable Increment, gets no real
stakeholder involvement, holds no ownership, and shows no drive to improve. It
passes a checklist inspection of events and artifacts. On close inspection the
outcomes are missing.

An AI-run process is exposed to a specific form of this. A fluent model can
generate every artifact file, populate every field, and report every event as
done while none of it changes the product or reflects real work. The plain files
in `.scrum/` can look complete and still be theater. The checks below test for
real outcomes, not paperwork: real stakeholder feedback, a real releasable
Increment each Sprint, real improvements that change later behavior, and real
self-organization visible in the file traces.

The checks are grouped into four areas, one per outcome the process is supposed
to produce. Stakeholder value asks whether the team builds what is needed and
validates it with the person who needs it. Delivery flow asks whether a usable
Increment actually ships each Sprint. Improvement follow-through asks whether
inspection changes later behavior. Team autonomy asks whether the team owns its
own work and resolves its own impediments.

The four areas are connected. When Sprints stop producing a working Increment,
the feedback loop closes, validation is lost, Sprints feel like empty timeboxes,
the urge to improve fades, and self-organization erodes. Recovery in one area
supports the others. Decay in one accelerates the others.

## 2. How to run the health check

`/scrum health` runs standalone at any stage and is also read during the
Retrospective. Procedure:

1. Read the process state: `.scrum/product/product-goal.md`,
   `.scrum/product/backlog.md`, every `.scrum/sprints/sprint-NNN/sprint.md`,
   `review.md`, and `retrospective.md`, plus `.scrum/impediments.md`,
   `.scrum/metrics.md`, `.scrum/team.md`, and `.scrum/DEFINITION_OF_DONE.md`.
2. Evaluate each check in section 4 against that evidence. Each check is PASS,
   FAIL, or `n/a` (with a one-line reason). Cite the file and field that decided
   it, the same way the Definition of Done gate cites evidence.
3. Score each area 0 to 10 as `10 * passing / applicable`, excluding `n/a`
   checks from the denominator. Flag any area scoring 6 or lower on that scale.
4. Run the suspicious-signal checks in section 5. A "too good" metric is itself
   a finding.
5. Apply the decision rules in section 6, then report findings in the format of
   section 7 and recommend one recovery action per flagged area. Do not
   recommend more than one action per area at a time. Improve one thing at a
   time, small enough for a single Sprint.

Scoring needs at least one completed Sprint to be meaningful. On a project with
zero finished Sprints, report the founding and vision checks only (S1.1, S1.2,
S1.7, S1.11, S4.5, S4.8) and say the rest are pending first Sprint data.

## 3. Adaptation notes for AI teams

Some symptoms assume a co-located human team. Each adaptation below preserves the
symptom's intent and is applied inside the relevant checks.

- **Adaptation: stakeholder distance.** The distance measure counts the hops
  between builders and a real user. Here the human user is the stakeholder and
  sits one hop from the team by construction. The distance risk does not
  disappear; it moves. The failure mode is a stakeholder who never actually
  exercises the Increment, or a Review that is skipped or simulated. The distance
  checks (S1.6, S1.10) test for real hands-on engagement in `review.md`, not for
  hop count.
- **Adaptation: external memory.** A co-located team prizes a physical board and
  information radiators as external memory. Here the external memory is the
  `.scrum/` directory itself: committed, current, plain-file traces any tool can
  read. S4.8 checks that those traces are populated and current, not that a board
  exists.
- **Adaptation: skill redundancy and team composition.** The signs check skill
  coverage and the team's say in its own membership. Worker agents are fungible
  and re-spawned per task, so single-agent bottlenecks (S2.9) and composition
  votes (S4.3) map weakly. These are marked `n/a` for single-model runs and
  evaluated as "the Orchestrator can add or swap an agent for a needed skill" for
  multi-agent runs.
- **Adaptation: learning from outside.** S3.9 (engage sources outside the team)
  maps to the process consulting the grounding files, the engineering standards,
  and external documentation rather than answering from model memory alone.

## 4. The four areas as automated checks

Each check names its PASS assertion, the concrete `.scrum/` evidence that decides
it, and the recovery action to recommend on failure. The recovery actions are
plain, single-Sprint-sized moves, one per failing check.

### Area 1: Stakeholder value

This area inspects whether the team builds what is needed and validates it with
the person who needs it. Failure themes: no stated product purpose, unvalidated
assumptions about value, an order nobody can explain, distance between builders
and a real user, a Product Owner with no real mandate, and output measured in
place of value.

| ID | PASS assertion | How to evaluate against `.scrum/` | Recovery to recommend |
|---|---|---|---|
| S1.1 | The product has a stated purpose | `product/product-goal.md` contains a purpose line of the form "This product exists in order to..." and a "does not exist in order to" boundary | State the purpose and keep it visible in `product-goal.md`; trace who uses and benefits |
| S1.2 | Every backlog item records why it matters | Each PBI in `product/backlog.md` has a non-empty `Value` naming a stakeholder-facing outcome, not an internal task restated | Rewrite each item as a desired outcome: who benefits, what changes, why it matters |
| S1.3 | Each Sprint Goal states stakeholder value | Every `sprint.md` `Sprint Goal` names an outcome or hypothesis, not a list of tasks to finish | Rewrite the Sprint Goal as an outcome or hypothesis, not a task list |
| S1.4 | The backlog is bounded, not monotonically growing | `product/backlog.md` shows at least one `Status: dropped` item over history, and length is not strictly rising every Sprint | Cap the backlog length and drop stale items |
| S1.5 | Sprints test value hypotheses | `sprint.md` goals and `review.md` record what was validated or learned about value, not only what shipped | Frame each Sprint around a value hypothesis and test it hands-on at the Review |
| S1.6 | The stakeholder actively uses the Increment | `review.md` records the stakeholder exercising the increment (hands-on, questions, change requests), not "presented, no comment" every Sprint | Have the stakeholder drive the running product at the Review; observe real use |
| S1.7 | At least one real end user is identifiable | `team.md` or `product-goal.md` names a real user or user segment for the product | Trace who uses, benefits from, or pays for the product; name a real user |
| S1.8 | Value and outcome metrics are tracked, not only output | `metrics.md` records value notes (satisfaction, outcome, or value measures), not only throughput and DoD pass rate | Track outcome and value measures alongside throughput |
| S1.9 | Release and value are known to the PO | `review.md` records a PO release decision and a value note per Sprint | Record the release decision and a stakeholder-value note each Sprint |
| S1.10 | The stakeholder actually engages at Review | Across recent Sprints, `review.md` files show real stakeholder feedback, and Reviews are not skipped or self-answered (see Adaptation: stakeholder distance) | Run the Review as a hands-on working session; confirm real feedback |
| S1.11 | The order tells a value story | The `Order rationale` fields in `product/backlog.md` explain why each item precedes the ones below it, so the top of the list reads as a sequence of value ("first this, which makes that possible"), rather than each rationale restating the item | Rewrite the top rationales as one sequence: what value comes first and what it unlocks next |
| S1.12 | The stakeholder informs the order | `review.md` or the `Order rationale` fields record stakeholder input into priority after founding, which the PO role weighs when reordering; the PO still decides (S4.5), and an order set once and never revisited fails this check | Ask the stakeholder to rank the next few items at the Review; record what moved and why |
| S1.13 | Developers reach the stakeholder directly | `review.md` records Developer questions answered by the stakeholder, not every exchange routed through the PO role | Let Developers put their open questions to the stakeholder at the Review |
| S1.14 | Stale items are renewed or removed | No PBI sits at `Status: draft` unchanged across many Sprints; old items are refined, reordered, or moved to `Dropped items` with a reason | Read the oldest items each refinement; refine, reorder, or drop each one |

### Area 2: Delivery flow

This area inspects whether a usable Increment actually ships each Sprint.
Failure themes: not grasping how frequent release reduces risk, plan-driven
governance that details work far ahead of building it, unremoved release
impediments, verification pushed past the Sprint that produced the work, and
items too large to finish in one Sprint.

| ID | PASS assertion | How to evaluate against `.scrum/` | Recovery to recommend |
|---|---|---|---|
| S2.1 | A releasable Increment exists every Sprint | Every completed `sprints/sprint-NNN/` has at least one PBI at `Status: done` with filled `DoD evidence`, demonstrated in `review.md` | Commit to a releasable Increment every Sprint to surface what blocks it |
| S2.2 | Releasing needs few or no manual steps | `DEFINITION_OF_DONE.md` or `team.md` records automated build, test, and deploy commands, not a long manual checklist | Automate build, test, and deploy; remove manual release steps one at a time |
| S2.3 | Releases are frequent and small | `metrics.md` throughput shows steady per-Sprint delivery, not work batched and withheld across many Sprints | Release small and often; stop batching work across Sprints |
| S2.4 | The process can name the risk of not shipping faster | `product-goal.md` or `retrospective.md` records the risks that grow when delivery slows | Name the risks that grow when delivery slows; cost out the manual release steps |
| S2.5 | Cycle time is tracked and low or falling | `metrics.md` records cycle or lead time per Sprint and it is not trending up | Track cycle and lead time and drive them down |
| S2.6 | Forecast items are small enough to finish | `sprint.md` forecasts hold no `Size: L` item (L must be split before forecast), and carryover is low | Slice items smaller; split any L before forecast |
| S2.7 | Upcoming work is refined during the Sprint | `product/backlog.md` holds `Status: ready` items ahead of the next planning, refined during the current Sprint | Refine upcoming work during the current Sprint |
| S2.8 | The DoD covers everything needed to release | `DEFINITION_OF_DONE.md` includes tested, packaged, and documented, not only "code written" | Extend the DoD until the Increment is releasable: tested, packaged, documented |
| S2.9 | No single skill or dependency blocks release | Multi-agent: the Orchestrator can add or swap an agent for any needed skill. Single-model: `n/a` (see Adaptation) | Map needed skills; ensure any one can be re-spawned, no single bottleneck |
| S2.10 | Work in progress is limited | `sprint.md` task log shows few PBIs `in-progress` at once, not the whole forecast open in parallel | Limit work in progress; finish before starting |
| S2.11 | The Sprint Review is held, not cancelled | Every completed sprint dir contains a `review.md` with real feedback; none are missing or marked cancelled | Hold the Review every Sprint; never skip it |
| S2.12 | Detail matches nearness | `product/backlog.md` carries acceptance criteria and sizes on the items near the top and short `draft` descriptions further down, rather than full specification of work many Sprints away | Refine only the next items; leave distant work coarse until it approaches |
| S2.13 | Verification happens inside the Sprint that builds the work | `DoD evidence` for each `done` PBI comes from commands run in the Sprint that built it, and `reworked` tasks do not trace to testing postponed to a later Sprint | Verify each item in the Sprint that builds it; stop carrying testing forward |
| S2.14 | Escaped defects are fixed promptly | Defects the stakeholder found at a Review enter the next Sprint's backlog and reach `done`, rather than sliding Sprint after Sprint | Schedule each escaped defect into the next Sprint and close it there |
| S2.15 | Completion spreads across the Sprint | The `sprint.md` task log shows tasks reaching `done` at several checkpoints, not the whole forecast landing at the last one | Take the first item to `done` early; keep finishing work at every checkpoint |

### Area 3: Improvement follow-through

This area inspects whether inspection changes later behavior. Failure themes:
fear of mistakes, retrospectives with no tangible result, small comfortable
improvements chosen over the problem that matters, no self-critique of how the
team works, and no learning from outside the team.

| ID | PASS assertion | How to evaluate against `.scrum/` | Recovery to recommend |
|---|---|---|---|
| S3.1 | Each Retrospective produces a concrete improvement | Every `retrospective.md` records at least one improvement item, not "nothing to change" | Produce at least one concrete improvement each Retrospective |
| S3.2 | Improvement actions are specific and measured | Improvement items name an owner, a first step, and a success measure, not a vague intention | Reduce each improvement to a first step with an owner and a success measure |
| S3.3 | Metrics are inspected in Retrospectives | `retrospective.md` cites `metrics.md` figures as the basis for at least one finding | Inspect metrics in the Retrospective as the basis for a finding |
| S3.4 | All four metric families are tracked | `metrics.md` covers four families, not velocity alone: responsiveness (throughput, cycle or lead time), quality (DoD pass rate, escaped defects), improving (rework trend, improvement items landed), and value. The value family holds the PO's value measures from `core/roles/product-owner.md`: current value, unrealized value, time-to-market, ability-to-innovate | Track all four families, not velocity alone: responsiveness, quality, improving, and value |
| S3.5 | Improvement items from earlier Retros were acted on | Cross-Sprint: an improvement from Retro N appears as a later change in `team.md`, a `sprint.md` plan, or the DoD. Items that accumulate with no downstream trace fail this check | Confirm prior improvements changed later behavior; dig into why they stalled |
| S3.6 | Doubts and impediments are raised in-session | `impediments.md` and `retrospective.md` show concerns surfaced during the Sprint, not only after failure | Surface doubts and impediments in-session; ask questions that invite them |
| S3.7 | Successes are acknowledged | `retrospective.md` records what went well, not only defects | Acknowledge what went well; mark small successes such as each release |
| S3.8 | Improvements are owned by the team | Improvement items are assigned to a role on the team, not deferred to an outside party | Assign each improvement to a team role, not an outside party |
| S3.9 | The process learns from outside itself | Retros or briefs cite the grounding files, engineering standards, or external docs, not model memory alone (see Adaptation) | Consult grounding files, standards, and external docs, not model memory alone |
| S3.10 | Beliefs and rules are periodically challenged | At least occasionally a Retro questions a rule or the DoD itself (double-loop), not only tweaks practice | Periodically challenge a rule or the DoD itself, not only tweak practice |
| S3.11 | The Retrospective faces the largest problem | The Sprint's biggest failure or longest-running impediment appears in `retrospective.md`; a Retro that lists only small comfortable adjustments while a known problem stands unmentioned fails this check | Name the Sprint's largest problem first in the Retrospective, then the smaller ones |
| S3.12 | Uncertain work is attempted, not avoided | Forecasts and `decisions.md` show the team taking work whose outcome was uncertain, with the risk contained to one Sprint, rather than a run of Sprints holding only safe low-value items | Take the riskiest assumption early while its blast radius still fits one Sprint |
| S3.13 | Improvements sometimes remove work | Across recent Retros, at least one improvement removes a step, a rule, or an artifact rather than adding another one | Ask what to stop doing; drop one step that costs more than it returns |
| S3.14 | Working agreements change as the team learns | The `Working agreement` section of `team.md` is amended over time and the `Amendments log` records what changed and when, rather than standing untouched from founding | Amend the working agreement when practice changes; log the amendment |

### Area 4: Team autonomy

This area inspects whether the team owns its own work and resolves its own
impediments. Failure themes: too little autonomy, solutions copied wholesale,
one actor resolving every impediment, absent or imposed goals, decisions taken
by whoever is loudest rather than by the role that owns them, hidden work traces,
and blocking standardization.

| ID | PASS assertion | How to evaluate against `.scrum/` | Recovery to recommend |
|---|---|---|---|
| S4.1 | Each Sprint has a clear goal that aligns work | Every `sprint.md` has one `Sprint Goal` that the forecast items serve | Set one clear Sprint Goal that the forecast serves |
| S4.2 | The team can state how stakeholders benefit | The `Sprint Goal` ties to a stakeholder outcome, traceable to `product-goal.md` | Tie the Sprint Goal to a stakeholder benefit |
| S4.3 | The team has a say in its composition | Multi-agent: the Orchestrator, not an outside party, decides agent assignment. Single-model: `n/a` | Keep agent assignment with the Orchestrator; make outside constraints visible |
| S4.4 | The team can change its tools and workspace | `team.md` records that tool and process choices are the team's within the DoD floor, not blocked on outside approval | Make tool and process choices the team's within the DoD floor |
| S4.5 | The Product Owner holds a real mandate | `product/backlog.md` order and PBI acceptance are set by the PO role, not dictated item-by-item by the stakeholder | Give the PO a real mandate over order and acceptance |
| S4.6 | The team keeps one product focus at a time | State shows one active Product Goal and one active Sprint, not many parallel efforts | Keep one product focus at a time; limit parallel efforts |
| S4.7 | Skill redundancy buffers absence | Multi-agent: a needed skill can be re-spawned. Single-model: `n/a` (see Adaptation) | Ensure any needed skill can be re-spawned; no single point of failure |
| S4.8 | Work traces are visible as external memory | `.scrum/` files are populated and current: the task log, goal, and evidence match the work actually done, not stale or empty while work proceeds only in conversation | Keep `.scrum/` files current so work traces stay visible |
| S4.9 | The team develops local solutions | Decisions in `retrospective.md` and `team.md` are reasoned for this project, not a framework copied wholesale | Reason each decision for this project; do not copy a framework wholesale |
| S4.10 | The team resolves most of its own impediments | `impediments.md` shows most items resolved by the team through the escalation ladder; stakeholder escalation is the exception, reserved for scope, destructive actions, or an exhausted ladder | Let the team resolve its own impediments; reserve escalation for org-level blockers |
| S4.11 | Items are not stuck waiting on outside approval | No PBI or task sits blocked on the stakeholder for many checkpoints when the escalation ladder was available | Find the few essential rules; drop procedural approvals that only wait |
| S4.12 | Requests for help are explicit and answered | `impediments.md` entries name the blocker, the owner, and the resolution, not vague "blocked" with no ask | Make each request for help explicit: blocker, owner, and the ask |
| S4.13 | The Sprint Goal is set by the team | `sprint.md` records a Goal the PO and Developers set at Planning from stakeholder outcomes and constraints; a Goal that is a fixed item list handed in from outside fails this check | Set the Sprint Goal at Planning; turn stakeholder demands into an outcome the team commits to |
| S4.14 | Each decision sits with the role that owns it | Backlog order and PBI acceptance are recorded by the PO role, the plan and the forecast by the Developers in `sprint.md`, and DoD changes by the whole team; no record shows the stakeholder choosing the technical approach or Developers reordering the Product Backlog | Return each decision to its owning role and record who decided |
| S4.15 | Resolved impediments stay resolved | `impediments.md` shows closed entries not reappearing; the same blocker recurring across Sprints means the recorded resolution treated a symptom | Reopen the recurring impediment and address its cause before closing it again |
| S4.16 | Waiting on outside approval is counted | Each wait on the stakeholder in `impediments.md` records when it started and when it cleared, so the cost of low autonomy is visible rather than absorbed silently | Log every wait for approval with its duration; report the total at the Retrospective |

## 5. Suspicious-signal checks: when a perfect number is the finding

Process decay can produce metrics that look excellent. These inverse checks flag
a result that is too clean to be real. Each is a signal, not a verdict; on a hit,
recommend the spot-audit named, not an immediate failing grade.

| Signal | Why it is suspicious | Spot-audit to recommend |
|---|---|---|
| DoD gate pass rate 100% with zero rework across many Sprints | Real independent verification catches failures sometimes. A gate that never fails is likely rubber-stamping evidence, not walking it | Re-verify a sample of `done` PBIs against `DEFINITION_OF_DONE.md`; confirm each `DoD evidence` field holds real command output, not a claim |
| Every forecast item done, every Sprint, always | Suggests the forecast is padded low, not stretched toward a goal; the Sprint Goal is not driving scope | Compare forecast size to capacity; check that the Sprint Goal, not item count, framed planning |
| The same generic improvement appears in Retro after Retro | Retro theater: inspect-and-adapt is not happening | Trace whether prior improvement items changed later behavior (S3.5); if not, the Retro is not producing real change |
| Zero impediments ever logged | An openness failure, not a frictionless team. Real complex work meets obstacles | Check whether blockers appear in the task log or conversation but never reached `impediments.md` |
| Review feedback is always "looks great, no changes" | The stakeholder is not exercising the Increment, or it was not really demonstrated | Confirm `review.md` shows hands-on stakeholder engagement and real evidence, not a summary |
| Velocity rising and reported as the success measure | Efficiency mindset: output is high, outcome unknown (S1.8 and S3.4 fail together) | Confirm value and outcome metrics exist alongside throughput |
| `.scrum/` files complete but not matching the repo | The paperwork is generated, the work is not real (S4.8 fails) | Diff the claimed increment against the actual repo and test results |
| Every Retro improvement is a small comfort change while the Sprint's known problem goes unmentioned | The Retrospective is working around the issue that matters, which is an openness failure rather than a calm Sprint | Check whether the Sprint's largest impediment or failure appears anywhere in `retrospective.md` (S3.11) |
| The same impediment is closed, then logged again a Sprint later | The recorded resolution treated a symptom and the cause is still in place | Read the resolution text of each recurrence; confirm it names a cause, not a workaround (S4.15) |
| The backlog is fully specified far into the future | Detail written long before the work starts rests on assumptions later Sprints will invalidate; it signals planning ahead of learning | Compare detail depth against position in the order; confirm distant items are still coarse (S2.12) |

## 6. Decision rules

Applied after scoring.

| Condition | Interpretation | Action |
|---|---|---|
| Any area scores 6 or lower | That area shows process decay | Run that area's diagnostic; recommend one recovery action for it |
| S2.1 fails (no releasable Increment each Sprint) | The single essential rule is broken; the lever for all four areas is disabled | Prioritize shipping a releasable Increment and evolving the Definition of Done before other work |
| S1.8 fails but output metrics are tracked | Efficiency mindset: output high, outcomes unknown | Add outcome metrics alongside throughput |
| S3.1 or S3.5 fails | Retrospectives produce nothing or nothing that sticks | Make each improvement specific and measured; inspect metrics in Retros; verify prior items were acted on |
| Multiple areas flag at once | The areas are connected; symptoms reinforce each other | Start small on one improvement the team controls; do not attempt all at once |
| A recommended improvement is too large for one Sprint | It will stall and demotivate | Break it down to a first step that fits one Sprint |
| S4.15 fails: an impediment recurs after being closed | The earlier resolution addressed a symptom | Reopen it, treat the cause, and do not close it again on the same evidence |
| S3.11 fails while its area still scores above 6 | The Retrospective is improving comfortable things while a known problem stands | Put the Sprint's largest problem first on the next Retrospective agenda |
| The stakeholder asks to share the health report upward | The scores are a self-inspection aid for the team, not a performance measure | Report to the stakeholder plainly; never use area scores to compare or rank teams |

## 7. Reporting findings and feeding recovery

Report each health check as a short structured result, not prose padding:

```markdown
# Health check: sprint-NNN (YYYY-MM-DD)
- Area 1 Stakeholder value:          X/10  [OK | FLAG]
- Area 2 Delivery flow:              X/10  [OK | FLAG]
- Area 3 Improvement follow-through: X/10  [OK | FLAG]
- Area 4 Team autonomy:              X/10  [OK | FLAG]

## Failing checks
- S2.1 FAIL: sprint-003 shows no PBI at done with DoD evidence.
  Recommend: commit to a releasable Increment every Sprint.
- ...

## Suspicious signals
- DoD pass rate 100% over 5 Sprints with zero rework. Recommend spot-audit of done PBIs.

## Recommended actions (one per flagged area)
- Area 2: extend the Definition of Done to include the missing release steps.
```

Feeding recovery into the loop:

- At the Retrospective (`core/events/retrospective.md`), a flagged area supplies
  the improvement item. Turn the recommended action into a specific step with an
  owner and a success measure, sized for one Sprint, and record it in
  `sprints/sprint-NNN/retrospective.md`. Amend `team.md` if the change is a
  standing norm.
- A failing S2.1 is escalated at once, not deferred to the next Retrospective:
  the releasable-Increment rule is the lever for every other area.
- Re-run `/scrum health` a Sprint later to confirm the score moved. An
  improvement that does not move its check is not a real improvement (S3.5).

The templates that hold this evidence are `templates/retrospective.md` and the
per-Sprint files under `templates/sprint.md` and `templates/review.md`. The
metrics the checks read live in `.scrum/metrics.md`, appended at each Review and
Retrospective.
