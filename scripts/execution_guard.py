#!/usr/bin/env python3
"""Enforce small, auditable execution limits for Scrum project sessions."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_STATE = Path(".scrum/runtime/execution.json")


class GuardError(ValueError):
    """Raised when a requested action violates the recorded operating limits."""


def now() -> datetime:
    return datetime.now(timezone.utc)


def stamp(value: datetime | None = None) -> str:
    return (value or now()).isoformat(timespec="seconds")


def load(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"schema": 1, "roster": {}, "workers": {}, "timer": None,
                "usage": {}, "handoff": None, "open_outcomes": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise GuardError(f"Cannot read execution state {path}: {error}") from error
    if data.get("schema") != 1:
        raise GuardError("Unsupported execution-state schema")
    return data


def save(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def set_roster(data: dict[str, Any], seat: str, limit: int, reason: str = "") -> None:
    if limit < 1:
        raise GuardError("Roster limits must be positive")
    previous = data["roster"].get(seat)
    active = sum(
        1 for worker in data["workers"].values()
        if worker["active"] and worker["seat"] == seat
    )
    if active > limit:
        raise GuardError("Roster change cannot reduce a seat below its active workers")
    if previous is not None and previous != limit and not reason.strip():
        raise GuardError("A roster change requires a recorded reason")
    data["roster"][seat] = limit
    if previous is not None and previous != limit:
        data.setdefault("roster_changes", []).append({
            "seat": seat,
            "from": previous,
            "to": limit,
            "reason": reason,
            "recorded_at": stamp(),
        })


def spawn(data: dict[str, Any], agent: str, seat: str) -> None:
    if any(item.get("pause_new_work") for item in data.get("usage", {}).values()):
        raise GuardError("Usage threshold reached; do not start new work")
    if seat not in data["roster"]:
        raise GuardError(f"Seat {seat!r} is absent from the recorded roster")
    if any(
        worker["seat"] == seat and not worker["active"]
        and not worker.get("handoff_note")
        for worker in data["workers"].values()
    ):
        raise GuardError(f"Seat {seat!r} needs an outgoing handoff note before refill")
    active = sum(1 for worker in data["workers"].values() if worker["active"])
    occupied = sum(
        1 for worker in data["workers"].values()
        if worker["active"] and worker["seat"] == seat
    )
    if occupied >= data["roster"][seat]:
        raise GuardError(f"Roster limit reached for seat {seat!r}")
    total_limit = sum(data["roster"].values())
    total_started = data.get("worker_starts", 0)
    if total_started >= total_limit:
        raise GuardError("Sprint worker-spawn limit reached")
    data["workers"][agent] = {"seat": seat, "active": True, "started_at": stamp()}
    data["worker_starts"] = total_started + 1
    data["max_concurrent_seen"] = max(data.get("max_concurrent_seen", 0), active + 1)


def stop_worker(data: dict[str, Any], agent: str, handoff_note: str = "") -> None:
    worker = data["workers"].get(agent)
    if not worker or not worker["active"]:
        raise GuardError(f"No active roster seat for {agent!r}")
    worker["active"] = False
    worker["ended_at"] = stamp()
    worker["handoff_note"] = handoff_note.strip()


def start_timer(data: dict[str, Any]) -> None:
    if data["timer"] and not data["timer"].get("stopped_at"):
        raise GuardError("An active timer already exists")
    data["timer"] = {
        "started_at": stamp(),
        "active_seconds": 0,
        "paused_at": None,
        "pause_reason": None,
        "stopped_at": None,
    }


def pause_timer(data: dict[str, Any], reason: str) -> None:
    timer = data.get("timer")
    if not timer or timer.get("stopped_at") or timer.get("paused_at"):
        raise GuardError("No running timer is available to pause")
    current = now()
    timer["active_seconds"] += max(0, int((current - datetime.fromisoformat(
        timer.get("last_resumed_at") or timer["started_at"]
    )).total_seconds()))
    timer["paused_at"] = stamp(current)
    timer["pause_reason"] = reason


def extend_timebox(data: dict[str, Any], name: str, seconds: int,
                   reason_class: str, reason: str) -> None:
    allowed = {"new-evidence", "scope-change", "technical-dependency", "other"}
    if seconds < 1 or not reason.strip() or reason_class not in allowed:
        raise GuardError(
            "A positive extension, allowed reason class, and detail are required"
        )
    if re.search(
        r"\b(idle|wait(?:ing)?|stakeholder|reset|external job)\b", reason, re.I
    ):
        raise GuardError("Paused waits do not justify a timebox extension")
    data.setdefault("timebox_extensions", []).append(
        {
            "name": name,
            "seconds": seconds,
            "reason_class": reason_class,
            "reason": reason,
            "recorded_at": stamp(),
        }
    )


def resume_timer(data: dict[str, Any]) -> None:
    timer = data.get("timer")
    if not timer or not timer.get("paused_at") or timer.get("stopped_at"):
        raise GuardError("No paused timer is available to resume")
    timer["last_resumed_at"] = stamp()
    timer["paused_at"] = None
    timer["pause_reason"] = None


def stop_timer(data: dict[str, Any]) -> None:
    timer = data.get("timer")
    if not timer or timer.get("stopped_at"):
        raise GuardError("No active timer is available to stop")
    current = now()
    if not timer.get("paused_at"):
        timer["active_seconds"] += max(0, int((current - datetime.fromisoformat(
            timer.get("last_resumed_at") or timer["started_at"]
        )).total_seconds()))
    timer["stopped_at"] = stamp(current)


def timer_status(timer: dict[str, Any]) -> dict[str, int | str | None]:
    started_at = datetime.fromisoformat(timer["started_at"])
    wall_end = datetime.fromisoformat(timer["stopped_at"] or stamp())
    active = timer["active_seconds"]
    if not timer["paused_at"] and not timer["stopped_at"]:
        active += max(0, int((wall_end - datetime.fromisoformat(
            timer.get("last_resumed_at") or timer["started_at"]
        )).total_seconds()))
    return {
        "active_seconds": active,
        "wall_seconds": max(0, int((wall_end - started_at).total_seconds())),
        "paused": bool(timer["paused_at"]),
        "pause_reason": timer["pause_reason"],
    }


def add_usage(data: dict[str, Any], window: str, percent: float, threshold: float) -> None:
    if not 0 <= percent <= 100 or not 0 < threshold <= 100:
        raise GuardError("Usage and pause threshold must be within 0–100 percent")
    data["usage"][window] = {
        "percent": percent,
        "recorded_at": stamp(),
        "pause_new_work": percent >= threshold,
    }


def record_handoff(data: dict[str, Any], successor: str, receipt: str) -> None:
    if not successor.strip() or not receipt.strip():
        raise GuardError("Handoff requires a successor identifier and confirmation receipt")
    data["handoff"] = {
        "successor_id": successor,
        "confirmation_receipt": receipt,
        "confirmed_at": stamp(),
    }


def authorize_completion(data: dict[str, Any]) -> None:
    handoff = data.get("handoff") or {}
    if data.get("open_outcomes") and not (
        handoff.get("successor_id") and handoff.get("confirmation_receipt")
    ):
        raise GuardError("Open outcomes require a confirmed successor before session end")


def start_session(lock_path: Path, session_id: str, stale_after: int,
                  stale_confirmed: bool) -> dict[str, Any]:
    current = now()
    previous = None
    if lock_path.is_file():
        try:
            previous = json.loads(lock_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise GuardError(f"Cannot read session lock: {error}") from error
        if not isinstance(previous, dict):
            raise GuardError("Session lock must contain a JSON object")
        if previous.get("status") == "active":
            try:
                checkpoint = datetime.fromisoformat(previous["last_checkpoint"])
                age = (current - checkpoint).total_seconds() / 60
            except (KeyError, TypeError, ValueError) as error:
                raise GuardError("Active session lock lacks a valid checkpoint") from error
            if age < stale_after:
                raise GuardError(
                    f"Session {previous.get('session_id')} has an active lock "
                    f"({age:.0f} minutes old)"
                )
            if not stale_confirmed:
                raise GuardError("Stale lock requires inspection and --stale-confirmed")
    lock = {
        "schema": 1,
        "session_id": session_id,
        "started_at": stamp(current),
        "last_checkpoint": stamp(current),
        "checkpoint_count": 0,
        "status": "active",
        "stale_after_minutes": stale_after,
        "previous_session": previous,
    }
    save(lock_path, lock)
    return lock


def checkpoint_session(lock_path: Path, session_id: str) -> dict[str, Any]:
    lock = load_lock(lock_path, session_id)
    lock["last_checkpoint"] = stamp()
    lock["checkpoint_count"] = lock.get("checkpoint_count", 0) + 1
    save(lock_path, lock)
    return lock


def load_lock(path: Path, session_id: str) -> dict[str, Any]:
    try:
        lock = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise GuardError(f"Cannot read session lock: {error}") from error
    if lock.get("session_id") != session_id or lock.get("status") != "active":
        raise GuardError("Session ID does not own the active lock")
    return lock


def end_session(lock_path: Path, session_id: str, data: dict[str, Any]) -> dict[str, Any]:
    authorize_completion(data)
    lock = load_lock(lock_path, session_id)
    if lock.get("checkpoint_count", 0) < 1:
        raise GuardError("A saved checkpoint is required before session end")
    lock["status"] = "stale"
    lock["ended_at"] = stamp()
    save(lock_path, lock)
    return lock


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--state", type=Path, default=DEFAULT_STATE)
    p.add_argument("--project-root", type=Path, default=Path.cwd())
    sub = p.add_subparsers(dest="command", required=True)
    roster = sub.add_parser("roster-set")
    roster.add_argument("seat")
    roster.add_argument("--limit", type=int, required=True)
    roster.add_argument("--reason", default="")
    launch = sub.add_parser("worker-start")
    launch.add_argument("agent")
    launch.add_argument("seat")
    stop = sub.add_parser("worker-stop")
    stop.add_argument("agent")
    stop.add_argument("--handoff-note", default="")
    sub.add_parser("timer-start")
    pause = sub.add_parser("pause-timer")
    pause.add_argument(
        "--reason",
        required=True,
        choices=["stakeholder", "usage-reset", "external-job"],
    )
    sub.add_parser("resume-timer")
    sub.add_parser("stop-timer")
    usage = sub.add_parser("record-usage")
    usage.add_argument("window")
    usage.add_argument("--percent", type=float, required=True)
    usage.add_argument("--threshold", type=float, default=95)
    handoff = sub.add_parser("record-handoff")
    handoff.add_argument("--successor-id", required=True)
    handoff.add_argument("--confirmation-receipt", required=True)
    outcomes = sub.add_parser("set-open-outcomes")
    outcomes.add_argument("ids", nargs="*")
    extension = sub.add_parser("extend-timebox")
    extension.add_argument("name")
    extension.add_argument("--seconds", type=int, required=True)
    extension.add_argument(
        "--reason-class",
        choices=["new-evidence", "scope-change", "technical-dependency", "other"],
        required=True,
    )
    extension.add_argument("--reason", required=True)
    sub.add_parser("authorize-completion")
    start = sub.add_parser("session-start")
    start.add_argument("--session-id", required=True)
    start.add_argument("--stale-after-minutes", type=int, default=45)
    start.add_argument("--stale-confirmed", action="store_true")
    checkpoint = sub.add_parser("session-checkpoint")
    checkpoint.add_argument("--session-id", required=True)
    end = sub.add_parser("session-end")
    end.add_argument("--session-id", required=True)
    sub.add_parser("status")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        data = load(args.state)
        if args.command == "roster-set":
            set_roster(data, args.seat, args.limit, args.reason)
        elif args.command == "worker-start":
            spawn(data, args.agent, args.seat)
        elif args.command == "worker-stop":
            stop_worker(data, args.agent, args.handoff_note)
        elif args.command == "timer-start":
            start_timer(data)
        elif args.command == "pause-timer":
            pause_timer(data, args.reason)
        elif args.command == "resume-timer":
            resume_timer(data)
        elif args.command == "stop-timer":
            stop_timer(data)
        elif args.command == "record-usage":
            add_usage(data, args.window, args.percent, args.threshold)
        elif args.command == "record-handoff":
            record_handoff(data, args.successor_id, args.confirmation_receipt)
        elif args.command == "set-open-outcomes":
            data["open_outcomes"] = args.ids
        elif args.command == "extend-timebox":
            extend_timebox(
                data, args.name, args.seconds, args.reason_class, args.reason
            )
        elif args.command == "authorize-completion":
            authorize_completion(data)
        elif args.command == "session-start":
            if args.stale_after_minutes < 1:
                raise GuardError("Stale-lock interval must be positive")
            lock = start_session(
                args.project_root / ".scrum" / "session-lock.json",
                args.session_id,
                args.stale_after_minutes,
                args.stale_confirmed,
            )
            print(json.dumps(
                {"command": args.command, "result": "passed", "lock": lock},
                indent=2,
            ))
            return 0
        elif args.command == "session-checkpoint":
            lock = checkpoint_session(
                args.project_root / ".scrum" / "session-lock.json", args.session_id
            )
            print(json.dumps(
                {"command": args.command, "result": "passed", "lock": lock},
                indent=2,
            ))
            return 0
        elif args.command == "session-end":
            lock = end_session(
                args.project_root / ".scrum" / "session-lock.json",
                args.session_id,
                data,
            )
            print(json.dumps(
                {"command": args.command, "result": "passed", "lock": lock},
                indent=2,
            ))
            return 0
        if args.command == "status":
            result = dict(data)
            if data.get("timer"):
                result["timer_status"] = timer_status(data["timer"])
            print(json.dumps(result, indent=2))
            return 0
        save(args.state, data)
        print(json.dumps({"command": args.command, "result": "passed"}, indent=2))
        return 0
    except (OSError, GuardError, ValueError) as error:
        print(f"execution-guard: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
