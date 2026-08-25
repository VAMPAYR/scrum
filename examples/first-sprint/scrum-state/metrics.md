# Metrics

*Illustrative output from the fictional project in `examples/first-sprint/walkthrough.md`, not a real project's state.*

## sprint-001 (2026-07-14)
- Throughput: 2
- DoD pass rate: 2/2  |  Rework count: 1
- Cycle time: one session, about 3 hours from idea to a released JPEG tool
- Escaped defects: 0
- Security and assurance note: TM-001 and TM-002 mitigated; TM-003 remains open for batch-mode recovery and is reviewed with PBI-002.
- Verification health: no flaky or skipped tests; one missing destructive-path test caused gate rework and became a regression test.
- Value note: the stakeholder ran it on a real card dump and stopped renaming by hand; asked for HEIC to cover their own iPhone photos.

## sprint-001 retro
- Improvement committed: briefs for file-writing PBIs must name the destructive path and require a failure-path test.
- Prior improvement landed: n/a (first sprint)
- Double-loop note (if any belief/rule was challenged): the team assumed "rename" was a safe operation; a same-second timestamp collision made it destructive, so treat any file write as potentially destructive.
