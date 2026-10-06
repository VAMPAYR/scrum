from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import audit_health  # noqa: E402


class HealthAuditTests(unittest.TestCase):
    def test_malformed_execution_ledger_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / ".scrum" / "runtime"
            runtime.mkdir(parents=True)
            (runtime / "execution.json").write_text("{broken", encoding="utf-8")
            findings = audit_health.audit(root)
        self.assertTrue(any(item.startswith("FAIL:") and "ledger" in item for item in findings))

    def test_stale_lock_and_unacknowledged_message_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state = root / ".scrum"
            state.mkdir()
            (state / "session-lock.json").write_text(json.dumps({
                "status": "active", "started_at": "2026-01-01T00:00:00+00:00",
                "last_checkpoint": "2026-01-01T00:00:00+00:00", "stale_after_minutes": 45,
            }), encoding="utf-8")
            (state / "inbox.md").write_text("MSG-001: update the Sprint goal\n", encoding="utf-8")
            findings = audit_health.audit(root)
        self.assertTrue(any("lock" in item.lower() for item in findings))
        self.assertTrue(any("MSG-001" in item for item in findings))

    def test_open_outcome_without_successor_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / ".scrum" / "runtime"
            runtime.mkdir(parents=True)
            (runtime / "execution.json").write_text(json.dumps({
                "roster": {"Tier 2": 1}, "worker_starts": 1,
                "open_outcomes": ["ship"], "handoff": None,
            }), encoding="utf-8")
            findings = audit_health.audit(root)
        self.assertTrue(any(item.startswith("FAIL:") and "successor" in item for item in findings))

    def test_idle_extension_is_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / ".scrum" / "runtime"
            runtime.mkdir(parents=True)
            (runtime / "execution.json").write_text(json.dumps({
                "roster": {}, "worker_starts": 0, "open_outcomes": [],
                "timebox_extensions": [{"reason": "external-job"}],
            }), encoding="utf-8")
            findings = audit_health.audit(root)
        self.assertTrue(any(item.startswith("FAIL:") and "timebox" in item for item in findings))


if __name__ == "__main__":
    unittest.main()
