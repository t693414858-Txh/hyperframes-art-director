# Experience and Interaction Standard

Apply this gate to tool updates, tutorials, reviews, workflow explainers, and lead-magnet videos. A project does not pass by displaying feature names alone.

## Coverage Gate

Passing individual checks is not enough. Follow the separate `content-rhythm-standard.md`, validate the planned timeline before TTS, and measure again against final narration timestamps before rendering:

- Experience-led content must cover at least 40 percent of runtime.
- Interaction-led content must cover at least 20 percent of runtime.
- After merging overlaps, experience plus interaction must cover at least 60 percent of runtime.
- Interaction should form a loop across the narrative: an opening self-check or promise, a mid-video choice or judgment, and a closing payoff using one final action.
- A feature-list segment does not count unless it states or visibly demonstrates a user decision, felt change, workflow consequence, or limitation.

## Experience Gate

All four checks must pass:

1. **Felt change**: State one concrete difference the viewer experiences before versus after, such as fewer handoffs, less copying, faster verification, or clearer control.
2. **Best-fit task**: Name one task shape where the feature is worth using and show the input, operation, and result.
3. **Boundary**: Name one limitation, cost, authorization step, unavailable plan, or task where the simpler workflow remains better.
4. **Evidence**: Keep at least one visible experience proof on screen long enough to understand. Adjectives such as “powerful” or “efficient” do not count as evidence.

## Interaction Gate

All five checks must pass:

1. **Early invitation**: Place one low-friction interaction before 60 percent of the runtime.
2. **Single primary action**: The final CTA asks for one primary behavior. Do not stack follow, like, save, comment, and direct message.
3. **Exact response format**: Show the literal reply format, such as `A / B / C` or one keyword.
4. **Specific reward**: State what the viewer receives or how the response changes the next episode.
5. **Contract consistency**: Narration, captions, on-screen CTA, publishing description, and pinned comment use the same keyword and reward.

## Evidence Record

For each video, save an `experience-interaction-qa.json` containing:

- the exact narration lines that satisfy each gate;
- timestamps and frame evidence;
- CTA keyword or response format;
- promised reward;
- pass or fail for every check.
- measured experience, interaction, and combined unique coverage with timestamp ranges.

Any failed check is blocking unless the user explicitly approves a no-experience or no-interaction format for that video.
