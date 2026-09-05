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

**5. Prior-period carryover disposition.** A table: each item carried over from the prior
period's reconciliation — its reconciling items and its list of what the Controller had to
act on — with its current-period status (cleared, still outstanding, posted, no effect) and
the evidence. State "none" explicitly if the prior period had none. Confirm here (or
cross-reference `source-population-validation`'s prior-period continuity check) that the
current beginning balances tie to the prior period's reported ending and, where the prior
adjustments were expected to post, to its adjusted balance — a gap is evidence a prior
proposed adjustment posted, even without direct confirmation of the posting itself.

**6. Matched activity.** State the matching basis explicitly — the tolerance and date
window used, and that they came from the Controller for this engagement. Show every match,
with any date difference displayed rather than smoothed over. **Every source row on both
sides appears exactly once** across the matched table and the reconciling items; say so.
State that no match was forced.

**7. Reconciling items.** A table: reference, side, date, description, amount,
classification, and the specific evidence supporting it. Classify per
`03 cash-reconciliation-policy.md` §6 — timing difference, requires GL adjustment,
requires counterparty investigation, or unresolved exception.

Then the reconciliation statement: each side's reported balance, its reconciling items,
its adjusted balance, and that the two adjusted balances agree. **Where the data genuinely
supports two readings of an item, present both readings with equal weight** — a full
reconciliation statement for each, not a full statement for one and a summary line for the
other — and avoid labeling one "primary" unless there's a stated basis for preferring it.
An asymmetric presentation privileges an answer the analysis hasn't actually settled.

**8. Proof against the raw difference.** Separate from the statement, and required:

```
unmatched items on side A  −  unmatched items on side B  =  the balance difference
residual unexplained difference = ____
```

State the residual explicitly, **including when it is zero**. This is the line that shows
nothing was plugged. If it is not zero, that residual is an unresolved exception — disclose
it, do not absorb it.

**9. Proposed adjustments.** Marked *proposed only — not posted*. Give account, account
name, debit/credit, a plain-language description, and the source row supporting it. State
that they require approval and are not reflected in any balance above. Where an item needs
no entry (a timing difference), say so rather than leaving it ambiguous.

**10. Unresolved exceptions.** Explicitly "none" if there are none. Do not omit the section.

**11. Open observations.** Things that do not change the reconciliation but that the
reviewer should know — an ambiguity you deliberately did not resolve, something that may
affect a later period. Give both readings and say why you did not choose between them.

**12. Escalation assessment.** The threshold applied and its source, then each item against
it with an escalated yes/no. Include items escalated for reasons other than amount.

**13. Conclusion.** Whether the account reconciles, in one sentence, with the figures. Then
a numbered list of **what the Controller must act on** — approvals needed, questions
answered, items to confirm in a later period. **If the conclusion depends on an assumption
or contingency that isn't confirmed, state the contingency in the same sentence as the
conclusion itself, not after it** — a reader who stops at the first sentence should not
come away more confident than the analysis actually supports.

**14. Judgment log.** A table of every judgment made: what was decided, on what basis, and
its **source of authority** — a company document with section, a Controller instruction
with date, or preparer inference. Label inferences as inferences. **When a judgment rests
on more than one source, attribute each part of the judgment to the specific source that
supports it** — don't cite two or three documents against a single compound claim as if
each supported all of it; a citation that covers only half the claim and is presented as
covering the whole thing overclaims.

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
- Before finishing, check the workpaper against every numbered section above, in order. A
  required section whose content is scattered across other sections instead of gathered in
  its own place does not count as present — a reviewer looking for it should find an actual
  section, not have to reconstruct one from mentions elsewhere.
