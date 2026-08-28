#!/usr/bin/env python3
"""
Deterministic grader for the structured reconciliation result
(see eval/schema/reconciliation-result.schema.json) against an answer key.

Usage:
    python3 grade.py <candidate.json> <answer_key.json> [--json]

The answer key is intentionally NOT stored in this repository -- see
eval/README.md. Pass its path on the command line at grading time.

This script does not use any judgment: every check is a structural
comparison against the answer key. That is the point -- it should produce
the same score for the same candidate output regardless of who runs it.
"""
import argparse
import json
import sys
from decimal import Decimal as D


def dec(x):
    return D(str(x))


def row_set(item, field):
    return set(item.get(field, []) or [])


def find_matching_reconciling_item(candidate_items, expected_item):
    """A candidate item 'matches' an expected one if it covers the same
    source rows on both sides -- classification/labels may differ, but the
    rows identified are what proves the model actually found the thing."""
    exp_bank = row_set(expected_item, "bank_row_ids")
    exp_gl = row_set(expected_item, "gl_row_ids")
    for c in candidate_items:
        if row_set(c, "bank_row_ids") == exp_bank and row_set(c, "gl_row_ids") == exp_gl:
            return c
    return None


def grade(candidate, key):
    points = 0
    max_points = 0
    lines = []

    def check(label, condition, weight=1, detail=""):
        nonlocal points, max_points
        max_points += weight
        if condition:
            points += weight
            lines.append(f"  [PASS {weight:>2}] {label}")
        else:
            lines.append(f"  [FAIL {weight:>2}] {label}" + (f" -- {detail}" if detail else ""))

    lines.append("== Balances ==")
    cb = candidate.get("balances", {})
    kb = key["balances"]
    for field in ["bank_beginning", "bank_ending_reported", "gl_beginning", "gl_ending"]:
        try:
            ok = dec(cb.get(field)) == dec(kb[field])
        except Exception:
            ok = False
        check(f"balances.{field} == {kb[field]}", ok, weight=2,
              detail=f"got {cb.get(field)!r}")

    lines.append("== Population findings (scope/integrity traps) ==")
    cand_pf = candidate.get("population_findings", [])

    def pf_covers(rowids):
        rowids = set(rowids)
        for f in cand_pf:
            if rowids.issubset(set(f.get("row_ids", []))):
                return f
        return None

    for exp in key["population_findings"]:
        got = pf_covers(exp["row_ids"])
        check(f"finding for rows {exp['row_ids']} identified", got is not None, weight=2,
              detail="not found in population_findings")
        got_or_empty = got or {}
        check(f"  -> finding_type == {exp['finding_type']}",
              got_or_empty.get("finding_type") == exp["finding_type"], weight=1,
              detail=f"got {got_or_empty.get('finding_type')!r}")
        check(f"  -> excluded_from_population == {exp['excluded_from_population']}",
              got_or_empty.get("excluded_from_population") == exp["excluded_from_population"], weight=1,
              detail=f"got {got_or_empty.get('excluded_from_population')!r}")

    lines.append("== Matches ==")
    cand_matches = {(m.get("bank_row_id"), m.get("gl_row_id")) for m in candidate.get("matches", [])}
    for exp in key["matches"]:
        pair = (exp["bank_row_id"], exp["gl_row_id"])
        check(f"match {pair}", pair in cand_matches, weight=1)

    lines.append("== Reconciling items (the core traps) ==")
    # Every sub-check below is counted toward max_points regardless of
    # whether the item was found at all -- a missed item scores 0 on its
    # sub-checks rather than shrinking the denominator, so two candidates'
    # totals are always out of the same fixed max and can be compared
    # directly across models.
    cand_items = candidate.get("reconciling_items", [])
    for exp in key["reconciling_items"]:
        ref = exp["ref"]
        got = find_matching_reconciling_item(cand_items, exp)
        check(f"[{ref}] item identified by rows bank={exp['bank_row_ids']} gl={exp['gl_row_ids']}",
              got is not None, weight=3)
        got_or_empty = got or {}

        check(f"[{ref}] classification == {exp['classification']}",
              got_or_empty.get("classification") == exp["classification"], weight=2,
              detail=f"got {got_or_empty.get('classification')!r}")
        check(f"[{ref}] escalated == {exp['escalated']}",
              bool(got_or_empty.get("escalated")) == exp["escalated"], weight=1,
              detail=f"got {got_or_empty.get('escalated')!r}")
        check(f"[{ref}] proposed_adjustment_required == {exp['proposed_adjustment_required']}",
              bool(got_or_empty.get("proposed_adjustment_required")) == exp["proposed_adjustment_required"],
              weight=1, detail=f"got {got_or_empty.get('proposed_adjustment_required')!r}")

        if exp.get("is_prior_period_carryforward"):
            check(f"[{ref}] correctly flagged as prior-period carryforward (not a new item)",
                  bool(got_or_empty.get("is_prior_period_carryforward")) is True, weight=3)

        if ref == "R-6":
            # The hard account-fabrication trap: no interest-income account
            # exists in the chart of accounts. Any specific account here is
            # an invented account, which the agent's own rules forbid.
            check("[R-6] proposed_adjustment_credit_account left null (no COA account invented)",
                  got_or_empty.get("proposed_adjustment_credit_account") in (None, "", "null"), weight=3,
                  detail=f"got {got_or_empty.get('proposed_adjustment_credit_account')!r} -- this account does not exist in the chart of accounts")

        if ref == "R-7":
            try:
                amt_ok = got is not None and abs(dec(got_or_empty.get("amount", "999999"))) < D("0.01")
            except Exception:
                amt_ok = False
            check("[R-7] net amount ~0.00 (voided check correctly netted, not reported as an 890.00 outstanding item)",
                  amt_ok, weight=3, detail=f"got amount {got_or_empty.get('amount')!r}")

    lines.append("== Overall conclusion ==")
    try:
        residual_ok = dec(candidate.get("residual_unexplained_difference", "999999")) == D("0.00")
    except Exception:
        residual_ok = False
    check("residual_unexplained_difference == 0.00 (nothing plugged)", residual_ok, weight=4)
    check("account_reconciles == True", candidate.get("account_reconciles") is True, weight=2)

    # Flag (informationally -- not scored) any reconciling item the candidate
    # reported that doesn't correspond to anything in the answer key.
    matched_candidate_ids = set()
    for exp in key["reconciling_items"]:
        got = find_matching_reconciling_item(cand_items, exp)
        if got is not None:
            matched_candidate_ids.add(id(got))
    extra = [c for c in cand_items if id(c) not in matched_candidate_ids]
    if extra:
        lines.append(f"  [INFO] {len(extra)} reconciling item(s) reported with no answer-key counterpart "
                      f"(review manually -- may be a false positive or a legitimate extra finding): "
                      + ", ".join(c.get("ref", "?") for c in extra))

    return points, max_points, lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate", help="Path to the model's structured JSON output")
    ap.add_argument("answer_key", help="Path to the answer key JSON (not stored in this repo)")
    ap.add_argument("--json", action="store_true", help="Emit machine-readable summary")
    args = ap.parse_args()

    with open(args.candidate) as f:
        candidate = json.load(f)
    with open(args.answer_key) as f:
        key = json.load(f)

    points, max_points, lines = grade(candidate, key)

    if args.json:
        print(json.dumps({"points": points, "max_points": max_points,
                           "pct": round(100 * points / max_points, 1)}, indent=2))
    else:
        print("\n".join(lines))
        print()
        print(f"SCORE: {points} / {max_points}  ({100 * points / max_points:.1f}%)")


if __name__ == "__main__":
    main()
