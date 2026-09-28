---
name: reconciliation-workpaper-construction
description: Structure a reconciliation workpaper so an independent reviewer can test it without recreating the preparer's analysis — sources, tie-out proofs, matched detail, classified reconciling items, proposed (not posted) adjustments, disclosed open items, escalation assessment, conclusion, and judgment log. Use when preparing or reviewing any account reconciliation workpaper.
---

# Reconciliation Workpaper Construction

The standard the workpaper has to meet: **an independent reviewer can test every
conclusion without redoing the work.** Everything below serves that. When in doubt, show
the proof rather than assert the result.

Write to `workpapers/<period> <subject>.md`.

## Required sections

**1. Header.** Entity, account under reconciliation (GL and counterparty), period,
preparer, date prepared, and a **blank reviewer block** — reviewer name, date, and outcome
(approved / returned with questions). State that the work is not effective until
independently reviewed. Never fill in the reviewer block yourself.

**2. Sources used.** Every file, what it contains, and its row count. A reviewer must be
able to confirm you looked at the right things and all of them.

**3. Balances to be reconciled.** Both sides' beginning and ending balances, and the
difference to be explained, stated as a number up front. Note whether beginning balances
agree — if they do not, a prior-period item is carrying forward.

**4. Population completeness.** The roll-forward proofs and integrity checks, retained in
full. See the `source-population-validation` skill.

**5. Matched activity.** State the matching basis explicitly — the tolerance and date
window used, and that they came from the Controller for this engagement. Show every match,
with any date difference displayed rather than smoothed over. **Every source row on both
sides appears exactly once** across the matched table and the reconciling items; say so.
State that no match was forced.

**6. Reconciling items.** A table: reference, side, date, description, amount,
classification, and the specific evidence supporting it. Classify per
`03 cash-reconciliation-policy.md` §6 — timing difference, requires GL adjustment,
requires counterparty investigation, or unresolved exception.

Then the reconciliation statement: each side's reported balance, its reconciling items,
its adjusted balance, and that the two adjusted balances agree.

**7. Proof against the raw difference.** Separate from the statement, and required:

```
unmatched items on side A  −  unmatched items on side B  =  the balance difference
residual unexplained difference = ____
```

State the residual explicitly, **including when it is zero**. This is the line that shows
nothing was plugged. If it is not zero, that residual is an unresolved exception — disclose
it, do not absorb it.

**8. Proposed adjustments.** Marked *proposed only — not posted*. Give account, account
name, debit/credit, a plain-language description, and the source row supporting it. State
that they require approval and are not reflected in any balance above. Where an item needs
no entry (a timing difference), say so rather than leaving it ambiguous.

**Where an item has two supportable readings you have not resolved (§10), no single
entry is "the" proposal.** Draft each entry under the reading that would require it and
label it *conditional — posts only if the Controller determines <reading>*. Do not draft
an entry for a reading you have said the data cannot choose between, and do not present
one reading as "primary" in the reconciliation statement (§6): show the statement under
each reading side by side. Entries that do not depend on any open reading are presented
normally.

**9. Unresolved exceptions.** Explicitly "none" if there are none. Do not omit the section.

**10. Open observations.** Things that do not change the reconciliation but that the
reviewer should know — an ambiguity you deliberately did not resolve, something that may
affect a later period. Give both readings and say why you did not choose between them.

**11. Escalation assessment.** The threshold applied and its source, then each item against
it with an escalated yes/no. Include items escalated for reasons other than amount.

**12. Conclusion.** Whether the account reconciles, in one sentence, with the figures —
under each open reading if §8 applies, not under a chosen one. Then
a numbered list of **what the Controller must act on** — approvals needed, questions
answered, items to confirm in a later period.

**13. Judgment log.** A table of every judgment made: what was decided, on what basis, and
its **source of authority** — a company document with section, a Controller instruction
with date, or preparer inference. Label inferences as inferences.

This section is what makes the workpaper reviewable rather than merely readable. A reviewer
disagreeing with a conclusion needs to find the reasoning without reverse-engineering it
from the numbers. Parameters the Controller supplied are logged here, scoped to this
engagement — not adopted as standing rules.

## Discipline

- Every figure traces to a named source file and row, or to a computation shown on the page.
- Show zero-difference proofs; a passed check is evidence.
- Prefer the disclosed open question to the tidy resolution.
- Present, do not summarize away: if a reviewer would have to recompute it to trust it, it
  belongs on the page.

## Retained calculation scripts

A script that produced the workpaper's figures is evidence, held to the same standard as
the workpaper: a reviewer must be able to run it and reproduce the page.

- Save it beside the workpaper as `workpapers/<period> <subject>.py`, and say in the
  workpaper how to run it.
- Locate inputs by path **relative to the repository root**. Never an absolute path on the
  preparer's machine.
- Read prior-period figures (opening balances, carryover items) from the prior-period
  source files. Where a figure exists only in a prior workpaper, hardcode it once, in a
  labelled constant that names its source, and list it in the workpaper as an input taken
  from that source. Never let a prior-period number sit uncited in the logic, where it
  goes stale silently when the script is reused.
- No dead, placeholder, or commented-out code.
- Print every figure the workpaper cites, so a reviewer can compare line for line.
