# Definition of Done

The Definition of Done (DoD) is the quality bar an Increment must clear before it
counts as real. It is a commitment attached to the Increment: a formal
description of the state the Increment reaches when it meets the quality measures
required for the product. The moment a Product Backlog Item (PBI) meets the DoD,
an Increment exists. A PBI that does not meet the DoD is not released and is not
presented at Sprint Review; it returns to the Product Backlog for future
consideration.

This skill enforces the DoD as a verification gate with recorded evidence, not a
self-reported checkbox. This file defines the two universal tiers (Tier 0 and
Tier 1), the gate protocol, the official rules that govern any DoD, and how
project-specific criteria (Tier 3) merge in. Stack-specific criteria (Tier 2)
live in `core/dod/profiles.md`. The fuller engineering reference the Developers
draw from is `core/engineering-standards.md`.

## The four tiers

The DoD is layered. Every project gets Tier 0 and Tier 1. Tier 2 profiles are
selected at setup for the stacks the project uses. Tier 3 holds rules specific to
this project. At setup the selected tiers are flattened into one checklist in the
target repo at `.scrum/DEFINITION_OF_DONE.md`, instantiated from
`templates/definition-of-done.md`.

| Tier | Scope | Source |
|---|---|---|
| 0 Universal | Every increment, every project | This file |
| 1 Security | Any code touching external input or authentication | This file |
| 2 Stack profiles | Selected per stack at setup (Web UI, API/service, Library, CLI, AI/LLM) | `core/dod/profiles.md` |
| 3 Project-specific | Merged from the founding interview and detected standards | `setup/founding-interview.md`, `setup/project-scan.md` |

Each criterion below states four things: the **rule** (what must hold), the
**why** (the risk it removes), **verify** (generic command guidance, since the
skill is stack-agnostic), and **evidence** (what the verifier records into the
PBI so a reader can confirm the check ran).

## Tier 0: Universal

Every PBI, in every project, clears all of Tier 0.

### 0.1 Read before edit
- **Rule.** Every file a change touches was read in full before it was edited,
  and the call sites of any changed function or interface were located.
- **Why.** Context-blind edits break callers the author never saw and reintroduce
  removed behavior. Reading first is the cheapest defect prevention available.
- **Verify.** Review-level check: the delegation brief named the files in scope,
  and the change stays inside them. A search for the changed symbol shows every
  caller was considered.
- **Evidence.** List of files read and the search used to find call sites.

### 0.2 Builds cleanly
- **Rule.** The project builds from a clean checkout with the committed lockfile,
  no manual steps, no errors.
- **Why.** A green local build that depends on undocumented state does not
  reproduce in CI or on another machine. A clean build is the precondition for
  every other check.
- **Verify.** Run the project build with the deterministic install
  (`npm ci`, `pip install --require-hashes`, `cargo build --locked`,
  `go build ./...`, or the stack equivalent). Exit code 0.
- **Evidence.** Build command and its exit status or final lines.

### 0.3 Full test suite passes
- **Rule.** The entire test suite passes, not only the tests added for this PBI.
- **Why.** A change that passes its own new tests can still break unrelated code.
  Running the full suite is what catches that regression before Sprint Review.
- **Verify.** Run the whole suite (`pytest`, `go test ./...`, `cargo test`,
  `npm test`, or the stack runner). All pass; none skipped without a reason.
- **Evidence.** Runner summary line (counts of passed, failed, skipped).

### 0.4 New behavior has tests proportional to risk
- **Rule.** New or changed behavior carries tests sized to its risk and blast
  radius. Higher-risk paths (auth, money, data loss, external input) get more.
- **Why.** Tests written with the change turn intended behavior into an executable
  specification and a permanent guardrail. Skipping them defers the cost to a
  future incident. Test-first or test-with-code is the team's practice: describe
  the expected behavior in an executable form, then implement against it.
- **Verify.** Confirm each acceptance criterion maps to at least one test.
  Higher-risk criteria map to more than one, including a failure-path test.
- **Evidence.** Mapping from acceptance criteria to test names.

### 0.5 Lint and type checks clean
- **Rule.** The linter and, where the language has one, the type checker pass with
  no new errors or suppressions added to force a pass.
- **Why.** Lint and type gates catch a class of defects mechanically, so reviewers
  spend attention on logic. A silenced warning is deferred debt.
- **Verify.** Run the linter and type checker (`eslint`/`tsc`, `ruff`/`mypy`,
  `golangci-lint`, `clippy`, or the stack equivalent). Zero new findings.
- **Evidence.** Linter and type-checker exit status.

### 0.6 No debug output
- **Rule.** No stray print, console, or debug logging remains in production code
  paths. Diagnostics go through the structured logger.
- **Why.** Ad-hoc prints are unqueryable, leak data, and clutter output. Routing
  diagnostics through the logger keeps them redacted and greppable (see
  `core/engineering-standards.md`, structured logging with redaction).
- **Verify.** Grep changed files for banned raw-print calls outside test code.
- **Evidence.** Grep pattern used and that it returned no production hits.

### 0.7 No hardcoded secrets
- **Rule.** No API keys, tokens, passwords, or credential-bearing URLs appear in
  source, config, or fixtures.
- **Why.** A committed secret is a leak the moment it enters history, and history
  is hard to scrub. Detection at the point of change is the only cheap moment.
- **Verify.** Run a secret scanner over the changed tree (`gitleaks`,
  `trufflehog`, `detect-secrets`) with an allowlist for example files.
- **Evidence.** Scanner output showing zero findings, or each finding justified.

### 0.8 Errors handled at boundaries
- **Rule.** Every entry point (request handler, command, external call) validates
  its inputs and handles failure. Errors returned outward are generic; internal
  detail stays server-side.
- **Why.** Unhandled failures at a boundary crash the caller or leak internals.
  A boundary that validates and degrades gracefully contains the failure (see
  `core/engineering-standards.md`, handler template and error handling).
- **Verify.** For each new boundary, a test drives the failure path and asserts a
  handled, non-leaking response.
- **Evidence.** Names of the failure-path tests.

### 0.9 Docs updated when behavior changes
- **Rule.** When behavior a user or caller relies on changes, the documentation
  that describes it changes in the same PBI. Documentation lives near the code and
  is versioned with it.
- **Why.** Documentation that drifts from behavior misleads the next reader and
  the next agent. The Scrum Team decides the type and amount of documentation its
  DoD requires; the rule is that changed behavior does not ship with stale docs.
- **Verify.** Confirm changed public behavior has a matching doc edit (README,
  API reference, help text, or changelog).
- **Evidence.** Paths of the updated docs.

### 0.10 Scoped commits with conventional messages
- **Rule.** Commits are scoped to the PBI and use a conventional message
  (`type(scope): subject`). No unrelated changes ride along.
- **Why.** Machine-readable messages drive changelogs and versioning and force
  intent into history. Scoped commits keep review and revert precise (see
  `core/engineering-standards.md`, CI is the merge gate).
- **Verify.** Read the diff: every hunk serves the PBI. The message matches the
  conventional shape.
- **Evidence.** Commit message and a one-line confirmation the diff is in scope.

### 0.11 No unrelated changes
- **Rule.** The change set contains only what the PBI requires. Opportunistic
  refactors, formatting sweeps, and unrelated fixes are separate PBIs.
- **Why.** Mixed diffs hide the real change, enlarge the review surface, and
  complicate revert. Small, single-purpose batches are the team's discipline:
  refactoring needed for the PBI is allowed and named, drive-by edits are not.
- **Verify.** Diff review confirms scope. Refactoring needed for the PBI is
  allowed and named; drive-by edits are not.
- **Evidence.** Confirmation in the DoD evidence that the diff is single-purpose.

## Tier 1: Security

Tier 1 applies to any PBI whose code touches external input, authentication, or
authorization. If a PBI touches none of these, mark each Tier 1 item `n/a` with
that reason. The fuller reference for each item is `core/engineering-standards.md`.

### 1.1 Validation at trust boundaries
- **Rule.** No raw external input reaches a database, a downstream service, or a
  rendering sink. Every entry point validates against a schema, coerces and
  escapes, and rejects known-malicious patterns.
- **Why.** The network-to-application boundary is where injection enters (XSS,
  SQL injection, template injection, null bytes). Validating once at the boundary
  stops hostile data before it propagates to where it is harder to neutralize.
- **Verify.** Unit-test the validator with hostile inputs (script tags,
  `javascript:` URLs, null bytes, oversized strings). Confirm parameterized
  queries or ORM binding, not string concatenation, for any query.
- **Evidence.** Names of the input-validation tests and their result.

### 1.2 Authorization on every protected path
- **Rule.** Every protected route, action, and realtime connection checks
  authentication and authorization before it does work. Realtime and streaming
  channels authenticate at connect time.
- **Why.** A protected path missing its check is a direct route to another user's
  data or actions. Realtime channels bypass per-request HTTP auth, so an
  unauthenticated socket is a broadcast leak.
- **Verify.** Integration test: unauthenticated and wrong-user requests are
  rejected before any effect. For realtime, a connection with no or invalid token
  is refused before any message is delivered.
- **Evidence.** Names of the auth-guard tests.

### 1.3 No sensitive data in logs
- **Rule.** Logs never contain passwords, tokens, keys, or message contents. The
  structured logger redacts a defined set of sensitive field names automatically.
- **Why.** Automatic redaction keeps secrets out of logs even when an author
  forgets, which is the realistic failure mode. Aggregated logs are a common
  leak surface.
- **Verify.** Unit-test that logging an object with sensitive keys emits the
  redaction placeholder, not the value.
- **Evidence.** Name of the log-redaction test.

### 1.4 No stack traces to clients
- **Rule.** Error responses returned to clients are generic and carry a
  correlation ID. Stack traces, file paths, and dependency detail stay in
  server-side logs only.
- **Why.** Stack traces leak internal structure to attackers and give legitimate
  clients nothing actionable. A stable error contract plus a request ID gives
  clients something to report while keeping internals private.
- **Verify.** Security test asserting no stack trace or internal path appears in
  any error response, and every error body carries a request ID.
- **Evidence.** Name of the error-handling test.

### 1.5 Dependency audit clean
- **Rule.** No dependency carries a known vulnerability at the project's chosen
  severity threshold or higher. Dependencies are pinned to exact versions.
- **Why.** Ranges allow silent upgrades that can introduce breakage or a
  supply-chain compromise between builds. Auditing catches known advisories at the
  point of introduction rather than in production.
- **Verify.** Run the stack audit tool (`npm audit --audit-level=moderate`,
  `pip-audit`, `cargo audit`, `govulncheck`, `bundler-audit`, or the equivalent).
  Confirm the lockfile is committed and in sync.
- **Evidence.** Audit command and its summary (zero findings at threshold, or
  each finding triaged).

### 1.6 Rate limiting on public endpoints
- **Rule.** Every public or authenticated endpoint enforces a request-rate cap,
  tuned tighter for auth, writes, and expensive operations.
- **Why.** Rate limits contain brute-force credential attacks, spam, scraping,
  and resource-exhaustion denial of service.
- **Verify.** Integration test that exceeding the limit returns HTTP 429, and the
  response carries rate-limit headers.
- **Evidence.** Name of the rate-limit test and the limits applied to new
  endpoints.

### 1.7 Secret scanning
- **Rule.** A secret scan runs over the whole source tree as a test and in CI,
  with an allowlist for example and fixture files.
- **Why.** Scanning as a test converts "do not commit secrets" from a hope into
  an enforced gate that also guards future commits.
- **Verify.** Run the secret-scan test and the CI scanner. Both pass.
- **Evidence.** Scanner result over the source tree.

## The gate protocol

`done` is a verified state, never a claim. When a Developer reports a PBI
complete, the gate runs.

1. **Independent verifier.** The verifier is an agent distinct from the
   implementer, or the Orchestrator acting as verifier. A Developer never passes
   its own work through the final gate. In single-model mode, where no separate
   agent exists, a labeled self-verification pass (`[DEV]` to `[ORCH]`) runs
   instead; this is weaker and `adapters/generic.md` states the limits and
   mitigations.
2. **Walk the instantiated DoD.** The verifier reads `.scrum/DEFINITION_OF_DONE.md`
   (the flattened Tier 0 + Tier 1 + selected Tier 2 profiles + Tier 3 rules) and
   checks every item against the actual change, running the verify command for
   each rather than trusting a summary.
3. **Record evidence per item.** For each DoD item the verifier writes concrete
   evidence into the PBI's `DoD evidence` field: command output, a test-summary
   line, or a file path. Evidence is specific enough that a reader can confirm the
   check ran without re-running it.
4. **`n/a` needs a reason.** An item that does not apply to this PBI is marked
   `n/a` with the reason (for example "no external input, Tier 1 not triggered").
   An item is never silently skipped. An unverifiable item is `n/a` with a reason,
   not an implicit pass.
5. **Honest failure reporting.** A failed check is reported verbatim. Failed test
   output is pasted as-is, never paraphrased or smoothed over. A PBI that fails
   any item is not `done`; it returns to the Developers or the backlog. The
   Developers decide whether an Increment is releasable against the DoD, and that
   judgment is not overridable from outside the team.
6. **The increment is the passed set.** The Increment is exactly the set of PBIs
   that passed the gate. Only those are demonstrated at Sprint Review; nothing
   else is shown. See `core/events/sprint-review.md`.

The Orchestrator triggers the gate on every "done" claim and does not accept a
PBI as complete without recorded evidence (see `core/orchestrator.md`, section 5,
evidence never trust). The PBI record format and its `DoD evidence` field are
fixed in `SKILL.md`.

## Official rules that govern a DoD

The DoD is not the team's private preference. Three rules from the official Scrum
definition (2020) constrain it, stated here as the skill's own rules.

- **Organizational floor.** If the Definition of Done is part of the standards of
  the organization, all Scrum Teams follow it as a minimum. If no organizational
  standard exists, the Scrum Team creates one appropriate for the product. In
  this skill, the Tier 3 merge treats any detected organizational standard as that
  floor (see below).
- **Strengthen, never weaken.** A team may add criteria above the floor; it may
  not drop below it. Expanding the DoD is part of continuous improvement: as the
  team closes a capability gap (for example a reliable deployment pipeline), it
  can put stronger quality goals into the DoD, step by step. A Retrospective may
  strengthen the DoD; it may not relax Tier 0, Tier 1, or the organizational
  floor.
- **Who owns it.** The Scrum Team creates and owns its DoD. The Developers are
  accountable for conforming to it and for judging whether an Increment is
  releasable against it; nobody outside the Developers can force delivery of work
  that is not Done. The Product Owner is accountable for not reducing the quality
  goals the DoD encodes. In this skill the Orchestrator holds the gate; the
  Product Owner protects the quality goals during ordering and acceptance; the
  Developer agents deliver against the DoD. Roles stay labeled and separated (see
  `core/orchestrator.md`, section 6, role labeling).

## How Tier 3 project-specific criteria merge in

Tier 3 is where this project's own rules enter the DoD. Two sources feed it, both
run at stage 0 FOUNDING.

1. **Project scan.** `setup/project-scan.md` detects existing standards and gates
   already in the repo: an engineering-standards or contributing document, CI
   config with required checks, a linter or formatter config, a commit-message
   convention, pre-commit hooks. Each detected standard becomes a Tier 3 floor.
   The DoD adopts these as minimums the team may strengthen and may not weaken,
   per the organizational-floor rule above.
2. **Founding interview.** `setup/founding-interview.md` asks the stakeholder for
   quality rules the scan cannot detect: regulatory or audit requirements, a
   required release sign-off, performance or accessibility targets, data-handling
   rules. A required sign-off, if one exists, is written into the DoD and obtained
   during the Sprint as part of the delivery pipeline, not deferred to a gate
   after the fact.

The merge produces `.scrum/DEFINITION_OF_DONE.md`: Tier 0 and Tier 1 verbatim,
the Tier 2 profiles selected for this project's stacks (`core/dod/profiles.md`),
and the Tier 3 rules from the two sources above. Where a Tier 3 rule generalizes
a standard already stated in `core/engineering-standards.md`, cite that file so a
maintainer can trace it. The instantiated file, not this one, is what the gate
walks; this file is the source the instantiation is built from.

## Adaptation note

**Adaptation:** Official Scrum leaves the content of a DoD to the team. This skill
ships a concrete, tiered, evidence-gated default (Tier 0 and Tier 1) so a new
project has a working quality bar on day one, and treats detected organizational
standards as a floor on top of it. The intent, an Increment that is genuinely
usable and transparent about its quality, is preserved: the tiers are a starting
minimum the team strengthens over time, never a ceiling and never a substitute
for the team's judgment.
