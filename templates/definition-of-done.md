<!--
  TEMPLATE: definition-of-done.md
  Instantiate to .scrum/DEFINITION_OF_DONE.md at stage 0 FOUNDING; refresh with
  /scrum dod. The authoritative rules and gate protocol are in
  core/dod/definition-of-done.md. Stack items come from core/dod/profiles.md.
  Tier 3 merges the founding interview and project scan. Keep this file as plain
  markdown committed with the project.
-->

# Definition of Done

- Project: <name>
- Instantiated: <YYYY-MM-DD> | Last refreshed: <YYYY-MM-DD>
- Selected stack profiles: <Web UI | API/service | Library | CLI | AI/LLM | ...>
- Project commands: build `<cmd>` | test `<cmd>` | lint `<cmd>` | typecheck `<cmd>` | format `<cmd>`

## Tier 0: Universal

- [ ] Scope and context were read before edit; the diff stays inside authorized scope
- [ ] Acceptance criteria map to evidence; risk, test, security, and UX routes are recorded
- [ ] The project builds reproducibly from its declared dependency graph
- [ ] Fit-for-purpose checks and the full relevant test suite pass
- [ ] Applicable lint, type, format, static-analysis, policy, and CI gates pass
- [ ] A verifier inspected the actual diff, tests, generated files, configuration, dependencies, and deletions
- [ ] No secrets, unnecessary personal data, proprietary source material, or private local paths ship
- [ ] Changed boundaries validate their contracts and fail safely
- [ ] Documentation and Scrum artifacts match the result and pass the artifact writing audit
- [ ] Production consequences, rollback, recovery, and telemetry are handled where applicable
- [ ] The increment is scoped, attributable, and recoverable

## Tier 1: Security and assurance

<!--
  Evaluate the trigger for every PBI. Apply relevant items when work changes a
  trust boundary, external input, identity, permission, secret, sensitive data,
  privacy behavior, cryptography, parser, public endpoint, dependency trust,
  build or deployment path, infrastructure, privileged tool, autonomous action,
  model or retrieval path, or a material architecture assumption. Mark each
  non-applicable item n/a with its individual reason.
-->

- [ ] A current risk or threat record covers the changed system and assumptions
- [ ] Trust-boundary input and output are constrained and tested
- [ ] Authentication, authorization, identity, and privilege follow least privilege
- [ ] Sensitive data is minimized, protected, and absent from unnecessary logs
- [ ] Timeout, partial failure, and internal error preserve security and data integrity
- [ ] Dependency and supply-chain findings are triaged by exposure and impact
- [ ] Abuse, rate, concurrency, cost, size, retry, and cancellation limits fit the threat model
- [ ] Relevant secret, static, dynamic, dependency, infrastructure, and policy checks ran
- [ ] Each mitigation maps to evidence; residual risk has an owner and review point

## Tier 2: Stack profiles

<!-- Copy only selected profiles from core/dod/profiles.md. Apply per PBI. -->

### Profile: <Web UI | API/service | Library | CLI | AI/LLM>

- [ ] <profile item from core/dod/profiles.md>
- [ ] <profile item>

## Tier 3: Project-specific floor

<!--
  Merge required CI gates, organizational and repository standards, stakeholder
  constraints, compliance duties, architecture rules, and design-system rules.
  Attribute each item to its public or project-local source. Keep the stricter
  rule when sources conflict.
-->

- [ ] <project rule> (source: <project path or public standard>)
- [ ] <CI gate> (source: <configuration path>)
- [ ] <stakeholder quality commitment>

## Gate protocol

- The implementer self-checks and returns exact evidence.
- A distinct verifier reads the PBI, brief, checklist, risk records, and diff from source.
- The verifier tries to falsify the result and records evidence per applicable item.
- An unavailable or failed check is a finding, not a pass. Mark only genuinely non-applicable items `n/a` with a reason.
- A PBI joins the Increment only after a clean gate. Single-model self-verification records its weaker independence.
