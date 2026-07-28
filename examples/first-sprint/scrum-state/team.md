# Team charter

*Illustrative output from the fictional project in `examples/first-sprint/walkthrough.md`, not a real project's state.*

- Project: exif-rename
- Stakeholder: the photographer (the human user), who offloads memory cards to a laptop
- Adapter: claude-code
- Founded: 2026-07-14

## Communication
- Update style: terse status
- Vocabulary: plain language; Scrum terms defined on first use
- Source: stakeholder choice

## Interruption tolerance
- Batch non-blocking questions to the Review: yes
- Interrupt immediately for: scope decisions, destructive or irreversible actions, exhausted escalation ladder
- Additional interrupt triggers: none stated

## Risk appetite
- Default lean: moderate
- Take the riskiest assumption early when blast radius fits one Sprint: yes
- Areas that must stay conservative: anything that writes, moves, or deletes a photo on disk

## Quality bar vs speed
- Never-drop floor: universal tier + security tier of the Definition of Done
- Bar above the floor: plus the CLI stack profile
- Areas where a rough, labeled spike is acceptable: none
- Feeds Tier 3 of .scrum/DEFINITION_OF_DONE.md

## Cadence
- Sprint length (one work cycle, one Sprint Goal): a few hours, one evening session
- Review frequency: end of each session
- Checkpoints per Sprint (adapted Daily Scrum): between task batches

## Definition of value
- Value the team optimizes for: a user dumps a memory card and gets chronologically sortable filenames without renaming by hand
- How the stakeholder knows a cycle was worth it: "I stop renaming photos by hand in Finder."

## Technical constraints
- Language / framework / platform: Python 3.12; Pillow for EXIF; argparse for the CLI
- Hosting / deployment target: local command-line tool on macOS and Linux; installed with pip
- Required or forbidden dependencies: no network dependencies; the tool makes no network calls
- Data and compliance rules: photos are personal data; image data never leaves the machine

## Review evidence
- Required evidence per PBI: a runnable result the stakeholder drives, plus test output
- Stakeholder drives the demo: yes

## Staffing
- Tiers available in this runtime: two, a strong tier and a mid-tier worker tier
- Orchestrator, PO, and SM tier: the strongest available model
- Developer tier: mid-tier worker models
- Senior Developer: off. One small CLI with no task large enough to need a standing design-and-review seat this cycle.
- Senior Developer tier: n/a
- Verifier tier: at least the implementer's tier, never weaker; the strongest available model for any PBI that writes, moves, or deletes a photo

## Delivery mode
- Mode: commit
- The photographer does not read diffs, so the team commits `.scrum/` and each increment together from a clean working tree, and a bad rename can be traced and reverted one commit at a time.

## Stack profiles selected
- CLI

## Detected commands (project scan)
<!-- The founding scan found an empty repo; the toolchain below was chosen at founding and established during sprint-001. -->
- Build: uv build
- Test: uv run pytest
- Lint: uv run ruff check .
- Typecheck: uv run mypy src
- Format: uv run ruff format --check .
- Package manager / environment: uv, dependencies pinned in uv.lock

## CI gates (project scan)
- none detected; no CI configured yet (new repo at founding)

## Existing standards files (project scan)
- none; new repo at founding

## Working agreement
- Honest reporting: failed output is reported verbatim, never smoothed over.
- Ask for help early: blockers reach impediments.md with a clear ask.
- Evidence over claims: no "done" without gate evidence.
- The floor holds: universal and security tiers are never lowered for a deadline.
- Version control: the Delivery mode section above governs how each increment lands. Start from a clean working tree.
- Never move or overwrite a photo the tool cannot safely rename; a collision resolves to a new name.

## Amendments log
- 2026-07-14, sprint-001: any PBI that writes, moves, or deletes files must name the overwrite or destructive path in its delegation brief and carry a failure-path test before it reaches the gate. Added after PBI-001 passed its happy-path tests but overwrote a same-second collision on the first gate walk.
