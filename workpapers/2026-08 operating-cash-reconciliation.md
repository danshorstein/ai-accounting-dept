# Operating Cash Reconciliation — August 2026

**STATUS: HALTED AT THE DATA-QUALITY GATE. Reconciliation NOT performed. Escalated to the Controller.**

| | |
|---|---|
| **Entity** | Riverton Sporting Goods, Inc. |
| **GL account** | 101000 — Operating Cash |
| **Bank account** | Operating Checking |
| **Period** | 2026-08 (2026-08-01 through 2026-08-31) |
| **Prepared by** | Staff Accountant (Claude) |
| **Date prepared** | 2026-09-28 |
| **Reviewed by** | _________________ (Controller) |
| **Date reviewed** | _________________ |
| **Review outcome** | ☐ Approved  ☐ Returned with questions/corrections |

Prepared under `03 cash-reconciliation-policy.md` and `04 bank-reconciliation-procedure.md`, using the `source-population-validation` and `reconciliation-workpaper-construction` skills. **This work is not effective until independently reviewed by the Controller under `05 independent-review-control.md`. The preparer has not approved it.** The Controller was not available for this engagement; no Controller instruction or parameter was received.

**Calculation script:** `workpapers/2026-08 operating-cash-reconciliation.py`. Run from the repository root with `python3 "workpapers/2026-08 operating-cash-reconciliation.py"`. It prints every figure cited below. Inputs are read from `data/` by relative path, including prior-period figures, which come from the July source files.

---

## 1. Sources used

| File | Content | Rows |
|---|---|---:|
| `data/august-2026-bank.csv` | Bank transaction detail (id, date, description, amount) | 17 |
| `data/august-2026-bank-summary.csv` | Bank beginning/ending balance, Operating Checking, 2026-08 | 1 |
| `data/august-2026-gl-cash.csv` | GL cash detail (id, date, description, amount, account) | 15 |
| `data/august-2026-trial-balance.csv` | TB beginning, net activity, ending, account 101000, 2026-08 | 1 |
| `data/july-2026-bank-summary.csv`, `data/july-2026-trial-balance.csv` | Prior-period ending balances, used only for the continuity check | 1 each |

Sign convention (confirmed from the data): amounts are signed, with inflows positive and outflows negative on both sides.

## 2. Balances to be reconciled (as reported)

| | Bank | GL 101000 |
|---|---:|---:|
| Beginning balance | 74,060.00 | 73,440.00 |
| Ending balance (reported) | 78,659.75 | 85,384.00 |

Beginning balances **do not agree**: bank exceeds GL by **620.00**, so a prior-period item is carrying forward. The raw ending difference is bank less GL = **(6,724.25)**. I did not attempt to explain this difference, because the gate below failed. See section 4.

## 3. Population completeness: roll-forward proofs

### Bank roll-forward — **FAILS**

| Item | Amount | Source |
|---|---:|---|
| Beginning balance | 74,060.00 | `august-2026-bank-summary.csv` |
| Total activity (17 rows) | 7,899.75 | `august-2026-bank.csv`, B01–B17 |
| **Calculated ending balance** | **81,959.75** | computed |
| Reported ending balance | 78,659.75 | `august-2026-bank-summary.csv` |
| **Difference** | **3,300.00** | calculated exceeds reported |

### GL roll-forward — passes

| Item | Amount | Source |
|---|---:|---|
| Beginning balance per TB | 73,440.00 | `august-2026-trial-balance.csv` |
| Total activity, account 101000 rows only (14 of 15 rows) | 11,944.00 | `august-2026-gl-cash.csv`, all rows except G08 |
| **Calculated ending balance** | **85,384.00** | computed |
| Reported TB ending balance | 85,384.00 | `august-2026-trial-balance.csv` |
| **Difference** | **0.00** | pass |

The 101000 detail also ties to the TB `debits_credits_net` of 11,944.00 (difference 0.00). Including G08 would give an activity total of 10,694.00 and a calculated ending of 84,134.00, which is a (1,250.00) difference from the TB. The TB therefore excludes G08, which is consistent with G08 belonging to another account.

## 4. Integrity and scope checks, and the halt

| Check | Result |
|---|---|
| Row counts | Bank 17; GL 15 |
| Date range | Bank 2026-07-31 to 2026-08-29; GL 2026-08-01 to 2026-08-27 |
| Out-of-period rows | **Bank B01, 2026-07-31, "Customer deposit J", 2,600.00**, dated before the period start. It is not in `july-2026-bank.csv`. |
| Foreign-account rows | **GL G08, 2026-08-11, "AR write-off - Bright Retailers", (1,250.00), account 110000**. Not cash. It is excluded from the 101000 population and from the TB net. It is disclosed, not silently dropped. |
| Duplicates on date + amount + description | **Bank B09 and B10, 2026-08-15, "Customer deposit K", 3,300.00, identical.** None in the GL. |
| Same description and amount on different dates (not duplicates) | Bank B05 (2026-08-06) and B13 (2026-08-20), "ACH Vendor Delta", (1,845.00). Disclosed only. |
| Zero, blank or non-numeric amounts | None |
| Beginning balances | Bank 74,060.00 vs GL 73,440.00, difference 620.00 |
| Prior-period continuity, bank | July bank ending 74,060.00 = August beginning 74,060.00. Difference 0.00. |
| Prior-period continuity, GL | July TB ending 73,475.00 vs August TB beginning 73,440.00. **Difference (35.00).** |

**Disposition: STOP.** The bank population does not tie to its own summary, and is overstated against the reported ending balance by 3,300.00. Under the `source-population-validation` skill §4 and the Staff Accountant escalation rules, I did not begin matching. The GL side ties. This halt is a data-quality halt, and it applies regardless of amount or any threshold.

**Observation on the 3,300.00 (two readings, neither resolved).** The failed roll-forward difference equals the amount of B10, the second of the two identical "Customer deposit K" rows.
- **Reading A:** B10 is a duplicated row in the bank extract. Removing it would make the bank roll-forward tie at 78,659.75. The extract would then be invalid as delivered, and a corrected extract would be needed.
- **Reading B:** both deposits are genuine, and the summary ending balance or the extract is wrong or incomplete in some other way. The equal amount would then be coincidence.

The data cannot choose between these readings. I did not remove B10 or adjust either figure. Other explanations, such as out-of-period B01 (2,600.00) combined with other omissions, are also not excluded by the data.

**Observation on the GL continuity break (35.00).** The August TB beginning balance is 35.00 lower than the July TB ending balance. This equals the amount of proposed adjustment AJE-1 (July bank service charge) in the July workpaper. That proposal was not approved or posted by me, and I have no evidence of Controller approval. Readings: (i) a 35.00 entry was posted to 101000 after the July TB was produced, or (ii) the opening balance is otherwise inconsistent with July. The August detail contains no matching entry. Not resolved.

**Observation on the 620.00 opening difference.** It equals July's outstanding check 1048 (620.00, July workpaper T-1), and the August bank file shows a Check 1048 clearing on 2026-08-04 for (620.00). I note the coincidence of amounts only. I did not match or classify it, because the population failed the gate.

## 5. Work not performed (blocked)

Withheld because the gate failed:
- Transaction matching, matched-activity table, and reconciling-item classification.
- Reconciliation statement and proof against the raw difference. The residual is not stated because it would not be reliable. I do not represent the account as reconciled or unreconciled.
- Proposed adjustments (section 8). I have no supported basis to propose any entry against a population that fails its tie-out.

Matching tolerance and date window were not needed and were not set. When a valid bank population is supplied, they should be re-derived from that data, not carried from July.

## 6. Unresolved exceptions

1. Bank roll-forward difference of 3,300.00 (section 3). Cause not established.
2. GL opening balance vs July closing balance, (35.00). Cause not established.
3. Opening bank-vs-GL difference of 620.00. Nature not investigated, as it is downstream of the gate.
4. Out-of-period bank row B01 (2,600.00, dated 2026-07-31).
5. Foreign-account GL row G08 (1,250.00 to 110000). It appears not to be a cash entry, and its handling is for the Controller.
6. Duplicate-looking bank rows B09 and B10 (3,300.00 each).

## 7. Escalation assessment

**Working assumption (preparer inference, not a Controller instruction):** no numeric escalation threshold is set. I derived none from a number, since no company document defines one and no Controller was available. Because the populations are small (17 and 15 rows), the failed check is a completeness question, and policy §5 requires unusual items to be investigated and escalated, every item below is escalated regardless of amount. This is my own derivation, and it does not reuse any figure from July.

| Item | Amount | Escalated? | Reason |
|---|---:|---|---|
| Bank roll-forward failure | 3,300.00 | **Yes** | Integrity failure; mandatory halt |
| GL opening vs July close | 35.00 | **Yes** | Continuity break, ambiguous in kind |
| Out-of-period row B01 | 2,600.00 | **Yes** | Scope exception |
| Foreign-account row G08 | 1,250.00 | **Yes** | Scope exception |
| Duplicate-looking rows B09/B10 | 3,300.00 | **Yes** | Possible duplicate |
| Opening difference | 620.00 | **Yes** | Carry-forward item, not investigated |

## 8. Proposed adjustments

**None proposed.** Nothing is posted or assumed into any balance above. AJE-1 from July remains a July proposal awaiting Controller decision, and I have not carried it into any August balance.

## 9. Conclusion

**No conclusion can be given on whether account 101000 reconciles for August 2026.** The GL population ties (difference 0.00). The bank population does not tie: the calculated ending is 81,959.75 against a reported 78,659.75, a difference of 3,300.00. Matching was not started. The reviewer block is blank and this work awaits Controller independent review.

**The Controller must act on:**
1. Direct how to proceed on the bank population. Options include providing a corrected bank extract, or confirming whether B10 is a duplicate row and whether the summary balance is right (readings A and B in section 4).
2. Confirm whether B01 (2026-07-31 "Customer deposit J", 2,600.00) belongs in the August bank activity.
3. Explain the (35.00) GL opening-balance difference to the July closing balance, and state whether July AJE-1 was posted.
4. Direct the treatment of GL row G08 (110000 entry in the cash detail file).
5. Set the matching tolerance, date window and escalation threshold for August, or confirm that the preparer should re-derive them once a valid population is available.
6. Once resolved, direct resumption of the reconciliation, including the 620.00 opening difference and the July Check 1048.

## 10. Judgment log

| # | Judgment | Basis | Source of authority |
|---:|---|---|---|
| J-1 | Halted before matching; no reconciliation or residual presented | The bank roll-forward differs by 3,300.00, and reconciling against a population that does not tie is prohibited | `source-population-validation` §4; Staff Accountant escalation rules; `04a` step 2 (proposed, not approved, consistent with the skill) |
| J-2 | Escalation: no numeric threshold; every item escalated regardless of amount | No threshold is defined and no Controller was available. Populations are small and the exceptions are integrity issues. Derived independently for August, not reused from July. | Preparer inference, stated as such; `03` §5 |
| J-3 | Matching tolerance and date window not set | Not needed, since matching did not occur. Left for Controller direction or later re-derivation from valid data. | Preparer inference |
| J-4 | G08 excluded from the 101000 population, and disclosed | Its account is 110000, and the TB net ties only when it is excluded | `source-population-validation` §1; TB tie-out |
| J-5 | B01 and B10 left in the bank population and disclosed. Nothing removed to force a tie. | Removing rows to reach the reported balance would be a plug | `03` §4; `04` §2 |
| J-6 | 3,300.00 = B10 amount recorded as an observation with two readings, neither adopted | The data cannot distinguish a duplicated row from a coincidence | `03` §4; Staff Accountant "two readings" rule |
| J-7 | 35.00 = July AJE-1 amount noted with two readings, not resolved | I cannot determine from the data whether AJE-1 was posted | Preparer inference; `03` §4 |
| J-8 | No proposed adjustments | Nothing supported against an untied population | `04` §4 |

---

*Prepared by the Staff Accountant. Not effective until independently reviewed and approved by the Controller per `05 independent-review-control.md`.*
