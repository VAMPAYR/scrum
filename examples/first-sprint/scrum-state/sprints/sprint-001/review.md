# Sprint 001 Review

*Illustrative output from the fictional project in `examples/first-sprint/walkthrough.md`, not a real project's state.*

- Date: 2026-07-14
- Sprint Goal (recap): A photographer can rename single photos to their capture date from the terminal and preview the change first, safely, without ever losing a file.
- Sprint Goal met: yes

## Increment demonstrated
- PBI-001: Rename one photo by its capture date (outcome: a JPEG becomes its capture date and time, and a name clash never overwrites a file)
- PBI-003: Preview renames without changing files (--dry-run) (outcome: the exact renames are shown before anything touches disk)

## Evidence
### PBI-001
- Runnable result: the stakeholder copied a handful of files off a memory card and ran `exif-rename IMG_4471.JPG`; the file became `2026-06-02_180233.jpg`. Running it again on two frames shot in the same second produced `..._180233.jpg` and `..._180233-1.jpg`, with both originals intact.
- Test output: `uv run pytest` 14 passed, including test_collision_appends_suffix and test_no_date_left_untouched.
- Screenshots / artifacts: terminal transcript in sprints/sprint-001/sprint.md task log; DoD evidence in product/backlog.md PBI-001.
- Risk and assurance evidence: TM-001 and TM-002 mitigated in `threat-model.md`; TM-003 remains open for explicit batch behavior in PBI-002. The no-overwrite claim is supported by the regression test and two-file run; the stakeholder owns acceptance of the stated filesystem-race residual risk.
- UI/UX evidence: n/a, CLI product with no graphical interface.
- Artifact audit: pass; outcomes precede process detail, claims point to commands and paths, and no private photo path appears.

### PBI-003
- Runnable result: the stakeholder ran `exif-rename --dry-run ./from-card/` on the same files and read the `old -> new` list; a directory listing before and after was identical.
- Test output: `uv run pytest` 14 passed, including test_dry_run_changes_nothing.
- Screenshots / artifacts: DoD evidence in product/backlog.md PBI-003.
- Risk and assurance evidence: dry-run performs no write; byte-identical before-and-after evidence supports that claim.
- UI/UX evidence: n/a, CLI product with no graphical interface.
- Artifact audit: pass; evidence is traceable and no private path appears.

## Stakeholder feedback
- "The dry-run is the part I trust. I ran it first every time."
- "It skipped every photo from my phone. Those are all HEIC, and that is most of what I shoot." This is the largest gap for the stakeholder's own library.
- No request to change the naming format; `YYYY-MM-DD_HHMMSS` sorts the way they wanted.

## Decisions
- Acceptance: the stakeholder accepts PBI-001 and PBI-003. Nothing rejected.
- Release decision (PO): release now. The tool installs from source with pip and is usable on JPEG today; HEIC follows.
- Product Goal still valid: yes, no change.

## Backlog changes
- New items: PBI-004 (Rename HEIC photos from iPhone), captured from the HEIC-skip feedback.
- Reordered: PBI-002 (batch a folder) placed above PBI-004, so the core whole-shoot outcome ships before the new format.
- Dropped: none.

## Metrics update
```markdown
## sprint-001 (2026-07-14)
- Throughput: 2
- DoD pass rate: 2/2  |  Rework count: 1
- Cycle time: one session, about 3 hours from idea to a released JPEG tool
- Escaped defects: 0
- Security and assurance note: TM-003 remains open for batch-mode failure and rollback; review at PBI-002.
- Verification health: no flaky or skipped tests; one missing destructive-path test caused gate rework and was added as a regression.
- Value note: the stakeholder ran it on a real card dump and stopped renaming by hand; asked for HEIC to cover their own iPhone photos.
```
