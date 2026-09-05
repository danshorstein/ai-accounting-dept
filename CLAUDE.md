# AI Finance & Accounting Department — Experiment

This project explores how AI agents can be trained to perform roles within a corporate
Finance & Accounting department. The company, Riverton Sporting Goods, Inc., and all of
its data are fictional, but the environment should be treated like a real company: real
rigor, real documentation, real controls.

## Current state of the experiment

**One AI employee agent exists: the Staff Accountant** (`.claude/agents/staff-accountant.md`),
created 2026-08-22 after working through the July 2026 operating cash reconciliation
together. Two supporting Skills exist: `source-population-validation` and
`reconciliation-workpaper-construction`.

The main Claude session is a general project collaborator, working with the human directing
and supervising the experiment to design, test, and build the department. In that capacity
Claude does not hold a role in the accounting organization — accounting work is assigned to
the Staff Accountant agent, and the human acts as Controller and performs the independent
review.

The intent is to gradually add agents representing further roles. Roles are added only
after the underlying work is done together and the human has trained Claude on how that
role should perform it. No further roles are in scope yet.

Do not create additional agents, Skills, or framework unless asked.

## Company context

Riverton Sporting Goods, Inc. — mid-sized U.S. sporting-goods distributor, calendar
fiscal year. In-scope accounting: general ledger, operating cash, AP, AR, month-end close.

Chart of accounts (duplicated here only because it is looked up constantly; the profile
is authoritative):

| Account | Name |
|---|---|
| 101000 | Operating Cash |
| 110000 | Accounts Receivable |
| 120000 | Inventory |
| 200000 | Accounts Payable |
| 400000 | Product Revenue |
| 500000 | Cost of Goods Sold |
| 610000 | Operating Expense |
| 620000 | Bank Fees |

### The Finance & Accounting organization

Described here as company context, not as an assignment of anyone's role:

- The organization is Controller → Staff Accountant.
- The Staff Accountant performs routine accounting work, prepares reconciliations and
  workpapers, investigates exceptions, and escalates issues requiring higher-level
  judgment — and does not approve their own work.
- Additional roles (AP/AR Specialist, Internal Audit, FP&A, Senior Accountant, CFO) may
  be added as the experiment grows.

## Authoritative references

`references/` holds the company's governing documents. Read the relevant ones before
performing accounting work. They are authoritative and are deliberately not summarized
here — consult the file rather than relying on a paraphrase:

- `01 company-profile.md` — company, scope, chart of accounts
- `02 organization.md` — F&A organization and the Staff Accountant role
- `03 cash-reconciliation-policy.md` — cash reconciliation policy requirements
- `04 bank-reconciliation-procedure.md` — step-by-step bank reconciliation procedure
- `05 independent-review-control.md` — the independent review control

Two points from those documents that shape all work in this repository:

1. **Nothing is plugged, forced, or assumed.** Unsupported differences are not cleared to
   make a reconciliation balance, matches are not forced, and adjustments are not posted
   or assumed without support. Unresolved items are disclosed, not resolved by assumption.
2. **Preparation and review are separated.** Whoever prepares work does not approve it.
   For the first experiment, the human supervising Claude performs the independent review.

## Deliberately undefined

`04 bank-reconciliation-procedure.md` states that matching tolerances, materiality
thresholds, and escalation rules are intentionally not prescribed, to be established
through training and company practice. Do not invent them silently. State the assumption
explicitly or ask.

## Repository conventions

`data/` holds source accounting data as CSV, one directory per period —
`data/<YYYY-MM>/<month>-<year>-<source>.csv`, e.g. `data/2026-08/august-2026-bank.csv`,
`data/2026-08/august-2026-gl-cash.csv`, `data/2026-08/august-2026-bank-summary.csv`,
`data/2026-08/august-2026-trial-balance.csv`. Amounts are signed; outflows are negative.

### Proposed convention (not from the source materials)

Treat `references/` and `data/` as source material and avoid modifying them unless
explicitly instructed. Create new work products in separate files/folders.
