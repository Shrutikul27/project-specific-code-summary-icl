#!/usr/bin/env python3
"""
compute_results.py — Compute result summary from evaluation labels.

Reads data/evaluation_labels.csv, groups by method and label,
computes counts, correctness rate, and incorrect-summary rate,
prints a clean results table, and saves to outputs/result_summary.csv.

Usage:
    python scripts/compute_results.py
"""

import sys
from pathlib import Path

import pandas as pd

# Resolve project root relative to this script
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LABELS_PATH = PROJECT_ROOT / "data" / "evaluation_labels.csv"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "result_summary.csv"

EXPECTED_METHODS = {"Generic Prompting", "Project-Specific ICL"}
EXPECTED_LABELS = {"Correct", "Partial", "Incorrect"}


def load_labels(path: Path) -> pd.DataFrame:
    """Load and validate the evaluation labels CSV."""
    if not path.exists():
        print(f"ERROR: Labels file not found: {path}", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(path)

    required_cols = {"function_id", "method", "label"}
    missing = required_cols - set(df.columns)
    if missing:
        print(f"ERROR: Missing columns in labels file: {missing}", file=sys.stderr)
        sys.exit(1)

    unexpected_methods = set(df["method"].unique()) - EXPECTED_METHODS
    if unexpected_methods:
        print(f"WARNING: Unexpected methods found: {unexpected_methods}", file=sys.stderr)

    unexpected_labels = set(df["label"].unique()) - EXPECTED_LABELS
    if unexpected_labels:
        print(f"WARNING: Unexpected labels found: {unexpected_labels}", file=sys.stderr)

    return df


def compute_results(df: pd.DataFrame) -> pd.DataFrame:
    """Compute result summary grouped by method."""
    rows = []
    for method in ["Generic Prompting", "Project-Specific ICL"]:
        subset = df[df["method"] == method]
        total = len(subset)
        if total == 0:
            print(f"WARNING: No rows found for method '{method}'", file=sys.stderr)
            continue

        correct = (subset["label"] == "Correct").sum()
        partial = (subset["label"] == "Partial").sum()
        incorrect = (subset["label"] == "Incorrect").sum()
        correctness_rate = (correct / total) * 100 if total > 0 else 0.0
        incorrect_rate = (incorrect / total) * 100 if total > 0 else 0.0

        rows.append({
            "Method": method,
            "Correct": int(correct),
            "Partial": int(partial),
            "Incorrect": int(incorrect),
            "Total": int(total),
            "Correctness Rate (%)": round(correctness_rate, 1),
            "Incorrect Rate (%)": round(incorrect_rate, 1),
        })

    return pd.DataFrame(rows)


def print_results(results: pd.DataFrame) -> None:
    """Print results table to stdout."""
    try:
        from tabulate import tabulate
        print(tabulate(results, headers="keys", tablefmt="grid", showindex=False))
    except ImportError:
        print(results.to_string(index=False))


def main():
    print(f"Loading labels from: {LABELS_PATH}")
    df = load_labels(LABELS_PATH)
    print(f"Loaded {len(df)} label rows.\n")

    results = compute_results(df)

    print("=" * 70)
    print("RESULT SUMMARY")
    print("=" * 70)
    print_results(results)
    print()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(OUTPUT_PATH, index=False)
    print(f"Results saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
