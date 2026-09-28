# Short-Form Retention Standard

Use this standard for vertical operation tutorials, workflow demonstrations,
hands-on product reviews and tutorial lead magnets. Choose the format with
[production-format.md](production-format.md) first. Case analysis, artwork
showcases, stories and long-form films require their own review; illustrative
stock footage must not be entered as a real product operation to pass this gate.

These timings are an adopted tutorial production profile informed by one account's
diagnosis. They are editorial constraints, not empirically established universal
thresholds or a guarantee of improved performance.

The gate exists because distribution does not compensate for a weak opening. A
video can receive recommendation traffic and still fail when the audience does
not see a concrete result, real operation, or proof quickly enough.

## Release Contract

Before voice generation or composition implementation, create
`shortform-retention-plan.json` and validate it with:

```bash
python3 scripts/validate_shortform_retention.py shortform-retention-plan.json
```

Do not continue when the validator reports an error.

## Opening Checkpoints

For an applicable video:

- By `0.8s`: show the problem and a recognizable preview of the result.
- By `2.5s`: begin a real operation, not an explanation of what will happen.
- By `5.0s`: show the first visible proof that the operation changed something.
- By `8.0s`: show a before/after comparison, verification, or measurable outcome.
- During the first `12s`: create a meaningful state change at least every `2.5s`.

A meaningful state change alters the viewer's understanding of the result. Cursor
movement, decorative zooming, subtitle replacement, or presenter gestures alone
do not count.

## Demonstration Rules

- Use one continuous workspace or source transformation as the main evidence.
- Show `input -> operation -> visible_result -> verification`.
- Prefer direct cuts, reframing, and focus changes inside the same workspace.
- Do not replace the operation with a sequence of poster cards or pasted
  screenshots.
- A presenter may support the demonstration but must not cover the primary
  evidence.

## Runtime Bands

- `single_task`: no more than `35s`.
- `multi_step`: no more than `50s`.
- Longer videos require a runtime waiver with:
  - a concrete reason the proof cannot be shortened,
  - at least two chapters,
  - an explanation of why splitting the video would reduce usefulness.

The waiver is not permission to keep repetition, setup narration, or decorative
transitions.

## Evidence Requirements

Every early state change must include:

- a timestamp,
- a description of the visible change,
- a storyboard frame, screenshot, or review artifact path.

The evidence should make it possible to inspect the plan without relying on the
author's intent.

## Post-Publish Calibration

These are account-calibration targets, not promises that can be verified before
release:

Keep the measurement window, sample size, video length, traffic mix and platform
metric definition with each observation. Compare similar formats at comparable
ages, such as 24 and 72 hours. Low samples and missing metrics remain uncertain;
do not report a predicted score as measured retention or infer a causal lift from
one revised video.

| Metric | Initial target |
| --- | ---: |
| 2-second bounce rate | `< 40%` |
| 5-second completion rate | `> 32%` |
| Average play ratio for 35-50s videos | `> 25%` |
| Favorite rate | `> 0.8%` |
| Follow conversion | `> 0.15%` |

Review the stable post-publish sample and respond to misses:

- High 2-second bounce: replace the opening sentence and first frame.
- Acceptable 2-second bounce but weak 5-second completion: move operation and
  proof earlier.
- Weak average play ratio: remove repeated explanation or split the workflow.
- Strong watch depth but weak distribution: repackage the topic, cover, and first
  frame.
- Strong views but weak follows: tighten the connection between the topic and the
  account's promised value.

Treat these targets as a rolling baseline. Update them only from a comparable
sample of videos, never from one outlier.
