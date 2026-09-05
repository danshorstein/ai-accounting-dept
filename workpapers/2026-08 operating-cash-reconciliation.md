# Operating Cash Reconciliation — August 2026

| | |
|---|---|
| **Entity** | Riverton Sporting Goods, Inc. |
| **GL account** | 101000 — Operating Cash |
| **Bank account** | Operating Checking |
| **Period** | 2026-08 (2026-08-01 through 2026-08-31) |
| **Prepared by** | Staff Accountant (Claude) |
| **Date prepared** | 2026-08-29 |
| **Reviewed by** | _______________ (Controller) |
| **Date reviewed** | _______________ |
| **Review outcome** | ☐ Approved  ☐ Returned with questions/corrections |

Prepared under `03 cash-reconciliation-policy.md` and `04 bank-reconciliation-procedure (proposed revision).md`. Submitted for independent review under `05 independent-review-control.md`. The preparer has not approved this work and does not approve their own work.

Arithmetic performed by `workpapers/2026-08 operating-cash-reconciliation.py` (retained with this workpaper). Every figure below traces to a source row in §1 or to a computation shown on the page.

> **Preparation note.** This workpaper was first issued as an incomplete draft halted at
> population validation (bank side did not tie by 3,300.00). The Controller reviewed that
> draft and, on 2026-08-29, directed: set duplicate bank row B10 aside and proceed with the
> detailed reconciliation excluding it; carry all other findings through to where they
> land; use the engagement parameters in §10; verify roll-forward continuity from July; and
> confirm July carryover items. This version implements that direction.

> **Correction note (2026-09-05).** The independent review of this workpaper, dated
> 2026-09-05 (`workpapers/2026-08 operating-cash-reconciliation — independent review.md`),
> returned two items for correction: (1) RP-1 — a required "Open observations" section was
> missing; its content existed but was scattered across §3, §5, and the former §11's action
> item 7. Added as new §9, consolidating that disclosure, with subsequent sections
> renumbered. (2) ST-1 — the conclusion's lead sentence stated "reconciles" before its
> governing contingency (duplicate bank row B10) rather than before or alongside it. The
> lead sentence in what is now §12 was reordered accordingly. No figure, match,
> classification, judgment-log entry, or conclusion substance was changed. The review's
> FLAG items (ST-2, ST-3, ST-4, ST-6, RP-8) are escalations for the Controller, not
> preparer corrections, and are not addressed in this workpaper.

---

## 1. Sources used

| File | Content | Rows |
|---|---|---:|
| `data/2026-08/august-2026-bank.csv` | Bank transaction detail (id, date, description, amount) | 17 |
| `data/2026-08/august-2026-bank-summary.csv` | Bank beginning/ending balance — Operating Checking, 2026-08 | 1 |
| `data/2026-08/august-2026-gl-cash.csv` | GL cash detail (id, date, description, amount, account) | 15 |
| `data/2026-08/august-2026-trial-balance.csv` | TB beginning balance, net activity, ending balance — account 101000, 2026-08 | 1 |
| `workpapers/2026-07 operating-cash-reconciliation.md` | Prior-period reconciliation — carryover items (§7) and continuity (§4) | — |

**Account and period (procedure §1).** The bank summary names "Operating Checking / 2026-08"; the trial balance names account 101000 / 2026-08. The GL detail file contains **14 rows posted to 101000** and **1 row posted to 110000** (G08 — finding I-3, excluded from the reconciled population). The bank detail contains **16 rows dated in 2026-08** and **1 row dated 2026-07-31** (B01 — finding I-2, retained). Sign convention (repository convention): amounts signed, outflows negative — confirmed on both files, with one anomaly at finding I-4 (G09).

## 2. Balances to be reconciled

| | Bank (Operating Checking) | GL 101000 |
|---|---:|---:|
| Beginning balance | 74,060.00 | 73,440.00 |
| Net August activity | 4,599.75 (excl. B10 — see §3) | 11,944.00 |
| Ending balance (reported) | 78,659.75 | 85,384.00 |

Sources: bank beginning/ending from `august-2026-bank-summary.csv`; GL beginning, net, ending from `august-2026-trial-balance.csv`; bank net activity computed from `august-2026-bank.csv` (16 rows, B10 excluded).

**Beginning balances do not agree.** Bank 74,060.00 − GL 73,440.00 = **620.00**. This is the July 2026 outstanding Check 1048 — Office Supply Co (620.00) carrying forward (July workpaper item T-1). It is resolved within August — see §5 item C-1 and §7.

**Difference to be explained at 8/31:** bank ending 78,659.75 − GL ending 85,384.00 = **(6,724.25)**. This figure is reconciled in full in §6, with an explicit residual of 0.00.

## 3. Population completeness — roll-forward proofs

### Bank roll-forward — ties (B10 excluded)

| Item | Amount | Source |
|---|---:|---|
| Beginning balance | 74,060.00 | `august-2026-bank-summary.csv` |
| Total August bank activity — 16 rows, **excluding duplicate row B10** | 4,599.75 | `august-2026-bank.csv` |
| **Calculated ending balance** | **78,659.75** | computed |
| Reported ending balance | 78,659.75 | `august-2026-bank-summary.csv` |
| **Difference** | **0.00** | — |

With all 17 rows the bank detail over-explains the balance change by **3,300.00**, which equals bank row **B10** exactly (B09 and B10 are an exact duplicate on date + amount + description: 2026-08-15, "Customer deposit K", 3,300.00). Per Controller direction (2026-08-29), B10 is set aside as a likely data-quality artifact and excluded from all matching and totals below; it remains a disclosed integrity finding (I-1) and an escalation (§11). **The reported bank ending balance of 78,659.75 already reflects a single deposit K**, so excluding B10 makes the population internally consistent. The preparer has not confirmed B10 is spurious rather than a genuine second same-day deposit — see I-1 and the conclusion caveat in §12.

### GL roll-forward — ties

| Item | Amount | Source |
|---|---:|---|
| Beginning balance per TB | 73,440.00 | `august-2026-trial-balance.csv` |
| Total August GL activity — 14 rows posted to 101000 only | 11,944.00 | `august-2026-gl-cash.csv` |
| **Calculated ending balance** | **85,384.00** | computed |
| Reported TB ending balance | 85,384.00 | `august-2026-trial-balance.csv` |
| **Difference** | **0.00** | — |

The GL detail sum (101000 rows only) also agrees exactly to the TB `debits_credits_net` of 11,944.00 (difference 0.00). Row G08 (account 110000) is excluded; including it, the file sums to 10,694.00 and does not tie — confirming G08 does not belong to this population (I-3). The GL population is **internally consistent with its own trial balance**. It nonetheless contains substance anomalies (I-4, I-6) that flow through to reconciling items in §5–§6, because the trial balance appears to have been built from the same detail.

### Integrity checks

- Bank: 17 rows; no zero, blank, or non-numeric amounts; date range 2026-07-31 to 2026-08-29 (see I-2). One exact-duplicate pair, B09/B10 (I-1).
- GL: 15 rows; no zero, blank, or non-numeric amounts; date range 2026-08-01 to 2026-08-27; no duplicate date/amount/description rows.
- Beginning-balance comparison: bank 74,060.00 vs GL 73,440.00 → 620.00 prior-period carryforward (§2, §5 C-1).

### Integrity findings carried forward

| Ref | Population | Row(s) | Finding | Effect on the roll-forward | Where it lands |
|---|---|---|---|---|---|
| I-1 | Bank | B09, B10 | Exact-duplicate row: 2026-08-15, "Customer deposit K", 3,300.00, twice | Breaks the bank roll-forward by 3,300.00; excluding B10 ties it exactly | Set aside per Controller (§3); escalation (§11); conclusion caveat (§12) |
| I-2 | Bank | B01 | "Customer deposit J", 2,600.00, dated **2026-07-31** in the August file; not in the July bank population | None — needed for the bank side to tie; matched to G02 | Disclosed observation; matched pair 1 (§6); recurring cutoff pattern (§5 C-3); consolidated in **§9 Open observations** |
| I-3 | GL | G08 | "AR write-off - Bright Retailers", (1,250.00), posted to **110000**, present in the cash-detail file | None — excluded from the 101000 net; GL still ties | Excluded from population; reconciling-items table (§6); escalation (§11) |
| I-4 | GL | G09 | Sign anomaly: "Vendor Zeta payment" **+2,410.00** where every other vendor payment is negative | None — TB built from same detail; ties internally | Reconciling item **R-1** (§6); proposed **AJE-1** (§7); escalation (§11) |
| I-5 | GL | G04, G06 | Check 1052 — Acme Freight written (−890.00, 8/5) and voided (+890.00, 8/7); net zero | None — nets to zero | Reconciling item **R-7** (§6); no adjustment; Controller confirmation requested (§12) |
| I-6 | GL vs Bank | G10 / B08 | "Vendor Theta payment" GL **(5,436.00)** vs bank **(5,463.00)** — apparent 27.00 transposition | None to the GL roll-forward (internally consistent); prevents an exact match | Reconciling item **R-2** (§6); proposed **AJE-2** or bank investigation (§7, §8); escalation (§11) |

### Disposition

Both populations tie to their reported ending balances (bank after excluding B10 per Controller direction). They are a valid basis for transaction-level matching. Integrity findings I-1 through I-6 are carried forward as disclosed items, not resolved by assumption.

## 4. Roll-forward continuity from July 2026

| Continuity check | July ending | August beginning | Reconciles? |
|---|---:|---:|---|
| Bank (Operating Checking) | 74,060.00 (July workpaper §2; `july-2026-bank-summary.csv`) | 74,060.00 | **Yes — equal.** |
| GL 101000 — raw | 73,475.00 (July TB ending, July workpaper §2) | 73,440.00 | No — differs by 35.00 |
| GL 101000 — after July AJE-1 | 73,475.00 − 35.00 = **73,440.00** | 73,440.00 | **Yes — equal after posting the July bank-fee adjustment.** |

The 35.00 GL discontinuity is exactly the July proposed adjustment **AJE-1** (Dr 620000 Bank Fees / Cr 101000 Operating Cash, 35.00 — the unrecorded July bank service charge, July workpaper item T-2). The August GL beginning balance equals the July *adjusted* book balance, which indicates AJE-1 was approved and posted after the July trial balance was struck. The preparer has no direct posting confirmation in the August source data and asks the Controller to confirm (§12). No other continuity break exists.

## 5. July 2026 carryover items — disposition in August

| Ref | July item (July workpaper) | Amount | August status | Evidence |
|---|---|---:|---|---|
| C-1 | T-1 — outstanding Check 1048, Office Supply Co (timing difference) | 620.00 | **Cleared.** Paid by bank 2026-08-04. Consumes the 620.00 beginning-balance difference (§2). No August GL entry expected (recorded in July books). Not a reconciling item at 8/31. | Bank row **B03** (2026-08-04, "Check 1048 - Office Supply Co", −620.00) |
| C-2 | T-2 / AJE-1 — unrecorded July bank service charge | 35.00 | **Posted** (per §4 continuity). Confirm with Controller. | August GL beginning balance 73,440.00 = July TB ending 73,475.00 − 35.00 |
| C-3 | §6 cutoff observation — "AR receipt E" (7,400.00) dated 2026-08-01 but included in July TB activity; bank deposit cleared 2026-07-31 | 7,400.00 | **Not double-counted.** No "deposit E" in the August bank file and no "AR receipt E" in the August GL file; the item sits only in the July populations. No August effect. | Absence from `august-2026-bank.csv` and `august-2026-gl-cash.csv` |

No outstanding deposits in transit were carried forward from July (all July deposits cleared within July per that workpaper). The recurring posting-date pattern flagged in July C-3 appears again in August as I-2 (bank deposit dated 7/31 / GL receipt dated 8/1) — disclosed, no reconciliation effect; consolidated with its July precedent in **§9 Open observations**.

## 6. Matched activity and reconciliation

**Matching basis (engagement parameters, Controller, 2026-08-29 — scoped to this engagement, §10):** exact amount ($0.00 tolerance); date window up to 5 days; description used as corroborating evidence. B10 excluded (§3).

### Matched pairs — 10 bank rows to 10 GL rows

| # | Bank id | Bank date | Bank description | Amount | GL id | GL date | GL description | Date gap (days) |
|---:|---|---|---|---:|---|---|---|---:|
| 1 | B01 | 2026-07-31 | Customer deposit J | 2,600.00 | G02 | 2026-08-01 | AR receipt J | 1 |
| 2 | B02 | 2026-08-01 | Customer deposit F | 5,200.00 | G01 | 2026-08-01 | AR receipt F | 0 |
| 3 | B04 | 2026-08-05 | ACH Vendor Alpha | (3,410.00) | G03 | 2026-08-05 | Vendor Alpha payment | 0 |
| 4 | B05 | 2026-08-06 | ACH Vendor Delta | (1,845.00) | G05 | 2026-08-06 | Vendor Delta payment | 0 |
| 5 | B06 | 2026-08-09 | Customer deposit G | 7,850.00 | G07 | 2026-08-09 | AR receipt G | 0 |
| 6 | B09 | 2026-08-15 | Customer deposit K | 3,300.00 | G11 | 2026-08-15 | AR receipt K | 0 |
| 7 | B11 | 2026-08-15 | Payroll | (10,200.00) | G12 | 2026-08-15 | Payroll run | 0 |
| 8 | B12 | 2026-08-18 | Customer deposit H | 6,300.00 | G13 | 2026-08-18 | AR receipt H | 0 |
| 9 | B14 | 2026-08-22 | ACH Vendor Beta | (2,975.00) | G14 | 2026-08-22 | Vendor Beta payment | 0 |
| 10 | B15 | 2026-08-27 | Customer deposit I | 8,150.00 | G15 | 2026-08-27 | AR receipt I | 0 |
| | | | **Total matched** | **14,970.00** | | | **14,970.00** | |

Pair 1 has a 1-day gap, within the 5-day window, exact amount, corroborating description. B01 also carries a 2026-07-31 date in the August bank file (I-2) — disclosed; because the item is matched and each side falls in its own period population, it is not a reconciling item.

No match was forced. **Every source row appears exactly once** across the matched table (§6), the reconciling items (below), or the set-aside/excluded list: 17 bank rows = 10 matched + 6 unmatched (B03, B07, B08, B13, B16, B17) + 1 set aside (B10); 15 GL rows = 10 matched + 4 unmatched (G04, G06, G09, G10) + 1 foreign-account excluded (G08).

### Reconciling items

| Ref | Side | Date | Description | Amount | Classification (`03` §6) | Support |
|---|---|---|---|---:|---|---|
| C-1 | Bank only | 2026-08-04 | Check 1048 — Office Supply Co clears | (620.00) | Timing difference — prior-period outstanding check clearing; offsets the 620.00 beginning-balance difference | Bank row B03; July workpaper item T-1; no August GL row (recorded July) |
| R-1 | Both (error) | 2026-08-12 | Vendor Zeta payment — GL posted **+2,410.00**, bank paid **(2,410.00)** | (4,820.00) | Requires GL adjustment — apparent posting-sign error (G09) | Bank row B07 (−2,410.00) vs GL row G09 (+2,410.00); all other vendor payments in the file are negative |
| R-2 | Both (error) | 2026-08-14 | Vendor Theta payment — GL posted **(5,436.00)**, bank paid **(5,463.00)** | (27.00) | Requires GL adjustment **or** bank investigation — apparent 27.00 transposition (5,436 ↔ 5,463) | Bank row B08 (−5,463.00) vs GL row G10 (−5,436.00) |
| R-3 | Bank only | 2026-08-20 | ACH Vendor Delta — second identical payment, not in GL | (1,845.00) | Requires GL adjustment **or** bank investigation — see two readings below | Bank row B13 (−1,845.00); GL has only one Delta payment (G05, matched to B05); no GL row within the window |
| R-4 | Bank only | 2026-08-29 | Bank service charge | (42.00) | Requires GL adjustment — unrecorded bank fee | Bank row B16; no GL entry |
| R-5 | Bank only | 2026-08-29 | Interest earned | 9.75 | Requires GL adjustment — unrecorded interest income; **no suitable income account in the chart** (§8, §11) | Bank row B17; no GL entry |
| R-7 | GL only | 2026-08-05 / 08-07 | Check 1052 — Acme Freight written (G04, −890.00) then voided (G06, +890.00) | 0.00 | Timing difference — net zero; no bank activity, no adjustment | GL rows G04 and G06; no bank clearing (check voided before clearing) |
| I-3 | GL only | 2026-08-11 | AR write-off — Bright Retailers, posted to account **110000**, present in the cash-detail file | (1,250.00) | Not a cash item — excluded from the reconciled population; coding / file-sourcing question | GL row G08; account 110000, not 101000 |

**Two readings for R-2 and R-3, not resolved (`03` §4):**
- *GL-error reading (primary presentation below):* the bank is correct; G10 is understated by 27.00 and a second Delta payment was omitted from the GL. Both require GL adjustments (AJE-2, AJE-3).
- *Bank-error reading:* the GL is correct; the bank overcharged 27.00 on the Theta ACH and double-charged the 1,845.00 Delta ACH. Both require bank investigation and no GL entry.
The reconciliation balances to a 0.00 residual under either reading (see proof); the difference is only in whether the correction lands on the book side or the bank side. The preparer cannot choose between them from the data alone.

### Reconciliation statement (primary reading — GL errors)

| | Amount |
|---|---:|
| **Balance per bank, 2026-08-31** (per summary; excludes duplicate B10) | **78,659.75** |
| Deposits in transit | 0.00 |
| Outstanding checks (Check 1048 cleared 8/4; Check 1052 voided 8/7 — none outstanding) | 0.00 |
| **Adjusted bank balance** | **78,659.75** |
| | |
| **Balance per GL 101000, 2026-08-31** | **85,384.00** |
| Proposed AJE-1 — correct Vendor Zeta payment direction (R-1) | (4,820.00) |
| Proposed AJE-2 — correct Vendor Theta payment amount (R-2) | (27.00) |
| Proposed AJE-3 — record second Vendor Delta payment (R-3) | (1,845.00) |
| Proposed AJE-4 — record bank service charge (R-4) | (42.00) |
| Proposed AJE-5 — record interest earned (R-5) | 9.75 |
| **Adjusted book balance** | **78,659.75** |
| | |
| **Difference (adjusted bank − adjusted book)** | **0.00** |

Under the bank-error reading, AJE-2 and AJE-3 move to the bank side instead; adjusted bank and adjusted book then both equal **80,531.75**, difference **0.00** (see script output).

### Proof against the raw difference

| | Amount |
|---|---:|
| Bank ending 78,659.75 − GL ending 85,384.00 | (6,724.25) |
| Beginning-balance difference (Check 1048 outstanding at 8/1, bank higher) | 620.00 |
| Sum of unmatched bank items (B03, B07, B08, B13, B16, B17) | (10,370.25) |
| Less: sum of unmatched GL items (G04, G06, G09, G10) | (3,026.00) |
| Unmatched bank − unmatched GL | (7,344.25) |
| Beginning difference + (unmatched bank − unmatched GL) = 620.00 + (7,344.25) | (6,724.25) |
| **Residual unexplained difference** | **0.00** |

Item-level decomposition of the (6,724.25): Check 1048 begin diff +620.00 and its clearing (620.00) net to 0.00; R-1 (4,820.00); R-2 (27.00); R-3 (1,845.00); R-4 (42.00); R-5 +9.75; R-7 written +... voided nets to 0.00. Total (6,724.25). Nothing was plugged, forced, or assumed.

## 7. Proposed general-ledger adjustments

**Proposed only — not posted, and not assumed into any balance presented as "reported" above.** Each requires Controller approval. Offsetting accounts for the vendor-payment corrections (AJE-1 to AJE-3) are coded to **200000 Accounts Payable** on the inference that Zeta, Theta, and Delta are trade vendors whose payments relieve AP; the preparer has no AP subledger or invoice support and flags this for Controller confirmation (J-6). AJE-2 and AJE-3 are proposed **only under the GL-error reading**; under the bank-error reading they are replaced by a bank investigation request and no entry is posted.

| Ref | Account | Account name | Debit | Credit | Purpose / support |
|---|---|---|---:|---:|---|
| AJE-1 | 200000 | Accounts Payable | 4,820.00 | | Correct Vendor Zeta payment posted 2026-08-12 as +2,410.00 (GL G09) to the actual (2,410.00) cash outflow per bank B07. Net cash effect (4,820.00). |
| AJE-1 | 101000 | Operating Cash | | 4,820.00 | |
| AJE-2 | 200000 | Accounts Payable | 27.00 | | Correct Vendor Theta payment from (5,436.00) (GL G10) to (5,463.00) per bank B08 — 27.00 understatement. |
| AJE-2 | 101000 | Operating Cash | | 27.00 | |
| AJE-3 | 200000 | Accounts Payable | 1,845.00 | | Record second Vendor Delta ACH payment of (1,845.00) dated 2026-08-20 per bank B13, not in the GL. |
| AJE-3 | 101000 | Operating Cash | | 1,845.00 | |
| AJE-4 | 620000 | Bank Fees | 42.00 | | Record August bank service charge assessed 2026-08-29 per bank B16, not in the GL. Same treatment as July AJE-1. |
| AJE-4 | 101000 | Operating Cash | | 42.00 | |
| AJE-5 | 101000 | Operating Cash | 9.75 | | Record interest earned 2026-08-29 per bank B17, not in the GL. **Credit account undetermined** — no interest-income account exists in the chart of accounts (`01`). Controller to designate the account or add one; the preparer will not invent one. |
| AJE-5 | *TBD* | *interest income — to be designated by Controller* | | 9.75 | |

Items needing **no** GL entry: C-1 (outstanding check cleared — timing), R-7 (check written and voided, net zero).

## 8. Unresolved exceptions

- **The R-2 / R-3 classification is not resolved** — GL error vs bank error (§6). Both readings are disclosed; the reconciliation residual is 0.00 either way, but the required corrective action differs and is a Controller decision.
- **Duplicate bank row B10 (3,300.00)** is set aside per Controller direction, not confirmed as spurious (I-1). If it is a genuine transaction, the bank side does not reconcile by 3,300.00.
- **AJE-5 has no valid credit account** in the chart (§7).

No unexplained monetary residual exists: the (6,724.25) difference is fully explained (§6 proof, residual 0.00).

## 9. Open observations

Content that does not change the reconciliation but that a reviewer should know about. This
consolidates disclosures that otherwise appear only in passing elsewhere in this workpaper
(§3's integrity-findings table, §5's carryover note, and §12's action item 7); it does not
replace those mentions, which remain in place as cross-references to this section.

**Recurring cutoff pattern — bank deposit dated the last day of a month; GL receipt posted
the first of the next month.**

- **August (finding I-2):** Bank row B01 — "Customer deposit J," 2,600.00 — carries a
  2026-07-31 date in the August bank file, while the corresponding GL entry G02 — "AR
  receipt J" — is dated 2026-08-01. The two are matched at a 1-day gap, within the 5-day
  window, on exact amount and corroborating description (§6, pair 1). Each side sits in its
  own period's reported population (§3), so this is not a reconciling item and has no effect
  on either roll-forward.
- **July precedent (item C-3, prior workpaper):** The same pattern occurred one month
  earlier — "AR receipt E" (7,400.00) was dated 2026-08-01 in the GL but tied to a bank
  deposit that had cleared 2026-07-31, per the July workpaper. Checked directly against the
  August source files (§5): no "deposit E" appears in `august-2026-bank.csv` and no "AR
  receipt E" appears in `august-2026-gl-cash.csv` — the item was not duplicated into August.

Two occurrences in two consecutive months of the same bank-cleared-last-day /
GL-posted-first-day pattern is not, by itself, an error — a deposit can legitimately clear a
day before the corresponding AR receipt is posted. But it is a pattern rather than a
one-off, and it is disclosed here — rather than resolved — because resolving it would
require visibility into the bank's and the AR system's posting timestamps, which this
reconciliation's source data does not provide. It is worth the Controller's attention as a
cutoff-testing question and possibly a GL posting-date-convention question, independent of
either month's individual reconciliation conclusion.

This observation does not affect the residual proof (§6) or the conclusion (§12) in either
period.

## 10. Engagement parameters

Supplied by the Controller for **this engagement only** on 2026-08-29; not standing rules and not carried forward (`04` "Judgment").

| Parameter | Value | Applied where |
|---|---|---|
| Matching tolerance (amount) | $0.00 — exact | §6 matching; caused B07/G09 and B08/G10 to remain unmatched |
| Date window | 5 days | §6 matching; pair 1 (B01/G02) accepted at a 1-day gap |
| Escalation threshold | $200.00 | §11 |
| Materiality | Not specified | Working assumption below |

**Materiality — working assumption (preparer, flagged):** no materiality floor is applied. Every unmatched item and every apparent error is investigated, classified, and disclosed regardless of amount; nothing is netted or waived as immaterial. Amount-based escalation uses the $200.00 threshold; items below it are still escalated when unusual **in kind** (an apparent posting error, a chart-of-accounts gap). If the Controller intends a different treatment, this reconciliation should be revisited.

## 11. Escalation assessment

Threshold: **$200.00** (Controller, 2026-08-29). Items are also escalated below the threshold when unusual in kind.

| Item | Amount | Meets $200? | Unusual in kind? | Escalated? | Reason |
|---|---:|---|---|---|---|
| I-1 duplicate bank row B10 | 3,300.00 | Yes | Yes — data integrity | **Yes** | Bank detail vs summary inconsistency; conclusion depends on it being spurious |
| R-1 Vendor Zeta sign error | 4,820.00 | Yes | Yes — posting error | **Yes** | GL correction required |
| R-3 second Vendor Delta payment | 1,845.00 | Yes | Yes — omitted entry or bank double-charge | **Yes** | Two readings; corrective action is a Controller decision |
| I-3 AR write-off in cash file (acct 110000) | 1,250.00 | Yes | Yes — wrong file/account | **Yes** | Coding and data-sourcing question |
| R-2 Vendor Theta amount error | 27.00 | No | Yes — posting error / bank error | **Yes** | Escalated on kind, not amount |
| R-5 interest earned — no income account | 9.75 | No | Yes — chart-of-accounts gap | **Yes** | Escalated on kind; Controller must designate an account |
| R-4 bank service charge | 42.00 | No | No — routine unrecorded fee, supported | No | Adjustment proposed (AJE-4); same as July T-2 |
| C-1 Check 1048 cleared | 620.00 | — | No — expected timing resolution | No | Prior-period item, resolved in August |
| R-7 Check 1052 written/voided | 0.00 | No | No | No | Net zero; disclosed |
| I-2 deposit J dated 2026-07-31 | 0.00 (matched) | No | Minor — recurring cutoff pattern | No | Disclosed observation; noted for cutoff testing |

## 12. Conclusion

**Account 101000 Operating Cash conditionally reconciles for August 2026, contingent on treating duplicate bank row B10 (3,300.00) as a spurious, unconfirmed data artifact — see the caveats below.** Subject to that contingency: the (6,724.25) difference between the bank ending balance of 78,659.75 (excluding duplicate row B10) and the GL ending balance of 85,384.00 is fully explained by supported reconciling items with a residual of **0.00**, and nothing was plugged, forced, or assumed. Adjusted bank and adjusted book balances both equal **78,659.75** under the primary (GL-error) reading, or **80,531.75** under the bank-error reading; the residual is 0.00 either way.

**The GL is not correct as reported.** Bringing adjusted book into agreement requires five proposed adjustments with a net cash effect of **(6,724.25)**: AJE-1 (4,820.00), AJE-2 (27.00), AJE-3 (1,845.00), AJE-4 (42.00), AJE-5 +9.75. None are posted.

**Caveats:** (1) the clean result depends on treating duplicate bank row B10 (3,300.00) as a spurious data artifact per Controller direction — if B10 is a genuine transaction the bank side is unreconciled by 3,300.00; (2) R-2 and R-3 are presented as GL errors but may be bank errors requiring investigation rather than GL adjustments.

### What the Controller must act on

1. **Approve or reject the proposed adjustments** AJE-1 through AJE-5 (§7). Net cash effect (6,724.25).
2. **Designate the credit account for AJE-5** (interest earned, 9.75) — no interest-income account exists in the chart of accounts; add one or specify coding. The preparer will not invent an account.
3. **Decide the R-2 / R-3 classification** (§6, §8): GL errors (post AJE-2, AJE-3) or bank errors (open a bank investigation for the 27.00 Theta overcharge and the 1,845.00 duplicate Delta ACH; post neither adjustment).
4. **Direct the disposition of duplicate bank row B10** (I-1, 3,300.00): confirm whether the bank record is one deposit K or two, and obtain a corrected bank file if the summary is wrong. Confirm whether GL "AR receipt K" (G11, 3,300.00) is correct as a single receipt.
5. **Confirm the coding / sourcing of GL row G08** (I-3): an AR write-off (1,250.00) posted to account 110000 appears in `august-2026-gl-cash.csv`; confirm it is correctly excluded from the cash reconciliation and why it is in this file.
6. **Confirm July AJE-1 (35.00 bank fee) was posted** (§4, §5 C-2) — the August GL beginning balance implies it was, but there is no direct posting confirmation in the August source data.
7. **Note the recurring cutoff pattern** (I-2 / July C-3): deposits dated the last day of a month posting to the GL on the first of the next. No August reconciliation effect; relevant to cutoff testing and the GL posting-date convention. See **§9 Open observations** for the consolidated disclosure.
8. **Confirm Check 1052** (R-7) is genuinely voided and no payment to Acme Freight is outstanding.

## 13. Judgment log

| # | Judgment | Basis | Source of authority |
|---:|---|---|---|
| J-1 | Exclude duplicate bank row B10 from matching and totals; keep it disclosed as an integrity finding and an escalation | Bank detail with B10 over-explains the reported bank ending by exactly 3,300.00; reported summary reflects a single deposit K | Controller instruction, 2026-08-29; `04` §2 |
| J-2 | Do not conclude B10 is spurious; state the conclusion's dependence on that treatment | Data does not exclude a genuine second same-day deposit of equal amount | `03` §4; CLAUDE.md "nothing is assumed"; preparer inference (labelled) |
| J-3 | GL net computed from the 14 rows posted to 101000, excluding G08 (110000); G08 reported, not silently dropped | Only in-scope rows belong in the account roll-forward; excluding G08 ties the GL side to its TB and TB net | `source-population-validation` skill §1; `01` chart of accounts |
| J-4 | 620.00 beginning-balance difference identified as the July Check 1048 carryforward, resolved by B03 clearing in August | Amount and description tie to July workpaper item T-1; bank B03 shows the clearing | `04` §2; `workpapers/2026-07 operating-cash-reconciliation.md` |
| J-5 | Matching parameters: exact amount ($0.00), 5-day window; escalation threshold $200.00 | Supplied for this engagement; **not** standing rules, not carried forward | Controller instruction, 2026-08-29; `04` "Judgment" |
| J-6 | Vendor-payment corrections (AJE-1 to AJE-3) offset to 200000 Accounts Payable | Vendor payments normally relieve AP; no AP subledger or invoice support available — flagged for confirmation | Preparer inference (labelled); `01` chart of accounts |
| J-7 | R-1 (Zeta) presented as a GL sign error requiring adjustment | Bank B07 is a (2,410.00) outflow; GL G09 is +2,410.00; every other vendor payment in the file is negative | `04` §4; preparer inference (labelled) |
| J-8 | R-2 (Theta 27.00) and R-3 (Delta 1,845.00) left with two readings — GL error or bank error — not resolved | Data supports both; residual is 0.00 either way; corrective action differs and is a Controller decision | `03` §4; `04` §4 |
| J-9 | R-4 (42.00 bank fee) proposed as an adjustment, not escalated | Routine unrecorded bank fee, fully supported, below the $200 threshold, not unusual in kind; consistent with July T-2 | `04` §5; Controller threshold 2026-08-29 |
| J-10 | R-5 (9.75 interest) escalated despite being below threshold; no credit account assumed | No interest-income account in the chart; a chart-of-accounts gap is unusual in kind; "do not invent accounts" | CLAUDE.md conventions; `01`; `03` §5 |
| J-11 | R-7 (Check 1052 written and voided) treated as net-zero, no adjustment; confirmation still requested | G04 and G06 offset exactly; no bank clearing | `04` §4; preparer inference (labelled) |
| J-12 | Materiality: no floor applied; every item investigated and disclosed regardless of amount | No materiality threshold supplied; `03` §3 and §6 require identification and classification of all reconciling items | `03` §3, §6; preparer working assumption (flagged, §10) |
| J-13 | July AJE-1 treated as posted for continuity purposes, with Controller confirmation requested | August GL beginning (73,440.00) = July TB ending (73,475.00) − 35.00; exact match to July AJE-1 | `04` §2; preparer inference (labelled) |
| J-14 | B01 (2026-07-31 date in the August bank file) matched to G02 and disclosed as observation I-2, not treated as a reconciling item | Exact amount, 1-day gap within the 5-day window, corroborating description; each side sits in its own period population | J-5; `source-population-validation` skill §1, §4 |

---

*Prepared by the Staff Accountant. Not effective until independently reviewed and approved by the Controller per `05 independent-review-control.md`.*
