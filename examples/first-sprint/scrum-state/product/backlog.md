# Product Backlog

*Illustrative output from the fictional project in `examples/first-sprint/walkthrough.md`, not a real project's state.*

## Ordered items

### PBI-002: Rename every photo in a folder
- Status: ready
- Value: A user renames a whole shoot in one command instead of file by file.
- Order rationale: Top of the ready work. Batching a folder delivers the whole-shoot outcome the Product Goal names; single-file rename (PBI-001) already shipped, and the dry-run (PBI-003) already covers the preview path a batch run needs.
- Size: S
- Acceptance criteria:
  - [ ] `exif-rename ./shoot/` renames every supported image in the folder by its EXIF date.
  - [ ] Files that cannot be dated are skipped, listed on stderr, and do not stop the rest.
  - [ ] A summary line on stdout reports counts of renamed, skipped, and collided files.
- DoD evidence: <links/paths filled at completion>

### PBI-004: Rename HEIC photos from iPhone
- Status: draft
- Value: An iPhone shooter renames native HEIC photos, not only JPEG and camera files.
- Order rationale: New from the sprint-001 Review. Ordered below batch so the core whole-shoot outcome ships first; refine before forecast.
- Size: S
- Acceptance criteria:
  - [ ] `exif-rename photo.heic` reads the HEIC capture date and renames it the same way as a JPEG.
  - [ ] A HEIC file with no readable capture date follows the same skip-and-report path as a JPEG.
- DoD evidence: <links/paths filled at completion>

### PBI-001: Rename one photo by its capture date
- Status: done
- Value: A user renames a single photo to its capture date so it sorts by when it was taken.
- Order rationale: The foundation. Reading the EXIF date and producing a safe new name is what every later item builds on, so it went first.
- Size: S
- Acceptance criteria:
  - [x] A JPEG with an EXIF DateTimeOriginal is renamed to `YYYY-MM-DD_HHMMSS.jpg`.
  - [x] A photo with no readable EXIF date is left untouched, reported on stderr, and the command exits non-zero.
  - [x] When the target name already exists, the tool appends `-1`, `-2`, and so on, and never overwrites the existing file.
- DoD evidence: Gate PASS after one rework (see sprints/sprint-001/sprint.md, task "single-file rename"). Build `uv build` exit 0. Tests `uv run pytest` 14 passed, including test_renames_by_exif_date, test_no_date_left_untouched, and the rework test test_collision_appends_suffix. Lint and type `uv run ruff check .` and `uv run mypy src` clean. Tier 1.1: EXIF parsed through a guarded Pillow reader that rejects missing or malformed tags (test_corrupt_exif_rejected). Files: src/exif_rename/rename.py, src/exif_rename/cli.py, tests/test_rename.py, pyproject.toml.

### PBI-003: Preview renames without changing files (--dry-run)
- Status: done
- Value: A user previews every planned rename before committing, so a mistake costs nothing.
- Order rationale: Small, high safety value, and it reuses PBI-001's name-planning function, so it was forecast alongside it.
- Size: XS
- Acceptance criteria:
  - [x] `exif-rename --dry-run photo.jpg` prints the planned `old -> new` mapping to stdout and changes nothing on disk.
  - [x] The exit code is 0 when the file can be dated and non-zero when it cannot.
- DoD evidence: Gate PASS, no rework. Tests `uv run pytest` 14 passed, including test_dry_run_prints_mapping and test_dry_run_changes_nothing; the on-disk tree is byte-identical after `--dry-run`. Lint and type clean. CLI profile: `--help` lists `--dry-run`; exit 0 when datable, non-zero otherwise (test_dry_run_exit_codes). Files: src/exif_rename/cli.py, src/exif_rename/plan.py, tests/test_dry_run.py.

## Dropped items
- none
