#!/usr/bin/env python3
"""Validate pre-voice content coverage, interaction loop, and scene density."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


DEFAULT_THRESHOLDS = {
    "experience_percent_min": 40.0,
    "interaction_percent_min": 20.0,
    "combined_unique_percent_min": 60.0,
    "max_uncovered_gap_percent": 15.0,
    "long_scene_seconds": 8.0,
    "min_information_units_long_scene": 3.0,
}


def is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def merge_ranges(ranges: list[dict[str, object]]) -> list[dict[str, float]]:
    merged: list[dict[str, float]] = []
    for item in sorted(ranges, key=lambda value: (float(value["start"]), float(value["end"]))):
        start = float(item["start"])
        end = float(item["end"])
        if not merged or start > merged[-1]["end"]:
            merged.append({"start": start, "end": end})
        else:
            merged[-1]["end"] = max(merged[-1]["end"], end)
    return merged


def ranges_duration(ranges: list[dict[str, object]]) -> float:
    return sum(item["end"] - item["start"] for item in merge_ranges(ranges))


def validate_ranges(
    name: str,
    value: object,
    runtime: float,
    errors: list[str],
) -> list[dict[str, object]]:
    if not isinstance(value, list) or not value:
        errors.append(f"{name} must contain at least one range.")
        return []

    valid: list[dict[str, object]] = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"{name}[{index}] must be an object.")
            continue
        start = item.get("start")
        end = item.get("end")
        if (
            not is_number(start)
            or not is_number(end)
            or float(start) < 0
            or float(end) <= float(start)
            or float(end) > runtime
        ):
            errors.append(f"{name}[{index}] must satisfy 0 <= start < end <= runtime.")
            continue
        valid.append({**item, "start": float(start), "end": float(end)})
    return valid


def largest_uncovered_gap(
    ranges: list[dict[str, object]], runtime: float
) -> tuple[float, float]:
    cursor = 0.0
    largest = (0.0, 0.0)
    for item in merge_ranges(ranges):
        if item["start"] - cursor > largest[1] - largest[0]:
            largest = (cursor, item["start"])
        cursor = max(cursor, item["end"])
    if runtime - cursor > largest[1] - largest[0]:
        largest = (cursor, runtime)
    return largest


def validate_content_rhythm(data: object) -> tuple[list[str], dict[str, object]]:
    if not isinstance(data, dict):
        return ["Content rhythm root must be a JSON object."], {}

    errors: list[str] = []
    runtime_value = data.get("runtime_seconds")
    if not is_number(runtime_value) or float(runtime_value) <= 0:
        return ["runtime_seconds must be a positive number."], {}
    runtime = float(runtime_value)

    thresholds = dict(DEFAULT_THRESHOLDS)
    overrides = data.get("thresholds", {})
    if not isinstance(overrides, dict):
        errors.append("thresholds must be an object.")
        overrides = {}
    for name, value in overrides.items():
        if name not in thresholds:
            errors.append(f"thresholds.{name} is not supported.")
        elif not is_number(value) or float(value) < 0:
            errors.append(f"thresholds.{name} must be a non-negative number.")
        else:
            thresholds[name] = float(value)

    experience = validate_ranges(
        "experience_ranges", data.get("experience_ranges"), runtime, errors
    )
    interaction = validate_ranges(
        "interaction_ranges", data.get("interaction_ranges"), runtime, errors
    )

    experience_seconds = ranges_duration(experience)
    interaction_seconds = ranges_duration(interaction)
    combined_seconds = ranges_duration([*experience, *interaction])
    experience_percent = experience_seconds / runtime * 100
    interaction_percent = interaction_seconds / runtime * 100
    combined_percent = combined_seconds / runtime * 100

    if experience_percent < thresholds["experience_percent_min"]:
        errors.append(
            f"Experience coverage {experience_percent:.1f}% is below "
            f"{thresholds['experience_percent_min']:.1f}%."
        )
    if interaction_percent < thresholds["interaction_percent_min"]:
        errors.append(
            f"Interaction coverage {interaction_percent:.1f}% is below "
            f"{thresholds['interaction_percent_min']:.1f}%."
        )
    if combined_percent < thresholds["combined_unique_percent_min"]:
        errors.append(
            f"Combined unique coverage {combined_percent:.1f}% is below "
            f"{thresholds['combined_unique_percent_min']:.1f}%."
        )

    phases = {
        str(item.get("phase", "")).lower(): item for item in interaction
    }
    for phase in ("opening", "middle", "closing"):
        if phase not in phases:
            errors.append(f"interaction_ranges must include phase={phase}.")
    if "opening" in phases and float(phases["opening"]["start"]) > runtime * 0.15:
        errors.append("Opening interaction must begin within the first 15 percent.")
    if "middle" in phases and float(phases["middle"]["start"]) > runtime * 0.60:
        errors.append("Middle interaction must begin before 60 percent.")
    if "closing" in phases and float(phases["closing"]["end"]) < runtime * 0.85:
        errors.append("Closing interaction must resolve after 85 percent.")

    gap_start, gap_end = largest_uncovered_gap([*experience, *interaction], runtime)
    gap_percent = (gap_end - gap_start) / runtime * 100
    if gap_percent > thresholds["max_uncovered_gap_percent"]:
        errors.append(
            f"Largest unclassified gap {gap_start:.2f}-{gap_end:.2f}s "
            f"({gap_percent:.1f}%) exceeds "
            f"{thresholds['max_uncovered_gap_percent']:.1f}%."
        )

    scenes = data.get("scenes")
    long_scenes = 0
    if not isinstance(scenes, list) or not scenes:
        errors.append("scenes must contain the planned scene rhythm map.")
    else:
        for index, scene in enumerate(scenes):
            if not isinstance(scene, dict):
                errors.append(f"scenes[{index}] must be an object.")
                continue
            start = scene.get("start")
            end = scene.get("end")
            units = scene.get("information_units")
            if (
                not is_number(start)
                or not is_number(end)
                or float(start) < 0
                or float(end) <= float(start)
                or float(end) > runtime
            ):
                errors.append(f"scenes[{index}] must satisfy 0 <= start < end <= runtime.")
                continue
            if not is_number(units) or float(units) < 0:
                errors.append(f"scenes[{index}].information_units must be non-negative.")
                continue
            scene_duration = float(end) - float(start)
            if scene_duration >= thresholds["long_scene_seconds"]:
                long_scenes += 1
                if float(units) < thresholds["min_information_units_long_scene"]:
                    label = scene.get("label", str(index))
                    errors.append(
                        f"Long scene {label!r} has {float(units):g} information units; "
                        f"minimum is {thresholds['min_information_units_long_scene']:g}."
                    )

    report = {
        "experience_percent": round(experience_percent, 1),
        "interaction_percent": round(interaction_percent, 1),
        "combined_unique_percent": round(combined_percent, 1),
        "largest_uncovered_gap_seconds": round(gap_end - gap_start, 2),
        "long_scenes_checked": long_scenes,
    }
    return errors, report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate content coverage and rhythm before voice generation."
    )
    parser.add_argument("rhythm", type=Path, help="Path to content-rhythm.json.")
    args = parser.parse_args()

    try:
        data = json.loads(args.rhythm.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: File not found: {args.rhythm}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON: {exc}", file=sys.stderr)
        return 2

    errors, report = validate_content_rhythm(data)
    if errors:
        print("CONTENT RHYTHM QA FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "CONTENT RHYTHM QA PASSED: "
        f"experience={report['experience_percent']:.1f}%, "
        f"interaction={report['interaction_percent']:.1f}%, "
        f"combined={report['combined_unique_percent']:.1f}%, "
        f"largest_gap={report['largest_uncovered_gap_seconds']:.2f}s, "
        f"long_scenes={report['long_scenes_checked']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
