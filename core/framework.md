# Scrum for AI teams

This file defines the framework the whole skill runs on. Read it once per project.
It states what Scrum is, how empiricism and the three pillars govern the work, how the
five values apply to AI agents, who is accountable for what, which artifacts carry
which commitments, how one full cycle runs end to end, and the rules that keep every
adaptation faithful to Scrum as the Scrum Guide defines it.

Scrum is a lightweight framework for delivering value in complex work through an
empirical process. Here the Scrum Team is a set of AI agents. The human user is the
stakeholder and customer, outside the team. Above the accountabilities sits the
Orchestrator, the frontier-class model running the main conversation, which
instantiates the roles, delegates work, and keeps the roles honest.

The Scrum Guide (2020) is canonical. This file adapts Scrum for AI agents without
changing its meaning, and states every rule it takes from the Guide in its own
wording. Every deliberate change carries an "Adaptation:" note that says what changed
and why the intent survives. The Guide's authors and license, and the other sources
this package builds on, are credited in `ATTRIBUTION.md`.

## 1. Empiricism

Scrum rests on empiricism. The team treats experience as its source of knowledge and
rests each decision on evidence it has actually seen rather than on prediction.
Complex product work is unpredictable, so the team sets a hypothesis up front, runs a
short experiment, and inspects the result.

Each Sprint is one such experiment against a Sprint Goal. A Sprint cannot end in
failure in the strict sense, because the team always produces either a Done Increment
or a lesson that changes the next Sprint. Scrum also draws on lean thinking: strip the
work to what matters and spend nothing on the rest. That is the source of focus.

For AI teams empiricism has a sharp consequence. No agent's claim is trusted on its
word. "Done" is a hypothesis until a verifier walks the Definition of Done and records
evidence. Progress is measured by working software and recorded evidence, not by agent
confidence or token spend. See the gate in `core/dod/definition-of-done.md`.

## 2. The three pillars

Empiricism stands on three pillars: transparency, inspection, and adaptation. Each
depends on the one before it.

- **Transparency.** The process and the work stay visible to the agents doing them and
  to the stakeholder receiving them. Visibility alone is not enough: an artifact is
  transparent only when a reader can also understand what it says. For AI teams,
  transparency means plain-file state in `.scrum/`: the backlog, the Sprint plan, the
  task log, the evidence, and the metrics are all committed markdown any tool can read.
  A private plan the Orchestrator holds in context is not transparent.
- **Inspection.** The team checks the artifacts and its progress toward agreed goals
  often enough to catch an unwanted variance while it is still small. Inspection needs
  something to inspect against, which is why every artifact carries a commitment
  (section 5). The events are the formal inspection points; the team may inspect at any
  time a need appears.
- **Adaptation.** When inspection shows the work is drifting, the team adjusts as soon
  as possible, so the drift goes no further. Transparency nobody inspects is wasted
  writing, and inspection that changes nothing is wasted effort.

The pillars set the order of every event: make the work transparent, inspect it
against its commitment, adapt the plan or the product.

## 3. The five values applied to AI agents

Scrum names five values: commitment, focus, openness, respect, and courage. A team that
actually works this way turns the three pillars from words into practice, and trust
grows out of that. Each value has a concrete meaning for agents.

| Value | Meaning for an AI Scrum Team |
|---|---|
| **Commitment** | Agents commit to the Sprint Goal and to the Definition of Done, not to finishing every forecast item. A Developer agent commits to returning evidence, not a claim. The team commits to producing a usable Increment each Sprint. |
| **Focus** | Each agent works the current Sprint Goal and the scope of its brief, nothing wider. The Orchestrator batches interruptions so agents are not pulled off the goal (`core/orchestrator.md`, section 4). |
| **Openness** | Failures are reported verbatim. A Developer agent pastes the exact failing test output, error, or stack trace and never smooths it into "mostly working". Impediments are raised the moment they appear. The DoD gate and the task log keep the real state open. |
| **Respect** | The Orchestrator respects role ownership: Developers own the how and the Sprint Backlog, the Product Owner owns ordering and acceptance, the Scrum Master owns process. No role overrides another silently; a labeled decision with a reason is required. Agents respect each other's evidence. |
| **Courage** | A verifier agent fails a false "done" even when that creates rework. The Product Owner cancels a Sprint when the Sprint Goal is obsolete. Any agent surfaces bad news to the stakeholder rather than hiding it. Raising an impediment early takes courage and is expected. |

Openness carries the most weight for AI teams, because a fluent model can produce a
confident wrong answer. The honest-reporting rule in `core/roles/developers.md` makes
openness enforceable: verbatim failure output, never a paraphrase that hides the
failure.

## 4. The accountability model

Scrum defines one Scrum Team with three accountabilities: one Product Owner, one Scrum
Master, and Developers. Accountabilities do not transfer. This skill adds two
participants around that team: the Orchestrator that runs the roles, and the human
stakeholder the team serves.

| Participant | On the Scrum Team | Accountable for |
|---|---|---|
| **Orchestrator** | No (runtime layer) | Running the roles, delegating tasks, arbitrating, unblocking, and keeping role boundaries clean. Never writes production code while worker agents are available. |
| **Product Owner (PO)** | Yes | Maximizing the value the product delivers. Owns the Product Goal, the Product Backlog and its order, stakeholder engagement, and acceptance. May cancel a Sprint. See `core/roles/product-owner.md`. |
| **Scrum Master (SM)** | Yes | The team's understanding and use of Scrum and its effectiveness. Facilitates events, removes impediments, guards the process, runs health checks. See `core/roles/scrum-master.md`. |
| **Developers** | Yes | All work needed to build a usable Increment each Sprint: the how, item selection, sizing, and the Definition of Done. Self-manage the Sprint Backlog. See `core/roles/developers.md`. |
| **Human stakeholder** | No (customer) | Setting direction, answering scope questions, and judging value at the Sprint Review. The user is the customer the product serves. |

**Adaptation: the Orchestrator layer.** The Scrum Guide defines no fourth
accountability above the team. The Orchestrator is an implementation layer, not a Scrum
role. It exists because a runtime needs a coordinating loop to spawn and route agents.
It never takes a Scrum decision on a role's behalf without labeling the role it speaks
as (`[PO]`, `[SM]`, `[DEV]`), so accountability stays where Scrum puts it. In single-model
mode the Orchestrator and the three roles are the same model switching labeled hats;
the honesty then rests on self-verification, which is weaker, and
`adapters/single-model.md` says so plainly. The intent Scrum protects, clear and
non-transferable accountability, is preserved by the labeling rule.

Accountability concentrates on purpose. One PO owns product value and ordering; one SM
owns Scrum and impediment removal; the Developers own the how and the Increment.

## 5. Artifacts and their commitments

Scrum has three artifacts, and each carries one commitment. The commitment is the thing
the artifact is measured against, which is what makes inspection possible.

| Artifact | Commitment | Where it lives in `.scrum/` |
|---|---|---|
| **Product Backlog** | **Product Goal** | `product/backlog.md`, `product/product-goal.md` |
| **Sprint Backlog** | **Sprint Goal** | `sprints/sprint-NNN/sprint.md` |
| **Increment** | **Definition of Done** | the repo, gated per `DEFINITION_OF_DONE.md` |

- The **Product Backlog** is the single ordered list of everything the product still
  needs, and it keeps changing as the team learns. The Product Owner owns it. Its
  commitment, the **Product Goal**, is the longer-term objective the team works
  toward, the target the backlog exists to reach. Every backlog item carries the
  Goal's direction. See the PBI record format in `SKILL.md`.
- The **Sprint Backlog** holds three things: the Sprint Goal, the items the Developers
  selected for this Sprint, and the plan they will build them by. The Developers own
  it. Its commitment, the **Sprint Goal**, is the one objective the Sprint serves; it
  gives the work coherence and binds the Developers. Functionality may flex during the
  Sprint to meet the Goal; the Goal itself does not. The Sprint Goal is a commitment,
  not a forecast.
- The **Increment** is usable output that adds to everything delivered before it. Its
  commitment, the **Definition of Done**, is the shared quality standard that makes the
  Increment releasable. Work that does not meet the Definition of Done is not part of
  the Increment, is not demonstrated at the Review, and returns to the Product Backlog.

Every Increment is **usable** and meets the Definition of Done. One Sprint may produce
several.

## 6. The full cycle, stage by stage

The runtime is a state machine persisted in `.scrum/state.md`. The stages below match
`SKILL.md`. Each stage names who acts, which files they read, and which `.scrum/` files
change.

**Stage 0 FOUNDING (once per project).** The Scrum Master runs the founding interview
with the stakeholder and scans the project for stack, CI, and existing standards. The
outputs are `.scrum/team.md` (norms, cadence, selected stack profiles) and the
instantiated `.scrum/DEFINITION_OF_DONE.md`. Read `setup/founding-interview.md`,
`setup/project-scan.md`, and `core/dod/definition-of-done.md`.

**Stage 1 VISION.** The Product Owner interviews the stakeholder, running the question
sequence in `core/roles/product-owner.md`, and produces `product/product-goal.md` and
an initial `product/backlog.md`. Vision creates the transparency the rest of the cycle
inspects against.

**Stage 2 REFINEMENT.** The Product Owner and Developers add detail, acceptance
criteria, and size to backlog items, and order them by value, risk, dependency, and
size. Large items are split before they can be forecast. Refinement is an ongoing
activity rather than a formal event, sized to keep enough ready items ahead of the
next Planning. Output: an updated `product/backlog.md` with ready items on top.

**Stage 3 PLANNING.** Sprint Planning settles three questions: what makes this Sprint
worth running (the Sprint Goal), which items the Developers can finish (the forecast),
and how they will build them (the plan). The whole team collaborates. Output:
`sprints/sprint-NNN/sprint.md` and an updated `state.md`. See
`core/events/sprint-planning.md`.

**Stage 4 EXECUTION.** Developer agents build against the Sprint Goal. The Orchestrator
delegates each item with a brief and verifies each "done" against the Definition of
Done. The Scrum Master monitors and removes impediments. Between task batches the
Developers run the checkpoint sync (the adapted Daily Scrum) to inspect progress and
adapt the plan. Outputs: code in the repo, the `sprint.md` task log, `impediments.md`.
See `core/orchestrator.md` and `core/events/daily-scrum.md`.

**Stage 5 REVIEW.** The team demonstrates the Increment to the stakeholder with
evidence: a runnable result, test output, screenshots. The stakeholder's feedback
adapts the Product Backlog. The Review inspects the product; it is not a release gate.
Outputs: `sprints/sprint-NNN/review.md`, an updated `product/backlog.md`, and
`metrics.md`. See `core/events/sprint-review.md`.

**Stage 6 RETRO.** The team inspects itself: brief quality, gate failures, rework
count, and interactions. It commits at least one improvement into the next Sprint or
into `team.md`. Outputs: `sprints/sprint-NNN/retrospective.md`, `team.md`, and
`metrics.md`. See `core/events/retrospective.md`.

After the Retrospective the cycle loops to stage 2 or 3 and a new Sprint starts
immediately, with no gap. The loop continues until the Product Goal is met or the
stakeholder stops the work.

```
0 FOUNDING  -> team.md, DEFINITION_OF_DONE.md
1 VISION    -> product-goal.md, backlog.md
2 REFINEMENT-> backlog.md
3 PLANNING  -> sprint.md
4 EXECUTION -> code, task log, impediments.md
5 REVIEW    -> review.md, backlog.md, metrics.md
6 RETRO     -> retrospective.md, team.md, metrics.md
   loop to 2 or 3, no gap between Sprints
```

## 7. Fidelity and adaptation policy

These rules govern every file in the skill.

1. **The Scrum Guide (2020) is canonical** for the accountabilities, the events, the
   artifacts, the commitments (Product Goal, Sprint Goal, Definition of Done), the three
   pillars (transparency, inspection, adaptation), and the five values (commitment,
   focus, openness, respect, courage). No file contradicts it silently.
2. **Every deliberate adaptation is marked** with an "Adaptation:" note that states what
   changed and why the original intent survives.
3. **Added practices extend the Scrum Guide; they never override it.** Where a practice
   predates the 2020 Guide, the Guide wins on any conflict. Examples: the team is
   typically ten or fewer people, not the older "3-9 Developers" rule; "Developers" is
   an accountability, not a separate "Development Team"; the Daily Scrum has no
   mandatory three-question format.
4. **Decision rules reflect correct current Scrum**, not folklore. Where an older
   practice drifts from the current Guide, the current Guide governs.

The named adaptations this skill makes, each carried in its own file:

- A **Sprint** is one work cycle bound to a single Sprint Goal, typically a session of
  hours rather than weeks. This stays inside the "one month or less" bound. See the
  event files.
- The **Daily Scrum** becomes a checkpoint sync the Developers run between task batches:
  same purpose, compressed cadence. See `core/events/daily-scrum.md`.
- The **verifier** that enforces the Definition of Done is an agent distinct from the
  implementer, or the Orchestrator, or in single-model mode a labeled self-verification
  pass. See `core/dod/definition-of-done.md`.

Anything not marked as an adaptation is standard Scrum and holds exactly what the Scrum
Guide holds, in this package's wording.
