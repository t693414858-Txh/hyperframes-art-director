#!/usr/bin/env python3
"""Validate a structured HyperFrames art-direction brief."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


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

SCORE_FIELDS = (
    "intent_fit",
    "material_fit",
    "credibility_fit",
    "audience_fit",
    "brand_fit",
)

CONTENT_FIELDS = (
    "primary_category",
    "secondary_category",
    "communication_intent",
    "audience",
    "viewing_context",
    "emotional_temperature",
    "evidence_requirement",
    "credibility_requirement",
    "available_source_material",
    "brand_cultural_sensitivity",
)

VISUAL_FIELDS = (
    "primary_material",
    "composition_logic",
    "identity_anchors",
    "variation_axes",
    "typography_roles",
    "palette_roles",
    "image_treatment",
    "texture_depth",
    "motion_character",
    "transition_language",
)

SCENE_TEXT_FIELDS = (
    "id",
    "name",
    "script_beat",
    "narrative_purpose",
    "dominant_visual_idea",
    "primary_focal_point",
    "secondary_eye_path",
    "hero_frame",
    "primary_motion_intent",
    "transition_intent",
)

HEX_COLOR = re.compile(r"#[0-9A-Fa-f]{6}\b")

FINGERPRINT_TYPES = (
    "semantic_transformation",
    "source_evidence",
    "structural",
    "typographic",
    "motion_behavior",
    "brand_asset",
    "material",
    "color",
)

IDENTITY_ROLES = (
    "complete",
    "establish",
    "develop",
    "prove",
    "resolve",
    "support",
)
TEMPLATE_SWAP_RESULTS = ("requires_redesign", "copy_only")
REPLACEMENT_DIMENSIONS = (
    "composition",
    "source_evidence",
    "semantic_transformation",
    "motion_behavior",
    "data_structure",
    "material_treatment",
)


def is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def require_object(
    parent: dict[str, object], key: str, errors: list[str]
) -> dict[str, object]:
    value = parent.get(key)
    if not isinstance(value, dict):
        errors.append(f"{key} must be a JSON object.")
        return {}
    return value


def require_nonempty_string(
    parent: dict[str, object], key: str, path: str, errors: list[str]
) -> str:
    value = parent.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path}.{key} must be a non-empty string.")
        return ""
    return value.strip()


def validate_string_list(
    value: object,
    path: str,
    errors: list[str],
    minimum: int = 0,
) -> list[str]:
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item.strip() for item in value
    ):
        errors.append(f"{path} must be a list of non-empty strings.")
        return []
    if len(value) < minimum:
        errors.append(f"{path} must contain at least {minimum} item(s).")
    return [item.strip() for item in value]


def validate_delivery(data: dict[str, object], errors: list[str]) -> float | None:
    delivery = require_object(data, "delivery", errors)
    for field in ("platform", "aspect_ratio", "sound_context"):
        require_nonempty_string(delivery, field, "delivery", errors)

    duration = delivery.get("planned_duration_seconds")
    if not is_number(duration) or duration <= 0:
        errors.append(
            "delivery.planned_duration_seconds must be a positive number."
        )
        return None
    return float(duration)


def validate_content_profile(
    data: dict[str, object], errors: list[str]
) -> None:
    profile = require_object(data, "content_profile", errors)
    for field in CONTENT_FIELDS:
        if field == "secondary_category":
            value = profile.get(field)
            if not isinstance(value, str):
                errors.append("content_profile.secondary_category must be a string.")
        elif field == "available_source_material":
            validate_string_list(
                profile.get(field),
                "content_profile.available_source_material",
                errors,
                minimum=1,
            )
        else:
            require_nonempty_string(profile, field, "content_profile", errors)

    for field in ("evidence_requirement", "credibility_requirement"):
        value = profile.get(field)
        if value not in {"low", "medium", "high"}:
            errors.append(
                f"content_profile.{field} must be low, medium, or high."
            )


def validate_candidate_scores(
    route: dict[str, object], primary_route: str, errors: list[str]
) -> None:
    candidates = route.get("candidate_scores")
    if not isinstance(candidates, list) or len(candidates) < 2:
        errors.append(
            "route_decision.candidate_scores must contain at least two candidates."
        )
        return

    seen: set[str] = set()
    totals: dict[str, int] = {}
    for index, candidate in enumerate(candidates):
        path = f"route_decision.candidate_scores[{index}]"
        if not isinstance(candidate, dict):
            errors.append(f"{path} must be a JSON object.")
            continue

        name = candidate.get("route")
        if name not in ROUTES:
            errors.append(f"{path}.route must be a supported route.")
            continue
        if name in seen:
            errors.append(f"{path}.route duplicates {name}.")
        seen.add(name)

        score_total = 0
        valid_scores = True
        for field in SCORE_FIELDS:
            score = candidate.get(field)
            if (
                not isinstance(score, int)
                or isinstance(score, bool)
                or not 0 <= score <= 2
            ):
                errors.append(f"{path}.{field} must be an integer from 0 to 2.")
                valid_scores = False
            else:
                score_total += score

        declared_total = candidate.get("total")
        if not isinstance(declared_total, int) or isinstance(declared_total, bool):
            errors.append(f"{path}.total must be an integer.")
        elif valid_scores and declared_total != score_total:
            errors.append(
                f"{path}.total is {declared_total}; expected {score_total}."
            )
        elif valid_scores:
            totals[name] = score_total

    if primary_route and primary_route not in seen:
        errors.append("The primary route must appear in candidate_scores.")

    if primary_route in totals and totals:
        highest = max(totals.values())
        if totals[primary_route] < highest:
            override = route.get("override_reason")
            if not isinstance(override, str) or not override.strip():
                errors.append(
                    "route_decision.override_reason is required when the "
                    "primary route is not the highest-scoring candidate."
                )


def validate_route_decision(
    data: dict[str, object], errors: list[str]
) -> tuple[str, str | None, str]:
    route = require_object(data, "route_decision", errors)
    primary = route.get("primary_route")
    if primary not in ROUTES:
        errors.append("route_decision.primary_route must be a supported route.")
        primary_name = ""
    else:
        primary_name = str(primary)

    supporting = route.get("supporting_route")
    supporting_name: str | None
    if supporting is None:
        supporting_name = None
    elif supporting not in ROUTES:
        errors.append(
            "route_decision.supporting_route must be null or a supported route."
        )
        supporting_name = None
    else:
        supporting_name = str(supporting)

    if primary_name and supporting_name == primary_name:
        errors.append("Primary and supporting routes must be different.")

    scope = route.get("supporting_scope")
    if not isinstance(scope, str):
        errors.append("route_decision.supporting_scope must be a string.")
    elif supporting_name and not scope.strip():
        errors.append(
            "route_decision.supporting_scope is required for a supporting route."
        )

    confidence = route.get("confidence")
    if confidence not in {"low", "medium", "high"}:
        errors.append("route_decision.confidence must be low, medium, or high.")
        confidence_name = ""
    else:
        confidence_name = str(confidence)

    for field in ("rationale", "rejected_alternative"):
        require_nonempty_string(route, field, "route_decision", errors)

    for field in (
        "override_reason",
        "named_reference_translation",
    ):
        if not isinstance(route.get(field), str):
            errors.append(f"route_decision.{field} must be a string.")

    validate_candidate_scores(route, primary_name, errors)
    return primary_name, supporting_name, confidence_name


def validate_visual_system(data: dict[str, object], errors: list[str]) -> None:
    visual = require_object(data, "visual_system", errors)
    for field in VISUAL_FIELDS:
        if field in {"identity_anchors", "variation_axes"}:
            validate_string_list(
                visual.get(field),
                f"visual_system.{field}",
                errors,
                minimum=2,
            )
        elif field in {"typography_roles", "palette_roles"}:
            value = visual.get(field)
            if not isinstance(value, dict) or len(value) < 2:
                errors.append(
                    f"visual_system.{field} must be an object with at least "
                    "two roles."
                )
            elif any(
                not isinstance(item, str) or not item.strip()
                for item in value.values()
            ):
                errors.append(
                    f"visual_system.{field} values must be non-empty strings."
                )
        else:
            require_nonempty_string(visual, field, "visual_system", errors)

    palette = visual.get("palette_roles")
    if isinstance(palette, dict):
        if len(palette) < 3:
            errors.append(
                "visual_system.palette_roles must contain at least three colors."
            )
        for role, value in palette.items():
            if isinstance(value, str) and not HEX_COLOR.search(value):
                errors.append(
                    f"visual_system.palette_roles.{role} must include a "
                    "six-digit hex color."
                )


def validate_visual_evidence(data: dict[str, object], errors: list[str]) -> None:
    evidence = require_object(data, "visual_evidence", errors)

    reference_status = evidence.get("reference_analysis_status")
    if reference_status not in {"completed", "not_supplied"}:
        errors.append(
            "visual_evidence.reference_analysis_status must be completed "
            "or not_supplied."
        )

    reference_path = evidence.get("reference_analysis_path")
    if not isinstance(reference_path, str):
        errors.append(
            "visual_evidence.reference_analysis_path must be a string."
        )
    elif reference_status == "completed" and not reference_path.strip():
        errors.append(
            "visual_evidence.reference_analysis_path is required when "
            "reference analysis is completed."
        )

    require_nonempty_string(
        evidence,
        "asset_readiness_path",
        "visual_evidence",
        errors,
    )
    selected = require_nonempty_string(
        evidence,
        "selected_direction",
        "visual_evidence",
        errors,
    )
    require_nonempty_string(
        evidence,
        "selection_evidence",
        "visual_evidence",
        errors,
    )

    waiver = evidence.get("comparison_waiver")
    if not isinstance(waiver, str):
        errors.append("visual_evidence.comparison_waiver must be a string.")
        waiver_text = ""
    else:
        waiver_text = waiver.strip()

    candidates = evidence.get("direction_candidates")
    if not isinstance(candidates, list) or not candidates:
        errors.append(
            "visual_evidence.direction_candidates must contain at least "
            "one candidate."
        )
        return
    if len(candidates) < 2 and not waiver_text:
        errors.append(
            "At least two visual direction candidates are required unless "
            "visual_evidence.comparison_waiver explains why."
        )

    candidate_ids: set[str] = set()
    for index, candidate in enumerate(candidates):
        path = f"visual_evidence.direction_candidates[{index}]"
        if not isinstance(candidate, dict):
            errors.append(f"{path} must be a JSON object.")
            continue

        candidate_id = require_nonempty_string(
            candidate, "id", path, errors
        )
        if candidate_id:
            if candidate_id in candidate_ids:
                errors.append(f"{path}.id duplicates {candidate_id}.")
            candidate_ids.add(candidate_id)

        if candidate.get("route") not in ROUTES:
            errors.append(f"{path}.route must be a supported route.")
        for field in (
            "premise",
            "primary_material_requirement",
            "strength",
            "risk",
        ):
            require_nonempty_string(candidate, field, path, errors)
        validate_string_list(
            candidate.get("hero_frame_concepts"),
            f"{path}.hero_frame_concepts",
            errors,
            minimum=3,
        )

    if selected and selected not in candidate_ids:
        errors.append(
            "visual_evidence.selected_direction must match a candidate id."
        )


def validate_project_fingerprint(
    data: dict[str, object], errors: list[str]
) -> None:
    fingerprint = require_object(data, "project_fingerprint", errors)
    for field in (
        "recognition_target",
        "blind_test_prompt",
        "differentiation_strategy",
    ):
        require_nonempty_string(
            fingerprint,
            field,
            "project_fingerprint",
            errors,
        )

    proof_assets = validate_string_list(
        fingerprint.get("proof_assets"),
        "project_fingerprint.proof_assets",
        errors,
        minimum=1,
    )
    validate_string_list(
        fingerprint.get("confusable_with"),
        "project_fingerprint.confusable_with",
        errors,
        minimum=1,
    )

    proof_asset_ids = set(proof_assets)
    scenes = data.get("scenes")
    scene_ids = (
        {
            scene["id"]
            for scene in scenes
            if isinstance(scene, dict)
            and isinstance(scene.get("id"), str)
            and scene["id"].strip()
        }
        if isinstance(scenes, list)
        else set()
    )

    anchors = fingerprint.get("anchors")
    if not isinstance(anchors, list) or len(anchors) < 3:
        errors.append(
            "project_fingerprint.anchors must contain at least three anchors."
        )
        anchors = []

    anchor_ids: set[str] = set()
    anchor_types: set[str] = set()
    minimum_appearances: dict[str, int] = {}
    for index, anchor in enumerate(anchors):
        path = f"project_fingerprint.anchors[{index}]"
        if not isinstance(anchor, dict):
            errors.append(f"{path} must be a JSON object.")
            continue

        anchor_id = require_nonempty_string(anchor, "id", path, errors)
        if anchor_id:
            if anchor_id in anchor_ids:
                errors.append(f"{path}.id duplicates {anchor_id}.")
            anchor_ids.add(anchor_id)

        anchor_type = anchor.get("type")
        if anchor_type not in FINGERPRINT_TYPES:
            errors.append(f"{path}.type must be a supported fingerprint type.")
        else:
            anchor_types.add(str(anchor_type))

        require_nonempty_string(anchor, "description", path, errors)
        appearances = anchor.get("minimum_scene_appearances")
        minimum_anchor_appearances = 1 if len(scene_ids) == 1 else 2
        if (
            not isinstance(appearances, int)
            or isinstance(appearances, bool)
            or appearances < minimum_anchor_appearances
        ):
            errors.append(
                f"{path}.minimum_scene_appearances must be an integer "
                f"of at least {minimum_anchor_appearances}."
            )
        elif scene_ids and appearances > len(scene_ids):
            errors.append(
                f"{path}.minimum_scene_appearances exceeds the scene count."
            )
        elif anchor_id:
            minimum_appearances[anchor_id] = appearances

    for required_type in ("semantic_transformation", "source_evidence"):
        if required_type not in anchor_types:
            errors.append(
                "project_fingerprint.anchors must include a "
                f"{required_type} anchor."
            )

    recurrence = fingerprint.get("scene_recurrence")
    if not isinstance(recurrence, list) or not recurrence:
        errors.append(
            "project_fingerprint.scene_recurrence must contain scene mappings."
        )
        return

    mapped_scenes: set[str] = set()
    anchor_counts = {anchor_id: 0 for anchor_id in anchor_ids}
    proof_asset_counts = {asset_id: 0 for asset_id in proof_asset_ids}
    core_scene_count = 0
    copy_only_count = 0
    identity_roles: set[str] = set()
    semantic_anchor_ids = {
        str(anchor.get("id"))
        for anchor in anchors
        if isinstance(anchor, dict)
        and anchor.get("type") == "semantic_transformation"
        and isinstance(anchor.get("id"), str)
    }
    source_anchor_ids = {
        str(anchor.get("id"))
        for anchor in anchors
        if isinstance(anchor, dict)
        and anchor.get("type") == "source_evidence"
        and isinstance(anchor.get("id"), str)
    }
    for index, item in enumerate(recurrence):
        path = f"project_fingerprint.scene_recurrence[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{path} must be a JSON object.")
            continue

        scene_id = require_nonempty_string(item, "scene_id", path, errors)
        if scene_id:
            if scene_id not in scene_ids:
                errors.append(f"{path}.scene_id references an unknown scene.")
            if scene_id in mapped_scenes:
                errors.append(f"{path}.scene_id duplicates {scene_id}.")
            mapped_scenes.add(scene_id)

        mapped_anchors = validate_string_list(
            item.get("anchor_ids"),
            f"{path}.anchor_ids",
            errors,
            minimum=1,
        )
        unknown = [
            anchor_id
            for anchor_id in mapped_anchors
            if anchor_id not in anchor_ids
        ]
        if unknown:
            errors.append(
                f"{path}.anchor_ids references unknown anchors: "
                + ", ".join(unknown)
                + "."
            )
        for anchor_id in set(mapped_anchors):
            if anchor_id in anchor_counts:
                anchor_counts[anchor_id] += 1

        identity_role = item.get("identity_role")
        if identity_role not in IDENTITY_ROLES:
            errors.append(f"{path}.identity_role must be a supported role.")
            identity_role_name = ""
        else:
            identity_role_name = str(identity_role)
            identity_roles.add(identity_role_name)

        swap_result = item.get("template_swap_result")
        if swap_result not in TEMPLATE_SWAP_RESULTS:
            errors.append(
                f"{path}.template_swap_result must be requires_redesign "
                "or copy_only."
            )
            swap_result_name = ""
        else:
            swap_result_name = str(swap_result)
            if swap_result_name == "copy_only":
                copy_only_count += 1

        is_core = item.get("core_identity_scene")
        if not isinstance(is_core, bool):
            errors.append(f"{path}.core_identity_scene must be a boolean.")
            is_core = False
        elif is_core:
            core_scene_count += 1

        scene_proof_assets = validate_string_list(
            item.get("proof_asset_ids"),
            f"{path}.proof_asset_ids",
            errors,
            minimum=1 if is_core else 0,
        )
        unknown_assets = [
            asset_id
            for asset_id in scene_proof_assets
            if asset_id not in proof_asset_ids
        ]
        if unknown_assets:
            errors.append(
                f"{path}.proof_asset_ids references unknown proof assets: "
                + ", ".join(unknown_assets)
                + "."
            )
        for asset_id in set(scene_proof_assets):
            if asset_id in proof_asset_counts:
                proof_asset_counts[asset_id] += 1

        replacement_dimensions = validate_string_list(
            item.get("replacement_dimensions"),
            f"{path}.replacement_dimensions",
            errors,
            minimum=2 if is_core else 0,
        )
        unsupported_dimensions = [
            dimension
            for dimension in replacement_dimensions
            if dimension not in REPLACEMENT_DIMENSIONS
        ]
        if unsupported_dimensions:
            errors.append(
                f"{path}.replacement_dimensions contains unsupported values: "
                + ", ".join(unsupported_dimensions)
                + "."
            )

        if is_core:
            if swap_result_name == "copy_only":
                errors.append(
                    f"{path} is a core identity scene but passes the "
                    "template swap with copy-only changes."
                )
            if not semantic_anchor_ids.intersection(mapped_anchors):
                errors.append(
                    f"{path} is a core identity scene without a "
                    "semantic_transformation anchor."
                )
            if not source_anchor_ids.intersection(mapped_anchors):
                errors.append(
                    f"{path} is a core identity scene without a "
                    "source_evidence anchor."
                )

        require_nonempty_string(
            item,
            "project_specific_evidence",
            path,
            errors,
        )

    missing_scenes = sorted(scene_ids - mapped_scenes)
    if missing_scenes:
        errors.append(
            "project_fingerprint.scene_recurrence must cover every scene; "
            "missing: "
            + ", ".join(missing_scenes)
            + "."
        )

    for anchor_id, minimum in minimum_appearances.items():
        actual = anchor_counts.get(anchor_id, 0)
        if actual < minimum:
            errors.append(
                f"Project fingerprint anchor {anchor_id} appears in {actual} "
                f"scene(s); minimum is {minimum}."
            )

    scene_count = len(scene_ids)
    minimum_core_scenes = (
        1 if scene_count == 1 else max(2, (scene_count * 3 + 4) // 5)
    )
    if core_scene_count < minimum_core_scenes:
        errors.append(
            f"Project fingerprint has {core_scene_count} core identity "
            f"scene(s); minimum is {minimum_core_scenes} for {scene_count} scenes."
        )

    maximum_copy_only = scene_count // 4
    if copy_only_count > maximum_copy_only:
        errors.append(
            f"Project fingerprint has {copy_only_count} copy-only scene(s); "
            f"maximum is {maximum_copy_only}."
        )

    if scene_count == 1:
        required_roles = ("complete",)
    elif scene_count == 2:
        required_roles = ("establish", "resolve")
    else:
        required_roles = ("establish", "prove", "resolve")
    for required_role in required_roles:
        if required_role not in identity_roles:
            errors.append(
                "project_fingerprint.scene_recurrence must include an "
                f"{required_role} identity role."
            )

    unused_assets = sorted(
        asset_id
        for asset_id, count in proof_asset_counts.items()
        if count == 0
    )
    if unused_assets:
        errors.append(
            "Project fingerprint proof assets are not mapped to scenes: "
            + ", ".join(unused_assets)
            + "."
        )

    swap_test = fingerprint.get("template_swap_test")
    if not isinstance(swap_test, dict):
        errors.append("project_fingerprint.template_swap_test must be an object.")
    else:
        require_nonempty_string(
            swap_test,
            "alternate_project",
            "project_fingerprint.template_swap_test",
            errors,
        )
        if swap_test.get("result") != "requires_redesign":
            errors.append(
                "project_fingerprint.template_swap_test.result must be "
                "requires_redesign."
            )
        required_redesigns = validate_string_list(
            swap_test.get("required_redesigns"),
            "project_fingerprint.template_swap_test.required_redesigns",
            errors,
            minimum=3,
        )
        unsupported_redesigns = [
            dimension
            for dimension in required_redesigns
            if dimension not in REPLACEMENT_DIMENSIONS
        ]
        if unsupported_redesigns:
            errors.append(
                "project_fingerprint.template_swap_test.required_redesigns "
                "contains unsupported values: "
                + ", ".join(unsupported_redesigns)
                + "."
            )
        require_nonempty_string(
            swap_test,
            "evidence",
            "project_fingerprint.template_swap_test",
            errors,
        )


def validate_rhythm(data: dict[str, object], errors: list[str]) -> None:
    rhythm = require_object(data, "rhythm_map", errors)
    for field in ("arrival", "development", "contrast", "climax", "resolve"):
        require_nonempty_string(rhythm, field, "rhythm_map", errors)


def validate_scenes(
    data: dict[str, object],
    planned_duration: float | None,
    supporting_route: str | None,
    errors: list[str],
) -> None:
    scenes = data.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        errors.append("scenes must contain at least one scene.")
        return

    ids: set[str] = set()
    total_duration = 0.0
    supporting_duration = 0.0
    supporting_count = 0

    for index, scene in enumerate(scenes):
        path = f"scenes[{index}]"
        if not isinstance(scene, dict):
            errors.append(f"{path} must be a JSON object.")
            continue

        for field in SCENE_TEXT_FIELDS:
            require_nonempty_string(scene, field, path, errors)

        scene_id = scene.get("id")
        if isinstance(scene_id, str) and scene_id.strip():
            if scene_id in ids:
                errors.append(f"{path}.id duplicates {scene_id}.")
            ids.add(scene_id)

        validate_string_list(
            scene.get("source_material"),
            f"{path}.source_material",
            errors,
            minimum=1,
        )

        duration = scene.get("duration_seconds")
        if not is_number(duration) or duration <= 0:
            errors.append(f"{path}.duration_seconds must be a positive number.")
            duration_value = 0.0
        else:
            duration_value = float(duration)
            total_duration += duration_value

        if scene.get("energy") not in {"low", "medium", "high"}:
            errors.append(f"{path}.energy must be low, medium, or high.")

        route_role = scene.get("route_role")
        if route_role not in {"primary", "supporting"}:
            errors.append(f"{path}.route_role must be primary or supporting.")
        elif route_role == "supporting":
            supporting_count += 1
            supporting_duration += duration_value
            if supporting_route is None:
                errors.append(
                    f"{path} uses route_role supporting without a supporting route."
                )

    if planned_duration is not None and abs(total_duration - planned_duration) > 0.1:
        errors.append(
            f"Scene durations total {total_duration:.2f}s; planned duration is "
            f"{planned_duration:.2f}s."
        )

    if supporting_route and supporting_count == 0:
        errors.append(
            "At least one scene must use route_role supporting when a "
            "supporting route is declared."
        )

    route = data.get("route_decision")
    override = route.get("override_reason") if isinstance(route, dict) else ""
    if total_duration > 0 and supporting_duration / total_duration > 0.4:
        if not isinstance(override, str) or not override.strip():
            errors.append(
                "Supporting-route scenes exceed 40% of the timeline; provide "
                "route_decision.override_reason or reduce their duration."
            )


def validate_direction(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["Direction brief root must be a JSON object."]

    require_nonempty_string(data, "project", "root", errors)
    mode = data.get("mode")
    if mode not in {"full_direction", "review_pass", "fast_pass"}:
        errors.append(
            "mode must be full_direction, review_pass, or fast_pass."
        )

    planned_duration = validate_delivery(data, errors)
    validate_content_profile(data, errors)
    _, supporting_route, confidence = validate_route_decision(data, errors)
    require_nonempty_string(data, "creative_thesis", "root", errors)
    validate_visual_evidence(data, errors)
    validate_project_fingerprint(data, errors)
    validate_visual_system(data, errors)
    validate_rhythm(data, errors)
    validate_scenes(data, planned_duration, supporting_route, errors)
    validate_string_list(data.get("avoidances"), "avoidances", errors, minimum=3)
    assumptions = validate_string_list(
        data.get("assumptions"), "assumptions", errors
    )
    validate_string_list(
        data.get("style_preferences_applied"),
        "style_preferences_applied",
        errors,
    )
    validate_string_list(
        data.get("style_preferences_rejected"),
        "style_preferences_rejected",
        errors,
    )
    if confidence == "low" and not assumptions:
        errors.append("Low-confidence directions must record at least one assumption.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a HyperFrames structured art-direction brief."
    )
    parser.add_argument(
        "direction_brief",
        type=Path,
        help="Path to direction-brief.json.",
    )
    args = parser.parse_args()

    try:
        data = json.loads(args.direction_brief.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: File not found: {args.direction_brief}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON: {exc}", file=sys.stderr)
        return 2

    errors = validate_direction(data)
    if errors:
        print("DIRECTION BRIEF FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    scenes = data["scenes"]
    duration = sum(scene["duration_seconds"] for scene in scenes)
    route = data["route_decision"]["primary_route"]
    recurrence = data["project_fingerprint"]["scene_recurrence"]
    core_scenes = sum(
        1 for item in recurrence if item["core_identity_scene"]
    )
    print(
        f"DIRECTION BRIEF PASSED: route={route}, "
        f"scenes={len(scenes)}, core_identity={core_scenes}/{len(scenes)}, "
        f"duration={duration:.2f}s"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
