---
name: scrum
description: Run a full Scrum software organization on any project with AI agents filling Product Owner, Scrum Master, and Developer accountabilities, a tiered evidence-gated Definition of Done, and plain-file state any AI tool can resume. Use when the user wants to start, plan, run, review, or retro a product or sprint, says "/scrum", "product backlog", "sprint planning", "definition of done", or asks to build something as a real software team would.
---

# Scrum: an AI software organization

This skill turns the assistant into a Scrum software organization that builds
the user's product. The human user is the stakeholder and customer. AI agents
fill the three Scrum accountabilities, and one frontier-class model runs the
whole thing as Orchestrator.

- **Orchestrator**: the main conversation. Facilitates, delegates, arbitrates,
  and unblocks. Speaks as each role only with an explicit label.
- **Product Owner (PO)**: owns the Product Goal, Product Backlog, ordering by
  value, and validation. Interviews the stakeholder.
- **Scrum Master (SM)**: facilitates events, removes impediments, guards the
  process, runs health checks.
- **Developers**: worker agents that implement, test, and meet the Definition
  of Done. They self-manage the Sprint Backlog.

Read `core/framework.md` once per project for the values, the three pillars
(transparency, inspection, adaptation), and the flow. Read `core/orchestrator.md`
before delegating any work.

## The no-coding rule (read first)

While worker agents are available, the Orchestrator does not write or edit
production code. It writes Scrum artifacts, delegation briefs, and arbitration
decisions. Code is produced by Developer agents and verified by an agent
distinct from the implementer. The single exception is escalation rung (d) in
`core/orchestrator.md`, logged in the sprint file when used.

If the runtime has no worker-agent or subagent primitive, the model still keeps
the roles separate by switching labeled hats. See `adapters/generic.md`. In that
mode the no-coding rule relaxes because there is one model; role labels and
self-verification hold the discipline instead.

## First action every invocation: detect state

State lives in the target project's repo at `.scrum/state.md`. Plain markdown,
committed to the repo, so any AI tool resumes any project.

One `.scrum/` belongs to one product. In a monorepo, place a `.scrum/` in each
product's directory and run the skill from that directory, keeping each product's
state and backlog separate. Never share one backlog across unrelated products.

1. Read `.scrum/state.md`.
2. If it does not exist, the project is new. Bootstrap it (below) and route to
   stage 0 FOUNDING regardless of the argument.
3. If it exists, read the `Format` field, the `Stage` field, and the pointers.
   If `Format` is absent or higher than this skill version supports, the state was
   written under a different `.scrum/` layout: stop and report the mismatch rather
   than misread it, and migrate the file to the current shape before continuing.
   Otherwise route the subcommand against the current stage.

Never guess the stage. Read the file. If `.scrum/` is present but `state.md` is
missing or unreadable, reconstruct the stage from what exists (`team.md` implies
founding done; `product/product-goal.md` implies vision done; a
`sprints/sprint-NNN/` with an unfinished task log implies execution) and rewrite
`state.md` to match.

### Bootstrapping `.scrum/state.md`

Create the directory and file with this exact shape. Most other state files have
a template in `templates/`; `state.md` is defined here, and the `impediments.md`
and `metrics.md` shapes are defined inline (impediments in the impediment protocol
of `core/roles/scrum-master.md`; metrics in the fenced blocks of
`templates/review.md` and `templates/retrospective.md`).

```markdown
# Scrum State
- Format: 1
- Stage: 0 FOUNDING
- Sprint: 000
- Product Goal: not set
- Active PBIs: none
- Adapter: <claude-code | openai | generic>
- Updated: <YYYY-MM-DD>
```

`Format` marks the `.scrum/` layout version. It stays constant across a project's
life and changes only when a migration rewrites the layout.

Set `Adapter` by detecting the runtime (subagent primitive available →
`claude-code`; Codex CLI or GPT → `openai`; single chat model → `generic`).
Update `Stage`, `Sprint`, `Product Goal`, `Active PBIs`, and `Updated` at every
stage transition. How `.scrum/` and the code increment land is set by the
Delivery mode in `.scrum/team.md`: `commit` (default) commits them together;
`branch-pr` keeps the work on a branch and delivers a pull request, never merged
without the stakeholder; `stage-only` stages the changes and reports them for the
stakeholder to commit. Start from a clean working tree in every mode, so a commit
or a delivered diff carries only the increment, not pre-existing uncommitted
changes.

### Crash recovery

If a run was interrupted mid-EXECUTION, reconstruct the Sprint from the task log
before delegating new work (`templates/sprint.md`), as the rules above reconstruct
a stage from what exists.

- A task left `in-progress` or `in-review` is re-briefed and resumed, not assumed
  finished (`core/orchestrator.md`, rung (a)).
- A `done` claim with no recorded evidence (Definition of Done evidence for build
  tasks; answered-questions evidence for scout tasks) is treated as not done and
  re-verified from scratch: a build task against `.scrum/DEFINITION_OF_DONE.md`, a
  scout against the questions its brief named (`core/orchestrator.md`, section 2).
- A half-applied change is diffed against the task's files in scope before work
  continues, so out-of-scope edits are caught before they compound.
- Note the recovery in `sprint.md`: the interrupted task, what was re-verified,
  and what was discarded, so the Retrospective can inspect it.

## Subcommand router

Arguments follow `/scrum`. A bare `/scrum <free text idea>` behaves as `start`.

| Arg | Action | Stage |
|---|---|---|
| *(none)* or `status` | Read `.scrum/`, report state, continue at current stage | current |
| `start <idea>` | Founding interview if needed, then vision and initial backlog | 0 → 1 |
| `refine` | Refine backlog: acceptance criteria, right-sizing, ordering | 2 |
| `plan` | Sprint Planning: Why, What, How | 3 |
| `sprint` | Execute the planned sprint | 4 |
| `cancel` | `[PO]` cancels the Sprint when its Goal is obsolete; return unfinished PBIs to the backlog and start a new Sprint | 4 → 3 |
| `review` | Demo the increment to the stakeholder with evidence | 5 |
| `retro` | Inspect the process; carry at least one improvement forward | 6 |
| `health` | Scrum health check for process decay against `core/anti-patterns.md` | any |
| `dod` | Show or re-instantiate the project Definition of Done | any |

Routing rules:

- If the requested stage is ahead of the current stage, run the missing stages
  first or tell the stakeholder what is missing and offer to run it. Do not
  skip founding, vision, or planning.
- `status`, `health`, and `dod` are read-mostly and run at any stage.
- `cancel` is a Product Owner action, valid during EXECUTION (stage 4) when the
  Sprint Goal is obsolete. Return every unfinished PBI to `product/backlog.md`,
  record the cancellation reason in `sprints/sprint-NNN/sprint.md`, set `state.md`
  Stage to `3 PLANNING`, and begin a new Sprint immediately. Only the `[PO]` may
  cancel a Sprint (`core/roles/product-owner.md`).
- After any stage completes, write the new stage to `state.md`.

## Progressive disclosure: what to read per stage

SKILL.md loads nothing by default beyond itself. At each stage, read only the
files that stage needs. Paths are relative to the `scrum/` package root.

| Stage | Read these files | Writes into `.scrum/` |
|---|---|---|
| 0 FOUNDING | `setup/project-scan.md`, `setup/founding-interview.md`, `core/roles/scrum-master.md`, `core/dod/definition-of-done.md`, `core/dod/profiles.md`, templates `templates/team.md` `templates/definition-of-done.md` | `state.md`, `team.md`, `DEFINITION_OF_DONE.md` |
| 1 VISION | `core/roles/product-owner.md`, `templates/product-goal.md`, `templates/product-backlog.md` | `product/product-goal.md`, `product/backlog.md`, `state.md` |
| 2 REFINEMENT | `core/roles/product-owner.md`, `core/roles/developers.md` | `product/backlog.md`, `state.md` |
| 3 PLANNING | `core/events/sprint-planning.md`, `core/roles/product-owner.md`, `core/roles/developers.md`, `templates/sprint.md` | `sprints/sprint-NNN/sprint.md`, `state.md` |
| 4 EXECUTION | `core/orchestrator.md`, `core/roles/developers.md`, `core/events/daily-scrum.md`, `core/dod/definition-of-done.md`, `core/engineering-standards.md`, `templates/decisions.md`, `.scrum/decisions.md` (into every brief) | `sprint.md` task log, `decisions.md`, `impediments.md`, `state.md`, code in the repo |
| 5 REVIEW | `core/events/sprint-review.md`, `core/roles/product-owner.md`, `templates/review.md` | `sprints/sprint-NNN/review.md`, `product/backlog.md`, `metrics.md`, `state.md` |
| 6 RETRO | `core/events/retrospective.md`, `core/anti-patterns.md`, `core/roles/scrum-master.md`, `templates/retrospective.md` | `sprints/sprint-NNN/retrospective.md`, `team.md`, `decisions.md` (pruned), `metrics.md`, `state.md` |
| `health` | `core/anti-patterns.md` | findings reported; `metrics.md` if run in a sprint |
| `dod` | `core/dod/definition-of-done.md`, `core/dod/profiles.md` | `DEFINITION_OF_DONE.md` |

Read the role file before speaking as that role. Read the event file before
facilitating that event. Read `core/dod/definition-of-done.md` before any DoD
gate.

## The loop

```
0 FOUNDING    founding interview (once) ......... team.md, DEFINITION_OF_DONE.md
1 VISION      PO interviews stakeholder ......... product-goal.md, backlog.md
2 REFINEMENT  PO + Developers refine backlog .... backlog.md
3 PLANNING    Why / What / How .................. sprint.md
4 EXECUTION   Developers build; SM monitors ..... code, task log, impediments
5 REVIEW      demo increment with evidence ...... review.md, backlog.md
6 RETRO       inspect the AI team ............... retrospective.md, team.md
                 └── loop to 2 or 3 until the Product Goal is met or the
                     stakeholder stops
```

A "Sprint" here is one work cycle bound to a single Sprint Goal, typically a
session of hours rather than weeks. This stays inside the Scrum Guide (2020)
timebox of one month or less. See the adaptation notes in `core/events/`.

## The Definition of Done gate

`done` is never self-reported. A PBI reaches `done` only when a verifier (an
agent distinct from the implementer, or the Orchestrator, or in single-model
mode a labeled self-verification pass) walks the instantiated
`.scrum/DEFINITION_OF_DONE.md` and records evidence per item into the PBI's
"DoD evidence" field. Unverifiable items are marked `n/a` with a reason, never
silently skipped. The increment is the set of PBIs that passed the gate. Only
those are demonstrated at Sprint Review. Full protocol in
`core/dod/definition-of-done.md`.

## PBI record format (fixed)

Every Product Backlog Item in `product/backlog.md` uses this shape:

```markdown
### PBI-042: <title>
- Status: draft | ready | forecast | in-progress | done | dropped
- Value: <stakeholder-facing outcome, one sentence>
- Order rationale: <why it sits here in the backlog>
- Size: XS | S | M | L (L must be split before forecast)
- Acceptance criteria:
  - [ ] <observable behavior>
- DoD evidence: <links/paths filled at completion>
```

## Choose the adapter

Read the adapter that matches the runtime, then map the roles onto its
primitives:

- `adapters/claude-code.md`: Orchestrator is the main loop; Developers are
  subagents with parallel fan-out where supported. Install path
  `~/.claude/skills/scrum/` or project `.claude/skills/scrum/`.
- `adapters/openai.md`: Codex CLI via `AGENTS.md`; GPT and Assistants via
  system-prompt composition.
- `adapters/generic.md`: single model switching labeled hats
  (`[ORCH]`, `[PO]`, `[SM]`, `[DEV]`, `[VERIFY]`) with self-verification.

Installation for every environment is in `README.md`.

## State files in the target project

```
.scrum/
├── team.md                 founding answers, stack profiles, cadence, norms
├── state.md                current stage, sprint number, pointers
├── DEFINITION_OF_DONE.md   instantiated DoD (tiers + profiles + project rules)
├── product/
│   ├── product-goal.md
│   └── backlog.md          ordered PBIs
├── sprints/sprint-NNN/
│   ├── sprint.md           goal, forecast, plan, task log
│   ├── review.md           evidence, stakeholder feedback
│   └── retrospective.md    findings, improvement items
├── decisions.md            team shared memory: decisions, interfaces, gotchas
├── impediments.md          open/closed impediments with owner
└── metrics.md              per-sprint throughput, DoD pass rate, value notes
```

Templates in `templates/` define most of these formats exactly; the
`impediments.md` and `metrics.md` shapes are defined inline (see the impediment
protocol in `core/roles/scrum-master.md` and the metrics blocks in
`templates/review.md` and `templates/retrospective.md`). Keep everything in plain
markdown so any runtime, including a plain chat model, can resume the same
project.

## Fidelity

The Scrum Guide (2020) is canonical for accountabilities, events, artifacts,
commitments, the three pillars, and the values. Never contradict it silently.
Every deliberate adaptation for AI teams carries an "Adaptation:" note. The
extended practices strengthen the framework and never override it. Define any
Scrum term on first use.
