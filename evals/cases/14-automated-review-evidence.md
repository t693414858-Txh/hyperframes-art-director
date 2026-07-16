# Automated Review Evidence

A 28-second HyperFrames draft has four scenes and an approved `DESIGN.md`. The reviewer must inspect the arrival, development, climax, and resolve without manually taking arbitrary screenshots.

Use the art-direction Skill to prepare the review evidence and score the draft.

## Evaluation Focus

- A valid `review-capture-plan.json` records the source video, design path, output directory, and ordered scene timestamps
- Timestamps represent settled hero states rather than transition midpoints
- Full-size frames and a contact sheet are generated from the same plan
- `review-evidence.json` maps every frame to scene id, role, label, and timestamp
- The scorecard uses the generated evidence paths
- Motion and rhythm are still reviewed from playback, not inferred from the contact sheet
