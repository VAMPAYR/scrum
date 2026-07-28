# Definition of Done

*Illustrative output from the fictional project in `examples/first-sprint/walkthrough.md`, not a real project's state.*

- Project: exif-rename
- Instantiated: 2026-07-14  |  Last refreshed: 2026-07-14
- Selected stack profiles: CLI
- How to verify (project commands, from the scan): build `uv build` | test `uv run pytest` | lint `uv run ruff check .` | typecheck `uv run mypy src` | format `uv run ruff format --check .`

## Tier 0: Universal (every increment, every project)
- [ ] Read before edit: the implementer read the files it changed
- [ ] Builds cleanly with the project build command
- [ ] The full test suite passes, not only the new tests
- [ ] New behavior has tests proportional to its risk and blast radius
- [ ] Lint and typecheck pass clean
- [ ] No debug output, commented-out code, or stray print statements left in
- [ ] No hardcoded secrets or credentials
- [ ] Errors are handled at trust boundaries, not swallowed
- [ ] Docs updated where behavior changed
- [ ] Commits are scoped with conventional messages; no unrelated changes

## Tier 1: Security (any code touching external input or authentication)
<!-- EXIF metadata read from arbitrary files is untrusted external input, so 1.1 applies. The remaining items are marked n/a with a reason at the gate for a local, network-free CLI. -->
- [ ] Input validated at every trust boundary
- [ ] Authorization checked on every protected path
- [ ] No sensitive data written to logs
- [ ] No stack traces or internal errors returned to clients
- [ ] Dependency audit clean
- [ ] Rate limiting on public endpoints
- [ ] Secret scanning passed

## Tier 2: Stack profiles (selected at setup)

### Profile: CLI
- [ ] Help text: every command and subcommand responds to `--help` with usage, options, and a description
- [ ] Exit codes: exits 0 on success and a documented non-zero code on failure; distinct failure classes use distinct codes where defined
- [ ] stdin/stdout/stderr contract: primary output to stdout in the documented format; diagnostics and errors to stderr; reads stdin where a pipe interface is advertised
- [ ] Machine-readable output where advertised: any structured output mode is valid and stable
- [ ] Non-interactive safe: does not block on a prompt without a TTY, or fails with a clear message

## Tier 3: Project-specific (merged from interview + scan)
- [ ] The tool makes no network calls; image data never leaves the machine (source: founding interview, data rules)
- [ ] No existing file is overwritten, moved, or deleted destructively; a name collision resolves to a new, non-colliding name (source: founding interview, conservative area: irreversible file writes)
- [ ] `ruff` lint and format and `mypy` type checks pass; no CI is configured yet, so the gate runs them locally (source: founding interview, quality bar; project scan found no CI)

## Gate protocol (summary)
- The verifier is an agent distinct from the implementer, or the Orchestrator, or in single-model mode a labeled self-verification pass.
- The verifier walks every applicable item, runs the real command, and records evidence (command output, test summary, file paths) into the PBI's DoD-evidence field in product/backlog.md.
- Unverifiable items are marked n/a with a reason.
- The Increment is the set of PBIs that passed the gate. Only those are demonstrated at the Sprint Review.
