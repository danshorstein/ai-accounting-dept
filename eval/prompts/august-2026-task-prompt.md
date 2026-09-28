# August 2026 model-comparison test — how to run it

The point of the exercise is the model, not the agent or the process, so every model
under test gets: the **same Staff Accountant agent and Skills, unchanged**; the **same
starting repository state**, pinned to one commit; **no visibility into each other's
runs**; and **no visibility into the schema-before-analysis, the grading logic, or the
answer key**.

## Why this isn't just "clone the repo"

`eval/` (this file, the schema, the generator, the grader) lives only on
`claude/reconciliation-model-testing-5yat7g`. That branch's `eval/generation/generate_august.py`
tags every row with its ground truth (`"tag": "DUPLICATE_ROW"`, `"tag": "GL_SIGN_ERROR"`,
etc.) and `eval/README.md` spells out all nine traps in prose — either one is the
answer key in a different shape. A model reconciling August only needs `data/`,
`references/`, `.claude/`, and last month's `workpapers/` entry — exactly what a real
engagement has.

So: **test sessions must never check out `claude/reconciliation-model-testing-5yat7g`.**
They check out **`eval-fixture/august-2026-v2`**, pinned to commit
**`14a8edb471f6ab68a1eef38782fcbd9ffcb7d76c`**. That branch's own git history never
contained `eval/` at any point — it was built by branching off the commit *before*
`eval/` existed and cherry-picking only the four August CSVs on top — so even
`git log -p` or `git show` inside that checkout can't recover it. (A model would still
need to actively go hunting with `git branch -r` / `git fetch --all` against the
shared GitHub remote to discover the other branch exists at all; a normal reconciliation
run has no reason to do that. If you want that residual path closed off too — fully
airtight rather than "no realistic path" — mirror this branch into a separate,
dedicated repo instead of a branch of the same one. Worth doing if you're testing
adversarial thoroughness specifically; not necessary for a capability/cost comparison.)

Always re-verify before a test run, in case the fixture branch is ever regenerated:

```
git log --oneline -- eval/    # run against eval-fixture/august-2026-v2 -- must print nothing
```

## Per-model isolation

Each model gets its own session via `create_session`, pointed at the pinned fixture
commit, with its own unique output branch so runs can never see each other:

- `source_url`: this repository
- `source_revision`: `14a8edb471f6ab68a1eef38782fcbd9ffcb7d76c` (NOT the working branch)
- `model`: the model under test
- `outcome_branch`: something unique per run, e.g. `eval-run/<model-name>-<date>` —
  never reuse one across models, and never point it at a branch another run reads
- `permission_mode`: `bypassPermissions` (or `acceptEdits`) so an unattended run
  doesn't stall on a tool-approval prompt with nobody watching
- `prompt`: Step 1 below

These are separate containers with separate clones — nothing another session writes
is visible unless you deliberately point two sessions at the same branch, so don't.

## Step 1 — the real accounting work

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

This is graded qualitatively (does the workpaper meet the standard in
`reconciliation-workpaper-construction`?) and is also the input to Step 2. Wait for
this to finish before sending Step 2 — don't hand the model the schema up front.

## Step 1b — the expected halt, and the scripted Controller reply

**Expect the Staff Accountant to stop at the population gate** and ask for direction. The
exact-duplicate bank row makes the bank roll-forward fail, and its own rules
(`source-population-validation` §4, agent escalation rules) require a stop before
matching. Confirmed on 2026-09-28: it halts even when told no Controller is available.
That halt is correct behavior, not a failure. Score it as a gate result, then resume it.

Resume by starting a new session from the halted run's pushed commit (a cloud session
that has finished cannot be messaged) and sending this scripted Controller reply. It names
only the row the agent itself flagged, and reveals nothing about any other finding:

> Use the staff-accountant agent. You previously halted the August 2026 operating cash
> reconciliation at the population-validation gate; your halted workpaper and script are
> in `workpapers/`. I am the Controller and have reviewed that draft. My direction:
> 1. Set duplicate bank row B10 aside as a likely data-quality artifact and proceed with
>    the detailed reconciliation excluding it. Keep it disclosed as an integrity finding
>    and escalation.
> 2. Carry all your other findings through to where they land.
> 3. Engagement parameters for this engagement only: matching tolerance exact amount
>    ($0.00); date window 5 days; escalation threshold $200.00; no materiality figure is
>    specified.
> 4. Verify roll-forward continuity from July and confirm the July carryover items
>    against the July workpaper.
>
> Complete the reconciliation: update the existing workpaper and calculation script in
> place, following the workpaper skill. When finished, commit everything and push.

Use the same reply for every model so runs stay comparable. Grade the resumed run's
workpaper, not the halted one.

## Step 2 — structured translation (send only after Step 1's workpaper is done)

Paste the full contents of `eval/schema/reconciliation-result.schema.json` (from the
working branch — the child session doesn't have this file) directly into the message,
followed by:

> Translate the workpaper you just finished into JSON conforming exactly to the
> schema above. This is a serialization step, not a new analysis — every value must
> come from the workpaper you already produced. Reference source rows by the `id`
> column in the CSVs (e.g. `B07`, `G09`). Write the result to
> `workpapers/2026-08 operating-cash-reconciliation.json`. Do not create, drop, or
> re-classify anything that isn't already in the workpaper.
>
> Then commit everything you produced this session (the workpaper and this JSON file)
> and push.

## Collecting and grading results

After each session finishes and pushes to its `outcome_branch`:

```
git fetch origin <outcome_branch>
git show origin/<outcome_branch>:"workpapers/2026-08 operating-cash-reconciliation.json" > /tmp/<model-name>.json
python3 eval/grading/grade.py /tmp/<model-name>.json <path-to-answer-key.json>
```

Run this from the working branch, in your own session — **never inside a test
session**. That's what keeps the grading logic and the answer key from ever being in
the same process as the model being graded.
