from __future__ import annotations

import sys
import unittest
from pathlib import Path
from typing import Any


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT / "scripts"))

import context_router  # noqa: E402


class ContextRouterTests(unittest.TestCase):
    config: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.config = context_router.load_config()

    def test_every_route_and_heading_resolves(self) -> None:
        context_router.validate_config(self.config)
        for stage in self.config["stages"]:
            selected = context_router.resolve_route(self.config, stage, [], None)
            rendered = context_router.render_sources(selected)
            self.assertTrue(rendered)

    def test_execution_route_is_stage_specific(self) -> None:
        selected = context_router.resolve_route(self.config, "execution", [], None)
        rendered = context_router.render_sources(selected)
        paths = {item["path"] for item in rendered}
        self.assertIn("core/orchestrator.md", paths)
        self.assertNotIn("core/roles/product-owner.md", paths)
        self.assertNotIn("core/stall-recovery.md", paths)

    def test_execution_checkpoint_is_last(self) -> None:
        selected = context_router.resolve_route(self.config, "4", [], None)
        self.assertEqual(next(reversed(selected)), "core/execution-checklist.md")

    def test_stall_trigger_adds_canonical_protocol(self) -> None:
        selected = context_router.resolve_route(self.config, "4", ["stall"], None)
        rendered = context_router.render_sources(selected)
        paths = {item["path"] for item in rendered}
        self.assertIn("core/stall-recovery.md", paths)

    def test_cancel_trigger_loads_product_owner_decision(self) -> None:
        selected = context_router.resolve_route(self.config, "4", ["cancel"], None)
        rendered = context_router.render_sources(selected)
        item = next(
            entry
            for entry in rendered
            if entry["path"] == "core/roles/product-owner.md"
        )
        self.assertIn("### Canceling a Sprint", item["content"])

    def test_selected_sections_are_verbatim(self) -> None:
        selected = context_router.resolve_route(self.config, "vision", [], None)
        rendered = context_router.render_sources(selected)
        item = next(entry for entry in rendered if entry["path"] == "core/roles/product-owner.md")
        source = (PACKAGE_ROOT / item["path"]).read_text(encoding="utf-8")
        for chunk in item["content"].strip().split("\n\n## "):
            probe = chunk if chunk.startswith("## ") else chunk
            self.assertIn(probe[:120], source)

    def test_small_budget_refuses_silent_truncation(self) -> None:
        selected = context_router.resolve_route(self.config, "4", [], None)
        rendered = context_router.render_sources(selected)
        manifest = context_router.build_manifest("4", [], None, rendered)
        self.assertGreater(manifest["estimated_tokens"], 1)
        with self.assertRaises(context_router.BudgetExceeded):
            context_router.enforce_budget(manifest, 1)

    def test_over_budget_requires_explicit_override(self) -> None:
        selected = context_router.resolve_route(self.config, "4", [], None)
        rendered = context_router.render_sources(selected)
        manifest = context_router.build_manifest("4", [], None, rendered)
        context_router.enforce_budget(manifest, 1, allow_over_budget=True)

    def test_route_cannot_escape_package(self) -> None:
        with self.assertRaises(context_router.RouteError):
            context_router.safe_source_path(PACKAGE_ROOT, "../private.md")


if __name__ == "__main__":
    unittest.main()
