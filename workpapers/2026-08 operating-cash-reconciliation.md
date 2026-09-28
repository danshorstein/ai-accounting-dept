# Operating Cash Reconciliation — August 2026

**STATUS: Reconciliation performed on the Controller-directed population (bank row B10 set aside). Prepared, not approved. Open items and escalations in sections 9, 11 and 12.**

| | |
|---|---|
| **Entity** | Riverton Sporting Goods, Inc. |
| **GL account** | 101000 — Operating Cash |
| **Bank account** | Operating Checking |
| **Period** | 2026-08 (2026-08-01 through 2026-08-31) |
| **Prepared by** | Staff Accountant (Claude) |
| **Date prepared** | 2026-09-28 (initial halted draft and this completed version, same date) |
| **Reviewed by** | _________________ (Controller) |
| **Date reviewed** | _________________ |
| **Review outcome** | ☐ Approved  ☐ Returned with questions/corrections |

Prepared under `03 cash-reconciliation-policy.md` and `04 bank-reconciliation-procedure.md`, using the `source-population-validation` and `reconciliation-workpaper-construction` skills. **This work is not effective until independently reviewed by the Controller under `05 independent-review-control.md`. The preparer has not approved it.** Reference `04a` is a proposed revision, not an approved document, and is not relied on for authority.

**Calculation script:** `workpapers/2026-08 operating-cash-reconciliation.py`. Run from the repository root with `python3 "workpapers/2026-08 operating-cash-reconciliation.py"`. It prints every figure cited below. All inputs are read from `data/` by relative path, including July figures. No figure is taken only from a prior workpaper; the July classifications (check 1048, service charge) are recomputed by the script from the July source files and then compared to the July workpaper (section 4).

**How the first draft changed.** The first version of this workpaper halted at the population gate because the bank roll-forward failed by 3,300.00. The Controller reviewed it and directed the work below. Section 4 keeps the failed proof in full and adds the proof after the Controller-directed exclusion.

---

## 1. Sources used

| File | Content | Rows |
|---|---|---:|
| `data/august-2026-bank.csv` | Bank transaction detail (id, date, description, amount) | 17 (16 after B10 set aside) |
| `data/august-2026-bank-summary.csv` | Bank beginning/ending balance, Operating Checking, 2026-08 | 1 |
| `data/august-2026-gl-cash.csv` | GL cash detail (id, date, description, amount, account) | 15 (14 in account 101000) |
| `data/august-2026-trial-balance.csv` | TB beginning, net activity, ending, account 101000, 2026-08 | 1 |
| `data/july-2026-bank-summary.csv`, `data/july-2026-trial-balance.csv` | July ending balances, for the continuity check | 1 each |
| `data/july-2026-bank.csv`, `data/july-2026-gl-cash.csv` | July detail, to confirm the carryover items | 10 each |
| `workpapers/2026-07 operating-cash-reconciliation.md` | July workpaper (T-1, T-2, AJE-1), compared to the script's recomputation | — |

Sign convention (confirmed from the data): inflows are positive and outflows negative on both sides, with one exception noted at G09 (section 6).

## 2. Balances to be reconciled

| | Bank | GL 101000 |
|---|---:|---:|
| Beginning balance, 2026-08-01 | 74,060.00 | 73,440.00 |
| Ending balance (reported) | 78,659.75 | 85,384.00 |

**Difference to be explained: bank less GL = (6,724.25).** Beginning balances **do not agree**: bank exceeds GL by 620.00, so a prior-period item carries forward. It is identified in section 4 as July's outstanding check 1048.

## 3. Engagement parameters and Controller direction

Given by the Controller for **this engagement only**. They are not standing rules and must not be carried into another period.

- Matching tolerance: exact amount ($0.00).
- Date window: 5 days.
- Escalation threshold: $200.00.
- **Materiality: no figure was specified and none is used.** Every unmatched item is investigated and disclosed regardless of amount.
- Bank row B10 is set aside as a likely data-quality artifact. It is kept disclosed as an integrity finding and escalated.
- Verify roll-forward continuity from July, and confirm the July carryover items against the July workpaper.

## 4. Population completeness

### 4a. Bank roll-forward as delivered (17 rows) — FAILS (retained from the first draft)

| Item | Amount | Source |
|---|---:|---|
| Beginning balance | 74,060.00 | `august-2026-bank-summary.csv` |
| Total activity (17 rows) | 7,899.75 | `august-2026-bank.csv`, B01–B17 |
| Calculated ending balance | 81,959.75 | computed |
| Reported ending balance | 78,659.75 | `august-2026-bank-summary.csv` |
| **Difference** | **3,300.00** | |

### 4b. Bank roll-forward after setting aside B10 (16 rows) — passes

| Item | Amount | Source |
|---|---:|---|
| Beginning balance | 74,060.00 | `august-2026-bank-summary.csv` |
| Total activity (16 rows, B10 excluded) | 4,599.75 | `august-2026-bank.csv`, B01–B09, B11–B17 |
| Calculated ending balance | 78,659.75 | computed |
| Reported ending balance | 78,659.75 | `august-2026-bank-summary.csv` |
| **Difference** | **0.00** | pass |

**Caveat.** This pass is the result of the Controller-directed exclusion. The tie is consistent with B10 being a duplicated row, but it does not prove that. The alternative is that B10 is a genuine deposit and the summary or extract is wrong in some other way, with the equal amount a coincidence. I followed the direction and did not decide between these. B10 stays out of every table in sections 6 to 8 and is disclosed as an integrity finding (section 9, item 1).

### 4c. GL roll-forward — passes

| Item | Amount | Source |
|---|---:|---|
| Beginning balance per TB | 73,440.00 | `august-2026-trial-balance.csv` |
| Total activity, account 101000 rows (14 of 15 rows) | 11,944.00 | `august-2026-gl-cash.csv`, all rows except G08 |
| Calculated ending balance | 85,384.00 | computed |
| Reported TB ending balance | 85,384.00 | `august-2026-trial-balance.csv` |
| **Difference** | **0.00** | pass |

The 101000 detail ties to the TB `debits_credits_net` of 11,944.00 (difference 0.00). Including G08 would give an ending of 84,134.00, which is (1,250.00) from the TB. The TB therefore excludes G08.

### 4d. Scope and integrity checks

| Check | Result |
|---|---|
| Row counts | Bank 17; GL 15 |
| Date range | Bank 2026-07-31 to 2026-08-29; GL 2026-08-01 to 2026-08-27 |
| Out-of-period rows | **Bank B01, 2026-07-31, "Customer deposit J", 2,600.00.** It is not in `july-2026-bank.csv`. See section 10, item 2. |
| Foreign-account rows | **GL G08, 2026-08-11, "AR write-off - Bright Retailers", (1,250.00), account 110000.** Not cash. It is excluded from the 101000 population and from the TB net, and disclosed. |
| Duplicates on date + amount + description | **Bank B09 and B10, 2026-08-15, "Customer deposit K", 3,300.00.** B10 is set aside per the Controller. Only one GL entry (G11) exists. |
| Same description and amount on different dates | B05 (2026-08-06) and B13 (2026-08-20), "ACH Vendor Delta", (1,845.00). Not duplicates. See B13 in section 6. |
| Zero, blank or non-numeric amounts | None |

### 4e. Continuity from July and confirmation of July carryover items

| Check | Figures | Result |
|---|---|---|
| Bank: July ending vs August beginning | 74,060.00 vs 74,060.00 | Difference 0.00. Ties. |
| GL: July TB ending vs August TB beginning | 73,475.00 vs 73,440.00 | **Difference (35.00). Does not tie.** |
| July items recomputed from July source files by the script (exact amount, 5-day window) | GL only: 2026-07-30 Check 1048 (620.00). Bank only: 2026-07-29 Bank service charge (35.00). | Agrees to July workpaper T-1 and T-2. July difference 585.00 = (35.00) − (620.00). |
| July adjusted bank balance | 74,060.00 − 620.00 = 73,440.00 | Agrees to July workpaper statement. |
| July adjusted book balance | 73,475.00 − 35.00 = 73,440.00 | Agrees to July workpaper statement. |
| August GL beginning vs July adjusted book balance | 73,440.00 vs 73,440.00 | Difference 0.00 |
| August opening difference vs July outstanding check | 620.00 vs (620.00) | Residual 0.00. The opening difference is entirely July T-1. |
| July check 1048 clearing | B03, 2026-08-04, "Check 1048 - Office Supply Co", (620.00); July GL date 2026-07-30 | Exact amount, 5-day gap (the window's outer limit, inclusive). T-1 cleared in August, as July item 3 asked to be confirmed. |
| July fee (35.00) in August GL detail | Not present | See below. |

**The (35.00) GL continuity break.** The August TB opens at July's adjusted book balance, not July's reported TB ending balance. The difference equals July's proposed AJE-1 (35.00 bank fee). Two readings exist, and I resolve neither. (A) AJE-1 was approved and posted to July after the July TB was produced. The August opening then fits July's adjusted figures exactly. (B) The opening balance moved for some other reason that happens to equal 35.00. I have no evidence of Controller approval or posting of AJE-1, and the August GL detail has no 35.00 entry. I did not carry AJE-1 into any August balance. Under either reading the August reconciliation is unaffected, because it uses the reported August TB. The question of whether AJE-1 was posted is for the Controller.

**Disposition of the gate.** Bank (after the directed exclusion) and GL both tie. The detail explains each side's beginning-to-ending change, so matching proceeded.

## 5. Matched activity

Basis: **exact amount ($0.00 tolerance), date window 5 days, both set by the Controller for this engagement (section 3).** Descriptions were used as corroboration. No match was forced. Each pairing was re-tested in the script and would fail the run if it broke either test.

| # | Bank | Bank date | Bank description | Bank amount | GL | GL date | GL description | GL amount | Date gap (days) |
|---:|---|---|---|---:|---|---|---|---:|---:|
| 1 | B01 | 2026-07-31 | Customer deposit J | 2,600.00 | G02 | 2026-08-01 | AR receipt J | 2,600.00 | **1** |
| 2 | B02 | 2026-08-01 | Customer deposit F | 5,200.00 | G01 | 2026-08-01 | AR receipt F | 5,200.00 | 0 |
| 3 | B04 | 2026-08-05 | ACH Vendor Alpha | (3,410.00) | G03 | 2026-08-05 | Vendor Alpha payment | (3,410.00) | 0 |
| 4 | B05 | 2026-08-06 | ACH Vendor Delta | (1,845.00) | G05 | 2026-08-06 | Vendor Delta payment | (1,845.00) | 0 |
| 5 | B06 | 2026-08-09 | Customer deposit G | 7,850.00 | G07 | 2026-08-09 | AR receipt G | 7,850.00 | 0 |
| 6 | B09 | 2026-08-15 | Customer deposit K | 3,300.00 | G11 | 2026-08-15 | AR receipt K | 3,300.00 | 0 |
| 7 | B11 | 2026-08-15 | Payroll | (10,200.00) | G12 | 2026-08-15 | Payroll run | (10,200.00) | 0 |
| 8 | B12 | 2026-08-18 | Customer deposit H | 6,300.00 | G13 | 2026-08-18 | AR receipt H | 6,300.00 | 0 |
| 9 | B14 | 2026-08-22 | ACH Vendor Beta | (2,975.00) | G14 | 2026-08-22 | Vendor Beta payment | (2,975.00) | 0 |
| 10 | B15 | 2026-08-27 | Customer deposit I | 8,150.00 | G15 | 2026-08-27 | AR receipt I | 8,150.00 | 0 |
| | | | **Total matched** | **14,970.00** | | | | **14,970.00** | |

Pair 6 matches G11 to B09 only. B10 has no counterpart and is set aside, not matched.

**Row accounting.** Bank: 10 matched + 6 reconciling items + 1 set aside (B10) = 17 of 17. GL: 10 matched + 4 reconciling items + 1 foreign-account row (G08) = 15 of 15. Every source row appears exactly once across sections 5 and 6, or is the disclosed set-aside or foreign-account row.

## 6. Reconciling items

Classification per `03` §6. "Investigation" means the bank or the vendor must be asked.

| Ref | Side | Date | Description | Amount | Classification | Evidence |
|---|---|---|---|---:|---|---|
| B03 | Bank only | 2026-08-04 | Check 1048 - Office Supply Co | (620.00) | **Timing difference, carried from July** (July T-1 clearing). No August GL entry needed. | GL row dated 2026-07-30 in `july-2026-gl-cash.csv`, same exact amount, 5-day gap (section 4e). |
| B07 | Bank only | 2026-08-12 | ACH Vendor Zeta | (2,410.00) | **Requires GL adjustment** (paired with G09) | Bank shows an outflow of 2,410.00. GL G09 "Vendor Zeta payment" is +2,410.00, the same absolute amount, same date, opposite sign. Not matched because the signed amounts differ. |
| G09 | GL only | 2026-08-12 | Vendor Zeta payment | 2,410.00 | **Requires GL adjustment.** Payment appears recorded as a receipt. GL needs to move by (4,820.00). | As above. The description says "payment"; only the sign conflicts. |
| B08 | Bank only | 2026-08-14 | ACH Vendor Theta | (5,463.00) | **Unresolved exception, two readings** (paired with G10) | Bank 5,463.00 vs GL 5,436.00. Digits 3 and 6 transposed. Difference 27.00, outside the $0.00 tolerance, so not matched. |
| G10 | GL only | 2026-08-14 | Vendor Theta payment | (5,436.00) | **Unresolved exception, two readings** | As above. |
| B13 | Bank only | 2026-08-20 | ACH Vendor Delta | (1,845.00) | **Unresolved exception, two readings** | Same description and amount as B05, which matched G05. No GL entry for a second Delta payment. |
| B16 | Bank only | 2026-08-29 | Bank service charge | (42.00) | **Requires GL adjustment** (unrecorded bank fee) | Bank row; no GL entry (GL detail has no 42.00 row). |
| B17 | Bank only | 2026-08-29 | Interest earned | 9.75 | **Requires GL adjustment** (unrecorded interest). Credit account not selected, see section 8. | Bank row; no GL entry. |
| G04 | GL only | 2026-08-05 | Check 1052 - Acme Freight | (890.00) | **Offsetting GL-only pair with G06. Net 0.00. No adjustment.** | No bank clearing of check 1052 in August. |
| G06 | GL only | 2026-08-07 | Void Check 1052 - Acme Freight | 890.00 | As G04. | Void row offsets G04 exactly. See section 10, item 3. |

**Two readings, B13.** (A) Requires GL adjustment: a second Delta payment of 1,845.00 was made and never recorded. (B) Requires bank investigation: the bank processed a duplicate ACH debit or an erroneous debit. The data cannot choose. The repeated description and amount is a pattern, not evidence of either.

**Two readings, B08/G10.** (A) Requires GL adjustment: the GL amount was mis-keyed and the bank amount, 5,463.00, is correct. (B) Requires bank investigation: the bank debited 27.00 more than was authorized, and the GL is right. The data cannot choose.

**Excluded, not a reconciling item:** G08 (110000, (1,250.00)) is outside account 101000 and has no cash effect.

### Reconciliation statement

Items that do not depend on an open reading (G09 correction, B16, B17) are applied on the GL side. Items depending on an open reading (B13, B08/G10) are shown under each reading side by side. Every adjustment on the GL side is proposed only and not posted (section 8).

| | Amount |
|---|---:|
| Balance per GL 101000, 2026-08-31 | 85,384.00 |
| G09 sign correction (proposed) | (4,820.00) |
| B16 bank service charge (proposed) | (42.00) |
| B17 interest earned (proposed) | 9.75 |
| **GL balance adjusted for items not dependent on an open reading** | **80,531.75** |
| Balance per bank, 2026-08-31 (B10 set aside; reported figure) | 78,659.75 |
| Bank items outstanding from July (B03) | none remaining; check 1048 cleared 08-04 |
| Remaining difference, GL adjusted less bank | 1,872.00 = 1,845.00 (B13) + 27.00 (B08/G10) |

The remaining 1,872.00 is resolved differently under each reading:

| B13 reading | B08/G10 reading | Adjusted GL | Adjusted bank | Difference |
|---|---|---:|---:|---:|
| A: GL unrecorded payment. GL (1,845.00) | A: GL error. GL (27.00) | 78,659.75 | 78,659.75 | 0.00 |
| A: GL (1,845.00) | B: bank error. Bank +27.00 | 78,686.75 | 78,686.75 | 0.00 |
| B: bank error. Bank +1,845.00 | A: GL (27.00) | 80,504.75 | 80,504.75 | 0.00 |
| B: bank error. Bank +1,845.00 | B: bank +27.00 | 80,531.75 | 80,531.75 | 0.00 |

No reading is presented as primary. The true cash balance differs by up to 1,872.00 depending on the answer, which is why the answer matters.

## 7. Proof against the raw difference

| | Amount |
|---|---:|
| Bank ending less GL ending: 78,659.75 − 85,384.00 | (6,724.25) |
| Unmatched bank items (B03, B07, B08, B13, B16, B17): (620.00) + (2,410.00) + (5,463.00) + (1,845.00) + (42.00) + 9.75 | (10,370.25) |
| Unmatched GL items (G04, G06, G09, G10): (890.00) + 890.00 + 2,410.00 + (5,436.00) | (3,026.00) |
| Unmatched bank less unmatched GL | (7,344.25) |
| Add: opening difference, bank less GL at 2026-08-01 (July T-1) | 620.00 |
| Sum | (6,724.25) |
| **Residual unexplained difference** | **0.00** |

Cross-check: B03 (620.00) clears the 620.00 opening item, so August's unmatched items alone, excluding B03, are (9,750.25) − (3,026.00) = (6,724.25), equal to the raw difference. Residual 0.00. The raw difference is explained arithmetically, with nothing plugged. Note that this shows the items account for the difference. It does not show that each item's cause is settled (B08 and B13 are open).

## 8. Proposed adjustments

**Proposed only — not posted, and not reflected in any balance above except where the reconciliation statement labels it as proposed.** All require Controller approval. Amounts are general ledger entries. Where the counter-account is my inference it is labelled.

| Ref | Account | Account name | Debit | Credit | Description and support |
|---|---|---|---:|---:|---|
| AJE-A1 | 620000 | Bank Fees | 42.00 | | Record August bank service charge. Support: B16, `august-2026-bank.csv`. |
| AJE-A1 | 101000 | Operating Cash | | 42.00 | |
| AJE-A2 | 200000 | Accounts Payable | 4,820.00 | | Correct G09, a Vendor Zeta payment recorded as a 2,410.00 receipt: reverse the erroneous debit (2,410.00) and record the payment (2,410.00). Support: B07 vs G09. **Counter-account 200000 is my inference** (a vendor payment ordinarily relieves AP). The original credit side of G09 is not in the data. Confirm before posting. |
| AJE-A2 | 101000 | Operating Cash | | 4,820.00 | |
| AJE-A3 | 101000 | Operating Cash | 9.75 | | Record interest earned. Support: B17. **Credit account not proposed:** the chart of accounts in `01` has no interest income account, and I will not invent one. Controller to designate the account. |

**Conditional entries.** Each posts only if the Controller determines the stated reading.

| Ref | Account | Debit | Credit | Condition |
|---|---|---:|---:|---|
| AJE-C1 | 200000 Accounts Payable | 1,845.00 | | Posts only if the Controller determines B13 is a genuine second Vendor Delta payment not recorded in the GL (reading A). Counter-account is my inference, as for AJE-A2. |
| AJE-C1 | 101000 Operating Cash | | 1,845.00 | |
| AJE-C2 | 200000 Accounts Payable | 27.00 | | Posts only if the Controller determines the GL amount for Vendor Theta was mis-keyed and 5,463.00 is correct (reading A). Counter-account is my inference, and AP may be the wrong counter-account if the invoice was 5,436.00. |
| AJE-C2 | 101000 Operating Cash | | 27.00 | |

Under the alternative readings (B), no GL entry is proposed. A bank inquiry is needed instead: B13 (1,845.00) and B08 (27.00).

**No entry is proposed for:** B03 (timing difference, already recorded in July), G04/G06 (offsetting pair, net 0.00), G08 (outside cash), B01 and G02 (matched). July's AJE-1 remains a July proposal awaiting Controller decision and is not carried into any August balance.

## 9. Unresolved exceptions

1. **Bank row B10, 3,300.00, "Customer deposit K", 2026-08-15 — integrity finding, set aside per the Controller.** Identical to B09 on date, amount and description. Including it makes the bank roll-forward fail by exactly 3,300.00, and excluding it makes the roll-forward tie. This is consistent with a duplicated row but is not proven. Not resolved. A corrected bank extract or bank confirmation would close it.
2. **B13, (1,845.00),** two readings (section 6). Unresolved.
3. **B08 / G10, 27.00 difference,** two readings (section 6). Unresolved.
4. **(35.00) GL continuity break** between the July TB ending and the August TB beginning (section 4e). Cause not established.

Residual unexplained difference in section 7: 0.00. The items above are unresolved as to cause, not as to arithmetic.

## 10. Open observations

1. **G08, (1,250.00), AR write-off to 110000, present in the cash detail file.** It appears to be a mis-extracted non-cash row. It is excluded from the population, and the TB ties only without it. Not a cash item, but its presence means the GL extract was not filtered to 101000. That raises the question of whether the extract is otherwise complete. The GL roll-forward passes, which supports completeness. Controller to direct any follow-up on the extract.
2. **B01, 2,600.00, dated 2026-07-31, in the August bank file.** It is not in the July bank file, and July's bank roll-forward tied without it. The August roll-forward also ties with B01 counted as August activity. Reading A: the bank posted it in August with a 2026-07-31 effective date. Reading B: the row date is wrong. It matched G02 (GL 2026-08-01, 1-day gap), and the matching does not depend on the reading. If it had genuinely cleared on 2026-07-31, the July bank ending would have been 2,600.00 higher, which contradicts the July summary. I did not choose. It relates to the July cutoff observation (July workpaper section 6) on posting dates.
3. **G04/G06, check 1052 (890.00) issued 2026-08-05 and voided 2026-08-07.** Net zero, and no bank clearing was seen. Void support is not in the data. If the check had been released before the void, it could clear the bank later. I did not test September.
4. **B16 and July T-2.** The bank service charge was 35.00 in July and 42.00 in August. The change is noted, not investigated. The fee schedule is not in the data.
5. **B17 interest earned, 9.75.** The chart of accounts has no place to record it (section 8). This may recur monthly.
6. **The reconciling items are fully explained arithmetically, but the reconciliation is not complete.** An account can balance with open questions. See sections 6 and 9.

## 11. Escalation assessment

Threshold: **$200.00, set by the Controller for this engagement (section 3).** I apply it as "at or above $200.00" (my inference on the boundary, and no item is exactly 200.00). Items below the threshold are also escalated where they are unsupported, unusual or ambiguous in kind.

| Item | Amount | Meets $200 | Escalated | Reason |
|---|---:|---|---|---|
| B10 duplicate row, set aside | 3,300.00 | Yes | **Yes** | Data-integrity finding (Controller asked that it stay escalated) |
| G09 / B07 sign error | 4,820.00 (GL effect) | Yes | **Yes** | GL adjustment above threshold |
| B13 unrecorded or duplicate ACH | 1,845.00 | Yes | **Yes** | Unresolved, two readings |
| G08 foreign-account row | 1,250.00 | Yes | **Yes** | Scope exception |
| B01 out-of-period date | 2,600.00 | Yes | **Yes** | Scope exception (matched; date reading open) |
| B03 July check clearing | 620.00 | Yes | No | Supported timing difference, confirmed to July T-1 |
| B08 / G10 | 27.00 | No | **Yes** | Ambiguous in kind: GL error or bank error |
| GL continuity break | 35.00 | No | **Yes** | Unexplained opening movement, ambiguous in kind |
| B17 interest earned | 9.75 | No | **Yes** | No account in the chart of accounts |
| G04 / G06 void pair | 0.00 net | No | **Yes** | Void support not in data (low priority) |
| B16 bank fee | 42.00 | No | No | Supported and routine |
| Residual unexplained | 0.00 | No | No | |

## 12. Conclusion

**Account 101000 reconciles arithmetically for August 2026 on the Controller-directed population (B10 set aside), with a residual of 0.00.** Bank 78,659.75 and GL 85,384.00 differ by (6,724.25). After the July carryover (620.00), the Vendor Zeta sign error (4,820.00), the bank fee (42.00), interest (9.75), and the open items B13 (1,845.00) and B08/G10 (27.00), the adjusted balances agree under each of the four open readings: 78,659.75, 78,686.75, 80,504.75 and 80,531.75 (section 6). The reconciling items depend on unposted proposals. The reconciliation is not settled, because B13 and B08 are unresolved, B10 is set aside without resolution, and the 35.00 continuity break is unexplained.

**The Controller must act on:**

1. **B10 (3,300.00):** obtain a corrected bank extract or bank confirmation, or confirm the row is a duplicate. My reconciliation excludes it on your direction and does not resolve it. If B10 is genuine, the bank population and summary are inconsistent and this reconciliation needs to be redone.
2. **AJE-1 (July, 35.00):** state whether it was posted. This explains or not the (35.00) August opening break.
3. **Approve or reject AJE-A1** (42.00 bank fee to 620000).
4. **Approve or reject AJE-A2** (4,820.00 correction of the Vendor Zeta sign error). Confirm the counter-account (200000 is my inference).
5. **Designate the account for AJE-A3** (interest, 9.75). The chart of accounts has none, and adding accounts is not mine to do.
6. **B13 (1,845.00):** decide reading A (unrecorded payment, AJE-C1) or B (bank inquiry for duplicate debit). Investigate with the bank or vendor before deciding.
7. **B08 / G10 (27.00):** decide reading A (GL mis-key, AJE-C2) or B (bank inquiry). Investigate with the vendor invoice.
8. **G08 (1,250.00):** direct the treatment of the 110000 row found in the cash detail, and whether the GL extract needs to be re-run.
9. **B01:** state whether the 2026-07-31 date reflects an August posting or a misdated row (section 10).
10. **September follow-up:** confirm nothing further clears for check 1052 (G04/G06), and confirm the treatment of interest going forward.

## 13. Judgment log

| # | Judgment | Basis | Source of authority |
|---:|---|---|---|
| J-1 | Initial halt at the population gate, retained in section 4a | Bank roll-forward differed by 3,300.00 | `source-population-validation` §4; Staff Accountant escalation rules |
| J-2 | Set aside B10, proceeded with matching, kept it disclosed and escalated | Controller directed it as a likely data-quality artifact. I did not verify it is a duplicate. Both readings remain open. | **Controller instruction, 2026-09-28** |
| J-3 | Matching tolerance exact amount ($0.00); date window 5 days | Provided for this engagement only. Not a standing rule. Not carried from July, though the values coincide with July's. | **Controller instruction, 2026-09-28** |
| J-4 | Escalation threshold $200.00, applied at or above the amount | Provided for this engagement only. The "at or above" boundary is my inference; no item is exactly 200.00. | **Controller instruction, 2026-09-28**; boundary is preparer inference |
| J-5 | No materiality figure used. Every unmatched item investigated and disclosed. | None was specified, and none is defined in company documents. | Controller instruction, 2026-09-28; `03` §3, §6 |
| J-6 | Verified continuity from July and confirmed July carryover items to the July workpaper (section 4e) | Controller direction | **Controller instruction, 2026-09-28** |
| J-7 | Escalated items below $200 where ambiguous or unusual in kind | Amount is one trigger, not the only one | Staff Accountant escalation rules; `03` §5 |
| J-8 | G08 excluded from the 101000 population, and disclosed | Account is 110000; the TB net ties only without it | `source-population-validation` §1; TB tie-out |
| J-9 | B01 matched to G02 despite the 1-day date difference and the July date | Exact amount, corroborating description, gap within the 5-day window. Roll-forward includes B01 as August activity. | J-3; `04` §2 |
| J-10 | B03 classified as a timing difference clearing July T-1 | Exact amount to the July GL row, 5-day gap (inclusive) within the window, and it closes the 620.00 opening difference exactly | J-3; July workpaper T-1 |
| J-11 | B07 and G09 not matched | Signed amounts differ (opposite signs). Matching them would be forcing. Classified as a GL sign error because the GL description says "payment". | `03` §4; `04` §2; classification is preparer inference |
| J-12 | B08 and G10 not matched; two readings shown; entries conditional | 27.00 difference is outside the $0.00 tolerance. The data cannot say whether the GL or the bank is wrong. | J-3; reconciliation skill §8; `03` §4 |
| J-13 | B13 left unmatched; two readings shown; entries conditional | Repeated description and amount is not evidence of either reading | Reconciliation skill §8; `03` §4 |
| J-14 | Counter-account 200000 proposed for AJE-A2, C1, C2 | Vendor payments ordinarily go through AP. The original posting side is not in the data. | Preparer inference, stated as such; `01` chart of accounts |
| J-15 | No credit account proposed for interest (AJE-A3) | No interest income account in the chart of accounts | `01` chart of accounts; Staff Accountant rule not to invent accounts |
| J-16 | G04/G06 presented as an offsetting pair with no adjustment | Net 0.00. Each appears once in section 6. | Preparer inference |
| J-17 | July AJE-1 not carried into any August balance; 35.00 break disclosed with two readings | I cannot tell from the data whether it was posted | `03` §4; Staff Accountant "two readings" rule |
| J-18 | Statement shown under four readings, none primary | Two open items, each with two readings | Reconciliation skill §6, §8 |

---

*Prepared by the Staff Accountant. Not effective until independently reviewed and approved by the Controller per `05 independent-review-control.md`.*
