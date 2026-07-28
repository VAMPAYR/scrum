# Adapter: generic single-model

Use this adapter when the runtime has no worker-agent or subagent primitive: a
plain chat model, or any tool that runs one model in one conversation. One model
plays every role by switching labeled hats. Set `Adapter: generic` in
`.scrum/state.md`. Read this alongside `SKILL.md` and `core/orchestrator.md`.

## The labeled-hat protocol

The model wears one hat per turn and prefixes the turn with its label. Never
blend two roles in one turn. The hats:

| Label | Role | Does |
|---|---|---|
| `[ORCH]` | Orchestrator | facilitates, delegates, arbitrates, writes briefs and artifacts, runs the DoD gate |
| `[PO]` | Product Owner | Product Goal, backlog, ordering by value, acceptance criteria, validation |
| `[SM]` | Scrum Master | event facilitation, impediments, process guard, health checks |
| `[DEV]` | Developers | implements, tests, meets the DoD, self-manages the Sprint Backlog |
| `[VERIFY]` | verification pass | walks the DoD against the increment and records evidence |

Rules:

1. **Label every turn.** The first token of a role turn is its label. A reader
   scanning the transcript can tell who decided what.
2. **Keep decisions separated.** Ordering and acceptance are `[PO]` decisions;
   process is an `[SM]` decision; implementation is a `[DEV]` decision. Do not let
   one hat make another hat's call.
3. **Brief before build.** `[ORCH]` writes the delegation brief (PBI id, Sprint
   Goal, acceptance criteria, applicable DoD tiers, files in scope, constraints,
   evidence to return) before any `[DEV]` turn starts. The brief is the contract
   the `[VERIFY]` pass checks against.
4. **Read before speaking.** Read the role file in `core/roles/` before wearing
   that hat, the event file in `core/events/` before facilitating an event, and
   `core/dod/definition-of-done.md` before any gate.

## The no-coding rule in single-model mode

The Orchestrator's no-coding rule assumes separate worker agents. With one model
there are no separate workers, so the rule relaxes: the same model writes code
under the `[DEV]` hat. The discipline the rule protects is preserved by two
mechanisms instead:

- **Role labels** keep facilitation, product decisions, and implementation from
  collapsing into one undifferentiated stream.
- **Self-verification** replaces the independent verifier at the DoD gate.

## Staffing in single-model mode

The Staffing section of `.scrum/team.md` is a no-op here. One model fills every
seat, so there is no stronger or cheaper tier to assign and no separate senior
Developer; record the single tier in `team.md` and move on. The labeled-hat
discipline substitutes for what staffing buys elsewhere: judgment stays visible
because no turn blends two hats, and the `[VERIFY]` pass re-derives its checks
from the written criteria instead of relying on a distinct agent.

## Self-verification (replaces independent verifiers)

The DoD gate in `core/dod/definition-of-done.md` normally uses a verifier agent
distinct from the implementer. Here the same model runs a `[VERIFY]` pass. Make
it as independent as a single model can:

1. **Re-derive from the source, not from memory.** Re-read
   `.scrum/DEFINITION_OF_DONE.md` and the PBI's acceptance criteria from the file.
   Do not verify against what the `[DEV]` turn believed it did; verify against the
   written criteria.
2. **Run real checks, record real output.** Execute the build, the full test
   suite, lint, and typecheck if the runtime can. Paste the actual command output
   into the PBI's "DoD evidence" field. If the runtime cannot run a check, mark
   the item `n/a` with the reason; never assume a pass.
3. **Adversarial reading.** In the `[VERIFY]` turn, actively try to fail each
   item: look for the untested branch, the unhandled error at the boundary, the
   secret left in a log, the acceptance criterion with no matching test. Report
   what you find verbatim.
4. **Fresh statement of results.** Write the verdict per item as if reporting to
   someone who did not write the code. A false "done" is what this pass exists to
   catch.

## Honest note: self-verification is weaker

Self-verification is weaker than an independent verifier, and the gate should say
so out loud in `.scrum/`. One model checking its own work shares the blind spots
that produced the work: a criterion it misread while building it will be misread
again while checking it, and confirmation bias favors the "done" it just claimed.
Running actual commands and pasting real output is the strongest guard, because
tool output does not share the model's bias. Reasoning-only checks are the
weakest.

Mitigations, in order of strength:

- Prefer executed checks with recorded output over any reasoning-only judgment.
- Separate the `[VERIFY]` turn from the `[DEV]` turn by re-reading the source
  criteria first, so the check anchors on the spec rather than the code.
- For high-stakes increments (security-sensitive, destructive, or hard to
  reverse), ask the human stakeholder to review the evidence, or run the same
  `.scrum/` project through `adapters/claude-code.md` or `adapters/openai.md`
  where an independent verifier agent is available. The plain-file state makes
  that handoff clean.

Record in `metrics.md` that the sprint used self-verification so the
Retrospective can weigh escaped defects against the weaker gate.

## State handling without a filesystem

If the runtime has file access, write `.scrum/` to disk and commit it. If not,
keep each `.scrum/` file as a fenced markdown block in the conversation. On every
stage transition, re-emit the changed block (`state.md`, `backlog.md`,
`sprint.md`, and so on). On resume, paste the last blocks back so `[ORCH]` can
read the stage and continue. The formats are fixed by `templates/` and by the PBI
record in `SKILL.md`.

## Escalation ladder in single-model mode

The rungs in `core/orchestrator.md` still apply, run as labeled turns:

1. **Rebrief**: `[ORCH]` sharpens the brief and adds the failure trace; a new
   `[DEV]` turn retries.
2. **Fresh attempt**: restate the problem from scratch in a new `[DEV]` turn,
   discarding the prior approach, with the failure output in view.
3. **Split or contrast**: decompose into smaller `[DEV]` turns, or run two
   `[DEV]` turns with different approaches and keep the better result after a
   `[VERIFY]` pass on each.
4. **Direct resolution**: already the norm here, since one model does the work;
   log the difficulty in the sprint file.
5. **Stakeholder escalation**: `[ORCH]` batches the open questions, presents
   options with a recommendation, and waits for your decision.

Interrupt the stakeholder during EXECUTION only for scope decisions, destructive
actions, or an exhausted ladder. Everything else waits for the Sprint Review.
