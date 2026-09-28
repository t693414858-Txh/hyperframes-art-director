# More cuts with the same material

## Prompt

A revised film has 20 shots made from seven source files. Several are crops of
the same source interval. All but one show the same studio. The user approves
the movement style but says the film still repeats itself. The final freeze
deliberately recalls the opening.

## Expected behavior

- Inspect source IDs and in/out points, with crops mapped back to their originals.
- Separate accidental interval repetition from the intentional final callback.
- Evaluate actions, work stages, environments and shot scale, not file count alone.
- Replace unrelated or repeated shots while retaining the approved visual direction.
- Review variable durations and cut points against narration rather than imposing
  a uniform fast-cut schedule.

## Failure condition

The agent counts crops as new sources, adds faces without relevant actions, claims
20 shots prove variety or removes the deliberate callback without considering its role.
