# Reference Analysis Protocol

Use this protocol when the user supplies a video, URL, screenshot, mood board, prior render, competitor example, or named visual reference. The goal is to extract useful visual behavior without copying identity.

## Evidence Standard

Inspect the actual supplied source whenever access and tools permit.

- For video, sample the opening, first structural change, midpoint, climax, ending, and any user-identified moment.
- For a page or image set, inspect both the overall system and representative details.
- For a named brand without a supplied artifact, state that the analysis is based on broad public characteristics and is less reliable than direct evidence.
- Record inaccessible, low-resolution, incomplete, or ambiguous evidence.

Do not infer an entire motion system from a thumbnail. Do not claim visual fidelity from a text description alone.

## Analyze Properties

Record:

1. Narrative structure and information density
2. Composition archetypes and focal hierarchy
3. Typography roles, physical character, and behavior
4. Palette roles and material treatment
5. Image, footage, UI, data, or illustration treatment
6. Motion hierarchy, pacing, stillness, and transition language
7. Repeated identity anchors
8. Deliberate variation across structural beats
9. What makes the reference effective for its original purpose
10. What would conflict with the current manuscript, assets, audience, or platform

## Translate, Do Not Copy

Sort findings into:

- `retain`: a transferable principle that serves the current project
- `transform`: a useful behavior that must be adapted to different content, format, or assets
- `reject`: a protected, irrelevant, overused, or strategically harmful element

Never retain a third party's logo, masthead, slogan, proprietary typeface, signature interface, exact layout sequence, product silhouette, or trade dress without supplied authorization.

## `reference-analysis.json`

When a detailed reference record is useful, use the following structure. Compact review can record the same relevant observations and limitations in the existing design notes; a new JSON file is optional.

```json
{
  "project": "example-video",
  "sources": [
    {
      "id": "reference-01",
      "location": "URL or project-local path",
      "source_type": "video",
      "access_status": "inspected",
      "rights_note": "Used for analysis only; not a distributable asset.",
      "sampled_moments": [
        {
          "location": "00:00",
          "observation": "A single image establishes the subject before labels appear."
        }
      ]
    }
  ],
  "findings": {
    "narrative_structure": "Outcome first, evidence second, quiet resolution.",
    "composition": ["Large off-axis crop", "One compact metadata zone"],
    "typography": ["Display text behaves as a framing edge"],
    "palette_material": ["Warm neutral canvas", "Natural source color"],
    "motion_rhythm": ["One primary movement per beat", "Long hold at climax"],
    "identity_anchors": ["Edge rule", "Warm paper field"],
    "variation": ["Crop distance", "Density", "Image-to-type balance"]
  },
  "translation": {
    "retain": ["Outcome-first structure", "Controlled negative space"],
    "transform": ["Replace publication metadata with project evidence labels"],
    "reject": ["Masthead", "Exact page grid", "Proprietary typeface"]
  },
  "originality_risk": "medium",
  "confidence": "high",
  "limitations": []
}
```

Use `access_status` values `inspected`, `partial`, or `unavailable`. When a decisive source is `unavailable`, stop before claiming a reference-led direction or label the direction as assumption-led.
