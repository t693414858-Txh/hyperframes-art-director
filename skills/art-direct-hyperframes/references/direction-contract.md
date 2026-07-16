# Direction Brief Contract

For `Full Direction` and major redesigns, save a structured `direction-brief.json` next to `DESIGN.md`. It makes route selection, script coverage, timing, and scene intent testable before HTML implementation.

Validate it with:

```bash
python3 <skill-directory>/scripts/validate_direction.py direction-brief.json
```

## Required Structure

```json
{
  "project": "project-name",
  "mode": "full_direction",
  "delivery": {
    "platform": "vertical social",
    "aspect_ratio": "9:16",
    "planned_duration_seconds": 8,
    "sound_context": "sound-on with captions"
  },
  "content_profile": {
    "primary_category": "Technology education",
    "secondary_category": "",
    "communication_intent": "Teach",
    "audience": "New Codex users",
    "viewing_context": "Mobile",
    "emotional_temperature": "Calm and precise",
    "evidence_requirement": "high",
    "credibility_requirement": "high",
    "available_source_material": ["Real UI capture", "Narration"],
    "brand_cultural_sensitivity": "Use supplied brand assets only"
  },
  "route_decision": {
    "primary_route": "Knowledge Explainer",
    "supporting_route": null,
    "supporting_scope": "",
    "confidence": "high",
    "rationale": "The viewer must learn a real workflow.",
    "rejected_alternative": "Precision Product would overemphasize desire.",
    "override_reason": "",
    "named_reference_translation": "",
    "candidate_scores": [
      {
        "route": "Knowledge Explainer",
        "intent_fit": 2,
        "material_fit": 2,
        "credibility_fit": 2,
        "audience_fit": 2,
        "brand_fit": 2,
        "total": 10
      },
      {
        "route": "Precision Product",
        "intent_fit": 1,
        "material_fit": 2,
        "credibility_fit": 1,
        "audience_fit": 1,
        "brand_fit": 2,
        "total": 7
      }
    ]
  },
  "creative_thesis": "Make the viewer feel capable by revealing the workflow through calm, evidence-led steps.",
  "visual_evidence": {
    "reference_analysis_status": "completed",
    "reference_analysis_path": "reference-analysis.json",
    "asset_readiness_path": "asset-readiness.json",
    "direction_candidates": [
      {
        "id": "direction-a",
        "route": "Knowledge Explainer",
        "premise": "Teach through readable context-to-detail interface evidence.",
        "hero_frame_concepts": [
          "Outcome fills the frame.",
          "Prompt and target control share one causal composition.",
          "Verified output resolves beside a compact evidence strip."
        ],
        "primary_material_requirement": "Readable UI and output captures",
        "strength": "Instruction remains immediately reproducible.",
        "risk": "May feel dry if crop and scale do not evolve."
      },
      {
        "id": "direction-b",
        "route": "Precision Product",
        "premise": "Present the workflow as a polished product reveal.",
        "hero_frame_concepts": [
          "Output appears as one immaculate object.",
          "Interface floats in generous neutral space.",
          "Product result becomes the final macro reveal."
        ],
        "primary_material_requirement": "High-resolution interface and product captures",
        "strength": "Creates desire and material clarity.",
        "risk": "Can weaken the tutorial's instructional purpose."
      }
    ],
    "selected_direction": "direction-a",
    "selection_evidence": "Direction A preserves readable operations and scores better on instructional clarity at thumbnail size.",
    "comparison_waiver": ""
  },
  "project_fingerprint": {
    "recognition_target": "A Codex request becoming a visible change and verified result.",
    "proof_assets": ["Real Codex UI", "Finished output"],
    "anchors": [
      {
        "id": "request-change-verification",
        "type": "semantic_transformation",
        "description": "One request progresses through change and verification.",
        "minimum_scene_appearances": 2
      },
      {
        "id": "real-codex-evidence",
        "type": "source_evidence",
        "description": "Readable product evidence proves the workflow.",
        "minimum_scene_appearances": 2
      },
      {
        "id": "verification-rule",
        "type": "structural",
        "description": "One evidence rule links action to result.",
        "minimum_scene_appearances": 2
      }
    ],
    "scene_recurrence": [
      {
        "scene_id": "scene-01",
        "anchor_ids": [
          "request-change-verification",
          "real-codex-evidence",
          "verification-rule"
        ],
        "identity_role": "establish",
        "core_identity_scene": true,
        "template_swap_result": "requires_redesign",
        "proof_asset_ids": ["Finished output"],
        "replacement_dimensions": [
          "composition",
          "source_evidence",
          "semantic_transformation"
        ],
        "project_specific_evidence": "The finished artifact appears with verification."
      },
      {
        "scene_id": "scene-02",
        "anchor_ids": [
          "request-change-verification",
          "real-codex-evidence",
          "verification-rule"
        ],
        "identity_role": "resolve",
        "core_identity_scene": true,
        "template_swap_result": "requires_redesign",
        "proof_asset_ids": ["Real Codex UI", "Finished output"],
        "replacement_dimensions": [
          "source_evidence",
          "semantic_transformation",
          "motion_behavior"
        ],
        "project_specific_evidence": "The real request and resulting change remain visible."
      }
    ],
    "blind_test_prompt": "Ignore names, logos, captions, and presenter; identify the request-to-verification workflow.",
    "confusable_with": ["Generic AI tutorial"],
    "differentiation_strategy": "Use real request, change, and verification evidence as the recurring mechanism.",
    "template_swap_test": {
      "alternate_project": "Expense approval tutorial",
      "result": "requires_redesign",
      "required_redesigns": [
        "composition",
        "source_evidence",
        "semantic_transformation"
      ],
      "evidence": "Copy changes cannot replace the Codex interface, file change, and verification loop."
    }
  },
  "visual_system": {
    "primary_material": "Real UI capture",
    "composition_logic": "Context-to-detail progression",
    "identity_anchors": ["Warm-white canvas", "Black annotation rules"],
    "variation_axes": ["Crop", "Scale", "Evidence format"],
    "typography_roles": {
      "display": "Exact, compact sans",
      "supporting": "Highly legible sans",
      "labels": "Compact metadata"
    },
    "palette_roles": {
      "canvas": "#F5F5F3",
      "primary_text": "#121212",
      "secondary_text": "#666666",
      "accent": "#146EF5"
    },
    "image_treatment": "Crisp UI with controlled crops",
    "texture_depth": "Soft optical shadow only",
    "motion_character": "Stepwise and restrained",
    "transition_language": "One consistent directional reveal"
  },
  "rhythm_map": {
    "arrival": "Show the finished outcome.",
    "development": "Reveal the steps.",
    "contrast": "Pause on the common failure.",
    "climax": "Complete the workflow.",
    "resolve": "Return to the finished output."
  },
  "scenes": [
    {
      "id": "scene-01",
      "name": "Outcome",
      "script_beat": "The result appears first.",
      "narrative_purpose": "Create immediate relevance.",
      "route_role": "primary",
      "dominant_visual_idea": "One large finished artifact.",
      "primary_focal_point": "Artifact title",
      "secondary_eye_path": "Result metadata",
      "source_material": ["Real output capture"],
      "hero_frame": "The artifact fills the frame with one annotation.",
      "duration_seconds": 4,
      "energy": "medium",
      "primary_motion_intent": "Reveal the artifact as one visual group.",
      "transition_intent": "Directional reveal into the workflow."
    },
    {
      "id": "scene-02",
      "name": "Verification",
      "script_beat": "The requested change is verified.",
      "narrative_purpose": "Prove the workflow result.",
      "route_role": "primary",
      "dominant_visual_idea": "Real change and verification evidence share the frame.",
      "primary_focal_point": "Verified change",
      "secondary_eye_path": "Source request",
      "source_material": ["Real UI capture", "Real output capture"],
      "hero_frame": "The verified change remains connected to the original request.",
      "duration_seconds": 4,
      "energy": "high",
      "primary_motion_intent": "Reveal cause before consequence.",
      "transition_intent": "Resolve into a held verified result."
    }
  ],
  "avoidances": [
    "No generic AI gradients",
    "No tiny UI captures",
    "No repeated centered card layouts"
  ],
  "assumptions": [],
  "style_preferences_applied": [],
  "style_preferences_rejected": []
}
```

## Contract Rules

- Candidate scores use integers from `0` to `2`; `total` must equal the five factors.
- The primary route should have the highest score. A lower-scoring selection requires `override_reason`.
- Use only one supporting route and identify its bounded `supporting_scope`.
- Record whether supplied visual references were inspected and where the analysis is stored.
- Link the validated `asset-readiness.json` used to prove the direction is feasible.
- Compare at least two materially different visual directions, each with three hero-frame concepts.
- Use `comparison_waiver` only for an approved concrete direction or existing design system.
- `selected_direction` must match a candidate id and include visible selection evidence.
- Define a `project_fingerprint` that remains recognizable without names, logos, captions, presenter, or generic route styling.
- Include at least three fingerprint anchors, including `semantic_transformation` and `source_evidence`.
- Map every scene to project-specific evidence and recurring anchor ids.
- Each anchor must meet its declared `minimum_scene_appearances`.
- Color, typography, cards, presenter placement, and subtitle treatment cannot be the only fingerprint anchors.
- Multi-scene videos require at least 60 percent core identity scenes.
- Core identity scenes must include both semantic-transformation and source-evidence anchors.
- Core identity scenes must reference proof assets and at least two replacement dimensions.
- No more than 25 percent of planned scenes may survive through copy-only changes.
- A template-swap test must name an unrelated project and at least three required redesigns.
- Single-scene videos use the `complete` identity role; multi-scene videos use establish and resolve, plus prove when there are three or more scenes.
- Scene durations must sum to `planned_duration_seconds`.
- A supporting route should not dominate the timeline; keep it at or below roughly 40 percent unless `override_reason` explains why.
- Every scene maps one script beat to one dominant visual idea and one hero frame.
- `palette_roles` uses exact hex colors.
- `avoidances` contains at least three project-specific failures to prevent.
- Record both applied and rejected saved preferences when `STYLE-PREFERENCES.md` exists.
