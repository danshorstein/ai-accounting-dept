# Runbook — testing a new model on the August 2026 reconciliation

Follow this top to bottom. It tells you which steps you do yourself, and which
steps to hand to a Claude Code session by pasting the given instruction in.
"Orchestrator session" below means whatever Claude Code session you're doing this
work from — it can be this one.

Do not skip ahead to "Grade the results" out of curiosity before a run finishes —
that's the one step that must never happen inside the same session as a model
under test.

---

## 0. Before you start (you do this)

- [ ] Decide which models you're comparing this round, and write down their exact
      model IDs.
- [ ] Confirm you still have the answer key file
      (`answer-key-august-2026.json`, sent to you as a file earlier — not in this
      repo). Know its path on your machine. If you've lost it, ask the orchestrator
      session to run `eval/generation/generate_august.py` again with a
      `--answer-key-out` path outside this repo, and send it to you again.
- [ ] Confirm the fixture commit hasn't changed. Run:
      ```
      git log --oneline -- eval/
      ```
      on branch `eval-fixture/august-2026`. **This must print nothing.** If it
      prints anything, stop — the fixture is no longer clean, and testing against
      it would leak the answer. Ask the orchestrator session to rebuild it before
      continuing (see `eval/README.md`, "Isolation architecture").

## 1. Start one test session per model (orchestrator session does this)

For each model, tell the orchestrator session:

> Start a new test session for model `<exact model ID>`. Use `create_session` with:
> - `source_url`: this repository
> - `source_revision`: the current commit of `eval-fixture/august-2026`
> - `model`: `<exact model ID>`
> - `outcome_branch`: `eval-run/<short-model-name>-<today's date>`
> - `permission_mode`: `bypassPermissions`
>
> Then send it the Step 1 prompt from `eval/prompts/august-2026-task-prompt.md`.

Repeat once per model, each as its own `create_session` call. **Do not reuse an
`outcome_branch` name across models** — if two runs share a branch, the second
run's session can see the first's committed work, which defeats the isolation.

Write down each model's `outcome_branch` name as you go — you'll need it in step 3.

## 2. Send Step 2 once each session finishes its workpaper (orchestrator session does this)

Wait for a session to report that it has produced
`workpapers/2026-08 operating-cash-reconciliation.md`. Do not send Step 2 early —
the whole point of splitting the prompt is that the model commits to its judgment
before ever seeing the required output shape.

Once it's done, tell the orchestrator session:

> Send the Step 2 prompt from `eval/prompts/august-2026-task-prompt.md` to
> `<session name/ID>`, with the schema
> (`eval/schema/reconciliation-result.schema.json`, read from this branch) pasted
> into the message as instructed there.

Confirm the session reports it committed and pushed both files.

## 3. Fetch every run's result (orchestrator session does this)

For each model's `outcome_branch`:

> Fetch `<outcome_branch>` and extract
> `workpapers/2026-08 operating-cash-reconciliation.json` from it to
> `/tmp/<short-model-name>.json`.

## 4. Grade every run (orchestrator session does this — but only after ALL runs are fetched)

> Run `python3 eval/grading/grade.py /tmp/<short-model-name>.json
> <path-to-your-answer-key>` for each model and report the score and the
> pass/fail breakdown for each.

This is the one step that must happen only here, on this branch, after every
model's session is finished — never ask a model-under-test session to grade
itself or another model.

## 5. Record and review (you do this)

- [ ] Note each model's score, and separately its token cost / price for the run
      (from wherever your usage is billed) — keep these as two separate columns,
      don't blend them into one number.
- [ ] Skim the actual workpaper `.md` files, not just the JSON scores, for at
      least the lowest- and highest-scoring runs — the score tells you *that*
      something was missed, the workpaper tells you *how* the model reasoned
      about it, which matters more for deciding whether a cheaper model is
      "good enough."
- [ ] Decide whether to keep the per-model branches (recommended — they're a real
      audit trail of what each model actually did) or delete them once you're
      done.

## If something looks wrong

- **A session asks you (the human) a clarifying question mid-run**: that's fine
  and expected — the task prompt deliberately doesn't hand it every parameter.
  Answer as the Controller would, but don't tell it anything about the traps.
- **A session's output doesn't match the JSON schema**: don't hand-fix it before
  grading — that would be grading your correction, not the model's work. Score it
  as-is (or note it as a schema-compliance failure) and move on.
- **You're not sure whether a branch is safe to test against**: re-run the check
  in step 0. When in doubt, don't test against it — ask the orchestrator session
  to rebuild the fixture branch fresh.
