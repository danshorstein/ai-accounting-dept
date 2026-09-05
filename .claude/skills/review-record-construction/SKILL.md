---
name: review-record-construction
description: Structure an independent-review record so it is itself testable by someone else — a header establishing scope and independence, a stated result vocabulary, per-item checklist blocks with basis/method/findings/result, a gathered synthesis, and a decision held for the Controller until acted on. Use whenever writing up the output of a workpaper-review.
---

# Review Record Construction

The review record has to meet the same bar the workpaper it reviews does: someone reading
it — including the Controller, including a future reviewer — should be able to confirm what
was actually checked and what was found, without re-performing the review themselves.

Write to `workpapers/<period> <subject> — independent review.md`, alongside the workpaper
it reviews.

## Required header

- The workpaper under review (path).
- Reviewer and date.
- **Scope and independence confirmation** — a plain statement that the reviewer did not
  prepare the workpaper under review (`03` §7; `05` control design opens on this point).
- The engagement parameters the review is testing against, with their source (which
  Controller instruction, which date) — read from the workpaper's own judgment log, not
  re-derived or assumed.
- Which checks, if any, were deliberately excluded from this review and why. A scope
  decision made on purpose is not the same as an omission — record which it was.

## Legend

State the result vocabulary explicitly at the top of every review record — don't assume
the reader already knows it. See `workpaper-review` for the four values (Pass / Fail / Flag
/ N/A) and their definitions.

## Per-item blocks

One block per check, each with a stable ID (group checks by pass — e.g., one prefix for
top-down analytical checks, another for bottom-up reperformance — so findings can
cross-reference cleanly, the same way a workpaper's own reconciling-item and judgment-log
references do). Each block has exactly four fields, in this order:

```
### <ID> — <short name>                                          [<tag>]
**Basis:** <the specific document and section that requires or supports this check, or
"reviewer judgment — not directly prescribed" stated plainly when nothing does>
**Method:** <what was actually done to perform this check>
**Findings:** <what was found, specific enough — figures, row references, quoted text —
that someone else could verify it without redoing the work>
**Result:** ☐ Pass ☐ Fail ☐ Flag ☐ N/A
```

The `<tag>` names whether the check is policy/procedure-**Required**, a **Verification**
of a stated preparer practice, or genuine **Reviewer judgment** added beyond what any
document prescribes. Carry this distinction through honestly — it tells the Controller how
much of the review is compliance versus how much is the reviewer's own added scrutiny.

Never leave Findings blank on a completed item, including a Pass. "Checked, no issue" with
no supporting specifics is not different, to a later reader, from not having checked at
all.

## Synthesis section

Gather every FAIL and FLAG into one place — don't make the reader hunt across all the
individual blocks. Sort per `workpaper-review`'s three buckets (must return / escalate to
Controller / note only). Restate any already-disclosed open items from the workpaper itself
that remain live, so the synthesis is a complete picture of everything the Controller needs
to act on, not just what the review added.

## Decision section

State the draft decision (approve / return) and its basis. In a co-review or training
context, mark it explicitly as **held for the Controller** rather than final. Where the
review surfaced a tension in its own rules (e.g., a low-severity finding that technically
triggers a hard must-return rule), name the tension explicitly here rather than resolving
it silently one way or the other.

## Discipline

- Every result traces to a specific finding, not a general impression.
- A missing citation is more honest than a stretched one — label reviewer judgment as such.
- Present the synthesis; don't make the reader reassemble it from many individual items.
- The record is retained evidence (`03` §8), not a working scratchpad.
