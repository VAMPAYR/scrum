#!/usr/bin/env python3
"""Check persisted Scrum continuity and execution state without changing it."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else None
    except (OSError, json.JSONDecodeError):
        return None


def audit(project: Path, max_changes: int = 100) -> list[str]:
    state = project / ".scrum"
    findings: list[str] = []
    execution_path = state / "runtime" / "execution.json"
    lock_path = state / "session-lock.json"
    execution = read_json(execution_path)
    lock = read_json(lock_path)
    if execution_path.exists() and execution is None:
        findings.append("FAIL: execution ledger is unreadable or malformed")
    if lock_path.exists() and lock is None:
        findings.append("FAIL: session lock is unreadable or malformed")
    if lock:
        last = lock.get("last_checkpoint") or lock.get("started_at")
        try:
            age_minutes = (
                datetime.now(timezone.utc) - datetime.fromisoformat(last)
            ).total_seconds() / 60
            stale_after = int(lock.get("stale_after_minutes", 45))
            if age_minutes > stale_after and lock.get("status") == "active":
                findings.append(
                    f"WARN: active session lock is {age_minutes:.0f} minutes old; "
                    "inspect its owner before resuming"
                )
        except (TypeError, ValueError):
            findings.append(
                "WARN: session lock has no valid checkpoint timestamp"
            )
    elif (state / "state.md").is_file():
        findings.append("WARN: Scrum state exists without a session lock")

    inbox = state / "inbox.md"
    if inbox.is_file():
        content = inbox.read_text(encoding="utf-8")
        messages = set(re.findall(r"\b(MSG-[A-Za-z0-9_-]+)\b", content))
        acknowledgments = set(re.findall(r"\bACK-(MSG-[A-Za-z0-9_-]+)\b", content))
        pending = sorted(messages - acknowledgments)
        if pending:
            findings.append(
                "WARN: inbox messages lack acknowledgment: "
                f"{', '.join(pending)}"
            )

    if execution:
        roster = execution.get("roster", {})
        started = execution.get("worker_starts", 0)
        limit = sum(value for value in roster.values() if isinstance(value, int))
        if started > limit:
            findings.append(
                f"FAIL: worker starts ({started}) exceed roster total ({limit})"
            )
        active_by_seat: dict[str, int] = {}
        for worker in execution.get("workers", {}).values():
            if worker.get("active"):
                seat = worker.get("seat", "<missing>")
                active_by_seat[seat] = active_by_seat.get(seat, 0) + 1
        for seat, active in active_by_seat.items():
            if active > roster.get(seat, 0):
                findings.append(
                    f"FAIL: active workers for {seat} ({active}) exceed the "
                    "recorded seat limit"
                )
        for change in execution.get("roster_changes", []):
            if not change.get("reason"):
                findings.append(
                    "FAIL: roster limit changed without a recorded reason"
                )
                break
        for extension in execution.get("timebox_extensions", []):
            allowed_reasons = {
                "new-evidence", "scope-change", "technical-dependency", "other"
            }
            idle_reason = re.search(
                r"\b(idle|wait(?:ing)?|stakeholder|reset|external job)\b",
                extension.get("reason", ""),
                re.I,
            )
            if extension.get("reason_class") not in allowed_reasons or idle_reason:
                findings.append(
                    "FAIL: timebox extension records a paused wait as its reason"
                )
                break
        outcomes = execution.get("open_outcomes", [])
        handoff = execution.get("handoff") or {}
        if outcomes and not (
            handoff.get("successor_id") and handoff.get("confirmation_receipt")
        ):
            findings.append("FAIL: open outcomes have no confirmed successor")

    team = state / "team.md"
    commit_mode = team.is_file() and re.search(
        r"(?im)^-\s*Mode:\s*(commit|branch-pr)\b",
        team.read_text(encoding="utf-8"),
    )
    if commit_mode:
        result = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=all"],
            cwd=project,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            count = sum(bool(line.strip()) for line in result.stdout.splitlines())
            if count >= max_changes:
                findings.append(
                    f"WARN: {count} uncommitted paths meet or exceed the "
                    f"limit ({max_changes})"
                )
        else:
            findings.append(
                "WARN: cannot inspect Git change count in this project"
            )

    if not findings:
        findings.append("PASS: no continuity or execution-health findings")
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--max-uncommitted", type=int, default=100)
    args = parser.parse_args(argv)
    findings = audit(args.project_root.resolve(), args.max_uncommitted)
    for finding in findings:
        print(finding)
    return 1 if any(item.startswith("FAIL:") for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
