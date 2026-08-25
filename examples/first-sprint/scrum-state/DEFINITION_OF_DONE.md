# Definition of Done

*Illustrative output from the fictional project in `examples/first-sprint/walkthrough.md`, not a real project's state.*

- Project: exif-rename
- Instantiated: 2026-07-14 | Last refreshed: 2026-08-25
- Selected stack profiles: CLI
- Project commands: build `uv build` | test `uv run pytest` | lint `uv run ruff check .` | typecheck `uv run mypy src` | format `uv run ruff format --check .`

## Tier 0: Universal

- [ ] Changed files and exact routed instruction modules were read before edit; the diff stays inside authorized scope
- [ ] Acceptance maps to evidence; risk, test, security, UX, capability, attempt, baseline, stop, and diagnostic routes are recorded
- [ ] The project builds reproducibly from `uv.lock`
- [ ] Fit-for-purpose checks and the full `pytest` suite pass
- [ ] Ruff lint and format, mypy, and project policy gates pass
- [ ] A verifier inspects the actual diff, tests, generated fixtures, dependency changes, and deletions
- [ ] No credentials, unnecessary photo data, private source material, or local private paths ship
- [ ] EXIF and filesystem boundaries validate their contracts and fail safely
- [ ] Help text, README, and Scrum artifacts match the result and pass the writing audit
- [ ] File-write rollback and recovery behavior are exercised where applicable
- [ ] The increment is scoped, attributable, and recoverable

## Tier 1: Security and assurance

<!-- EXIF metadata and filenames are untrusted input, and rename is a potentially destructive file action. Apply relevant items and mark each other item n/a with its own reason. -->

- [ ] A current threat record covers malformed EXIF, path handling, collisions, partial failure, and overwrite risk
- [ ] EXIF values, filenames, paths, and output names are constrained and tested
- [ ] Identity and authorization are n/a unless a later version adds shared or remote use
- [ ] Photo data stays local and is absent from logs except for the minimum path the user requested
- [ ] Corrupt input, collision, timeout, and partial rename preserve every original file
- [ ] Pillow and transitive dependencies have an intentional source, locked graph, and triaged audit
- [ ] File count, file size, path length, and batch resource limits apply when folder mode ships
- [ ] Secret, dependency, and relevant static checks run
- [ ] Each threat mitigation maps to a test; residual file-loss risk has an owner and review point

## Tier 2: Stack profiles

### Profile: CLI

- [ ] Every command and subcommand responds to `--help` with usage, options, and a description
- [ ] Exit codes are documented; success exits 0 and failure exits non-zero
- [ ] Primary output goes to stdout and diagnostics go to stderr
- [ ] Any advertised structured output is valid and stable
- [ ] The command does not block on a prompt without a TTY

## Tier 3: Project-specific floor

- [ ] The tool makes no network calls; image data never leaves the machine (source: founding interview, data rules)
- [ ] No existing file is overwritten, moved, or deleted destructively; a name collision resolves to a new name (source: founding interview, irreversible file-write constraint)
- [ ] Ruff lint and format and mypy type checks pass locally while CI is absent (source: founding interview and project scan)

## Gate protocol

- The implementer self-checks and returns exact evidence.
- A distinct verifier reads the PBI, brief, threat record, checklist, and diff from source and tries to falsify the result.
- The verifier records evidence or an individual `n/a` reason per item. Failed or unavailable checks do not pass.
- Only a PBI with a clean gate joins the Increment and appears at the Sprint Review.
