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
    / "validate_direction.py"
)
SPEC = importlib.util.spec_from_file_location("validate_direction", MODULE_PATH)
assert SPEC and SPEC.loader
validate_direction = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_direction)


class ValidateDirectionTests(unittest.TestCase):
    def load_example(self, name: str) -> dict:
        return json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))

    def test_passing_direction_brief(self) -> None:
        errors = validate_direction.validate_direction(
            self.load_example("direction-brief.pass.json")
        )
        self.assertEqual(errors, [])

    def test_failing_direction_brief(self) -> None:
        errors = validate_direction.validate_direction(
            self.load_example("direction-brief.fail.json")
        )
        self.assertTrue(any("evidence_requirement" in error for error in errors))
        self.assertTrue(any("Scene durations total" in error for error in errors))
        self.assertTrue(any("six-digit hex color" in error for error in errors))

    def test_supporting_route_requires_scope(self) -> None:
        brief = self.load_example("direction-brief.pass.json")
        brief["route_decision"]["supporting_route"] = "Precision Product"
        errors = validate_direction.validate_direction(brief)
        self.assertTrue(any("supporting_scope is required" in error for error in errors))

    def test_candidate_total_is_recomputed(self) -> None:
        brief = self.load_example("direction-brief.pass.json")
        brief["route_decision"]["candidate_scores"][0]["total"] = 9
        errors = validate_direction.validate_direction(brief)
        self.assertTrue(any("expected 10" in error for error in errors))

    def test_lower_scoring_primary_requires_override(self) -> None:
        brief = self.load_example("direction-brief.pass.json")
        brief["route_decision"]["candidate_scores"][1]["intent_fit"] = 2
        brief["route_decision"]["candidate_scores"][1]["credibility_fit"] = 2
        brief["route_decision"]["candidate_scores"][1]["audience_fit"] = 2
        brief["route_decision"]["candidate_scores"][1]["total"] = 10
        brief["route_decision"]["candidate_scores"][0]["brand_fit"] = 1
        brief["route_decision"]["candidate_scores"][0]["total"] = 9
        errors = validate_direction.validate_direction(brief)
        self.assertTrue(any("override_reason is required" in error for error in errors))

    def test_low_confidence_requires_assumption(self) -> None:
        brief = self.load_example("direction-brief.pass.json")
        brief["route_decision"]["confidence"] = "low"
        errors = validate_direction.validate_direction(brief)
        self.assertTrue(any("record at least one assumption" in error for error in errors))

    def test_scene_durations_match_delivery(self) -> None:
        brief = self.load_example("direction-brief.pass.json")
        brief["scenes"][0]["duration_seconds"] = 5
        errors = validate_direction.validate_direction(brief)
        self.assertTrue(any("planned duration" in error for error in errors))

    def test_supporting_route_cannot_dominate_without_override(self) -> None:
        brief = self.load_example("direction-brief.pass.json")
        brief["route_decision"]["supporting_route"] = "Precision Product"
        brief["route_decision"]["supporting_scope"] = "Execution scenes"
        brief["scenes"][1]["route_role"] = "supporting"
        brief["scenes"][2]["route_role"] = "supporting"
        errors = validate_direction.validate_direction(brief)
        self.assertTrue(any("exceed 40%" in error for error in errors))

    def test_preference_decisions_are_required(self) -> None:
        brief = self.load_example("direction-brief.pass.json")
        del brief["style_preferences_rejected"]
        errors = validate_direction.validate_direction(brief)
        self.assertTrue(
            any("style_preferences_rejected" in error for error in errors)
        )

    def test_visual_direction_comparison_requires_two_candidates(self) -> None:
        brief = self.load_example("direction-brief.pass.json")
        brief["visual_evidence"]["direction_candidates"] = [
            brief["visual_evidence"]["direction_candidates"][0]
        ]
        errors = validate_direction.validate_direction(brief)
        self.assertTrue(
            any("At least two visual direction candidates" in error for error in errors)
        )

    def test_single_direction_waiver_is_allowed(self) -> None:
        brief = self.load_example("direction-brief.pass.json")
        brief["visual_evidence"]["direction_candidates"] = [
            brief["visual_evidence"]["direction_candidates"][0]
        ]
        brief["visual_evidence"]["comparison_waiver"] = (
            "The supplied and approved brand system fixes the visual direction."
        )
        errors = validate_direction.validate_direction(brief)
        self.assertEqual(errors, [])

    def test_selected_visual_direction_must_exist(self) -> None:
        brief = self.load_example("direction-brief.pass.json")
        brief["visual_evidence"]["selected_direction"] = "direction-z"
        errors = validate_direction.validate_direction(brief)
        self.assertTrue(
            any("selected_direction must match" in error for error in errors)
        )

    def test_project_fingerprint_requires_semantic_anchor(self) -> None:
        brief = self.load_example("direction-brief.pass.json")
        brief["project_fingerprint"]["anchors"][0]["type"] = "color"
        errors = validate_direction.validate_direction(brief)
        self.assertTrue(
            any("semantic_transformation anchor" in error for error in errors)
        )

    def test_project_fingerprint_must_cover_every_scene(self) -> None:
        brief = self.load_example("direction-brief.pass.json")
        brief["project_fingerprint"]["scene_recurrence"].pop()
        errors = validate_direction.validate_direction(brief)
        self.assertTrue(
            any("must cover every scene" in error for error in errors)
        )

    def test_project_fingerprint_anchor_must_recur(self) -> None:
        brief = self.load_example("direction-brief.pass.json")
        anchor_id = brief["project_fingerprint"]["anchors"][0]["id"]
        for scene in brief["project_fingerprint"]["scene_recurrence"][1:]:
            scene["anchor_ids"] = [
                item for item in scene["anchor_ids"] if item != anchor_id
            ]
        errors = validate_direction.validate_direction(brief)
        self.assertTrue(
            any("minimum is" in error for error in errors)
        )

    def test_project_fingerprint_requires_core_scene_coverage(self) -> None:
        brief = self.load_example("direction-brief.pass.json")
        brief["project_fingerprint"]["scene_recurrence"][1][
            "core_identity_scene"
        ] = False
        brief["project_fingerprint"]["scene_recurrence"][2][
            "core_identity_scene"
        ] = False
        errors = validate_direction.validate_direction(brief)
        self.assertTrue(
            any("core identity scene(s); minimum is 3" in error for error in errors)
        )

    def test_core_scene_cannot_be_copy_only(self) -> None:
        brief = self.load_example("direction-brief.pass.json")
        brief["project_fingerprint"]["scene_recurrence"][0][
            "template_swap_result"
        ] = "copy_only"
        errors = validate_direction.validate_direction(brief)
        self.assertTrue(
            any("core identity scene but passes" in error for error in errors)
        )

    def test_scene_proof_assets_must_be_declared(self) -> None:
        brief = self.load_example("direction-brief.pass.json")
        brief["project_fingerprint"]["scene_recurrence"][0][
            "proof_asset_ids"
        ] = ["unknown-proof"]
        errors = validate_direction.validate_direction(brief)
        self.assertTrue(
            any("references unknown proof assets" in error for error in errors)
        )

    def test_template_swap_test_must_require_redesign(self) -> None:
        brief = self.load_example("direction-brief.pass.json")
        brief["project_fingerprint"]["template_swap_test"]["result"] = "copy_only"
        errors = validate_direction.validate_direction(brief)
        self.assertTrue(
            any("template_swap_test.result must be requires_redesign" in error for error in errors)
        )

    def test_template_swap_redesigns_use_supported_dimensions(self) -> None:
        brief = self.load_example("direction-brief.pass.json")
        brief["project_fingerprint"]["template_swap_test"][
            "required_redesigns"
        ][0] = "make it nicer"
        errors = validate_direction.validate_direction(brief)
        self.assertTrue(
            any("contains unsupported values" in error for error in errors)
        )

    def test_single_scene_direction_can_use_complete_identity_role(self) -> None:
        brief = self.load_example("direction-brief.pass.json")
        brief["delivery"]["planned_duration_seconds"] = 4
        brief["scenes"] = [brief["scenes"][0]]
        fingerprint = brief["project_fingerprint"]
        fingerprint["proof_assets"] = ["Finished project output"]
        fingerprint["scene_recurrence"] = [fingerprint["scene_recurrence"][0]]
        fingerprint["scene_recurrence"][0]["identity_role"] = "complete"
        for anchor in fingerprint["anchors"]:
            anchor["minimum_scene_appearances"] = 1
        errors = validate_direction.validate_direction(brief)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
