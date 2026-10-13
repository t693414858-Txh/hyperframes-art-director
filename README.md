# HyperFrames Art Director

A Codex Skill for directing and revising HyperFrames videos. It chooses visual material, plans editorial rhythm and reviews the actual export. Installed HyperFrames skills handle implementation and rendering.

[中文说明](README.zh-CN.md)

## What changed in 0.11.0

Production feedback showed that repeated rules and mandatory paperwork could obscure the editing problem. The entrypoint now uses five steps, with compact review by default and detailed contracts when a project needs them.

| Keep | Reduce or scope |
| --- | --- |
| Content-aware style and format selection | Automatic prestige-brand styling |
| Source evidence and topic-specific identity | Identity percentages required for every video |
| Relevant footage, real actions and deliberate rhythm | Forced state changes and uniformly fast cuts |
| Approved voice, final timing and export checks | Regenerating voice for a visual-only revision |
| Timestamped defects and current review evidence | Every edit producing a full set of JSON contracts |
| Project-specific caption and ending preferences | One account's settings imposed on all installations |

A new or repeatedly rejected direction is checked with a representative sample before full production. Timing profiles can allow justified reading holds while keeping operation and evidence requirements.

## Workflow

1. Lock the viewer promise, exact version, approved choices and requested changes.
2. Choose the production format and visual direction. Inspect supplied references.
3. Inspect representative artwork or a moving sample when the direction or action is uncertain.
4. Plan shots, implement, and repair the layer responsible for each defect.
5. Review the exact export and document remaining issues.

| Format | Main material | Review focus |
| --- | --- | --- |
| Operation tutorial | Recorded input, action, result and verification | Causality, readability and truthful demonstration |
| Case analysis | Relevant people, work stages and environments, with source inserts | Claim attribution, material variety and editorial rhythm |
| Artwork/product showcase | Approved work, details and comparisons | Integrity, proportions and inspectable results |
| Story/concept film | Actions, reactions and consequences | Whether the promised action actually unfolds |

Footage variety is assessed by source intervals, actions, environments, work stages and shot function. Different crops of one interval do not count as new footage. An intentional callback is allowed when its purpose is recorded.

## Review depth

**Compact review is the default.** Use the existing design document, storyboard and a short defect record: timestamp, observed problem, cause, edit and verification evidence. Check the subject, visual readability, playback, audio and export identity.

**Detailed review is available** for formal comparisons, repeated unresolved failures, complex compositions and existing automated pipelines. Read [review-workflow.md](skills/art-direct-hyperframes/references/review-workflow.md) to select only the contracts that apply.

| Contract | Tool |
| --- | --- |
| Asset feasibility and rights | `validate_asset_readiness.py` |
| Structured direction and scene coverage | `validate_direction.py` |
| Adopted tutorial timings | `validate_shortform_retention.py` |
| Adopted instructional coverage | `validate_content_rhythm.py` |
| Instructional experience and CTA consistency | `validate_experience_interaction.py` |
| Repeatable frames and contact sheet | `prepare_visual_review.py` |
| Detailed aesthetic scorecard | `validate_review.py` |

The existing detailed identity ratios and score thresholds remain supported. They are review-profile settings, not universal measures of aesthetic quality. Technical success does not establish audience engagement or overrule a visible defect.

## Tutorial timing configuration

Existing plans without overrides keep the previous defaults: result preview by 0.8s, operation by 2.5s, proof by 5s, verification by 8s, early gaps up to 2.5s, and 35/50s runtime bands.

For a new project using this profile, record why those timings fit or supply `thresholds` and `threshold_rationale` before production. For example, add these fields to an otherwise complete plan:

```json
{
  "thresholds": {"meaningful_state_change_gap_seconds_max": 4.5},
  "threshold_rationale": "Hold the rename preview so viewers can compare the filenames."
}
```

The validator reports effective settings and rejects invalid limits. Overrides cannot remove proof or operation requirements. Do not change thresholds solely to disguise a failed export. See [the timing contract](skills/art-direct-hyperframes/references/shortform-retention-standard.md).

## Install and use

From this repository:

```bash
cp -R skills/art-direct-hyperframes "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Refresh or restart Codex if discovery does not update. Invoke it for direction or revision:

```text
Use $art-direct-hyperframes to revise this video. Preserve the approved voice
and visual direction. Diagnose repetition and pacing, fix their causes, and
review the actual export with the applicable checks.
```

For a new video, supply the script or brief, audience, format, source material and known preferences. The Skill records reasonable assumptions and asks only for a missing decision that changes the direction.

## Resources

- [Production formats](skills/art-direct-hyperframes/references/production-format.md)
- [Content-to-style router](skills/art-direct-hyperframes/references/content-style-router.md)
- [Footage selection and rhythm](skills/art-direct-hyperframes/references/footage-editing.md)
- [Final audio and export review](skills/art-direct-hyperframes/references/final-delivery-review.md)
- [Optional account profile](examples/account-style-profile.md)
- [Evaluation cases](evals/README.md)
- [Changelog](CHANGELOG.md)

Project-specific engine settings, platform workflows and publication authorization stay with the project. This Skill does not grant publication permission or create a recurring schedule.

## Repository checks

```bash
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests -v
python3 skills/art-direct-hyperframes/scripts/validate_shortform_retention.py \
  examples/shortform-retention.pass.json --json
```

GitHub Actions also runs the existing passing contract examples. Validators use the Python standard library; automated frame capture requires FFmpeg and FFprobe. Tests check contracts and behavior, not artistic quality. New evaluation prompts require actual agent runs before they can be described as independently tested.

MIT license. Third-party assets and supplied references retain their own terms.
