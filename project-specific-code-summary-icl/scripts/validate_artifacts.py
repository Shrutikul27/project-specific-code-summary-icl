#!/usr/bin/env python3
"""
validate_artifacts.py — Validate artifact repository integrity.

Checks that all expected files exist, row counts match, function IDs
are consistent, labels and methods use canonical values, and label
counts match the paper's reported results.

Exits with code 1 if any validation check fails.

Usage:
    python scripts/validate_artifacts.py
"""

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Expected label counts from the paper
EXPECTED_COUNTS = {
    "Generic Prompting": {"Correct": 7, "Partial": 4, "Incorrect": 4},
    "Project-Specific ICL": {"Correct": 11, "Partial": 3, "Incorrect": 1},
}

VALID_METHODS = {"Generic Prompting", "Project-Specific ICL"}
VALID_LABELS = {"Correct", "Partial", "Incorrect"}

errors = []


def check(condition: bool, message: str) -> None:
    """Record a validation failure if condition is False."""
    if not condition:
        errors.append(message)
        print(f"  FAIL: {message}")
    else:
        print(f"  PASS: {message}")


def main():
    print("=" * 70)
    print("ARTIFACT VALIDATION")
    print("=" * 70)

    # --- 1. Check expected files exist ---
    print("\n[1] Checking expected files exist...")
    expected_files = [
        "README.md",
        "requirements.txt",
        ".gitignore",
        "data/target_functions.csv",
        "data/project_examples.csv",
        "data/evaluation_labels.csv",
        "prompts/generic_prompt.txt",
        "prompts/project_specific_prompt.txt",
        "outputs/generic_outputs.csv",
        "outputs/project_specific_outputs.csv",
        "scripts/compute_results.py",
        "scripts/summarize_labels.py",
        "scripts/validate_artifacts.py",
        "scripts/generate_latex_tables.py",
        "baseline_reproducibility/README.md",
        "baseline_reproducibility/baselines_config.json",
        "baseline_reproducibility/inspect_baselines.py",
        "docs/artifact_report.md",
        "docs/reproduction_instructions.md",
    ]
    for fpath in expected_files:
        full = PROJECT_ROOT / fpath
        check(full.exists(), f"File exists: {fpath}")

    # --- 2. Load CSVs ---
    print("\n[2] Loading CSV files...")
    target_df = pd.read_csv(PROJECT_ROOT / "data" / "target_functions.csv")
    generic_df = pd.read_csv(PROJECT_ROOT / "outputs" / "generic_outputs.csv")
    project_df = pd.read_csv(PROJECT_ROOT / "outputs" / "project_specific_outputs.csv")
    labels_df = pd.read_csv(PROJECT_ROOT / "data" / "evaluation_labels.csv")

    # --- 3. Row counts ---
    print("\n[3] Checking row counts...")
    check(len(target_df) == 15, f"target_functions.csv has 15 rows (found {len(target_df)})")
    check(len(generic_df) == 15, f"generic_outputs.csv has 15 rows (found {len(generic_df)})")
    check(len(project_df) == 15, f"project_specific_outputs.csv has 15 rows (found {len(project_df)})")
    check(len(labels_df) == 30, f"evaluation_labels.csv has 30 rows (found {len(labels_df)})")

    # --- 4. Function ID consistency ---
    print("\n[4] Checking function_id consistency...")
    target_ids = set(target_df["function_id"])

    generic_ids = set(generic_df["function_id"])
    check(generic_ids.issubset(target_ids),
          f"All generic_outputs function_ids exist in target_functions (extra: {generic_ids - target_ids})")

    project_ids = set(project_df["function_id"])
    check(project_ids.issubset(target_ids),
          f"All project_specific_outputs function_ids exist in target_functions (extra: {project_ids - target_ids})")

    label_ids = set(labels_df["function_id"])
    check(label_ids.issubset(target_ids),
          f"All evaluation_labels function_ids exist in target_functions (extra: {label_ids - target_ids})")

    # --- 5. Valid methods ---
    print("\n[5] Checking method values...")
    label_methods = set(labels_df["method"].unique())
    check(label_methods == VALID_METHODS,
          f"Methods are exactly {VALID_METHODS} (found {label_methods})")

    # --- 6. Valid labels ---
    print("\n[6] Checking label values...")
    label_values = set(labels_df["label"].unique())
    check(label_values.issubset(VALID_LABELS),
          f"Labels are subset of {VALID_LABELS} (found {label_values})")

    # --- 7. Label counts match paper ---
    print("\n[7] Checking label counts match paper's reported results...")
    for method, expected in EXPECTED_COUNTS.items():
        subset = labels_df[labels_df["method"] == method]
        for label, expected_count in expected.items():
            actual_count = (subset["label"] == label).sum()
            check(actual_count == expected_count,
                  f"{method} — {label}: expected {expected_count}, found {actual_count}")

    # --- 8. No empty summaries ---
    print("\n[8] Checking for empty generated_summary values...")
    generic_empty = generic_df["generated_summary"].isna().sum() + (generic_df["generated_summary"].str.strip() == "").sum()
    check(generic_empty == 0, f"No empty summaries in generic_outputs.csv (found {generic_empty} empty)")

    project_empty = project_df["generated_summary"].isna().sum() + (project_df["generated_summary"].str.strip() == "").sum()
    check(project_empty == 0, f"No empty summaries in project_specific_outputs.csv (found {project_empty} empty)")

    # --- 9. Repository coverage ---
    print("\n[9] Checking repository coverage...")
    repos = set(target_df["repository"].unique())
    expected_repos = {"requests", "pandas", "scikit-learn"}
    check(repos == expected_repos, f"Repositories are {expected_repos} (found {repos})")

    for repo in expected_repos:
        count = (target_df["repository"] == repo).sum()
        check(count == 5, f"Repository '{repo}' has 5 functions (found {count})")

    # --- 10. No duplicate function_id + method rows in labels ---
    print("\n[10] Checking for duplicate function_id + method rows in labels...")
    dup_check = labels_df.groupby(["function_id", "method"]).size()
    duplicates = dup_check[dup_check > 1]
    check(len(duplicates) == 0,
          f"No duplicate function_id+method rows in evaluation_labels.csv (found {len(duplicates)} duplicates)")

    # --- Summary ---
    print("\n" + "=" * 70)
    if errors:
        print(f"VALIDATION FAILED: {len(errors)} error(s) found.")
        for i, err in enumerate(errors, 1):
            print(f"  {i}. {err}")
        sys.exit(1)
    else:
        print("ALL VALIDATION CHECKS PASSED.")
        sys.exit(0)


if __name__ == "__main__":
    main()
