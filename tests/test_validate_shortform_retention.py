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
    def test_reading_hold_uses_declared_profile_without_fake_state_changes(self):
        plan = load_example("shortform-retention.pass.json")
        plan["meaningful_state_changes"].pop(2)
        baseline_errors, _ = MODULE.validate_plan(plan)
        self.assertTrue(any("largest gap" in error for error in baseline_errors))
        plan["thresholds"] = {"meaningful_state_change_gap_seconds_max": 4.5}
        plan["threshold_rationale"] = "Hold the rename preview long enough to read its filenames."
        errors, report = MODULE.validate_plan(plan)
        self.assertEqual(errors, [])
        self.assertAlmostEqual(report["largest_early_state_change_gap_seconds"], 4.4)
        self.assertEqual(report["effective_thresholds"]["meaningful_state_change_gap_seconds_max"], 4.5)
        self.assertEqual(MODULE.SHORTFORM_THRESHOLDS["meaningful_state_change_gap_seconds_max"], 2.5)

    def test_overrides_require_a_rationale_and_supported_positive_limits(self):
        cases = [
            ({"meaningful_state_change_gap_seconds_max": 3.0}, "", "threshold_rationale"),
            ({"ignore_evidence": 1}, "Make proof optional", "unsupported threshold"),
            ({"early_window_seconds": 0}, "Disable the window", "finite positive"),
            ({"early_window_seconds": float("nan")}, "Invalid number", "finite positive"),
            ({"early_window_seconds": float("inf")}, "Invalid number", "finite positive"),
            ({"early_window_seconds": True}, "Invalid number", "finite positive"),
            ({"runtime_waiver_chapter_count_min": 1}, "Change a fixed rule", "unsupported threshold"),
            ({"first_real_operation_seconds_max": 6}, "After proof limit", "checkpoint threshold"),
            ({"meaningful_state_change_gap_seconds_max": 13}, "Beyond the window", "cannot exceed"),
        ]
        for overrides, rationale, expected in cases:
            with self.subTest(overrides=overrides):
                plan = load_example("shortform-retention.pass.json")
                plan["thresholds"] = overrides
                plan["threshold_rationale"] = rationale
                errors, _ = MODULE.validate_plan(plan)
                self.assertTrue(any(expected in error for error in errors))

    def test_each_supported_override_controls_its_validation(self):
        cases = [
            ("problem_and_result_preview_seconds_max", 0.5, "single_task", "checkpoints.problem_and_result_preview_seconds"),
            ("first_real_operation_seconds_max", 1.5, "single_task", "operation_chain.start_seconds"),
            ("first_visible_proof_seconds_max", 4.0, "single_task", "checkpoints.first_visible_proof_seconds"),
            ("before_after_or_verification_seconds_max", 7.0, "single_task", "checkpoints.before_after_or_verification_seconds"),
            ("early_window_seconds", 13.0, "single_task", "operation_chain.end_seconds"),
            ("meaningful_state_change_gap_seconds_max", 2.0, "single_task", "largest gap"),
            ("single_task_runtime_seconds_max", 31.0, "single_task", "requires runtime_waiver"),
            ("multi_step_runtime_seconds_max", 31.0, "multi_step", "requires runtime_waiver"),
        ]
        for key, limit, video_format, expected in cases:
            with self.subTest(threshold=key):
                plan = load_example("shortform-retention.pass.json")
                plan["format"] = video_format
                plan["thresholds"] = {key: limit}
                plan["threshold_rationale"] = "Use this declared timing profile for the test."
                errors, report = MODULE.validate_plan(plan)
                self.assertTrue(any(expected in error for error in errors))
                self.assertEqual(report["effective_thresholds"][key], limit)

    def test_custom_timing_keeps_evidence_and_operation_requirements(self):
        plan = load_example("shortform-retention.pass.json")
        plan["thresholds"] = {"meaningful_state_change_gap_seconds_max": 4.5}
        plan["threshold_rationale"] = "The result needs a reading hold."
        plan["meaningful_state_changes"][0]["evidence"] = ""
        plan["operation_chain"]["continuous_workspace"] = False
        errors, _ = MODULE.validate_plan(plan)
        self.assertTrue(any("evidence" in error for error in errors))
        self.assertTrue(any("continuous_workspace" in error for error in errors))

    def test_nonfinite_checkpoint_cannot_pass(self):
        for value in [float("nan"), float("inf"), True]:
            with self.subTest(value=value):
                plan = load_example("shortform-retention.pass.json")
                plan["checkpoints"]["first_visible_proof_seconds"] = value
                errors, _ = MODULE.validate_plan(plan)
                self.assertTrue(any("first_visible_proof_seconds" in error for error in errors))

    def test_invalid_operation_steps_return_errors(self):
        plan = load_example("shortform-retention.pass.json")
        plan["operation_chain"]["steps"] = [{"operation": "click"}]
        errors, _ = MODULE.validate_plan(plan)
        self.assertTrue(any("array of strings" in error for error in errors))

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
