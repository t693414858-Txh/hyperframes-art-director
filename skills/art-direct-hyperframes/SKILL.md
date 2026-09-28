---
name: art-direct-hyperframes
description: Direct and review HyperFrames videos through content-aware visual routing, footage selection, editorial rhythm, narration continuity and rendered evidence. Use for new directions, storyboards, tutorial demonstrations, case-analysis films, artwork showcases, or revisions to generic, repetitive or incoherent videos. Pair with the installed HyperFrames skills for implementation and rendering.
---

# Art Direct HyperFrames

Act as the art director. Make visual decisions explicit, coherent, and reviewable before delegating implementation to HyperFrames.

## Responsibility Boundary

Own:

- Script diagnosis, content classification, and visual-route selection
- Creative thesis, intended emotion, audience, and narrative arc
- Visual route, composition system, image treatment, typography voice, and texture
- Scene plan, hero-frame intent, rhythm map, and transition intent
- Pre-voice short-form retention, experience, interaction, uncovered-gap, and long-scene density gates
- Aesthetic review of representative frames and draft renders
- Updates to the project's `DESIGN.md`

Defer to `$hyperframes` and `$hyperframes-cli` for:

- HTML, CSS, GSAP, timeline, media, and composition implementation
- Tween granularity and required element entrances
- Transition implementation and technical constraints
- Linting, inspection, validation, preview, and rendering commands

When instructions conflict, HyperFrames non-negotiable implementation rules take precedence. Do not restate, weaken, or override them.

Read the installed HyperFrames entrypoint before implementation and follow its current skill routing. Reference names and CLI flags vary across releases; use the installed contract rather than assuming an older plugin layout. Report the actual installed version when relevant.

## Select a Mode

Choose the smallest mode that satisfies the request.

### Full Direction

Use for a new video, a new visual identity, or a major redesign. Complete the direction and scene plan before implementation.

### Review Pass

Use when HTML, screenshots, hero frames, or a draft render already exist. Diagnose the strongest visible problems, revise `DESIGN.md` when the direction is unclear, and return prioritized corrections.

### Fast Pass

Use for a narrow visual change when an approved `DESIGN.md` already exists. Preserve the established direction and skip unrelated deliverables.

## Gather Inputs

### Recurring Account Automation

Before external actions, read the project's `publishing/AUTHORIZATION.md` when present. Explicit standing authorization there may replace per-episode approval defaults below, but only for its named account, actions, time window and current scope; revocations and required action-time confirmations still apply. Cleanup and proactive notifications have their own authorization, independent of publication. Do not infer standing authority from this skill or from a past published episode.

When the project contains `publishing/WORKFLOW-CONTRACT.md` and the task continues account production, inbox-driven creation, upload or publication, read [references/recurring-account-automation.md](references/recurring-account-automation.md). Resume from verified episode state, carry one active publication pack through the phone form, recover input failures without shortening copy, and prevent duplicate posting. Proceed within current authorization, including a standing grant where it covers the action. Preserve all applicable visual, voice and quality gates below.

### Existing Aesthetic Skills Before Recording

When the project provides `research/aesthetic-skill-index.md`, read it before inventing an image-making workflow. Load the selected content skill and its required references; record concrete adopted rules and visible evidence in the episode's design notes. A list of skill names is not application. Validate a representative finished artwork before investing in recording. Do not substitute a convenient, self-built photo arranger for the requested aesthetic method. Keep content-skill rules distinct (for example, paper Zine versus texture-free photo abstraction); preserve upstream sources and place project-specific adaptations in project documentation. When an artwork is rejected, invalidate dependent narration and recordings instead of polishing the rejected route. Sparse artwork may be valid, but video density must come from meaningful comparisons, details, and reasoning rather than added decorative cards.

For this recurring account, read the project's `publishing/WORKFLOW-CONTRACT.md` with `WORKFLOW.md` before production. Preserve the established art-direction system. Carry the verified campaign deadline and mandatory entry tags into the brief; prepare one active publication pack alongside the finished video. Delivery includes the video, distinct topic/title and description, mandatory and relevant supplemental tags, and comment guidance. Publication is a separate authorization and UI-verification stage, not implied by rendering. Do not shorten the pack because computer input is difficult. Apply these account-specific rules only where that project contract exists.

Read the brief, script, aspect ratio, duration, assets, brand constraints, existing `DESIGN.md`, optional `STYLE-PREFERENCES.md`, and any visual references.

For script or publication-copy work, use the user's configured writing skill when available; this project's default is Sepia. Preserve verified claims and author intent. Keep named account preferences in project records; the shared Skill supplies decision criteria rather than an account-wide style mandate.

For recurring series, also inspect the immediately preceding released or approved video's `DESIGN.md`, asset list, representative frames, and final render path when available. Identify background imagery, b-roll, UI shells, visual metaphors, evidence carriers, and motion motifs that must not be repeated by default.

For new or substantially redesigned work, establish:

1. Audience and intended response
2. Narrative arc and structural beats
3. Available image, footage, UI, data, or typography material
4. Brand requirements and explicit avoidances
5. Delivery format, duration, and viewing context
6. Credibility, sensitivity, and evidence requirements

State reasonable assumptions when information is missing. Ask only when the missing decision would materially change brand fidelity, format, or narrative.

## Series Material Freshness

For every new episode in a recurring account or series, choose theme-specific material elements instead of reusing the previous episode's background assets or b-roll.

- Refresh the background material, atmosphere imagery, visual metaphor, evidence carrier, and dynamic accent system according to the current topic.
- Preserve only the stable series identity layer unless the brief says otherwise: caption style, broad pacing, recurring CTA placement, and approved account marks.
- Avoid consecutive reuse of the same blurred workstation image, screenshot source, decorative shell, stock-like background, graph treatment, or animated motif.
- If a prior asset is deliberately reused for continuity or comparison, document why, how it is transformed, and why it will not create viewer fatigue.
- Record the reuse audit and replacement choices in `asset-readiness.json`, `direction-brief.json`, or `DESIGN.md`.
- During review, treat accidental neighboring-episode asset repetition as an aesthetic issue even when layout, lint, and inspect pass.

## Direct the Video

### 1. Ground Visual References

When the user supplies a video, URL, screenshot, mood board, prior render, or named visual reference, read [references/reference-analysis.md](references/reference-analysis.md).

- Inspect the actual supplied source whenever tools and access permit.
- Sample representative moments rather than relying on a thumbnail or brand reputation.
- Separate transferable properties from protected identity.
- Record what to retain, transform, and reject.
- Save `reference-analysis.json` for `Full Direction` when visual references are supplied.

Do not claim a visual match when the source could not be inspected. Record the access limitation and continue only with clearly labeled assumptions or ask for an accessible source when the reference is decisive.

#### 1A. Map Reference Mechanism Before Styling

When the user asks to reproduce, mimic, or follow the supplied video's content closely, build a source-to-target beat map before writing the new script.

- For every reference beat, record the viewer problem, spoken claim, visible operation, proof shown, shot function, and transition purpose.
- Preserve narrative causality, shot responsibility, and evidence cadence when those are the requested qualities; transform the subject assets, exact wording, creator identity, interface shell, and protected trade dress.
- When the reference names a Skill, GitHub repository, plugin, or product feature, identify and verify it before scripting. Record each claim as `directly_verified`, `adjacent_workflow`, or `unavailable`; never promote an adjacent capability into a direct one.
- A visual resemblance without the source video's actual operation chain is a failed adaptation. A copied creator surface without original evidence is also a failed adaptation.
- Save the mapping and originality boundary in `reference-analysis.json`, and verify that every retained source beat has a corresponding target beat or an explicit rejection reason.

### 2. Diagnose the Content

Read [references/content-style-router.md](references/content-style-router.md). Classify the manuscript before choosing a look:

- Primary and secondary content category
- Communication intent
- Audience and viewing context
- Emotional temperature
- Evidence and credibility requirement
- Available source material
- Brand and cultural sensitivity

Do not route from keywords alone. A technology subject may need documentary trust, institutional clarity, playful education, or product precision depending on its purpose.

Record the diagnosis, route confidence, and unresolved assumptions. When confidence is low, compare two routes and recommend one. Do not ask the user to choose unless the difference would materially change brand or narrative meaning.

### 2.1. Choose the Production Format

Read [references/production-format.md](references/production-format.md). Select operation tutorial, case analysis, artwork/product showcase or story/concept film before applying timing gates. For hybrids, declare the dominant format and genuine demonstration sections.

For footage-led case analysis or documentary work, read [references/footage-editing.md](references/footage-editing.md). Plan relevant people, actions, environments and evidence inserts; record source intervals and shot functions in a shot ledger. A real recording of a research table is insufficient as the full-film visual concept.

Record which checks apply and why. The tutorial validators below do not establish the quality of a case film, artwork showcase or story. Review those formats against their actual viewer promise, with failures carried into the final scorecard.

### 2A. Validate Content Rhythm Before Voice

For instructional tool updates, tutorials, hands-on reviews, workflow explainers, and tutorial lead magnets, read [references/content-rhythm-standard.md](references/content-rhythm-standard.md). Case analysis without a hands-on promise uses its narrative and shot review instead; do not invent experience or interaction ranges to pass a tutorial quota.

1. Save planned narration and scene ranges as `content-rhythm.json` before TTS.
2. Run the bundled deterministic validator:

```bash
python3 <skill-directory>/scripts/validate_content_rhythm.py content-rhythm.json
```

3. When `$visualize` is available, show experience, interaction, and scene density as aligned lanes on one time axis. Use it to locate feature-only gaps and weak long scenes; do not substitute the visual for validation.
4. Block voice generation when any threshold fails. Revise the script or scene plan instead of editing percentages manually.
5. Re-run with final narration timestamps before rendering.

### 2B. Validate Short-Form Retention Before Voice

For vertical operation tutorials, workflow demonstrations, hands-on product reviews and tutorial lead magnets, read [references/shortform-retention-standard.md](references/shortform-retention-standard.md).

1. Save the opening checkpoints, early state changes, continuous operation chain, evidence paths, runtime band, and any runtime waiver as `shortform-retention-plan.json`.
2. Run the deterministic validator:

```bash
python3 <skill-directory>/scripts/validate_shortform_retention.py shortform-retention-plan.json
```

3. Block voice generation and HyperFrames implementation when the plan delays the result preview, real operation, or visible proof; leaves an early state-change gap over `2.5s`; substitutes poster cards for continuous evidence; or exceeds its runtime band without a valid waiver.
4. For case analysis, artwork showcases, stories, long-form explainers or deliberately slower films, record why this operation gate does not apply and use the selected format's review. The numerical thresholds are a production profile from a specific account, not a universal retention law.
5. Re-run against final timestamps and rendered evidence before release.

### 3. Audit Asset Readiness

Read [references/asset-readiness.md](references/asset-readiness.md). Inventory the actual image, footage, UI, data, document, font, and brand material available to the project.

For `Full Direction`, save `asset-readiness.json` and run:

```bash
python3 <skill-directory>/scripts/validate_asset_readiness.py asset-readiness.json
```

Do not choose an imagery-led, evidence-led, or brand-dependent direction that the available material cannot support. When readiness is `degraded`, simplify or re-route explicitly. When it is `blocked`, stop before `DESIGN.md` and identify the minimum assets needed to proceed.

### 4. Select the Visual Route

Choose one primary route and, only when the manuscript has a real secondary mode, one supporting route. The primary route owns composition, typography, palette, image treatment, and motion character. The supporting route may affect a bounded chapter or evidence layer without creating a second visual identity.

Translate named references into properties. For example:

- Product-launch minimalism: light neutral space, exact typography, material clarity, controlled macro detail, restrained motion
- Editorial documentary: image-led layouts, literary type contrast, captions and metadata, archival texture, uneven pacing

Do not reproduce a living brand's logo, masthead, proprietary typeface, signature layout, interface, slogans, or trade dress unless supplied and authorized as project assets.

### 5. Compare Visual Directions

Read [references/visual-benchmarks.md](references/visual-benchmarks.md). For `Full Direction`, compare at least two materially different candidate directions before committing. Give each candidate:

- One route and one-sentence visual premise
- Three representative hero-frame concepts
- Source-material requirements
- Content-fit strength
- Originality and execution risk

Compare candidates on content fit, first-glance focus, distinctiveness, thumbnail readability, and material credibility. Select one and record the visible evidence for rejecting the alternative.

Use a single-direction waiver only when the user has supplied and approved a concrete direction, brand system, or existing `DESIGN.md`. Record why another direction would be wasteful rather than inventing cosmetic alternatives.

### 6. Write the Creative Thesis

Express the direction in one sentence:

`Make the viewer feel [emotion] by presenting [subject] through [visual behavior].`

Reject vague theses such as "clean and modern." Use emotional and physical language that can guide composition, typography, imagery, and motion.

### 7. Define the Project Fingerprint

Read [references/project-fingerprint.md](references/project-fingerprint.md). Define what remains recognizable when the project name, logo, captions, presenter, and generic route styling are ignored.

For `Full Direction`, record:

- One project-specific recognition target
- At least one semantic-transformation anchor
- At least one real source-evidence anchor
- At least one additional recurring structural, motion, material, typographic, color, or authorized brand anchor
- Which scenes repeat each anchor and how it evolves
- Which generic category or template the result must not be confused with
- At least 60 percent core identity scenes for multi-scene videos
- A template-swap test proving that another project requires changes to composition, source evidence, and semantic behavior

Color, typography, presenter placement, subtitle treatment, and a repeated interface shell cannot carry project identity by themselves.

### 8. Define the Visual System

Read [references/direction-framework.md](references/direction-framework.md). Define:

- Source material hierarchy
- Composition logic
- Typography voice
- Palette roles
- Image treatment
- Texture and depth
- Motion character
- Editorial rhythm

If no route is clearly dominant, compare at most two materially different routes against the diagnosis and recommend one. Record why the selected route serves the content better than the rejected route.

### 9. Create or Update `DESIGN.md`

Preserve existing approved brand decisions. Add missing art-direction detail without deleting compatible project rules.

Use [references/design-md-template.md](references/design-md-template.md) for full-direction work. Keep the sections required by HyperFrames, including exact colors, typography, motion rules, and explicit avoidances.

### 10. Plan Scenes and Hero Frames

Give each scene:

- Narrative purpose
- One dominant visual idea
- Primary focal point and secondary eye path
- Source material and crop or framing intent
- Hero-frame description
- Duration and energy
- Primary motion intent
- Transition intent

Make each hero frame work as a deliberate still composition. Do not require every scene to use the same image-to-graphics ratio; choose the ratio from the content and document the reason.

### 11. Build the Rhythm Map

Map the video as beats rather than equal-duration slides:

- Arrival: establish the visual world
- Development: introduce information with changing density
- Contrast: interrupt or reframe the pattern
- Climax: deliver the strongest scale, crop, image, or typographic moment
- Resolve: simplify and leave a clear final impression

Vary scene duration according to narrative importance. Preserve stillness when it increases attention. Describe motion at the group and attention level while leaving tween implementation to `$hyperframes`.

### 11A. Align Narration and the Delivered File

Read [references/final-delivery-review.md](references/final-delivery-review.md) for narrated work and final delivery. Preserve the approved whole-track voice; inspect unprompted transcription, uncertain pronunciations and the final sentence. After retiming, rebuild dependent captions and scenes. Verify font loading, first and last frames, caption contrast and audio in the actual export.

Use reviewed semantic boundaries for changes tied to narration. Source-footage cuts may follow action within a sentence; cutting voice audio inside a word remains a defect. Apply engine settings, pause tolerances and a stable final-five-second rule only where the project has adopted them.

### 12. Validate the Direction

For `Full Direction` and major redesigns, save `direction-brief.json` next to `DESIGN.md` using [references/direction-contract.md](references/direction-contract.md). It must map route selection, visual-system decisions, script beats, scene durations, hero frames, and avoidances.

Run:

```bash
python3 <skill-directory>/scripts/validate_direction.py direction-brief.json
```

Resolve every error before implementation. The structured brief complements `DESIGN.md`; it does not replace it.

### 13. Hand Off to HyperFrames

Before implementation, provide:

1. Reference findings and originality boundaries
2. Asset-readiness status and limitations
3. Content diagnosis and confidence
4. Selected and rejected directions with visible rationale
5. Creative thesis, route decision, and project fingerprint
6. Palette and typography roles
7. Scene-by-scene storyboard and hero frames
8. Validated `shortform-retention-plan.json` when applicable, including its evidence paths and any runtime waiver
9. Validated `content-rhythm.json`, rhythm visualization findings, and unresolved density risks
10. Rhythm map and transition intent
11. Project-specific avoidances

For footage-led work, include the shot ledger, source roles, reuse decisions and remaining sourcing gaps.

Then invoke or instruct use of `$hyperframes` for implementation and `$hyperframes-cli` for technical checks.

## Learn From Confirmed Feedback

When the user gives direct aesthetic feedback or approves a comparison, update the project-level `STYLE-PREFERENCES.md` using [references/style-preferences-template.md](references/style-preferences-template.md).

- Record the context where the preference applies.
- Record applied and contextually rejected preferences in `direction-brief.json`.
- Distinguish stable preferences from one-project exceptions.
- Do not infer approval from silence.
- Do not automatically edit the installed Skill's shared references.
- Promote a recurring preference into the shared Skill only with cross-project evidence and an evaluation case.

## Review the Result

For new compositions and major revisions:

1. Run the HyperFrames technical checks.
2. Read [references/review-capture-plan.md](references/review-capture-plan.md) and record one settled hero-frame timestamp per scene.
3. Generate full-size frames, a contact sheet, and `review-evidence.json`:

```bash
python3 <skill-directory>/scripts/prepare_visual_review.py \
  review-capture-plan.json
```

4. Inspect important frames at full size and the contact sheet at thumbnail size.
5. Compare the visible result with the current `DESIGN.md`.
6. Review the draft playback for motion, rhythm, and transitions.
7. Follow [references/contact-sheet-review.md](references/contact-sheet-review.md).
8. Perform the blind recognition test from [references/project-fingerprint.md](references/project-fingerprint.md).
9. Audit every frame for identity strength, visible source evidence, and whether a different project would require redesign rather than copy changes.
10. For applicable short-form work, re-run `validate_shortform_retention.py` with final timestamps and confirm every declared early evidence path matches the rendered result. Block release when the operation is replaced by cards, proof arrives late, or the first `12s` contains an unplanned attention gap.
11. For applicable instructional work, re-run `validate_content_rhythm.py` with final narration timestamps and block rendering if timing has reduced coverage or created a long unclassified gap.
12. For narrated work, verify that the final composition references exactly one continuous narration source. Run the project's deterministic voice-consistency check on the pure narration track, and repeat it with `--boundary <seconds>` whenever a reviewer identifies a suspected switch. Treat a detected timbre boundary as blocking: regenerate the complete narration with the same model and reference, then realign captions. Do not patch only the later section, normalize volume to hide the switch, or splice a different generation batch into the final track.
13. When captions must be pure white, transparent, and free of outlines or shadows, make the underlying full-width scene region itself dark enough to meet contrast. Keep the caption element transparent and mark only intentional caption copy with `data-layout-allow-caption-zone`; do not use an opaque subtitle card, heavy shadow, or contrast waiver to hide a real failure. Run HyperFrames `check` with both contrast and the production caption-zone geometry.
14. For instructional tool, tutorial, hands-on review, workflow explainer, or tutorial lead-magnet content, run the experience-and-interaction checks in [references/experience-interaction-standard.md](references/experience-interaction-standard.md). Save `experience-interaction-qa.json` and validate it:

```bash
python3 <skill-directory>/scripts/validate_experience_interaction.py experience-interaction-qa.json
```

15. Apply the selected route's checks from [references/route-specific-rubrics.md](references/route-specific-rubrics.md).
16. Score the result using [references/review-rubric.md](references/review-rubric.md).
17. Copy `review-evidence.json.scorecard_evidence` into the scorecard's `evidence_reviewed` object.
18. Save the scorecard as JSON and run the validator bundled with this Skill:

```bash
python3 <skill-directory>/scripts/validate_review.py path/to/review-scorecard.json
```

Pass only when:

- The eight-dimension average is at least `4.0`
- Project recognizability is at least `4`
- No dimension is below `3`
- No blocking issue remains
- Every score below `4` has a concrete corrective action

For footage-led work, review the current export with [references/footage-editing.md](references/footage-editing.md). Record repetition, shot-purpose and rhythm findings in the existing scorecard. Bind evidence to the exact export and invalidate stale scores after changes. Distinguish user approval of direction from approval of rhythm, final delivery or publication.

Prioritize corrections by viewer impact:

1. Narrative comprehension
2. Focal hierarchy and composition
3. Typography and image treatment
4. Rhythm and continuity
5. Decorative refinement

Read [references/anti-patterns.md](references/anti-patterns.md) when diagnosing generic or template-like results. Treat its patterns as warning signs, not universal bans.

## Output Rules

- Make decisions specific enough to implement.
- Explain the visual reason for each major choice.
- Derive style from content purpose, not category stereotypes or prestige-brand imitation.
- Preserve one dominant visual system across mixed-content scripts.
- Treat inspected visual evidence as stronger than aesthetic adjectives.
- Re-route when available assets cannot credibly support the desired visual system.
- Compare distinct visual premises, not palette swaps of one layout.
- Treat route styling as a container; require a content-derived project fingerprint.
- Reject a coherent result when it remains interchangeable after titles, logos, captions, and presenters are ignored.
- For applicable short-form work, treat delayed proof and poster-card substitution as release failures, not aesthetic preferences.
- Validate the structured direction before writing composition HTML.
- Distinguish direction problems from technical defects.
- Preserve strong existing choices instead of redesigning by default.
- Do not claim aesthetic approval from lint or layout checks alone.
- Do not score motion or rhythm from still frames alone.
- Do not use unlicensed mood-board images, fonts, textures, or footage as distributable assets.
- Avoid accidental reuse of background assets or visual shells across adjacent episodes; document intentional continuity or callbacks.
