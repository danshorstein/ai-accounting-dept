# Bank Reconciliation Procedure — PROPOSED REVISION

> **Status: proposed revision — not yet approved.**
> `04 bank-reconciliation-procedure.md` remains authoritative until the Controller
> approves this document. Drafted 2026-08-22 following the July 2026 operating cash
> reconciliation training exercise.
>
> **What changed from `04`:**
> 1. New step 2 — validate source population completeness before comparing activity.
>    Prior steps 2–6 renumbered to 3–7.
> 2. Step 6 (workpaper contents) expanded to require the completeness proofs, a
>    residual-difference proof, an escalation assessment, and a judgment log.
> 3. Closing "Judgment" section now states how tolerances and thresholds are supplied and
>    recorded, without prescribing any values.
>
> No matching tolerance, date window, materiality level, or escalation threshold is
> established by this revision. That remains deliberately undefined.

## Objective

Prepare a complete and supportable monthly reconciliation of the Operating Cash account.

## Procedure

### 1. Obtain source data

Obtain the bank activity for the month and the general-ledger detail for the related cash
account.

Confirm that the correct account and accounting period are being reviewed.

### 2. Validate source population completeness

Before comparing bank and book activity, establish that each population is complete and in
scope on its own.

For each side independently, confirm that the beginning balance plus the transaction detail
equals the reported ending balance. Take beginning and ending balances from the bank
summary and the trial balance; take activity from the transaction detail.

Also confirm that every detail row belongs to the account and period under reconciliation,
and check the data for duplicates, out-of-range dates, and missing or non-numeric amounts.
Compare the two beginning balances — a difference indicates a prior-period reconciling item
carrying forward.

**If a side does not tie, stop.** Do not begin matching. Report which side failed, by how
much, and escalate for direction. A reconciliation performed against a population that does
not tie cannot be relied on.

If every side ties, continue. This step is a data-quality gate, not an approval checkpoint;
passing it does not require sign-off.

Retain the completeness proofs — they are evidence and belong in the workpaper.

### 3. Compare bank and book activity

Compare bank transactions to general-ledger activity.

Identify transactions that appear to correspond and distinguish them from items that remain
unmatched.

Do not force a match merely because doing so would make the reconciliation balance.

### 4. Investigate unmatched items

Review unmatched bank and general-ledger items.

Determine whether each item appears to be:

- a timing difference;
- a bank-side exception;
- a general-ledger exception;
- an item requiring additional research.

Document the reasoning for significant or unusual conclusions.

### 5. Identify required adjustments

Identify items that appear to require a general-ledger adjustment, such as bank fees that
have not yet been recorded.

Do not post or assume an adjustment without sufficient support.

### 6. Prepare the reconciliation workpaper

Prepare a workpaper that clearly presents:

- the bank-side information reviewed;
- the general-ledger information reviewed;
- the source population completeness proofs from step 2;
- matched activity, and the matching basis applied;
- reconciling items;
- a proof that the unmatched items fully explain the difference between the two ending
  balances, stating the residual explicitly — including when the residual is zero;
- unresolved exceptions;
- any proposed general-ledger adjustments, identified as proposed and not posted;
- an assessment of each item against the escalation threshold in effect for the engagement;
- a log of the judgments made, each with its basis and its source of authority;
- the overall conclusion.

The workpaper should be understandable to an independent reviewer without requiring them to
recreate the preparer's analysis.

### 7. Submit for review

Submit the completed reconciliation and supporting evidence for independent review.

Address reviewer questions or requested corrections before the reconciliation is considered
complete.

## Judgment

This procedure intentionally does not prescribe every matching tolerance, materiality
threshold, or escalation rule. Those expectations may be established through training and
company practice.

Where a reconciliation requires such a parameter, the preparer obtains it from the
Controller for that engagement and records it in the workpaper's judgment log, together
with its date and the fact that the Controller supplied it. A parameter supplied for one
reconciliation is not a standing rule and is not carried forward to another without being
established as company practice. The preparer does not adopt a parameter that was not given
to them.
