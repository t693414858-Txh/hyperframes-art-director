#!/usr/bin/env python3
"""Validate a HyperFrames art-direction review scorecard."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path


DIMENSIONS = (
    "content_style_fit",
    "project_recognizability",
    "narrative_clarity",
    "composition_and_focus",
    "typography_system",
    "image_and_material_treatment",
    "motion_and_rhythm",
    "continuity_and_distinctiveness",
)

ROUTES = (
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

REDESIGN_DIMENSIONS = (
    "composition",
    "source_evidence",
    "semantic_transformation",
    "motion_behavior",
    "data_structure",
    "material_treatment",
)


def nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_review_evidence(data: dict[str, object], errors: list[str]) -> None:
    evidence = data.get("evidence_reviewed")
    if not isinstance(evidence, dict):
        errors.append("evidence_reviewed must be a JSON object.")
        return

    for field in ("design_md", "contact_sheet", "draft_playback"):
        if not nonempty_string(evidence.get(field)):
            errors.append(
                f"evidence_reviewed.{field} must be a non-empty path or URL."
            )

    frames = evidence.get("full_size_frames")
    if not isinstance(frames, list) or not frames or any(
        not nonempty_string(item) for item in frames
    ):
        errors.append(
            "evidence_reviewed.full_size_frames must contain at least one "
            "non-empty path or URL."
        )


def validate_route_review(data: dict[str, object], errors: list[str]) -> None:
    route_review = data.get("route_review")
    if not isinstance(route_review, dict):
        errors.append("route_review must be a JSON object.")
        return

    if route_review.get("primary_route") not in ROUTES:
        errors.append("route_review.primary_route must be a supported route.")

    checks = route_review.get("checks")
    if not isinstance(checks, list) or len(checks) < 3:
        errors.append("route_review.checks must contain at least three checks.")
        return

    for index, check in enumerate(checks):
        path = f"route_review.checks[{index}]"
        if not isinstance(check, dict):
            errors.append(f"{path} must be a JSON object.")
            continue
        for field in ("criterion", "evidence"):
            if not nonempty_string(check.get(field)):
                errors.append(f"{path}.{field} must be a non-empty string.")

        status = check.get("status")
        if status not in {"pass", "fail", "not_applicable"}:
            errors.append(
                f"{path}.status must be pass, fail, or not_applicable."
            )

        action = check.get("action")
        if not isinstance(action, str):
            errors.append(f"{path}.action must be a string.")
        elif status == "fail" and not action.strip():
            errors.append(f"{path}.action is required when status is fail.")
        if status == "fail":
            errors.append(f"{path} has not passed its route-specific check.")


def validate_identity_review(data: dict[str, object], errors: list[str]) -> None:
    review = data.get("identity_review")
    if not isinstance(review, dict):
        errors.append("identity_review must be a JSON object.")
        return

    ignored = review.get("ignored_elements")
    required = {"project_name", "logo", "captions", "presenter"}
    if not isinstance(ignored, list) or any(
        not nonempty_string(item) for item in ignored
    ):
        errors.append(
            "identity_review.ignored_elements must be a list of non-empty strings."
        )
    elif not required.issubset(set(ignored)):
        errors.append(
            "identity_review.ignored_elements must include project_name, "
            "logo, captions, and presenter."
        )

    result = review.get("result")
    if result not in {"pass", "fail"}:
        errors.append("identity_review.result must be pass or fail.")
    elif result == "fail":
        errors.append("Blind project-recognition test failed.")

    for field in ("recognized_as", "evidence"):
        if not nonempty_string(review.get(field)):
            errors.append(
                f"identity_review.{field} must be a non-empty string."
            )

    confused = review.get("confusable_with")
    if not isinstance(confused, list) or any(
        not nonempty_string(item) for item in confused
    ):
        errors.append(
            "identity_review.confusable_with must be a list of non-empty strings."
        )
    elif result == "pass" and confused:
        errors.append(
            "A passing identity review cannot remain confusable with "
            "unrelated projects."
        )

    scene_audit = review.get("scene_audit")
    if not isinstance(scene_audit, list) or not scene_audit:
        errors.append("identity_review.scene_audit must contain scene results.")
        scene_audit = []

    evidence = data.get("evidence_reviewed")
    frames = evidence.get("full_size_frames") if isinstance(evidence, dict) else []
    if isinstance(frames, list) and len(scene_audit) != len(frames):
        errors.append(
            "identity_review.scene_audit must contain one item per "
            "full-size frame."
        )

    scene_ids: set[str] = set()
    primary_count = 0
    generic_count = 0
    source_evidence_count = 0
    for index, item in enumerate(scene_audit):
        path = f"identity_review.scene_audit[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{path} must be a JSON object.")
            continue

        scene_id = item.get("scene_id")
        if not nonempty_string(scene_id):
            errors.append(f"{path}.scene_id must be a non-empty string.")
        elif scene_id in scene_ids:
            errors.append(f"{path}.scene_id duplicates {scene_id}.")
        else:
            scene_ids.add(str(scene_id))

        strength = item.get("identity_strength")
        if strength not in {"primary", "supporting", "generic"}:
            errors.append(
                f"{path}.identity_strength must be primary, supporting, or generic."
            )
        elif strength == "primary":
            primary_count += 1
        elif strength == "generic":
            generic_count += 1

        swap_result = item.get("template_swap_result")
        if swap_result not in {"requires_redesign", "copy_only"}:
            errors.append(
                f"{path}.template_swap_result must be requires_redesign "
                "or copy_only."
            )
        elif strength == "primary" and swap_result != "requires_redesign":
            errors.append(
                f"{path} is a primary identity scene but needs only copy changes."
            )

        source_visible = item.get("source_evidence_visible")
        if not isinstance(source_visible, bool):
            errors.append(f"{path}.source_evidence_visible must be a boolean.")
        elif source_visible:
            source_evidence_count += 1

        if not nonempty_string(item.get("project_specific_evidence")):
            errors.append(
                f"{path}.project_specific_evidence must be a non-empty string."
            )

    scene_count = len(scene_audit)
    if scene_count:
        minimum_primary = math.ceil(scene_count * 0.6)
        minimum_source = math.ceil(scene_count * 0.4)
        maximum_generic = math.floor(scene_count * 0.2)
        if primary_count < minimum_primary:
            errors.append(
                f"Identity scene coverage has {primary_count} primary scene(s); "
                f"minimum is {minimum_primary}."
            )
        if source_evidence_count < minimum_source:
            errors.append(
                f"Source evidence is visible in {source_evidence_count} scene(s); "
                f"minimum is {minimum_source}."
            )
        if generic_count > maximum_generic:
            errors.append(
                f"Identity audit has {generic_count} generic scene(s); "
                f"maximum is {maximum_generic}."
            )

    swap_test = review.get("template_swap_test")
    if not isinstance(swap_test, dict):
        errors.append("identity_review.template_swap_test must be an object.")
    else:
        for field in ("alternate_project", "evidence"):
            if not nonempty_string(swap_test.get(field)):
                errors.append(
                    f"identity_review.template_swap_test.{field} must be "
                    "a non-empty string."
                )
        if swap_test.get("result") != "requires_redesign":
            errors.append(
                "identity_review.template_swap_test.result must be "
                "requires_redesign."
            )
        redesigns = swap_test.get("required_redesigns")
        if not isinstance(redesigns, list) or len(redesigns) < 3 or any(
            not nonempty_string(item) for item in redesigns
        ):
            errors.append(
                "identity_review.template_swap_test.required_redesigns must "
                "contain at least three non-empty strings."
            )
        else:
            unsupported = [
                item for item in redesigns if item not in REDESIGN_DIMENSIONS
            ]
            if unsupported:
                errors.append(
                    "identity_review.template_swap_test.required_redesigns "
                    "contains unsupported values: "
                    + ", ".join(unsupported)
                    + "."
                )


def validate_scorecard(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["Scorecard root must be a JSON object."]

    project = data.get("project")
    if not isinstance(project, str) or not project.strip():
        errors.append("project must be a non-empty string.")

    validate_review_evidence(data, errors)
    validate_route_review(data, errors)
    validate_identity_review(data, errors)

    dimensions = data.get("dimensions")
    if not isinstance(dimensions, dict):
        return errors + ["dimensions must be a JSON object."]

    scores: list[int] = []
    for name in DIMENSIONS:
        item = dimensions.get(name)
        if not isinstance(item, dict):
            errors.append(f"Missing dimension: {name}.")
            continue

        score = item.get("score")
        if not isinstance(score, int) or isinstance(score, bool) or not 1 <= score <= 5:
            errors.append(f"{name}.score must be an integer from 1 to 5.")
        else:
            scores.append(score)
            if name == "project_recognizability" and score < 4:
                errors.append(
                    "project_recognizability.score must be at least 4 to pass."
                )

        evidence = item.get("evidence")
        if not isinstance(evidence, str) or not evidence.strip():
            errors.append(f"{name}.evidence must be a non-empty string.")

        action = item.get("action")
        if not isinstance(action, str):
            errors.append(f"{name}.action must be a string.")
        elif isinstance(score, int) and score < 4 and not action.strip():
            errors.append(f"{name}.action is required when score is below 4.")

    blockers = data.get("blocking_issues")
    if not isinstance(blockers, list) or any(
        not isinstance(item, str) or not item.strip() for item in blockers
    ):
        errors.append("blocking_issues must be a list of non-empty strings.")
    elif blockers:
        errors.append("Blocking issues remain: " + "; ".join(blockers))

    if len(scores) == len(DIMENSIONS):
        average = sum(scores) / len(scores)
        if average < 4.0:
            errors.append(f"Average score is {average:.2f}; minimum passing average is 4.00.")
        if min(scores) < 3:
            errors.append(f"Lowest score is {min(scores)}; no dimension may be below 3.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a HyperFrames aesthetic review scorecard."
    )
    parser.add_argument("scorecard", type=Path, help="Path to the scorecard JSON file.")
    args = parser.parse_args()

    try:
        data = json.loads(args.scorecard.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: File not found: {args.scorecard}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON: {exc}", file=sys.stderr)
        return 2

    errors = validate_scorecard(data)
    if errors:
        print("REVIEW FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    scores = [
        data["dimensions"][name]["score"]
        for name in DIMENSIONS
    ]
    scene_audit = data["identity_review"]["scene_audit"]
    primary_count = sum(
        1 for item in scene_audit if item["identity_strength"] == "primary"
    )
    source_count = sum(
        1 for item in scene_audit if item["source_evidence_visible"]
    )
    print(
        f"REVIEW PASSED: average={sum(scores) / len(scores):.2f}, "
        f"minimum={min(scores)}, identity={primary_count}/{len(scene_audit)}, "
        f"source_evidence={source_count}/{len(scene_audit)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
