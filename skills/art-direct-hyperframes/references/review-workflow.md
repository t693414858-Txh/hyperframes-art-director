# Select the review depth

Use the smallest review that can verify the requested outcome. A new full direction
does not automatically require every JSON contract. Preserve an existing pipeline
when its consumers actually rely on those contracts.

## Compact review: default

Use existing `DESIGN.md`, storyboard and delivery notes. Record the intended result,
format, sources and approved choices once. Review the current export with a short
defect table: timestamp, observed problem, cause, edit and verification evidence.
Keep unresolved issues explicit. Do not fill absent checks with guessed passes.

For a narrow fix, recheck the changed region and its dependencies. The whole video
still needs valid current final-file evidence; unaffected evidence can be carried
forward only with a stated basis. Use this impact map:

| Change | Recheck |
| --- | --- |
| Crop, font, caption styling | Affected frames, phone-size reading, contrast and collisions |
| Shot source, order or duration | Source role, repeated intervals, adjacent cut continuity and playback |
| Voice wording or generation | Whole narration completeness and voice continuity; dependent timing |
| Audio retiming | Transcript, captions, scenes, lip-sync where present, and encoded ending |
| Topic, claimed result or central artwork | Script claims, visual direction, dependent recordings and applicable voice wording |

A cosmetic change does not require new voice generation or a new direction study.
An approved still does not waive a motion test when the request promises action.

## Detailed review: when selected

Use for formal comparisons, repeated unresolved failures, complex scene systems,
or a project that has adopted the structured pipeline. Choose relevant contracts:

| Contract | When it adds value | Reference / validator |
| --- | --- | --- |
| Asset readiness | Missing sources, uncertain permissions or unsupported claims | [Asset contract](asset-readiness.md) / `validate_asset_readiness.py` |
| Direction brief | Automated scene coverage or formal direction comparison | [Direction contract](direction-contract.md) / `validate_direction.py` |
| Tutorial timing | A declared operation-tutorial profile | [Tutorial profile](shortform-retention-standard.md) / `validate_shortform_retention.py` |
| Content rhythm | An adopted instructional coverage profile | [Coverage profile](content-rhythm-standard.md) / `validate_content_rhythm.py` |
| Experience and CTA | An instructional or lead-magnet brief with a real interaction promise | [Experience contract](experience-interaction-standard.md) / `validate_experience_interaction.py` |
| Capture plan | Repeatable frame capture across scene revisions | [Capture contract](review-capture-plan.md) / `prepare_visual_review.py` |
| Aesthetic scorecard | Comparative or formal scored review | [Review rubric](review-rubric.md) / `validate_review.py` |

Read each reference before creating its contract. Run a selected validator as
`python3 <skill-directory>/scripts/<validator>.py <project-json>`; resolve its errors
before claiming that contract passes. For frame capture, use the capture-plan
reference's generation command. Do not run a scorecard validator on compact notes.

The direction and scorecard contracts retain their established identity coverage
ratios, scene audits and comparison requirements for compatibility. These numbers
belong to that detailed profile. Do not impose them on every shot or invent assets
to satisfy a ratio. If the profile conflicts with the requested format, document
the mismatch and use an appropriate review instead of claiming a false pass.

## Numeric targets are adopted settings

In a tutorial plan, default timings remain available for existing projects.
For a new plan, state the chosen timing targets and why they suit reading time,
task complexity and narration. The short-form validator accepts `thresholds`
overrides with `threshold_rationale`; output reports the effective settings.
Keep genuine state changes and evidence even when using a slower profile.

Set the plan before production; update it transparently when the brief or inspected
sample changes. Do not relax a failing number after rendering solely to claim pass.
Likewise, do not fabricate timestamps to match a target. Timing validation checks
declared data; rendered evidence still needs inspection.

Publication metrics are subsequent observations. Record the measurement window,
sample size, length and traffic mix; compare similar work. Aesthetic scores,
timing checks and modeled predictions do not establish audience retention.

## Close one revision

Keep the active version unambiguous. Mark each requested defect resolved, unresolved
or superseded by an explicit new requirement, with evidence. A rule change should
reduce a demonstrated failure; record its scope and retire conflicting old wording.
Keep approval and authorizations tied to the aspect or action actually approved.
