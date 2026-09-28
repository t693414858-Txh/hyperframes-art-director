import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "art-direct-hyperframes" / "scripts" / "validate_shortform_retention.py"
SPEC = importlib.util.spec_from_file_location("validate_shortform_retention", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def load_example(name: str):
    with (ROOT / "examples" / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


class ValidateShortformRetentionTest(unittest.TestCase):
    def test_passing_example(self):
        errors, report = MODULE.validate_plan(
            load_example("shortform-retention.pass.json")
        )
        self.assertEqual(errors, [])
        self.assertEqual(report["error_count"], 0)
        self.assertLessEqual(
            report["largest_early_state_change_gap_seconds"],
            MODULE.SHORTFORM_THRESHOLDS[
                "meaningful_state_change_gap_seconds_max"
            ],
        )

    def test_failing_example_exposes_core_release_blockers(self):
        errors, _ = MODULE.validate_plan(
            load_example("shortform-retention.fail.json")
        )
        joined = "\n".join(errors)
        self.assertIn("problem_and_result_preview_seconds", joined)
        self.assertIn("first_visible_proof_seconds", joined)
        self.assertIn("largest gap", joined)
        self.assertIn("continuous_workspace must be true", joined)
        self.assertIn("poster_or_card_montage must be false", joined)
        self.assertIn("requires runtime_waiver", joined)

    def test_valid_runtime_waiver_allows_longer_multi_step_video(self):
        plan = load_example("shortform-retention.pass.json")
        plan["format"] = "multi_step"
        plan["runtime_seconds"] = 54
        plan["runtime_waiver"] = {
            "reason": "Two tools must be compared against the same source.",
            "chapter_count": 2,
            "split_rejected_reason": "Splitting removes the direct comparison."
        }
        errors, report = MODULE.validate_plan(plan)
        self.assertEqual(errors, [])
        self.assertTrue(report["runtime_waiver_used"])

    def test_each_state_change_requires_review_evidence(self):
        plan = load_example("shortform-retention.pass.json")
        plan["meaningful_state_changes"][1]["evidence"] = ""
        errors, _ = MODULE.validate_plan(plan)
        self.assertIn(
            "meaningful_state_changes[1].evidence must be a non-empty string",
            errors,
        )


if __name__ == "__main__":
    unittest.main()
