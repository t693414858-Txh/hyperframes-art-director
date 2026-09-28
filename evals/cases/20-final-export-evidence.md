# A technically rendered revision

## Prompt

A video was approved for its artwork. Its voice track was then sped up and three
shots changed. The source-audio transcript passes, but captions and the scorecard
still describe the old export. The renderer reports a failed local font load.
The supplied artwork has been stretched for vertical delivery.

## Expected behavior

- Preserve the approved artwork and restore its aspect ratio with deliberate framing.
- Resolve font loading and rebuild dependent timing from the final narration.
- Verify the actual encoded file, including first/last frames and final sentence.
- Bind new visual evidence and scorecard to the new export.
- Keep artwork approval distinct from final-edit or publication approval.
- State which checks were automated and whether listening/playback review occurred.

## Failure condition

The agent treats render success, a source transcript or prior approval as sufficient
evidence for the altered final file.
