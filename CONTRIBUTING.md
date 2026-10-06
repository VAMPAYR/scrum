# Contributing

Changes to this package are welcome. This file states how to propose a change,
the constraints every change must hold, and how to test one before you open it.

## Proposing a change

- Open an issue first for changes to behavior, state layout, or the Definition of
  Done. Describe the problem, desired outcome, and proposed change.
- Send a pull request for the change. Keep it scoped to one concern, and update
  every file the change touches in the same PR so the package stays consistent.
- Small fixes (wording, a broken path, a typo) can go straight to a pull request.

## Constraints every change must hold

- `core/` stays vendor-neutral. Use "Orchestrator", "worker agent", and "the
  runtime"; keep runtime-specific detail in `adapters/`, never in `core/`.
- Adapter files are named for runtime capability, never for a vendor, and the
  `Adapter` token in `.scrum/state.md` uses those capability names. Name a
  specific product only as one example among at least two, only inside an adapter
  file or a `README.md` matrix cell, and never as the default, the primary, or the
  reference implementation.
- Keep the prose free of name-dropping and marketing. Credit is a separate matter
  from prose style: every external framework, model, or standard the package reuses
  is credited in `ATTRIBUTION.md`, and where a distinctive taxonomy is reproduced
  (a named set of levels, areas, or measures), credit its originator at the point
  of use as well. Reproduce no third-party text; state every rule in fresh wording.
- Never commit private research files, source extracts, credentials, personal
  data, or local absolute paths. Keep temporary research under an ignored
  directory, verify the ignore rule and tracked-file list, then cite only public
  sources in distributable package text.
- Content states rules directly. Prefer the imperative rule over description of who
  said it.
- No em dashes. Write concise, formal prose in active voice.
- Apply `core/artifact-writing-standard.md` to package prose. Project-specific
  writing guides remain optional inputs; preserve `ux-fit` as a conditional
  standalone specialist route.
- Stay accurate to the Scrum Guide (2020) for accountabilities, events, artifacts,
  commitments, pillars, and values. Never contradict it silently. State its rules
  in this package's own wording rather than reproducing its text. Mark every
  deliberate change for AI teams with an explicit "Adaptation:" note.
- Every change to a `.scrum/` state format bumps the `Format` field in
  `state.md` and documents a migration so existing projects can move forward.
- Templates and core files stay consistent. If you change a record shape in
  `core/`, update the matching file in `templates/`, and the reverse, in the same
  change.
- Keep full knowledge in canonical modules. Change stage, adapter, and trigger
  selection in `core/context-routes.json`; do not duplicate that routing table in
  another entry file or replace selected source text with a generated summary.
- Keep `core/stall-recovery.md` as the sole definition site for `STALL-1` through
  `STALL-10`. Other files cite those identifiers and specialize runtime mapping
  without redefining the invariants.

## Testing a change

- Run `python -m unittest discover -s tests -v` and
  `python scripts/audit_skill.py`. The first checks observable routing and stop
  behavior; the second checks route headings, context budgets, references,
  canonical rule ownership, privacy patterns, and excluded source formats.
- Run `python scripts/context_router.py --stage 4 --manifest` and inspect the
  selected execution sources and estimated size. Exercise at least one trigger
  and one adapter when either map changed.
- Run the lifecycle on a toy project in at least one runtime, from `start` through
  `retro`, and confirm the state files it writes match the templates.
- Run the health check (`/scrum health`) and confirm it reports cleanly.
- Run `python scripts/audit_health.py --project-root <fixture>` against a fixture
  containing continuity state, including clean, pending-message, stale-lock, and
  open-outcome cases.
- Confirm the paths named in `README.md` and `SKILL.md` resolve to real files.
- Exercise one deterministic TDD route, one non-TDD route, one security trigger,
  and both outcomes of the UI/UX trigger. Confirm each route leaves the evidence
  required by the Definition of Done.
- Search the package and tracked-file list for private filenames, absolute local
  paths, source extracts, and secrets before publishing.
