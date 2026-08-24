# AI Finance & Accounting Department — Experiment

This project explores how AI agents can be trained to perform roles within a corporate
Finance & Accounting department. The company, Riverton Sporting Goods, Inc., and all of
its data are fictional, but the environment is treated like a real company: real rigor,
real documentation, real controls.

## Current state

**One AI employee agent exists: the Staff Accountant** (`.claude/agents/staff-accountant.md`),
created 2026-08-22 after working through the July 2026 operating cash reconciliation
together. Two supporting Skills exist:

- `source-population-validation`
- `reconciliation-workpaper-construction`

The main Claude session acts as a general project collaborator, working with a human who
directs and supervises the experiment. Accounting work itself is assigned to the Staff
Accountant agent, and the human acts as Controller, performing independent review.

Roles are added only after the underlying work is done together and Claude has been
trained on how that role should perform it.

## Company context

Riverton Sporting Goods, Inc. — a mid-sized, fictional U.S. sporting-goods distributor,
calendar fiscal year. In-scope accounting: general ledger, operating cash, AP, AR,
month-end close.

## Repository layout

- `references/` — the company's governing documents (company profile, org structure,
  cash reconciliation policy, bank reconciliation procedure, independent review control)
- `data/` — source accounting data as CSV
- `workpapers/` — completed reconciliation workpapers
- `.claude/agents/` — role agent definitions
- `.claude/skills/` — supporting Skills used by role agents

See `CLAUDE.md` for full project instructions and conventions.
