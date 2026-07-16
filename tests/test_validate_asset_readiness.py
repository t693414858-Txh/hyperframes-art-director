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
    / "validate_asset_readiness.py"
)
SPEC = importlib.util.spec_from_file_location(
    "validate_asset_readiness", MODULE_PATH
)
assert SPEC and SPEC.loader
validate_asset_readiness = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_asset_readiness)


class ValidateAssetReadinessTests(unittest.TestCase):
    def load_example(self, name: str) -> dict:
        return json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))

    def test_passing_asset_report(self) -> None:
        errors = validate_asset_readiness.validate_asset_readiness(
            self.load_example("asset-readiness.pass.json")
        )
        self.assertEqual(errors, [])

    def test_failing_asset_report(self) -> None:
        errors = validate_asset_readiness.validate_asset_readiness(
            self.load_example("asset-readiness.fail.json")
        )
        self.assertTrue(any("unknown rights" in error for error in errors))
        self.assertTrue(any("references unknown assets" in error for error in errors))
        self.assertTrue(any("ready status cannot" in error for error in errors))

    def test_ready_requires_primary_asset(self) -> None:
        report = self.load_example("asset-readiness.pass.json")
        for asset in report["assets"]:
            asset["role"] = "supporting"
        errors = validate_asset_readiness.validate_asset_readiness(report)
        self.assertTrue(
            any("requires at least one primary asset" in error for error in errors)
        )

    def test_required_evidence_needs_coverage(self) -> None:
        report = self.load_example("asset-readiness.pass.json")
        report["coverage"][0]["covered_by"] = []
        errors = validate_asset_readiness.validate_asset_readiness(report)
        self.assertTrue(
            any("requires evidence but has no supporting asset" in error for error in errors)
        )

    def test_blocked_status_identifies_missing_asset(self) -> None:
        report = self.load_example("asset-readiness.pass.json")
        report["status"] = "blocked"
        errors = validate_asset_readiness.validate_asset_readiness(report)
        self.assertTrue(
            any("blocked status must identify" in error for error in errors)
        )


if __name__ == "__main__":
    unittest.main()
