# Changelog

All notable changes to this project are documented here.

## 0.11.0 - 2026-10-13

### Changed

- Shorten the entrypoint around format choice, representative samples, shot planning, targeted revisions and review of the actual export.
- Use compact project notes by default. Keep detailed JSON contracts and identity/interaction quotas available for projects that adopt those profiles, rather than requiring them for every video or visual correction.
- Preserve approved narration during visual-only revisions; check changed shots and their dependencies without restarting unrelated work.
- Keep device-specific publishing recovery in the account project instead of the shared art-direction Skill.
- Revise conflicting preferences in place instead of accumulating a universal rule for each failed edit.

### Added

- Review-depth and change-impact guide, plus behavioral evaluation cases for narrow visual fixes and intentional reading holds.
- Configurable tutorial timing thresholds with a required rationale, reported effective settings and unchanged evidence requirements.
- Regression tests for declared reading holds, invalid overrides, non-finite timestamps and malformed operation steps.

### Migration

- Existing JSON plans without overrides retain their previous defaults; existing validators and detailed contracts remain available.
- Choose a timing profile before production. A new profile is not permission to fabricate actions or relax a failed target merely to report a pass.
- A passing validator checks the supplied plan or evidence record. It does not establish aesthetic quality, human listening or improved audience retention.

## 0.10.0 - 2026-09-28

### Changed

- Route operation tutorials, case analysis, artwork showcases and stories separately; tutorial timing and interaction quotas no longer govern every short video.
- Require case-film review to assess work stages, actions, environments and source intervals instead of treating more cuts or cropped duplicates as richer footage.
- Bind review evidence to the delivered export and invalidate scores after a visual revision.
- Preserve existing publication authorization, including scoped standing grants, when resuming recurring projects.

### Added

- Footage-editing reference with a shot-ledger contract, source-interval overlap rule, intentional callback handling and playback review.
- Final-file review for whole-track narration, retiming, font loading, source proportions, first/last frames and evidence freshness.
- An opt-in account style profile and three behavioral evaluation cases for format routing, material repetition and final-export regressions.

### Migration

- Existing tutorial JSON plans and validators are unchanged. Declare the production format before selecting validators; case analysis uses footage and narrative review recorded in the existing aesthetic scorecard.
- Local voice-engine settings and account-specific caption or ending preferences belong in the project profile. The shared Skill does not impose them on every installation.

## 0.9.0 - 2026-07-25

### Added

- Data-informed short-form retention standard for tool tutorials, workflow demonstrations, reviews, and lead magnets
- Deterministic `shortform-retention-plan.json` validator covering opening proof timing, early state changes, continuous operation evidence, and runtime bands
- Passing and failing retention plans, unit tests, and a delayed-proof regression evaluation
- Post-publish calibration targets for 2-second bounce, 5-second completion, average play ratio, favorites, and follow conversion

### Changed

- Full production and render-review workflows now block applicable short-form videos when proof arrives late or poster cards replace real operation
- Repository validation and GitHub Actions now include the short-form retention gate

## 0.8.0 - 2026-07-16

### Added

- Detailed English and Chinese GitHub documentation for public release
- Pre-voice `content-rhythm.json` contract and validator for experience, interaction, and information-density coverage
- `experience-interaction-qa.json` contract and validator for felt experience change, proof, CTA timing, and CTA consistency
- Passing and failing examples plus unit tests for both new validation gates

### Changed

- GitHub Actions now runs content-rhythm and experience-interaction validation
- Repository validation now requires bilingual public documentation and the new validator resources

## 0.7.0 - 2026-06-13

### Added

- Quantitative core-identity coverage for direction plans and rendered frames
- Per-scene template-swap results, proof-asset references, and replacement dimensions
- Review thresholds requiring 60 percent primary identity and 40 percent visible source evidence
- Generic-frame ceiling of 20 percent during rendered contact-sheet review
- Template-swap test proving that an unrelated project requires at least three redesign areas
- Single-scene `complete` identity role with compatible recurrence rules
- Meeting-action redesign blueprint derived from a real failed light-template output
- Auto-generated per-frame identity-review scaffold in `review-evidence.json`

### Changed

- Core identity scenes must contain both semantic-transformation and source-evidence anchors
- Multi-scene directions require establish, prove, and resolve identity roles
- Copy-only adaptation is now measured independently from visual coherence and average aesthetic score
- Template-swap redesign dimensions now use a fixed vocabulary instead of free-form claims

## 0.6.0 - 2026-06-11

### Added

- Project-fingerprint protocol separating route style from project recognition
- Required semantic-transformation and source-evidence anchors
- Scene-level fingerprint recurrence and minimum-appearance validation
- Blind recognition test that ignores project name, logo, captions, and presenter
- `Project Recognizability` as an eighth review dimension with a hard minimum score of `4`
- Regression case for coherent but interchangeable light editorial meeting videos

### Changed

- Full Direction now fails when identity depends only on palette, typography, cards, presenter, subtitles, or a repeated shell
- Aesthetic review now blocks videos that can be relabeled as unrelated projects without redesign
- Presenter presence is treated as channel continuity rather than sufficient project identity

## 0.5.0 - 2026-06-11

### Added

- FFmpeg-backed `prepare_visual_review.py` for deterministic hero-frame extraction
- `review-capture-plan.json` contract for ordered scene timestamps and contact-sheet layout
- Automatic `review-evidence.json` output compatible with the aesthetic scorecard
- Passing and failing capture-plan examples plus five focused tests

### Changed

- Major reviews now generate full-size frames and a contact sheet from one declared plan
- Review evidence records exact source video, timestamps, dimensions, and artifact paths
- Runtime documentation now distinguishes standard-library validators from optional FFmpeg capture

## 0.4.0 - 2026-06-11

### Added

- Visual-reference analysis protocol with sampled evidence and retain, transform, and reject decisions
- Asset-readiness contract and dependency-free validator for rights, quality, primary material, and claim coverage
- Visual benchmark protocol and pairwise candidate-direction comparison
- Contact-sheet review protocol for thumbnail, full-size, and playback inspection
- Route-specific review checks for all ten visual routes
- Passing and failing asset-readiness examples plus five focused validator tests
- Three evaluation cases for reference adaptation, asset-constrained re-routing, and visual-direction comparison

### Changed

- Full Direction now requires asset readiness and visual candidate evidence before HyperFrames implementation
- Direction validation now enforces three hero-frame concepts per candidate and a documented selection
- Review validation now requires contact-sheet, full-frame, playback, and route-specific evidence

## 0.3.0 - 2026-06-11

### Added

- `Knowledge Explainer` route for tutorials, software education, and workflow instruction
- Candidate-route scoring across intent, material, credibility, audience, and brand fit
- Structured `direction-brief.json` contract for pre-implementation art direction
- Dependency-free direction validator covering route logic, palette specificity, script coverage, scene timing, and supporting-route scope
- Project-level `STYLE-PREFERENCES.md` template for contextual preference memory
- Passing and failing direction-brief examples plus direction-validator unit tests
- Scene grammar with stable identity anchors and controlled variation axes

### Changed

- Full Direction now validates both `DESIGN.md` and a structured direction brief before HyperFrames implementation
- Continuity review now detects coherent but monotonous scene systems
- Repository validation and CI now cover the direction contract

## 0.2.0 - 2026-06-11

### Added

- Manuscript diagnosis covering intent, audience, emotional temperature, evidence, assets, and sensitivity
- Content-to-style router with nine content categories and nine visual routes
- Primary and supporting route rules for mixed-content scripts
- Originality guardrails for named references such as Apple and The New York Times
- Content-to-style fit as a seventh review dimension
- Four forward-testing cases for technology, culture, mixed content, and public information

### Changed

- `DESIGN.md` template now records route choice, confidence, rejected alternatives, and documented exceptions
- Anti-pattern library now detects category costumes, prestige-brand mimicry, default dark technology styling, and uncontrolled hybrids
- Review examples, validator, tests, repository validation, and agent metadata now enforce adaptive routing

## 0.1.0 - 2026-06-10

### Added

- Installable `art-direct-hyperframes` Skill
- Explicit responsibility boundary with HyperFrames implementation skills
- Full Direction, Review Pass, and Fast Pass workflows
- Visual-direction framework and compatible `DESIGN.md` template
- Six-dimension aesthetic review rubric
- Dependency-free JSON scorecard validator
- Four forward-testing cases covering imagery, typography, data, and redesign
- Contact-sheet, full-frame, playback, and `DESIGN.md` evidence requirements
- Anti-patterns for persistent interface shells, unsupported claims, sparse post-cut states, and presenter obstruction
- Repository validation, unit tests, and GitHub Actions workflow
