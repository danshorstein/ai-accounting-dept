import csv
base="/Users/danielshorstein/playground/pythonic/ai-accounting-dept/data/2026-08/"
def rows(f):
    with open(base+f) as fh: return list(csv.DictReader(fh))
bank=rows("august-2026-bank.csv"); gl=rows("august-2026-gl-cash.csv")
bs=rows("august-2026-bank-summary.csv")[0]; tb=rows("august-2026-trial-balance.csv")[0]

bank_begin=float(bs['beginning_balance']); bank_end=float(bs['ending_balance'])
tb_begin=float(tb['beginning_balance']); tb_net=float(tb['debits_credits_net']); tb_end=float(tb['ending_balance'])

# ---- roll-forward continuity vs July ----
jul_bank_end=74060.00      # workpapers/2026-07 §2 / july-2026-bank-summary
jul_gl_tb_end=73475.00     # workpapers/2026-07 §2 (July TB ending)
jul_aje1=35.00             # July AJE-1 bank fee
print("CONTINUITY")
print(f"  July bank ending {jul_bank_end:.2f} vs Aug bank beginning {bank_begin:.2f} -> diff {jul_bank_end-bank_begin:.2f}")
print(f"  July GL TB ending {jul_gl_tb_end:.2f} - July AJE-1 {jul_aje1:.2f} = {jul_gl_tb_end-jul_aje1:.2f} vs Aug GL beginning {tb_begin:.2f} -> diff {jul_gl_tb_end-jul_aje1-tb_begin:.2f}")
print(f"  (raw July GL TB ending {jul_gl_tb_end:.2f} vs Aug GL beginning {tb_begin:.2f} -> diff {jul_gl_tb_end-tb_begin:.2f})")

# ---- populations ----
B={r['id']:(r['date'],r['description'],float(r['amount'])) for r in bank}
G={r['id']:(r['date'],r['description'],float(r['amount']),r['account']) for r in gl}
bank_excl_B10=[i for i in B if i!='B10']
gl_101=[i for i in G if G[i][3]=='101000']

sb=sum(B[i][2] for i in bank_excl_B10)
sg=sum(G[i][2] for i in gl_101)
print("\nROLL-FORWARD (B10 excluded)")
print(f"  bank {bank_begin:.2f} + {sb:.2f} = {bank_begin+sb:.2f}  reported {bank_end:.2f}  diff {bank_begin+sb-bank_end:.2f}")
print(f"  GL   {tb_begin:.2f} + {sg:.2f} = {tb_begin+sg:.2f}  reported {tb_end:.2f}  diff {tb_begin+sg-tb_end:.2f}")
print(f"  begin diff bank-GL = {bank_begin-tb_begin:.2f}")
print(f"  ending diff bank-GL = {bank_end-tb_end:.2f}")

# ---- matching: exact amount, 5-day window ----
from datetime import date
def d(s): 
    y,m,dd=map(int,s.split('-')); return date(y,m,dd)
matches=[]; used_g=set()
for bi in bank_excl_B10:
    bd,bdesc,ba=B[bi]
    for gi in gl_101:
        if gi in used_g: continue
        gd,gdesc,ga,_=G[gi]
        if ba==ga and abs((d(bd)-d(gd)).days)<=5:
            matches.append((bi,gi,ba,(d(bd)-d(gd)).days)); used_g.add(gi); break
matched_b={m[0] for m in matches}; matched_g={m[1] for m in matches}
print("\nMATCHES (exact amount, <=5 days)")
for bi,gi,a,gap in matches:
    print(f"  {bi} {B[bi][0]} {B[bi][1]:30s} {a:11.2f} <-> {gi} {G[gi][0]} {G[gi][1]:28s} gap {gap}")
print(f"  matched total bank {sum(m[2] for m in matches):.2f}")

ub=[i for i in bank_excl_B10 if i not in matched_b]
ug=[i for i in gl_101 if i not in matched_g]
print("\nUNMATCHED BANK")
for i in ub: print(f"  {i} {B[i][0]} {B[i][1]:32s} {B[i][2]:11.2f}")
print(f"  sum unmatched bank {sum(B[i][2] for i in ub):.2f}")
print("UNMATCHED GL")
for i in ug: print(f"  {i} {G[i][0]} {G[i][1]:32s} {G[i][2]:11.2f}")
print(f"  sum unmatched GL {sum(G[i][2] for i in ug):.2f}")

# ---- proof ----
res=(bank_end-tb_end) - ( (bank_begin-tb_begin) + (sum(B[i][2] for i in ub) - sum(G[i][2] for i in ug)) )
print(f"\nPROOF: (bank_end-gl_end) - [ (begin diff) + (sum unmatched bank - sum unmatched GL) ] = {res:.2f}")

# ---- reconciling item decomposition (contribution to bank-book) ----
items={
 'Check1048 begin diff': +620.00,
 'Check1048 clears B03': -620.00,
 'R-1 Zeta sign (B07 -2410 vs G09 +2410)': B['B07'][2]-G['G09'][2],
 'R-2 Theta amt (B08 -5463 vs G10 -5436)': B['B08'][2]-G['G10'][2],
 'R-3 Delta 2nd pmt B13 not in GL': B['B13'][2]-0,
 'R-4 bank fee B16 not in GL': B['B16'][2]-0,
 'R-5 interest B17 not in GL': B['B17'][2]-0,
 'R-7 Check1052 written G04': 0-G['G04'][2],
 'R-7 Check1052 void G06': 0-G['G06'][2],
}
tot=0
print("\nDECOMPOSITION of ending diff (bank-book):")
for k,v in items.items():
    tot+=v; print(f"  {k:45s} {v:11.2f}")
print(f"  {'TOTAL':45s} {tot:11.2f}   (target {bank_end-tb_end:.2f})")

# ---- adjusted balances (book-error reading) ----
book_adj = G['G09'][2]*0  # placeholder
adj_book = tb_end + (B['B07'][2]-G['G09'][2]) + (B['B08'][2]-G['G10'][2]) + B['B13'][2] + B['B16'][2] + B['B17'][2]
print(f"\nAdjusted book = {tb_end:.2f} + reconciling = {adj_book:.2f}")
print(f"Adjusted bank = {bank_end:.2f}")
print(f"Agree? diff {adj_book-bank_end:.2f}")

# alt reading: R-2,R-3 are bank errors
adj_bank_alt = bank_end - (B['B08'][2]-G['G10'][2]) - B['B13'][2]
adj_book_alt = tb_end + (B['B07'][2]-G['G09'][2]) + B['B16'][2] + B['B17'][2]
print(f"ALT: adj bank {adj_bank_alt:.2f}  adj book {adj_book_alt:.2f}  diff {adj_bank_alt-adj_book_alt:.2f}")

# proposed AJE net cash effect
aje_cash = (B['B07'][2]-G['G09'][2]) + (B['B08'][2]-G['G10'][2]) + B['B13'][2] + B['B16'][2] + B['B17'][2]
print(f"\nNet cash effect of proposed AJEs: {aje_cash:.2f}")
