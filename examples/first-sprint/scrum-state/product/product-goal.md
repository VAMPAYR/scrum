# Product Goal

## Purpose
- This product exists in order to give a photographer chronologically sortable filenames drawn from each photo's capture date, without renaming by hand.
- This product does not exist in order to edit, tag, upload, or organize photos into albums.

## Target future state
A small command-line tool that renames one photo or a whole folder to its EXIF capture date, previews the change safely before touching disk, never overwrites an existing file, and runs entirely on the local machine.

## Who it is for
- Primary user(s): hobbyist and semi-professional photographers who offload memory cards to a computer.
- Their need this product addresses: camera filenames such as IMG_1234.JPG do not sort by time across cards, cameras, or devices, so a mixed shoot loses its chronological order.

## Value measures
- Manual renaming time removed: a full card is renamed in one command instead of file by file.
- How we will know the Goal is being approached: the stakeholder stops renaming photos by hand.

## Boundaries and constraints
- In scope: rename by EXIF date, single file and whole folder, dry-run preview, collision safety.
- Out of scope: photo editing, tagging, uploading, and album management.
- Constraints: Python 3.12; runs locally; no network calls; image data never leaves the machine.

## Status
- Set: 2026-07-14
- State: active
- Last reviewed: 2026-07-14, at Sprint Review
