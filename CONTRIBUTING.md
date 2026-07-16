# Contributing

Contributions should improve the Skill's ability to make specific, coherent, and reviewable art-direction decisions without duplicating HyperFrames implementation rules.

## Before Opening a Change

1. Keep `SKILL.md` concise and procedural.
2. Put detailed design knowledge in `references/`.
3. Keep implementation constraints owned by `$hyperframes` and `$hyperframes-cli`.
4. Treat anti-patterns as diagnostic signals with documented exceptions.
5. Do not add copyrighted or ambiguously licensed fonts, footage, images, textures, or mood-board assets.
6. Translate named brand references into visual properties; do not encode imitation of protected identity systems.
7. Keep user taste memory project-local unless a preference generalizes across multiple projects.
8. Treat inspected visual evidence as stronger than style adjectives or brand reputation.
9. Do not select a material-dependent route without a valid asset-readiness report.
10. Separate route-level styling from project-level recognizability.

## Add or Change a Rule

Describe:

- The visible symptom
- Why it harms comprehension or visual identity
- The corrective action
- When an exception is justified

Add or update an evaluation case that can reveal whether the rule generalizes.

## Add or Change a Style Route

Document:

- Which content intents and evidence conditions the route serves
- Which source materials it expects
- Composition, typography, palette, image, and motion behavior
- When the route should not be selected
- How it remains original when a user supplies a recognizable brand reference
- How it can support, or be supported by, another route without replacing the primary system

Add at least one positive routing case and one nearby case where the route should be rejected.

When a route is added, update:

- `references/content-style-router.md`
- `scripts/validate_direction.py`
- The passing direction-brief example
- Repository validation and at least one unit test

## Change the Direction Contract

Keep the JSON contract deterministic and dependency-free. Add a passing example, a failing example, and a focused unit test for every new required invariant.

## Change the Asset Gate

Document:

- Which asset, rights, quality, or evidence failure the rule detects
- Whether it should produce `degraded` or `blocked`
- Which visual routes are most affected
- A viable re-route or minimum acquisition requirement

Add or update passing and failing `asset-readiness.json` examples and focused tests.

## Change the Project Fingerprint

Document:

- What specific project transformation should remain recognizable without labels
- Which real source evidence proves it
- Which anchors recur across scenes
- Which unrelated project or generic template it could be confused with
- How the blind recognition test should fail before the change and pass after it
- Which composition, evidence, motion, data, or material decisions must change in a template-swap test

Do not use color, typography, cards, logo, captions, or presenter as the only fingerprint evidence.

## Validate

Run:

```bash
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests -v
python3 skills/art-direct-hyperframes/scripts/validate_asset_readiness.py \
  examples/asset-readiness.pass.json
python3 skills/art-direct-hyperframes/scripts/validate_direction.py \
  examples/direction-brief.pass.json
python3 skills/art-direct-hyperframes/scripts/prepare_visual_review.py \
  examples/review-capture-plan.pass.json --validate-only
```

For material workflow changes, forward-test at least:

- An imagery-led brand or documentary video
- A typography-led announcement
- A data or UI explainer
- A redesign of an existing HyperFrames composition
- A mixed-content manuscript that could produce an incoherent hybrid
- A named brand reference that must be translated rather than copied
- A tutorial where instruction should outrank product-launch aesthetics
- A saved preference that applies only in a specific context
- A supplied reference that must be inspected and translated without copying
- An imagery-led request with insufficient or unlicensed production assets
- Two plausible visual directions that must be compared with hero-frame evidence
- A rendered draft whose planned timestamps generate a complete review evidence package
- A coherent light or dark video that still fails project recognizability

Record failures as changes to the Skill or evaluation criteria, not as one-off prompt patches.

## Pull Requests

Keep pull requests focused. Explain the behavior changed, the evaluation case used, and any compatibility assumptions about HyperFrames.
