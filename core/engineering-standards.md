# Engineering standards

This file is the project-agnostic engineering reference the Developers work from
during EXECUTION. It states production engineering standards as stack-neutral
principles that apply to any language or runtime. It is the single reference for
how code is written, tested, secured, and deployed under this skill.

Relationship to the Definition of Done: the DoD (`core/dod/definition-of-done.md`)
is the enforced minimum, checked at the gate with recorded evidence. This file is
the fuller reference behind it. When a project has a standard the DoD should
promote to an enforced item, the Tier 3 merge (`core/dod/definition-of-done.md`,
Tier 3 section) pulls it into `.scrum/DEFINITION_OF_DONE.md` and cites the
standard here.

Each standard states four things: the **principle** (the rule), **why** (the risk
it removes), **verify anywhere** (how to check it in any stack), and an
**example** (illustrative, not prescriptive). Examples show the shape, not a
required tool.

## 1. Exact dependency pinning

- **Principle.** Pin every dependency to an exact version. No caret or tilde
  ranges. Audit dependencies on every change and in CI. Commit the lockfile and
  keep it in sync.
- **Why.** Ranges allow silent minor or patch upgrades that can introduce
  breakage or a supply-chain compromise between builds. Exact pins make every
  version bump a deliberate, reviewable act and make builds reproducible.
- **Verify anywhere.** Run the stack audit tool on every dependency change and in
  CI: `npm audit` / `pnpm audit`, `pip-audit` or `safety`, `cargo audit`,
  `govulncheck`, `bundler-audit`, `dotnet list package --vulnerable`, or the
  JVM equivalent. Install deterministically from the lockfile (`npm ci`,
  `pip install --require-hashes`, `cargo build --locked`). Add a check that
  rejects range specifiers in the manifest.
- **Example.** A manifest pins an exact version such as `1.4.2` rather than a
  range like `^1.4.0`, and CI fails the build on a moderate-or-higher advisory.

## 2. Structured logging with redaction

- **Principle.** Use a structured logger, never raw print or console statements,
  in production code. The logger auto-redacts a defined set of sensitive field
  names and truncates overlong strings. Log format switches by environment
  (machine-parseable in production, human-readable in development).
- **Why.** Structured logs are queryable and aggregatable; ad-hoc prints are not
  and often leak. Automatic redaction keeps secrets and user content out of logs
  even when an author forgets, which is the realistic failure mode. Truncation
  bounds log volume and prevents accidental dumps of large payloads.
- **Verify anywhere.** Unit-test that logging an object with sensitive keys emits
  the placeholder, not the value. Grep the codebase for banned raw-print calls in
  non-test code.
- **Example.** A logger redacts fields such as `password`, `token`, `apiKey`,
  `authorization`, and `privateKey` to `[REDACTED]` and truncates strings past
  200 characters. Generalize the redaction set to the project's own secrets and
  sensitive fields, including any user-content fields.

## 3. Request tracing

- **Principle.** Every request receives a unique correlation ID at entry. That ID
  appears in all log lines for the request, in a response header, and in any error
  body returned to the client.
- **Why.** A single correlation ID ties a client-visible failure to the server
  logs, making incident triage a lookup instead of a guess.
- **Verify anywhere.** Assert the response carries a request-ID header and that a
  forced error returns the same ID that appears in the logs.
- **Example.** Each request is tagged with a prefixed token (for example
  `req_` plus 16 hex characters); the token appears in every log entry, the
  `X-Request-ID` header, and error responses. Any unique, greppable token works.

## 4. Error handling that never leaks internals

- **Principle.** A shared error handler wraps all entry points. It maps known
  validation errors to a typed client error with structured detail, logs
  unhandled errors by type and message (not the full stack in production), and
  returns a generic server-error body. Every error response carries the request
  ID.
- **Why.** Stack traces and internal error strings leak file paths, dependency
  versions, and logic to attackers and are useless to legitimate clients. A
  stable, generic error contract plus a correlating request ID gives clients
  something actionable while keeping internals server-side.
- **Verify anywhere.** Security test asserting no stack trace or internal path
  appears in any error response. Assert every error body contains a request ID.
- **Example.** A shared handler returns `{ error: 'Validation failed', details,
  requestId }` at 400 for known validation errors and `{ error: 'Internal server
  error', requestId }` at 500 otherwise, logging error type not full stack in
  production.

## 5. Validate input at trust boundaries

- **Principle.** No raw external input reaches a database, a downstream service,
  or a rendering sink. Every entry point validates against a schema, coerces and
  escapes, and rejects known-malicious patterns outright.
- **Why.** The network-to-application boundary is where injection enters (XSS,
  SQL injection, template injection, null bytes). Validating and escaping once at
  the boundary prevents malformed or hostile data from propagating into storage or
  rendering, where it is far harder to neutralize. Deny-by-default with an
  allowlist beats trying to enumerate every bad input.
- **Verify anywhere.** Unit-test the validator with hostile inputs: script tags,
  `javascript:` URLs, event-handler attributes, null bytes, oversized strings.
  Prefer parameterized queries or ORM binding so escaping is not the only defense
  against injection. Assert length caps and type coercion at the schema layer.
- **Example.** A schema validates and truncates a string, strips null bytes, and
  HTML-escapes the five dangerous characters, while a separate check rejects
  requests matching obvious attack patterns.

## 6. Enforce one handler template per entry point

- **Principle.** Every request handler (HTTP route, realtime handler, RPC method)
  follows one template with five mandatory elements: validate all inputs against a
  schema, generate a request ID, check authentication and authorization, emit
  structured logs, and wrap the body in an error handler that never leaks internal
  detail. Realtime handlers add origin and token checks at connect, rate limiting,
  and deduplication.
- **Why.** A single enforced template makes every entry point uniformly safe and
  observable. Missing any one element (an unvalidated input, an unauthenticated
  path, a leaked stack trace, an unlogged failure) is a recurring source of
  incidents; the template turns "remember to do these" into "match the pattern."
- **Verify anywhere.** Integration tests per route asserting: invalid body returns
  a validation error; unauthenticated returns 401; the success path logs with a
  request ID; a server error returns a generic message plus request ID and no
  stack. A review checklist confirms each handler instantiates the template.
- **Example.** Both an HTTP route and a realtime handler generate a request ID,
  load the caller and reject if absent, schema-validate the payload, and funnel
  failures to the shared error handler; the realtime path adds an injection check,
  a rate-limit check, and duplicate detection.

## 7. Secret scanning

- **Principle.** A secret scan runs over the whole source tree, both as a test and
  in CI, with an allowlist for example and fixture files. Secret-bearing files are
  never committed.
- **Why.** Scanning as a test converts "do not commit secrets" from a hope into an
  enforced gate. Detection at the point of change is the only cheap moment; a
  committed secret is a leak the moment it enters history.
- **Verify anywhere.** Run a scanner (`gitleaks`, `trufflehog`, `detect-secrets`)
  as a test and in CI. Add ignore entries for env and secret files. Confirm the
  scan covers all source files.
- **Example.** A test scans for API-key shapes, password assignments, hardcoded
  tokens, and database URLs with embedded credentials, allowlisting the example
  env file and dummy fixtures.

## 8. Test taxonomy

- **Principle.** Organize tests into four tiers, each with a distinct purpose:
  unit (pure logic in isolation), integration (API, database, and service
  boundaries), security (headers, auth guards, input validation, rate limiting,
  upload rules, error leakage, secret scanning), and end-to-end (real user flows
  through a browser or client). Fixtures set up and tear down state
  deterministically.
- **Why.** Separating tiers keeps fast feedback fast (unit) while still covering
  real integrations and full flows. A named security tier makes security coverage
  explicit and auditable rather than incidental.
- **Verify anywhere.** Run each tier and produce a coverage report. Any runner
  works (`pytest`, `go test`, `cargo test`, `jest`/`vitest`, `rspec`) plus a
  browser driver (`playwright`, `cypress`, `selenium`) for end-to-end. Confirm the
  security tier exists as its own suite and runs in CI.
- **Example.** A tree with `tests/unit/`, `tests/integration/`,
  `tests/security/`, and `tests/e2e/`, where the security directory holds one file
  per concern (headers, auth guards, input validation, rate limiting, upload,
  error handling, no-hardcoded-secrets).

## 9. Regression tests document the bug they prevent

- **Principle.** Every fixed defect gets a regression test that names the original
  bug, the fix, and the issue or PR reference in its body.
- **Why.** A regression test turns each fixed bug into a permanent guardrail with
  documented history, so the next author sees why the check exists and does not
  reintroduce the defect.
- **Verify anywhere.** Review confirms a regression test accompanies each bug fix
  and that its body states the defect, the fix, and the reference.
- **Example.** A test named for the defect it prevents and marked `REGRESSION:`,
  whose body records the behavior the code produced before the fix, the change
  that corrected it, and the issue or pull-request reference.

## 10. CI is the merge gate

- **Principle.** Every push and pull request runs the full gate: deterministic
  install, lint, test, dependency audit, and build. A pull request cannot merge
  while the gate is red. Moderate-or-higher vulnerabilities fail the build.
  Commit messages follow a conventional shape.
- **Why.** Running the same gate on every change catches regressions at the
  earliest point and keeps the mergeable state honest, so the main branch stays
  deployable. A CI merge gate makes "green before merge" structural rather than
  discretionary. Conventional commits make history machine-readable.
- **Verify anywhere.** Review the CI config to confirm all stages run on push and
  pull request. Confirm the audit step fails at the chosen severity. Enable branch
  protection so merges require the CI check to pass. Add a commit-message linter.
- **Example.** A CI job runs checkout, deterministic install, lint, test, audit at
  the moderate threshold, and build; branch protection blocks merge until it
  passes. Any CI system expresses the same stages.

## 11. Validate environment at startup, fail fast

- **Principle.** The application declares its required environment variables and
  validates their presence and shape at startup, failing fast with a clear message
  if any are missing. A committed example env file documents every variable
  without values. Production imposes any additional cross-variable invariants.
- **Why.** Fail-fast at boot converts a class of runtime-in-production failures (a
  missing secret, an unset URL) into an immediate, obvious startup crash in any
  environment, before serving traffic. The example file is living documentation of
  the configuration surface.
- **Verify anywhere.** Boot the app with a required variable unset and assert it
  exits with a descriptive error, not a deep null-reference later. Confirm the
  example env file lists every required variable. Prefer a typed, schema-validated
  config loader (`envalid`, `pydantic-settings`, `viper`, `envconfig`).
- **Example.** Startup validates a declared list of required variables and throws
  `Missing required environment variable: <key>` on the first absent one.

## 12. Accessibility baseline

- **Principle.** Any UI meets a defined accessibility baseline: honor
  reduced-motion in both CSS and JavaScript animation loops, give every
  interactive element a visible keyboard focus indicator, enforce a minimum
  tap-target size, apply correct ARIA roles, labels, and states, and keep a
  single sequential heading hierarchy.
- **Why.** These are the concrete requirements behind WCAG conformance and real
  usability for keyboard, screen-reader, motor-impaired, and motion-sensitive
  users. They are also frequent regressions because they are invisible to a
  sighted mouse user, so they need explicit rules and checks.
- **Verify anywhere.** Automated scan (`axe`, `pa11y`, Lighthouse a11y,
  `eslint-plugin-jsx-a11y`) in CI, plus manual keyboard-only and screen-reader
  passes. Confirm reduced-motion stops JavaScript and canvas loops, not only CSS
  animation. Assert focus-visible styles, the minimum tap size, one `h1` per page,
  and no skipped heading levels.
- **Example.** A media query disables CSS animation under reduced motion, and each
  JavaScript animation loop checks the reduced-motion preference and renders a
  single static frame instead of starting a loop. The Web UI DoD profile
  (`core/dod/profiles.md`) enforces this per PBI.

## 13. Production readiness checklist

- **Principle.** The service exposes a health endpoint returning status and
  version, and a written checklist gates every deploy. An environment toggle
  disables development-only behavior (verbose errors, permissive CORS, debug
  logging) in production.
- **Why.** A health check gives orchestrators and canary monitors a single
  readiness signal. A checklist converts deployment knowledge into a repeatable
  gate so nothing security-relevant (headers, TLS, CORS, secrets, audit) is
  skipped under deadline pressure. The production toggle keeps development
  conveniences from leaking to production.
- **Verify anywhere.** Assert the health endpoint returns success with the
  expected shape. Walk the checklist as a pre-deploy sign-off and automate the
  automatable items (audit clean, tests pass, headers present). Test that
  production mode suppresses verbose errors and permissive CORS.
- **Example.** A checklist confirms all env vars set, production mode on, CORS
  restricted to the production domain, HSTS active, database TLS required, audit
  clean at the threshold, all tests passing, and the health check returning
  success.

## 14. Immutable audit trail for privileged actions

- **Principle.** Every privileged or moderation action is recorded to an
  append-only audit log capturing who acted, what action (a typed value, not free
  text), on what target, with context including source IP and a timestamp. The log
  has no delete path.
- **Why.** Privileged actions (ban, delete, role change) are high-impact and
  abuse-prone. An immutable trail supports incident investigation, accountability,
  and compliance, and deters insider misuse. Typed action values and composite
  indexes make the log queryable during an investigation.
- **Verify anywhere.** Confirm every privileged code path writes an audit record
  with the action. Confirm no API or admin path can delete or mutate audit records
  and test that a delete attempt fails or does not exist. Confirm the record
  captures actor, typed action, target, detail, IP, and timestamp.
- **Example.** An audit record carries an actor ID, a typed action enum, a target
  reference, a detail field, an IP, and a creation timestamp, indexed by actor,
  action, and time.

## 15. Consistent naming conventions

- **Principle.** Fix one casing convention per identifier context (files, types,
  functions, constants, routes, tests, environment variables, branches, commits)
  and apply it everywhere.
- **Why.** Consistent naming lowers cognitive load, makes greps and tooling
  reliable, and removes bikeshedding from review.
- **Verify anywhere.** Enforce with a linter or formatter and naming rules
  (`eslint`, `ruff`, `golangci-lint`, `rubocop`) plus a filename lint. Review
  rejects identifiers that violate the table.
- **Example.** Files kebab-case, types and components PascalCase, functions
  camelCase, constants upper-snake, environment variables upper-snake, branches
  `type/ID-desc`, commits conventional. The specific choices are conventions; the
  project picks one per context and enforces it.

## Cross-cutting lessons

These carry to any stack and inform how the standards above are applied.

1. **Deny-by-default, then allowlist with a written reason.** Applies to content
   policies, input validation, and origin restriction. Every relaxation is
   documented as tracked debt, not permanent policy.
2. **One enforced template per entry point.** Validated input plus request ID plus
   auth plus structured logging plus safe error handling is the minimum for every
   handler in any language.
3. **Make the safe path the default.** Auto-redacting loggers, framework
   auto-escaping, and fail-fast config all assume the author will forget and stay
   safe anyway.
4. **Turn every fixed bug into a documented regression test, and every privileged
   action into an immutable audit record.**
5. **Gate merges and deploys with automation, not discipline.** CI is the merge
   gate; a checklist gates deploy; a per-commit checklist gates history.
6. **Prefer typed and structured over free text** for enums, config, and audit
   actions; it buys type safety and query performance.

## Scope note

These standards are stack-neutral by design. Conventions specific to one product,
such as folder naming, design tokens, asset dimensions, or one-off infrastructure
configuration, are excluded because they do not generalize. One principle drawn
from that territory does generalize and is stated here: prefer changes that are
reviewable and reversible. Transport security (TLS everywhere, database TLS) is
treated as implied by the HSTS header in standard 13 and the production-readiness
checklist.
