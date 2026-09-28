# Case 17: Short-Form Retention Gate

## Prompt

Create a 65-second vertical tutorial from a software workflow. Start with an
eight-second presenter introduction, explain the method with static cards, and
show the first real operation after 12 seconds.

## Expected behavior

- Classify the request as an applicable short-form retention-gate project.
- Refuse to proceed directly to voice generation or HyperFrames implementation.
- Create `shortform-retention-plan.json`.
- Move the problem and result preview into the first `0.8s`.
- Begin a real operation by `2.5s` and show visible proof by `5s`.
- Replace static poster-card sequencing with a continuous workspace operation.
- Reduce the single-task runtime to `35s` or require a valid runtime waiver.
- Run `validate_shortform_retention.py` and expose the result as review evidence.

## Failure condition

The skill preserves the delayed proof, treats poster cards as sufficient
demonstration, or starts implementation without passing the retention validator.
