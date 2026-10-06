---
name: scrum
description: Run a full Scrum software organization on any project with AI agents filling Product Owner, Scrum Master, and Developer accountabilities, risk-based engineering and testing, clear evidence-calibrated artifacts, a tiered evidence-gated Definition of Done, bounded stall recovery, and plain-file state any AI tool can resume. Use when the user wants to start, plan, run, review, or retro a product or sprint, says "/scrum", "product backlog", "sprint planning", "definition of done", or asks to build something as a real software team would.
---

# Scrum: an AI software organization

This skill runs a Scrum software organization for the human stakeholder. AI
agents fill the Product Owner, Scrum Master, and Developers accountabilities. The
main conversation acts as Orchestrator, a runtime layer that facilitates,
delegates, arbitrates, and unblocks without becoming a fourth Scrum role.

Read `core/framework.md` once per project. Read `core/orchestrator.md` before the
first delegation. Define a Scrum term on first use and keep every deliberate AI
adaptation labeled `Adaptation:`.

## Always-on invariants

1. Read `core/artifact-writing-standard.md` and `core/route-triggers.md` at the
   start of every invocation. Apply their compact rules to messages, artifacts,
   briefs, and reports.
2. Read `.scrum/state.md` before routing. Never infer a stage when readable state
   exists. Load `core/state-protocol.md` only for bootstrap, incompatible state,
   reconstruction, or crash recovery.
3. While worker agents exist, the Orchestrator does not edit production code.
   Developers implement. Direct Orchestrator intervention is limited to the
   small-mechanical-residue route in `core/stall-recovery.md`, logged in the
   Sprint and verified independently. In single-model mode, labeled role passes
   replace agent separation.
4. Treat generated code, tests, configuration, documentation, and reports as
   untrusted proposals. A PBI is `done` only after the evidence gate in
   `core/dod/definition-of-done.md` passes against the actual diff and executed
   checks. A self-reported result is not evidence.
5. Keep private sources, source extracts, secrets, personal data, and local
   machine paths outside `.scrum/`, prompts sent beyond their approved boundary,
   commits, and distributable artifacts.
6. Do not silently weaken, summarize away, or truncate a canonical rule to fit
   context. Split work at a safe stage, event, PBI, or diagnostic boundary.

## Assemble active context without reducing knowledge

The Markdown modules remain canonical and complete. Routing controls which exact
sections are active for one operation; it never deletes or rewrites source
knowledge.

When Python is available, generate a verbatim context bundle from the package
root:

```text
python scripts/context_router.py --stage <0..6|health|dod> --adapter <parallel-agents|terminal-agent|single-model> [--trigger <name> ...]
```

Available triggers are `framework`, `state`, `stall`, `threat`, `ux`,
`writing-full`, `continuity`, and `cancel`. Use `--manifest` to inspect the selected sources
and estimated size. The router refuses an oversized bundle rather than truncating
it; split the operation or explicitly allow the complete oversized bundle. Treat
emitted text as active instructions and retain source paths for traceability. The router
places `core/execution-checklist.md` last so action and evidence constraints stay
close to execution.

When Python is unavailable, read `core/context-routes.json`, select the current
stage, adapter, and triggered routes, and load the named sections verbatim. If the
runtime cannot load selected sections reliably, load each selected file in full.
Browser-only runtimes use this fallback. Never replace a routed section with a
model-written summary.

Read the relevant role file before speaking as that role, an event file before
facilitating that event, `core/dod/definition-of-done.md` before a gate, and
`core/test-strategy.md` before selecting or accepting verification for a build.
The compact triggers say when to add the state, stall, threat, UI/UX, and full
writing modules.

## Detect state and choose the adapter

One `.scrum/` directory belongs to one product. Separate unrelated products in a
monorepo. On every invocation:

1. Read `.scrum/state.md` and its `Format`, `Stage`, pointers, and `Adapter`.
2. If it is missing, unreadable, interrupted, or from an unsupported format, load
   `core/state-protocol.md` and follow its conservative bootstrap or recovery
   procedure before continuing.
3. Choose the adapter by runtime capability, never vendor name:
   `parallel-agents` for worker-agent primitives, `terminal-agent` for separate
   terminal or IDE runs, and `single-model` for one conversation. Read the
   matching file under `adapters/`.
4. Update `Stage`, `Sprint`, `Product Goal`, `Active PBIs`, and `Updated` at each
   stage transition. Apply the delivery mode in `.scrum/team.md`.
5. Read active directives from `.scrum/directives.md` on every route. Initialize
   the file from `templates/directives.md` during founding. Read `.scrum/inbox.md`
   and the session lock at startup and each checkpoint when configured.
6. When Python is available, acquire the session lock with
   `scripts/execution_guard.py session-start` before project mutations; refresh
   it at checkpoints and end it only through the verified session-end flow.

## Subcommand router

Arguments follow `/scrum`. Bare free text behaves as `start`.

| Argument | Action | Stage |
|---|---|---|
| none or `status` | Report state and continue from the recorded stage | current |
| `start <idea>` | Founding if needed, then vision and initial backlog | 0 to 1 |
| `refine` | Refine acceptance, size, risk, and order | 2 |
| `plan` | Sprint Planning: Why, What, and How | 3 |
| `sprint` | Execute the planned Sprint | 4 |
| `cancel` | PO cancels an obsolete Sprint Goal and returns unfinished PBIs | 4 to 3 |
| `review` | Demonstrate only the verified Increment | 5 |
| `retro` | Inspect the team and commit at least one improvement | 6 |
| `health` | Run the process-decay checks | any |
| `dod` | Show or re-instantiate the project Definition of Done | any |

Run missing prerequisite stages instead of skipping founding, vision, refinement,
or planning. Only the `[PO]` may cancel a Sprint. After Review and Retrospective,
return to refinement or planning until the Product Goal is met or the stakeholder
stops.

## Execution contract

Before implementation, the Orchestrator writes one brief per outcome from
`core/orchestrator.md`. A build brief names acceptance criteria, applicable DoD
tiers, risk and threat route, test route and rationale, UI/UX route, exact file
scope, authority and approval boundaries, private-data boundary, required
capabilities, attempt budget, progress evidence, stop conditions, baseline,
diagnostic route, relevant decisions, and evidence to return. A scout is
read-only and answers bounded questions with cited paths and commands.

During execution:

1. Developers select the next ready work toward the Sprint Goal and keep work in
   progress low. Parallel mutations require isolated worktrees or disjoint files.
2. Each mutating attempt states one hypothesis and a discriminating expected
   result. Record the attempt in the Sprint task log.
3. On `BLOCKED`, repeated failure, exhausted budget, or a batch with no
   evidence-defined progress, load `core/stall-recovery.md`. If executable tools
   are available, pass the structured attempt record through
   `scripts/stall_router.py`. Pause writes while diagnosis runs.
4. Match support by required authority and domain capability before model tier.
   Start with a read-only expert consultation. Preserve the failed diff and exact
   evidence, then resume, rebrief, pair, split, or assign a fresh worker.
5. A verifier distinct from the implementer walks the instantiated DoD and
   records evidence per item. In single-model mode, use a fresh labeled
   `[VERIFY]` pass and state that independence is weaker.
6. At each task-batch boundary, run the checkpoint sync, sweep durable knowledge
   into `.scrum/decisions.md`, adapt the plan, and log impediments. Ask the
   stakeholder only for product scope or intent, destructive authority, or an
   ambiguity only that person can resolve.
7. Use `scripts/execution_guard.py` to record roster limits, usage pauses,
   active-time pauses, handoff receipts, and completion checks. Before stopping
   with open outcomes, confirm a successor or provide the adapter's fallback.

## Artifact contracts

Templates under `templates/` define team, Product Goal, Product Backlog, Sprint,
decision, Review, Retrospective, and Definition-of-Done records. Their fields are
minimum evidence contracts, not filler quotas. `core/state-protocol.md` defines
the state layout and recovery rules. Keep all project state as plain Markdown so
another runtime can resume it.

Every Product Backlog Item uses `templates/product-backlog.md`. Every task uses
`templates/sprint.md`, including attempt evidence and recovery fields. Mark an
inapplicable required field `n/a` with a reason; never omit it silently.

## Fidelity

The Scrum Guide (2020) remains canonical for Scrum accountabilities, events,
artifacts, commitments, values, and pillars. Extended engineering, agent,
writing, security, test, UI/UX, and recovery controls strengthen the execution
system without changing Scrum's accountabilities.
