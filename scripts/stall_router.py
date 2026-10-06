#!/usr/bin/env python3
"""Apply the deterministic boundaries of the Scrum stall-recovery protocol."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


VALID_RISKS = {"normal", "high-impact", "irreversible"}
VALID_OUTCOMES = {"failed", "passed", "inconclusive"}
STAKEHOLDER_CAUSES = {"scope", "product-intent", "destructive-authority"}
ENVIRONMENT_CAUSES = {"environment", "tool", "permission"}


class PolicyError(ValueError):
    """Raised when the attempt record cannot be interpreted safely."""


def normalize_signature(value: str) -> str:
    normalized = value.strip().lower()
    normalized = re.sub(
        r"\b\d{4}-\d{2}-\d{2}[t ]\d{2}:\d{2}:\d{2}(?:\.\d+)?z?\b",
        "<time>",
        normalized,
    )
    normalized = re.sub(
        r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
        "<uuid>",
        normalized,
    )
    return " ".join(normalized.split())


def _number(value: Any, default: float = 0.0) -> float:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    return default


def _string_set(value: Any, field: str) -> set[str]:
    if value is None:
        return set()
    if not isinstance(value, list):
        raise PolicyError(f"{field} must be a list")
    return {str(item).strip().lower() for item in value if str(item).strip()}


def select_support(record: dict[str, Any]) -> dict[str, Any] | None:
    required = _string_set(
        record.get("required_capabilities", []), "required_capabilities"
    )
    required_authority = _string_set(
        record.get("required_authority", []), "required_authority"
    )
    candidates = record.get("available_support", [])
    if not isinstance(candidates, list):
        raise PolicyError("available_support must be a list")

    ranked: list[tuple[tuple[float, ...], dict[str, Any]]] = []
    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, dict) or not candidate.get("id"):
            raise PolicyError("Every support candidate needs an id")
        capabilities = _string_set(
            candidate.get("capabilities", []), "candidate capabilities"
        )
        authority = _string_set(candidate.get("authority", []), "candidate authority")
        if not required_authority <= authority:
            continue
        coverage = len(required & capabilities)
        full_match = int(not required or required <= capabilities)
        rank = (
            full_match,
            coverage,
            _number(candidate.get("diagnostic_strength")),
            _number(candidate.get("model_tier")),
            -_number(candidate.get("cost")),
            -float(index),
        )
        ranked.append((rank, candidate))
    if not ranked:
        return None
    return max(ranked, key=lambda item: item[0])[1]


def decide(record: dict[str, Any]) -> dict[str, Any]:
    attempts = record.get("attempts", [])
    if not isinstance(attempts, list):
        raise PolicyError("attempts must be a list")
    risk = str(record.get("risk", "normal"))
    if risk not in VALID_RISKS:
        raise PolicyError(f"risk must be one of: {', '.join(sorted(VALID_RISKS))}")
    cause = str(record.get("cause", "unknown"))
    budget = record.get("attempt_budget", 2)
    if not isinstance(budget, int) or isinstance(budget, bool) or budget < 1:
        raise PolicyError("attempt_budget must be a positive integer")
    if budget > 2:
        if not str(record.get("budget_extension_reason", "")).strip():
            raise PolicyError("An attempt budget above 2 needs budget_extension_reason")
        if not str(record.get("budget_extension_evidence", "")).strip():
            raise PolicyError("An attempt budget above 2 needs budget_extension_evidence")

    mutating: list[dict[str, Any]] = []
    for attempt in attempts:
        if not isinstance(attempt, dict):
            raise PolicyError("Every attempt must be an object")
        if attempt.get("mutating", True):
            for field in ("hypothesis", "action", "expected_result", "stop_condition"):
                if not str(attempt.get(field, "")).strip():
                    raise PolicyError(f"Every mutating attempt needs {field}")
            if not isinstance(attempt.get("progress"), bool):
                raise PolicyError("Every mutating attempt needs boolean progress")
            outcome = str(attempt.get("outcome", ""))
            if outcome not in VALID_OUTCOMES:
                raise PolicyError(
                    "Every mutating attempt outcome must be one of: "
                    f"{', '.join(sorted(VALID_OUTCOMES))}"
                )
            if outcome == "failed" and not str(attempt.get("failure_signature", "")).strip():
                raise PolicyError("Every failed mutating attempt needs failure_signature")
            mutating.append(attempt)

    rules = ["STALL-1", "STALL-2"]
    reasons: list[str] = []
    action = "continue"
    route = "next-discriminating-attempt"

    stall_minutes = _number(record.get("active_minutes_since_progress"), -1)
    stall_threshold = _number(record.get("stall_interval_minutes"), 2)
    if stall_threshold <= 0:
        raise PolicyError("stall_interval_minutes must be positive")
    review_rounds = record.get("review_rounds", 0)
    if not isinstance(review_rounds, int) or isinstance(review_rounds, bool) or review_rounds < 0:
        raise PolicyError("review_rounds must be a nonnegative integer")
    new_variants = record.get("new_variants_on_last_review", False)
    if not isinstance(new_variants, bool):
        raise PolicyError("new_variants_on_last_review must be boolean")

    repeated = False
    if len(mutating) >= 2:
        last_two = mutating[-2:]
        signatures = [
            normalize_signature(str(item.get("failure_signature", "")))
            for item in last_two
        ]
        repeated = bool(signatures[0]) and signatures[0] == signatures[1]
        repeated = repeated and all(item.get("outcome") == "failed" for item in last_two)
        repeated = repeated and not any(item["progress"] for item in last_two)

    last_outcome = mutating[-1]["outcome"] if mutating else None
    timed_stall = stall_minutes >= stall_threshold
    variation_loop = review_rounds >= 2 and new_variants
    if variation_loop:
        action = "pause-and-rebrief"
        route = "finite-variation-table"
        rules.extend(["STALL-4", "STALL-10"])
        reasons.append(
            "A second review introduced new variants; enumerate accepted "
            "variants and expected results before another review."
        )
    elif timed_stall:
        action = "pause-and-diagnose"
        route = "read-only-expert-consult"
        rules.extend(["STALL-4", "STALL-5", "STALL-9"])
        reasons.append(
            f"No progress event occurred for {stall_minutes:g} active minutes, "
            f"reaching the {stall_threshold:g}-minute threshold."
        )
    elif cause in STAKEHOLDER_CAUSES:
        action = "pause-and-ask-stakeholder"
        route = "stakeholder-decision"
        rules.extend(["STALL-4", "STALL-8"])
        reasons.append("The team lacks product scope, intent, or destructive authority.")
    elif cause in ENVIRONMENT_CAUSES:
        action = "pause-and-diagnose"
        route = "scout-or-impediment"
        rules.extend(["STALL-3", "STALL-4"])
        reasons.append(
            "Further code mutation cannot supply the missing environment, tool, or permission."
        )
    elif last_outcome == "passed":
        action = "ready-for-verification"
        route = "definition-of-done-gate"
        reasons.append("The latest attempt passed its stated discriminating check.")
    elif risk in {"high-impact", "irreversible"} and last_outcome == "failed":
        action = "pause-and-diagnose"
        route = "read-only-expert-consult"
        rules.extend(["STALL-3", "STALL-4", "STALL-5", "STALL-6"])
        reasons.append(
            "High-impact work requires outside diagnosis after its first failed mutation."
        )
    elif repeated:
        action = "pause-and-diagnose"
        route = "read-only-expert-consult"
        rules.extend(["STALL-3", "STALL-4", "STALL-5", "STALL-6"])
        reasons.append("Two consecutive attempts repeated the same failure without new evidence.")
    elif len(mutating) >= budget:
        action = "pause-and-diagnose"
        route = "read-only-expert-consult"
        rules.extend(["STALL-3", "STALL-4", "STALL-5", "STALL-6"])
        reasons.append(f"The mutating-attempt budget of {budget} is exhausted.")
    elif not mutating:
        reasons.append("No mutating attempt has run; state one hypothesis before editing.")
    else:
        reasons.append("The attempt budget remains and no mandatory stop condition fired.")

    selected = select_support(record) if action == "pause-and-diagnose" else None
    support_gap = (
        action == "pause-and-diagnose"
        and bool(record.get("available_support"))
        and selected is None
    )
    if selected:
        rules.append("STALL-5")
    if support_gap:
        reasons.append("No available support candidate has the required authority.")
    result = {
        "schema": 1,
        "action": action,
        "route": route,
        "rules": list(dict.fromkeys(rules)),
        "mutating_attempts_used": len(mutating),
        "attempt_budget": budget,
        "repeated_failure": repeated,
        "selected_support": selected.get("id") if selected else None,
        "support_gap": support_gap,
        "reason": " ".join(reasons),
    }
    if action.startswith("pause"):
        result["required_output"] = "blocker-packet"
    if action == "pause-and-rebrief":
        result["required_output"] = "finite-variation-table"
    return result


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate a JSON attempt record against core/stall-recovery.md"
    )
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        help="JSON file; omit to read JSON from standard input",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        raw = args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read()
        record = json.loads(raw)
        if not isinstance(record, dict):
            raise PolicyError("Input must be a JSON object")
        print(json.dumps(decide(record), indent=2))
        return 0
    except (OSError, json.JSONDecodeError, PolicyError) as error:
        print(f"stall-router: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
