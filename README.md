# scrum: an AI-agnostic Scrum software organization

`scrum` is a reusable, project-agnostic skill that turns any capable AI coding
assistant into a full Scrum software organization. You are the stakeholder and
customer. AI agents fill the three Scrum accountabilities, Product Owner, Scrum
Master, and Developers, and build your product under a tiered, evidence-gated
Definition of Done. All state is plain markdown in your repo under `.scrum/`, so
any AI tool can resume any project. "Done" is a verification gate with recorded
evidence, never a self-reported checkbox. Engineering is risk-driven and
AI-aware: the team selects TDD or another verification route to fit the claim,
threat-models consequential boundaries, treats generated work as untrusted, and
writes every artifact under a concise, evidence-calibrated prose standard.
The package keeps its full knowledge modules while a deterministic context router
activates only the verbatim sections needed for the current stage and triggers.

## Works with any runtime

The core is plain markdown with no vendor assumptions. Thin adapters map it onto
each runtime. Adapters are named for runtime capability, never for a vendor, so
find the row that describes what your runtime can do, follow the linked files, and
you are set. No runtime is preferred and none is a reference implementation.

| Runtime capability | Example runtimes | How the skill runs there | Follow |
|---|---|---|---|
| Spawns parallel worker agents and auto-discovers a skill folder from `SKILL.md` | Claude Code, Goose, or another harness that scans a skills directory and dispatches concurrent worker agents | Install into the skills directory the runtime scans; no include line. The Orchestrator is the main loop, Developers are worker agents with parallel fan-out, and a distinct agent runs the verification gate. | `SKILL.md` + `adapters/parallel-agents.md` |
| Reads an `AGENTS.md` or a rules file and can start separate runs or background agents | Cline, Codex CLI, Cursor, or a Kimi or Llama-based terminal agent | Point the file your agent reads at the package with one include line. Separate runs or background agents act as Developers; where none can start, the roles switch sequentially in one session. | `AGENTS.md` + `adapters/terminal-agent.md` |
| Runs as a single conversation with file access and no worker primitive | Aider, Continue, or a desktop assistant with file tools | One model plays every role by switching labeled hats, and verification is a distinct labeled pass. `.scrum/` is written to disk as usual. | `adapters/single-model.md` |
| Has no file access at all | ChatGPT, Claude, Gemini, or another chat model in a browser | Paste a bootstrap prompt, then paste the core files the protocol asks for. `.scrum/` state lives in chat blocks you save and paste back. | `adapters/bootstrap-prompt.md` + `adapters/single-model.md` |

Rows describe primitives, so many products fit each row, and the row order runs
from the most runtime primitives to the fewest without ranking them. Products
inside a row are listed alphabetically, each as one example among others that show
the shape of a capability; naming one implies no endorsement, no preference, and
no claim that the package was built against it. Runtime capabilities change, so
confirm yours in the runtime's own documentation. The Setup subsections below
follow the same order.

Because every project's state is plain markdown under `.scrum/`, a project
started under one runtime can be resumed by another.

## Quick start

1. Get the package. Clone or download this repository into the project you want to
   build; its root is the `scrum` package, the folder that holds `AGENTS.md` and
   `SKILL.md`. Keep the folder name `scrum`, since every include path below
   (`scrum/SKILL.md`, `scrum/adapters/terminal-agent.md`) assumes it.

   ```bash
   git clone <repo-url> <project>/scrum
   ```

   A runtime that auto-discovers a skill folder can instead take the package from
   a directory it scans, for example a user-level skills directory that serves
   every project or a project-level one that serves a single repository. Clone into
   that path when your runtime works that way, again keeping the folder name:

   ```bash
   git clone <repo-url> <skills-dir>/scrum
   ```

2. Wire it into your runtime. The mechanism differs by capability: a skill folder
   is auto-discovered from `SKILL.md` with no include line; a terminal or IDE agent
   reads `AGENTS.md` or takes one include line in the rules file it loads; a single
   conversation with file access is pointed at the package directly; a chat-only
   model gets a pasted bootstrap prompt. Find your row in the capability matrix
   above and follow the matching Setup subsection.
3. Start the work. Invocation also differs by runtime: type `/scrum start "your
   product idea"` where slash commands exist, ask in natural language to build,
   plan, or run a product as a software team, or paste the chat-only prompt to
   begin the founding interview.

The agent runs the founding interview once, then walks you from idea to a
reviewed increment. You answer questions about outcomes and priorities; the team
does the building. No docs to read first.

## The two entry files

The package root holds two entry files that describe the same system. Neither is
primary, and a runtime needs only the one it can read.

- `AGENTS.md` is the file terminal and IDE agents read automatically. An agent that
  opens it learns what the package is, when to route to `SKILL.md`, how to pick a
  capability adapter, the load-on-demand rule, and the rules that hold before
  any code is written.
- `SKILL.md` is the file skill-folder runtimes discover from its `name` and
  `description` frontmatter. It carries the operating invariants, state and
  subcommand routing, context-assembly contract, and execution gate. Exact
  per-stage sections live in `core/context-routes.json` so one machine-readable
  source controls every runtime.

Both point at the same `core/` files and the same `.scrum/` state, so the system
behaves the same whichever one a runtime reads first. Where an agent reads only the
`AGENTS.md` at the repository root and the package sits in a subdirectory, add the
include line from the setup subsection below so the root file points at
`scrum/SKILL.md`.

## Example

The fastest way to see what a session looks like is the illustrative walkthrough
in `examples/first-sprint/walkthrough.md`. It is a written-out session for a
small fictional project, not a transcript of a real one, and it runs from the
first invocation through founding, vision, planning, an execution loop that
includes a Definition of Done gate failure and the rework it forces, the Review,
and the Retrospective. The example state sits beside it in
`examples/first-sprint/scrum-state/` and mirrors what the tool writes to
`.scrum/` in a real project.

## Setup per runtime capability

Follow exactly one subsection. Each is self-contained, each matches one row of the
matrix above in the same order, and the products named in the headings are
examples of the capability rather than requirements.

### Runtimes that auto-discover a skill folder (for example Claude Code or Goose)

Install the package as a skill so the runtime discovers it from the `name` and
`description` frontmatter in `SKILL.md`. No include line is needed. Copy the
package, keeping the folder name `scrum`, into a directory the runtime scans:

- a user-level skills directory, which makes it available in every project;
- a project-level skills directory, which scopes it to one repository.

Directory names differ per runtime; take the exact path from the runtime's own
documentation. Invoke the skill by asking to start, plan, run, review, or retro a
product, or by typing `/scrum <idea>` where slash commands exist. The Orchestrator
maps to the main loop and Developers to worker agents with parallel fan-out.
Details in `adapters/parallel-agents.md`.

### Terminal and IDE agents that read an instruction file (for example Cline, Codex CLI, or Cursor)

Some agents read an `AGENTS.md` at the repository root; an editor-integrated agent
reads a rules file instead. Copy the package to `<project>/scrum/`. An agent that
reads nested instruction files finds `scrum/AGENTS.md` on its own and needs no
further setup. Where the agent reads only the repository-root file, add this
include to whichever file it reads:

```markdown
# AGENTS.md
## Scrum organization
When asked to build, plan, run, review, or retro a product as a software team,
follow scrum/SKILL.md. Read scrum/adapters/terminal-agent.md for the role mapping.
Assemble exact stage and trigger context with scrum/scripts/context_router.py, or
follow scrum/core/context-routes.json when Python is unavailable. Keep all project
state in .scrum/ as plain markdown and commit it with each increment.
```

This is the same block `adapters/terminal-agent.md` carries; that file is the
canonical copy. Where the setup can start separate runs or background agents,
those act as Developers; where it cannot, the roles switch sequentially in one
session. Details in `adapters/terminal-agent.md`.

For an editor that loads a rules file rather than an `AGENTS.md`, put the same
instruction there as a rule:

```markdown
When the user asks to build, plan, or run a product as a software team, load
scrum/SKILL.md and follow scrum/adapters/terminal-agent.md when this runtime can
start separate runs or background agents as workers, and
scrum/adapters/single-model.md when it cannot. All state lives in .scrum/.
```

### One conversation with file access (for example Aider or Continue)

Copy the package to `<project>/scrum/`, then point the conversation at it: paste
Prompt A from `adapters/bootstrap-prompt.md`, or ask the model to read
`scrum/SKILL.md` and `scrum/adapters/single-model.md` and follow them. With no
  worker primitive the model plays every role by switching labeled hats (`[ORCH]`,
  `[PO]`, `[SM]`, `[DEV]`, `[DIAG]`, `[VERIFY]`), and a distinct `[VERIFY]` pass walks the
Definition of Done. State is written to `.scrum/` on disk and committed with the
increment. Self-verification is weaker than an independent verifier;
`adapters/single-model.md` states the limits and the mitigations.

### A chat model with no file access (for example ChatGPT, Claude, or Gemini)

No filesystem or tool access is required. Open `adapters/bootstrap-prompt.md` and
paste Prompt B, then paste each package file the protocol asks for:

1. `SKILL.md`, `core/artifact-writing-standard.md`,
   `core/route-triggers.md`, and `core/context-routes.json` first.
2. `core/framework.md` once for the project and `adapters/single-model.md` before
   the first role turn.
3. The exact stage sources selected by `core/context-routes.json`. Paste selected
   sections verbatim, or full selected files when reliable section loading is not
   available.
4. Any state, stall, threat, UI/UX, or full-writing module activated by
   `core/route-triggers.md`.

Keep the `.scrum/` state as fenced markdown blocks in the conversation, save each
block the model emits, and paste the latest ones back on resume. The same
self-verification limits and mitigations apply here.

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

### Engineering and specialist routing

The package does not equate engineering discipline with one testing ritual.
`core/test-strategy.md` uses TDD for deterministic behavior and regressions, then
routes legacy behavior, parsers, service boundaries, user journeys, visual work,
and probabilistic model behavior to methods that can test those claims.
`core/threat-modeling.md` activates when a PBI changes a material trust, data,
identity, dependency, deployment, or agent boundary.

Writing is integrated into Scrum. `core/artifact-writing-standard.md` loads the
standalone `research-clinical-writing` skill when available and supplies a
portable fallback otherwise. Product-specific design remains modular:
`core/ux-integration.md` calls the standalone `ux-fit` skill only for PBIs that
need UI or UX judgment. Backend and implementation-only work do not pay that
design cost.

Instruction routing is also explicit. `scripts/context_router.py` reads
`core/context-routes.json` and emits exact source sections for one stage, adapter,
and set of triggers. It never summarizes or truncates content; it fails on an
oversized bundle so the work can split at a safe boundary. Browser-only runtimes
follow the same route file manually and load full selected files when needed.
Every generated bundle ends with `core/execution-checklist.md`, keeping the final
scope, authority, attempt, evidence, privacy, and state checks near the action.
The optional scripts require Python 3.10 or later and use only the standard
library; the Markdown and JSON fallback has no executable dependency.

Stalled work follows `core/stall-recovery.md`: one hypothesis per mutating
attempt, evidence-defined progress, a default two-attempt budget, preserved diffs,
and read-only expert diagnosis selected by capability before model tier.
`scripts/stall_router.py` enforces the deterministic stop and support-selection
rules when code execution is available.

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
- **Expect an adaptive test choice.** Every build brief names TDD or another
  verification route and explains why it fits. A deterministic defect should show
  a failing regression test before the fix; a legacy refactor may need
  characterization evidence first; a parser may need fuzz or property evidence.
- **Keep specialist skills modular.** Install `research-clinical-writing` and
  `ux-fit` beside Scrum when the runtime supports skills. Scrum uses the writing
  skill for all artifacts and calls the design skill only when a UI/UX trigger
  applies. Its built-in fallbacks keep the package usable when either is absent.
- **Run `status` to orient**, `health` when momentum feels off or output rises
  while value stalls, and `dod` to see or re-instantiate the current gate.
- **Tune `.scrum/team.md` between sprints.** Retrospective items land there.
  Adjust cadence, norms, or the quality bar, and the next sprint follows the
  change.
- **When agents stall**, the worker stops mutating and returns a blocker packet.
  The Orchestrator preserves the failed work, selects a capability-matched expert
  for read-only diagnosis, then resumes, rebriefs, pairs, splits, or assigns a
  fresh worker. You are asked only for product intent, scope, or authority that
  the team cannot own.

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
├── .gitignore                blocks private research and generated scratch files
├── AGENTS.md                 entry point for agents that read it automatically
├── SKILL.md                  entry point and full router for skill-folder runtimes
├── README.md                 this file
├── CHANGELOG.md              version history
├── CONTRIBUTING.md           how to propose and test a change
├── ATTRIBUTION.md            sources this package builds on, and their licenses
├── adapters/                 named for runtime capability, never for a vendor
│   ├── parallel-agents.md    Orchestrator = main loop; Developers = worker agents
│   ├── terminal-agent.md     AGENTS.md or rules-file include; workers = separate runs
│   ├── single-model.md       single-model labeled-hat protocol
│   └── bootstrap-prompt.md   copy-paste prompts to boot any agent
├── core/
│   ├── framework.md          Scrum for AI teams: pillars, values, flow
│   ├── orchestrator.md       delegation, evidence gate, and bounded recovery routing
│   ├── events/               sprint-planning, daily-scrum, sprint-review, retrospective
│   ├── roles/                product-owner, scrum-master, developers
│   ├── dod/                  definition-of-done, profiles
│   ├── engineering-standards.md  risk, secure design, AI and supply-chain controls
│   ├── test-strategy.md      adaptive TDD and complementary verification routes
│   ├── threat-modeling.md    triggers, threat records, mitigation evidence
│   ├── artifact-writing-standard.md  compact writing and communication router
│   ├── artifact-writing-full.md      complete portable writing fallback
│   ├── context-routes.json   canonical stage, trigger, and adapter selections
│   ├── route-triggers.md     always-active conditional-route index
│   ├── stall-recovery.md     attempt limits and capability-aware diagnosis
│   ├── state-protocol.md     conditional bootstrap and crash recovery
│   ├── ux-integration.md     conditional bridge to the standalone ux-fit skill
│   └── anti-patterns.md      process-decay symptoms as automated checks
├── scripts/
│   ├── context_router.py     emits bounded verbatim instruction bundles
│   ├── stall_router.py       enforces stop and support-selection boundaries
│   └── audit_skill.py        checks routes, references, privacy, and rule ownership
├── tests/                    behavior tests for both deterministic routers
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
│   ├── threat-model.md     optional, when the security trigger applies
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
Keep private research files and extracts outside `.scrum/`; artifacts record only
the public or project-local evidence needed to reproduce a decision.
Start under one tool, continue under another, and the new tool reads `state.md`
and picks up where the last left off.

By default the team commits `.scrum/` and each code increment for you, so the
history stays resumable. Start from a clean working tree so each commit captures
only the increment, not pre-existing uncommitted changes. To keep commits in your
own hands, set `Delivery mode: stage-only` in `.scrum/team.md` and the team stages
its changes and reports them for you to commit, or set `branch-pr` to get the work
on a branch as a pull request the team never merges without you.

## FAQ

**Does this work without worker agents?**
Yes. `adapters/single-model.md` defines a single-model protocol where one model
plays every role by switching labeled hats and self-verifies the Definition of Done.
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
For stalled work, the capability registry takes precedence: required authority
and domain capability, then diagnostic strength, model tier, and cost.

**Does selective context remove knowledge from the skill?**
No. Every Markdown module remains canonical and complete. The router emits
verbatim sections for one operation and retains source paths. If a complete route
is too large, it stops instead of trimming; the team splits the operation at a
stage, event, PBI, or diagnostic boundary. A runtime without Python follows the
same JSON route and may load each selected file in full.

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
Use the chat-only path in `adapters/bootstrap-prompt.md` or
`adapters/single-model.md`.
The model keeps each `.scrum/` file as a fenced markdown block in the conversation
and re-emits it on every change. You save the blocks and paste them back to resume.

**Can two different tools work the same project?**
Yes. All state is plain markdown under `.scrum/`. One tool can plan a sprint,
another can execute it, and a third can run the review, as long as each reads
`state.md` first. This is the reason to commit `.scrum/`.

**How do I uninstall or stop using it?**
Stop invoking `/scrum`. To remove the package, delete the `scrum/` folder from
wherever you cloned it, your project or a skills directory, and delete the include
line if you added one. Your project's `.scrum/` directory is just markdown; keep it
as a record or delete it. Neither affects your source code.

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
