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
    / "validate_content_rhythm.py"
)
SPEC = importlib.util.spec_from_file_location("validate_content_rhythm", MODULE_PATH)
assert SPEC and SPEC.loader
validate_content_rhythm = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_content_rhythm)


class ValidateContentRhythmTests(unittest.TestCase):
    def load_example(self, name: str) -> dict:
        return json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))

    def test_passing_rhythm(self) -> None:
        errors, report = validate_content_rhythm.validate_content_rhythm(
            self.load_example("content-rhythm.pass.json")
        )
        self.assertEqual(errors, [])
        self.assertGreaterEqual(report["experience_percent"], 40)
        self.assertGreaterEqual(report["interaction_percent"], 20)
        self.assertGreaterEqual(report["combined_unique_percent"], 60)

    def test_failing_rhythm(self) -> None:
        errors, _ = validate_content_rhythm.validate_content_rhythm(
            self.load_example("content-rhythm.fail.json")
        )
        self.assertTrue(any("Experience coverage" in error for error in errors))
        self.assertTrue(any("phase=opening" in error for error in errors))
        self.assertTrue(any("phase=middle" in error for error in errors))
        self.assertTrue(any("information units" in error for error in errors))

    def test_overlap_is_merged_before_measurement(self) -> None:
        rhythm = self.load_example("content-rhythm.pass.json")
        rhythm["experience_ranges"] = [
            {"start": 0, "end": 30},
            {"start": 20, "end": 50},
        ]
        _, report = validate_content_rhythm.validate_content_rhythm(rhythm)
        self.assertEqual(report["experience_percent"], 50.0)

    def test_middle_interaction_must_start_before_sixty_percent(self) -> None:
        rhythm = self.load_example("content-rhythm.pass.json")
        middle = next(
            item for item in rhythm["interaction_ranges"] if item["phase"] == "middle"
        )
        middle["start"] = 70
        middle["end"] = 78
        errors, _ = validate_content_rhythm.validate_content_rhythm(rhythm)
        self.assertTrue(any("before 60 percent" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
