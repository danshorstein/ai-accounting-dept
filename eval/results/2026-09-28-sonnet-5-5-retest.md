# Retest — retrained workpaper skill, Sonnet 5.5, 2026-09-28

Purpose: confirm the two defects found in the first August workpaper are fixed by the
retrained `reconciliation-workpaper-construction` skill (commit `cb070ea`).
Agent file unchanged. Fixture: `eval-fixture/august-2026-v2` @ `14a8edb`.

| Stage | Branch | Commit | Outcome |
|---|---|---|---|
| 1 | `eval-run/sonnet-5-5-retest-20260928` | `47ba57f` | Halted at the bank roll-forward gate (3,300.00), no matching, no adjustments |
| 2 (after scripted Controller reply) | `eval-run/sonnet-5-5-retest-20260928-resume` | `3f71c5d` | Completed, residual 0.00 |

Model: `claude-sonnet-5-5`. Reasoning level was not set for these sessions (the first August
run used extra-high), so the two scores are not strictly comparable.

## Defect 1 — unresolved readings: FIXED

Delta payment (B13): previously classified as a GL error and AJE-3 drafted under it.
Now classified `unresolved_exception`, entry drafted only as **conditional** (AJE-C1,
"posts only if the Controller determines ..."), and the reconciliation statement shows
all four reading combinations side by side, with the sentence "No reading is presented
as primary." The conclusion is stated under each reading.

Side effect to watch: the 27.00 transposition (B08/G10) is also held open under two
readings. It is conditional and disclosed, so it obeys the new rule, but it is more
hedged than the answer key, which treats it as a GL error.

## Defect 2 — retained script: FIXED (one minor nit)

- No absolute paths; runs from the repository root and exits 0 (verified).
- July balances are read from the July source CSVs, not hardcoded.
- No dead or placeholder code; prints the residual the workpaper cites.
- Nit: one July-derived literal, `D("-35.00")`, sits in the logic (the July bank-fee
  amount, used to test whether it appears in August GL). Should be a labelled, cited
  constant. Not enough to re-edit the skill for one instance.

## Grader (stage 2 workpaper, mapped to the schema by hand)

**87 / 94 (92.6%).** Lost points: 1 cutoff-finding vocabulary; 3 on the transposition item
(hedged, see above); 2 on the Delta classification (`unresolved_exception` vs the key's
`bank_exception`; its proposed-adjustment field now matches the key); 1 for escalating the
voided-check pair. The candidate JSON was built by hand from the workpaper, not produced
by the model in a Step 2 translation.

## Harness finding

The agent halts at the duplicate-row gate even when told no Controller is available. That
is correct under its own rules, so a one-shot harness run can never complete. The runbook
now uses a two-stage protocol with a scripted Controller reply (Step 1b).
