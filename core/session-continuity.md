# Session continuity

This module governs resumable work across agent sessions. The host adapter
defines which scheduling and messaging capabilities exist. Never claim that a
successor was scheduled until the host confirms its identifier.

## CONT-1 — Record the operating limit

At founding, record a context handoff threshold and a measurable fallback in
`.scrum/team.md`. The default is the lower of 350,000 tokens or 40% of the
reported context window. If the host reports neither context use nor window size,
record a proxy (elapsed active time or message count) and its threshold. Check
the limit at each task-batch checkpoint. Begin handoff before reaching it.

## CONT-2 — Persist state before stopping

Before a session stops with unfinished work:

1. Commit and push verified work when the delivery mode permits; preserve all
   unverified changes and describe them accurately.
2. Append a dated checkpoint to `.scrum/handoff-log.md`, including current stage,
   Sprint and PBI, verified state, active agent seats, unresolved blockers,
   relevant action receipts, next steps, and open stakeholder questions.
3. Create a successor through the configured host scheduler. If no scheduler
   exists, write a paste-ready continuation prompt and tell the stakeholder.
4. Confirm the successor by querying the scheduler. Record its identifier and
   confirmation evidence in the handoff log.
5. Mark the ending session lock stale only after the checkpoint and successor
   evidence are saved.

If the host cannot confirm a successor, report that limitation; do not report a
completed handoff. Record completion when no work remains; create successors
only for unfinished work.

## CONT-3 — Lock active sessions

At startup, read `.scrum/session-lock.json`. A lock younger than the configured
staleness interval (default 45 minutes) belongs to an active session. Do not
mutate shared project state until that session is confirmed stopped or the
stakeholder resolves the conflict. Refresh the lock at least every 30 minutes,
including immediately before and after a long external wait. Store a session ID,
start time, last checkpoint, and status. A stale lock is evidence to inspect,
not permission to discard the prior session's work.

When Python is available, acquire the lock with `python
scripts/execution_guard.py session-start --session-id <id> --project-root .`.
Refresh it with `session-checkpoint`. Inspect an older lock and confirm it is
stale before passing `--stale-confirmed`. Use `session-end` only after saving the
checkpoint and any required successor confirmation.

The Orchestrator is the single writer for the execution ledger. Serialize guard
commands. Before a session can end, synchronize unfinished deliverables with
`set-open-outcomes <ids...>`; set an empty list when none remain. After the host
confirms a successor, record its ID and query receipt with `record-handoff`.
The guard requires both values before it marks the session lock stale. A worker
seat may be refilled only after `worker-stop --handoff-note <summary>` records
what the next occupant needs.

## CONT-4 — Read and acknowledge stakeholder messages

At startup and each checkpoint, inspect `.scrum/inbox.md` when the adapter or
project uses it. Apply each unacknowledged message through its accountable role
and append an acknowledgment with the message ID, date, and resulting action.
Do not put secrets or private source material in the inbox. A host with reliable
cross-session messaging may use that channel; persist the decision and
acknowledgment in project state.

## CONT-5 — Preserve continuity in briefs

Delegation briefs and successor prompts carry the active standing directives
that apply to their scope, copied verbatim from `.scrum/directives.md`, and link
to the relevant decisions and checkpoint. They carry no unrelated project or
personal information.
