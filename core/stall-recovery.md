# Stall recovery protocol

Read this file only when a worker reports `BLOCKED`, repeats a materially similar
failure, exhausts its attempt budget, or reaches a checkpoint without new
evidence. It is the canonical source for stalled-task recovery. Other files cite
the `STALL-*` rules instead of restating them.

## Invariants

- **STALL-1, evidence defines progress.** Progress means the work reproduced the
  failure, eliminated a stated hypothesis, narrowed the failing surface, changed
  the result in the predicted direction, identified an environmental constraint,
  or passed a previously failing check without a new regression. Code churn,
  repeated commands with unchanged inputs, and a new speculative patch are not
  progress.
- **STALL-2, one hypothesis per mutating attempt.** Before editing, state the
  suspected cause, the change or probe, the expected discriminating result, and
  the stop condition. A failed attempt may still count as progress under STALL-1.
- **STALL-3, bounded attempts.** A worker gets at most two mutating attempts by
  default before outside diagnosis. Stop earlier when two consecutive attempts
  produce the same normalized failure without new evidence. High-impact or
  irreversible work receives expert review before another mutation after its
  first failure. The Orchestrator may extend a budget only by recording the new
  evidence and distinct hypothesis that justify another attempt.
- **STALL-4, pause writes on trigger.** A stalled worker preserves its diff and
  evidence, stops editing, and returns the blocker packet below. It does not keep
  trying while another agent diagnoses the task.
- **STALL-5, match capability before model tier.** Select support by required
  authority, relevant domain capability, diagnostic strength, model tier, then
  cost. The strongest general model is the fallback, not an automatic substitute
  for a relevant specialist.
- **STALL-6, consult before takeover.** Expert support starts read-only. The
  expert diagnoses and proposes one discriminating next step. The Orchestrator
  then resumes the worker, assigns a fresh worker, pairs them, or splits the task.
  If the expert edits production code, the expert becomes a co-implementer and
  cannot perform final verification.
- **STALL-7, isolate retries.** Preserve the baseline commit or diff before a
  retry. Use an isolated worktree when the runtime supports one. Otherwise
  serialize edits and inspect the scoped diff before continuing. Never discard a
  failed attempt until its evidence is captured, and never reset unrelated work.
- **STALL-8, keep stakeholder escalation narrow.** Ask the stakeholder only for
  scope, product intent, authority for a destructive or irreversible action, or
  an ambiguity only the stakeholder can resolve. Technical uncertainty remains
  with the team.

## Attempt contract

Every build brief carries these fields before work starts:

```markdown
- Required capabilities: <domain and diagnostic capabilities>
- Attempt budget: <default 2 mutating attempts; lower or higher with reason>
- Progress evidence: <what would reproduce, narrow, eliminate, or verify>
- Stop conditions: <repeated failure, exhausted budget, authority boundary, ...>
- Baseline: <commit, worktree, or scoped diff state>
- Diagnostic route: <senior/specialist/fresh agent/single-model pass>
```

A read-only scout uses a question and time boundary instead of a mutating-attempt
budget. Repeated read-only probes still stop when they answer no new question.

## Executable stop guard

When Python is available, pass the current ledger to
`scripts/stall_router.py <record.json>` before authorizing another mutation. The
script enforces required attempt fields, the default budget, evidence-backed
budget extension, high-impact early review, repeated-failure stops, stakeholder
boundaries, authority filtering, and capability-first support selection. It does
not diagnose the code or replace the evidence gate.

```json
{
  "risk": "normal",
  "cause": "specialist-gap",
  "attempt_budget": 2,
  "required_capabilities": ["database"],
  "required_authority": ["repo-read", "test-execute"],
  "attempts": [
    {
      "mutating": true,
      "hypothesis": "the transaction boundary is wrong",
      "action": "add one boundary probe and make the scoped change",
      "expected_result": "the failing signature moves to the isolated boundary",
      "stop_condition": "stop if the same signature returns without new evidence",
      "outcome": "failed",
      "progress": false,
      "failure_signature": "normalized relevant failure"
    }
  ],
  "available_support": [
    {
      "id": "database-specialist",
      "capabilities": ["database"],
      "authority": ["repo-read", "test-execute"],
      "diagnostic_strength": 4,
      "model_tier": 3,
      "cost": 2
    }
  ]
}
```

An attempt budget above two also requires `budget_extension_reason` and
`budget_extension_evidence`. Never treat the script's selected support as
permission to exceed that support candidate's recorded authority.

## Blocker packet

The worker returns this packet when STALL-3 or STALL-4 fires:

```markdown
## BLOCKED: <task and PBI>
- Last command or action: <exact command or mutation>
- Failure evidence: <exact relevant output; path to preserved full output if long>
- Attempts:
  - A1 | hypothesis: <cause> | evidence: <result> | progress: <yes/no and why>
- Current diff: <paths and summary; preserved worktree or patch>
- Hypotheses eliminated: <evidence-backed list>
- Remaining unknown: <the question that blocks progress>
- Requested capability or decision: <specific help needed>
```

Keep the exact relevant error. Remove unstable timestamps, random identifiers, or
temporary paths only when comparing whether two failures are materially the same.
Never smooth a failure into a summary such as "mostly working."

## Diagnose and route

The Orchestrator reviews the original brief, blocker packet, actual diff, and
failure evidence before selecting one route.

| Cause | Evidence | Route |
|---|---|---|
| Brief or context gap | Criteria, files, decision, or constraint was absent | Rebrief the same worker with the missing material |
| Fixed wrong model | The worker repeats a disproven assumption or materially identical patch | Use a fresh capable worker with the failed path and exact evidence |
| Specialist knowledge gap | A named subsystem or domain distinction controls the failure | Run a read-only specialist consultation, then resume, pair, or reroute |
| Oversized or coupled task | The brief contains several outcomes or cannot fit one batch | Split by observable outcome; pair or mob only the coupled decision |
| Environment, tool, or permission | The code cannot affect the missing access, service, dependency, or tool | Stop code trials; run a scout or log an impediment with owner and ask |
| Nondeterminism | The same inputs produce inconsistent results | Characterize and stabilize the failure before changing product behavior |
| Small mechanical residue | The diagnosis is settled, scope is small, and workers failed the mechanical step | The Orchestrator may intervene, log it, and use an independent verifier |
| Scope, product intent, or destructive authority | The team lacks the decision or authorization | Apply STALL-8 and ask the stakeholder with options and a recommendation |

Two approaches may run in parallel only when isolated worktrees prevent collision
or when both are read-only. Do not ask two agents to edit the same working tree.

## Expert consultation

Where `team.md` enables a senior Developer or identifies a relevant specialist,
that agent receives the blocker packet and performs a read-only pass. It returns:

1. observed facts and the most likely cause, with confidence and evidence;
2. the prior hypotheses the evidence excludes;
3. one next experiment that distinguishes the leading explanations;
4. the expected result for each explanation;
5. the stop condition and any safety boundary.

The expert guides the work rather than silently taking it over. The original
worker may implement the next step while paired with the expert. A fresh worker
is preferable when context rot or a fixed mental model caused the loop.

In a single-tier runtime, capability still outranks nominal seniority. In a
single-model runtime, start a fresh labeled `[DIAG]` pass with only the blocker
packet, diff, and relevant files. State that this pass is not independent. Use a
separate `[VERIFY]` pass after implementation.

## Logging and learning

Record only compact attempt summaries in `sprint.md`; place long output in a
referenced evidence file or preserve it in tool output. Log the attempt count,
diagnosis, selected capability, recovery route, resolution, and verifier.

At each checkpoint, a task that consumed a full batch without STALL-1 evidence
becomes `blocked`. At the Retrospective, inspect repeated failure signatures,
late escalation, wrong capability routing, environment blockers treated as code
defects, and any recovery that lost verifier independence. Change one process
rule only when the evidence shows the current rule caused or prolonged the stall.
