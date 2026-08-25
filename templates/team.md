<!--
  TEMPLATE: team.md
  Instantiate to .scrum/team.md at stage 0 FOUNDING.
  Source of answers: setup/founding-interview.md (preferences) and
  setup/project-scan.md (codebase facts). The Retrospective may amend this file;
  log amendments in the last section. Keep it plain markdown, committed to the repo.
  Delete these comment blocks when you fill a section, or keep them as guidance.
-->

# Team charter

<!-- One line: the product or project name and the stakeholder (the human user). -->
- Project: <name>
- Stakeholder: <who the team serves; the customer>
<!-- Adapter values are adapter file basenames in scrum/adapters/, named for runtime capability rather than for a vendor; matches the Adapter field in .scrum/state.md. -->
- Adapter: <parallel-agents | terminal-agent | single-model>
- Founded: <YYYY-MM-DD>

## Communication
<!-- Founding interview area 1. Update length/tone; note if this is a default. -->
- Update style: <terse status | short narrative | full detail with reasoning>
- Vocabulary: <plain language | Scrum terms, defined on first use>
- Writing standard: core/artifact-writing-standard.md; load research-clinical-writing when discoverable
- Source: <stakeholder choice | default>

## Interruption tolerance
<!-- Area 2. Sets when the team stops to ask vs reports at Review. -->
- Batch non-blocking questions to the Review: <yes | no>
- Interrupt immediately for: product scope or intent, destructive or irreversible authority, or an ambiguity only the stakeholder can resolve
- Additional interrupt triggers: <stakeholder-specific, if any>

## Risk appetite
<!-- Area 3. Sets how boldly the team slices and sequences, and spike/experiment tone. -->
- Default lean: <proven and safe | moderate | bold, learn from failure>
- Take the riskiest assumption early when blast radius fits one Sprint: <yes | no>
- Areas that must stay conservative: <security, irreversible actions, data, ...>

## Quality bar vs speed
<!-- Area 4. The floor never drops; this sets the height above it and rough-ok areas. -->
- Never-drop floor: universal tier + security tier of the Definition of Done
- Bar above the floor: <floor only | plus stack profiles | strict project rules>
- Areas where a rough, labeled spike is acceptable: <list, or none>
- Feeds Tier 3 of .scrum/DEFINITION_OF_DONE.md

## Cadence
<!-- Area 5. Sets Sprint scope size and checkpoint frequency. -->
- Sprint length (one work cycle, one Sprint Goal): <a few hours | a day | ...>
- Review frequency: <end of each session | ...>
- Checkpoints per Sprint (adapted Daily Scrum): <between task batches>

## Definition of value
<!-- Area 6. At least one outcome measure beyond output. Forwarded to product-goal.md. -->
- Value the team optimizes for: <user-facing outcome, satisfaction, time-to-market, capability unlocked>
- How the stakeholder knows a cycle was worth it: <in their words>

## Technical constraints
<!-- Area 7 + project scan. Fixed elements bound the solution space; feed Tier 3. -->
- Language / framework / platform: <detected or stated>
- Hosting / deployment target: <...>
- Required or forbidden dependencies: <...>
- Data and compliance rules: <...>

## Engineering and specialist routes
<!--
  From the project scan. These are routing facts, not a universal choice for every
  PBI. Refinement evaluates the trigger again for each item.
-->
- Test topology: <unit | component | contract | integration | end-to-end | property | fuzz | static | visual/a11y | eval; commands and gaps>
- Default test-strategy note: choose per PBI under core/test-strategy.md; TDD is preferred for deterministic behavior and reproducible defects
- Threat-model artifacts and triggers: <paths and signals | none detected>
- AI-assisted development access: <available read/write/execute/network/deploy/secret capabilities and limits>
- Product AI/agent use: <yes, select AI/LLM profile | no>
- Private-source and scratch-data controls: <safe ignored location; tracked-file findings; never record private filenames or paths here>
- UI/UX route: <ux-fit when triggered | fallback when triggered | n/a>
- Design Brief and design-system evidence: <project paths | none detected>

## Review evidence
<!-- Area 8. Sets what each done PBI must return and what the Review records. -->
- Required evidence per PBI: <runnable result | test output | screenshots | walkthrough | command output>
- Stakeholder drives the demo: <yes | no>

## Staffing
<!--
  Area 9. Which model tier fills each seat. Places judgment where it pays and
  cheap capacity where it does not. Realized by the adapter in scrum/adapters/.
  Adaptation: a senior Developer is a skill distribution inside the single
  Developers accountability, not a new role or title. The Scrum Guide (2020)
  defines no sub-roles or titles inside Developers.
-->
- Tiers available in this runtime: <what the stakeholder can actually run>
- Orchestrator, PO, and SM tier: <default: the strongest available model>
- Developer tier: <default: mid-tier worker models>
- Senior Developer: <on | off> (default: on when a stronger tier exists, off in a single-tier runtime)
- Senior Developer tier: <the strongest available model when on; n/a when off>
- Verifier tier: at least the implementer's tier, never weaker; the strongest available for security-sensitive or irreversible work
- Capability registry:
  - <agent or labeled pass>: <domain/subsystem capabilities>; <available authority and tools>; <diagnostic strength>
- Recovery selection: required authority and capability, then diagnostic strength, model tier, and cost

## Delivery mode
<!--
  Area 10. How each increment lands. Absorbs the older Auto-commit setting:
  Auto-commit: on maps to commit, Auto-commit: off maps to stage-only.
-->
- Mode: <commit | branch-pr | stage-only>
  - commit (default): the team commits `.scrum/` and the code increment together.
  - branch-pr: the team works on a branch and delivers a pull request; it never merges without the stakeholder.
  - stage-only: the team stages its changes and reports them; the stakeholder commits.
- Branch and pull-request convention (branch-pr only): <naming, target branch>
- Start from a clean working tree in every mode, so a commit or a delivered diff carries only the increment.

## Stack profiles selected
<!-- From core/dod/profiles.md, chosen at founding. The AI/LLM profile applies if the product calls models. -->
- <Web UI | API/service | Library | CLI | AI/LLM | ...>

## Detected commands (project scan)
<!-- From setup/project-scan.md. The DoD gate runs these real commands. Mark absent categories. -->
- Build: <command | absent>
- Test: <command | absent>
- Lint: <command | absent>
- Typecheck: <command | absent>
- Format: <command | absent>
- Package manager / environment: <...>

## CI gates (project scan)
<!-- Each becomes a Tier 3 DoD item. The team's DoD is at least as strict as CI. -->
- <check: required | advisory> (source: <path>)

## Existing standards files (project scan)
<!-- Quote by path; their testable rules become Tier 3 items, never weakened. -->
- <path>: <rules extracted>

## Working agreement
<!-- Founding-interview norms. Keep to a handful of lines the team follows. -->
- Honest reporting: failed output is reported verbatim, never smoothed over.
- Ask for help early: blockers reach impediments.md with a clear ask.
- Bounded attempts: one hypothesis per mutation; pause on repeated failure,
  exhausted budget, or a no-progress batch and preserve the blocker packet.
- Evidence over claims: no "done" without gate evidence.
- Routed context: load exact stage and triggered modules; never replace canonical
  rules with a generated summary or silent truncation.
- Artifact quality: outcome first, clear actors and actions, evidence-calibrated detail, available citations, no AI filler.
- Adaptive tests: record the selected verification route and why it fits; do not force TDD where another method answers the claim better.
- AI boundaries: generated work is untrusted; minimum authority, private-data limits, approval gates, and stop conditions belong in every brief.
- The floor holds: universal and security tiers are never lowered for a deadline.
- Version control: the Delivery mode section above governs how each increment lands. A project written before that section used `Auto-commit: <on | off>`; `on` maps to `commit` and `off` maps to `stage-only`.
- <stakeholder-specific norm, in their words>

## Amendments log
<!-- The Retrospective may change any answer above. Record what changed and which Sprint. -->
- <YYYY-MM-DD, sprint-NNN>: <what changed and why>
