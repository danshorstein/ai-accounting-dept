# Operating Cash Reconciliation — July 2026

| | |
|---|---|
| **Entity** | Riverton Sporting Goods, Inc. |
| **GL account** | 101000 — Operating Cash |
| **Bank account** | Operating Checking |
| **Period** | 2026-07 (2026-07-01 through 2026-07-31) |
| **Prepared by** | Staff Accountant (Claude) |
| **Date prepared** | 2026-08-22 |
| **Reviewed by** | _________________ (Controller) |
| **Date reviewed** | _________________ |
| **Review outcome** | ☐ Approved  ☐ Returned with questions/corrections |

Prepared under `03 cash-reconciliation-policy.md` and `04 bank-reconciliation-procedure.md`. Submitted for independent review under `05 independent-review-control.md`. The preparer has not approved this work.

---

## 1. Sources used

| File | Content | Rows |
|---|---|---:|
| `data/july-2026-bank.csv` | Bank transaction detail (date, description, amount) | 10 |
| `data/july-2026-bank-summary.csv` | Bank beginning/ending balance, Operating Checking, 2026-07 | 1 |
| `data/july-2026-gl-cash.csv` | GL cash detail (date, description, amount, account) | 10 |
| `data/july-2026-trial-balance.csv` | TB beginning balance, net activity, ending balance, account 101000 | 1 |

Account and period confirmed (procedure §1): the bank file covers Operating Checking for 2026-07; every GL detail row is posted to account 101000 and no other account appears in the population.

## 2. Balances to be reconciled

| | Bank | GL 101000 |
|---|---:|---:|
| Beginning balance | 50,000.00 | 50,000.00 |
| Net July activity | 24,060.00 | 23,475.00 |
| Ending balance | 74,060.00 | 73,475.00 |

Beginning balances agree exactly, so no prior-period reconciling item is carried forward. The difference to be explained is **74,060.00 − 73,475.00 = 585.00**.

## 3. Population completeness — roll-forward proofs

### Bank roll-forward

| Item | Amount | Source |
|---|---:|---|
| Beginning balance | 50,000.00 | `july-2026-bank-summary.csv` |
| Total July bank activity (10 rows) | 24,060.00 | `july-2026-bank.csv` |
| **Calculated ending balance** | **74,060.00** | computed |
| Reported ending balance | 74,060.00 | `july-2026-bank-summary.csv` |
| **Difference** | **0.00** | — |

### GL roll-forward

| Item | Amount | Source |
|---|---:|---|
| Beginning balance per TB | 50,000.00 | `july-2026-trial-balance.csv` |
| Total GL activity (10 rows) | 23,475.00 | `july-2026-gl-cash.csv` |
| **Calculated ending balance** | **73,475.00** | computed |
| Reported TB ending balance | 73,475.00 | `july-2026-trial-balance.csv` |
| **Difference** | **0.00** | — |

The GL detail sum also agrees exactly to the TB `debits_credits_net` of 23,475.00 (difference 0.00).

### Other completeness and integrity checks

- Bank file: all 10 rows dated within 2026-07-01 to 2026-07-31.
- GL file: all 10 rows posted to 101000; **one row dated 2026-08-01** is included in July TB activity — see reconciling item T-2 and the cutoff observation in §6.
- No duplicate date/amount/description combinations on either side; no zero or non-numeric amounts.

**Conclusion:** both populations are complete and internally consistent — the transaction detail fully explains each side's beginning-to-ending balance change with no unexplained roll-forward variance. The detail is a valid basis for transaction-level matching.

## 4. Matched activity

Matching basis: **exact amount, with a date window of up to 5 days**, description used as corroborating evidence. Nine of ten bank items and nine of ten GL items matched.

| # | Bank date | Bank description | Bank amount | GL date | GL description | GL amount | Date gap |
|---:|---|---|---:|---|---|---:|---:|
| 1 | 2026-07-02 | Customer deposit A | 12,500.00 | 2026-07-02 | AR receipt A | 12,500.00 | 0 |
| 2 | 2026-07-03 | ACH Vendor Alpha | (3,250.00) | 2026-07-03 | Vendor Alpha payment | (3,250.00) | 0 |
| 3 | 2026-07-07 | Customer deposit B | 8,400.00 | 2026-07-07 | AR receipt B | 8,400.00 | 0 |
| 4 | 2026-07-10 | ACH Vendor Beta | (4,725.00) | 2026-07-10 | Vendor Beta payment | (4,725.00) | 0 |
| 5 | 2026-07-14 | Customer deposit C | 6,650.00 | 2026-07-14 | AR receipt C | 6,650.00 | 0 |
| 6 | 2026-07-16 | Payroll | (9,800.00) | 2026-07-16 | Payroll run | (9,800.00) | 0 |
| 7 | 2026-07-21 | Customer deposit D | 9,100.00 | 2026-07-21 | AR receipt D | 9,100.00 | 0 |
| 8 | 2026-07-24 | ACH Vendor Gamma | (2,180.00) | 2026-07-24 | Vendor Gamma payment | (2,180.00) | 0 |
| 9 | 2026-07-31 | Customer deposit E | 7,400.00 | 2026-08-01 | AR receipt E | 7,400.00 | **1** |
| | | **Total matched** | **24,095.00** | | | **24,095.00** | |

Item 9 has a one-day date difference, within the approved 5-day window, and is matched on exact amount and corroborating description. Because both sides fall in the same reconciled period totals, it is not a reconciling item — but the GL posting date is in the next fiscal month, which is disclosed as a cutoff observation in §6.

No match was forced. Every bank row and every GL row appears exactly once — either above or in §5.

## 5. Reconciling items

| Ref | Side | Date | Description | Amount | Classification | Support |
|---|---|---|---|---:|---|---|
| T-1 | GL only | 2026-07-30 | Check 1048 — Office Supply Co | (620.00) | **Timing difference** — outstanding check | GL detail row; no corresponding bank clearing in July bank activity |
| T-2 | Bank only | 2026-07-29 | Bank service charge | (35.00) | **GL exception** — unrecorded bank fee, requires GL adjustment | Bank detail row; no corresponding GL entry in July GL cash detail |

### Reconciliation statement

| | Amount |
|---|---:|
| **Balance per bank, 2026-07-31** | **74,060.00** |
| Less: outstanding check — Check 1048 (T-1) | (620.00) |
| **Adjusted bank balance** | **73,440.00** |
| | |
| **Balance per GL 101000, 2026-07-31** | **73,475.00** |
| Less: unrecorded bank service charge (T-2) | (35.00) |
| **Adjusted book balance** | **73,440.00** |
| | |
| **Difference** | **0.00** |

### Proof against the raw difference

| | Amount |
|---|---:|
| Bank ending less GL ending | 585.00 |
| Unmatched bank items less unmatched GL items: (35.00) − (620.00) | 585.00 |
| **Residual unexplained difference** | **0.00** |

The full 585.00 difference is explained by supported transaction-level items. Nothing was plugged, forced, or assumed.

## 6. Cutoff observation (disclosure, not a reconciling item)

GL row "AR receipt E" is dated **2026-08-01** but is included in the July trial-balance net activity of 23,475.00. The corresponding bank deposit cleared 2026-07-31. Two readings are possible from the data alone — a posting-date convention that differs from the effective date, or a genuine cutoff error in which an August-dated entry was captured in July.

I cannot determine which from the available data, and the answer does not change the July reconciliation: the item is in both the July bank population and the July GL population, so the account reconciles either way. It is raised for Controller awareness because it could affect August cutoff testing and the GL posting-date convention. **No adjustment is proposed for it.**

## 7. Proposed general-ledger adjustment

**Proposed only — not posted, and not assumed into any balance above.** Requires Controller approval.

| Ref | Account | Account name | Debit | Credit |
|---|---|---|---:|---:|
| AJE-1 | 620000 | Bank Fees | 35.00 | |
| AJE-1 | 101000 | Operating Cash | | 35.00 |

*To record the July 2026 bank service charge of 35.00 assessed 2026-07-29, per the bank transaction detail, not previously recorded in the general ledger.*

Support: `data/july-2026-bank.csv`, row dated 2026-07-29, "Bank service charge", (35.00). Account 620000 Bank Fees selected per the chart of accounts in `01 company-profile.md`. No adjustment is proposed for T-1 — an outstanding check is a timing difference requiring no GL entry.

## 8. Unresolved exceptions

**None.** Both reconciling items are supported by source evidence and classified. There is no unexplained residual difference.

The cutoff observation in §6 is an open question for the Controller, not an unresolved reconciling item.

## 9. Escalation assessment

Threshold applied: **$5,000 for unresolved variances** (set by the Controller for this engagement).

| Item | Amount | Unresolved? | Escalated? |
|---|---:|---|---|
| T-1 outstanding check | 620.00 | No — supported timing difference | No |
| T-2 unrecorded bank fee | 35.00 | No — supported, adjustment proposed | No |
| Unexplained residual | 0.00 | — | No |

No item meets the escalation threshold. The §6 cutoff observation is surfaced to the Controller as a judgment matter regardless of amount.

## 10. Conclusion

**Account 101000 Operating Cash reconciles for July 2026.** The 585.00 difference between the bank ending balance of 74,060.00 and the GL ending balance of 73,475.00 is fully explained by one outstanding check (620.00) and one unrecorded bank service charge (35.00), both supported by source evidence. Adjusted bank and adjusted book balances both equal 73,440.00.

Open for Controller action:
1. Approve or reject proposed adjustment AJE-1 (35.00 bank fee to 620000).
2. Respond to the cutoff observation in §6 regarding the 2026-08-01 GL posting date.
3. Confirm Check 1048 clears in the August bank activity as part of the August reconciliation.

## 11. Judgment log

| # | Judgment | Basis | Source of authority |
|---:|---|---|---|
| J-1 | Matching tolerance: exact amount only, date window up to 5 days | Applied as instructed for this exercise; **not adopted as a standing rule** | Controller instruction, 2026-08-22 |
| J-2 | Escalation threshold: $5,000 for unresolved variances | Applied as instructed for this exercise | Controller instruction, 2026-08-22 |
| J-3 | Every unmatched item investigated and disclosed regardless of amount | No company materiality threshold is defined; policy §3 and §6 require identification and classification of all reconciling items | `03` §3, §6 |
| J-4 | T-1 classified as a timing difference (outstanding check) rather than a GL exception | Check was written and recorded 2026-07-30 with no bank clearing in the July population; consistent with normal check float | Preparer inference, stated as such |
| J-5 | T-2 classified as a GL exception requiring adjustment, coded to 620000 Bank Fees | Bank-assessed service charge present on bank side only; account selected from chart of accounts | `04` §4; `01` chart of accounts |
| J-6 | Item 9 matched despite a one-day date difference | Exact amount, corroborating description, within the approved 5-day window | J-1 |
| J-7 | 2026-08-01 GL posting date disclosed as an observation rather than resolved | The data does not distinguish a posting-date convention from a cutoff error; policy §4 prohibits resolving by assumption | `03` §4; CLAUDE.md "nothing is assumed" |
| J-8 | No adjustment proposed for the §6 observation and no residual plugged | Insufficient support to conclude; unresolved matters are disclosed, not forced | `03` §4; `04` §4 |

---

*Prepared by the Staff Accountant. Not effective until independently reviewed and approved by the Controller per `05 independent-review-control.md`.*
