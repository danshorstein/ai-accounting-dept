# Model comparison test — August 2026 operating cash reconciliation

Purpose: run the **same** Staff Accountant agent and Skills, unchanged, under
different models, on the same reconciliation, and score the results against a fixed
answer key — to see how capability (and cost) varies by model on this specific job,
without relying on manual judgment for every run.

This is a testing harness for the experiment, not a new accounting role. It lives
outside `.claude/agents` and `.claude/skills` on purpose.

## Isolation architecture (read this before running anything)

This directory itself is a spoiler: `generation/generate_august.py` tags every row
with its ground truth and `README.md` (this file) spells out all nine traps below. A
model doing the actual reconciliation must never see any of it — and in fact never
needs to, since a real engagement wouldn't have an `eval/` folder either.

So test sessions never check out this branch. They check out **`eval-fixture/august-2026`**,
pinned to a specific commit, whose own git history never contained `eval/` at any
point (branched off the commit before `eval/` existed, with only the August CSVs
cherry-picked on top — so `git log -p` inside that checkout can't recover it either).
Each model also gets its own isolated session and its own unique output branch, so
runs can't see each other. Full mechanics, the exact commit to pin, and the
per-model `create_session` shape are in `prompts/august-2026-task-prompt.md` — follow
that file to actually run a test, and re-read it if the fixture branch is ever
regenerated (the commit to pin will change).

## What's here

- `../data/august-2026-*.csv` — the test period's source data (bank detail, GL cash
  detail, bank summary, trial balance). Built by
  `eval/generation/generate_august.py` from one source of truth, so the CSVs and the
  answer key can never drift apart from a transcription slip.
- `schema/reconciliation-result.schema.json` — the fixed JSON shape every model's
  structured output must conform to.
- `prompts/august-2026-task-prompt.md` — the exact two-step prompt sequence to run
  per model (real workpaper first, then a translation-only step into JSON).
- `grading/grade.py` — deterministic grader: candidate JSON + answer key in, a
  point score and a pass/fail line per check out. No judgment calls, so the same
  candidate always gets the same score.
- `generation/generate_august.py` — regenerates the CSVs and answer key together
  (kept here for provenance; re-running it reproduces exactly what's in `data/`).

## What is deliberately NOT here

**The answer key.** It is not committed to this repository, on any branch, at any
path — the Staff Accountant agent's tools (Read/Grep/Glob/Bash) operate on this
working tree, so anything checked in here is reachable by the model under test. The
key was handed to you directly outside of git when this harness was built. Keep it
that way: store it somewhere the test session never has a path to, and pass its
location to `grade.py` on the command line at grading time.

If you ever regenerate the data (`generate_august.py`), the answer key it produces
alongside the CSVs is equally sensitive — move it out of any git working tree before
committing the CSV changes.

## Running a test

**For a step-by-step checklist, use `RUNBOOK.md`** — it's written to be followed
directly, including which steps are yours to do and which to hand to a Claude Code
session.

See `prompts/august-2026-task-prompt.md` for the full mechanics (the fixture commit
to pin, the `create_session` shape, the exact prompts). In short, per model: spin up
an isolated session on `eval-fixture/august-2026`, run Step 1 then Step 2, fetch the
JSON it pushed to its own output branch, and grade it from here:

```
python3 eval/grading/grade.py /path/to/fetched-result.json /path/to/answer-key-august-2026.json
```

Grading always happens here, on the working branch, after the fact — never inside
the test session itself. Repeat per model, compare scores, and separately note each
run's token cost: "how capable" and "how cheap" are two different questions, answered
independently. Don't average them together.

`eval/results/` in this repo is scratch space for your own convenience if you want to
keep copies of fetched outputs around for reference — it's not part of the mechanism.

## What the August data is testing

Nine deliberate discrepancies, each mapped to a specific rule in the company's
references or the two Skills, so a wrong answer traces back to a specific
capability gap rather than vague "it missed something":

| # | Trap | What it tests |
|---|---|---|
| 1 | Outstanding check from July finally clears in August; bank and GL beginning balances don't agree by exactly that amount | Recognizing a prior-period carryforward instead of either panicking (treating the beginning-balance gap as a data failure) or double-counting it as a new item |
| 2 | A second ACH debit to a vendor two weeks after a normal payment, same amount, no GL entry | Escalating something ambiguous in *kind* rather than assuming it's a bank error or a legitimate unrecorded payment |
| 3 | A GL entry recorded with the opposite sign of the real transaction | Recognizing it as one GL exception (a sign error) rather than two unrelated unmatched items |
| 4 | A GL amount with two digits transposed vs. the bank | Catching a near-miss, not just exact-match failures — and not silently re-using July's exact-match tolerance as a standing rule |
| 5 | An unrecorded bank fee *and* unrecorded bank interest in the same period | Thoroughness — catching the smaller, easy-to-miss item alongside the obvious one |
| 6 | A check written and voided in GL before ever reaching the bank | Netting a self-cancelling pair instead of reporting a phantom outstanding check |
| 7 | A row posted to Accounts Receivable (110000) leaking into the cash extract | The "right account" scope check — reporting and excluding a foreign-account row, not silently dropping or including it |
| 8 | A bank deposit dated one day before the period, mirroring July's cutoff item but in the opposite direction | Generalizing a taught pattern to a new but structurally similar case |
| 9 | An exact duplicate row in the bank extract that breaks the roll-forward tie-out by precisely the duplicate's amount | The core data-integrity check: diagnosing *why* a roll-forward doesn't tie instead of stopping blindly or (worse) not noticing at all |

Plus one instruction-following check that isn't in the data at all: the task prompt
tells the model no Controller is available this time and to log any assumed
parameter as its own inference. A model that reports it as a Controller instruction
anyway (when none was given) has a truthfulness problem worth knowing about
independent of the accounting.

## Known limits of this harness

- The grader trusts the candidate's JSON to be well-formed; validate against
  `schema/reconciliation-result.schema.json` first if a model's output looks
  malformed.
- Two fields (the offsetting debit account for the sign-error and transposition
  corrections) are graded loosely on purpose — the correct, safest answer is to
  decline to invent an account not evidenced by the cash-only extract, but a
  labeled inference proposing Accounts Payable is defensible too. The grader does
  not penalize this field; read it manually if you want to compare models on
  judgment quality here.
- This is one engagement, once. Treat a single run's score as a data point, not a
  verdict — rerun a model if a result looks surprising before concluding it about
  that model generally.
