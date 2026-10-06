from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import execution_guard  # noqa: E402


class ExecutionGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = execution_guard.load(Path("missing-state-for-test.json"))

    def test_worker_spawn_cannot_exceed_roster_total(self) -> None:
        execution_guard.set_roster(self.data, "Tier 2", 1)
        execution_guard.spawn(self.data, "reviewer", "Tier 2")
        execution_guard.stop_worker(
            self.data,
            "reviewer",
            "Reviewed task complete; evidence is in the Sprint log.",
        )
        with self.assertRaisesRegex(execution_guard.GuardError, "spawn limit"):
            execution_guard.spawn(self.data, "replacement", "Tier 2")

    def test_usage_threshold_stops_new_work(self) -> None:
        execution_guard.set_roster(self.data, "Tier 3", 2)
        execution_guard.add_usage(self.data, "weekly", 95, 95)
        with self.assertRaisesRegex(execution_guard.GuardError, "Usage threshold"):
            execution_guard.spawn(self.data, "dev-1", "Tier 3")

    def test_confirmed_handoff_requires_both_receipts(self) -> None:
        with self.assertRaisesRegex(execution_guard.GuardError, "successor identifier"):
            execution_guard.record_handoff(self.data, "", "receipt")
        with self.assertRaisesRegex(execution_guard.GuardError, "confirmation receipt"):
            execution_guard.record_handoff(self.data, "next-session", "")
        execution_guard.record_handoff(self.data, "next-session", "scheduler-query-17")
        self.assertEqual(self.data["handoff"]["successor_id"], "next-session")

    def test_paused_wait_does_not_count_as_active_time(self) -> None:
        execution_guard.start_timer(self.data)
        execution_guard.pause_timer(self.data, "stakeholder")
        status = execution_guard.timer_status(self.data["timer"])
        self.assertTrue(status["paused"])
        self.assertGreaterEqual(status["wall_seconds"], status["active_seconds"])
        with self.assertRaisesRegex(execution_guard.GuardError, "running timer"):
            execution_guard.pause_timer(self.data, "external-job")
        execution_guard.resume_timer(self.data)
        execution_guard.stop_timer(self.data)
        self.assertFalse(execution_guard.timer_status(self.data["timer"])["paused"])

    def test_completion_waits_for_successor_when_outcomes_remain(self) -> None:
        self.data["open_outcomes"] = ["finish-review"]
        with self.assertRaisesRegex(execution_guard.GuardError, "confirmed successor"):
            execution_guard.authorize_completion(self.data)
        execution_guard.record_handoff(self.data, "next-session", "receipt")
        execution_guard.authorize_completion(self.data)

    def test_idle_wait_cannot_extend_timebox(self) -> None:
        with self.assertRaisesRegex(execution_guard.GuardError, "Paused waits"):
            execution_guard.extend_timebox(
                self.data, "task", 600, "other", "waiting for usage reset"
            )
        execution_guard.extend_timebox(
            self.data,
            "task",
            600,
            "new-evidence",
            "A new reproducible failure requires coverage.",
        )
        self.assertEqual(len(self.data["timebox_extensions"]), 1)

    def test_state_round_trips_atomically(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "execution.json"
            execution_guard.set_roster(self.data, "Tier 1", 1)
            execution_guard.save(path, self.data)
            self.assertEqual(execution_guard.load(path)["roster"], {"Tier 1": 1})

    def test_active_session_lock_blocks_second_session(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            lock = Path(directory) / "session-lock.json"
            execution_guard.start_session(lock, "session-a", 45, False)
            with self.assertRaisesRegex(execution_guard.GuardError, "active lock"):
                execution_guard.start_session(lock, "session-b", 45, False)

    def test_session_end_requires_successor_for_open_work(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            lock_path = Path(directory) / "session-lock.json"
            execution_guard.start_session(lock_path, "session-a", 45, False)
            self.data["open_outcomes"] = ["pbi-1"]
            with self.assertRaisesRegex(execution_guard.GuardError, "confirmed successor"):
                execution_guard.end_session(lock_path, "session-a", self.data)
            execution_guard.record_handoff(self.data, "session-b", "schedule-query-1")
            with self.assertRaisesRegex(execution_guard.GuardError, "checkpoint"):
                execution_guard.end_session(lock_path, "session-a", self.data)
            execution_guard.checkpoint_session(lock_path, "session-a")
            result = execution_guard.end_session(lock_path, "session-a", self.data)
            self.assertEqual(result["status"], "stale")


if __name__ == "__main__":
    unittest.main()
