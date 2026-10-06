# Two-session continuity example

This fixture shows how a standing rule survives a session handoff. It uses a
generic product and synthetic IDs.

## Before session A

The project has `.scrum/directives.md`:

```markdown
## Active entries

| ID | Date | Stakeholder's words | Operational rule | Scope | Owner | Status |
|---|---|---|---|---|---|---|
| DIR-001 | 2026-01-12 | "Show me evidence before calling work done." | A PBI remains in review until a verifier records command or test evidence. | all agents | Orchestrator | active |
```

The context router includes `DIR-001` on every stage route. Session A reads the
directive, verifies one PBI, and records a checkpoint with one open outcome.

## Handoff from session A

The host scheduler creates `session-B-001`. The Orchestrator lists scheduled
work and records the returned confirmation receipt in `.scrum/handoff-log.md`.
The execution guard records both values:

```text
python scripts/execution_guard.py record-handoff --successor-id session-B-001 --confirmation-receipt scheduler-list-confirmed
python scripts/execution_guard.py session-end --session-id session-A-001
```

The session lock changes to `stale` only after the checkpoint and successor
receipt are saved.

## Resume in session B

Session B acquires a new lock, reads the current stage route, and receives the
same active directive:

```text
Standing directive DIR-001: A PBI remains in review until a verifier records command or test evidence.
```

Session B verifies the remaining work, updates the outcome, and records evidence.
The stakeholder does not need to restate the rule. If the host has no scheduler,
session A records a paste-ready successor prompt and reports that scheduling was
unavailable; it does not claim that a successor exists.
