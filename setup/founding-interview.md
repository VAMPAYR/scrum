# The founding interview

The Scrum Master runs this interview once per project, at stage 0 FOUNDING,
before any product vision or code. It captures how the stakeholder wants the team
to work: communication style, interruption tolerance, risk appetite, the quality
bar against speed, cadence and session length, the definition of value, technical
constraints, review-evidence preferences, staffing, and delivery mode. The
answers persist to
`.scrum/team.md` using `templates/team.md`, and they shape team behavior for the
whole project.

This interview captures *how the team works*. It does not capture *what to build*.
The product vision is the Product Owner's interview at stage 1, driven from
`core/roles/product-owner.md`. Keep the two separate so the stakeholder is not
asked to design the product before the team knows how to operate.

Run it alongside the project scan (`setup/project-scan.md`), which detects
existing stack, commands, CI, and standards. The scan supplies facts about the
codebase; this interview supplies the stakeholder's preferences. Both feed
`team.md` and the instantiated Definition of Done.

## Scrum Master stance for the interview

The Scrum Master facilitates; it does not lecture. Create the container and let
the stakeholder fill it with content. Teach the "why" behind each question in a
sentence so the stakeholder answers with understanding rather than guessing.

- **Container, not content.** Ask the question, give the one-line reason it
  matters, then wait. Silence after a question is the stakeholder thinking, not a
  cue to fill the gap.
- **Meet them a half-step ahead.** Offer a sensible default with each question so
  a stakeholder new to Scrum can accept it and move on, and an experienced one can
  override it. Do not present ten options; present a default and the axis it sits
  on.
- **Teach the trade-off, do not decide it.** Several questions set a real
  trade-off (speed against quality, autonomy against interruption). Name both
  sides and let the stakeholder choose. Record the choice; do not overrule it.
- **A task orientation, kept short.** A good start-up is a focused pass, not a
  workshop. Ask the ten areas below, confirm the norms, and hand off to vision.
  Do not expand the interview into product design.

If the stakeholder wants to skip the interview, run the defaults, write them to
`team.md` marked as defaults, and note that the Retrospective can amend any of
them later. A Sprint's worth of real behavior is better evidence than a long
up-front questionnaire.

## The question sequence

Ask the ten areas in order. Each area gives the question to ask, why it matters,
how the answer changes team behavior, a default to offer, and the field it lands
in inside `team.md`. Record the stakeholder's own words where they are specific;
paraphrase to the field where they are not.

Do not add a methods questionnaire. The project scan detects test, security, AI,
privacy, and UI/UX signals. Developers then select TDD or another verification
route per PBI under `core/test-strategy.md`. Ask the stakeholder only when a
missing product constraint, risk owner, or design choice would materially change
the result.

### 1. Communication style

**Ask:** "How do you want the team to talk to you during the work: terse status
lines, short narrative updates, or full detail with reasoning? And how much Scrum
vocabulary do you want, versus plain language?"

**Why it matters:** Transparency requires artifacts that are visible *and*
understood. An update the stakeholder does not read is not transparent. Matching
the register keeps communication effective.

**How it changes team behavior:** Sets the default length and tone of checkpoint
notes, Review summaries, and escalation messages. A terse preference tightens the
Review to evidence and decisions; a detailed preference expands rationale in
briefs and reviews. Length preference does not weaken
`core/artifact-writing-standard.md`: every artifact still leads with the outcome,
uses clear actors and actions, calibrates uncertainty, cites available evidence,
and removes generic filler. The team also applies any project writing guide named
in `.scrum/team.md`.

**Default:** Short narrative updates, plain language, Scrum terms defined on first
use, with the package writing standard applied.

**Lands in:** `team.md` > Communication.

### 2. Interruption tolerance

**Ask:** "During a work cycle, when should the team stop and ask you, and when
should it keep going and report at the Review? Do you want to be pinged as
questions arise, or batched?"

**Why it matters:** Focus is a Scrum value: agents work the Sprint Goal and are
not pulled off it needlessly. The Orchestrator batches interruptions so the team
stays on the goal, and only breaks in for scope or product-intent decisions,
destructive authority, or an ambiguity only the stakeholder can resolve
(`core/stall-recovery.md`, STALL-8).

**How it changes team behavior:** Sets the interruption threshold. A low
tolerance means the team batches non-blocking questions to the Review and
escalates only the three reserved cases. A high tolerance means the team asks
sooner. It also sets how aggressively the team self-resolves impediments before
escalating (`core/anti-patterns.md`, check S4.10).

**Default:** Batch non-blocking questions to the Sprint Review; interrupt only for
scope or product-intent decisions, destructive or irreversible authority, or an
ambiguity only the stakeholder can resolve.

**Lands in:** `team.md` > Interruption tolerance.

### 3. Risk appetite

**Ask:** "When the team faces a choice between a safe, proven approach and a
faster or bolder one that might fail, which way should it lean by default? How do
you feel about the team trying something and learning from a failed experiment?"

**Why it matters:** Scrum reduces risk by containing each experiment to a single
Sprint. A Sprint cannot end in failure in the strict sense, because the team
always produces a Done Increment or a lesson. A team afraid of any failure selects
only easy, low-value work, which is itself a process-decay sign
(`core/anti-patterns.md`, Area 3).

**How it changes team behavior:** Sets how boldly the team slices and sequences
work. High appetite means the team may tackle the riskiest assumption first to
learn early. Low appetite means the team de-risks with spikes and proven patterns
and keeps the blast radius small. It also sets the tone of the Retrospective:
whether experiments are named honestly or renamed to hide uncertainty
(`core/anti-patterns.md`, check S3.6).

**Default:** Moderate: take the riskiest assumption early when the blast radius is
contained to one Sprint, and prefer proven approaches for irreversible or
security-sensitive work.

**Lands in:** `team.md` > Risk appetite.

### 4. Quality bar against speed

**Ask:** "When speed and quality pull against each other near the end of a cycle,
which gives? Is there a floor of quality you never drop, and are there areas where
a rough first version is fine to learn faster?"

**Why it matters:** The Definition of Done is the quality commitment, and it is
never weakened to hit a deadline; cutting it hides the true state of the
Increment. Yet the *height* of the bar above the floor is a legitimate stakeholder
choice. If the organization already has a standard, it is the minimum and the team
may only add to it.

**How it changes team behavior:** Sets the height of the Definition of Done above
its universal and security floor, and which stack profiles apply
(`core/dod/definition-of-done.md`, `core/dod/profiles.md`). A high bar adds
profile tiers and stricter project rules; a speed lean keeps the bar at the floor
and marks rough areas as explicit throwaway spikes. The floor itself does not
move: builds pass, tests pass, no secrets, errors handled at boundaries.

**How it changes team behavior, continued:** This answer is a direct input to the
instantiated `.scrum/DEFINITION_OF_DONE.md`. Record the never-drop floor and any
areas where a rough version is acceptable, so the DoD gate applies the right bar
per PBI.

**Default:** Hold the universal and security tiers as an unmovable floor; set the
stack-profile tier to match the product type; allow clearly labeled throwaway
spikes to move faster with a lower bar, never merged as product.

**Lands in:** `team.md` > Quality bar, and into Tier 3 of
`.scrum/DEFINITION_OF_DONE.md`.

### 5. Sprint cadence and session length

**Ask:** "How long is one work cycle for you: a single session of a few hours, a
day, or longer? And how often do you want to come back for a Review?"

**Why it matters:** A Sprint is short so feedback is fast and risk stays low.
**Adaptation:** here a Sprint is one work cycle bound to a single Sprint Goal,
typically a session of hours rather than weeks, which stays inside the Scrum
Guide (2020) timebox of one month or less (see `core/events/`). The
stakeholder's availability sets the real cadence.

**How it changes team behavior:** Sets how much scope a Sprint Goal can hold and
how often the team returns for feedback. A short session means a tight,
single-outcome Sprint Goal and small forecasts. A longer cycle allows a larger
goal but still one coherent objective. It also sets checkpoint frequency: the
adapted Daily Scrum runs between task batches, so cadence determines how many
checkpoints a Sprint holds (`core/events/daily-scrum.md`).

**Default:** One session of a few hours per Sprint, one Sprint Goal per session,
Review at the end of each session.

**Lands in:** `team.md` > Cadence.

### 6. Definition of value

**Ask:** "How will you know this product is succeeding? What outcome, for whom,
tells you a cycle was worth it, beyond features being built?"

**Why it matters:** The Product Owner maximizes *value*, and velocity or item
count is not a value measure. A process in decay measures output over value; a
team that reports only throughput shows a process-decay sign
(`core/anti-patterns.md`, Area 1). Value has to be named to be tracked.

**How it changes team behavior:** Sets the outcome metrics the team records in
`.scrum/metrics.md` and inspects at the Retrospective, and gives the Product Owner
the yardstick for ordering the backlog by value. It also seeds the product purpose
line the PO sharpens at vision ("This product exists in order to..."). Capture the
stakeholder's value definition here and hand it to the PO; do not design the
product.

**Default:** Name at least one outcome measure beyond output: a user-facing result,
a satisfaction signal, a time-to-market target, or a capability the product
unlocks. Record it as the value the team optimizes for.

**Lands in:** `team.md` > Definition of value, and forwarded to
`product/product-goal.md` at stage 1.

### 7. Technical constraints

**Ask:** "What is fixed about how this is built: language, framework, platform,
hosting, data rules, dependencies you must or must not use, compliance the product
must meet?"

**Why it matters:** The Developers own the how, but real constraints bound the
solution space, and non-functional and compliance requirements belong in the work
and the Definition of Done. Naming constraints up front prevents rework and keeps
the DoD honest about security and compliance.

**How it changes team behavior:** Constraints flow into Tier 3 of the Definition
of Done and into every delegation brief's "constraints" field. Compliance and data
rules may add security-tier and profile items (`core/dod/definition-of-done.md`,
`core/dod/profiles.md`). A fixed stack tells the project scan what to detect and
tells Developer agents what not to introduce.

**How it changes team behavior, continued:** Cross-check the answers here against
`setup/project-scan.md` findings. Where the stakeholder states a constraint the
scan confirms, record it as detected. Where they conflict, resolve with the
stakeholder before writing the DoD; existing org standards are a floor and are not
weakened by a stated preference.

**Default:** Adopt whatever the project scan detects as the current stack and
treat it as a constraint; add any compliance or data rule the stakeholder names.

**Lands in:** `team.md` > Technical constraints, and into Tier 3 of
`.scrum/DEFINITION_OF_DONE.md`.

### 8. Review-evidence preferences

**Ask:** "At the Review, how do you want to see that the work is real: a running
demo you drive yourself, screenshots, test output, a walkthrough, or all of these?
What convinces you a thing is done?"

**Why it matters:** "Done" is never self-reported; the Increment is demonstrated
with evidence, and the Review hands the stakeholder the product to use rather than
presenting at them. The evidence the stakeholder trusts sets what the DoD gate
must produce.

**How it changes team behavior:** Sets the evidence format Developer agents return
and the Review records in `.scrum/sprints/sprint-NNN/review.md`: which of runnable
result, test summary, screenshots, or command output are required per PBI. A
stakeholder who wants to drive the demo raises the bar on the increment being
genuinely runnable, not just described. This preference is the acceptance signal
the whole gate serves (`core/dod/definition-of-done.md`).

**Default:** A runnable result the stakeholder can drive, plus test output and
screenshots for anything not driven live; each `done` PBI carries its evidence in
its DoD-evidence field.

**Lands in:** `team.md` > Review evidence.

### 9. Staffing

**Ask:** "Which model tiers, specialist agents, tools, and permissions can this
runtime actually provide? Do you want a senior Developer available for difficult
diagnosis and high-impact work?"

**Why it matters:** Judgment and cost sit in different places. Orchestration,
diagnosis, and verification decide what happens and whether it is really done, so
they pay for the strongest available model. Implementation under a precise brief
carries most of the token volume and runs well on a mid-tier worker model.
Naming the tiers up front puts the money where the judgment is instead of
spreading it evenly. **Adaptation:** a senior Developer is a skill distribution
inside the single Developers accountability, not a new role or title; the Scrum
Guide (2020) defines no sub-roles inside Developers.

**How it changes team behavior:** Builds the capability registry used when the
adapter dispatches work (`adapters/`). A senior Developer or specialist takes
high-impact work and performs read-only diagnosis when a task stalls. Required
authority and domain capability outrank nominal model tier; model strength then
breaks ties (`core/stall-recovery.md`, STALL-5 and STALL-6). The verifier never
runs below the implementer's tier. In a single-tier runtime, record the available
capabilities and use fresh labeled diagnostic and verification passes
(`adapters/single-model.md`).

**Default:** The strongest available model on the Orchestrator, PO, SM, and
verifier; mid-tier worker models on ordinary Developer briefs; the senior
Developer on when a stronger tier exists; specialist routing by capability before
model tier.

**Lands in:** `team.md` > Staffing.

### 10. Delivery mode

**Ask:** "How should finished work reach you: committed with the increment, on a
branch as a pull request you review and merge, or staged for you to commit
yourself?"

**Why it matters:** The Increment must be usable and inspectable, and how it
lands sets how much the stakeholder trusts and reviews it. A stakeholder who
wants to read every diff is poorly served by automatic commits; a stakeholder who
wants momentum is poorly served by a queue of staged changes waiting on them.

**How it changes team behavior:** Sets what the team does at the end of each
verified PBI and at each stage transition. `commit` commits `.scrum/` and the
code together, so the project stays resumable. `branch-pr` keeps work on a
branch and delivers a pull request the team never merges without the stakeholder.
`stage-only` stages and reports, leaving the commit to the stakeholder. Every
mode starts from a clean working tree so the delivered diff carries only the
increment.

**Default:** `commit`: the team commits `.scrum/` and each increment together
from a clean working tree.

**Lands in:** `team.md` > Delivery mode.

## Operating profile (questions 11–17)

Ask these once during founding. Revisit an answer only when the stakeholder changes
the operating rule. Record the answer in the named file; do not ask each new session.

### 11. Session handoff
**Ask:** "At what context use should a session hand off, and how should the next
session start?"
**Default:** The lower of 350,000 tokens and 40% of the context window; schedule a
successor when the host supports confirmed scheduling, otherwise provide a
paste-ready prompt. Record in `team.md` > Session continuity.

### 12. Tiers and roster
**Ask:** "Which capability tiers are available, and how many agents may fill each
seat in one Sprint?"
**Default:** One Tier 1 lead, up to three Tier 2 specialists, and four to eight
Tier 3 implementers, subject to host limits. Record seat, capability, and count in
`team.md` > Staffing.

### 13. Unattended work and authority
**Ask:** "How long may work continue unattended, and which actions must wait for
you?"
**Default:** Eight hours. Destructive actions, legal and financial decisions, and
release authorization require stakeholder approval. Record exceptions in
`.scrum/directives.md`.

### 14. Usage limits
**Ask:** "Which usage windows apply, and at what reported level should new work
pause?"
**Default:** Stop starting work at 95% of any reported limit. Record windows and
reset behavior in `team.md` > Execution control.

### 15. Delivery authority
**Ask:** "Who may commit, push, open pull requests, and merge, and what evidence
is required?"
**Default:** Branch and pull request; stakeholder approval before merge. Record
in `team.md` > Delivery mode.

### 16. Product writing and specialist routes
**Ask:** "Which writing guide governs product text, and which specialist guides
should the team use for writing, interface design, and security?"
**Default:** The package writing contract applies; additional guides are optional
and recorded by path in `team.md` or `.scrum/directives.md`.

### 17. Stakeholder-owned decisions
**Ask:** "Which decisions belong only to you?"
**Default:** Pricing, legal wording, data deletion, releases, and brand choices.
Record the list in `.scrum/directives.md`.

## Team norms and working agreement

After the ten areas, confirm a short working agreement: shared values, rules for
working together, and logistics. Keep it to a handful of lines the team will
actually follow.

- **Honest reporting.** Failed output is reported verbatim, never smoothed into
  "mostly working" (Scrum value: openness; `core/roles/developers.md`).
- **Ask for help early.** An agent does not struggle indefinitely before raising
  an impediment; blockers reach `impediments.md` with a clear ask.
- **Evidence over claims.** No "done" without gate evidence.
- **Clear artifacts.** Apply `core/artifact-writing-standard.md` to stakeholder
  messages, Scrum state, briefs, reports, and technical documentation. Detail must
  support a decision or verification; filler does not count.
- **Adaptive verification.** Select TDD or another test route from
  `core/test-strategy.md` according to the claim and risk, then record why.
- **Specialists by trigger.** Run threat modeling and the standalone UI/UX route
  only when their triggers apply; carry their evidence into the PBI and gate.
- **The floor holds.** The Definition of Done's universal and security tiers are
  never lowered to hit a deadline.
- **Version control.** The delivery mode from area 10 governs how work lands. By
  default the team commits `.scrum/` and each increment together, so the project
  stays resumable. A stakeholder who prefers to review first sets `branch-pr` or
  `stage-only` in `team.md`. Start from a clean working tree in every mode, so a
  commit or a delivered diff carries only the increment.

Record any stakeholder-specific norm here too, in the stakeholder's own words.

## Persisting to team.md and handing off

1. Write every answer into `.scrum/team.md` using `templates/team.md`, one section
   per area plus the working agreement. Mark any answer taken as a default so the
   Retrospective knows it was not an explicit choice.
2. Record the selected stack profiles (from the quality-bar and constraints
   answers), detected commands and CI, test topology, security signals, privacy
   findings, and UI/UX route (from `setup/project-scan.md`) in the same file, so
   planning and the DoD gate can read them.
3. Feed the quality-bar, constraints, and review-evidence answers into the
   instantiated `.scrum/DEFINITION_OF_DONE.md` via
   `core/dod/definition-of-done.md`.
4. Forward the definition-of-value answer to the Product Owner for stage 1 VISION
   (`core/roles/product-owner.md`).
5. Set the state to stage 1 and continue. The founding interview runs once; later
   changes come through the Retrospective, which may amend `team.md`
   (`core/events/retrospective.md`).

The Retrospective can revise any founding answer. Record such revisions in the
`team.md` amendments log with the Sprint that made the change, so the team's
operating agreement stays transparent and improves over time.
