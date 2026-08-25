# Sprint 001

*Illustrative output from the fictional project in `examples/first-sprint/walkthrough.md`, not a real project's state.*

- Started: 2026-07-14
- Cadence: a few hours, one evening session

## Sprint Goal (Why)
A photographer can rename single photos to their capture date from the terminal and preview the change first, safely, without ever losing a file.

## Forecast (What)
- PBI-001: Rename one photo by its capture date (Size: S)
- PBI-003: Preview renames without changing files (--dry-run) (Size: XS)

## Plan (How)
Build the date-to-name core and the single-file rename first (PBI-001), then reuse its name-planning function for the dry-run (PBI-003), which only reports the plan instead of applying it. The riskiest assumption to test first is that an EXIF DateTimeOriginal is present and parseable across camera makes; probe it with fixture images before writing the rename path. PBI-003 depends on PBI-001's planning function, so PBI-001 is verified before PBI-003 starts.

- Material risks and assumptions: TM-001 malformed EXIF or path input; TM-002 a same-second collision overwrites a photo; TM-003 partial failure loses an original. The Developers own mitigation work; the stakeholder owns acceptance of residual photo-loss risk.
- Threat-model route: create `threat-model.md` for the EXIF and filesystem boundaries before PBI-001.
- Test routes by PBI: PBI-001 uses TDD for deterministic naming and file behavior plus malformed-boundary cases; any discovered defect uses regression-first TDD. PBI-003 uses TDD plus a before-and-after filesystem comparison.
- UX routes by PBI: n/a, CLI product with no graphical user interface.
- High-impact assurance cases: PBI-001 records a compact no-overwrite claim and evidence in its DoD record.

## Task log

### Task: single-file rename (PBI-001)
- Brief: inline in walkthrough.md (delegation brief PBI-001)
- Agent: dev-1
- Status: done
- Evidence returned: first pass returned `uv run pytest` 9 passed (test_renames_by_exif_date, test_no_date_left_untouched and 7 supporting), ruff and mypy clean; the TDD record had no failing collision test. After rebrief, `test_collision_appends_suffix` failed by reproducing the overwrite, then passed after the fix; `uv run pytest` returned 14 passed with test_corrupt_exif_rejected, Ruff and mypy clean, and `uv build` exit 0. TM-002 mapped to the collision test and the no-overwrite assurance claim.
- Verification: verify-1. FAIL on the first walk, then PASS after rework.
- Notes: Rework 1, escalation-ladder rung (a) rebrief. First pass met the happy-path criteria but the verifier drove two files with the same second-level timestamp and the second rename overwrote the first, failing DoD 0.2, 0.4, 0.6, Tier 1.9, acceptance criterion 3, and the Tier 3 no-overwrite rule. Rebrief named TM-002 explicitly; rework first reproduced the defect, then added a numeric suffix and passed the regression test.

### Task: dry-run preview (PBI-003)
- Brief: inline; reuse of PBI-001 plan_new_name, report-only
- Agent: dev-2
- Status: done
- Evidence returned: the dry-run tests were observed failing before implementation, then `uv run pytest` returned 14 passed, including test_dry_run_prints_mapping, test_dry_run_changes_nothing, and test_dry_run_exit_codes; on-disk tree was byte-identical after `--dry-run`; Ruff and mypy clean.
- Verification: verify-1. PASS.
- Notes: Rework 0. Built on the planning function verified in PBI-001, so it went straight through the gate.

## Checkpoints

### Checkpoint 1 (after the PBI-001 gate)
- Progress toward the Sprint Goal: single-file rename is Done and collision-safe; the safe-preview half of the Goal is not built yet.
- Plan adaptation: confirmed PBI-003 can reuse plan_new_name unchanged and only skip the write step, so no new planning logic is needed.
- Impediments surfaced: IMP-001 (no test images with known EXIF timestamps) surfaced at task start and was self-resolved before this checkpoint; logged in ../../impediments.md.

## Sprint outcome
- PBIs that passed the DoD gate (the Increment): PBI-001, PBI-003
- Carryover (not Done, returned to the backlog): none
- Sprint Goal met: yes. Single-file rename and safe preview both shipped with recorded evidence; the one gate failure was caught and reworked before the Review.
- Ended: 2026-07-14
