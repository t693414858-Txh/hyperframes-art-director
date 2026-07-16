#!/usr/bin/env python3
"""Extract hero frames and build a contact sheet for visual review."""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROLES = ("arrival", "development", "contrast", "climax", "resolve", "supporting")
HEX_COLOR = re.compile(r"^#[0-9A-Fa-f]{6}$")


def nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_plan(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["Review-capture plan root must be a JSON object."]

    for field in ("project", "source_video", "design_md", "output_directory"):
        if not nonempty_string(data.get(field)):
            errors.append(f"{field} must be a non-empty string.")

    sheet = data.get("contact_sheet")
    if not isinstance(sheet, dict):
        errors.append("contact_sheet must be a JSON object.")
    else:
        integer_ranges = {
            "columns": (1, 6),
            "thumbnail_width": (160, 1200),
            "padding": (0, 100),
            "margin": (0, 200),
        }
        for field, (minimum, maximum) in integer_ranges.items():
            value = sheet.get(field)
            if (
                not isinstance(value, int)
                or isinstance(value, bool)
                or not minimum <= value <= maximum
            ):
                errors.append(
                    f"contact_sheet.{field} must be an integer from "
                    f"{minimum} to {maximum}."
                )
        background = sheet.get("background")
        if not isinstance(background, str) or not HEX_COLOR.fullmatch(background):
            errors.append(
                "contact_sheet.background must be a six-digit hex color."
            )

    scenes = data.get("scenes")
    if not isinstance(scenes, list) or len(scenes) < 2:
        errors.append("scenes must contain at least two scene timestamps.")
        return errors

    ids: set[str] = set()
    previous_timestamp = -1.0
    for index, scene in enumerate(scenes):
        path = f"scenes[{index}]"
        if not isinstance(scene, dict):
            errors.append(f"{path} must be a JSON object.")
            continue

        scene_id = scene.get("id")
        if not nonempty_string(scene_id):
            errors.append(f"{path}.id must be a non-empty string.")
        elif scene_id in ids:
            errors.append(f"{path}.id duplicates {scene_id}.")
        else:
            ids.add(scene_id)

        if not nonempty_string(scene.get("label")):
            errors.append(f"{path}.label must be a non-empty string.")
        if scene.get("role") not in ROLES:
            errors.append(f"{path}.role must be a supported narrative role.")

        timestamp = scene.get("timestamp_seconds")
        if (
            not isinstance(timestamp, (int, float))
            or isinstance(timestamp, bool)
            or timestamp < 0
        ):
            errors.append(
                f"{path}.timestamp_seconds must be a non-negative number."
            )
        else:
            timestamp_value = float(timestamp)
            if timestamp_value <= previous_timestamp:
                errors.append(
                    "Scene timestamps must be strictly increasing in review order."
                )
            previous_timestamp = timestamp_value

    return errors


def safe_slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-")
    return slug or "scene"


def resolve_from_plan(plan_path: Path, value: str) -> Path:
    path = Path(value).expanduser()
    if path.is_absolute():
        return path
    return (plan_path.parent / path).resolve()


def run_command(command: list[str]) -> None:
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(detail or "Command failed without output.")


def probe_video(ffprobe: str, video_path: Path) -> tuple[float, int, int]:
    command = [
        ffprobe,
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height:format=duration",
        "-of",
        "json",
        str(video_path),
    ]
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "ffprobe failed.")

    try:
        data = json.loads(completed.stdout)
        stream = data["streams"][0]
        duration = float(data["format"]["duration"])
        width = int(stream["width"])
        height = int(stream["height"])
    except (KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise RuntimeError("Could not read video duration and dimensions.") from exc

    if duration <= 0 or width <= 0 or height <= 0:
        raise RuntimeError("Video duration and dimensions must be positive.")
    return duration, width, height


def build_contact_sheet_filter(
    frame_count: int,
    columns: int,
    thumbnail_width: int,
    source_width: int,
    source_height: int,
    padding: int,
    margin: int,
    background: str,
) -> str:
    thumbnail_height = max(
        2,
        int(round(thumbnail_width * source_height / source_width / 2) * 2),
    )
    color = "0x" + background.lstrip("#")
    filters: list[str] = []
    labels: list[str] = []
    for index in range(frame_count):
        label = f"v{index}"
        labels.append(f"[{label}]")
        filters.append(
            f"[{index}:v]scale={thumbnail_width}:{thumbnail_height}:"
            "force_original_aspect_ratio=decrease,"
            f"pad={thumbnail_width}:{thumbnail_height}:"
            f"(ow-iw)/2:(oh-ih)/2:color={color}[{label}]"
        )

    layout: list[str] = []
    for index in range(frame_count):
        column = index % columns
        row = index // columns
        x = column * (thumbnail_width + padding)
        y = row * (thumbnail_height + padding)
        layout.append(f"{x}_{y}")

    rows = math.ceil(frame_count / columns)
    grid_width = columns * thumbnail_width + max(0, columns - 1) * padding
    grid_height = rows * thumbnail_height + max(0, rows - 1) * padding
    filters.append(
        "".join(labels)
        + f"xstack=inputs={frame_count}:layout={'|'.join(layout)}:"
        f"fill={color}[grid]"
    )
    filters.append(
        f"[grid]pad={grid_width + 2 * margin}:{grid_height + 2 * margin}:"
        f"{margin}:{margin}:color={color}[out]"
    )
    return ";".join(filters)


def extract_frames(
    ffmpeg: str,
    video_path: Path,
    scenes: list[dict[str, object]],
    frames_directory: Path,
) -> list[dict[str, object]]:
    frames_directory.mkdir(parents=True, exist_ok=True)
    frame_records: list[dict[str, object]] = []

    for index, scene in enumerate(scenes, start=1):
        scene_id = str(scene["id"])
        output_path = frames_directory / (
            f"{index:03d}-{safe_slug(scene_id)}.png"
        )
        command = [
            ffmpeg,
            "-y",
            "-ss",
            f"{float(scene['timestamp_seconds']):.3f}",
            "-i",
            str(video_path),
            "-frames:v",
            "1",
            "-vsync",
            "0",
            str(output_path),
        ]
        run_command(command)
        frame_records.append(
            {
                "id": scene_id,
                "label": scene["label"],
                "role": scene["role"],
                "timestamp_seconds": float(scene["timestamp_seconds"]),
                "path": str(output_path.resolve()),
            }
        )

    return frame_records


def create_contact_sheet(
    ffmpeg: str,
    video_path: Path,
    scenes: list[dict[str, object]],
    output_path: Path,
    filter_graph: str,
) -> None:
    command = [ffmpeg, "-y"]
    for scene in scenes:
        command.extend(
            [
                "-ss",
                f"{float(scene['timestamp_seconds']):.3f}",
                "-i",
                str(video_path),
            ]
        )
    command.extend(
        [
            "-filter_complex",
            filter_graph,
            "-map",
            "[out]",
            "-frames:v",
            "1",
            str(output_path),
        ]
    )
    run_command(command)


def build_identity_review_scaffold(
    frame_records: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "ignored_elements": [
            "project_name",
            "logo",
            "captions",
            "presenter",
        ],
        "result": "",
        "recognized_as": "",
        "confusable_with": [],
        "evidence": "",
        "scene_audit": [
            {
                "scene_id": record["id"],
                "label": record["label"],
                "role": record["role"],
                "timestamp_seconds": record["timestamp_seconds"],
                "identity_strength": "",
                "template_swap_result": "",
                "source_evidence_visible": None,
                "project_specific_evidence": "",
            }
            for record in frame_records
        ],
        "template_swap_test": {
            "alternate_project": "",
            "result": "",
            "required_redesigns": [],
            "evidence": "",
        },
    }


def prepare_review(plan_path: Path, data: dict[str, object]) -> Path:
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if not ffmpeg or not ffprobe:
        raise RuntimeError("ffmpeg and ffprobe must be available on PATH.")

    video_path = resolve_from_plan(plan_path, str(data["source_video"]))
    design_path = resolve_from_plan(plan_path, str(data["design_md"]))
    output_directory = resolve_from_plan(plan_path, str(data["output_directory"]))

    if not video_path.is_file():
        raise RuntimeError(f"Source video not found: {video_path}")
    if not design_path.is_file():
        raise RuntimeError(f"DESIGN.md not found: {design_path}")

    duration, source_width, source_height = probe_video(ffprobe, video_path)
    scenes = data["scenes"]
    assert isinstance(scenes, list)
    for scene in scenes:
        assert isinstance(scene, dict)
        timestamp = float(scene["timestamp_seconds"])
        if timestamp > duration:
            raise RuntimeError(
                f"Scene {scene['id']} timestamp {timestamp:.3f}s exceeds "
                f"video duration {duration:.3f}s."
            )

    output_directory.mkdir(parents=True, exist_ok=True)
    frames_directory = output_directory / "frames"
    frame_records = extract_frames(
        ffmpeg,
        video_path,
        scenes,
        frames_directory,
    )

    sheet = data["contact_sheet"]
    assert isinstance(sheet, dict)
    filter_graph = build_contact_sheet_filter(
        frame_count=len(scenes),
        columns=int(sheet["columns"]),
        thumbnail_width=int(sheet["thumbnail_width"]),
        source_width=source_width,
        source_height=source_height,
        padding=int(sheet["padding"]),
        margin=int(sheet["margin"]),
        background=str(sheet["background"]),
    )
    contact_sheet_path = output_directory / "contact-sheet.png"
    create_contact_sheet(
        ffmpeg,
        video_path,
        scenes,
        contact_sheet_path,
        filter_graph,
    )

    evidence = {
        "project": data["project"],
        "source_video": str(video_path.resolve()),
        "video_duration_seconds": duration,
        "video_dimensions": {
            "width": source_width,
            "height": source_height,
        },
        "frames": frame_records,
        "contact_sheet": str(contact_sheet_path.resolve()),
        "scorecard_evidence": {
            "design_md": str(design_path.resolve()),
            "contact_sheet": str(contact_sheet_path.resolve()),
            "full_size_frames": [record["path"] for record in frame_records],
            "draft_playback": str(video_path.resolve()),
        },
        "identity_review_scaffold": build_identity_review_scaffold(
            frame_records
        ),
    }
    evidence_path = output_directory / "review-evidence.json"
    evidence_path.write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return evidence_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract hero frames and build a visual-review contact sheet."
    )
    parser.add_argument(
        "review_capture_plan",
        type=Path,
        help="Path to review-capture-plan.json.",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate the plan without reading or rendering the video.",
    )
    args = parser.parse_args()

    try:
        data = json.loads(args.review_capture_plan.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(
            f"ERROR: File not found: {args.review_capture_plan}",
            file=sys.stderr,
        )
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON: {exc}", file=sys.stderr)
        return 2

    errors = validate_plan(data)
    if errors:
        print("REVIEW CAPTURE PLAN FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    if args.validate_only:
        print(
            f"REVIEW CAPTURE PLAN PASSED: scenes={len(data['scenes'])}"
        )
        return 0

    try:
        evidence_path = prepare_review(args.review_capture_plan.resolve(), data)
    except RuntimeError as exc:
        print(f"REVIEW CAPTURE FAILED: {exc}", file=sys.stderr)
        return 1

    print(f"VISUAL REVIEW EVIDENCE READY: {evidence_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
