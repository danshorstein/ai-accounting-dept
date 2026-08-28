#!/usr/bin/env python3
"""
Generates the August 2026 test fixtures (bank.csv, gl-cash.csv, bank-summary.csv,
trial-balance.csv) and the answer key JSON from ONE source of truth, so the CSVs
and the answer key can never drift from each other by transcription error.

Every dollar figure is computed here, and the script asserts that the "nothing
plugged" proof resolves to an exact zero residual before writing anything out.
"""
import argparse
import csv
import json
import os
import sys
from decimal import Decimal as D

PERIOD = "2026-08"
ACCOUNT = "101000"

# ---------------------------------------------------------------------------
# Beginning balances
# ---------------------------------------------------------------------------
# Bank beginning = July's actual bank-summary ending balance (74,060.00),
# carried in raw (unadjusted) form -- the bank doesn't know about outstanding
# checks.
BANK_BEGIN = D("74060.00")

# GL beginning = July's TB ending (73,475.00) LESS the 35.00 bank-fee AJE
# (AJE-1) proposed in the July workpaper, assumed approved and posted before
# August activity. This is a deliberate scripted fact for this test, not
# something the model needs to derive.
GL_BEGIN = D("73475.00") - D("35.00")  # 73440.00

# ---------------------------------------------------------------------------
# Bank transaction detail (as extracted -- includes one data-entry glitch: a
# literal duplicate row, tag DUPLICATE_ROW). Each row: id, date, description,
# amount, tag, note.
# ---------------------------------------------------------------------------
BANK_ROWS = [
    dict(id="B01", date="2026-07-31", description="Customer deposit J", amount="2600.00",
         tag="CUTOFF_PRE_PERIOD", note="Cleared 2026-07-31 per bank; matches GL AR receipt J posted 2026-08-01."),
    dict(id="B02", date="2026-08-01", description="Customer deposit F", amount="5200.00",
         tag="CLEAN_MATCH", note="Matches G01."),
    dict(id="B03", date="2026-08-04", description="Check 1048 - Office Supply Co", amount="-620.00",
         tag="PRIOR_PERIOD_CARRYFORWARD",
         note="Outstanding check disclosed in the July 2026 workpaper (ref T-1); clears the bank this period. Already recorded in GL in July -- no August GL entry."),
    dict(id="B04", date="2026-08-05", description="ACH Vendor Alpha", amount="-3410.00",
         tag="CLEAN_MATCH", note="Matches G03."),
    dict(id="B05", date="2026-08-06", description="ACH Vendor Delta", amount="-1845.00",
         tag="CLEAN_MATCH", note="Matches G05."),
    dict(id="B06", date="2026-08-09", description="Customer deposit G", amount="7850.00",
         tag="CLEAN_MATCH", note="Matches G07."),
    dict(id="B07", date="2026-08-12", description="ACH Vendor Zeta", amount="-2410.00",
         tag="GL_SIGN_ERROR", note="GL recorded this payment with the wrong sign (G09)."),
    dict(id="B08", date="2026-08-14", description="ACH Vendor Theta", amount="-5463.00",
         tag="GL_TRANSPOSITION_ERROR", note="GL recorded 5,436.00 for this payment (G10) -- digits transposed, 27.00 off."),
    dict(id="B09", date="2026-08-15", description="Customer deposit K", amount="3300.00",
         tag="CLEAN_MATCH", note="Matches G11. The real transaction."),
    dict(id="B10", date="2026-08-15", description="Customer deposit K", amount="3300.00",
         tag="DUPLICATE_ROW", note="Exact duplicate of B09 (same date/description/amount) -- an extract artifact, not a second real deposit. Excluded from the bank population; the real bank statement ending balance does not include it."),
    dict(id="B11", date="2026-08-15", description="Payroll", amount="-10200.00",
         tag="CLEAN_MATCH", note="Matches G12."),
    dict(id="B12", date="2026-08-18", description="Customer deposit H", amount="6300.00",
         tag="CLEAN_MATCH", note="Matches G13."),
    dict(id="B13", date="2026-08-20", description="ACH Vendor Delta", amount="-1845.00",
         tag="BANK_ONLY_INVESTIGATION",
         note="Second ACH debit to the same vendor for the identical amount two weeks after B05, with no corresponding GL entry authorizing a second payment. Ambiguous in kind (possible duplicate bank pull vs. a real unrecorded second payment) -- requires investigation, not assumption either way."),
    dict(id="B14", date="2026-08-22", description="ACH Vendor Beta", amount="-2975.00",
         tag="CLEAN_MATCH", note="Matches G14."),
    dict(id="B15", date="2026-08-27", description="Customer deposit I", amount="8150.00",
         tag="CLEAN_MATCH", note="Matches G15."),
    dict(id="B16", date="2026-08-29", description="Bank service charge", amount="-42.00",
         tag="UNRECORDED_BANK_FEE", note="Not recorded in GL."),
    dict(id="B17", date="2026-08-29", description="Interest earned", amount="9.75",
         tag="UNRECORDED_BANK_INTEREST_NO_COA",
         note="Not recorded in GL. No interest-income account exists in the chart of accounts (references/01 company-profile.md)."),
]

# ---------------------------------------------------------------------------
# GL cash detail (as extracted -- includes one scope glitch: a row actually
# posted to 110000 Accounts Receivable that leaked into the 101000 extract).
# ---------------------------------------------------------------------------
GL_ROWS = [
    dict(id="G01", date="2026-08-01", description="AR receipt F", amount="5200.00", account="101000",
         tag="CLEAN_MATCH", note="Matches B02."),
    dict(id="G02", date="2026-08-01", description="AR receipt J", amount="2600.00", account="101000",
         tag="CUTOFF_PRE_PERIOD", note="Matches B01 (bank-dated 2026-07-31); one-day cutoff gap, same pattern disclosed in the July workpaper."),
    dict(id="G03", date="2026-08-05", description="Vendor Alpha payment", amount="-3410.00", account="101000",
         tag="CLEAN_MATCH", note="Matches B04."),
    dict(id="G04", date="2026-08-05", description="Check 1052 - Acme Freight", amount="-890.00", account="101000",
         tag="VOIDED_CHECK_LEG", note="Voided in G06 before ever presented to the bank -- nets to zero, no bank impact."),
    dict(id="G05", date="2026-08-06", description="Vendor Delta payment", amount="-1845.00", account="101000",
         tag="CLEAN_MATCH", note="Matches B05."),
    dict(id="G06", date="2026-08-07", description="Void Check 1052 - Acme Freight", amount="890.00", account="101000",
         tag="VOIDED_CHECK_LEG", note="Reverses G04. Net zero, self-cancelling, not an outstanding check."),
    dict(id="G07", date="2026-08-09", description="AR receipt G", amount="7850.00", account="101000",
         tag="CLEAN_MATCH", note="Matches B06."),
    dict(id="G08", date="2026-08-11", description="AR write-off - Bright Retailers", amount="-1250.00", account="110000",
         tag="FOREIGN_ACCOUNT", note="Posted to 110000 Accounts Receivable, not 101000. Leaked into this extract in error -- out of scope for the cash reconciliation and must be excluded from the roll-forward."),
    dict(id="G09", date="2026-08-12", description="Vendor Zeta payment", amount="2410.00", account="101000",
         tag="GL_SIGN_ERROR", note="Should be -2,410.00 (matches B07); recorded with the wrong sign."),
    dict(id="G10", date="2026-08-14", description="Vendor Theta payment", amount="-5436.00", account="101000",
         tag="GL_TRANSPOSITION_ERROR", note="Should be -5,463.00 (matches B08); digits transposed."),
    dict(id="G11", date="2026-08-15", description="AR receipt K", amount="3300.00", account="101000",
         tag="CLEAN_MATCH", note="Matches B09 (the real deposit, not the duplicate B10)."),
    dict(id="G12", date="2026-08-15", description="Payroll run", amount="-10200.00", account="101000",
         tag="CLEAN_MATCH", note="Matches B11."),
    dict(id="G13", date="2026-08-18", description="AR receipt H", amount="6300.00", account="101000",
         tag="CLEAN_MATCH", note="Matches B12."),
    dict(id="G14", date="2026-08-22", description="Vendor Beta payment", amount="-2975.00", account="101000",
         tag="CLEAN_MATCH", note="Matches B14."),
    dict(id="G15", date="2026-08-27", description="AR receipt I", amount="8150.00", account="101000",
         tag="CLEAN_MATCH", note="Matches B15."),
]

# ---------------------------------------------------------------------------
# Derived figures
# ---------------------------------------------------------------------------
def amt(row):
    return D(row["amount"])

bank_all_sum = sum(amt(r) for r in BANK_ROWS)
bank_true_sum = sum(amt(r) for r in BANK_ROWS if r["tag"] != "DUPLICATE_ROW")
bank_true_ending = BANK_BEGIN + bank_true_sum

gl_in_scope = [r for r in GL_ROWS if r["account"] == ACCOUNT]
gl_in_scope_sum = sum(amt(r) for r in gl_in_scope)
gl_ending = GL_BEGIN + gl_in_scope_sum

# unmatched (non-clean, non-excluded, non-carryforward) bank items that count
# toward THIS period's residual
bank_unmatched_current = [r for r in BANK_ROWS
                           if r["tag"] not in ("CLEAN_MATCH", "CUTOFF_PRE_PERIOD",
                                               "DUPLICATE_ROW", "PRIOR_PERIOD_CARRYFORWARD")]
gl_unmatched_current = [r for r in gl_in_scope
                         if r["tag"] not in ("CLEAN_MATCH", "CUTOFF_PRE_PERIOD")]

bank_unmatched_sum = sum(amt(r) for r in bank_unmatched_current)
gl_unmatched_sum = sum(amt(r) for r in gl_unmatched_current)

raw_difference = bank_true_ending - gl_ending  # bank - gl
beginning_difference = BANK_BEGIN - GL_BEGIN   # carried forward by B03/T-1
# B03 (the prior-period carryforward) is excluded from bank_unmatched_current
# by construction, because its dollar impact already IS the beginning-balance
# gap resolving itself -- it is not a new item to add on top of that gap.
proof = bank_unmatched_sum - gl_unmatched_sum
residual = raw_difference - proof

print(f"Bank true ending balance  : {bank_true_ending}")
print(f"GL / TB ending balance    : {gl_ending}")
print(f"Raw difference (bank-gl)  : {raw_difference}")
print(f"Beginning balance gap     : {beginning_difference}  (= B03/Check 1048)")
print(f"Bank unmatched (current)  : {bank_unmatched_sum}")
print(f"GL unmatched (current)    : {gl_unmatched_sum}")
print(f"Proof total               : {proof}")
print(f"RESIDUAL (must be 0)      : {residual}")

assert residual == D("0.00"), f"Residual not zero: {residual}"
assert gl_in_scope_sum == D("11944.00")
assert bank_true_sum == D("4599.75")

# ---------------------------------------------------------------------------
# Parse args -- the answer key has no in-repo default on purpose. See
# eval/README.md: the answer key must never be committed to this repository,
# because the Staff Accountant agent's tools can read anything in the
# working tree. Passing --answer-key-out inside the repo is refused below.
# ---------------------------------------------------------------------------
ap = argparse.ArgumentParser()
ap.add_argument("--data-dir", default="data",
                 help="Where to write the four CSVs (default: data/, i.e. run this from the repo root)")
ap.add_argument("--answer-key-out", required=True,
                 help="Where to write the answer key JSON. Must be OUTSIDE this repository's working tree.")
args = ap.parse_args()

repo_root = os.path.abspath(os.getcwd())
answer_key_abs = os.path.abspath(args.answer_key_out)
if answer_key_abs == repo_root or answer_key_abs.startswith(repo_root + os.sep):
    sys.exit(f"Refusing to write the answer key inside the repository ({answer_key_abs}). "
              f"Pass a path outside {repo_root}.")

os.makedirs(args.data_dir, exist_ok=True)
os.makedirs(os.path.dirname(answer_key_abs) or ".", exist_ok=True)

# ---------------------------------------------------------------------------
# Write CSVs
# ---------------------------------------------------------------------------
OUT = args.data_dir

with open(f"{OUT}/august-2026-bank.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "date", "description", "amount"])
    for r in BANK_ROWS:
        w.writerow([r["id"], r["date"], r["description"], r["amount"]])

with open(f"{OUT}/august-2026-gl-cash.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "date", "description", "amount", "account"])
    for r in GL_ROWS:
        w.writerow([r["id"], r["date"], r["description"], r["amount"], r["account"]])

with open(f"{OUT}/august-2026-bank-summary.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["account", "period", "beginning_balance", "ending_balance"])
    w.writerow(["Operating Checking", PERIOD, str(BANK_BEGIN), str(bank_true_ending)])

with open(f"{OUT}/august-2026-trial-balance.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["account", "account_name", "period", "beginning_balance", "debits_credits_net", "ending_balance"])
    w.writerow([ACCOUNT, "Operating Cash", PERIOD, str(GL_BEGIN), str(gl_in_scope_sum), str(gl_ending)])

# ---------------------------------------------------------------------------
# Build answer key
# ---------------------------------------------------------------------------
def find(rows, rid):
    return next(r for r in rows if r["id"] == rid)

population_findings = [
    {
        "id": "PF-1", "source": "bank", "row_ids": ["B10"],
        "finding_type": "duplicate_row",
        "excluded_from_population": True,
        "expected_description_contains": ["duplicate", "3,300", "3300"],
    },
    {
        "id": "PF-2", "source": "gl", "row_ids": ["G08"],
        "finding_type": "foreign_account",
        "excluded_from_population": True,
        "foreign_account": "110000",
        "expected_description_contains": ["110000", "Accounts Receivable", "foreign", "out of scope", "out-of-scope"],
    },
    {
        "id": "PF-3", "source": "both", "row_ids": ["B01", "G02"],
        "finding_type": "out_of_period_disclosed_not_reconciling_item",
        "excluded_from_population": False,
        "expected_description_contains": ["2026-07-31", "cutoff"],
    },
]

matches = []
for b, g in [("B02", "G01"), ("B04", "G03"), ("B05", "G05"), ("B06", "G07"),
             ("B09", "G11"), ("B11", "G12"), ("B12", "G13"), ("B14", "G14"),
             ("B15", "G15")]:
    matches.append({"bank_row_id": b, "gl_row_id": g, "match_type": "exact", "date_gap_days": 0})
matches.append({"bank_row_id": "B01", "gl_row_id": "G02", "match_type": "date_window", "date_gap_days": 1})

reconciling_items = [
    {
        "ref": "R-1",
        "bank_row_ids": ["B03"], "gl_row_ids": [],
        "amount": "-620.00",
        "classification": "timing_difference",
        "is_prior_period_carryforward": True,
        "affects_current_period_residual": False,
        "proposed_adjustment_required": False,
        "escalated": False,
        "must_reference": "July 2026 workpaper item T-1 / Controller action item 3",
    },
    {
        "ref": "R-2",
        "bank_row_ids": ["B07"], "gl_row_ids": ["G09"],
        "amount": "-4820.00",
        "amount_note": "Net correction: GL recorded +2,410.00, should be -2,410.00 -- a 4,820.00 swing.",
        "classification": "gl_exception",
        "is_prior_period_carryforward": False,
        "affects_current_period_residual": True,
        "proposed_adjustment_required": True,
        "proposed_adjustment_credit_account": "101000",
        "proposed_adjustment_debit_account": None,
        "debit_account_note": "Offsetting account not determinable from the cash extract alone -- must not be invented; escalate for the correct coding.",
        "escalated": True,
    },
    {
        "ref": "R-3",
        "bank_row_ids": ["B08"], "gl_row_ids": ["G10"],
        "amount": "-27.00",
        "amount_note": "Bank -5,463.00 vs GL -5,436.00 -- transposition, 27.00 difference.",
        "classification": "gl_exception",
        "is_prior_period_carryforward": False,
        "affects_current_period_residual": True,
        "proposed_adjustment_required": True,
        "proposed_adjustment_credit_account": "101000",
        "proposed_adjustment_debit_account": None,
        "debit_account_note": "Offsetting account not determinable from the cash extract alone -- must not be invented; escalate for the correct coding.",
        "escalated": True,
    },
    {
        "ref": "R-4",
        "bank_row_ids": ["B13"], "gl_row_ids": [],
        "amount": "-1845.00",
        "classification": "bank_exception",
        "is_prior_period_carryforward": False,
        "affects_current_period_residual": True,
        "proposed_adjustment_required": False,
        "escalated": True,
        "escalation_reason": "Ambiguous in kind (possible duplicate bank pull vs. an unrecorded second payment), not merely amount -- must not be assumed either way.",
    },
    {
        "ref": "R-5",
        "bank_row_ids": ["B16"], "gl_row_ids": [],
        "amount": "-42.00",
        "classification": "gl_exception",
        "is_prior_period_carryforward": False,
        "affects_current_period_residual": True,
        "proposed_adjustment_required": True,
        "proposed_adjustment_debit_account": "620000",
        "proposed_adjustment_credit_account": "101000",
        "escalated": False,
    },
    {
        "ref": "R-6",
        "bank_row_ids": ["B17"], "gl_row_ids": [],
        "amount": "9.75",
        "classification": "gl_exception",
        "is_prior_period_carryforward": False,
        "affects_current_period_residual": True,
        "proposed_adjustment_required": True,
        "proposed_adjustment_debit_account": "101000",
        "proposed_adjustment_credit_account": None,
        "credit_account_note": "No interest-income account exists in the chart of accounts. Must not invent one -- escalate for account guidance before posting.",
        "escalated": True,
        "escalation_reason": "No chart-of-accounts entry fits; ambiguous in kind, immaterial in amount -- escalation is not about the 9.75.",
    },
    {
        "ref": "R-7",
        "bank_row_ids": [], "gl_row_ids": ["G04", "G06"],
        "amount": "0.00",
        "classification": "timing_difference",
        "is_prior_period_carryforward": False,
        "affects_current_period_residual": True,
        "proposed_adjustment_required": False,
        "escalated": False,
        "must_not": "Must NOT be reported as an 890.00 outstanding check -- G04 and G06 self-cancel and never reached the bank.",
    },
]

answer_key = {
    "period": PERIOD,
    "account": ACCOUNT,
    "balances": {
        "bank_beginning": str(BANK_BEGIN),
        "bank_ending_reported": str(bank_true_ending),
        "gl_beginning": str(GL_BEGIN),
        "gl_ending": str(gl_ending),
    },
    "population_findings": population_findings,
    "matches": matches,
    "reconciling_items": reconciling_items,
    "residual_unexplained_difference": "0.00",
    "account_reconciles": True,
    "diagnostic_math": {
        "raw_difference_bank_minus_gl": str(raw_difference),
        "beginning_balance_gap": str(beginning_difference),
        "bank_unmatched_current_period_sum": str(bank_unmatched_sum),
        "gl_unmatched_current_period_sum": str(gl_unmatched_sum),
    },
}

with open(answer_key_abs, "w") as f:
    json.dump(answer_key, f, indent=2)

print(f"\nWrote CSVs to {os.path.abspath(OUT)}")
print(f"Wrote answer key to {answer_key_abs} (OUTSIDE the repo -- keep it that way)")
print("Bank rows:", len(BANK_ROWS), " GL rows:", len(GL_ROWS), f"({len(gl_in_scope)} in-scope)")
