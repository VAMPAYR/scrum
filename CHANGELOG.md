# Changelog

Notable changes to this package are recorded here, newest first. Versions follow
semantic versioning (MAJOR.MINOR.PATCH). Each release names what changed; a change
to the `.scrum/` state layout bumps the `Format` field and ships a migration note.

## 1.1.0 - 2026-07-28

- Staffing tiers in `.scrum/team.md`: a model tier per seat, with the strongest
  available model on orchestration, diagnosis, and verification, mid-tier worker
  models on Developer briefs, a verifier never weaker than the implementer, and an
  optional senior Developer for the hardest task of a Sprint. **Adaptation:** the
  senior Developer is a skill distribution inside the single Developers
  accountability, not a new role or title.
- Shared team memory at `.scrum/decisions.md`: the durable decisions, interfaces,
  and gotchas every Developer brief carries, swept in at the checkpoint sync and
  pruned at the Retrospective, with a template in `templates/decisions.md`.
- Scout briefs for investigations: a read-only brief that returns findings rather
  than code changes, so exploration does not enter the increment unverified.
- Delivery modes replacing the single auto-commit switch: `commit` (default),
  `branch-pr` (work on a branch, deliver a pull request, never merge without the
  stakeholder), and `stage-only`. An existing `Auto-commit: on` maps to `commit`
  and `Auto-commit: off` maps to `stage-only`.
- Worktree isolation guidance for parallel Developers, so concurrent briefs cannot
  collide in the working tree where the runtime exposes worktrees.
- A diagnosis step on the escalation ladder, so a stalled task is understood
  before it is retried.

`Format` stays 1: every change here is additive or lives in a template, and an
existing `.scrum/` directory stays readable as written. `templates/team.md` gained
sections, but instantiated files do not have to be rewritten to match: a missing
`decisions.md` or a missing `Staffing` or `Delivery mode` section means only that
the feature is unset, with `Auto-commit` read per the mapping above. A project
written under 1.0.0 resumes without migration.

## 1.0.0 - 2026-07-14

Initial release.

- Role model and Orchestrator protocol: Product Owner, Scrum Master, and
  Developers as separate labeled accountabilities, with delegation briefs, an
  escalation ladder, and the rule that the Orchestrator writes no production code
  while worker agents are available.
- Evidence-gated tiered Definition of Done with stack profiles: a universal tier,
  a security tier, selectable stack profiles, and project-specific rules merged as
  a floor, where `done` is granted only against recorded evidence.
- Nine subcommands plus `cancel` covering the full lifecycle: `status`, `start`,
  `refine`, `plan`, `sprint`, `review`, `retro`, `health`, `dod`, and the Product
  Owner Sprint cancellation.
- Adapters for skill-folder, terminal, IDE, and chat-only runtimes, so the same
  core runs on a subagent-capable tool, a Codex-style terminal agent, an IDE
  agent, or a single chat model switching labeled hats.
- Plain-markdown `.scrum/` state with `Format` versioning, plus a worked
  first-sprint example that ships the resulting state tree for browsing.
