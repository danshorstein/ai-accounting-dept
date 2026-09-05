---
name: source-population-validation
description: Prove that source data populations are complete, in scope, and internally consistent before comparing or reconciling them. Use before any reconciliation, tie-out, or two-population comparison — bank to GL, subledger to GL, aging to control account — and whenever asked whether a data set can be relied on.
---

# Source Population Validation

Establish that each population is complete and in scope **on its own** before comparing it
to anything. Without this, a difference found later cannot be distinguished from data that
was simply missing rows.

Do all of it before matching, comparing, or reconciling.

## 1. Scope checks

For each population, confirm and record:

- **Right account.** Every row belongs to the account under reconciliation. Report any
  foreign account appearing in the population; do not silently filter it out.
- **Right period.** Every row falls in the period. Report any row that does not — an
  out-of-period row inside in-period totals is a finding, not something to drop.
- **Right entity/source.** The file is what it claims to be.
- **Sign convention.** Confirm it, and state it. Do not assume debits, credits, inflows,
  or outflows carry a particular sign.

## 2. Roll-forward proof

For each side independently:

```
beginning balance + sum of transaction detail = reported ending balance
```

Take the beginning and ending balances from the summary or trial balance — a reported
figure, not one you derived — and the activity from the transaction detail. Present it as
a table showing beginning balance, total activity with row count, calculated ending
balance, reported ending balance, and the difference, with a source named for each figure.

Where an independent net-activity figure exists (for example a trial balance's
debits/credits net), tie the detail to it as well.

**A difference of zero is the pass condition.** State it explicitly; do not omit the line
because it is zero.

### Prior-period continuity

Where a prior period's reconciliation exists, the roll-forward proof isn't complete at the
current period's own beginning balance — carry it one step further back. Confirm the
current period's beginning balance ties to **both**:

- the prior period's reported ending balance (from that period's summary or trial
  balance), and
- the prior reconciliation's *adjusted* balance, if its proposed adjustments were expected
  to post before this period began.

A gap between the two — the beginning balance matching the prior period's adjusted figure
rather than its raw reported one, for instance — is itself evidence: it indicates a prior
proposed adjustment was approved and posted, even without a direct posting confirmation in
the current period's source data. Say so, and say what it implies, rather than treating the
tie-out as done once the current period's own numbers agree with each other.

## 3. Integrity checks

- Row counts for each file
- Actual date range versus expected period
- Duplicate rows on date + amount + description
- Zero, blank, or non-numeric amounts
- Beginning balances of the two sides compared — a difference means a prior-period item is
  carrying forward and changes how the current period's difference is read

## 4. Disposition

**If every side ties:** state the conclusion — the detail fully explains each side's
beginning-to-ending balance change, so the populations are a valid basis for comparison —
and continue. This is a data-quality gate, not an approval checkpoint; it does not require
sign-off to pass.

**If any side does not tie:** stop. Do not begin matching. Report which side failed, by
how much, and what you checked. A population that does not tie is either incomplete or
inconsistent with its own summary, and reconciling against it produces a result nobody can
rely on. Escalate for direction.

**If a scope or integrity check surfaces something odd but everything still ties**, carry
it forward as a disclosed observation rather than resolving it. An out-of-period row that
nonetheless keeps the population in balance is exactly this case: it does not break the
reconciliation, and it is still worth the reviewer's attention.

## 5. Retention

The tie-out proofs are **evidence and belong in the finished workpaper**, not a preliminary
check discarded once passed. A reviewer needs to see that completeness was established, not
be told that it was.
