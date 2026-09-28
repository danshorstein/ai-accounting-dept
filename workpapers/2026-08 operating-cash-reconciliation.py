"""August 2026 operating cash (101000) - validation, matching and reconciliation.

Run from the repository root:
    python3 "workpapers/2026-08 operating-cash-reconciliation.py"

Prints every figure cited in "2026-08 operating-cash-reconciliation.md".
All inputs are read from data/ by path relative to the repository root.

Engagement parameters (Controller direction, this engagement only, not standing rules):
    matching tolerance exact amount ($0.00); date window 5 days; escalation threshold $200.00.
    No materiality figure was specified and none is used.
Controller direction: bank row B10 is set aside (excluded from the reconciled bank
population) as a likely data-quality artifact. It stays disclosed and escalated.
"""
import csv
from collections import Counter
from datetime import date
from decimal import Decimal as D

PERIOD_START, PERIOD_END = "2026-08-01", "2026-08-31"
GL_ACCOUNT = "101000"
TOLERANCE = D("0.00")
WINDOW_DAYS = 5
ESCALATION_THRESHOLD = D("200.00")
SET_ASIDE_BANK_IDS = {"B10"}

# Preparer-proposed pairings (bank id -> GL id). Each is re-tested below against the
# tolerance and the window; nothing is paired that fails either test.
PAIRS = {
    "B01": "G02", "B02": "G01", "B04": "G03", "B05": "G05", "B06": "G07",
    "B09": "G11", "B11": "G12", "B12": "G13", "B14": "G14", "B15": "G15",
}


def rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def fmt(x):
    return f"({abs(x):,.2f})" if x < 0 else f"{x:,.2f}"


def gap(d1, d2):
    return abs((date.fromisoformat(d1) - date.fromisoformat(d2)).days)


bank_all = rows("data/august-2026-bank.csv")
gl_all = rows("data/august-2026-gl-cash.csv")
bsum = rows("data/august-2026-bank-summary.csv")[0]
tb = rows("data/august-2026-trial-balance.csv")[0]
jul_bsum = rows("data/july-2026-bank-summary.csv")[0]
jul_tb = rows("data/july-2026-trial-balance.csv")[0]
jul_bank = rows("data/july-2026-bank.csv")
jul_gl = rows("data/july-2026-gl-cash.csv")

print("=== 1. ROW COUNTS ===")
print("bank", len(bank_all), "| gl", len(gl_all), "| bank summary 1 | tb 1 | july bank", len(jul_bank),
      "| july gl", len(jul_gl))
print("Bank summary:", bsum["account"], bsum["period"], "| TB:", tb["account"], tb["account_name"], tb["period"])

# ---------------------------------------------------------------- population gate
b_beg, b_end = D(bsum["beginning_balance"]), D(bsum["ending_balance"])
g_beg, g_end, g_net = D(tb["beginning_balance"]), D(tb["ending_balance"]), D(tb["debits_credits_net"])

print("\n=== 2. ROLL-FORWARD, BANK AS DELIVERED (17 rows) ===")
b_act_all = sum(D(r["amount"]) for r in bank_all)
print("beginning", fmt(b_beg), "| activity", fmt(b_act_all), "| calculated ending", fmt(b_beg + b_act_all),
      "| reported ending", fmt(b_end), "| DIFFERENCE", fmt(b_beg + b_act_all - b_end))

bank = [r for r in bank_all if r["id"] not in SET_ASIDE_BANK_IDS]
aside = [r for r in bank_all if r["id"] in SET_ASIDE_BANK_IDS]
b_act = sum(D(r["amount"]) for r in bank)
print("\n=== 2b. ROLL-FORWARD, BANK EXCLUDING SET-ASIDE ROWS", sorted(SET_ASIDE_BANK_IDS), "===")
for r in aside:
    print("SET ASIDE:", r["id"], r["date"], r["description"], fmt(D(r["amount"])))
print("rows", len(bank), "| beginning", fmt(b_beg), "| activity", fmt(b_act), "| calculated ending",
      fmt(b_beg + b_act), "| reported ending", fmt(b_end), "| DIFFERENCE", fmt(b_beg + b_act - b_end))

print("\n=== 3. ROLL-FORWARD, GL ===")
gl = [r for r in gl_all if r["account"] == GL_ACCOUNT]
foreign = [r for r in gl_all if r["account"] != GL_ACCOUNT]
g_in = sum(D(r["amount"]) for r in gl)
g_every = sum(D(r["amount"]) for r in gl_all)
print("beginning", fmt(g_beg), "| 101000 rows", len(gl), "activity", fmt(g_in), "| calculated ending",
      fmt(g_beg + g_in), "| reported ending", fmt(g_end), "| DIFFERENCE", fmt(g_beg + g_in - g_end))
print("TB net", fmt(g_net), "| 101000 detail", fmt(g_in), "| DIFFERENCE", fmt(g_in - g_net))
print("for reference, all 15 rows: activity", fmt(g_every), "calculated ending", fmt(g_beg + g_every),
      "DIFFERENCE vs TB", fmt(g_beg + g_every - g_end))
for r in foreign:
    print("FOREIGN ACCOUNT ROW:", r["id"], r["date"], r["description"], fmt(D(r["amount"])), r["account"])

print("\n=== 4. SCOPE / INTEGRITY ===")
print("date range bank", min(r["date"] for r in bank_all), max(r["date"] for r in bank_all),
      "| gl", min(r["date"] for r in gl_all), max(r["date"] for r in gl_all))
for name, data in (("bank", bank_all), ("gl", gl_all)):
    for r in data:
        if not PERIOD_START <= r["date"] <= PERIOD_END:
            print("OUT OF PERIOD", name, r["id"], r["date"], r["description"], fmt(D(r["amount"])))
    for k, n in Counter((r["date"], r["amount"], r["description"]) for r in data).items():
        if n > 1:
            print("DUPLICATE", name, k, "x", n, [r["id"] for r in data
                                                 if (r["date"], r["amount"], r["description"]) == k])
    print(name, "zero/blank/non-numeric amounts:",
          [r["id"] for r in data if not r["amount"].strip() or D(r["amount"]) == 0])
for k, n in Counter((r["description"], r["amount"]) for r in bank).items():
    if n > 1:
        print("SAME DESCRIPTION+AMOUNT (bank, not duplicates):", k,
              [r["id"] + " " + r["date"] for r in bank if (r["description"], r["amount"]) == k])
print("B01 present in july-2026-bank.csv:", any(r["description"] == "Customer deposit J" for r in jul_bank))

print("\n=== 5. BEGINNING BALANCES AND CONTINUITY FROM JULY ===")
print("beginning bank", fmt(b_beg), "| GL", fmt(g_beg), "| bank - GL", fmt(b_beg - g_beg))
jb_end, jg_end = D(jul_bsum["ending_balance"]), D(jul_tb["ending_balance"])
print("bank: July ending", fmt(jb_end), "vs Aug beginning", fmt(b_beg), "diff", fmt(b_beg - jb_end))
print("GL:   July TB ending", fmt(jg_end), "vs Aug TB beginning", fmt(g_beg), "diff", fmt(g_beg - jg_end))

# July carryover items, recomputed from July source files (exact amount, 5-day window)
jb_left = list(jul_bank)
jg_left = []
for g in jul_gl:
    hit = next((b for b in jb_left if D(b["amount"]) == D(g["amount"]) and gap(b["date"], g["date"]) <= WINDOW_DAYS), None)
    if hit:
        jb_left.remove(hit)
    else:
        jg_left.append(g)
print("July recomputed unmatched, bank only:", [(r["date"], r["description"], fmt(D(r["amount"]))) for r in jb_left])
print("July recomputed unmatched, GL only:  ", [(r["date"], r["description"], fmt(D(r["amount"]))) for r in jg_left])
jb_only = sum(D(r["amount"]) for r in jb_left)
jg_only = sum(D(r["amount"]) for r in jg_left)
print("July bank ending - GL ending", fmt(jb_end - jg_end), "| unmatched bank - unmatched GL",
      fmt(jb_only - jg_only))
jul_adj_book = jg_end + jb_only
jul_adj_bank = jb_end + jg_only
print("July adjusted bank", fmt(jul_adj_bank), "| July adjusted book (GL + unrecorded fee)", fmt(jul_adj_book),
      "| Aug GL beginning", fmt(g_beg), "| diff Aug GL beginning - July adjusted book", fmt(g_beg - jul_adj_book))
print("Aug opening bank - GL", fmt(b_beg - g_beg), "| July outstanding check", fmt(jg_only),
      "| residual", fmt(b_beg - g_beg + jg_only))
chk = [r for r in bank if "Check 1048" in r["description"]]
for r in chk:
    print("Aug bank row clearing July check:", r["id"], r["date"], r["description"], fmt(D(r["amount"])),
          "| July GL check date", jg_left[0]["date"], "| gap days", gap(r["date"], jg_left[0]["date"]),
          "| exact amount:", D(r["amount"]) == D(jg_left[0]["amount"]))
print("July fee (35.00) appears in August GL detail:", any(D(r["amount"]) == D("-35.00") for r in gl))

# ---------------------------------------------------------------- matching
print("\n=== 6. MATCHED ACTIVITY (exact amount, window", WINDOW_DAYS, "days) ===")
bmap = {r["id"]: r for r in bank}
gmap = {r["id"]: r for r in gl}
m_b = m_g = D(0)
for n, (bid, gid) in enumerate(PAIRS.items(), 1):
    b, g = bmap[bid], gmap[gid]
    diff = D(b["amount"]) - D(g["amount"])
    d = gap(b["date"], g["date"])
    assert abs(diff) <= TOLERANCE and d <= WINDOW_DAYS, (bid, gid)
    m_b += D(b["amount"])
    m_g += D(g["amount"])
    print(n, bid, b["date"], b["description"], fmt(D(b["amount"])), "|", gid, g["date"], g["description"],
          fmt(D(g["amount"])), "| gap", d, "| amount diff", fmt(diff))
print("matched pairs", len(PAIRS), "| bank total", fmt(m_b), "| GL total", fmt(m_g))
assert len(set(PAIRS.values())) == len(PAIRS)

un_b = [r for r in bank if r["id"] not in PAIRS]
un_g = [r for r in gl if r["id"] not in PAIRS.values()]
print("\nUNMATCHED BANK (excl. set-aside):")
for r in un_b:
    print(" ", r["id"], r["date"], r["description"], fmt(D(r["amount"])))
print("UNMATCHED GL (101000):")
for r in un_g:
    print(" ", r["id"], r["date"], r["description"], fmt(D(r["amount"])))
print("row accounting: bank", len(PAIRS), "matched +", len(un_b), "unmatched +", len(aside), "set aside =",
      len(PAIRS) + len(un_b) + len(aside), "of", len(bank_all))
print("row accounting: GL", len(PAIRS), "matched +", len(un_g), "unmatched +", len(foreign), "foreign =",
      len(PAIRS) + len(un_g) + len(foreign), "of", len(gl_all))
assert len(PAIRS) + len(un_b) + len(aside) == len(bank_all)
assert len(PAIRS) + len(un_g) + len(foreign) == len(gl_all)

# near-matches and sign flips, tested explicitly against the tolerance
print("\nNEAR-MATCH / SIGN TESTS (why these were not matched):")
for b in un_b:
    for g in un_g:
        d = D(b["amount"]) - D(g["amount"])
        if abs(D(b["amount"])) == abs(D(g["amount"])) and d != 0:
            print(" ", b["id"], "vs", g["id"], ": same absolute amount, opposite sign, signed diff", fmt(d),
                  "| date gap", gap(b["date"], g["date"]))
        elif 0 < abs(d) < 100 and D(b["amount"]) * D(g["amount"]) > 0 and gap(b["date"], g["date"]) <= WINDOW_DAYS:
            print(" ", b["id"], "vs", g["id"], ": signed diff", fmt(d), "outside $0.00 tolerance | date gap",
                  gap(b["date"], g["date"]))

# ---------------------------------------------------------------- proof against raw difference
print("\n=== 7. PROOF AGAINST THE RAW DIFFERENCE ===")
raw = b_end - g_end
ub = sum(D(r["amount"]) for r in un_b)
ug = sum(D(r["amount"]) for r in un_g)
print("balances: bank", fmt(b_end), "- GL", fmt(g_end), "= raw difference", fmt(raw))
print("unmatched bank", fmt(ub), "- unmatched GL", fmt(ug), "=", fmt(ub - ug))
print("plus opening difference (bank - GL at 08-01)", fmt(b_beg - g_beg), "=", fmt(ub - ug + b_beg - g_beg))
print("RESIDUAL unexplained (raw - (unmatched bank - unmatched GL + opening diff))",
      fmt(raw - (ub - ug + b_beg - g_beg)))
b03 = D(bmap["B03"]["amount"])
print("cross-check: B03 (clears July check 1048) removes opening item:", fmt(b_beg - g_beg), "+", fmt(b03), "=",
      fmt(b_beg - g_beg + b03), "| Aug unmatched excluding B03:", fmt((ub - b03) - ug), "| raw", fmt(raw),
      "| residual", fmt(raw - ((ub - b03) - ug)))

# ---------------------------------------------------------------- reconciliation statement
print("\n=== 8. RECONCILIATION STATEMENT ===")
G = {r["id"]: D(r["amount"]) for r in gl}
B = {r["id"]: D(r["amount"]) for r in bank}
fee, interest = B["B16"], B["B17"]
print("G09 sign correction: GL recorded", fmt(G["G09"]), "bank", fmt(B["B07"]), "adjustment to GL", fmt(B["B07"] - G["G09"]))
base_gl = g_end + (B["B07"] - G["G09"]) + fee + interest
print("GL", fmt(g_end), "+ G09 correction", fmt(B["B07"] - G["G09"]), "+ B16", fmt(fee), "+ B17", fmt(interest),
      "= GL adjusted for items not dependent on an open reading:", fmt(base_gl))
print("bank", fmt(b_end), "| remaining difference (GL - bank)", fmt(base_gl - b_end))
b13 = B["B13"]
b08_amt, g10_amt = B["B08"], G["G10"]
b08 = b08_amt - g10_amt
print("B13 (no GL entry)", fmt(b13), "| B08 - G10 =", fmt(b08), "| sum", fmt(b13 + b08),
      "| equals remaining difference (bank - GL):", (b13 + b08) == b_end - base_gl)
print("\nreading matrix  (B13: A=GL unrecorded payment, B=bank error/duplicate;  B08: A=GL error, B=bank error)")
for r13 in "AB":
    for r08 in "AB":
        gl_adj = base_gl + (b13 if r13 == "A" else 0) + (b08 if r08 == "A" else 0)
        bk_adj = b_end - (b13 if r13 == "B" else 0) - (b08 if r08 == "B" else 0)
        print(f"  B13={r13} B08={r08}: adjusted GL {fmt(gl_adj)} | adjusted bank {fmt(bk_adj)} | difference {fmt(gl_adj - bk_adj)}")

print("\n=== 9. ESCALATION vs THRESHOLD", ESCALATION_THRESHOLD, "(>= threshold) ===")
items = [("B10 set aside", D(aside[0]["amount"])), ("B13", b13), ("B08 vs G10", b08), ("B07/G09 sign", B["B07"] - G["G09"]),
         ("B16 fee", fee), ("B17 interest", interest), ("G08 foreign", D(foreign[0]["amount"])),
         ("G04/G06 pair net", G["G04"] + G["G06"]), ("July fee continuity", g_beg - jg_end), ("B01 date", B["B01"])]
for name, amt in items:
    print(f"  {name:22s} {fmt(amt):>12s}  meets threshold: {abs(amt) >= ESCALATION_THRESHOLD}")
