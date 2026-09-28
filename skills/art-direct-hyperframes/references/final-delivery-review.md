# Narration and final-file review

Use for narrated videos and final delivery. Apply the project's approved voice,
cost limits, caption style and ending behavior. Engine-specific generation
settings belong in the local voice profile rather than a shared skill default.

## One approved narration source

Use the approved model and voice reference for the complete narration. For
synthetic single-speaker work, regenerate the complete track when it drops words,
leaks reference text, duplicates a clause or switches timbre. Do not splice in a
different generation to repair one word. Intentional multi-speaker work follows
its own brief.

Transcribe without a text prompt to check the opening, all semantic units, proper
nouns and final sentence. Prompt-assisted recognition can help inspect a name,
but cannot prove that missing speech exists. Listen to uncertain pronunciations
when audio inspection is available; ASR homophones alone do not prove a spoken
error. A stable spoken form can differ from the formal product name in captions.

Silence detection is supporting evidence: a quiet interval can occur inside a
word. Compress only verified unwanted silence, retain a natural pause and record
the time mapping. Respect a project's chosen pause thresholds without imposing
them on expressive narration. Apply the same retiming to any lip-synced footage,
then rebuild captions, scenes and transitions from the final audio. Avoid repeated
global acceleration of an already sped-up track.

For scene changes tied to speech, use reviewed semantic boundaries from the final
transcript and check that transitions do not cover the incoming point. A project's
15ms alignment tolerance measures consistency with its declared boundary, not ASR
accuracy. A continuous scene can include editorial cutaways within a sentence;
do not force every footage cut onto a caption boundary.

## Fonts, captions and framing

Inspect actual font loading in a local render or snapshot. A successful CSS
declaration or a system font installed on the host does not establish that the
renderer used it. Resolve failed font loads before final rendering.

When the project requires white transparent captions without outlines or shadows,
provide enough contrast through the underlying composition. Verify the actual
caption region over time. Use caption-zone exceptions only for intentional
caption elements and the installed HyperFrames contract; they do not waive a
contrast defect. Respect the current project's approved font family.

Preserve source aspect ratio. Inspect vertical crops for faces, hands, products and
comparison details. Remove irrelevant phone chrome or workspace clutter when it
obscures the point. Report limited source resolution rather than presenting an
upscale as a native high-resolution original.

## Inspect the delivered file

Review the actual final MP4 after muxing and encoding:

- Capture frame zero, approximately 0.1s, important reveals and a frame inside the
  final duration. A CLI frame sampled after the end is not evidence of a blank ending.
- Ensure the opening already communicates its intended subject or hook and the
  last caption remains through the final word. Inspect orphan characters and
  cropped details at full size and a phone-sized view.
- Recheck the audio content, timing and ending in the encoded file. Voice-only
  checks and final mixed-audio checks serve different purposes; record which was used.
- Investigate an unintended silent tail. A deliberate music hold, source clip
  ending or user-requested end card is allowed with a recorded reason.
- Respect a project rule such as no new animation in the last five seconds only
  when that preference applies. Do not impose it on all films.
- Record warnings and what was actually reviewed. ASR, signal correlation and
  loudness measurements do not amount to human listening or approval.

## Invalidate stale review evidence

Identify the active export by path, duration and preferably SHA-256. Bind the
scorecard, contact sheet, transcript and delivery record to that export version.
After changing shots, re-render and repeat visual review; after retiming audio,
rebuild and check dependent timing. Carry over unchanged evidence only with a
stated reason. Never reuse an older version's score as a new edit's acceptance.

State separately what the user approved: direction, artwork, rhythm, final edit
or publication. Prepare one active delivery pack using the project's contract.
Publishing follows the user's current authorization; a render or style approval
does not itself change publication state.

For browser work, record pre-existing tabs and close completed temporary tabs
created for this task. Preserve user tabs, unsaved forms and intentional handoffs.
Record any retained task tab and why it is still needed.
