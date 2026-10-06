from __future__ import annotations

import sys
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT / "scripts"))

import stall_router  # noqa: E402


def attempt(
    signature: str, progress: bool = False, outcome: str = "failed"
) -> dict[str, object]:
    return {
        "mutating": True,
        "hypothesis": "a stated cause",
        "action": "one discriminating probe",
        "expected_result": "a result that separates two explanations",
        "stop_condition": "stop if the signature repeats",
        "failure_signature": signature,
        "progress": progress,
        "outcome": outcome,
    }


class StallRouterTests(unittest.TestCase):
    def test_active_time_without_progress_escalates(self) -> None:
        result = stall_router.decide({"attempts": [], "active_minutes_since_progress": 2})
        self.assertEqual(result["action"], "pause-and-diagnose")
        self.assertIn("STALL-9", result["rules"])

    def test_second_review_with_new_variants_requires_finite_table(self) -> None:
        result = stall_router.decide({"attempts": [], "review_rounds": 2,
                                      "new_variants_on_last_review": True})
        self.assertEqual(result["route"], "finite-variation-table")
        self.assertIn("STALL-10", result["rules"])

    def test_one_normal_failure_can_continue(self) -> None:
        result = stall_router.decide({"attempts": [attempt("E1")], "risk": "normal"})
        self.assertEqual(result["action"], "continue")

    def test_repeated_failure_stops_before_more_mutation(self) -> None:
        result = stall_router.decide(
            {"attempts": [attempt("same error"), attempt(" SAME   ERROR ")], "risk": "normal"}
        )
        self.assertEqual(result["action"], "pause-and-diagnose")
        self.assertTrue(result["repeated_failure"])
        self.assertIn("STALL-4", result["rules"])

    def test_attempt_budget_stops_distinct_failures(self) -> None:
        result = stall_router.decide(
            {"attempts": [attempt("first"), attempt("second")], "risk": "normal"}
        )
        self.assertEqual(result["action"], "pause-and-diagnose")
        self.assertIn("budget", result["reason"].lower())

    def test_high_impact_failure_gets_early_review(self) -> None:
        result = stall_router.decide(
            {"attempts": [attempt("danger")], "risk": "high-impact"}
        )
        self.assertEqual(result["route"], "read-only-expert-consult")

    def test_capability_outranks_general_model_tier(self) -> None:
        result = stall_router.decide(
            {
                "attempts": [attempt("one"), attempt("two")],
                "required_capabilities": ["postgresql"],
                "required_authority": ["repo-read"],
                "available_support": [
                    {
                        "id": "largest-general-model",
                        "capabilities": ["general"],
                        "authority": ["repo-read"],
                        "diagnostic_strength": 5,
                        "model_tier": 5,
                        "cost": 5,
                    },
                    {
                        "id": "database-specialist",
                        "capabilities": ["postgresql"],
                        "authority": ["repo-read"],
                        "diagnostic_strength": 4,
                        "model_tier": 3,
                        "cost": 2,
                    },
                ],
            }
        )
        self.assertEqual(result["selected_support"], "database-specialist")

    def test_unauthorized_specialist_is_not_selected(self) -> None:
        result = stall_router.decide(
            {
                "attempts": [attempt("one"), attempt("two")],
                "required_capabilities": ["postgresql"],
                "required_authority": ["production-read"],
                "available_support": [
                    {
                        "id": "database-specialist",
                        "capabilities": ["postgresql"],
                        "authority": ["repo-read"],
                        "diagnostic_strength": 5,
                    }
                ],
            }
        )
        self.assertIsNone(result["selected_support"])
        self.assertTrue(result["support_gap"])

    def test_extended_budget_requires_new_evidence(self) -> None:
        with self.assertRaises(stall_router.PolicyError):
            stall_router.decide({"attempts": [], "attempt_budget": 3})

    def test_passed_attempt_routes_to_independent_gate(self) -> None:
        result = stall_router.decide(
            {"attempts": [attempt("", progress=True, outcome="passed")]}
        )
        self.assertEqual(result["action"], "ready-for-verification")

    def test_environment_failure_stops_code_trials(self) -> None:
        result = stall_router.decide(
            {"attempts": [attempt("access denied")], "cause": "permission"}
        )
        self.assertEqual(result["route"], "scout-or-impediment")

    def test_only_product_or_authority_causes_route_to_stakeholder(self) -> None:
        product = stall_router.decide({"attempts": [], "cause": "product-intent"})
        technical = stall_router.decide({"attempts": [], "cause": "unknown"})
        self.assertEqual(product["action"], "pause-and-ask-stakeholder")
        self.assertNotEqual(technical["action"], "pause-and-ask-stakeholder")


if __name__ == "__main__":
    unittest.main()
