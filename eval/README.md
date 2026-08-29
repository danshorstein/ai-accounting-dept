# Model comparison test — August 2026 operating cash reconciliation

Run the **same** Staff Accountant agent and Skills, unchanged, under different models,
on the same reconciliation, and score the results against a fixed answer key — to see
how capability (and cost) varies by model on this specific job.

This is a testing harness for the experiment, not a new accounting role. It lives
outside `.claude/agents` and `.claude/skills` on purpose.

## What is in the repo (safe for the model under test to see)

- `../data/august-2026-*.csv` — the test period's source data (bank detail, GL cash
  detail, bank summary, trial balance). Columns are `id,date,description,amount`
  (plus `account` on the GL file) — no hints, tags, or notes.
- `schema/reconciliation-result.schema.json` — the fixed JSON shape the structured
  output must conform to. Given to the model only at Step 2 (the translation step),
  never during the accounting work itself.
- `results/` — where each model's `<model-name>-august-2026.json` is written.

## What is deliberately NOT in the repo

The Staff Accountant agent's tools (`Read`/`Grep`/`Glob`/`Bash`) operate on this
working tree, so **anything committed here is reachable by the model under test.**
Everything that would tip off the model therefore lives *outside* the repository,
in a sibling directory handed over separately when the harness was built:

```
../ai-accounting-dept-eval-private/
  README.md      — full running instructions and the list of what each trap tests
  prompts/       — the exact two-step prompt sequence to give the model
  generation/    — regenerates the CSVs and answer key together
  grading/       — the deterministic grader
```

The **answer key** is not in that directory either — it is not committed to any git
repository, on any branch, at any path. It was handed over directly, out of band.
Store it somewhere no test session has a path to, and pass its location to the grader
on the command line at grading time.

If you don't have the private directory or the answer key, ask whoever set up the
harness. Do not reconstruct the trap list into this repo.

## Running a test (summary — full version in the private README)

1. Fresh session on the model under test, no memory of other runs.
2. Give it **Step 1** from `../ai-accounting-dept-eval-private/prompts/august-2026-task-prompt.md`
   and let the Staff Accountant agent produce
   `workpapers/2026-08 operating-cash-reconciliation.md`.
3. Give it **Step 2** to translate that workpaper into
   `eval/results/<model-name>-august-2026.json`.
4. Grade it:
   ```
   python3 ../ai-accounting-dept-eval-private/grading/grade.py \
     eval/results/<model-name>-august-2026.json \
     /path/outside/any/repo/answer-key-august-2026.json
   ```
5. Repeat per model. Compare scores; note each run's token cost separately.

Never show the model the private README, the prompts file, the generator, the
grader, or the answer key.
