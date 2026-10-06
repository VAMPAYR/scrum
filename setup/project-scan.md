# The project scan

The project scan runs at stage 0 FOUNDING, alongside the founding interview
(`setup/founding-interview.md`), and again whenever `/scrum dod` re-instantiates
the Definition of Done. It detects an existing project's stack, its test, lint,
and build commands, its CI gates, and its existing standards files, then merges
those findings into Tier 3 of the Definition of Done. The founding interview
captures the stakeholder's preferences; the scan captures the codebase's facts.

The governing rule comes from the Scrum Guide (2020) rules for the Definition of
Done: where an organization already has a standard, that standard is the minimum
the team works to, and the team may only add to it. Existing org standards are a
floor. The scan never weakens a detected standard; it records it and lets the
team strengthen it.

## What the scan produces

- A stack profile: language, framework, platform, and package manager, used to
  select stack profiles in `core/dod/profiles.md`.
- The project's own commands for build, test, lint, typecheck, and format, so the
  Definition of Done gate runs real commands rather than generic guidance.
- The list of CI gates that already block a merge, so the team's DoD never falls
  below what CI already enforces.
- The set of existing standards files, quoted by path, so their rules become Tier
  3 DoD items.
- The existing test topology and the best initial route for deterministic,
  legacy, boundary, integration, UI, and model-driven work. The scan records
  capability; it does not force one method onto every PBI.
- A risk and specialist map: trust boundaries, sensitive data, privileged or
  autonomous actions, model use, threat-model artifacts, design briefs, design
  systems, and user-facing surfaces.
- A privacy check for local source material and generated scratch data: where it
  lives, whether the relevant ignore rules cover it, and whether any private path
  or extract is already tracked.
- A merge report written into `.scrum/team.md` and into Tier 3 of
  `.scrum/DEFINITION_OF_DONE.md` via `core/dod/definition-of-done.md`.

## Procedure

The scan is read-only detection. Read files and, where a command is needed to list
configuration, run only non-mutating commands (listing scripts, printing a config,
checking a tool version). Do not install, modify, or run build or test steps
during the scan; that happens later, inside the Definition of Done gate.

### Step 1: detect the stack

Identify the language and framework from manifest and lock files at the repo root
and in obvious subdirectories. Read each manifest to understand its contents; the
detection is grounded in file contents.

| Signal file | Indicates | Read for |
|---|---|---|
| `package.json` (+ `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`) | Node or a JS/TS framework | `scripts`, `dependencies`, `packageManager`, `engines` |
| `pyproject.toml`, `setup.cfg`, `requirements*.txt`, `poetry.lock`, `uv.lock` | Python | build backend, dependency groups, tool config |
| `Cargo.toml` (+ `Cargo.lock`) | Rust | `[package]`, `[dependencies]`, workspace members |
| `go.mod` (+ `go.sum`) | Go | module path, Go version, requirements |
| `pom.xml`, `build.gradle`, `build.gradle.kts` | Java or Kotlin (Maven/Gradle) | plugins, dependencies, test config |
| `Gemfile`, `composer.json`, `*.csproj`, `*.sln`, `mix.exs` | Ruby, PHP, .NET, Elixir | dependencies and scripts |
| `Dockerfile`, `docker-compose.yml`, `*.tf`, `k8s/`, `helm/` | Containerized or infrastructure targets | base images, services, provisioned resources |

Record the framework as well as the language: a `package.json` with `next` implies
a Web UI profile; one exposing a `bin` field implies a CLI profile; a service with
an HTTP server implies an API profile. Map the detected type to the stack profiles
in `core/dod/profiles.md`. If the product uses models or LLM calls, select the
AI/LLM profile.

### Step 2: extract build, test, lint, typecheck, and format commands

Prefer the project's declared commands over generic ones, so the gate runs what
the project already uses.

- **Node:** read `package.json` `scripts`. Map common names: `build`, `test`,
  `lint`, `typecheck` (or `tsc --noEmit`), `format` (Prettier), and any `test:*`
  variants. Note the package manager from the lockfile.
- **Python:** read `pyproject.toml` and `setup.cfg` for the test runner (`pytest`),
  linter and formatter (`ruff`, `flake8`, `black`, `isort`), and type checker
  (`mypy`, `pyright`). Note the environment tool (`poetry`, `uv`, `pip`).
- **Rust:** `cargo build`, `cargo test`, `cargo clippy`, `cargo fmt --check`.
- **Go:** `go build ./...`, `go test ./...`, `go vet ./...`, `gofmt` or
  `golangci-lint`.
- **Java/Kotlin:** the Maven or Gradle lifecycle: compile, `test`, and any
  configured lint (Checkstyle, Spotless, ktlint).
- **Other stacks:** read the manifest's task or script section and record the
  equivalents.

Where a category has no command, record it as absent. An absent test or lint
command is a Tier 3 finding: the team may add one, and its absence is visible to
the Definition of Done gate rather than silently skipped.

### Step 3: detect CI gates

Read the CI configuration to list the checks that already block a merge. These are
the enforced floor: the team's Definition of Done must cover at least what CI
already requires (`core/engineering-standards.md`, CI as a merge gate).

| CI system | Config location | Read for |
|---|---|---|
| GitHub Actions | `.github/workflows/*.yml` | jobs, required steps, matrix, branch protections referenced |
| GitLab CI | `.gitlab-ci.yml` | stages and jobs |
| CircleCI | `.circleci/config.yml` | workflows and jobs |
| Azure Pipelines | `azure-pipelines.yml` | stages and steps |
| Jenkins | `Jenkinsfile` | stages |
| Pre-commit | `.pre-commit-config.yaml` | hooks that run before commit |

Extract each gating check (test suite, lint, type check, security scan, coverage
threshold, build) and record it. Note whether the gate is required or advisory
where the config states it. If branch protection rules are visible, note which
checks are required to merge.

### Step 4: detect existing standards files

Locate documents that already state how the project must be built. Quote them by
path; their rules become Tier 3 DoD items and are not weakened.

- Engineering or coding standards: `ENGINEERING_STANDARDS.md`, `CODING_STANDARDS.md`,
  `STYLEGUIDE.md`, `docs/standards/*`.
- Contribution rules: `CONTRIBUTING.md`, pull-request and issue templates under
  `.github/`.
- Editor and tool config that encodes rules: `.editorconfig`, `.eslintrc*`,
  `.prettierrc*`, `ruff.toml`, `.golangci.yml`, `tsconfig.json` strictness flags.
- Security and dependency policy: `SECURITY.md`, `.github/dependabot.yml`,
  renovate config, `CODEOWNERS`.
- Architecture and decision records: `ARCHITECTURE.md`, `docs/adr/*`.

For each file found, extract the rules that are testable as Definition of Done
items (a required review, a coverage threshold, a naming or structure rule, a
security policy). Record the source path with each rule so its provenance is
traceable.

### Step 5: map test, security, AI, privacy, and UI/UX signals

Read configuration and existing artifacts to route later work correctly.

- **Test topology.** Identify unit, component, contract, integration, end-to-end,
  property, fuzz, static-analysis, visual, accessibility, performance, and model
  evaluation suites. Record commands, environments, fixtures, skipped or flaky
  tests, and any coverage rule. Do not treat a coverage percentage as proof.
- **Security model.** Locate threat models, data-flow diagrams, architecture
  records, data classifications, abuse cases, security tests, incident notes, and
  deployment boundaries. Record obvious entry points, stores, external services,
  privileged actions, and trust boundaries. Do not claim the scan itself is a
  complete threat model.
- **AI use.** Distinguish AI-assisted development from a product that calls a
  model or agent. For development agents, record available read, write, execute,
  network, deployment, and secret access so briefs can apply least privilege.
  Combine these facts with the founding interview's capability registry; never
  infer domain expertise from model tier alone. For product AI, select the AI/LLM
  profile and trigger threat modeling where the architecture warrants it.
- **Private material.** Check ignore files and tracked-file lists for source PDFs,
  books, exports, credentials, personal data, local absolute paths, and temporary
  extracts. Record only the category and safe location in public artifacts, not a
  private filename or path. An ignored file that was previously tracked remains a
  finding.
- **UI and UX.** Detect browser or app surfaces, component libraries, design
  tokens, design-system rules, screenshots, prototypes, usability evidence, and a
  Design Brief. Record whether `core/ux-integration.md` should route relevant
  PBIs to the standalone `ux-fit` skill or its fallback.

Write these findings into `.scrum/team.md` under Engineering and specialist
routes. Re-evaluate the route per PBI during refinement; a repository-level
signal does not make every item security-sensitive or design-sensitive.

### Step 6: merge into Tier 3, as a floor

Combine the findings into Tier 3 of the Definition of Done under the floor rule.

1. Every detected CI gate becomes a Tier 3 DoD item. The team's DoD is at least
   as strict as CI. It may add items CI does not enforce; it may not drop one CI
   enforces.
2. Every rule extracted from a standards file becomes a Tier 3 item, attributed to
   its source path. If two sources conflict, keep the stricter rule and note the
   conflict for the stakeholder.
3. The detected commands populate the "how to verify" for the universal tier: the
   gate runs `build`, `test`, `lint`, `typecheck`, and `format` using the
   project's own commands (`core/dod/definition-of-done.md`).
4. Where the founding interview stated a constraint the scan confirms, mark it
   detected. Where the interview and the scan conflict, resolve with the
   stakeholder before writing the DoD; a stated preference does not weaken a
   detected standard.
5. Write the merge report into `.scrum/team.md` (detected stack, commands, CI
   gates, standards files, test topology, risk signals, privacy findings, and
   specialist routes) and the Tier 3 items into `.scrum/DEFINITION_OF_DONE.md`.

Record what was detected and what was absent. An absent category is a finding, not
a silent gap: the DoD gate marks an unverifiable item `n/a` with a reason, never
skips it (`core/dod/definition-of-done.md`).

## Existing products

When the scan runs against an established codebase, it also maps the product as it
stands, so the backlog and the Definition of Done start from what is already there.
This runs alongside the founding steps above.

- **Map modules and entry points.** List the top-level modules with their
  responsibilities and the entry points (executables, servers, CLI commands,
  exported packages), so the Product Owner and Developers can see the product's
  shape before ordering work.
- **Harvest work already recorded.** Collect `TODO` and `FIXME` markers, open
  issues in the tracker, and failing or skipped tests. Each is a candidate Product
  Backlog Item the Product Owner triages into `product/backlog.md`
  (`core/roles/product-owner.md`), not a task the scan acts on.
- **Record the current commands.** Capture the project's test, lint, and CI
  commands as they run today (Steps 2 and 3), so the Definition of Done gate runs
  what the product already runs.
- **Treat existing standards docs as the floor.** Standards, contribution rules,
  and architecture records already in the repo set the Tier 3 minimum under the
  floor rule (Steps 4 and 6). The team may strengthen them, never weaken them.

Record these findings in `.scrum/team.md` beside the merge report, so the Product
Owner picks them up at vision and refinement.

## Greenfield projects

If the scan finds no manifest, no CI, and no standards files, the project is
greenfield. Record that plainly and do not invent a stack.

1. Note that no existing standard was found, so there is no external floor beyond
   the universal and security tiers.
2. Take the intended stack from the founding interview's technical-constraints
   answer, or defer the stack decision to the Product Owner and Developers at
   vision and planning.
3. When the Developers establish build, test, and lint commands during the first
   Sprint, record them and re-run step 6 to populate Tier 3. Re-running
   `/scrum dod` refreshes the Definition of Done as the stack takes shape.

A greenfield project has the universal and security tiers as its floor from the
first Sprint; those never wait for detection.

## Re-scanning

Re-run the scan when the stack changes, when CI gates are added, or when
`/scrum dod` is invoked. The scan is idempotent: it re-detects and re-merges,
strengthening Tier 3 where new standards appear and never dropping a rule a prior
scan recorded unless the source that defined it was removed and the stakeholder
confirms the removal.
