# Sprint 001 threat model

*Illustrative output from the fictional project in `examples/first-sprint/walkthrough.md`, not a real project's state.*

## System model

The local CLI reads a user-selected JPEG and its EXIF metadata, derives a target
filename, and asks the local filesystem to rename the file. Trust changes at the
CLI argument, EXIF parser, path construction, and filesystem write. The product
has no network, shared identity, or remote service.

### TM-001: Malformed EXIF changes path behavior
- Scope and asset: source photo and destination path
- Boundary or entry point: JPEG and EXIF parser
- Condition or event: malformed, absent, oversized, or unexpected date metadata reaches naming logic
- Consequence: crash, invalid path, or unintended rename
- Assumptions: Pillow returns parser errors without modifying the source
- Treatment: reduce
- Mitigation: validate the parsed date and construct a filename from allowed characters only; leave the source untouched on error
- Verification: `test_no_date_left_untouched`, `test_corrupt_exif_rejected`, and boundary-value date tests
- Owner: Developers
- Residual risk and review point: new image formats may expose different parser behavior; revisit for PBI-004
- Status: mitigated

### TM-002: Two photos map to one target name
- Scope and asset: both source photos
- Boundary or entry point: filesystem destination lookup and rename
- Condition or event: two photos share a second-level timestamp or an existing file already owns the target
- Consequence: one photo is overwritten and lost
- Assumptions: the local filesystem provides the expected existence and rename semantics
- Treatment: avoid
- Mitigation: choose the first free numeric suffix before each write and never replace an existing path
- Verification: `test_collision_appends_suffix` plus a two-file CLI run
- Owner: Developers
- Residual risk and review point: race between lookup and rename remains until atomic no-replace behavior is implemented; stakeholder reviews before folder mode
- Status: mitigated

### TM-003: Partial failure leaves an unclear state
- Scope and asset: source photo and user trust in the operation
- Boundary or entry point: filesystem rename
- Condition or event: permission, disk, or process failure interrupts the operation
- Consequence: the user cannot tell which file changed or whether recovery is needed
- Assumptions: a single-file rename is atomic on supported local filesystems
- Treatment: reduce
- Mitigation: change one file at a time, report the exact source and destination, stop on failure, and never delete the source separately
- Verification: permission-failure test and recovery message review
- Owner: Developers
- Residual risk and review point: batch rollback semantics remain open for PBI-002
- Status: open
