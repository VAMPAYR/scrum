#!/usr/bin/env python3
"""Run structural, context-route, and public-package checks for the skill."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import context_router


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".json", ".py", ".txt"}
PRIVATE_PATH_PATTERNS = {
    "Windows user path": re.compile(r"(?i)\b[a-z]:[\\/]users[\\/][^\\/\s`]+"),
    "Unix user path": re.compile(r"(?i)(?<![a-z0-9])/(?:users|home)/[^/\s`]+"),
    "file URI": re.compile(r"(?i)\bfile://"),
}
SOURCE_SUFFIXES = {".pdf", ".epub", ".mobi", ".azw", ".azw3", ".txt"}
PACKAGE_REF_RE = re.compile(
    r"`((?:core|adapters|templates|setup|scripts|tests|examples)/[^`\s]+|"
    r"(?:SKILL|README|AGENTS|CHANGELOG|CONTRIBUTING|ATTRIBUTION)\.md)`"
)


def distributable_paths() -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=PACKAGE_ROOT,
            capture_output=True,
            check=False,
        )
    except OSError:
        result = None
    if result is not None and result.returncode == 0:
        return [
            PACKAGE_ROOT / item.decode("utf-8", errors="surrogateescape")
            for item in result.stdout.split(b"\0")
            if item
        ]
    return [
        path
        for path in PACKAGE_ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts
    ]


def check_routes(errors: list[str]) -> None:
    try:
        config = context_router.load_config()
        context_router.validate_config(config)
        for stage in config["stages"]:
            combinations: list[tuple[str | None, list[str]]] = [(None, [])]
            combinations.extend((adapter, []) for adapter in config["adapters"])
            combinations.extend((None, [trigger]) for trigger in config["triggers"])
            for adapter, triggers in combinations:
                selection = context_router.resolve_route(
                    config, stage, triggers, adapter
                )
                if next(reversed(selection)) != "core/execution-checklist.md":
                    errors.append(f"route {stage} does not end with execution checkpoint")
                rendered = context_router.render_sources(selection)
                manifest = context_router.build_manifest(
                    stage, triggers, adapter, rendered
                )
                if manifest["estimated_tokens"] > context_router.DEFAULT_TOKEN_BUDGET:
                    label = adapter or (triggers[0] if triggers else "base")
                    errors.append(
                        f"route {stage}+{label} is approximately "
                        f"{manifest['estimated_tokens']} tokens, above "
                        f"{context_router.DEFAULT_TOKEN_BUDGET}"
                    )
    except (OSError, ValueError) as error:
        errors.append(f"context routes: {error}")


def check_stall_ownership(errors: list[str]) -> None:
    definitions: dict[str, list[str]] = {f"STALL-{number}": [] for number in range(1, 9)}
    for path in distributable_paths():
        if path.suffix.lower() != ".md" or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for rule in definitions:
            if re.search(rf"\*\*{re.escape(rule)},", text):
                definitions[rule].append(path.relative_to(PACKAGE_ROOT).as_posix())
    for rule, owners in definitions.items():
        if owners != ["core/stall-recovery.md"]:
            errors.append(f"{rule} must have one canonical owner; found {owners or 'none'}")


def check_public_package(errors: list[str]) -> None:
    for path in distributable_paths():
        if not path.is_file():
            continue
        relative = path.relative_to(PACKAGE_ROOT).as_posix()
        if path.suffix.lower() in SOURCE_SUFFIXES:
            errors.append(f"private source format present in package: {relative}")
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in PRIVATE_PATH_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{label} found in {relative}")

    ignore_path = PACKAGE_ROOT / ".gitignore"
    ignored = (
        set(ignore_path.read_text(encoding="utf-8").splitlines())
        if ignore_path.is_file()
        else set()
    )
    for ignore_pattern in (
        "sources/",
        "*.pdf",
        "*.epub",
        "*.mobi",
        "*.azw",
        "*.azw3",
        "*.txt",
    ):
        if ignore_pattern not in ignored:
            errors.append(f".gitignore is missing {ignore_pattern}")


def check_package_references(errors: list[str]) -> None:
    for path in distributable_paths():
        if path.suffix.lower() != ".md" or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for match in PACKAGE_REF_RE.finditer(text):
            reference = match.group(1).rstrip(".,;:")
            if reference.endswith("/") or any(
                marker in reference for marker in ("*", "<", ">")
            ):
                continue
            if not (PACKAGE_ROOT / reference).exists():
                relative = path.relative_to(PACKAGE_ROOT).as_posix()
                errors.append(f"broken package reference in {relative}: {reference}")


def main() -> int:
    errors: list[str] = []
    check_routes(errors)
    check_stall_ownership(errors)
    check_public_package(errors)
    check_package_references(errors)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: context routes, canonical stall rules, references, and privacy controls")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
