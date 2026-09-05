---
name: workpaper-review
description: Perform the independent review of a completed accounting workpaper — test its conclusions without recreating the preparer's analysis, independently reperform the mechanical proofs, and run analytical checks that a section-by-section read won't surface on its own. Use before deciding to approve or return any completed reconciliation or workpaper prepared by someone else.
---

# Workpaper Review

The standard: an independent reviewer can test every conclusion in the workpaper without
redoing the work — the same bar `reconciliation-workpaper-construction` sets for the
preparer. This skill is the reviewer's method for testing it.

Perform the review in two passes, **in this order**, not interchangeably.

## Pass 1 — Top-down, before touching the source data

Read the completed workpaper once, straight through, as a first-time reader would — no
side-channel knowledge of how it was built. Do this **before** Pass 2. Once the detail has
been reperformed, the "stranger reading this cold" vantage is gone, and analytical checks
done afterward tend to just confirm what the reperformance already found rather than
surface anything new.

Six analytical checks, run at this altitude. They generalize across workpaper types; the
descriptions stay deliberately unspecific to any one kind of reconciliation:

1. **Conclusion-vs-body.** Read only the header, the balances-to-be-reconciled figures, and
   the stated conclusion, in isolation. Does the plain-English conclusion overstate the
   confidence the body actually supports — especially in what the *lead sentence* claims
   before any caveat arrives? A conclusion that is technically qualified two sentences
   later still misleads a reader who stops at the first sentence.
2. **Error-pattern / systemic-risk scan.** Step back from individual dollar amounts and
   count the *kinds* of defects, not just their sizes. A handful of distinct defect types
   in one population, or a population that looks qualitatively different from the prior
   period's (routine timing items vs. actual data-entry errors), is worth naming as a
   process-health observation — separate from whatever gets said about the individual
   items.
3. **Directionality / cui bono scan.** Sign every item that affects the balance under
   reconciliation by its net effect, and check whether the effects skew consistently in one
   direction. Randomly distributed errors tend not to; a consistent skew — even a small one
   per item — is a different risk category and worth surfacing on its own, independent of
   what the item-by-item classification concludes about each one individually.
4. **Assumption-creep / framing scan.** Look for language that quietly privileges one
   answer to a question the preparer has otherwise disclosed as genuinely open — a "primary
   reading" label, an asymmetric level of detail given to two alternatives presented as
   equally undecided, a word choice that reads more resolved than the underlying analysis
   is. This is a framing check, distinct from checking whether anything was numerically
   plugged.
5. **Proportionality gut-check.** Given the scale of the account or population under
   reconciliation, do the escalated amounts feel proportionate to the scrutiny they're
   getting — over-escalated relative to the business's scale, or under-escalated? State
   plainly when this check is bounded by missing context (e.g., only one account's data is
   available, not full financials) rather than presenting it as a real materiality
   analysis.
6. **Trend vs. prior period.** Compare the current workpaper to the prior period's at the
   portfolio level — not item by item. Is there a trend in error count or error kind worth
   naming as its own observation? Note explicitly if the two periods used different
   engagement parameters (a different escalation threshold or basis, for instance) that
   make a literal number-for-number comparison unfair, and compare the underlying data
   quality instead.

**Explicitly out of scope for this skill:** recommending upstream control redesigns implied
by what the reconciliation turned up (e.g., "add a maker-checker on this posting type").
That may be worth doing, but it goes beyond the independent-review control's own defined
objective and belongs to a role scoped to evaluate controls, not to the reconciliation
reviewer, until a Controller decides otherwise for a specific engagement. Perform it only
when explicitly asked, and hold it separate from the checklist above rather than let it
become assumed practice.

## Pass 2 — Bottom-up reperformance

1. **Compliance check against the required structure.** Walk the workpaper against every
   section `reconciliation-workpaper-construction` requires. Confirm each is present, not
   just present in substance — content that is disclosed but scattered across other
   sections instead of gathered where the standard says a reviewer should find it is a real
   gap, not a stylistic nitpick.
2. **Independent re-derivation, not just re-running the preparer's tool.** Recompute the
   core proofs (roll-forwards, matching, the residual proof) using your own method, from the
   raw source data, before or in addition to re-running whatever script or process the
   preparer used. Re-running the preparer's own code only confirms it's reproducible — it
   will faithfully replicate any bug in that code, not catch one.
3. **Re-run the preparer's script or tool, unmodified**, and cross-check its output against
   both the workpaper's stated figures and your independent re-derivation. All three should
   agree exactly.
4. **Row/item-accounting completeness check.** Rebuild the full partition of every
   population under reconciliation yourself — every item accounted for in exactly one
   bucket (matched, unmatched/reconciling, excluded, set aside) — rather than trusting a
   stated count.
5. **Trace every reconciling item and proposed adjustment to its source.** Pull the actual
   source row or document cited and confirm every detail (id, date, description, amount)
   matches what the workpaper states.
6. **Recheck continuity against the actual prior-period record**, not the current
   workpaper's quotation of it. Go to the prior workpaper or source document directly.
7. **Recheck escalation logic and math** against the stated threshold for this engagement,
   including any below-threshold escalations made on grounds other than amount — confirm
   the stated distinction is actually applied consistently, not just asserted.
8. **Spot-check judgment-log citations.** Pull the actual text of every cited policy,
   procedure, or skill section and confirm it says what the entry claims. A citation that
   supports half of a compound judgment, with the other half resting on an uncited
   inference, is a real (if often minor) finding.

## Documentation discipline

Every check — in either pass — gets recorded with four things: what document or provision
authorizes doing this check at all (**Basis**), what was actually done (**Method**), what
was found (**Findings**, specific enough that someone else could verify it without redoing
the work), and a **Result**. See `review-record-construction` for the exact structure.

**Result vocabulary:**

| Result | Meaning |
|---|---|
| PASS | Checked; no issue found. |
| FAIL | Checked; found a defect the workpaper needs corrected. |
| FLAG | Checked; found something real, but it's a disclosed or judgment matter for the Controller — not a preparer defect. |
| N/A | Not applicable to this workpaper. |

**Be honest about Basis.** Some of the most valuable checks above are not directly
prescribed by any policy or procedure text — they are reviewer judgment. Say so plainly
("reviewer judgment — not directly prescribed") rather than stretching a citation to cover
something it doesn't actually say. A precise citation that admits its own limits is worth
more than an approximate one that overclaims authority.

## Synthesis and decision

Gather every FAIL and FLAG. Sort into:

- **Must return** — an unsupported item, a forced match, a plugged residual, a required
  section that's missing, an invented parameter, a figure that doesn't tie.
- **Escalate to the Controller, don't return** — something real that exceeds what the
  reviewer can close out alone: a contingent conclusion, a genuinely undecided judgment
  call, a pattern worth the Controller's attention before approving anything.
- **Note only** — doesn't block approval.

Apply the must-return rule as stated even when a finding's real-world severity is low — a
missing required section is a missing required section. If applying the rule rigidly feels
wrong for a specific finding, say so explicitly to the Controller rather than quietly
downgrading it yourself. That tension is itself useful information; deciding it alone is
not the reviewer's call to make.

## Retention

The review record is evidence, not a scratch file discarded once a decision is reached
(`03` §8; `05`). Retain it alongside the workpaper it reviews.
