#!/usr/bin/env python3
"""
generate_latex_tables.py — Generate LaTeX table snippets for the paper.

Produces tables for:
  1. Dataset composition
  2. Target functions
  3. Result summary
  4. Label percentages
  5. Reproducibility baseline status
  6. Top 22 above-the-knee papers
  7. Thematic group sizes
  8. Venn disjoint region counts
  9. Reproduction study table

Saves all tables to outputs/latex_tables.tex.

Usage:
    python scripts/generate_latex_tables.py
"""

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LABELS_PATH = PROJECT_ROOT / "data" / "evaluation_labels.csv"
TARGETS_PATH = PROJECT_ROOT / "data" / "target_functions.csv"
BASELINES_PATH = PROJECT_ROOT / "baseline_reproducibility" / "baseline_attempts.csv"
ABOVE_KNEE_PATH = PROJECT_ROOT / "data" / "above_knee_papers.csv"
THEMATIC_PATH = PROJECT_ROOT / "data" / "thematic_classification.csv"
VENN_PATH = PROJECT_ROOT / "data" / "venn_counts.csv"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "latex_tables.tex"


def generate_dataset_composition(targets: pd.DataFrame) -> str:
    """Table 1: Dataset composition by repository."""
    lines = []
    lines.append("% Table: Dataset Composition")
    lines.append("\\begin{table}[ht]")
    lines.append("\\centering")
    lines.append("\\caption{Dataset Composition by Repository}")
    lines.append("\\label{tab:dataset-composition}")
    lines.append("\\begin{tabular}{lcc}")
    lines.append("\\toprule")
    lines.append("Repository & Functions & Proportion \\\\")
    lines.append("\\midrule")
    total = len(targets)
    for repo in ["requests", "pandas", "scikit-learn"]:
        count = (targets["repository"] == repo).sum()
        pct = count / total * 100
        lines.append(f"{repo} & {count} & {pct:.1f}\\% \\\\")
    lines.append("\\midrule")
    lines.append(f"\\textbf{{Total}} & \\textbf{{{total}}} & \\textbf{{100.0\\%}} \\\\")
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("\\end{table}")
    return "\n".join(lines)


def generate_target_functions_table(targets: pd.DataFrame) -> str:
    """Table 2: Target functions."""
    lines = []
    lines.append("% Table: Target Functions")
    lines.append("\\begin{table}[ht]")
    lines.append("\\centering")
    lines.append("\\caption{Target Functions Used in the Study}")
    lines.append("\\label{tab:target-functions}")
    lines.append("\\begin{tabular}{llll}")
    lines.append("\\toprule")
    lines.append("ID & Repository & Module & Function \\\\")
    lines.append("\\midrule")
    for _, row in targets.iterrows():
        fid = row["function_id"]
        repo = row["repository"]
        module = row["module"].replace("_", "\\_")
        func = row["target_function"].replace("_", "\\_")
        lines.append(f"{fid} & {repo} & \\texttt{{{module}}} & \\texttt{{{func}}} \\\\")
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("\\end{table}")
    return "\n".join(lines)


def generate_result_summary_table(labels: pd.DataFrame) -> str:
    """Table 3: Result summary."""
    lines = []
    lines.append("% Table: Result Summary")
    lines.append("\\begin{table}[ht]")
    lines.append("\\centering")
    lines.append("\\caption{Summary of Evaluation Results}")
    lines.append("\\label{tab:result-summary}")
    lines.append("\\begin{tabular}{lccccc}")
    lines.append("\\toprule")
    lines.append("Method & Correct & Partial & Incorrect & Total & Correctness Rate \\\\")
    lines.append("\\midrule")
    for method in ["Generic Prompting", "Project-Specific ICL"]:
        subset = labels[labels["method"] == method]
        total = len(subset)
        correct = (subset["label"] == "Correct").sum()
        partial = (subset["label"] == "Partial").sum()
        incorrect = (subset["label"] == "Incorrect").sum()
        rate = correct / total * 100 if total > 0 else 0.0
        lines.append(f"{method} & {correct} & {partial} & {incorrect} & {total} & {rate:.1f}\\% \\\\")
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("\\end{table}")
    return "\n".join(lines)


def generate_label_percentage_table(labels: pd.DataFrame) -> str:
    """Table 4: Label percentages by method."""
    lines = []
    lines.append("% Table: Label Percentages")
    lines.append("\\begin{table}[ht]")
    lines.append("\\centering")
    lines.append("\\caption{Label Distribution (\\%) by Method}")
    lines.append("\\label{tab:label-percentages}")
    lines.append("\\begin{tabular}{lccc}")
    lines.append("\\toprule")
    lines.append("Method & Correct (\\%) & Partial (\\%) & Incorrect (\\%) \\\\")
    lines.append("\\midrule")
    for method in ["Generic Prompting", "Project-Specific ICL"]:
        subset = labels[labels["method"] == method]
        total = len(subset)
        c = (subset["label"] == "Correct").sum() / total * 100
        p = (subset["label"] == "Partial").sum() / total * 100
        i = (subset["label"] == "Incorrect").sum() / total * 100
        lines.append(f"{method} & {c:.1f} & {p:.1f} & {i:.1f} \\\\")
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("\\end{table}")
    return "\n".join(lines)


def generate_baseline_table(baselines_path: Path) -> str:
    """Table 5: Reproducibility baseline status."""
    lines = []
    lines.append("% Table: Reproducibility Baseline Status")
    lines.append("\\begin{table}[ht]")
    lines.append("\\centering")
    lines.append("\\caption{Reproducibility Status of Referenced Baseline Systems}")
    lines.append("\\label{tab:baseline-status}")
    lines.append("\\begin{tabular}{llll}")
    lines.append("\\toprule")
    lines.append("System & Repo Available & Status & Issue \\\\")
    lines.append("\\midrule")

    if baselines_path.exists():
        bdf = pd.read_csv(baselines_path)
        for _, row in bdf.iterrows():
            name = row.get("paper_or_system", row.get("system_name", "Unknown"))
            repo_found = row.get("repo_available", row.get("public_repo_found", "Unknown"))
            status = row.get("attempt_status", row.get("status", "Unknown"))
            issue = row.get("observed_issue", row.get("issue_observed", "N/A"))
            # Escape underscores for LaTeX
            name = str(name).replace("_", "\\_")
            issue = str(issue).replace("_", "\\_")
            lines.append(f"{name} & {repo_found} & {status} & {issue} \\\\")
    else:
        lines.append("\\multicolumn{4}{c}{\\textit{Baseline attempts file not found.}} \\\\")

    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("\\end{table}")
    return "\n".join(lines)


def main():
    print(f"Loading data from: {PROJECT_ROOT}")

    targets = pd.read_csv(TARGETS_PATH)
    labels = pd.read_csv(LABELS_PATH)

    tables = []
    tables.append(generate_dataset_composition(targets))
    tables.append("")
    tables.append(generate_target_functions_table(targets))
    tables.append("")
    tables.append(generate_result_summary_table(labels))
    tables.append("")
    tables.append(generate_label_percentage_table(labels))
    tables.append("")
    tables.append(generate_baseline_table(BASELINES_PATH))

    # --- New literature review tables ---
    if ABOVE_KNEE_PATH.exists():
        tables.append("")
        tables.append(generate_above_knee_table(ABOVE_KNEE_PATH))

    if THEMATIC_PATH.exists():
        tables.append("")
        tables.append(generate_thematic_group_table(THEMATIC_PATH))

    if VENN_PATH.exists():
        tables.append("")
        tables.append(generate_venn_table(VENN_PATH))

    tables.append("")
    tables.append(generate_reproduction_study_table(BASELINES_PATH))

    output = "\n\n".join(tables) + "\n"

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(output)
    print(f"LaTeX tables written to: {OUTPUT_PATH}")
    table_count = sum(1 for t in tables if t.strip().startswith("% Table"))
    print(f"Generated {table_count} table environments.")


def generate_above_knee_table(path: Path) -> str:
    """Table 6: Top 22 above-the-knee papers."""
    df = pd.read_csv(path)
    lines = []
    lines.append("% Table: Above-the-Knee Papers")
    lines.append("\\begin{table*}[ht]")
    lines.append("\\centering")
    lines.append("\\caption{Top 22 Above-the-Knee Papers by Citation Count}")
    lines.append("\\label{tab:above-knee}")
    lines.append("\\begin{tabular}{clc}")
    lines.append("\\toprule")
    lines.append("Rank & Title & Citations \\\\")
    lines.append("\\midrule")
    for _, row in df.iterrows():
        rank = int(row["rank"])
        title = str(row["title"]).replace("_", "\\_").replace("&", "\\&")
        cites = int(row["citation_count"])
        lines.append(f"{rank} & {title} & {cites} \\\\")
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("\\end{table*}")
    return "\n".join(lines)


def generate_thematic_group_table(path: Path) -> str:
    """Table 7: Thematic group sizes."""
    df = pd.read_csv(path)
    lines = []
    lines.append("% Table: Thematic Group Sizes")
    lines.append("\\begin{table}[ht]")
    lines.append("\\centering")
    lines.append("\\caption{Thematic Group Sizes (22 Above-the-Knee Papers)}")
    lines.append("\\label{tab:thematic-groups}")
    lines.append("\\begin{tabular}{lc}")
    lines.append("\\toprule")
    lines.append("Theme & Papers \\\\")
    lines.append("\\midrule")
    themes = [
        ("P: Project-Specific Context", "project_context"),
        ("I: In-Context Learning \\& Prompting", "in_context_learning"),
        ("M: Code Summarization Methods", "methods"),
        ("E: Evaluation \\& Reliability", "evaluation_reliability"),
    ]
    for label, col in themes:
        if col in df.columns:
            count = int(df[col].sum())
            lines.append(f"{label} & {count} \\\\")
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("\\end{table}")
    return "\n".join(lines)


def generate_venn_table(path: Path) -> str:
    """Table 8: Venn disjoint region counts."""
    df = pd.read_csv(path)
    lines = []
    lines.append("% Table: Venn Disjoint Region Counts")
    lines.append("\\begin{table}[ht]")
    lines.append("\\centering")
    lines.append("\\caption{Disjoint Venn Region Counts for Thematic Classification}")
    lines.append("\\label{tab:venn-counts}")
    lines.append("\\begin{tabular}{lc}")
    lines.append("\\toprule")
    lines.append("Region & Count \\\\")
    lines.append("\\midrule")
    for _, row in df.iterrows():
        region = str(row["region"]).replace("∩", "$\\cap$")
        count = int(row["count"])
        lines.append(f"{region} & {count} \\\\")
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("\\end{table}")
    return "\n".join(lines)


def generate_reproduction_study_table(baselines_path: Path) -> str:
    """Table 9: Reproduction study outcomes."""
    lines = []
    lines.append("% Table: Reproduction Study Outcomes")
    lines.append("\\begin{table*}[ht]")
    lines.append("\\centering")
    lines.append("\\caption{Baseline Reproduction Study Outcomes}")
    lines.append("\\label{tab:reproduction-study}")
    lines.append("\\begin{tabular}{lccll}")
    lines.append("\\toprule")
    lines.append("System & Repo Found & Runs & Feasible & Decision \\\\")
    lines.append("\\midrule")
    # Hardcoded from documented reproduction outcomes
    entries = [
        ("Ahmed \\& Devanbu 2022", "Yes", "No", "Maybe",
         "Conceptual baseline; API deprecated"),
        ("Ahmad et al.\\ 2020 (NeuralCodeSum)", "Yes", "No", "Maybe",
         "Supervised baseline; missing data"),
        ("Yun et al.\\ 2024 (P-CodeSum)", "Yes", "Partial", "Likely",
         "Most promising runnable baseline"),
    ]
    for name, repo, runs, feasible, decision in entries:
        lines.append(f"{name} & {repo} & {runs} & {feasible} & {decision} \\\\")
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("\\end{table*}")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
