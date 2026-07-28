# Impediments

### IMP-001: No test images with known EXIF timestamps
- Status: closed
- Blocker: The repo had no sample photos with known DateTimeOriginal values, so the rename output could not be asserted against a known-correct name.
- Owner: Developers
- Ask: A small set of fixture images with fixed, known EXIF capture dates.
- Sprint: sprint-001
- Raised: 2026-07-14
- Resolution: Generated three JPEG fixtures with Pillow, each stamped with a known DateTimeOriginal, committed under tests/fixtures/. Self-resolved by the Developers; no stakeholder action needed.
