# Review Capture Plan

Use `review-capture-plan.json` to turn a rendered draft into repeatable visual evidence. The bundled script uses FFmpeg and FFprobe to:

- Extract one full-resolution hero frame per planned scene
- Preserve narrative order and timestamps
- Generate a thumbnail contact sheet
- Write `review-evidence.json` with paths ready for `review-scorecard.json`

## Required Structure

```json
{
  "project": "example-video",
  "source_video": "render/final-draft.mp4",
  "design_md": "DESIGN.md",
  "output_directory": "review",
  "contact_sheet": {
    "columns": 3,
    "thumbnail_width": 420,
    "padding": 16,
    "margin": 24,
    "background": "#F5F5F3"
  },
  "scenes": [
    {
      "id": "scene-01",
      "label": "Outcome first",
      "role": "arrival",
      "timestamp_seconds": 1.5
    },
    {
      "id": "scene-02",
      "label": "Workflow evidence",
      "role": "development",
      "timestamp_seconds": 7.2
    }
  ]
}
```

Supported roles are `arrival`, `development`, `contrast`, `climax`, `resolve`, and `supporting`.

## Run

Validate the plan:

```bash
python3 <skill-directory>/scripts/prepare_visual_review.py \
  review-capture-plan.json --validate-only
```

Generate evidence:

```bash
python3 <skill-directory>/scripts/prepare_visual_review.py \
  review-capture-plan.json
```

The output directory contains:

```text
review/
├── contact-sheet.png
├── frames/
│   ├── 001-scene-01.png
│   └── 002-scene-02.png
└── review-evidence.json
```

Use `review-evidence.json.scorecard_evidence` as the `evidence_reviewed` object in the aesthetic scorecard.

The file also contains `identity_review_scaffold`, which preserves scene order, labels, roles, and timestamps. Complete its empty identity-strength, source-evidence, and template-swap fields before copying it into `review-scorecard.json`.

## Timestamp Rules

- Choose a stable hero moment after required entrances have settled.
- Avoid transition midpoints unless the transition itself is under review.
- Keep timestamps strictly increasing.
- Include one frame per scene; add a second timestamp only by modeling it as a separate review beat.
- Place the climax timestamp at its strongest readable state, not its busiest transient frame.

The script validates that every timestamp fits inside the rendered video. It does not decide whether the chosen moment is aesthetically representative; that remains an art-direction judgment.
