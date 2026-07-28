<!--
  TEMPLATE: definition-of-done.md
  Instantiate to .scrum/DEFINITION_OF_DONE.md at stage 0 FOUNDING; refresh with
  /scrum dod. Authoritative source and gate protocol: core/dod/definition-of-done.md.
  Stack profile items: core/dod/profiles.md. Tier 3 is merged from the founding
  interview (setup/founding-interview.md) and the project scan
  (setup/project-scan.md); existing org standards are a floor, never weakened.
  Keep it plain markdown, committed to the repo.

  This is the instantiated quality commitment for the Increment. A PBI reaches
  "done" only when a verifier distinct from the implementer walks these items and
  records evidence per item into the PBI's DoD-evidence field. Mark an
  unverifiable item n/a WITH A REASON; never skip it silently.
-->

# Definition of Done

- Project: <name>
- Instantiated: <YYYY-MM-DD>  |  Last refreshed: <YYYY-MM-DD>
- Selected stack profiles: <Web UI | API/service | Library | CLI | AI/LLM | ...>
- How to verify (project commands, from the scan): build `<cmd>` | test `<cmd>` | lint `<cmd>` | typecheck `<cmd>` | format `<cmd>`

## Tier 0: Universal (every increment, every project)
<!-- Fixed floor. Do not weaken. Verify each with the project's real commands. -->
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
<!-- Applies whenever the PBI touches external input or authn. Otherwise mark n/a with reason. -->
- [ ] Input validated at every trust boundary
- [ ] Authorization checked on every protected path
- [ ] No sensitive data written to logs
- [ ] No stack traces or internal errors returned to clients
- [ ] Dependency audit clean
- [ ] Rate limiting on public endpoints
- [ ] Secret scanning passed

## Tier 2: Stack profiles (selected at setup)
<!--
  Include only the profiles selected in team.md. Copy the item list for each
  from core/dod/profiles.md. Placeholders below; replace with the real items.
-->

### Profile: <Web UI | API/service | Library | CLI | AI/LLM>
- [ ] <profile item from core/dod/profiles.md>
- [ ] <profile item>

<!--
  AI/LLM profile applies if the product calls models. It adds: evals defined and
  passing before ship, prompt versioning, injection guardrails, cost and latency
  budgets, fallback on model failure, PII/data-privacy handling, model/version
  pinning, monitoring hooks. Copy the authoritative list from core/dod/profiles.md.
-->

## Tier 3: Project-specific (merged from interview + scan)
<!--
  From setup/founding-interview.md (quality bar, constraints) and
  setup/project-scan.md (CI gates, existing standards files). Every CI gate and
  every testable rule from a standards file becomes an item here, attributed to
  its source. Existing org standards are a floor; the team may add, never weaken.
-->
- [ ] <CI gate becomes a DoD item> (source: <path>)
- [ ] <rule from an existing standards file> (source: <path>)
- [ ] <stakeholder quality rule from the founding interview>

## Gate protocol (summary)
<!-- Full protocol in core/dod/definition-of-done.md. -->
- The verifier is an agent distinct from the implementer, or the Orchestrator, or
  in single-model mode a labeled self-verification pass.
- The verifier walks every applicable item, runs the real command, and records
  evidence (command output, test summary, file paths) into the PBI's DoD-evidence
  field in product/backlog.md.
- Unverifiable items are marked n/a with a reason.
- The Increment is the set of PBIs that passed the gate. Only those are
  demonstrated at the Sprint Review.

<!--
  Evolving the DoD is healthy. When the Retrospective adds a rule that would make
  the Increment more releasable (health check S2.8), add it to Tier 3 and record
  the change in metrics.md and team.md.
-->
