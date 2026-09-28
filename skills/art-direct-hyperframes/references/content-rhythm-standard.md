# Content Rhythm Standard

Use this pre-voice gate for instructional tool updates, tutorials, hands-on reviews, workflow explainers, and tutorial lead magnets. It prevents feature lists, late CTAs, and informationally empty long scenes from reaching TTS. Select the format with [production-format.md](production-format.md) first; case analysis, showcases and stories do not need invented experience or interaction ranges to satisfy this tutorial profile.

## Required Timeline

Save `content-rhythm.json` beside the video brief with:

- `runtime_seconds`: planned or final narration duration;
- `experience_ranges`: felt change, task input, operation consequence, result, fit, or boundary;
- `interaction_ranges`: one range for each `opening`, `middle`, and `closing` phase;
- `scenes`: planned scene ranges and count of distinct reusable information units;
- `thresholds`: project overrides, otherwise use the defaults below.

Ranges must use seconds and satisfy `0 <= start < end <= runtime_seconds`. Overlapping ranges are merged before measuring; never add overlapping durations manually.

## Blocking Defaults

- Experience coverage: at least 40 percent.
- Interaction coverage: at least 20 percent.
- Experience plus interaction after merging overlap: at least 60 percent.
- Opening interaction begins within the first 15 percent.
- Middle interaction begins before 60 percent.
- Closing interaction resolves after 85 percent.
- Any unclassified continuous gap is no more than 15 percent.
- Every scene lasting at least 8 seconds contains at least 3 distinct information units.

An information unit must help the viewer understand, decide, reproduce, verify, or avoid something. Enlarged text, decorative labels, repeated paraphrases, and background imagery do not count.

## Visualize Review

When `$visualize` is available, show experience, interaction, and scene density as aligned lanes on one time axis. Make threshold failures and uncovered gaps visible. Do not turn the review into a dashboard with unrelated metrics.

The visualization supports judgment but does not pass the gate. The deterministic validator remains the source of truth:

```bash
python3 <skill-directory>/scripts/validate_content_rhythm.py content-rhythm.json
```

Run once with planned durations before TTS and again with final narration timestamps before rendering. If the final timing changes coverage, revise the script or scene plan rather than editing percentages by hand.
