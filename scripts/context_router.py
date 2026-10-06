#!/usr/bin/env python3
"""Build a bounded Scrum instruction bundle from verbatim source sections."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any, Iterable


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = PACKAGE_ROOT / "core" / "context-routes.json"
DEFAULT_TOKEN_BUDGET = 32_000
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")

STAGE_ALIASES = {
    "founding": "0",
    "vision": "1",
    "refinement": "2",
    "planning": "3",
    "execution": "4",
    "sprint": "4",
    "review": "5",
    "retro": "6",
    "retrospective": "6",
    "health": "health",
    "dod": "dod",
}


class RouteError(ValueError):
    """Raised when a route points to missing or ambiguous source content."""


class BudgetExceeded(RouteError):
    """Raised instead of silently truncating a context bundle."""


def load_config(path: Path = DEFAULT_CONFIG) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)
    if config.get("schema") != 1:
        raise RouteError(f"Unsupported context-route schema: {config.get('schema')!r}")
    return config


def normalize_stage(value: str) -> str:
    normalized = value.strip().lower()
    return STAGE_ALIASES.get(normalized, normalized)


def _headings(lines: list[str]) -> list[tuple[int, int, str]]:
    found: list[tuple[int, int, str]] = []
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line.rstrip("\r\n"))
        if match:
            found.append((index, len(match.group(1)), match.group(2)))
    return found


def section_ranges(text: str, names: Iterable[str], source: str) -> list[tuple[int, int]]:
    lines = text.splitlines(keepends=True)
    requested = list(names)
    if not requested:
        raise RouteError(f"No sections configured for {source}")
    if "*" in requested:
        if len(requested) != 1:
            raise RouteError(f"Wildcard must be the only section for {source}")
        return [(0, len(lines))]

    headings = _headings(lines)
    ranges: list[tuple[int, int]] = []
    for name in requested:
        selector = HEADING_RE.match(name)
        if selector:
            selected_level = len(selector.group(1))
            selected_title = selector.group(2)
            matches = [
                entry
                for entry in headings
                if entry[1] == selected_level and entry[2] == selected_title
            ]
        else:
            matches = [entry for entry in headings if entry[2] == name]
        if not matches:
            raise RouteError(f"Missing heading {name!r} in {source}")
        if len(matches) > 1:
            raise RouteError(f"Ambiguous heading {name!r} in {source}")
        start, level, _ = matches[0]
        end = len(lines)
        for candidate_start, candidate_level, _ in headings:
            if candidate_start > start and candidate_level <= level:
                end = candidate_start
                break
        ranges.append((start, end))

    merged: list[list[int]] = []
    for start, end in sorted(ranges):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return [(start, end) for start, end in merged]


def extract_sections(text: str, names: Iterable[str], source: str) -> str:
    lines = text.splitlines(keepends=True)
    chunks = [
        "".join(lines[start:end]).rstrip()
        for start, end in section_ranges(text, names, source)
    ]
    return "\n\n".join(chunk for chunk in chunks if chunk) + "\n"


def safe_source_path(package_root: Path, relative_path: str) -> Path:
    root = package_root.resolve()
    candidate = (root / relative_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise RouteError(f"Routed source escapes the package: {relative_path}") from error
    return candidate


def safe_project_source_path(project_root: Path, relative_path: str) -> Path:
    root = project_root.resolve()
    candidate = (root / relative_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise RouteError(f"Project source escapes the project: {relative_path}") from error
    return candidate


def _append_sources(
    collected: "OrderedDict[str, list[str]]", sources: Iterable[dict[str, Any]]
) -> None:
    for source in sources:
        path = source["path"]
        sections = list(source["sections"])
        if path not in collected:
            collected[path] = []
        if "*" in collected[path]:
            continue
        if "*" in sections:
            collected[path] = ["*"]
            continue
        for section in sections:
            if section not in collected[path]:
                collected[path].append(section)


def resolve_route(
    config: dict[str, Any], stage: str, triggers: Iterable[str], adapter: str | None
) -> "OrderedDict[str, list[str]]":
    stage_key = normalize_stage(stage)
    if stage_key not in config["stages"]:
        choices = ", ".join(config["stages"].keys())
        raise RouteError(f"Unknown stage {stage!r}; choose one of: {choices}")

    collected: "OrderedDict[str, list[str]]" = OrderedDict()
    _append_sources(collected, config["always"])
    _append_sources(collected, config["stages"][stage_key]["sources"])

    for trigger in triggers:
        if trigger not in config["triggers"]:
            choices = ", ".join(config["triggers"].keys())
            raise RouteError(f"Unknown trigger {trigger!r}; choose one of: {choices}")
        _append_sources(collected, config["triggers"][trigger])

    if adapter:
        if adapter not in config["adapters"]:
            choices = ", ".join(config["adapters"].keys())
            raise RouteError(f"Unknown adapter {adapter!r}; choose one of: {choices}")
        _append_sources(collected, config["adapters"][adapter])
    _append_sources(collected, config["final"])
    return collected


def render_sources(
    selections: "OrderedDict[str, list[str]]",
    package_root: Path = PACKAGE_ROOT,
    project_root: Path = Path.cwd(),
) -> list[dict[str, Any]]:
    rendered: list[dict[str, Any]] = []
    for relative_path, sections in selections.items():
        project_source = relative_path.startswith(".scrum/")
        path = (
            safe_project_source_path(project_root, relative_path)
            if project_source
            else safe_source_path(package_root, relative_path)
        )
        if not path.is_file():
            if project_source and relative_path == ".scrum/directives.md":
                content = (
                    "<!-- Project directives are not initialized. Copy "
                    "templates/directives.md to .scrum/directives.md during founding. -->\n"
                )
                rendered.append({"path": relative_path, "sections": sections,
                                 "content": content, "characters": len(content),
                                 "estimated_tokens": math.ceil(len(content) / 4)})
                continue
            raise RouteError(f"Missing routed source: {relative_path}")
        text = path.read_text(encoding="utf-8")
        content = extract_sections(text, sections, relative_path)
        rendered.append(
            {
                "path": relative_path,
                "sections": sections,
                "content": content,
                "characters": len(content),
                "estimated_tokens": math.ceil(len(content) / 4),
            }
        )
    return rendered


def build_manifest(
    stage: str,
    triggers: list[str],
    adapter: str | None,
    rendered: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "schema": 1,
        "stage": normalize_stage(stage),
        "triggers": triggers,
        "adapter": adapter,
        "characters": sum(item["characters"] for item in rendered),
        "estimated_tokens": sum(item["estimated_tokens"] for item in rendered),
        "sources": [
            {
                "path": item["path"],
                "sections": item["sections"],
                "characters": item["characters"],
                "estimated_tokens": item["estimated_tokens"],
            }
            for item in rendered
        ],
    }


def render_bundle(manifest: dict[str, Any], rendered: list[dict[str, Any]]) -> str:
    lines = [
        "<!-- generated by scripts/context_router.py; source files remain canonical -->",
        (
            f"<!-- stage={manifest['stage']} estimated_tokens="
            f"{manifest['estimated_tokens']} sources={len(rendered)} -->"
        ),
        "",
    ]
    for item in rendered:
        sections = ", ".join(item["sections"])
        lines.extend(
            [
                f"<!-- context-source: {item['path']} | sections: {sections} -->",
                item["content"].rstrip(),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def enforce_budget(
    manifest: dict[str, Any], max_estimated_tokens: int, allow_over_budget: bool = False
) -> None:
    if max_estimated_tokens < 1:
        raise RouteError("Token budget must be a positive integer")
    if manifest["estimated_tokens"] <= max_estimated_tokens or allow_over_budget:
        return
    raise BudgetExceeded(
        "Context route is approximately "
        f"{manifest['estimated_tokens']} tokens, above the "
        f"{max_estimated_tokens} budget. Split the operation by stage or "
        "trigger, or pass --allow-over-budget. No content was emitted."
    )


def validate_config(config: dict[str, Any], package_root: Path = PACKAGE_ROOT) -> None:
    groups: list[Iterable[dict[str, Any]]] = [config["always"]]
    groups.extend(route["sources"] for route in config["stages"].values())
    groups.extend(config["triggers"].values())
    groups.extend(config["adapters"].values())
    groups.append(config["final"])
    for sources in groups:
        for source in sources:
            relative_path = source["path"]
            if relative_path.startswith(".scrum/"):
                continue
            path = safe_source_path(package_root, relative_path)
            if not path.is_file():
                raise RouteError(f"Missing routed source: {relative_path}")
            section_ranges(
                path.read_text(encoding="utf-8"), source["sections"], relative_path
            )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Emit exact Scrum source sections for one stage. The router never "
            "summarizes or silently truncates knowledge."
        )
    )
    parser.add_argument("--stage", required=True, help="Stage number or name")
    parser.add_argument(
        "--trigger",
        action="append",
        default=[],
        help="Add a conditional route; repeat for multiple triggers",
    )
    parser.add_argument(
        "--adapter",
        choices=["parallel-agents", "terminal-agent", "single-model"],
    )
    parser.add_argument(
        "--manifest",
        action="store_true",
        help="Print route metadata as JSON instead of source content",
    )
    parser.add_argument(
        "--max-estimated-tokens",
        type=int,
        default=DEFAULT_TOKEN_BUDGET,
        help=(
            "Fail rather than emit an oversized bundle; estimates use four "
            "characters per token and content is never truncated"
        ),
    )
    parser.add_argument(
        "--allow-over-budget",
        action="store_true",
        help="Emit the complete bundle even when it exceeds the configured budget",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Project root containing .scrum/ state (defaults to the current directory)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        config = load_config(args.config)
        validate_config(config)
        selections = resolve_route(config, args.stage, args.trigger, args.adapter)
        rendered = render_sources(selections, project_root=args.project_root)
        manifest = build_manifest(args.stage, args.trigger, args.adapter, rendered)
        if args.manifest:
            print(json.dumps(manifest, indent=2))
            return 0
        enforce_budget(manifest, args.max_estimated_tokens, args.allow_over_budget)
        sys.stdout.write(render_bundle(manifest, rendered))
        return 0
    except (OSError, json.JSONDecodeError, RouteError) as error:
        print(f"context-router: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
