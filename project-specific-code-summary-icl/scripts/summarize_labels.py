#!/usr/bin/env python3
"""
summarize_labels.py — Detailed breakdown of evaluation labels.

Prints counts, percentages, and details of Incorrect/Partial cases
to help explain "what was seen" in the paper.

Usage:
    python scripts/summarize_labels.py
"""

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LABELS_PATH = PROJECT_ROOT / "data" / "evaluation_labels.csv"


def main():
    if not LABELS_PATH.exists():
        print(f"ERROR: Labels file not found: {LABELS_PATH}", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(LABELS_PATH)
    methods = ["Generic Prompting", "Project-Specific ICL"]

    # --- Counts by method/label ---
    print("=" * 70)
    print("LABEL COUNTS BY METHOD")
    print("=" * 70)
    for method in methods:
        subset = df[df["method"] == method]
        total = len(subset)
        print(f"\n  {method} (n={total}):")
        for label in ["Correct", "Partial", "Incorrect"]:
            count = (subset["label"] == label).sum()
            print(f"    {label:12s}: {count}")

    # --- Percentages by method/label ---
    print("\n" + "=" * 70)
    print("LABEL PERCENTAGES BY METHOD")
    print("=" * 70)
    for method in methods:
        subset = df[df["method"] == method]
        total = len(subset)
        print(f"\n  {method} (n={total}):")
        for label in ["Correct", "Partial", "Incorrect"]:
            count = (subset["label"] == label).sum()
            pct = (count / total) * 100 if total > 0 else 0.0
            print(f"    {label:12s}: {count:2d} / {total} = {pct:5.1f}%")

    # --- Incorrect cases ---
    print("\n" + "=" * 70)
    print("INCORRECT CASES (details)")
    print("=" * 70)
    incorrect = df[df["label"] == "Incorrect"]
    if incorrect.empty:
        print("  No incorrect cases found.")
    else:
        for _, row in incorrect.iterrows():
            print(f"\n  [{row['method']}] {row['function_id']} — {row['repository']}.{row['target_function']}")
            print(f"    Notes: {row.get('notes', 'N/A')}")

    # --- Partial cases ---
    print("\n" + "=" * 70)
    print("PARTIAL CASES (details)")
    print("=" * 70)
    partial = df[df["label"] == "Partial"]
    if partial.empty:
        print("  No partial cases found.")
    else:
        for _, row in partial.iterrows():
            print(f"\n  [{row['method']}] {row['function_id']} — {row['repository']}.{row['target_function']}")
            print(f"    Notes: {row.get('notes', 'N/A')}")

    # --- Cross-method comparison ---
    print("\n" + "=" * 70)
    print("CROSS-METHOD COMPARISON (per function)")
    print("=" * 70)
    functions = df["function_id"].unique()
    improved = 0
    same = 0
    degraded = 0
    label_rank = {"Incorrect": 0, "Partial": 1, "Correct": 2}
    for fid in sorted(set(df[df["method"] == methods[0]]["function_id"])):
        g_row = df[(df["function_id"] == fid) & (df["method"] == methods[0])]
        p_row = df[(df["function_id"] == fid) & (df["method"] == methods[1])]
        if g_row.empty or p_row.empty:
            continue
        g_label = g_row.iloc[0]["label"]
        p_label = p_row.iloc[0]["label"]
        g_rank = label_rank.get(g_label, -1)
        p_rank = label_rank.get(p_label, -1)
        change = ""
        if p_rank > g_rank:
            change = "IMPROVED"
            improved += 1
        elif p_rank == g_rank:
            change = "SAME"
            same += 1
        else:
            change = "DEGRADED"
            degraded += 1
        print(f"  {fid}: {g_label:12s} -> {p_label:12s}  [{change}]")

    print(f"\n  Summary: {improved} improved, {same} same, {degraded} degraded")
    print()


if __name__ == "__main__":
    main()
