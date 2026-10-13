#!/usr/bin/env python3
"""Dependency-free structural validation for the repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "art-direct-hyperframes"
SKILL_MD = SKILL / "SKILL.md"


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def main() -> int:
    required = (
        ROOT / "README.md",
        ROOT / "README.zh-CN.md",
        ROOT / "LICENSE",
        ROOT / "CONTRIBUTING.md",
        ROOT / "CHANGELOG.md",
        ROOT / "evals" / "cases" / "05-tech-product-routing.md",
        ROOT / "evals" / "cases" / "06-cultural-editorial-routing.md",
        ROOT / "evals" / "cases" / "07-mixed-content-routing.md",
        ROOT / "evals" / "cases" / "08-high-credibility-routing.md",
        ROOT / "evals" / "cases" / "09-knowledge-explainer-routing.md",
        ROOT / "evals" / "cases" / "10-contextual-preference-memory.md",
        ROOT / "evals" / "cases" / "11-reference-analysis.md",
        ROOT / "evals" / "cases" / "12-asset-constrained-reroute.md",
        ROOT / "evals" / "cases" / "13-visual-direction-comparison.md",
        ROOT / "evals" / "cases" / "14-automated-review-evidence.md",
        ROOT / "evals" / "cases" / "15-light-template-project-recognition.md",
        ROOT / "evals" / "cases" / "16-copy-swap-bypass.md",
        ROOT / "evals" / "cases" / "17-shortform-retention-gate.md",
        ROOT / "evals" / "cases" / "18-case-analysis-format.md",
        ROOT / "evals" / "cases" / "19-footage-variety.md",
        ROOT / "evals" / "cases" / "20-final-export-evidence.md",
        ROOT / "evals" / "cases" / "21-narrow-visual-revision.md",
        ROOT / "evals" / "cases" / "22-reading-hold-profile.md",
        ROOT / "examples" / "account-style-profile.md",
        ROOT / "examples" / "asset-readiness.pass.json",
        ROOT / "examples" / "asset-readiness.fail.json",
        ROOT / "examples" / "reference-analysis.example.json",
        ROOT / "examples" / "review-capture-plan.pass.json",
        ROOT / "examples" / "review-capture-plan.fail.json",
        ROOT / "examples" / "review-scorecard.project-recognition.fail.json",
        ROOT / "examples" / "experience-interaction-qa.pass.json",
        ROOT / "examples" / "experience-interaction-qa.fail.json",
        ROOT / "examples" / "content-rhythm.pass.json",
        ROOT / "examples" / "content-rhythm.fail.json",
        ROOT / "examples" / "shortform-retention.pass.json",
        ROOT / "examples" / "shortform-retention.fail.json",
        ROOT / "examples" / "meeting-action-redesign-blueprint.md",
        ROOT / "examples" / "direction-brief.pass.json",
        ROOT / "examples" / "direction-brief.fail.json",
        SKILL_MD,
        SKILL / "agents" / "openai.yaml",
        SKILL / "references" / "content-style-router.md",
        SKILL / "references" / "reference-analysis.md",
        SKILL / "references" / "asset-readiness.md",
        SKILL / "references" / "visual-benchmarks.md",
        SKILL / "references" / "contact-sheet-review.md",
        SKILL / "references" / "route-specific-rubrics.md",
        SKILL / "references" / "review-capture-plan.md",
        SKILL / "references" / "project-fingerprint.md",
        SKILL / "references" / "direction-contract.md",
        SKILL / "references" / "direction-framework.md",
        SKILL / "references" / "design-md-template.md",
        SKILL / "references" / "review-rubric.md",
        SKILL / "references" / "review-workflow.md",
        SKILL / "references" / "experience-interaction-standard.md",
        SKILL / "references" / "content-rhythm-standard.md",
        SKILL / "references" / "shortform-retention-standard.md",
        SKILL / "references" / "production-format.md",
        SKILL / "references" / "footage-editing.md",
        SKILL / "references" / "final-delivery-review.md",
        SKILL / "references" / "anti-patterns.md",
        SKILL / "references" / "style-preferences-template.md",
        SKILL / "scripts" / "validate_direction.py",
        SKILL / "scripts" / "validate_asset_readiness.py",
        SKILL / "scripts" / "prepare_visual_review.py",
        SKILL / "scripts" / "validate_review.py",
        SKILL / "scripts" / "validate_experience_interaction.py",
        SKILL / "scripts" / "validate_content_rhythm.py",
        SKILL / "scripts" / "validate_shortform_retention.py",
    )
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if missing:
        fail("Missing required files: " + ", ".join(missing))

    text = SKILL_MD.read_text(encoding="utf-8")
    if "TODO" in text:
        fail("SKILL.md still contains TODO markers.")

    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail("SKILL.md must start with YAML frontmatter.")

    frontmatter = match.group(1)
    keys = [
        line.split(":", 1)[0].strip()
        for line in frontmatter.splitlines()
        if ":" in line
    ]
    if keys != ["name", "description"]:
        fail("SKILL.md frontmatter must contain only name and description.")
    if "name: art-direct-hyperframes" not in frontmatter:
        fail("Skill name must be art-direct-hyperframes.")
    if len(text.splitlines()) > 500:
        fail("SKILL.md must remain under 500 lines.")

    for reference in re.findall(r"\]\((references/[^)]+)\)", text):
        if not (SKILL / reference).is_file():
            fail(f"SKILL.md references missing file: {reference}")

    router = (SKILL / "references" / "content-style-router.md").read_text(
        encoding="utf-8"
    )
    required_routes = (
        "Precision Product",
        "Knowledge Explainer",
        "Editorial Documentary",
        "Evidence-Led Intelligence",
        "Scientific Clarity",
        "Civic Trust",
        "Human Warmth",
        "Craft and Heritage",
        "Kinetic Culture",
        "Brand Manifesto",
    )
    missing_routes = [
        route for route in required_routes if f"### {route}" not in router
    ]
    if missing_routes:
        fail("Missing style routes: " + ", ".join(missing_routes))

    review_validator = (SKILL / "scripts" / "validate_review.py").read_text(
        encoding="utf-8"
    )
    if '"content_style_fit"' not in review_validator:
        fail("Review validator must require content_style_fit.")

    direction_validator = (SKILL / "scripts" / "validate_direction.py").read_text(
        encoding="utf-8"
    )
    if '"Knowledge Explainer"' not in direction_validator:
        fail("Direction validator must include the Knowledge Explainer route.")
    if '"visual_evidence"' not in direction_validator:
        fail("Direction validator must require visual_evidence.")
    if '"project_fingerprint"' not in direction_validator:
        fail("Direction validator must require project_fingerprint.")
    if '"template_swap_result"' not in direction_validator:
        fail("Direction validator must enforce per-scene template swaps.")
    if '"core_identity_scene"' not in direction_validator:
        fail("Direction validator must enforce identity scene coverage.")

    asset_validator = (
        SKILL / "scripts" / "validate_asset_readiness.py"
    ).read_text(encoding="utf-8")
    if '"unknown"' not in asset_validator or '"blocked"' not in asset_validator:
        fail("Asset validator must enforce rights and blocked readiness states.")

    if "evidence_reviewed" not in review_validator:
        fail("Review validator must require inspected visual evidence.")
    if "route_review" not in review_validator:
        fail("Review validator must require route-specific checks.")
    if '"project_recognizability"' not in review_validator:
        fail("Review validator must require project recognizability.")
    if "identity_review" not in review_validator:
        fail("Review validator must require the blind identity review.")
    if "scene_audit" not in review_validator:
        fail("Review validator must require per-frame identity audits.")
    if "required_redesigns" not in review_validator:
        fail("Review validator must enforce the template-swap test.")

    experience_validator = (
        SKILL / "scripts" / "validate_experience_interaction.py"
    ).read_text(encoding="utf-8")
    if "EXPERIENCE_CHECKS" not in experience_validator:
        fail("Experience validator must define experience checks.")
    if "INTERACTION_CHECKS" not in experience_validator:
        fail("Experience validator must define interaction checks.")
    if "contract_consistency" not in experience_validator:
        fail("Experience validator must enforce CTA contract consistency.")
    if "60 percent of runtime" not in experience_validator:
        fail("Experience validator must enforce early interaction timing.")

    content_rhythm_validator = (
        SKILL / "scripts" / "validate_content_rhythm.py"
    ).read_text(encoding="utf-8")
    if "DEFAULT_THRESHOLDS" not in content_rhythm_validator:
        fail("Content rhythm validator must define default thresholds.")
    if "experience_ranges" not in content_rhythm_validator:
        fail("Content rhythm validator must require experience ranges.")
    if "interaction_ranges" not in content_rhythm_validator:
        fail("Content rhythm validator must require interaction ranges.")

    shortform_retention_validator = (
        SKILL / "scripts" / "validate_shortform_retention.py"
    ).read_text(encoding="utf-8")
    if "SHORTFORM_THRESHOLDS" not in shortform_retention_validator:
        fail("Short-form validator must define retention thresholds.")
    if "first_visible_proof_seconds" not in shortform_retention_validator:
        fail("Short-form validator must enforce first visible proof timing.")
    if "meaningful_state_changes" not in shortform_retention_validator:
        fail("Short-form validator must enforce early state changes.")
    if "poster_or_card_montage" not in shortform_retention_validator:
        fail("Short-form validator must reject poster-card substitution.")

    capture_script = (
        SKILL / "scripts" / "prepare_visual_review.py"
    ).read_text(encoding="utf-8")
    if "ffmpeg" not in capture_script or "review-evidence.json" not in capture_script:
        fail("Review capture must generate FFmpeg-backed review evidence.")
    if "identity_review_scaffold" not in capture_script:
        fail("Review capture must generate an identity-review scaffold.")

    openai_yaml = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
    if "$art-direct-hyperframes" not in openai_yaml:
        fail("agents/openai.yaml default_prompt must mention $art-direct-hyperframes.")

    print("REPOSITORY VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
