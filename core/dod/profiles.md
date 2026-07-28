# Definition of Done: Tier 2 stack profiles

Tier 2 holds the Definition-of-Done criteria that depend on what kind of thing a
PBI ships. A web page has accessibility duties a library does not; a library has
versioning duties a CLI does not; a feature built on a foundation model has
evaluation and guardrail duties none of the others have. This file defines one
profile per stack type. Tier 0 and Tier 1 (universal and security) live in
`core/dod/definition-of-done.md` and always apply on top of whatever profiles are
selected.

## Selecting profiles at setup

Profiles are chosen at stage 0 FOUNDING and recorded in `.scrum/team.md`.
`setup/project-scan.md` detects the stack; `setup/founding-interview.md` confirms
it with the stakeholder. More than one profile can apply: a service that ships
both a browser UI and a JSON API selects Web UI and API/service. A feature built
on a foundation model selects AI/LLM in addition to whatever hosts it (an
AI-backed web app is Web UI plus AI/LLM). The selected profiles are flattened
into `.scrum/DEFINITION_OF_DONE.md` alongside Tier 0, Tier 1, and Tier 3.

Apply a profile per PBI by relevance: a PBI that changes no UI does not trigger
Web UI items, so those items are marked `n/a` with that reason at the gate. The
gate protocol, the `n/a`-with-reason rule, and the evidence rules are in
`core/dod/definition-of-done.md`. Each item below is a checklist entry with
verify guidance. The fuller engineering reference behind the Web UI, API/service,
Library, and CLI profiles is `core/engineering-standards.md`.

## Profile: Web UI

For any PBI that renders or changes a browser-facing interface. Reference:
`core/engineering-standards.md`, accessibility baseline and production readiness.

- [ ] **Visible keyboard focus.** Every interactive element shows a focus
  indicator on keyboard navigation. Verify: keyboard-only pass over the changed
  UI; confirm a focus-visible style on each control.
- [ ] **ARIA roles, labels, and states.** Interactive and dynamic elements carry
  correct roles, labels, and states (toggle buttons expose label and expanded
  state; navigation landmarks are labeled; decorative graphics are hidden from
  assistive tech). Verify: automated a11y scan (`axe`, `pa11y`, Lighthouse a11y,
  `eslint-plugin-jsx-a11y`) plus a screen-reader spot check. Do not use a dialog
  role for a navigation panel.
- [ ] **Tap-target size.** Interactive targets meet the minimum touch size
  (44x44 px, WCAG 2.5.5), set via size or padding. Verify: measure changed
  controls; assert minimum dimensions.
- [ ] **Heading hierarchy.** One `h1` per page; heading levels descend without
  skipping. Verify: automated scan or a manual outline check of the changed page.
- [ ] **Reduced motion honored.** Animation respects the reduced-motion
  preference in both CSS and any JavaScript or canvas animation loop. Verify: set
  the OS reduced-motion preference and confirm animation stops, including
  script-driven loops that CSS cannot disable.
- [ ] **Responsive layout.** The UI works across the supported viewport range
  with no horizontal overflow or clipped content. Verify: check the change at
  mobile, tablet, and desktop widths.
- [ ] **Page metadata.** Each route sets at least a title, and any per-page
  metadata the project requires. Verify: load the route and confirm the title and
  metadata render.

## Profile: API/service

For any PBI that ships or changes a network service (HTTP API, RPC, realtime
backend). Reference: `core/engineering-standards.md`, handler template, request
tracing, error handling, and production readiness.

- [ ] **Health endpoint.** The service exposes a health check returning a success
  status and the running version. Verify: call the health route; assert 200 and
  the expected shape.
- [ ] **Request IDs.** Every request receives a unique correlation ID that
  appears in all its log lines, in a response header, and in any error body.
  Verify: force an error; confirm the same ID appears in the response and the
  logs.
- [ ] **Structured logging.** Handlers log through the structured logger, never
  raw print, with sensitive-field redaction on. Verify: grep changed handlers for
  raw-print calls; confirm log lines are structured and redacted.
- [ ] **Graceful errors.** Every handler funnels failures through a shared error
  handler that maps known errors to typed responses and returns a generic body
  with a request ID on unexpected failure. Verify: drive validation-error and
  server-error paths; assert typed 4xx and generic 5xx with no internal detail.
- [ ] **Input contract enforced.** Each endpoint validates its request against a
  schema and rejects malformed input with a clear client error. Verify:
  integration test sending an invalid body asserts a 400 with validation detail.
  (This overlaps Tier 1.1; record evidence once and reference it.)

## Profile: Library

For any PBI that ships or changes a package other code imports. Reference:
`core/engineering-standards.md`, exact dependency pinning and consistent naming.

- [ ] **Semantic versioning.** The version bump matches the change type: patch for
  fixes, minor for additive changes, major for breaking changes. Verify: compare
  the public surface before and after; confirm the bump matches.
- [ ] **Public API documented.** Every exported symbol has documentation covering
  its purpose, parameters, and return. Verify: run the doc generator or lint;
  confirm no undocumented public export.
- [ ] **Runnable examples.** At least one example exercises new or changed public
  behavior and runs as part of the test or doc build. Verify: execute the example;
  confirm it passes against the current version.
- [ ] **No unannounced breaking changes.** A breaking change to the public API is
  reflected in a major version bump and a changelog entry describing the break and
  its migration. Verify: diff the public surface; confirm removals and signature
  changes are announced.
- [ ] **Changelog updated.** The changelog records the change under the new
  version. Verify: confirm the entry exists and names the change.

## Profile: CLI

For any PBI that ships or changes a command-line interface. Reference:
`core/engineering-standards.md`, error handling and structured output.

- [ ] **Help text.** Every command and subcommand responds to `--help` with usage,
  options, and a description. Verify: run `--help`; confirm it lists the changed
  options.
- [ ] **Exit codes.** The command exits 0 on success and a documented non-zero
  code on failure; distinct failure classes use distinct codes where the project
  defines them. Verify: test the success and each failure path; assert the exit
  code.
- [ ] **stdin/stdout/stderr contract.** Primary output goes to stdout in the
  documented format; diagnostics and errors go to stderr; the command reads stdin
  where it advertises a pipe interface. Verify: pipe input and redirect streams;
  confirm output and error separation.
- [ ] **Machine-readable output where advertised.** If the command offers a
  structured output mode (JSON or similar), that output is valid and stable.
  Verify: parse the structured output; assert it validates.
- [ ] **Non-interactive safe.** The command does not block on a prompt when run
  without a TTY, or it fails with a clear message. Verify: run it piped or in a
  script context; confirm it does not hang.

## Profile: AI/LLM

For any PBI whose behavior is produced by a foundation model (an LLM or other
generative model). This profile stacks on top of the profile that hosts the
feature.

**Adaptation:** foundation-model output is open-ended and probabilistic, so
correctness cannot be read off the diff the way a pure function can. This profile
substitutes evaluation, guardrails, and monitoring for the certainty that code
review gives deterministic code.

### Core AI/LLM criteria

- [ ] **Evals defined before build and passing before ship.** Evaluation criteria
  and methods were written before the feature was built, each mapped to a concrete
  method, a dataset, and the product or business metric it protects. Results are
  sliced by input subgroup, not only averaged, and the sample size is justified.
  Verify: the eval set exists, ran, and passes its thresholds; confirm subgroup
  slices and a stated sample-size basis.
- [ ] **Prompts versioned and externalized.** Prompts live outside application
  code, each with metadata (identifier, version, target model, date, author,
  intended use), are version-controlled, and have their own test cases evaluated
  independently of surrounding code. A prompt change is evaluated against a fixed
  eval set in whole-system context before merge. Verify: locate the prompt store;
  confirm a result can be traced to the exact prompt version that produced it.
- [ ] **Model and version pinned.** The specific model version is pinned in config
  by a date-stamped or hashed identifier, not a floating alias. A regression check
  runs when the provider updates the model or the version changes, and a rollback
  path to the prior pinned version exists. Verify: read the pinned identifier;
  confirm the regression check and the rollback path.
- [ ] **Input guardrails and injection defenses.** Inputs are scanned for
  sensitive data before any prompt leaves the organization; detected spans are
  blocked or masked with a reversible map so responses can be restored without
  sending raw sensitive data outward. Defenses against prompt extraction,
  jailbreaking and injection, and information extraction exist at model, prompt,
  and system levels, and an instruction hierarchy (system outranks user, user
  outranks tool and model output) is enforced so injected instructions in
  retrieved or tool content stay lowest priority. Verify: test that a
  known-sensitive input is masked or blocked, and that a known injection attempt
  does not override the system instruction.
- [ ] **Output guardrails.** Outputs are screened for malformatted results,
  hallucination or factual inconsistency, toxic content, leaked private data, and
  brand-risk content, and each failure mode has a defined handling policy. The
  streaming-mode gap (unsafe tokens can reach the user before a guardrail
  decides) is acknowledged where streaming is used. Verify: drive each failure
  mode; confirm the policy fires.
- [ ] **Guardrails measured both ways.** Guardrail effectiveness tracks both the
  violation rate (unsafe outputs that slip through) and the false-refusal rate
  (legitimate requests wrongly blocked). An over-blocking system is a defect.
  Verify: both rates are instrumented and within target.
- [ ] **Generated actions gated.** Generated code runs only in isolation
  (a sandbox), and any impactful, write, or irreversible action requires explicit
  human approval. Verify: confirm the sandbox and the approval gate on write
  actions.
- [ ] **Cost and latency budgets.** A latency service-level objective is defined
  as time-to-first-token and time-per-output-token (or total latency), tracked at
  percentiles (p50, p90, p95, p99) rather than averages, and a per-request cost
  budget (input plus output tokens, cache hit rate) is tracked. Goodput (requests
  meeting the objective), not raw throughput, is the health target. Verify: the
  budgets exist and the metrics report at percentiles.
- [ ] **Caching scoped safely.** Any cache is chosen deliberately and cannot serve
  a user-specific or time-sensitive answer to a different user; it has an eviction
  policy and a lifetime rule. A semantic cache, if used, has a validated
  similarity threshold and a measured hit rate. Verify: confirm cache keys and
  scoping; test that a user-scoped response is not returned to another user.
- [ ] **Fallback on model failure.** A retry policy handles empty and malformed
  responses with an explicit cap and awareness of its latency and cost impact. A
  gateway falls back on rate limits and provider outages (alternate model, retry,
  or graceful degradation) so one provider failure does not take the feature down.
  A human-handoff path exists with defined triggers. Verify: simulate an empty
  response, a provider error, and a handoff trigger; confirm each path fires.
- [ ] **PII and data-privacy handling.** Personal and sensitive data is handled on
  both inputs and outputs, copyright and PII exposure through generated output is
  checked, and any user feedback captured is governed as user data with disclosure
  of how it is used. Verify: confirm the input and output PII checks and the
  feedback-data governance.
- [ ] **Monitoring hooks.** Mean time to detection, mean time to response, and
  change failure rate are computable for the feature. Quality, safety, cost,
  latency, and behavior metrics are instrumented and broken down by user, release,
  prompt version, and time. The system logs configuration, prompt template, final
  prompt, inputs, intermediate and final outputs, and tool calls, each tagged with
  a correlating ID, and distributed tracing can follow any request to the exact
  failing step. Drift detection covers system-prompt changes, user-behavior
  shifts, and undisclosed provider-side model changes, and monitoring findings
  feed back into the eval set. Verify: trace one request end to end; confirm the
  metrics, logs, and drift checks exist.

### Conditional sub-checklists

Add these only when the feature uses the pattern named.

**If the feature uses retrieval-augmented generation (RAG):**
- [ ] Retriever and generator are evaluated separately and end to end; retrieval
  quality is measured with context precision and context recall against a labeled
  set; chunking, reranking, query rewriting, and hybrid search are recorded
  configurations, not hidden defaults; the generated response is checked for local
  factual consistency with the retrieved context; a wrong answer is attributed to
  retrieval versus generation. Verify: the retrieval metrics exist and a failed
  answer is traceable to its cause.

**If the feature is an agent (tools, planning, or a loop):**
- [ ] Planning failures are tested (invalid tool, bad parameters, wrong values,
  goal failure, reflection error, budget overrun); tool outputs are validated
  before use; each tool is tested independently; a step, time, or token budget
  bounds the loop; efficiency (steps, tokens, wall-clock per task) is measured
  against a baseline, not only success rate. Verify: the budget enforces, tool
  errors are caught, and efficiency is reported.

**If the feature was fine-tuned:**
- [ ] The failure was diagnosed as behavior-based (form and style), not
  information-based (missing or outdated facts, which RAG fixes), before
  fine-tuning; cheaper adaptation rungs (prompting, few-shot, RAG) were shown
  insufficient first; the approach was validated on a small dataset before scaling
  data; a regression against general-capability evals checks for capability loss;
  the technique and any quantization are recorded with their trade-offs, and a
  serving and maintenance plan exists. Verify: the diagnosis, the ladder evidence,
  and the regression result exist.

**If the feature ships or depends on a curated dataset:**
- [ ] Data is checked for relevance, task alignment, annotator consistency,
  correct formatting, deduplication, and compliance; coverage spans the expected
  production input distribution with gaps documented; the pipeline runs inspect,
  deduplicate, clean and filter (including PII and toxicity removal), and format
  to the model's template; synthetic data is verified before use. Verify: the six
  quality checks and the pipeline steps ran.

## Note on numeric thresholds

The specific numbers in this file (44x44 px tap targets, the p50/p90/p95/p99
percentile set) are illustrative defaults. A project sets its own service-level
objective targets in Tier 3 and records them in `.scrum/team.md`. The rule is
that the target exists and is measured, not that it equals a particular number.
