# Reproduction Instructions

Step-by-step guide to reproduce the result tables reported in the paper.

## Prerequisites

- Python 3.9+
- pip

## Step 1: Clone the Repository

```bash
git clone <repo-url>
cd project-specific-code-summary-icl
```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `pandas>=2.0.0` — data manipulation
- `tabulate>=0.9.0` — formatted table output

## Step 3: Validate Artifact Integrity

```bash
python scripts/validate_artifacts.py
```

This script checks:
- All expected files exist
- `target_functions.csv` has exactly 15 rows
- `generic_outputs.csv` has exactly 15 rows
- `project_specific_outputs.csv` has exactly 15 rows
- `evaluation_labels.csv` has exactly 30 rows
- All function IDs are consistent across files
- Methods are exactly "Generic Prompting" and "Project-Specific ICL"
- Labels are exactly "Correct", "Partial", or "Incorrect"
- Label counts match the paper's reported results
- No empty generated summaries exist

**Expected output:** `ALL VALIDATION CHECKS PASSED.`

If validation fails, the script exits with code 1 and prints the specific
failures.

## Step 4: Compute Result Summary

```bash
python scripts/compute_results.py
```

This reproduces the main result table:

| Method | Correct | Partial | Incorrect | Total | Correctness Rate |
|--------|---------|---------|-----------|-------|-----------------|
| Generic Prompting | 7 | 4 | 4 | 15 | 46.7% |
| Project-Specific ICL | 11 | 3 | 1 | 15 | 73.3% |

Results are automatically saved to `outputs/result_summary.csv`.

## Step 5: Detailed Label Breakdown

```bash
python scripts/summarize_labels.py
```

This prints:
- Label counts by method
- Label percentages by method
- Details of all Incorrect cases with notes
- Details of all Partial cases with notes
- Per-function cross-method comparison (improved / same / degraded)

## Step 6: Generate LaTeX Tables

```bash
python scripts/generate_latex_tables.py
```

This generates `outputs/latex_tables.tex` containing five LaTeX table
environments ready to be included in the paper:
1. Dataset composition by repository
2. Target functions
3. Result summary
4. Label percentages
5. Reproducibility baseline status

## Step 7: Inspect Baseline Systems (Optional)

```bash
python baseline_reproducibility/inspect_baselines.py
```

This prints metadata for each referenced baseline system. No network calls
are made. Add `--clone` to clone public repositories (requires network access).

## Verifying the Results

After running Steps 3–4, confirm that:

1. `validate_artifacts.py` reports `ALL VALIDATION CHECKS PASSED.`
2. `compute_results.py` output matches the result table above.
3. `outputs/result_summary.csv` contains the same values.

These three checks confirm that the artifact repository faithfully supports
the paper's reported results.

## Troubleshooting

- **ModuleNotFoundError: No module named 'pandas'**
  → Run `pip install -r requirements.txt`
- **FileNotFoundError for CSV files**
  → Ensure you are running scripts from the repository root directory.
- **Validation fails on label counts**
  → Check that `data/evaluation_labels.csv` has not been modified.

## Verifying the Results

After running Steps 3–4, confirm that:

1. `validate_artifacts.py` reports `ALL VALIDATION CHECKS PASSED.`
2. `compute_results.py` output matches the table above.
3. `outputs/result_summary.csv` contains the same values.

These three checks confirm that the artifact repository faithfully supports
the paper's reported results.

## Troubleshooting

- **ModuleNotFoundError: No module named 'pandas'**
  → Run `pip install -r requirements.txt`
- **FileNotFoundError for CSV files**
  → Ensure you are running scripts from the repository root directory.
- **Validation fails on label counts**
  → Check that `data/evaluation_labels.csv` has not been modified.
