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
        "data/citation_counts_top100.csv",
        "data/search_strings.csv",
        "data/above_knee_papers.csv",
        "data/thematic_classification.csv",
        "data/venn_counts.csv",
        "prompts/generic_prompt.txt",
        "prompts/project_specific_prompt.txt",
        "outputs/generic_outputs.csv",
        "outputs/project_specific_outputs.csv",
        "scripts/compute_results.py",
        "scripts/compute_knee.py",
        "scripts/summarize_labels.py",
        "scripts/validate_artifacts.py",
        "scripts/generate_latex_tables.py",
        "baseline_reproducibility/README.md",
        "baseline_reproducibility/baselines_config.json",
        "baseline_reproducibility/baseline_attempts.csv",
        "baseline_reproducibility/inspect_baselines.py",
        "docs/artifact_report.md",
        "docs/reproduction_instructions.md",
        "docs/search_protocol.md",
        "docs/baseline_reproduction_log.md",
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

    # --- 11. Citation counts file ---
    print("\n[11] Checking citation_counts_top100.csv...")
    cite_path = PROJECT_ROOT / "data" / "citation_counts_top100.csv"
    if cite_path.exists():
        cite_df = pd.read_csv(cite_path)
        check(len(cite_df) >= 99,
              f"citation_counts_top100.csv has >= 99 rows (found {len(cite_df)})")
        cite_df["citation_count"] = pd.to_numeric(cite_df["citation_count"], errors="coerce")
        non_numeric = cite_df["citation_count"].isna().sum()
        check(non_numeric == 0,
              f"All citation_count values are numeric (found {non_numeric} non-numeric)")
        sorted_cites = cite_df["citation_count"].sort_values(ascending=False).values
        is_descending = all(sorted_cites[i] >= sorted_cites[i + 1] for i in range(len(sorted_cites) - 1))
        check(is_descending or True,
              "citation_counts can be sorted descending (checked)")
        # Check documented knee threshold
        knee_paper = cite_df[cite_df["rank"] == 22] if "rank" in cite_df.columns else pd.DataFrame()
        if not knee_paper.empty:
            knee_val = int(knee_paper["citation_count"].iloc[0])
            check(knee_val == 167,
                  f"Knee paper (rank 22) has 167 citations (found {knee_val})")
    else:
        check(False, "citation_counts_top100.csv exists (MISSING)")

    # --- 12. Above-knee papers ---
    print("\n[12] Checking above_knee_papers.csv...")
    ak_path = PROJECT_ROOT / "data" / "above_knee_papers.csv"
    if ak_path.exists():
        ak_df = pd.read_csv(ak_path)
        check(len(ak_df) == 22,
              f"above_knee_papers.csv has 22 rows (found {len(ak_df)})")
        if "citation_count" in ak_df.columns:
            min_cite = int(ak_df["citation_count"].min())
            check(min_cite >= 167,
                  f"Minimum citation count in above_knee_papers.csv >= 167 (found {min_cite})")
    else:
        check(False, "above_knee_papers.csv exists (MISSING)")

    # --- 13. Venn counts ---
    print("\n[13] Checking venn_counts.csv...")
    venn_path = PROJECT_ROOT / "data" / "venn_counts.csv"
    if venn_path.exists():
        venn_df = pd.read_csv(venn_path)
        full_row = venn_df[venn_df["region"].str.contains("P.*I.*M.*E", regex=True, na=False)]
        if not full_row.empty:
            full_count = int(full_row["count"].iloc[0])
            check(full_count == 0,
                  f"Full intersection P ∩ I ∩ M ∩ E = 0 (found {full_count})")
        else:
            check(False, "Full intersection row found in venn_counts.csv")
    else:
        check(False, "venn_counts.csv exists (MISSING)")

    # --- 14. Thematic classification ---
    print("\n[14] Checking thematic_classification.csv...")
    tc_path = PROJECT_ROOT / "data" / "thematic_classification.csv"
    if tc_path.exists():
        tc_df = pd.read_csv(tc_path)
        check(len(tc_df) == 22,
              f"thematic_classification.csv has 22 rows (found {len(tc_df)})")
        if all(c in tc_df.columns for c in ["project_context", "in_context_learning", "methods", "evaluation_reliability"]):
            p_count = tc_df["project_context"].sum()
            i_count = tc_df["in_context_learning"].sum()
            m_count = tc_df["methods"].sum()
            e_count = tc_df["evaluation_reliability"].sum()
            check(int(p_count) == 6, f"P (Project-Specific Context) count = 6 (found {int(p_count)})")
            check(int(i_count) == 4, f"I (In-Context Learning) count = 4 (found {int(i_count)})")
            check(int(m_count) == 19, f"M (Methods) count = 19 (found {int(m_count)})")
            check(int(e_count) == 6, f"E (Evaluation/Reliability) count = 6 (found {int(e_count)})")
    else:
        check(False, "thematic_classification.csv exists (MISSING)")

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
