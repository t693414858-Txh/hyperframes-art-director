#!/usr/bin/env python3
"""Validate experience and interaction QA for tutorial-style videos."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


EXPERIENCE_CHECKS = (
    "felt_change",
    "best_fit_task",
    "boundary",
    "evidence",
)

INTERACTION_CHECKS = (
    "early_invitation",
    "single_primary_action",
    "exact_response_format",
    "specific_reward",
    "contract_consistency",
)

CONSISTENCY_SURFACES = (
    "narration",
    "captions",
    "on_screen_cta",
    "publishing_description",
    "pinned_comment",
)


def nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def nonempty_string_list(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(
        nonempty_string(item) for item in value
    )


def number_in_runtime(value: object, runtime: float) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and 0 <= float(value) <= runtime
    )


def validate_common_check(
    check: object,
    path: str,
    runtime: float,
    errors: list[str],
) -> dict[str, object] | None:
    if not isinstance(check, dict):
        errors.append(f"{path} must be a JSON object.")
        return None

    status = check.get("status")
    if status not in {"pass", "fail"}:
        errors.append(f"{path}.status must be pass or fail.")
    elif status == "fail":
        errors.append(f"{path} has failed its gate.")

    if not nonempty_string_list(check.get("narration_lines")):
        errors.append(f"{path}.narration_lines must contain exact narration lines.")

    if not number_in_runtime(check.get("timestamp_seconds"), runtime):
        errors.append(
            f"{path}.timestamp_seconds must be a number within the video runtime."
        )

    if not nonempty_string(check.get("frame_evidence")):
        errors.append(f"{path}.frame_evidence must be a non-empty path or URL.")

    action = check.get("action")
    if action is not None and not isinstance(action, str):
        errors.append(f"{path}.action must be a string when present.")
    if status == "fail" and not nonempty_string(action):
        errors.append(f"{path}.action is required when status is fail.")

    return check


def validate_experience_gate(
    data: dict[str, object],
    runtime: float,
    errors: list[str],
) -> None:
    gate = data.get("experience_gate")
    if not isinstance(gate, dict):
        errors.append("experience_gate must be a JSON object.")
        return

    for name in EXPERIENCE_CHECKS:
        check = validate_common_check(gate.get(name), f"experience_gate.{name}", runtime, errors)
        if check is None:
            continue

        if name == "felt_change":
            for field in ("before", "after"):
                if not nonempty_string(check.get(field)):
                    errors.append(f"experience_gate.{name}.{field} must be non-empty.")
        elif name == "best_fit_task":
            for field in ("task_shape", "input", "operation", "result"):
                if not nonempty_string(check.get(field)):
                    errors.append(f"experience_gate.{name}.{field} must be non-empty.")
        elif name == "boundary":
            if not nonempty_string(check.get("limitation")):
                errors.append("experience_gate.boundary.limitation must be non-empty.")
        elif name == "evidence":
            if not nonempty_string(check.get("proof")):
                errors.append("experience_gate.evidence.proof must be non-empty.")


def validate_interaction_gate(
    data: dict[str, object],
    runtime: float,
    errors: list[str],
) -> None:
    gate = data.get("interaction_gate")
    if not isinstance(gate, dict):
        errors.append("interaction_gate must be a JSON object.")
        return

    for name in INTERACTION_CHECKS:
        check = validate_common_check(gate.get(name), f"interaction_gate.{name}", runtime, errors)
        if check is None:
            continue

        if name == "early_invitation":
            timestamp = check.get("timestamp_seconds")
            if number_in_runtime(timestamp, runtime) and float(timestamp) > runtime * 0.6:
                errors.append(
                    "interaction_gate.early_invitation.timestamp_seconds must be "
                    "before 60 percent of runtime."
                )
        elif name == "single_primary_action":
            if not nonempty_string(check.get("primary_action")):
                errors.append(
                    "interaction_gate.single_primary_action.primary_action must be non-empty."
                )
            secondary = check.get("secondary_actions")
            if not isinstance(secondary, list):
                errors.append(
                    "interaction_gate.single_primary_action.secondary_actions must be a list."
                )
            elif secondary:
                errors.append(
                    "interaction_gate.single_primary_action.secondary_actions must be empty."
                )
        elif name == "exact_response_format":
            if not nonempty_string(check.get("response_format")):
                errors.append(
                    "interaction_gate.exact_response_format.response_format must be non-empty."
                )
        elif name == "specific_reward":
            if not nonempty_string(check.get("reward")):
                errors.append("interaction_gate.specific_reward.reward must be non-empty.")
        elif name == "contract_consistency":
            keyword = check.get("keyword")
            reward = check.get("reward")
            if not nonempty_string(keyword):
                errors.append("interaction_gate.contract_consistency.keyword must be non-empty.")
            if not nonempty_string(reward):
                errors.append("interaction_gate.contract_consistency.reward must be non-empty.")

            surfaces = check.get("surfaces")
            if not isinstance(surfaces, dict):
                errors.append("interaction_gate.contract_consistency.surfaces must be an object.")
                continue
            for surface in CONSISTENCY_SURFACES:
                text = surfaces.get(surface)
                if not nonempty_string(text):
                    errors.append(
                        "interaction_gate.contract_consistency.surfaces."
                        f"{surface} must be non-empty."
                    )
                    continue
                if nonempty_string(keyword) and str(keyword) not in str(text):
                    errors.append(
                        "interaction_gate.contract_consistency.surfaces."
                        f"{surface} must include keyword {keyword!r}."
                    )
                if nonempty_string(reward) and str(reward) not in str(text):
                    errors.append(
                        "interaction_gate.contract_consistency.surfaces."
                        f"{surface} must include reward {reward!r}."
                    )


def validate_experience_interaction(data: object) -> list[str]:
    if not isinstance(data, dict):
        return ["QA root must be a JSON object."]

    errors: list[str] = []
    project = data.get("project")
    if not nonempty_string(project):
        errors.append("project must be a non-empty string.")

    runtime = data.get("runtime_seconds")
    if not isinstance(runtime, (int, float)) or isinstance(runtime, bool) or runtime <= 0:
        errors.append("runtime_seconds must be a positive number.")
        runtime_value = 0.0
    else:
        runtime_value = float(runtime)

    validate_experience_gate(data, runtime_value, errors)
    validate_interaction_gate(data, runtime_value, errors)

    blockers = data.get("blocking_issues")
    if not isinstance(blockers, list) or any(
        not nonempty_string(item) for item in blockers
    ):
        errors.append("blocking_issues must be a list of non-empty strings.")
    elif blockers:
        errors.append("Blocking issues remain: " + "; ".join(str(item) for item in blockers))

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate experience and interaction QA for a HyperFrames video."
    )
    parser.add_argument("qa", type=Path, help="Path to experience-interaction-qa.json.")
    args = parser.parse_args()

    try:
        data = json.loads(args.qa.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: File not found: {args.qa}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON: {exc}", file=sys.stderr)
        return 2

    errors = validate_experience_interaction(data)
    if errors:
        print("EXPERIENCE INTERACTION QA FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "EXPERIENCE INTERACTION QA PASSED: "
        f"experience={len(EXPERIENCE_CHECKS)}/{len(EXPERIENCE_CHECKS)}, "
        f"interaction={len(INTERACTION_CHECKS)}/{len(INTERACTION_CHECKS)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
