# scrum: an AI-agnostic Scrum software organization

`scrum` is a reusable, project-agnostic skill that turns any capable AI coding
assistant into a full Scrum software organization. You are the stakeholder and
customer. AI agents fill the three Scrum accountabilities, Product Owner, Scrum
Master, and Developers, and build your product under a tiered, evidence-gated
Definition of Done. All state is plain markdown in your repo under `.scrum/`, so
any AI tool can resume any project. "Done" is a verification gate with recorded
evidence, never a self-reported checkbox.

## Works with any agent

The core is plain markdown with no vendor assumptions. Thin adapters map it onto
each runtime. Pick your row, follow the linked doc, and you are set. No runtime is
preferred; the table is alphabetical.

| Runtime | How the skill runs there | Follow |
|---|---|---|
| Chat model, no file access (any vendor) | Paste the bootstrap prompt or the core files. One model plays every role by switching labeled hats and keeps `.scrum/` state as chat blocks you save and paste back. | `adapters/bootstrap-prompt.md` or `adapters/generic.md` |
| Claude Code | Skill folder auto-discovered from `SKILL.md`. Orchestrator is the main loop; Developers are subagents with parallel fan-out where supported. | `SKILL.md` + `adapters/claude-code.md` |
| Cursor and other IDE agents | Add a rules-file include that loads `SKILL.md`. Background or parallel agents act as Developers where the IDE exposes them. | `adapters/generic.md`, or `adapters/openai.md` when a worker primitive exists |
| OpenAI Codex CLI | Add an `AGENTS.md` include that points at `SKILL.md`. Separate runs act as Developers; otherwise roles switch sequentially. | `adapters/openai.md` |
| Other terminal coding agents | Add an `AGENTS.md`-style include per the Codex pattern. | `adapters/openai.md` |

Because every project's state is plain markdown under `.scrum/`, a project
started under one runtime can be resumed by another.

## Quick start

1. Get the package. Clone or download this repository; its root is the `scrum`
   package (the folder that holds `SKILL.md`). Keep the folder name `scrum`, since
   every include path below (`scrum/SKILL.md`, `scrum/adapters/openai.md`) assumes
   it.

   ```bash
   # skill-folder runtime (auto-discovered): clone into the skill location
   git clone <repo-url> ~/.claude/skills/scrum
   # every other runtime: clone into the project root
   git clone <repo-url> <project>/scrum
   ```

2. Wire it into your runtime. The mechanism differs by runtime: a skill folder is
   auto-discovered from `SKILL.md` with no include line; a terminal or IDE agent
   gets one include line in `AGENTS.md` or a rules file; a chat-only model gets a
   pasted bootstrap prompt. Find your row in the support matrix above and follow
   the matching Setup subsection.
3. Start the work. Invocation also differs by runtime: type `/scrum start "your
   product idea"` where slash commands exist, ask in natural language to build,
   plan, or run a product as a software team, or paste the chat-only prompt to
   begin the founding interview.

The agent runs the founding interview once, then walks you from idea to a
reviewed increment. You answer questions about outcomes and priorities; the team
does the building. No docs to read first.

## Example

The fastest way to see what a session looks like is the illustrative walkthrough
in `examples/first-sprint/walkthrough.md`. It is a written-out session for a
small fictional project, not a transcript of a real one, and it runs from the
first invocation through founding, vision, planning, an execution loop that
includes a Definition of Done gate failure and the rework it forces, the Review,
and the Retrospective. The example state sits beside it in
`examples/first-sprint/scrum-state/` and mirrors what the tool writes to
`.scrum/` in a real project.

## Setup per runtime

Follow exactly one subsection. Each is self-contained.

### Claude Code

Install as a skill so Claude Code auto-discovers it from the `name` and
`description` frontmatter in `SKILL.md`:

- User-wide: copy the package to `~/.claude/skills/scrum/`.
- Single project: copy it to `<project>/.claude/skills/scrum/`.

Invoke it by asking to start, plan, run, review, or retro a product, or by typing
`/scrum <idea>`. Claude Code maps the Orchestrator to the main loop and Developers
to subagents with parallel fan-out. Details in `adapters/claude-code.md`.

### OpenAI Codex CLI

Codex reads `AGENTS.md` from the project root. Copy the package to
`<project>/scrum/`, then add this include:

```markdown
# AGENTS.md
## Scrum organization
When asked to build, plan, run, review, or retro a product as a software team,
follow scrum/SKILL.md. Read scrum/adapters/openai.md for the role mapping.
Load scrum/core files by progressive disclosure per the stage table in
scrum/SKILL.md. Keep all project state in .scrum/ as plain markdown and commit
it with each increment.
```

This is the same block `adapters/openai.md` carries; that file is the canonical
copy. Codex runs the roles as separate runs where the setup allows spawning them,
and by sequential role-switching otherwise. Details in `adapters/openai.md`.

### Cursor and other IDE agents

IDE agents read a rules file, for example `.cursor/rules/` or a project rules
file. Copy the package to `<project>/scrum/` and add this rule:

```markdown
When the user asks to build, plan, or run a product as a software team, load
scrum/SKILL.md and follow scrum/adapters/generic.md, unless the IDE exposes a
worker-agent primitive, in which case follow scrum/adapters/openai.md. All state
lives in .scrum/.
```

If the IDE can run background or parallel agents, treat them as Developers.
Otherwise use the single-model labeled-hat protocol.

### Any plain chat model

No filesystem or tool access is required. Open `adapters/bootstrap-prompt.md` and
paste the chat-only prompt, or open `adapters/generic.md` and follow the
single-model protocol directly: the model switches labeled hats (`[ORCH]`,
`[PO]`, `[SM]`, `[DEV]`, `[VERIFY]`) in one conversation and self-verifies the
Definition of Done. When the protocol asks for a file, paste it into the chat:

1. `core/framework.md` and `core/orchestrator.md` at the start.
2. The role file for the active hat (`core/roles/*.md`).
3. `core/dod/definition-of-done.md` before any DoD gate.
4. The event file before each event (`core/events/*.md`).

Keep the `.scrum/` state as fenced markdown blocks in the conversation and paste
them back on resume. Self-verification is weaker than an independent verifier;
`adapters/generic.md` states the limits and the mitigations.

## How it works

### The role model

```
                    ┌──────────────────────────┐
                    │  Human stakeholder (you)  │
                    └────────────┬─────────────┘
                                 │ vision, decisions, acceptance
                    ┌────────────▼─────────────┐
                    │       Orchestrator        │  frontier model, main loop
                    │  facilitate · delegate ·  │  never writes production code
                    │  arbitrate · unblock      │  while workers are available
                    └───┬──────────┬─────────┬──┘
            labels as   │          │         │   delegation briefs
              a role    │          │         │
                ┌───────▼──┐  ┌────▼─────┐  ┌▼───────────────┐
                │ Product  │  │  Scrum   │  │  Developers    │
                │  Owner   │  │  Master  │  │ (worker agents)│
                │ backlog, │  │ events,  │  │ implement,     │
                │ value,   │  │ impedi-  │  │ test, meet     │
                │ validate │  │ ments    │  │ the DoD        │
                └──────────┘  └──────────┘  └────────────────┘
```

- **You, the stakeholder**, supply vision, priorities, and acceptance. You never
  need to write specs; you answer questions about outcomes.
- **Orchestrator** runs the conversation, delegates work, and arbitrates. It
  labels every role it speaks as, and keeps Product Owner decisions (ordering,
  acceptance) separate from Scrum Master decisions (process). While worker agents
  are available it does not write production code.
- **Product Owner** owns the Product Goal and ordered Product Backlog, interviews
  you, and runs validation.
- **Scrum Master** facilitates the events, removes impediments, guards the
  process, and runs Scrum health checks.
- **Developers** are worker agents that implement, test, and satisfy the
  Definition of Done, self-managing the Sprint Backlog.

The three accountabilities and their playbooks live in `core/roles/`. The
Orchestrator protocol is in `core/orchestrator.md`.

### The lifecycle

```
/scrum start "an idea"
      │
0 FOUNDING ─▶ 1 VISION ─▶ 2 REFINEMENT ─▶ 3 PLANNING ─▶ 4 EXECUTION ─▶ 5 REVIEW ─▶ 6 RETRO
 team.md,     product-    acceptance      Sprint Goal,   Developers    demo with   inspect the
 DoD          goal,       criteria,       forecast,      build; SM     evidence;   AI team;
              backlog     right-size,     plan           monitor;      feedback    ≥1 improvement
                          order                          gate = DoD    to backlog  to next sprint
                                                                                        │
                          └──────────────── loop to 2 or 3 until the Product ◀──────────┘
                                            Goal is met or you stop
```

What happens at each stage:

- **0 FOUNDING** (once per project): the Scrum Master interviews you about goals,
  stack, cadence, and quality bar, then writes `.scrum/team.md` and instantiates
  the Definition of Done into `.scrum/DEFINITION_OF_DONE.md`.
- **1 VISION**: the Product Owner interviews you, drafts the Product Goal, and
  seeds the initial backlog.
- **2 REFINEMENT**: the Product Owner and Developers add acceptance criteria,
  right-size items, and order the backlog by value, risk, and dependency.
- **3 PLANNING**: the team sets the Sprint Goal (why), selects backlog items
  (what), and plans the work (how).
- **4 EXECUTION**: Developers build; the Scrum Master monitors and clears
  impediments; the Orchestrator delegates and runs the Definition of Done gate on
  every "done" claim.
- **5 REVIEW**: the increment is demonstrated to you with evidence, and your
  feedback flows into the backlog.
- **6 RETRO**: the team inspects itself and carries at least one improvement into
  the next sprint or into `team.md`.

Then the loop returns to refinement or planning until the Product Goal is met or
you stop. A "Sprint" here is one work cycle bound to a single Sprint Goal, usually
hours rather than weeks, inside the Scrum Guide's timebox of one month or less.

## Using it effectively

- **Answer the founding interview honestly.** It sets the quality bar and the
  Definition of Done for every later sprint. Overstating your test setup or CI
  makes the gate weaker, not the work faster. The same interview sets staffing and
  delivery: whether an optional senior Developer runs on the strongest model you
  have, and whether each increment lands as a commit, as a pull request on a
  branch, or as staged changes you commit yourself. (**Adaptation:** the senior
  Developer is a skill distribution inside the one Developers accountability,
  never a new role or title.)
- **Give the Product Owner outcomes, not specs.** Say what a user should be able
  to do and why it matters. The Product Owner turns outcomes into ordered backlog
  items with acceptance criteria; that is its job, not yours.
- **Trust the team by default; intervene on scope.** During execution the team
  interrupts you only for scope decisions, destructive actions, or a blocker it
  could not resolve. Answer those. Let the rest wait for the Sprint Review.
- **Read DoD evidence at review.** Each accepted item carries recorded evidence
  (command output, test summary, file paths) in its "DoD evidence" field. Skim it.
  Evidence is the point; a "done" with no evidence is not done.
- **Run `status` to orient**, `health` when momentum feels off or output rises
  while value stalls, and `dod` to see or re-instantiate the current gate.
- **Tune `.scrum/team.md` between sprints.** Retrospective items land there.
  Adjust cadence, norms, or the quality bar, and the next sprint follows the
  change.
- **When agents stall**, the Orchestrator climbs an escalation ladder (rebrief,
  fresh agent, split or pair, direct intervention, then ask you). If it reaches
  you, it presents batched options with a recommendation. Pick one.

## Command reference

Arguments follow `/scrum`. A bare `/scrum <free text idea>` behaves as `start`.

| Arg | Action |
|---|---|
| *(none)* or `status` | Read `.scrum/`, report state, continue at the current stage |
| `start <idea>` | Founding interview if needed, then vision and initial backlog |
| `refine` | Refine the backlog: acceptance criteria, right-sizing, ordering |
| `plan` | Sprint Planning: Why (Sprint Goal), What (items), How (plan) |
| `sprint` | Execute the planned sprint |
| `cancel` | Product Owner cancels the current sprint when its Goal is obsolete: unfinished items return to the backlog and a new sprint starts |
| `review` | Demonstrate the increment to you with evidence; feedback to backlog |
| `retro` | Inspect the process; carry at least one improvement forward |
| `health` | Scrum health check for process decay against `core/anti-patterns.md` |
| `dod` | Show or re-instantiate the project Definition of Done |

## Repository layout

```
scrum/
├── SKILL.md                  entry point and router (skill-folder runtimes)
├── README.md                 this file
├── CHANGELOG.md              version history
├── CONTRIBUTING.md           how to propose and test a change
├── ATTRIBUTION.md            sources this package builds on, and their licenses
├── adapters/
│   ├── claude-code.md        Orchestrator = main loop; Developers = subagents
│   ├── openai.md             Codex CLI via AGENTS.md; GPT via system prompt
│   ├── generic.md            single-model labeled-hat protocol
│   └── bootstrap-prompt.md   copy-paste prompts to boot any agent
├── core/
│   ├── framework.md          Scrum for AI teams: pillars, values, flow
│   ├── orchestrator.md       Orchestrator protocol and escalation ladder
│   ├── events/               sprint-planning, daily-scrum, sprint-review, retrospective
│   ├── roles/                product-owner, scrum-master, developers
│   ├── dod/                  definition-of-done, profiles
│   ├── engineering-standards.md
│   └── anti-patterns.md      process-decay symptoms as automated checks
├── examples/
│   └── first-sprint/         worked session: walkthrough.md + scrum-state/
├── setup/
│   ├── founding-interview.md interview that writes .scrum/team.md
│   └── project-scan.md       detect stack, CI, existing standards
└── templates/                instantiated into each project's .scrum/
```

## What gets written to your project

The skill writes only inside `.scrum/` in your repo. Nothing else is touched
except the source files a Developer edits under an explicit brief.

```
.scrum/
├── team.md                 founding answers, stack profiles, cadence, norms
├── state.md                current stage, sprint number, pointers
├── DEFINITION_OF_DONE.md   instantiated DoD (tiers + profiles + project rules)
├── product/
│   ├── product-goal.md
│   └── backlog.md          ordered PBIs: id, value, size, acceptance, status
├── sprints/sprint-NNN/
│   ├── sprint.md           goal, forecast, plan, task log
│   ├── review.md           evidence, stakeholder feedback
│   └── retrospective.md    findings, improvement items
├── decisions.md            team shared memory: decisions, interfaces, gotchas
├── impediments.md          open and closed impediments with owner
└── metrics.md              per-sprint throughput, DoD pass rate, value notes
```

Commit `.scrum/` to your repo. It is safe and useful to keep under version
control: it is plain markdown, it records why each decision was made, and it lets
anyone (or any tool) resume the project at the exact stage it paused. Because the
state is plain markdown with no vendor lock-in, you can switch runtimes mid-project.
Start under one tool, continue under another, and the new tool reads `state.md`
and picks up where the last left off.

By default the team commits `.scrum/` and each code increment for you, so the
history stays resumable. Start from a clean working tree so each commit captures
only the increment, not pre-existing uncommitted changes. To keep commits in your
own hands, set `Delivery mode: stage-only` in `.scrum/team.md` and the team stages
its changes and reports them for you to commit, or set `branch-pr` to get the work
on a branch as a pull request the team never merges without you.

## FAQ

**Does this work without subagent support?**
Yes. `adapters/generic.md` defines a single-model protocol where one model plays
every role by switching labeled hats and self-verifies the Definition of Done.
Self-verification is weaker than an independent verifier, and the adapter says so
and lists mitigations.

**Can I mix stronger and weaker models?**
Yes, and that is the intent. The Staffing section of `.scrum/team.md` assigns a
model tier per seat: the strongest model you have on orchestration, diagnosis, and
verification, and mid-tier worker models on implementation, where most of the
token volume goes and the brief already carries the thinking. You can also turn on
a senior Developer that takes the hardest task of each cycle on the strongest tier
(**Adaptation:** a skill distribution inside the one Developers accountability,
not a new role or title). The founding interview asks which tiers your runtime
actually offers; with a single tier, staffing is a no-op and nothing else changes.

**Can I use my existing backlog?**
Yes. Point the Product Owner at your existing items during vision or refinement.
It maps them into the fixed PBI record format (id, value, order rationale, size,
acceptance criteria, DoD evidence) in `.scrum/product/backlog.md` and orders them.

**Can I run this on an existing codebase?**
Yes. At founding the project scan detects your stack, build and test commands, CI
gates, and standards files, and maps the current modules, entry points, and
recorded `TODO`/`FIXME` work into candidate backlog items. Existing organizational
standards become a Tier 3 floor the team may strengthen but never weaken. Follow
the brownfield path in `setup/project-scan.md`.

**I have a monorepo with several products. How does state work?**
One `.scrum/` belongs to one product. Place a `.scrum/` in each product's
directory and run the skill from that directory, so each product keeps its own
state and backlog separate. Never share one backlog across unrelated products.

**How is this different from just prompting the agent?**
Roles are separated and labeled, so product decisions, process decisions, and
implementation do not blur. Every "done" passes an evidence gate a distinct
verifier checks. All state persists as plain files, so work survives across
sessions and tools. The result is criteria-driven and low-noise, not vibes.

**What if my runtime has no file access?**
Use the chat-only path in `adapters/bootstrap-prompt.md` or `adapters/generic.md`.
The model keeps each `.scrum/` file as a fenced markdown block in the conversation
and re-emits it on every change. You save the blocks and paste them back to resume.

**Can two different tools work the same project?**
Yes. All state is plain markdown under `.scrum/`. One tool can plan a sprint,
another can execute it, and a third can run the review, as long as each reads
`state.md` first. This is the reason to commit `.scrum/`.

**How do I uninstall or stop using it?**
Stop invoking `/scrum`. To remove the skill, delete the `scrum/` folder from your
skill or rules location. Your project's `.scrum/` directory is just markdown; keep
it as a record or delete it. Neither affects your source code.

**Is my source code sent anywhere?**
The skill itself makes no network calls and sends no source code. It runs inside
whatever agent you already use, subject to that agent's own data handling, and
reads and writes only files in your project. One exception is worth naming: the
Definition of Done gate has the agent run your stack's dependency-audit tool (for
example `npm audit`, `pip-audit`, `cargo audit`, or `govulncheck`), and those
tools may contact package-advisory databases with your dependency names and
versions. That is the audit tool's own behavior, not the skill's, and it still
sends no source code.

**What is a "Sprint" here, in wall-clock time?**
One work cycle bound to a single Sprint Goal, usually a session of hours rather
than weeks. This compresses the cadence while staying inside the Scrum Guide's
timebox of one month or less. The event files in `core/events/` mark each timing
adaptation.

## Attribution

The definition of Scrum this package follows is the Scrum Guide (2020) by Ken
Schwaber and Jeff Sutherland, published at https://scrumguides.org under the
Creative Commons Attribution-ShareAlike 4.0 International license (CC BY-SA 4.0);
the rules appear here in this package's own wording. `ATTRIBUTION.md` credits
that source and every other framework, standard, and body of practice the
package builds on.

## License

MIT. See `LICENSE`.
