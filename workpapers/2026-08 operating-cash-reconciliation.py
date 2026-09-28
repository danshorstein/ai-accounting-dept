"""August 2026 operating cash (101000) - source population validation.

Run from the repository root:
    python3 "workpapers/2026-08 operating-cash-reconciliation.py"

Scope: validation gate only (roll-forwards, scope and integrity checks). No matching
is performed because the bank roll-forward does not tie (see workpaper section 4).
All inputs are located relative to the repository root.
"""
import csv
from collections import Counter
from decimal import Decimal as D

PERIOD_START, PERIOD_END = "2026-08-01", "2026-08-31"
GL_ACCOUNT = "101000"


def rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


bank = rows("data/august-2026-bank.csv")
gl = rows("data/august-2026-gl-cash.csv")
bsum = rows("data/august-2026-bank-summary.csv")[0]
tb = rows("data/august-2026-trial-balance.csv")[0]
jul_bsum = rows("data/july-2026-bank-summary.csv")[0]
jul_tb = rows("data/july-2026-trial-balance.csv")[0]

print("ROW COUNTS: bank", len(bank), "| gl", len(gl), "| bank summary 1 | tb 1")
print("Bank summary:", bsum["account"], bsum["period"])
print("TB:", tb["account"], tb["account_name"], tb["period"])

# Bank roll-forward
b_beg, b_end = D(bsum["beginning_balance"]), D(bsum["ending_balance"])
b_act = sum(D(r["amount"]) for r in bank)
print("\nBANK ROLL-FORWARD")
print("beginning", b_beg, "| activity", b_act, "| calculated ending", b_beg + b_act,
      "| reported ending", b_end, "| DIFFERENCE", b_beg + b_act - b_end)

# GL roll-forward
g_beg, g_end, g_net = D(tb["beginning_balance"]), D(tb["ending_balance"]), D(tb["debits_credits_net"])
g_all = sum(D(r["amount"]) for r in gl)
g_in = sum(D(r["amount"]) for r in gl if r["account"] == GL_ACCOUNT)
foreign = [r for r in gl if r["account"] != GL_ACCOUNT]
print("\nGL ROLL-FORWARD")
print("beginning", g_beg, "| all-row total", g_all, "| 101000-only total", g_in)
print("calculated ending (101000 rows)", g_beg + g_in, "| reported ending", g_end,
      "| DIFFERENCE", g_beg + g_in - g_end)
print("TB net", g_net, "| 101000 detail", g_in, "| DIFFERENCE", g_in - g_net)
print("calculated ending (ALL rows, for reference)", g_beg + g_all, "| DIFFERENCE", g_beg + g_all - g_end)
for r in foreign:
    print("FOREIGN ACCOUNT ROW:", r["id"], r["date"], r["description"], r["amount"], r["account"])

# Scope / integrity
print("\nDATE RANGE bank", min(r["date"] for r in bank), max(r["date"] for r in bank),
      "| gl", min(r["date"] for r in gl), max(r["date"] for r in gl))
for name, data in (("bank", bank), ("gl", gl)):
    for r in data:
        if not PERIOD_START <= r["date"] <= PERIOD_END:
            print("OUT OF PERIOD", name, r["id"], r["date"], r["description"], r["amount"])
    c = Counter((r["date"], r["amount"], r["description"]) for r in data)
    for k, n in c.items():
        if n > 1:
            print("DUPLICATE", name, k, "x", n, [r["id"] for r in data
                  if (r["date"], r["amount"], r["description"]) == k])
    print(name, "zero/blank/non-numeric amounts:",
          [r["id"] for r in data if not r["amount"].strip() or D(r["amount"]) == 0])

# Repeated description+amount on different dates (disclosure only, not treated as duplicates)
c2 = Counter((r["description"], r["amount"]) for r in bank)
for k, n in c2.items():
    if n > 1:
        print("SAME DESCRIPTION+AMOUNT, DIFFERENT/ANY DATE (bank):", k, [r["id"] + " " + r["date"] for r in bank
              if (r["description"], r["amount"]) == k])

# Beginning balances and prior-period continuity
print("\nBEGINNING BALANCES bank", b_beg, "| GL", g_beg, "| bank - GL", b_beg - g_beg)
print("PRIOR-PERIOD CONTINUITY (prior figures read from July source files)")
print("bank: July ending", jul_bsum["ending_balance"], "vs Aug beginning", b_beg,
      "diff", b_beg - D(jul_bsum["ending_balance"]))
print("GL: July TB ending", jul_tb["ending_balance"], "vs Aug TB beginning", g_beg,
      "diff", g_beg - D(jul_tb["ending_balance"]))
print("Raw ending difference bank - GL (reported):", b_end, "-", g_end, "=", b_end - g_end)

# Sensitivity facts for the reviewer (no matching performed)
print("\nBANK ROLL-FORWARD DIFFERENCE", b_beg + b_act - b_end,
      "| amount of B10", next(D(r["amount"]) for r in bank if r["id"] == "B10"))
