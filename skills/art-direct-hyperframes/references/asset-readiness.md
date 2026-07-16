# Asset Readiness Gate

Audit actual project assets before committing to a visual route. A direction is not viable merely because it sounds appropriate.

## Inventory

Record each usable image, footage clip, interface capture, chart, document, logo, font, illustration, texture, and audio source. For every asset, identify:

- Location or source
- Rights or license status
- Provenance
- Technical quality
- Narrative relevance
- Scenes and claims it can support

Do not count an unavailable idea, search result thumbnail, or unlicensed mood-board image as a production asset.

## Status

- `ready`: primary material, evidence coverage, rights, and technical quality support the route
- `degraded`: the route can proceed only with explicit simplification, substitutions, or reduced claims
- `blocked`: critical material, rights, provenance, or evidence is missing

High-credibility claims must map to visible evidence. An imagery-led route requires at least one primary visual asset. Unknown rights cannot pass as `ready`.

## Re-route Rules

- Missing documentary imagery: move toward evidence-led typography, documents, maps, or a narrower editorial scope.
- Missing readable UI: do not promise a workflow demonstration; capture the interface or change the narrative.
- Missing data provenance: remove the claim, source it, or present it as an explicitly labeled hypothesis.
- Missing premium product material: avoid a macro product-film direction built from generic cards.
- Missing brand assets: use an original neutral system and do not reconstruct the brand from memory.

## Validation

Save `asset-readiness.json` and run:

```bash
python3 <skill-directory>/scripts/validate_asset_readiness.py asset-readiness.json
```

The validator checks rights status, primary-material support, evidence coverage, asset references, and consistency between the declared readiness status and missing critical material.

Use this structure:

```json
{
  "project": "example-video",
  "intended_route": "Knowledge Explainer",
  "status": "ready",
  "primary_material_type": "Readable interface and output captures",
  "assets": [
    {
      "id": "ui-recording-01",
      "type": "video",
      "location": "assets/workflow.mp4",
      "role": "primary",
      "license_status": "owned",
      "provenance": "Recorded by the project owner.",
      "quality": "high",
      "duration_seconds": 42,
      "supports_scenes": ["scene-02", "scene-03"],
      "supports_claims": ["claim-workflow"]
    }
  ],
  "coverage": [
    {
      "id": "claim-workflow",
      "kind": "claim",
      "description": "Prove the workflow with a real interface recording.",
      "evidence_required": true,
      "covered_by": ["ui-recording-01"]
    }
  ],
  "missing_critical_assets": [],
  "limitations": ["Crop the recording without hiding target controls."],
  "route_recommendation": "Proceed with readable UI as primary material."
}
```

Supported asset types are `image`, `video`, `ui`, `data`, `document`, `audio`, `logo`, `font`, `texture`, and `illustration`. Image-like assets require positive `width` and `height`; video and audio require positive `duration_seconds`.
