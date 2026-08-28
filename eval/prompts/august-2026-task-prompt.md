# August 2026 model-comparison test — task prompts

Two prompts, given in sequence, to the **same Staff Accountant agent** (unchanged
`.claude/agents/staff-accountant.md` and its two Skills), under whichever model is
under test. The point of the exercise is the model, not the agent or the process.

Run each model as its own fresh session with no memory of other runs. Do not show the
model this file, the schema, or the answer key.

---

## Step 1 — the real accounting work (give this prompt alone)

> Prepare the **August 2026** operating cash reconciliation for account 101000,
> following the same process, references, and Skills you used for July. Source files
> are `data/august-2026-bank.csv`, `data/august-2026-gl-cash.csv`,
> `data/august-2026-bank-summary.csv`, and `data/august-2026-trial-balance.csv`.
>
> One difference from the July engagement: the Controller is not available
> synchronously during this engagement. Where you would normally stop and ask for a
> matching tolerance, materiality threshold, or escalation threshold, instead state
> your working assumption explicitly, proceed on that basis, and log it in the
> judgment log as **your own inference**, not as a Controller instruction — because
> none was actually given for this engagement. Do not carry forward July's specific
> numbers (the 5-day window, the $5,000 threshold) by assuming they still apply; if
> you land on the same numbers, say explicitly that you re-derived them rather than
> reused them.
>
> Produce the complete workpaper as usual.

This step is graded qualitatively (does the workpaper meet the standard in
`reconciliation-workpaper-construction`?) and is also the input to Step 2.

## Step 2 — structured translation (give only after Step 1's workpaper is complete)

> Now translate the workpaper you just finished into JSON conforming exactly to the
> schema at `eval/schema/reconciliation-result.schema.json`. This is a serialization
> step, not a new analysis — every value must come from the workpaper you already
> produced. Reference source rows by the `id` column in the CSVs (e.g. `B07`, `G09`).
> Write the result to `eval/results/<model-name>-august-2026.json`. Do not create,
> drop, or re-classify anything that isn't already in the workpaper.

Why split it this way: asking for the schema *before* the analysis risks teaching the
model to chase a known rubric instead of doing the accounting judgment the exercise is
actually testing. Translating a finished workpaper the model already committed to is a
much lower-risk, closer-to-mechanical step.

## Grading

```
python3 eval/grading/grade.py eval/results/<model-name>-august-2026.json <path-to-answer-key.json>
```

The answer key is deliberately not stored in this repository — see `eval/README.md`.
