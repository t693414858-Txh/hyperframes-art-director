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
    / "validate_experience_interaction.py"
)
SPEC = importlib.util.spec_from_file_location(
    "validate_experience_interaction", MODULE_PATH
)
assert SPEC and SPEC.loader
validate_experience_interaction = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_experience_interaction)


class ValidateExperienceInteractionTests(unittest.TestCase):
    def load_example(self, name: str) -> dict:
        return json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))

    def test_passing_qa(self) -> None:
        errors = validate_experience_interaction.validate_experience_interaction(
            self.load_example("experience-interaction-qa.pass.json")
        )
        self.assertEqual(errors, [])

    def test_failing_qa(self) -> None:
        errors = validate_experience_interaction.validate_experience_interaction(
            self.load_example("experience-interaction-qa.fail.json")
        )
        self.assertTrue(any("felt_change has failed" in error for error in errors))
        self.assertTrue(any("early_invitation.timestamp_seconds" in error for error in errors))
        self.assertTrue(any("secondary_actions must be empty" in error for error in errors))

    def test_every_check_requires_narration_lines(self) -> None:
        qa = self.load_example("experience-interaction-qa.pass.json")
        qa["experience_gate"]["evidence"]["narration_lines"] = []
        errors = validate_experience_interaction.validate_experience_interaction(qa)
        self.assertTrue(
            any("experience_gate.evidence.narration_lines" in error for error in errors)
        )

    def test_early_invitation_must_be_before_sixty_percent(self) -> None:
        qa = self.load_example("experience-interaction-qa.pass.json")
        qa["interaction_gate"]["early_invitation"]["timestamp_seconds"] = 50
        errors = validate_experience_interaction.validate_experience_interaction(qa)
        self.assertTrue(
            any("before 60 percent of runtime" in error for error in errors)
        )

    def test_contract_consistency_requires_keyword_on_every_surface(self) -> None:
        qa = self.load_example("experience-interaction-qa.pass.json")
        qa["interaction_gate"]["contract_consistency"]["surfaces"][
            "publishing_description"
        ] = "评论领取提示词、行动表和跟进模板。"
        errors = validate_experience_interaction.validate_experience_interaction(qa)
        self.assertTrue(
            any("publishing_description must include keyword" in error for error in errors)
        )

    def test_contract_consistency_requires_reward_on_every_surface(self) -> None:
        qa = self.load_example("experience-interaction-qa.pass.json")
        qa["interaction_gate"]["contract_consistency"]["surfaces"][
            "pinned_comment"
        ] = "回复“纪要”，我发你资料。"
        errors = validate_experience_interaction.validate_experience_interaction(qa)
        self.assertTrue(
            any("pinned_comment must include reward" in error for error in errors)
        )


if __name__ == "__main__":
    unittest.main()
