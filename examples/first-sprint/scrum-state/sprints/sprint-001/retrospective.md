# Sprint 001 Retrospective

*Illustrative output from the fictional project in `examples/first-sprint/walkthrough.md`, not a real project's state.*

- Date: 2026-07-14
- Participants: the AI Scrum Team (PO, SM, Developers). Stakeholder not present.

## Data inspected
- Metrics (from metrics.md): throughput 2, DoD pass rate 2/2, rework count 1, cycle time about 3 hours, escaped defects 0.
- Delegation-brief quality: the PBI-003 brief was clear and needed no rework. The PBI-001 brief listed "no overwrite" as an acceptance checkbox but did not name the collision path in its constraints or ask for a failure-path test, and that is where the rework came from.
- Stall recovery: no no-progress batch, repeated failure signature, or attempt-budget stop occurred. PBI-001 used both authorized attempts, but the first narrowed the failure and the second verified the fix, so no write suspension or expert consultation was required.
- Gate failures: one. PBI-001 passed its happy-path tests, then the verifier drove two files with the same second-level timestamp and the second rename overwrote the first. Caught at the gate, before the Review.
- Verification routes: TDD covered naming and unreadable dates but omitted the highest-impact collision criterion. The rebrief used regression-first TDD: the collision test reproduced the overwrite before the fix and passed after it. No tests were flaky or skipped.
- Security and assurance: TM-001 and TM-002 closed with tests; TM-003 remains open for batch-mode recovery in PBI-002. No incident escaped the gate.
- Artifact quality: the first brief named the outcome but did not connect the no-overwrite claim to a test or threat ID. No vague status claim or private path reached the Review.
- Specialist routes: threat modeling applied because the PBI crossed untrusted-file and destructive-write boundaries. UI/UX was correctly n/a for this CLI increment.
- Impediments: IMP-001 (no test images with known EXIF timestamps) was self-resolved by generating fixtures with Pillow; no stakeholder action needed.
- Health check (if run): not run this Sprint.

## What went well
- The dry-run (PBI-003) reused PBI-001's name-planning function and went through the gate with no rework.
- The verifier caught the overwrite by driving the failure path itself rather than trusting the "done" claim, so a data-loss bug never reached the stakeholder.

## What to improve
- The PBI-001 brief treated a destructive path as one acceptance checkbox among several, so the implementer tested the happy path and left the collision untested. Any work that writes or deletes files needs the destructive path called out and tested up front, not discovered at the gate.

## Improvement items
### Improvement 1
- Action: every delegation brief for a PBI that writes, moves, or deletes files names the overwrite or destructive path in its "Constraints" and requires a failure-path test in its "Evidence to return".
- Owner: Developers, with the SM confirming it at Planning.
- First step: amend team.md working agreement now, before sprint-002 Planning.
- Success measure: no file-writing PBI reaches the gate without a collision or overwrite test in its returned evidence.
- Lands in: team.md amendment.

## Carry-forward check
- Prior improvement(s): none; this is the first Sprint.
- Acted on: n/a for the first Sprint.

## Metrics update
```markdown
## sprint-001 retro
- Improvement committed: briefs for file-writing PBIs must name the destructive path and require a failure-path test.
- Prior improvement landed: n/a (first sprint)
- No-progress batches: 0 | Attempt-budget stops: 0 | Expert consultations: 0
- Recovery outcomes: PBI-001 rebriefed after evidence-producing gate failure; second attempt passed
- Double-loop note (if any belief/rule was challenged): the team assumed "rename" was a safe operation; a same-second timestamp collision made it destructive, so treat any file write as potentially destructive.
```
