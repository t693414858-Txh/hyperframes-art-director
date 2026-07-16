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
    / "validate_review.py"
)
SPEC = importlib.util.spec_from_file_location("validate_review", MODULE_PATH)
assert SPEC and SPEC.loader
validate_review = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_review)


class ValidateReviewTests(unittest.TestCase):
    def load_example(self, name: str) -> dict:
        return json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))

    def test_passing_scorecard(self) -> None:
        errors = validate_review.validate_scorecard(
            self.load_example("review-scorecard.pass.json")
        )
        self.assertEqual(errors, [])

    def test_failing_scorecard(self) -> None:
        errors = validate_review.validate_scorecard(
            self.load_example("review-scorecard.fail.json")
        )
        self.assertTrue(any("Average score" in error for error in errors))
        self.assertTrue(any("Lowest score" in error for error in errors))

    def test_low_score_requires_action(self) -> None:
        scorecard = self.load_example("review-scorecard.pass.json")
        scorecard["dimensions"]["narrative_clarity"]["score"] = 3
        scorecard["dimensions"]["narrative_clarity"]["action"] = ""
        errors = validate_review.validate_scorecard(scorecard)
        self.assertTrue(
            any("narrative_clarity.action is required" in error for error in errors)
        )

    def test_content_style_fit_is_required(self) -> None:
        scorecard = self.load_example("review-scorecard.pass.json")
        del scorecard["dimensions"]["content_style_fit"]
        errors = validate_review.validate_scorecard(scorecard)
        self.assertTrue(any("Missing dimension: content_style_fit" in error for error in errors))

    def test_blockers_fail_review(self) -> None:
        scorecard = self.load_example("review-scorecard.pass.json")
        scorecard["blocking_issues"] = ["Essential text is unreadable."]
        errors = validate_review.validate_scorecard(scorecard)
        self.assertTrue(any("Blocking issues remain" in error for error in errors))

    def test_contact_sheet_evidence_is_required(self) -> None:
        scorecard = self.load_example("review-scorecard.pass.json")
        scorecard["evidence_reviewed"]["contact_sheet"] = ""
        errors = validate_review.validate_scorecard(scorecard)
        self.assertTrue(
            any("evidence_reviewed.contact_sheet" in error for error in errors)
        )

    def test_route_review_requires_three_checks(self) -> None:
        scorecard = self.load_example("review-scorecard.pass.json")
        scorecard["route_review"]["checks"] = scorecard["route_review"]["checks"][:2]
        errors = validate_review.validate_scorecard(scorecard)
        self.assertTrue(
            any("route_review.checks must contain at least three" in error for error in errors)
        )

    def test_failed_route_check_fails_review(self) -> None:
        scorecard = self.load_example("review-scorecard.pass.json")
        scorecard["route_review"]["checks"][0]["status"] = "fail"
        scorecard["route_review"]["checks"][0]["action"] = "Redesign the frame."
        errors = validate_review.validate_scorecard(scorecard)
        self.assertTrue(
            any("has not passed its route-specific check" in error for error in errors)
        )

    def test_project_recognizability_must_score_four(self) -> None:
        scorecard = self.load_example("review-scorecard.pass.json")
        scorecard["dimensions"]["project_recognizability"]["score"] = 3
        scorecard["dimensions"]["project_recognizability"]["action"] = (
            "Strengthen the project fingerprint."
        )
        errors = validate_review.validate_scorecard(scorecard)
        self.assertTrue(
            any("project_recognizability.score must be at least 4" in error for error in errors)
        )

    def test_blind_recognition_failure_blocks_review(self) -> None:
        scorecard = self.load_example("review-scorecard.pass.json")
        scorecard["identity_review"]["result"] = "fail"
        scorecard["identity_review"]["confusable_with"] = [
            "Generic productivity explainer"
        ]
        errors = validate_review.validate_scorecard(scorecard)
        self.assertTrue(any("recognition test failed" in error for error in errors))

    def test_coherent_template_still_fails_project_identity(self) -> None:
        scorecard = self.load_example(
            "review-scorecard.project-recognition.fail.json"
        )
        errors = validate_review.validate_scorecard(scorecard)
        self.assertTrue(
            any("project_recognizability.score must be at least 4" in error for error in errors)
        )
        self.assertTrue(any("recognition test failed" in error for error in errors))
        self.assertFalse(any("Average score" in error for error in errors))

    def test_identity_scene_coverage_requires_sixty_percent_primary(self) -> None:
        scorecard = self.load_example("review-scorecard.pass.json")
        scorecard["identity_review"]["scene_audit"][1][
            "identity_strength"
        ] = "supporting"
        scorecard["identity_review"]["scene_audit"][2][
            "identity_strength"
        ] = "supporting"
        errors = validate_review.validate_scorecard(scorecard)
        self.assertTrue(
            any("Identity scene coverage has 1 primary" in error for error in errors)
        )

    def test_identity_review_requires_visible_source_evidence(self) -> None:
        scorecard = self.load_example("review-scorecard.pass.json")
        for item in scorecard["identity_review"]["scene_audit"]:
            item["source_evidence_visible"] = False
        errors = validate_review.validate_scorecard(scorecard)
        self.assertTrue(
            any("Source evidence is visible in 0 scene" in error for error in errors)
        )

    def test_review_template_swap_must_require_redesign(self) -> None:
        scorecard = self.load_example("review-scorecard.pass.json")
        scorecard["identity_review"]["template_swap_test"][
            "result"
        ] = "copy_only"
        errors = validate_review.validate_scorecard(scorecard)
        self.assertTrue(
            any("template_swap_test.result must be requires_redesign" in error for error in errors)
        )

    def test_review_template_swap_uses_supported_dimensions(self) -> None:
        scorecard = self.load_example("review-scorecard.pass.json")
        scorecard["identity_review"]["template_swap_test"][
            "required_redesigns"
        ][0] = "make it unique"
        errors = validate_review.validate_scorecard(scorecard)
        self.assertTrue(
            any("contains unsupported values" in error for error in errors)
        )


if __name__ == "__main__":
    unittest.main()
