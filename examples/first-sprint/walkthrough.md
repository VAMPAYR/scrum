# First sprint walkthrough: exif-rename

This is a condensed, illustrative run of a first `scrum` session for an imaginary
tiny project, `exif-rename`, a command-line tool that renames photo files to their
capture date read from EXIF metadata. It runs from the first invocation through
founding, vision, planning, one execution loop with a real Definition of Done
gate failure and its rework, the Review, and the Retrospective.

The resulting state sits in `scrum-state/` beside this file. That folder mirrors
what the tool writes to `.scrum/` in a real project; it carries a visible name
here so the files are browsable on GitHub. In a live project the tree lives at
`.scrum/`.

Role labels follow the package: `[ORCH]` Orchestrator, `[PO]` Product Owner,
`[SM]` Scrum Master, `[DEV]` a Developer agent, `[VERIFY]` the independent
verifier. `Stakeholder:` is the human user. Repeated exchanges are cut with `...`.

---

Stakeholder: `/scrum start "a CLI tool that renames photos by EXIF date"`

[ORCH] Reading `.scrum/state.md`. It does not exist, so this project is new.
Bootstrapping `.scrum/` and routing to stage 0 FOUNDING regardless of the
argument. The repo scan finds an empty project: no build, test, or CI config yet.
I loaded `core/artifact-writing-standard.md`; this runtime also discovered
`research-clinical-writing`, so every message and artifact uses its canonical
style guide.
The Scrum Master runs the founding interview once; it captures how you want the
team to work, not what to build.

## 0 FOUNDING

[SM] Four quick areas. First, how should the team talk to you during the work,
terse status or full detail, and when should it stop to ask you versus report at
the Review?

Stakeholder: Terse. Plain words. Only stop me for something you cannot undo, or a
real fork in the road.

[SM] Noted. Second, risk and quality. When a safe approach and a faster one pull
against each other, which way do you lean, and is there a floor you never drop?

Stakeholder: Play it safe with my files. Never lose a photo. Tests and types
clean is the floor; I do not care about anything fancier.

[SM] Good, and that floor holds even for a deadline. Third, cadence and value.
How long is one work cycle, and how will you know a cycle was worth it?

Stakeholder: A few hours tonight. It worked if I stop renaming photos by hand in
Finder.

[SM] Last, constraints and evidence. What is fixed about how this is built, and
what convinces you it is done?

Stakeholder: Python, runs on my Mac, and the photos never leave the machine. I
will run it on a card myself to believe it.

[SM] That is enough to start. Writing `.scrum/team.md`: terse plain updates, batch
questions to the Review, moderate risk with file writes kept conservative, the
universal and security floor plus the CLI stack profile, a few-hour cycle, value
measured as manual renaming removed, Python 3.12 with no network, and a
stakeholder-driven demo plus test output as evidence. The writing standard is
mandatory; AI-assisted work gets repo-local access only, no network or secrets;
the UI/UX route is n/a for this CLI. Instantiating
`.scrum/DEFINITION_OF_DONE.md` from that: Tier 0 and Tier 1 verbatim, the CLI
profile, and three Tier 3 rules (no network calls, no overwrite of an existing
file, local lint and type gates since there is no CI). Handing off to the Product
Owner.

## 1 VISION

[PO] I have your definition of value from founding. Now, what to build and why.
What outcome do you want, and why does it matter now?

Stakeholder: My photos come off three cameras and my phone. The filenames are all
IMG_1234 and they will not sort by time when I mix them. I want them named by when
I shot them.

[PO] Who is this for, and what do you do today instead?

Stakeholder: Me, and hobby shooters like me. Today I rename by hand in Finder. It
is fine for five files and miserable past twenty.

[PO] How will you know it works? Give me one concrete example, start to finish.

Stakeholder: I dump a card, run one command, and every file becomes its date and
time. I never touch Finder for this again.

[PO] And the non-negotiables. What must never happen?

Stakeholder: Never overwrite or delete a photo. If you cannot read a date, leave
the file alone.

[PO] Writing `.scrum/product/product-goal.md`: the product exists to give
sortable filenames from capture dates without manual renaming, and it does not
edit, tag, or upload. Seeding an ordered `.scrum/product/backlog.md` with three
items:

- PBI-001: Rename one photo by its capture date (Size S). The foundation.
- PBI-002: Rename every photo in a folder (Size S). The whole-shoot outcome.
- PBI-003: Preview renames without changing files, `--dry-run` (Size XS). Safety.

## 3 PLANNING

[SM] One real Sprint Goal, and keep the Definition of Done in the room. The
forecast is the Developers' to make.

[PO] The most valuable, most ready slice is a single-file rename that is safe, and
a preview so a mistake costs nothing. Ordering PBI-001 first, then PBI-003.

[DEV] Forecasting PBI-001 and PBI-003 for this session. PBI-003 reuses PBI-001's
name-planning function, so PBI-001 gets built and verified first, then the
report-only dry-run follows. PBI-002 (batch) waits; a folder run is just the
single rename in a loop once the single case is safe.

[DEV] The file and EXIF boundaries trigger `core/threat-modeling.md`. PBI-001
uses TDD for deterministic naming and file behavior, with regression-first TDD
for any reproduced defect. PBI-003 uses TDD plus a byte-for-byte filesystem
comparison. The UI/UX route is n/a. PBI-001 carries a compact no-overwrite
assurance claim because failure could destroy a personal photo.

[SM] Sprint Goal, agreed by the team: "A photographer can rename single photos to
their capture date from the terminal and preview the change first, safely, without
ever losing a file." Writing `.scrum/sprints/sprint-001/sprint.md`. Stage moves to
4 EXECUTION.

## 4 EXECUTION

[DEV] Before the rename path a blocker appeared: no sample photos with known EXIF
dates to test against. Logging IMP-001 and self-resolving it, generating three
JPEG fixtures with Pillow under `tests/fixtures/`, each stamped with a known
DateTimeOriginal. Closed, no stakeholder action needed.

[ORCH] Delegating PBI-001 to dev-1 with a full brief:

```
## Delegation brief: PBI-001 Rename one photo by its capture date
- Type: build
- Sprint Goal: A photographer renames single photos to their capture date from
  the terminal and previews the change first, safely, without losing a file.
- Task: Ship `exif-rename <file>` that renames one JPEG to its EXIF capture date.
- Acceptance criteria (from the PBI):
  - [ ] A JPEG with an EXIF DateTimeOriginal is renamed to YYYY-MM-DD_HHMMSS.jpg.
  - [ ] A photo with no readable date is left untouched, reported on stderr,
    exit non-zero.
  - [ ] An existing target name gets a -1, -2 suffix; no file is overwritten.
- Definition of Done tier checklist: Tier 0 all; EXIF input and filesystem
  writes trigger Tier 1, so apply relevant items and
  mark each other item n/a with reason; Tier 2 CLI profile. See
  .scrum/DEFINITION_OF_DONE.md.
- Risk and threat route: TM-001 malformed EXIF, TM-002 collision overwrite,
  TM-003 partial failure; see sprints/sprint-001/threat-model.md.
- Test strategy: TDD for deterministic naming and file behavior, including
  malformed and collision paths; regression-first TDD for any reproduced defect.
- UX route: n/a, CLI product with no graphical interface.
- Files in scope: src/exif_rename/rename.py, src/exif_rename/cli.py,
  tests/test_rename.py, pyproject.toml.
- Out of scope: folder handling (PBI-002), the --dry-run flag (PBI-003), any
  network code.
- Constraints: Python 3.12, Pillow for EXIF, argparse for the CLI, no network,
  image data never leaves the machine.
- Authority and action limits: read and edit the named repo files; run local
  build, test, lint, and type commands; no network, deployment, or deletion;
  stop after two failed implementation cycles.
- Private-data boundary: use only synthetic fixtures; do not place user photo
  names, private paths, or image content in prompts, logs, artifacts, or commits.
- Context the agent lacks: this is the first PBI; there is no code yet. Fixture
  images with known dates are in tests/fixtures/ (IMP-001).
- Writing and artifact standard: core/artifact-writing-standard.md with
  research-clinical-writing loaded.
- Evidence to return: `uv run pytest` summary; `uv run ruff check .` and
  `uv run mypy src` status; observed red-then-green result for each acceptance
  criterion; threat-to-test mapping; full diff and changed file paths.
- On blocking: stop and report the blocker verbatim; do not guess past it.
```

[DEV] (dev-1) Returned. Evidence:

```
uv run pytest  ->  9 passed  (test_renames_by_exif_date criterion 1;
                              test_no_date_left_untouched criterion 2; + 7)
uv run ruff check .  ->  clean      uv run mypy src  ->  clean
Files: src/exif_rename/rename.py, cli.py, tests/test_rename.py, pyproject.toml
Criterion 3 (collision) implemented: checks os.path.exists before writing.
TDD evidence: red-then-green recorded for criteria 1 and 2; no failing test was
recorded for criterion 3.
```

[VERIFY] (verify-1, distinct from dev-1) Walking `.scrum/DEFINITION_OF_DONE.md`
from source and inspecting the actual diff. Scope and build pass. DoD 0.2 and 0.4
fail: criterion 3 is the destructive path, TM-002 names it, and it maps to zero
tests. Driving it by hand, two frames shot in the same second both plan
`2026-06-02_180233.jpg` and the second write overwrote the first; the existence
check ran before the first rename, not the second.

```
$ exif-rename a.jpg b.jpg
renamed a.jpg -> 2026-06-02_180233.jpg
renamed b.jpg -> 2026-06-02_180233.jpg   # overwrote the first; a.jpg is gone
```

FAIL: DoD 0.2, 0.4, 0.6, Tier 1.9, acceptance criterion 3, and the Tier 3
no-overwrite rule. Reported
verbatim. PBI-001 is not done. Escalation ladder rung (a), rebrief: the collision
path was one checkbox and went untested. Rebriefing dev-1 to resolve a collision
to a new name and first add a regression test that reproduces the overwrite.

[DEV] (dev-1) Reworked. Evidence:

```
red: test_collision_appends_suffix failed; second source was overwritten
green: test_collision_appends_suffix passed after atomic suffix planning
uv run pytest  ->  14 passed
  test_collision_appends_suffix    (criterion 3, new)
  test_corrupt_exif_rejected       (Tier 1.2 and 1.5, new)
  + 12 prior tests
uv run ruff check .  ->  clean
uv run mypy src      ->  clean
$ exif-rename a.jpg b.jpg
renamed a.jpg -> 2026-06-02_180233.jpg
renamed b.jpg -> 2026-06-02_180233-1.jpg  # both originals intact
```

[VERIFY] Re-walking the gate. All Tier 0 pass; 0.4 now maps criterion 3 to
test_collision_appends_suffix and the manual drive shows the `-1` suffix with no
overwrite. Tier 1.1, 1.2, 1.4, 1.5, 1.6, 1.8, and 1.9 pass with the threat,
input, privacy, failure, dependency, scan, and mitigation evidence; identity and
network abuse items are n/a with individual reasons. CLI profile: `--help` lists usage, exit codes
documented, output and errors split across stdout and stderr. PASS. Recording
evidence into PBI-001's DoD-evidence field and marking it done.

[ORCH] Checkpoint 1: single-file rename is Done and collision-safe; the preview
half of the Goal is not built. PBI-003 can reuse `plan_new_name` unchanged.
Delegating PBI-003 to dev-2.

[DEV] (dev-2) ... report-only path built on `plan_new_name`. Evidence:
`uv run pytest` 14 passed, including test_dry_run_prints_mapping and
test_dry_run_changes_nothing; the on-disk tree is byte-identical after
`--dry-run`; ruff and mypy clean.

[VERIFY] ... walked the gate, PASS, no rework. Evidence recorded; PBI-003 done.

[ORCH] Forecast met. The Increment is PBI-001 and PBI-003. Stage moves to
5 REVIEW.

## 5 REVIEW

[PO] Sprint Goal was met. Both forecast items are Done with evidence. Demonstrate,
do not describe; you drive.

Stakeholder: (runs `exif-rename IMG_4471.JPG`) It became `2026-06-02_180233.jpg`.
(runs it on two same-second frames) One got `-1`. Both originals are still here.
(runs `exif-rename --dry-run ./from-card/`) The dry-run is the part I trust. I ran
it first every time.

[PO] The test evidence is in each PBI's DoD-evidence field; 14 tests pass.
TM-003 remains open for batch-mode recovery and belongs to PBI-002. Any gaps?

Stakeholder: It skipped every photo from my phone. Those are all HEIC, and that is
most of what I shoot.

[PO] Capturing that. New item PBI-004, "Rename HEIC photos from iPhone", from your
own library gap. I am ordering PBI-002 (batch a folder) above it, so the core
whole-shoot outcome ships before the new format. Naming format stays; it sorts the
way you wanted. Release decision: release now, it installs from source and works on
JPEG today. Writing `.scrum/sprints/sprint-001/review.md` and appending the metrics
row. Stage moves to 6 RETRO.

## 6 RETRO

[SM] The AI team inspects itself. Grounding in the numbers: throughput 2, DoD pass
rate 2/2, rework 1, escaped defects 0.

[DEV] What went well: the dry-run reused the verified planning function and passed
with no rework. The verifier caught the overwrite by driving the failure path
itself, so a data-loss bug never reached the Review.

[SM] What to improve, with the data behind it: the PBI-001 brief listed "no
overwrite" as one acceptance checkbox and did not name the destructive path in its
constraints or ask for a failure-path test, so the happy path shipped untested and
the gate caught it late.

[DEV] Improvement 1, owned by the Developers with the SM confirming at Planning:
every brief for a PBI that writes, moves, or deletes files names the destructive
path in "Constraints" and requires a failure-path test in "Evidence to return".
First step: amend `team.md` now. Success measure: no file-writing PBI reaches the
gate without a collision or overwrite test.

[SM] Landing it in `.scrum/team.md` as a working-agreement amendment dated
sprint-001, and appending the retro block to `metrics.md`. Carry-forward check:
none, this is the first Sprint. A new Sprint starts immediately; PBI-002 is next.

---

The full state after this session is in `scrum-state/`: `team.md` (with the retro
amendment), `state.md`, `DEFINITION_OF_DONE.md`, `product/` (goal and backlog with
PBI-001 and PBI-003 done, PBI-002 ready, PBI-004 new), `sprints/sprint-001/`
(sprint, review, retrospective), `impediments.md`, and `metrics.md`.
Sprint 001 also contains `threat-model.md`, which connects file-loss risks to
mitigations, tests, residual risk, and an owner.
