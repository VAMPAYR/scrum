# Scrum state protocol

Read this file when `.scrum/state.md` is absent, unreadable, incompatible, or
requires crash recovery. Normal invocations read the existing state and do not
load this protocol.

## Bootstrap

One `.scrum/` directory belongs to one product. In a monorepo, keep separate
state and backlogs for unrelated products.

Create `.scrum/state.md` with this shape:

```markdown
# Scrum State
- Format: 1
- Stage: 0 FOUNDING
- Sprint: 000
- Product Goal: not set
- Active PBIs: none
- Adapter: <parallel-agents | terminal-agent | single-model>
- Updated: <YYYY-MM-DD>
```

At founding, also copy `templates/directives.md` to `.scrum/directives.md`,
instantiate `templates/team.md`, and create empty `.scrum/inbox.md`. Preserve the
directive file's active-entry and stakeholder-decision headings; the context
router loads those sections on every route.

`Format` identifies the state layout. Stop when the value is higher than the
supported format. Treat a missing value as an unknown older layout and migrate it
before continuing. Do not infer fields under an unknown layout. Format stays `1`
until a migration rewrites the state shape.

Choose the adapter by runtime capability:

- worker-agent primitive: `parallel-agents`;
- separate terminal or IDE runs: `terminal-agent`;
- one conversation with no worker primitive: `single-model`.

Read legacy values as follows and write the current value on the next update:
`claude-code` becomes `parallel-agents`, `openai` becomes `terminal-agent`, and
`generic` becomes `single-model`. This mapping is read-compatible with Format 1.

Update `Stage`, `Sprint`, `Product Goal`, `Active PBIs`, and `Updated` at every
stage transition.

## Reconstruction and crash recovery

If `.scrum/` exists without a readable state file, reconstruct conservatively:

- `team.md` implies founding completed;
- `product/product-goal.md` implies vision completed;
- an unfinished task in `sprints/sprint-NNN/sprint.md` implies execution;
- completed Sprint evidence plus no Review implies review;
- a completed Review plus no Retrospective implies retrospective.

Rewrite `state.md` to match the evidence and record the reconstruction.

For interrupted execution:

1. Read the task log before delegating new work.
2. Treat `in-progress`, `in-review`, and unsupported `done` claims as unfinished.
3. Diff half-applied work against the task's authorized files.
4. Re-run missing Definition-of-Done evidence from scratch. For a scout, re-check
   every named question against cited paths or commands instead of applying the
   build gate.
5. For a stalled task, load `core/stall-recovery.md` and reconstruct its attempt
   count from the recorded evidence. Do not grant a fresh budget merely because
   the process restarted.
6. Record what was preserved, re-verified, or discarded.

## Delivery modes

`.scrum/team.md` selects one delivery mode:

- `commit`: commit state and the verified increment together;
- `branch-pr`: deliver a branch and pull request without merging for the user;
- `stage-only`: stage and report the changes for the user to commit.

Start from a clean working tree in every mode. Never include unrelated existing
changes in an increment.

## State layout

```text
.scrum/
|-- team.md
|-- directives.md
|-- inbox.md
|-- handoff-log.md
|-- state.md
|-- DEFINITION_OF_DONE.md
|-- product/
|   |-- product-goal.md
|   `-- backlog.md
|-- sprints/sprint-NNN/
|   |-- sprint.md
|   |-- threat-model.md       optional
|   |-- review.md
|   `-- retrospective.md
|-- decisions.md
|-- impediments.md
|-- metrics.md
|-- session-lock.json       runtime-owned; ignored by Git
`-- runtime/                runtime-owned execution ledger; ignored by Git
```

Keep state in plain Markdown so another runtime can resume it. Keep private
sources, source extracts, secrets, personal data, and personal local paths out of
state and distributable artifacts.
