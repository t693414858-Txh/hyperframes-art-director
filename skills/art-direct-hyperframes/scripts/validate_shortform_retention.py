#!/usr/bin/env python3
"""Validate an applicable short-form video's retention plan."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SHORTFORM_THRESHOLDS = {
    "problem_and_result_preview_seconds_max": 0.8,
    "first_real_operation_seconds_max": 2.5,
    "first_visible_proof_seconds_max": 5.0,
    "before_after_or_verification_seconds_max": 8.0,
    "early_window_seconds": 12.0,
    "meaningful_state_change_gap_seconds_max": 2.5,
    "single_task_runtime_seconds_max": 35.0,
    "multi_step_runtime_seconds_max": 50.0,
    "runtime_waiver_chapter_count_min": 2,
}

ALLOWED_PLATFORMS = {"douyin", "tiktok", "reels", "shorts", "other_shortform"}
ALLOWED_FORMATS = {"single_task", "multi_step"}
ALLOWED_EVIDENCE_CARRIERS = {
    "continuous_desktop_operation",
    "continuous_physical_demonstration",
    "continuous_source_transformation",
}
REQUIRED_OPERATION_STEPS = {"input", "operation", "visible_result", "verification"}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("root JSON value must be an object")
    return data


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def require_text(value: Any, field: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{field} must be a non-empty string")


def require_time(
    value: Any,
    field: str,
    runtime_seconds: float | None,
    errors: list[str],
) -> float | None:
    if not is_number(value):
        errors.append(f"{field} must be a number")
        return None
    timestamp = float(value)
    if timestamp < 0:
        errors.append(f"{field} must be >= 0")
    if runtime_seconds is not None and timestamp > runtime_seconds:
        errors.append(f"{field} cannot exceed runtime_seconds")
    return timestamp


def validate_plan(data: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []

    require_text(data.get("project"), "project", errors)

    platform = data.get("platform")
    if platform not in ALLOWED_PLATFORMS:
        errors.append(f"platform must be one of {sorted(ALLOWED_PLATFORMS)}")

    video_format = data.get("format")
    if video_format not in ALLOWED_FORMATS:
        errors.append(f"format must be one of {sorted(ALLOWED_FORMATS)}")

    runtime_value = data.get("runtime_seconds")
    runtime_seconds: float | None = None
    if not is_number(runtime_value) or float(runtime_value) <= 0:
        errors.append("runtime_seconds must be a positive number")
    else:
        runtime_seconds = float(runtime_value)

    checkpoints = data.get("checkpoints")
    checkpoint_values: dict[str, float | None] = {}
    checkpoint_limits = {
        "problem_and_result_preview_seconds": SHORTFORM_THRESHOLDS[
            "problem_and_result_preview_seconds_max"
        ],
        "first_real_operation_seconds": SHORTFORM_THRESHOLDS[
            "first_real_operation_seconds_max"
        ],
        "first_visible_proof_seconds": SHORTFORM_THRESHOLDS[
            "first_visible_proof_seconds_max"
        ],
        "before_after_or_verification_seconds": SHORTFORM_THRESHOLDS[
            "before_after_or_verification_seconds_max"
        ],
    }
    if not isinstance(checkpoints, dict):
        errors.append("checkpoints must be an object")
    else:
        for field, limit in checkpoint_limits.items():
            value = require_time(
                checkpoints.get(field),
                f"checkpoints.{field}",
                runtime_seconds,
                errors,
            )
            checkpoint_values[field] = value
            if value is not None and value > limit:
                errors.append(
                    f"checkpoints.{field} must be <= {limit:.1f}s; got {value:.1f}s"
                )

    state_changes = data.get("meaningful_state_changes")
    timestamps: list[float] = []
    if not isinstance(state_changes, list) or not state_changes:
        errors.append("meaningful_state_changes must be a non-empty array")
    else:
        for index, item in enumerate(state_changes):
            prefix = f"meaningful_state_changes[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{prefix} must be an object")
                continue
            timestamp = require_time(
                item.get("timestamp_seconds"),
                f"{prefix}.timestamp_seconds",
                runtime_seconds,
                errors,
            )
            require_text(item.get("description"), f"{prefix}.description", errors)
            require_text(item.get("evidence"), f"{prefix}.evidence", errors)
            if timestamp is not None:
                timestamps.append(timestamp)

    if timestamps and timestamps != sorted(timestamps):
        errors.append("meaningful_state_changes must be ordered by timestamp")
    if len(timestamps) != len(set(timestamps)):
        errors.append("meaningful_state_changes timestamps must be unique")

    early_window = (
        min(SHORTFORM_THRESHOLDS["early_window_seconds"], runtime_seconds)
        if runtime_seconds is not None
        else SHORTFORM_THRESHOLDS["early_window_seconds"]
    )
    early_timestamps = [timestamp for timestamp in timestamps if timestamp <= early_window]
    boundaries = [0.0, *early_timestamps, early_window]
    max_gap = 0.0
    if len(boundaries) >= 2:
        max_gap = max(
            later - earlier for earlier, later in zip(boundaries, boundaries[1:])
        )
        allowed_gap = SHORTFORM_THRESHOLDS[
            "meaningful_state_change_gap_seconds_max"
        ]
        if max_gap > allowed_gap:
            errors.append(
                "meaningful_state_changes must cover the first "
                f"{early_window:.1f}s with gaps <= {allowed_gap:.1f}s; "
                f"largest gap is {max_gap:.1f}s"
            )

    operation_chain = data.get("operation_chain")
    if not isinstance(operation_chain, dict):
        errors.append("operation_chain must be an object")
    else:
        start = require_time(
            operation_chain.get("start_seconds"),
            "operation_chain.start_seconds",
            runtime_seconds,
            errors,
        )
        end = require_time(
            operation_chain.get("end_seconds"),
            "operation_chain.end_seconds",
            runtime_seconds,
            errors,
        )
        if start is not None and start > SHORTFORM_THRESHOLDS[
            "first_real_operation_seconds_max"
        ]:
            errors.append("operation_chain.start_seconds must be <= 2.5s")
        if end is not None and end < early_window:
            errors.append(
                f"operation_chain.end_seconds must reach at least {early_window:.1f}s"
            )
        if start is not None and end is not None and end <= start:
            errors.append("operation_chain.end_seconds must be greater than start_seconds")
        if operation_chain.get("continuous_workspace") is not True:
            errors.append("operation_chain.continuous_workspace must be true")
        steps = operation_chain.get("steps")
        if not isinstance(steps, list):
            errors.append("operation_chain.steps must be an array")
        else:
            missing_steps = REQUIRED_OPERATION_STEPS - set(steps)
            if missing_steps:
                errors.append(
                    "operation_chain.steps is missing: "
                    + ", ".join(sorted(missing_steps))
                )

    presentation = data.get("presentation")
    if not isinstance(presentation, dict):
        errors.append("presentation must be an object")
    else:
        if presentation.get("poster_or_card_montage") is not False:
            errors.append("presentation.poster_or_card_montage must be false")
        carrier = presentation.get("primary_evidence_carrier")
        if carrier not in ALLOWED_EVIDENCE_CARRIERS:
            errors.append(
                "presentation.primary_evidence_carrier must be one of "
                f"{sorted(ALLOWED_EVIDENCE_CARRIERS)}"
            )

    runtime_limit = None
    if video_format == "single_task":
        runtime_limit = SHORTFORM_THRESHOLDS["single_task_runtime_seconds_max"]
    elif video_format == "multi_step":
        runtime_limit = SHORTFORM_THRESHOLDS["multi_step_runtime_seconds_max"]

    waiver_used = False
    if (
        runtime_seconds is not None
        and runtime_limit is not None
        and runtime_seconds > runtime_limit
    ):
        waiver = data.get("runtime_waiver")
        if not isinstance(waiver, dict):
            errors.append(
                f"runtime_seconds exceeds the {runtime_limit:.0f}s {video_format} "
                "limit and requires runtime_waiver"
            )
        else:
            waiver_used = True
            require_text(waiver.get("reason"), "runtime_waiver.reason", errors)
            require_text(
                waiver.get("split_rejected_reason"),
                "runtime_waiver.split_rejected_reason",
                errors,
            )
            chapter_count = waiver.get("chapter_count")
            if (
                not isinstance(chapter_count, int)
                or isinstance(chapter_count, bool)
                or chapter_count
                < SHORTFORM_THRESHOLDS["runtime_waiver_chapter_count_min"]
            ):
                errors.append("runtime_waiver.chapter_count must be an integer >= 2")

    report = {
        "project": data.get("project"),
        "platform": platform,
        "format": video_format,
        "runtime_seconds": runtime_seconds,
        "runtime_limit_seconds": runtime_limit,
        "early_window_seconds": early_window,
        "largest_early_state_change_gap_seconds": round(max_gap, 3),
        "runtime_waiver_used": waiver_used,
        "error_count": len(errors),
    }
    return errors, report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a short-form retention plan before production."
    )
    parser.add_argument("path", help="Path to shortform-retention-plan.json")
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    args = parser.parse_args()

    try:
        data = load_json(Path(args.path))
        errors, report = validate_plan(data)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps({"ok": not errors, "errors": errors, "report": report}, indent=2))
    elif errors:
        print("Short-form retention validation failed:")
        for error in errors:
            print(f"- {error}")
    else:
        print(
            "Short-form retention validation passed: "
            f"{report['format']}, {report['runtime_seconds']:.1f}s, "
            "early state-change gap "
            f"{report['largest_early_state_change_gap_seconds']:.1f}s."
        )

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
