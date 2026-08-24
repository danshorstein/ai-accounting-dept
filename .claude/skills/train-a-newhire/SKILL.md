---
name: train-a-newhire
description: Turn a supervised work exercise into a durable AI employee — a role agent, the minimum Skills that support it, and proposed revisions to company procedure. Use when adding a role to the Riverton Finance & Accounting department, when asked to "train" or "hire" an agent for a role, or when retraining an existing role agent after testing reveals a defect.
---

# Train a New Hire

How Riverton adds a role to the Finance & Accounting department: perform real work with
the human first, then extract what should persist, then build only what the exercise
justified.

Trainable roles include Staff Accountant, AP/AR Specialist, Internal Audit, FP&A, Senior
Accountant, CFO. The method is the same regardless of role.

## Prerequisite — do the work first

**Do not create a role agent for work that has not been performed together and reviewed.**
If asked to stand up a role cold, say so and propose the exercise instead.

The reason is not ceremony. Durable instructions are extracted from observed behavior —
what the human corrected, what they asked for that you did not think to do, where you were
about to over-generalize. None of that exists before the work does. An agent written from a
job description encodes assumptions; an agent written from a completed exercise encodes
what was actually learned.

A qualifying exercise is: a real deliverable, produced end to end, from real source data,
reviewed by the human, with their corrections incorporated. One is enough to start.

## Phase 1 — Perform the work

Work the assignment as the role would. Two habits make the later extraction possible:

- **Propose the approach before executing**, and let the human approve or edit it. Their
  edits are the highest-value training signal in the entire process — they are the human
  telling you how the role should behave, in the moment it matters.
- **Note guidance as it arrives**, and note whether it was scoped. "For this exercise" and
  "as a standing rule" are different instructions and must not be conflated later.

## Phase 2 — Analyze before building

Review the whole session and sort what happened into six categories. Present this to the
human for review **before creating any files.**

Pay particular attention to **guidance the human gave during the exercise versus what was
already in the source materials.** The source materials were already governing; the
human's in-session guidance is the new information, and it is the reason the exercise
happened. Separate the two explicitly and show your attribution.

**1. Role / agent instructions** — responsibilities, authority boundaries, judgment
expectations, escalation behavior, working posture. What kind of employee this is.

**2. Reusable Skills** — methods or competencies that would apply to other processes too.
Be conservative; see "How much to build."

**3. Process or procedure changes** — things learned that belong in the company procedure
rather than inside the employee, because they should govern anyone performing the work.

**4. Policy or control requirements** — things already governed by an existing document.
The employee should reference these, never duplicate them.

**5. Durable project/company knowledge** — conventions, file layout, org facts, how the
company works.

**6. Should NOT persist** — exercise-specific parameters, the period's figures, the
particular findings, the training scaffolding, and any expectation that the work came out
clean. Name these explicitly. Deciding what to discard is as much of the job as deciding
what to keep.

## Phase 3 — Decide the layer

The organizing principle, and the one that keeps agents from bloating:

> **Method goes in the procedure. Format goes in Skills. Only disposition goes in the agent.**

| Layer | Holds | Test |
|---|---|---|
| `references/` procedure | How the work is done | Would this govern *anyone* doing this job, human or agent? |
| Skill | A repeatable method or output structure | Would this apply to a different process too? |
| Agent | Responsibilities, boundaries, judgment, escalation | Is this about *who the employee is* rather than how a task is done? |

Two rules that follow from it:

- **Never copy policy text into an agent.** Point to the document. A paraphrase silently
  forks from the source the moment the source changes. The agent should say "read and
  comply with `03` and `04`," and should be told not to work from any paraphrase — including
  paraphrases in `CLAUDE.md`.
- **Never embed a parameter in an agent.** Tolerances, materiality, thresholds, and date
  windows are supplied per engagement by the Controller and recorded in the workpaper with
  their date and attribution. The durable behavior is *asking*; the value is disposable. An
  agent that carries last month's threshold will apply it to work nobody scoped it for.

## Phase 4 — Decide how much to build

**One agent per role.** Thin. If the agent file is filling up with method, the method is in
the wrong layer.

**Skills: only those the exercise actually justified.** The test is whether the competence
generalizes beyond the one process you just performed — and whether you have seen it
enough to encode it as a method rather than accidentally encoding the shape of one data
set. When a competence is genuinely generic but you have exercised it exactly once, say so
and propose revisiting it after a second, different exercise. Naming the skill you chose
*not* to build, and why, is a real part of the deliverable.

**Nothing else.** No agents for roles not in scope, no speculative skills, no framework.

## Phase 5 — Build

Create only what the human approved, and confirm the file list back to them.

**Agent** — `.claude/agents/<role>.md`, explicitly invoked rather than auto-triggering,
with tools narrowed to what the role needs. Include: responsibilities; authority boundaries
(what it may not decide, approve, post, or modify); how it obtains engagement parameters;
judgment expectations; escalation behavior; working posture; the Skills it is expected to
use; and file/naming conventions. Every role in this department is subject to
preparation/review separation — the agent does not approve its own work, and never fills in
a reviewer block.

**Skills** — `.claude/skills/<name>/SKILL.md`, with a `description` naming the concrete
triggers that should invoke it.

**Procedure revisions** — never edit an approved document in `references/` in place. Save a
proposed revision alongside it as `<NN>a <original name> (proposed revision).md`, opening
with a status block that states: it is not yet approved, the original remains authoritative
until the human approves it, the date, and an enumerated list of what changed. Prescribe
mechanisms, not values — a revision may say how a threshold is obtained and recorded; it
may not set one.

**`CLAUDE.md`** — update the "Current state of the experiment" section so it stops
contradicting the files that now exist. Keep the edit narrow.

**Verify before reporting.** Grep the new files for the exercise-specific values and
figures that were supposed to be discarded. Then list every file created or modified.

## Phase 6 — Hand off for testing

The agent has never run. Say so plainly rather than implying it works.

Recommend a test assignment where **something is wrong with the source data**. A clean
exercise cannot train or verify the failure paths — the stop-and-escalate behavior, the
refusal to plug, the posture of not expecting work to come out clean — and those are the
behaviors that matter most when nobody is watching closely.

## Retraining an existing hire

When testing or later use reveals a defect, diagnose the layer before editing anything:

| What went wrong | Where the fix belongs |
|---|---|
| Did the work wrong, or by a bad method | The procedure in `references/` (proposed revision) |
| Produced an output that was hard to review, or skipped required content | The relevant Skill |
| Overstepped authority, assumed something, failed to escalate, or invented a parameter | The agent |
| Applied a value nobody gave it | The agent — and check for an embedded parameter to remove |
| Complied with the letter of an instruction that was wrong | Whichever document holds the instruction; fix it at the source |

Fix one layer. Editing the agent to compensate for a procedure gap is how agents accumulate
method they should not hold — and the fix then applies only to that agent, when it should
govern everyone doing the work.

Then retest against the case that exposed the defect.

## Cautions

- **The human's scoping language is load-bearing.** "For this exercise" means the value
  dies with the exercise. When they correct you for over-generalizing, that correction is
  itself a durable lesson about the role.
- **Ask before building, not after.** Surface the decisions that would change the artifact
  — where files live, whether a gate is hard or soft, what scope the skill covers — and
  offer a default for each so the human can approve in one line.
- **Distinguish a checkpoint that was training scaffolding from a control.** A stop-for-
  approval that existed to keep you aligned during training usually should not survive into
  production. A stop that exists because continuing would be unsound — data that does not
  tie — should. Ask the human which one it was; do not decide alone.
- **Do not encode that the work came out clean.** The exercise's findings are not the
  role's expectations.
