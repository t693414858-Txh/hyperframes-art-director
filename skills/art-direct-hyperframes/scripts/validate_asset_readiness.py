#!/usr/bin/env python3
"""Validate a HyperFrames art-direction asset-readiness report."""

from __future__ import annotations

import argparse
import json
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

ASSET_TYPES = (
    "image",
    "video",
    "ui",
    "data",
    "document",
    "audio",
    "logo",
    "font",
    "texture",
    "illustration",
)

ROLES = ("primary", "supporting", "atmospheric", "reference_only")
LICENSE_STATUSES = (
    "owned",
    "licensed",
    "public_domain",
    "permission_granted",
    "internal_only",
    "unknown",
)
QUALITY_LEVELS = ("low", "medium", "high")


def nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def string_list(value: object) -> bool:
    return isinstance(value, list) and all(nonempty_string(item) for item in value)


def validate_asset_readiness(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["Asset-readiness root must be a JSON object."]

    for field in ("project", "primary_material_type", "route_recommendation"):
        if not nonempty_string(data.get(field)):
            errors.append(f"{field} must be a non-empty string.")

    route = data.get("intended_route")
    if route not in ROUTES:
        errors.append("intended_route must be a supported route.")

    status = data.get("status")
    if status not in {"ready", "degraded", "blocked"}:
        errors.append("status must be ready, degraded, or blocked.")

    limitations = data.get("limitations")
    if not string_list(limitations):
        errors.append("limitations must be a list of non-empty strings.")

    missing = data.get("missing_critical_assets")
    if not string_list(missing):
        errors.append(
            "missing_critical_assets must be a list of non-empty strings."
        )
        missing_items: list[str] = []
    else:
        missing_items = missing

    assets = data.get("assets")
    if not isinstance(assets, list):
        errors.append("assets must be a list.")
        assets = []

    asset_ids: set[str] = set()
    primary_assets = 0
    for index, asset in enumerate(assets):
        path = f"assets[{index}]"
        if not isinstance(asset, dict):
            errors.append(f"{path} must be a JSON object.")
            continue

        asset_id = asset.get("id")
        if not nonempty_string(asset_id):
            errors.append(f"{path}.id must be a non-empty string.")
        elif asset_id in asset_ids:
            errors.append(f"{path}.id duplicates {asset_id}.")
        else:
            asset_ids.add(asset_id)

        asset_type = asset.get("type")
        if asset_type not in ASSET_TYPES:
            errors.append(f"{path}.type must be a supported asset type.")

        for field in ("location", "provenance"):
            if not nonempty_string(asset.get(field)):
                errors.append(f"{path}.{field} must be a non-empty string.")

        role = asset.get("role")
        if role not in ROLES:
            errors.append(f"{path}.role must be a supported role.")
        elif role == "primary":
            primary_assets += 1

        license_status = asset.get("license_status")
        if license_status not in LICENSE_STATUSES:
            errors.append(
                f"{path}.license_status must be a supported license status."
            )
        elif role != "reference_only" and license_status == "unknown":
            errors.append(
                f"{path} has unknown rights but is declared as a production asset."
            )

        if asset.get("quality") not in QUALITY_LEVELS:
            errors.append(f"{path}.quality must be low, medium, or high.")

        for field in ("supports_scenes", "supports_claims"):
            if not string_list(asset.get(field)):
                errors.append(
                    f"{path}.{field} must be a list of non-empty strings."
                )

        if asset_type in {"image", "ui", "logo", "texture", "illustration"}:
            for field in ("width", "height"):
                value = asset.get(field)
                if (
                    not isinstance(value, int)
                    or isinstance(value, bool)
                    or value <= 0
                ):
                    errors.append(f"{path}.{field} must be a positive integer.")

        if asset_type in {"video", "audio"}:
            duration = asset.get("duration_seconds")
            if (
                not isinstance(duration, (int, float))
                or isinstance(duration, bool)
                or duration <= 0
            ):
                errors.append(
                    f"{path}.duration_seconds must be a positive number."
                )

    coverage = data.get("coverage")
    if not isinstance(coverage, list) or not coverage:
        errors.append("coverage must contain at least one requirement.")
        coverage = []

    coverage_ids: set[str] = set()
    for index, item in enumerate(coverage):
        path = f"coverage[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{path} must be a JSON object.")
            continue

        coverage_id = item.get("id")
        if not nonempty_string(coverage_id):
            errors.append(f"{path}.id must be a non-empty string.")
        elif coverage_id in coverage_ids:
            errors.append(f"{path}.id duplicates {coverage_id}.")
        else:
            coverage_ids.add(coverage_id)

        if item.get("kind") not in {"scene", "claim", "brand", "format"}:
            errors.append(f"{path}.kind must be scene, claim, brand, or format.")
        if not nonempty_string(item.get("description")):
            errors.append(f"{path}.description must be a non-empty string.")

        evidence_required = item.get("evidence_required")
        if not isinstance(evidence_required, bool):
            errors.append(f"{path}.evidence_required must be a boolean.")

        covered_by = item.get("covered_by")
        if not string_list(covered_by):
            errors.append(
                f"{path}.covered_by must be a list of non-empty asset ids."
            )
            covered_ids: list[str] = []
        else:
            covered_ids = covered_by

        missing_refs = [asset_id for asset_id in covered_ids if asset_id not in asset_ids]
        if missing_refs:
            errors.append(
                f"{path}.covered_by references unknown assets: "
                + ", ".join(missing_refs)
                + "."
            )
        if evidence_required is True and not covered_ids:
            errors.append(
                f"{path} requires evidence but has no supporting asset."
            )

    if status == "ready":
        if primary_assets == 0:
            errors.append("ready status requires at least one primary asset.")
        if missing_items:
            errors.append(
                "ready status cannot declare missing critical assets."
            )
    elif status == "blocked" and not missing_items:
        errors.append(
            "blocked status must identify at least one missing critical asset."
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a HyperFrames asset-readiness report."
    )
    parser.add_argument(
        "asset_readiness",
        type=Path,
        help="Path to asset-readiness.json.",
    )
    args = parser.parse_args()

    try:
        data = json.loads(args.asset_readiness.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: File not found: {args.asset_readiness}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON: {exc}", file=sys.stderr)
        return 2

    errors = validate_asset_readiness(data)
    if errors:
        print("ASSET READINESS FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "ASSET READINESS PASSED: "
        f"route={data['intended_route']}, status={data['status']}, "
        f"assets={len(data['assets'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
