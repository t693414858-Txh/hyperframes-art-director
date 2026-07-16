# HyperFrames Art Director

An independent Codex Skill that adds an art-direction, content-routing, and review layer to HyperFrames video production.

This project does not replace the official HyperFrames skills. It helps decide what a video should feel like, how it should be visually structured, what evidence it should show, and whether the rendered result is actually recognizable, coherent, and useful before HyperFrames handles HTML, GSAP, validation, preview, and rendering.

中文介绍见 [README.zh-CN.md](README.zh-CN.md).

## Problem

Technically valid HyperFrames videos can still fail in predictable ways:

- They look like generic templates.
- The visual style does not match the manuscript.
- Screenshots feel pasted onto a background.
- The video relies on presenter, title, or color instead of project-specific identity.
- The CTA appears only at the end and does not match the promised reward.
- Feature-update videos list capabilities without proving a viewer-facing experience change.

HyperFrames Art Director turns these subjective concerns into explicit direction contracts, review evidence, and deterministic validators.

## What It Does

The Skill guides five parts of video direction:

1. **Content diagnosis**
   Classifies the manuscript by intent, audience, emotional temperature, evidence needs, available material, and cultural sensitivity.

2. **Adaptive visual routing**
   Selects a visual route from content fit rather than topic keywords. A technology script can become a precise product demo, an evidence-led explainer, a documentary workflow, or a warm service story depending on the brief.

3. **Project fingerprinting**
   Defines what remains recognizable when names, logos, captions, presenter, and generic styling are ignored.

4. **Storyboard and rhythm planning**
   Converts the brief into hero frames, scene purposes, motion intent, transition logic, and content-density requirements.

5. **Evidence-backed review**
   Reviews rendered frames and draft playback against source evidence, identity strength, route-specific checks, experience value, CTA consistency, and score thresholds.

## Core Features

### Adaptive Style Router

Included route families:

- Precision Product
- Knowledge Explainer
- Editorial Documentary
- Evidence-Led Intelligence
- Scientific Clarity
- Civic Trust
- Human Warmth
- Craft and Heritage
- Kinetic Culture
- Brand Manifesto

Named references such as Apple or The New York Times are translated into transferable properties. The Skill does not copy living brand trade dress, proprietary type, mastheads, slogans, or interface identity unless the user supplies authorized assets.

### Project Fingerprint Gate

A visual route is not a project identity. Light minimalism, dark technology styling, cards, chapter bars, subtitles, and presenter placement are generic unless they express the specific subject.

Every full direction records:

- semantic transformation;
- real source-evidence anchor;
- recurring structural, material, motion, or typographic anchor;
- scene-by-scene recurrence;
- blind recognition test;
- template-swap test;
- core identity coverage for at least 60 percent of scenes.

### Content Rhythm Gate

`content-rhythm.json` checks whether a script is dense and useful before voice generation.

It validates:

- experience coverage;
- interaction coverage;
- combined unique coverage;
- opening, middle, and closing interaction timing;
- largest unclassified gap;
- information units in long scenes.

This prevents long visually polished scenes that do not teach, prove, decide, verify, or invite action.

### Experience And Interaction Gate

`experience-interaction-qa.json` checks that tutorials, workflow explainers, reviews, and lead-magnet videos prove a real viewer-facing experience change.

It validates:

- before-versus-after felt change;
- best-fit task with input, operation, and result;
- boundary or limitation;
- visible proof;
- early invitation before 60 percent of runtime;
- one primary CTA;
- exact response format;
- specific promised reward;
- CTA consistency across narration, captions, on-screen CTA, publishing description, and pinned comment.

### Render Review Gate

The review validator scores eight dimensions:

1. Content-to-style fit
2. Project recognizability
3. Narrative clarity
4. Composition and focus
5. Typography system
6. Image and material treatment
7. Motion and rhythm
8. Continuity and distinctiveness

A review passes only when:

- average score is at least 4.0;
- project recognizability is at least 4;
- no dimension is below 3;
- no blocking issue remains;
- identity and source-evidence coverage meet thresholds;
- every score below 4 has a concrete corrective action.

## Repository Layout

```text
hyperframes-art-director/
├── skills/art-direct-hyperframes/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/
│   └── scripts/
├── examples/
├── evals/cases/
├── tests/
├── scripts/validate_repo.py
└── .github/workflows/validate.yml
```

Important files:

- `skills/art-direct-hyperframes/SKILL.md` - the installable Codex Skill entrypoint.
- `references/content-style-router.md` - content-aware route selection.
- `references/project-fingerprint.md` - recognition and template-swap rules.
- `references/content-rhythm-standard.md` - pre-voice rhythm QA.
- `references/experience-interaction-standard.md` - viewer experience and CTA QA.
- `scripts/validate_direction.py` - validates `direction-brief.json`.
- `scripts/validate_asset_readiness.py` - validates asset feasibility and rights.
- `scripts/validate_content_rhythm.py` - validates content-density and interaction timing.
- `scripts/validate_experience_interaction.py` - validates experience proof and CTA consistency.
- `scripts/prepare_visual_review.py` - captures review frames and contact sheets from a rendered draft.
- `scripts/validate_review.py` - validates final aesthetic scorecards.

## Install

Copy the installable Skill folder into your Codex skills directory:

```bash
cp -R skills/art-direct-hyperframes "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Restart or refresh Codex if the Skill is not discovered immediately.

## Use

In Codex:

```text
Use $art-direct-hyperframes to define the visual direction, storyboard,
hero frames, rhythm, project fingerprint, and review gates for this script.
Then use $hyperframes to implement the composition and $hyperframes-cli to
validate, preview, and render it.
```

For an existing video:

```text
Use $art-direct-hyperframes to review this HyperFrames result. Diagnose why it
feels generic or incoherent, update DESIGN.md if needed, and produce concrete
corrections before another render.
```

## Workflow

### 1. Diagnose

Gather:

- script or brief;
- audience and platform;
- aspect ratio and runtime;
- assets, footage, UI, source documents, data, and fonts;
- brand constraints and avoidances;
- prior episode frames when working in a series.

### 2. Validate Assets

Create `asset-readiness.json`, then run:

```bash
python3 skills/art-direct-hyperframes/scripts/validate_asset_readiness.py \
  examples/asset-readiness.pass.json
```

### 3. Create Direction

Create `DESIGN.md` and `direction-brief.json`, then run:

```bash
python3 skills/art-direct-hyperframes/scripts/validate_direction.py \
  examples/direction-brief.pass.json
```

### 4. Check Pre-Voice Rhythm

For tutorials, reviews, workflow explainers, and lead-magnet videos:

```bash
python3 skills/art-direct-hyperframes/scripts/validate_content_rhythm.py \
  examples/content-rhythm.pass.json
```

### 5. Implement With HyperFrames

Use the official HyperFrames skills for:

- HTML composition;
- CSS layout;
- GSAP choreography;
- media timing;
- transitions;
- linting, inspect/check, preview, and rendering.

### 6. Capture Review Evidence

```bash
python3 skills/art-direct-hyperframes/scripts/prepare_visual_review.py \
  examples/review-capture-plan.pass.json --validate-only
```

For a real project, update the paths and remove `--validate-only`. The script writes:

- full-size frame captures;
- `contact-sheet.png`;
- `review-evidence.json`;
- identity review scaffold.

### 7. Validate Experience And Interaction

```bash
python3 skills/art-direct-hyperframes/scripts/validate_experience_interaction.py \
  examples/experience-interaction-qa.pass.json
```

### 8. Score The Render

```bash
python3 skills/art-direct-hyperframes/scripts/validate_review.py \
  examples/review-scorecard.pass.json
```

## Example: Operation-Led Meeting Notes Video

The included `meeting-action-redesign-blueprint.md` demonstrates an operation-led workflow explainer:

- a single desktop workbench persists across scenes;
- cursor movement is used only for meaningful operations;
- raw meeting lines transform into structured fields;
- missing owner, deadline, and acceptance criteria become visible gaps;
- follow-up replies repair the gaps;
- the final action contract is exported with a consistent CTA.

This pattern is useful when screenshots feel pasted onto the canvas. It turns the visual system into a continuous operation rather than a slideshow of static layouts.

## Validate The Repository

```bash
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests -v
python3 skills/art-direct-hyperframes/scripts/validate_asset_readiness.py \
  examples/asset-readiness.pass.json
python3 skills/art-direct-hyperframes/scripts/validate_direction.py \
  examples/direction-brief.pass.json
python3 skills/art-direct-hyperframes/scripts/validate_content_rhythm.py \
  examples/content-rhythm.pass.json
python3 skills/art-direct-hyperframes/scripts/validate_experience_interaction.py \
  examples/experience-interaction-qa.pass.json
python3 skills/art-direct-hyperframes/scripts/validate_review.py \
  examples/review-scorecard.pass.json
python3 skills/art-direct-hyperframes/scripts/prepare_visual_review.py \
  examples/review-capture-plan.pass.json --validate-only
```

The GitHub Actions workflow runs these checks on push and pull request.

## What This Skill Does Not Do

- It does not replace HyperFrames.
- It does not render videos by itself.
- It does not license third-party references, fonts, images, UI, or footage.
- It does not treat aesthetic approval as equivalent to lint or layout success.
- It does not copy living brand identity from named references.

## Compatibility

The validators use only the Python standard library. Automated visual review capture requires `ffmpeg` and `ffprobe` on `PATH`.

When this Skill conflicts with official HyperFrames implementation rules, the installed `$hyperframes` and `$hyperframes-cli` rules take precedence.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

New aesthetic rules should include:

- visible symptom;
- viewer impact;
- correction;
- at least one evaluation case;
- validator coverage when the rule is deterministic.

## License

MIT. See [LICENSE](LICENSE).
