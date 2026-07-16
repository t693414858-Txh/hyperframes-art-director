from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    ROOT
    / "skills"
    / "art-direct-hyperframes"
    / "scripts"
    / "prepare_visual_review.py"
)
SPEC = importlib.util.spec_from_file_location("prepare_visual_review", MODULE_PATH)
assert SPEC and SPEC.loader
prepare_visual_review = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(prepare_visual_review)


class PrepareVisualReviewTests(unittest.TestCase):
    def load_example(self, name: str) -> dict:
        return json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))

    def test_passing_plan(self) -> None:
        errors = prepare_visual_review.validate_plan(
            self.load_example("review-capture-plan.pass.json")
        )
        self.assertEqual(errors, [])

    def test_failing_plan(self) -> None:
        errors = prepare_visual_review.validate_plan(
            self.load_example("review-capture-plan.fail.json")
        )
        self.assertTrue(any("project must" in error for error in errors))
        self.assertTrue(any("strictly increasing" in error for error in errors))
        self.assertTrue(any("duplicates" in error for error in errors))

    def test_scene_timestamps_must_be_in_order(self) -> None:
        plan = self.load_example("review-capture-plan.pass.json")
        plan["scenes"][2]["timestamp_seconds"] = 4
        errors = prepare_visual_review.validate_plan(plan)
        self.assertTrue(any("strictly increasing" in error for error in errors))

    def test_safe_slug_removes_path_characters(self) -> None:
        self.assertEqual(
            prepare_visual_review.safe_slug("../Scene 01 / Hero"),
            "..-Scene-01-Hero",
        )

    def test_contact_sheet_filter_contains_every_input(self) -> None:
        graph = prepare_visual_review.build_contact_sheet_filter(
            frame_count=4,
            columns=2,
            thumbnail_width=400,
            source_width=1080,
            source_height=1920,
            padding=16,
            margin=24,
            background="#F5F5F3",
        )
        self.assertIn("[0:v]", graph)
        self.assertIn("[3:v]", graph)
        self.assertIn("xstack=inputs=4", graph)
        self.assertIn("layout=0_0|416_0|0_728|416_728", graph)
        self.assertIn("[out]", graph)

    def test_identity_review_scaffold_preserves_scene_order(self) -> None:
        records = [
            {
                "id": "scene-01",
                "label": "Arrival",
                "role": "arrival",
                "timestamp_seconds": 1.5,
                "path": "/tmp/scene-01.png",
            },
            {
                "id": "scene-02",
                "label": "Resolve",
                "role": "resolve",
                "timestamp_seconds": 8.0,
                "path": "/tmp/scene-02.png",
            },
        ]
        scaffold = prepare_visual_review.build_identity_review_scaffold(records)
        audit = scaffold["scene_audit"]
        self.assertEqual([item["scene_id"] for item in audit], ["scene-01", "scene-02"])
        self.assertIsNone(audit[0]["source_evidence_visible"])
        self.assertEqual(
            scaffold["template_swap_test"]["required_redesigns"],
            [],
        )


if __name__ == "__main__":
    unittest.main()
