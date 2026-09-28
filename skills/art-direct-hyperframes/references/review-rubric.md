# Aesthetic Review Rubric

Score each dimension from `1` to `5`. Cite visible evidence. Scores below `4` require a concrete corrective action.

## Required Evidence

Review:

- The current `DESIGN.md`
- One hero frame from every scene, assembled as a contact sheet
- Full-size frames for crop, typography, and readability inspection
- A draft playback or equivalent timing evidence for motion, rhythm, and transitions
- The validated `shortform-retention-plan.json` and its declared evidence for applicable short-form work

Do not infer motion quality from still frames. Record missing evidence as a blocking issue when it prevents a dimension from being assessed.

## Scoring Scale

- `5` Exceptional: specific, coherent, memorable, and fully supports the narrative
- `4` Strong: intentional and effective with only minor refinements
- `3` Acceptable: works, but contains generic, inconsistent, or underdeveloped choices
- `2` Weak: distracts from comprehension or visibly lacks direction
- `1` Failing: broken, contradictory, or unusable

## Dimensions

### Content-to-Style Fit

Check whether the route follows the manuscript's intent, audience, emotional temperature, evidence requirement, source material, and cultural context. Penalize category stereotypes, unsupported luxury cues, generic dark technology styling, and direct imitation of a prestige brand.

### Project Recognizability

Ignore the project name, logo, captions, presenter, call to action, and generic route styling. Check whether the remaining source evidence, semantic transformation, structural mechanism, and scene progression still identify this specific project rather than only its broad category.

A light canvas, navy typography, colored cards, editorial rules, presenter corner, subtitle bar, or repeated shell do not earn recognition credit by themselves. This dimension must score at least `4` to pass.

### Narrative Clarity

Check whether a first-time viewer can understand the progression, identify the main point, and recognize the climax and resolution.

### Composition and Focus

Check focal hierarchy, eye path, scale contrast, crop quality, edge tension, negative space, depth, and whether the frame reads at thumbnail size.

### Typography System

Check cultural fit, hierarchy, line breaks, measure, weight contrast, spacing, consistency, and whether typography behaves as part of the frame rather than web-page copy.

### Image and Material Treatment

Check source quality, crop intent, visual consistency, relationship to typography, color treatment, and whether texture or decoration has narrative purpose.

### Motion and Rhythm

Check pacing variation, hierarchy of movement, stillness, scene density, climax timing, and whether motion guides attention instead of competing for it. For applicable short-form work, verify the result preview by `0.8s`, real operation by `2.5s`, visible proof by `5s`, verification by `8s`, and meaningful state changes across the first `12s`.

### Continuity and Distinctiveness

Check fidelity to the creative thesis and `DESIGN.md`, whether scenes belong to one visual world, whether transitions support structural meaning, whether identity anchors remain stable while scale, crop, density, or depth evolve, and whether the result avoids both mechanical repetition and interchangeable template aesthetics.

## Blocking Issues

Apply format-specific items only after choosing the production format. Tutorial
operation thresholds do not apply to illustrative footage in case analysis.
Use [production-format.md](production-format.md) for routing.

Treat any of these as blocking:

- A rejected or superseded export remains the active delivery candidate
- Review evidence or scores describe an older cut without an explicit carry-over basis
- A footage-led case film uses a research form as its entire visual argument
- Repeated source intervals have no editorial reason, or new crops are counted as new material
- Illustrative people, reconstructed interfaces or generated concepts are presented as actual customers, product tests or results
- A requested action is replaced by camera movement over a static illustration
- The encoded export drops narration, loads the wrong font, distorts an approved source or ends before its final caption

- The main message cannot be understood
- Essential text is unreadable
- A hero subject is unintentionally cropped or obscured
- Brand requirements are violated
- The selected route materially conflicts with the content's credibility or cultural requirements
- A recognizable third-party brand identity is copied without supplied authorization
- The blind recognition test fails after names, logos, captions, and presenter are ignored
- Project identity depends only on generic route styling or a repeated presenter
- The direction contradicts itself across scenes
- Unlicensed distributable assets are included
- A visible technical defect prevents meaningful aesthetic review
- Required frame or playback evidence is missing for a scored dimension
- Tool or tutorial content only lists features without a visible user-experience judgment
- Interaction guidance lacks an executable action, a specific viewer reward, or consistency across narration, captions, CTA, and publishing copy
- Applicable short-form work does not have a passing `shortform-retention-plan.json`
- Applicable short-form work shows the problem and recognizable result preview after `0.8s`
- Applicable short-form work begins its first real operation after `2.5s` or shows its first visible proof after `5s`
- Applicable short-form work contains a meaningful state-change gap longer than `2.5s` during the first `12s`
- An applicable software or workflow demonstration uses poster cards or pasted screenshots instead of a continuous operation as its primary evidence
- Applicable short-form work exceeds `35s` for a single task or `50s` for a multi-step workflow without a valid waiver

## JSON Format

```json
{
  "project": "example-video",
  "evidence_reviewed": {
    "design_md": "DESIGN.md",
    "contact_sheet": "review/contact-sheet.png",
    "full_size_frames": [
      "review/scene-01.png",
      "review/scene-03.png"
    ],
    "draft_playback": "review/draft.mp4"
  },
  "route_review": {
    "primary_route": "Knowledge Explainer",
    "checks": [
      {
        "criterion": "Each frame teaches one reproducible step or concept.",
        "status": "pass",
        "evidence": "Every scene contains one operation and one visible result.",
        "action": ""
      },
      {
        "criterion": "Interface evidence remains readable long enough to understand.",
        "status": "pass",
        "evidence": "The smallest inspected interface label remains readable at full size.",
        "action": ""
      },
      {
        "criterion": "Instruction outranks product mystique.",
        "status": "pass",
        "evidence": "All decorative effects are subordinate to the demonstrated workflow.",
        "action": ""
      }
    ]
  },
  "identity_review": {
    "ignored_elements": [
      "project_name",
      "logo",
      "captions",
      "presenter"
    ],
    "result": "pass",
    "recognized_as": "A Codex request progressing through real interface action, file change, and verification.",
    "confusable_with": [],
    "evidence": "The request-change-verification loop remains visible across the contact sheet.",
    "scene_audit": [
      {
        "scene_id": "scene-01",
        "identity_strength": "primary",
        "template_swap_result": "requires_redesign",
        "source_evidence_visible": true,
        "project_specific_evidence": "The real request and result remain connected."
      },
      {
        "scene_id": "scene-03",
        "identity_strength": "primary",
        "template_swap_result": "requires_redesign",
        "source_evidence_visible": true,
        "project_specific_evidence": "The real file change and verification state remain visible."
      }
    ],
    "template_swap_test": {
      "alternate_project": "Expense approval tutorial",
      "result": "requires_redesign",
      "required_redesigns": [
        "composition",
        "source_evidence",
        "semantic_transformation"
      ],
      "evidence": "Changing only copy cannot replace the interface evidence and verification behavior."
    }
  },
  "dimensions": {
    "content_style_fit": {
      "score": 4,
      "evidence": "The editorial-documentary route matches the cultural subject and available archival photography.",
      "action": ""
    },
    "project_recognizability": {
      "score": 4,
      "evidence": "The content-specific transformation and real source evidence recur across setup, development, and result.",
      "action": ""
    },
    "narrative_clarity": {
      "score": 4,
      "evidence": "The opening problem and final result are immediately legible.",
      "action": ""
    },
    "composition_and_focus": {
      "score": 3,
      "evidence": "Scenes 2 and 3 use the same centered stack and lack a secondary eye path.",
      "action": "Move the UI crop off-center and use the headline as an edge anchor."
    },
    "typography_system": {
      "score": 4,
      "evidence": "Display, labels, and captions have distinct roles.",
      "action": ""
    },
    "image_and_material_treatment": {
      "score": 4,
      "evidence": "UI crops and grain treatment remain consistent.",
      "action": ""
    },
    "motion_and_rhythm": {
      "score": 4,
      "evidence": "The longest hold supports the result reveal.",
      "action": ""
    },
    "continuity_and_distinctiveness": {
      "score": 4,
      "evidence": "One crop and rule motif connects the scenes.",
      "action": ""
    }
  },
  "blocking_issues": []
}
```

Use [route-specific-rubrics.md](route-specific-rubrics.md) to populate `route_review`. A failed route-specific check prevents approval until corrected.

Perform the blind recognition test using [project-fingerprint.md](project-fingerprint.md). `identity_review.result` must pass, `confusable_with` must be empty, and `project_recognizability` must score at least `4`.

The `scene_audit` must contain one item per full-size frame. At least 60 percent must carry `primary` identity, source evidence must be visible in at least 40 percent, no more than 20 percent may be `generic`, and primary identity scenes must require redesign rather than copy-only changes. The template-swap test must identify at least three required redesigns.

Supported redesign dimensions are `composition`, `source_evidence`, `semantic_transformation`, `motion_behavior`, `data_structure`, and `material_treatment`.
