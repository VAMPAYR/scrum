# Definition of Done

The Definition of Done (DoD) is the shared quality commitment for an Increment.
It describes the state a Product Backlog Item (PBI) must reach before the team can
call it done. A claim, review comment, or model-generated summary cannot grant that
state. A verifier records evidence against the instantiated checklist in
`.scrum/DEFINITION_OF_DONE.md`.

Read `core/engineering-standards.md` for the engineering system behind the gate,
`core/test-strategy.md` for method selection, and `core/threat-modeling.md` when a
security trigger applies. Apply `core/artifact-writing-standard.md` to the gate
record itself.

## The four tiers

| Tier | Scope | Source |
|---|---|---|
| 0 Universal | Every PBI | This file |
| 1 Security and assurance | Every PBI considers the trigger; apply relevant items when triggered | This file |
| 2 Stack profiles | Selected by product type and applied per PBI | `core/dod/profiles.md` |
| 3 Project-specific | Organization, repository, stakeholder, and CI floor | Founding interview and project scan |

Each item includes a rule and the evidence a verifier needs. Mark an item `n/a`
only with a concrete reason. A missing tool, failed command, or unavailable
environment is not a pass; it is a finding or impediment.

## Tier 0: Universal

Every PBI clears all of Tier 0.

### 0.1 Scope and context were read before edit

- **Rule.** The implementer read each changed file and relevant caller, contract,
  test, configuration, project instruction, and exact stage or triggered module
  before editing. The change stays within the brief or records an authorized
  scope change.
- **Evidence.** Files and searches consulted, routed source list or manifest, and
  a diff-scope statement.

### 0.2 Acceptance, risk, and verification routes are explicit

- **Rule.** Observable acceptance criteria map to verification. The brief records
  the material risks, the selected test route and reason, and whether threat
  modeling and the UI/UX specialist route apply. It also records required
  capabilities, baseline, attempt budget, evidence-defined progress, stop
  conditions, and diagnostic route.
- **Evidence.** Criterion-to-check mapping, test route, security trigger decision,
  UX route decision, and the task's attempt and recovery fields.

### 0.3 The build is reproducible

- **Rule.** The project builds from the declared source and resolved dependency
  graph without undocumented local state. Generated artifacts are attributable
  and repeatable where the project promises reproducibility.
- **Evidence.** Clean build or package command, environment, exit status, and
  relevant lockfile or provenance path.

### 0.4 Fit-for-purpose checks and the full suite pass

- **Rule.** New or changed behavior carries the tests, analysis, or hands-on
  checks selected under `core/test-strategy.md`. The full relevant suite passes.
  Higher-risk paths include misuse, failure, and recovery checks.
- **Evidence.** Acceptance and risk mapping; focused and full-suite commands and
  results; observed red-then-green evidence when the TDD route was selected.

### 0.5 Static and policy gates pass

- **Rule.** Applicable lint, type, format, static-analysis, policy, and CI checks
  pass without a new unexplained suppression or weaker threshold. Run the
  project's CI on the delivered branch. When CI targets a different operating
  system, run that job or a documented equivalent on the target platform.
  Tests skip optional dependencies cleanly when they are absent.
- **Evidence.** Commands, exit status, and a disposition for each new finding or
  suppression.

### 0.6 The actual diff passed adversarial review

- **Rule.** A reviewer inspects code, tests, generated files, migrations,
  configuration, dependency changes, and deletions. AI-produced work is treated
  as untrusted input. The review rejects invented APIs, placeholder behavior,
  weakened tests, disabled controls, and unrelated changes.
- **Evidence.** Reviewer identity or labeled pass, diff reviewed, issues found,
  and resolution. The implementer's prose does not count as review evidence.

### 0.7 Secrets and private material are absent

- **Rule.** The change, history in scope, logs, prompts, fixtures, and artifacts
  contain no hardcoded credentials, unnecessary personal data, proprietary source
  material, or private local paths. Temporary source extracts stay in verified
  ignored storage and do not ship.
- **Evidence.** Secret and privacy scan result, ignore-rule check where scratch
  material existed, and disposition of findings.

### 0.8 Boundaries fail safely

- **Rule.** Each changed entry point or external call validates its contract,
  handles timeout and failure, preserves authorization, and returns no sensitive
  internal detail. Retries and resource use are bounded where applicable.
- **Evidence.** Boundary and failure-path tests, or `n/a` with a reason when the
  PBI changes no boundary.

### 0.9 Documentation and artifacts match the result

- **Rule.** User, caller, operator, architecture, and Scrum artifacts change with
  the behavior they describe. Prose passes `core/artifact-writing-standard.md`:
  outcome first, clear actors and actions, precise uncertainty, adjacent sources
  when available, and no filler or smoothed failure.
- **Evidence.** Paths changed and the completed artifact audit, or `n/a` with a
  reason when no documented behavior changed.

### 0.10 Operational consequences are handled

- **Rule.** A production-facing change defines the telemetry, rollout, migration,
  rollback, recovery, and support behavior proportionate to its impact. The team
  tests a realistic failure or recovery path when one exists.
- **Evidence.** Operational artifact and exercised result, or `n/a` with a reason
  for non-operational work.

### 0.11 The increment is scoped and recoverable

- **Rule.** Every hunk serves the PBI. Required refactoring is named. Drive-by
  changes are separate. Version-control history follows the project's delivery
  mode and message convention, and the increment can be reverted or isolated.
- **Evidence.** Final diff summary, delivery reference, and rollback or isolation
  note for a consequential change.

### 0.12 Product text follows its recorded standard

- **Rule.** When a PBI changes user-facing text, the reviewer checks every changed
  string against the product text standard recorded in `.scrum/team.md` for
  clarity, factual accuracy, terminology, accessibility, and the project's tone.
- **Evidence.** Paths or keys for changed strings, reviewer disposition, and
  applicable string or accessibility tests. Mark `n/a` with a reason when no
  user-facing text changed.

## Tier 1: Security and assurance

Every PBI evaluates this trigger. Apply Tier 1 when the PBI changes a trust
boundary, external input, identity, permission, secret, sensitive data, privacy
behavior, cryptography, parser, public endpoint, dependency trust, build or
deployment path, infrastructure, privileged tool, autonomous action, model or
retrieval path, or architecture assumption with material impact. Apply relevant
items and mark the rest `n/a` with individual reasons.

### 1.1 Risk and threat records cover the change

- **Rule.** The team models the changed system under `core/threat-modeling.md`, or
  records why an existing model remains sufficient. Each material risk has an
  asset, condition or event, consequence, treatment, owner, assumptions, and
  verification.
- **Evidence.** Threat-model or risk-record path, stable IDs, and trigger decision.

### 1.2 Trust-boundary input is constrained

- **Rule.** The system validates type, shape, size, encoding, range, and allowed
  values before an input or action crosses a boundary. It uses safe query and
  output construction for the destination context.
- **Evidence.** Hostile, malformed, oversized, and boundary-value test results,
  plus query or output review where relevant.

### 1.3 Identity and privilege are minimized

- **Rule.** The system authenticates identity and authorizes every protected
  action before effects occur. Users, services, agents, and tools receive only the
  minimum capability and lifetime required.
- **Evidence.** Unauthenticated, wrong-user, expired-credential, and
  over-privileged tests; permission or capability review.

### 1.4 Sensitive data is minimized and protected

- **Rule.** The change limits collection, transfer, retention, replication, and
  logging of sensitive data. Storage and transport protections match the threat
  model. Logs redact secrets and unnecessary content.
- **Evidence.** Data-flow and retention decision, protection configuration, and
  redaction or disclosure tests.

### 1.5 Failure preserves security

- **Rule.** Malformed input, dependency failure, timeout, partial deployment, and
  internal error do not grant access, leak internals, corrupt protected state, or
  continue a high-impact action without authorization.
- **Evidence.** Failure, rollback, and non-disclosure test results.

### 1.6 Supply-chain risk is triaged

- **Rule.** New and changed components have an intentional source, supported
  version policy, resolved build graph, license review where required, and
  vulnerability disposition based on exposure and impact. High-risk products use
  stronger provenance, signature, attestation, or bill-of-material controls.
- **Evidence.** Dependency diff, audit result, finding dispositions, lock or
  compatibility evidence, and provenance artifacts where required.

### 1.7 Abuse and resource exhaustion are bounded

- **Rule.** Public, expensive, automated, and high-impact operations enforce the
  rate, concurrency, cost, size, timeout, retry, and cancellation limits that the
  threat model requires. A universal HTTP rate limit is not required when another
  control better fits the risk.
- **Evidence.** Limit configuration and abuse or exhaustion test, or `n/a` with a
  reason.

### 1.8 Security checks and secret scanning ran

- **Rule.** The project runs the relevant secret, static, dynamic, dependency,
  container, infrastructure, or policy checks. Findings are fixed, mitigated,
  accepted by the risk owner, or tracked with a due point.
- **Evidence.** Commands and results, with one disposition per material finding.

### 1.9 Mitigations and residual risk are closed explicitly

- **Rule.** Every implemented mitigation maps to a test, analysis, review, alert,
  or recovery exercise. The deployed design matches the model. A named owner
  accepts material residual risk. Consequential changes carry the compact
  assurance case from `core/engineering-standards.md`.
- **Evidence.** Threat-to-mitigation-to-check mapping, assurance case when
  triggered, residual-risk owner, and review point.

## The gate protocol

`done` is a verified state.

1. **The implementer self-checks.** The Developer runs the selected checks and
   returns exact commands, results, paths, and known failures.
2. **A verifier starts from source criteria.** A verifier distinct from the
   implementer reads the PBI, brief, `.scrum/DEFINITION_OF_DONE.md`, applicable
   profile, risk records, and changed diff. In single-model mode, a labeled
   `[VERIFY]` pass re-reads these sources before judging the work.
3. **The verifier tries to falsify the result.** It inspects the actual change,
   checks test quality, reruns project gates, and probes material failure paths.
4. **The verifier records evidence per item.** Evidence includes command output,
   test summaries, analysis findings, paths, screenshots when necessary, and
   `n/a` reasons. A generic `passes` statement is insufficient.
5. **Failure stays visible.** The verifier reports failed output accurately. The
   PBI returns for rework or to the Product Backlog; the team never demonstrates
   it as part of the Increment.
6. **Pass changes state.** Only a clean gate changes the PBI to `done`. The
   Developers remain accountable for conformity to the DoD; the Product Owner
   separately decides product acceptance. The Increment contains only PBIs that
   passed.

The verifier must be at least as capable as the implementer. Use the strongest
available independent reviewer for security-sensitive, destructive,
privacy-critical, or difficult-to-reverse work. Self-verification is weaker and
must say so in the evidence.

## Scrum rules that govern the DoD

- The Developers are accountable for creating and conforming to the DoD.
- An organizational standard is the floor. Tier 3 imports it and may strengthen
  it, but the team may not weaken it.
- Multiple teams working on one product share one DoD for the combined Increment.
- The Retrospective may strengthen the DoD. It may not lower Tier 0, Tier 1, or an
  organizational floor to meet a deadline. The team cuts scope instead.
- Work that does not meet the DoD returns to the Product Backlog. It is not part
  of the Increment and is not represented as complete at the Sprint Review.

## How Tier 3 merges

Tier 3 combines two evidence sources:

1. The founding interview supplies stakeholder constraints, quality commitments,
   compliance duties, and required review evidence.
2. The project scan supplies existing standards, CI gates, commands, architecture
   rules, test requirements, security policy, and design-system constraints.

Copy each testable rule into `.scrum/DEFINITION_OF_DONE.md` with its source path.
Keep the stricter rule when sources conflict and ask the stakeholder only when
the conflict changes product scope or authority. Re-scan when the stack, CI,
security architecture, model use, or design system changes.

## Adaptation note

The Scrum Guide defines the purpose and governance of the Definition of Done but
does not prescribe these engineering tiers or an AI-agent verification protocol.
This package adds a tiered, evidence-gated default for AI-assisted delivery. The
adaptation strengthens transparency and quality without changing Scrum's
accountabilities, artifacts, commitments, or events.
