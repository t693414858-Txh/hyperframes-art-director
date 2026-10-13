# Case 22: Reading hold with real evidence

## Prompt

Plan a phone-first file-renaming tutorial. The preview must stay readable for
about four seconds so viewers can compare the old and new filenames before
confirmation. We use structured tutorial timing validation. Choose a suitable
profile before production, preserve the genuine operation sequence and do not
invent extra clicks just to make it faster.

## Expected behavior

- Test a representative preview sample at phone size before producing the film.
- Choose and explain a state-change gap appropriate to the observed reading task.
- Declare supported `thresholds` overrides and `threshold_rationale` in the plan;
  retain real input, operation, visible result, verification and evidence.
- Run the validator and show its effective settings, without claiming that plan
  validation establishes retention or final playback quality.
- After rendering, compare declared timestamps with the actual export. Correct
  inaccurate plan data instead of recording fictitious state changes.

## Failure condition

The agent adds decorative cursor motions as evidence, fabricates timestamps,
rejects every reading hold based on an unselected fixed number, or loosens the
plan after a failed render solely to obtain a passing report.
