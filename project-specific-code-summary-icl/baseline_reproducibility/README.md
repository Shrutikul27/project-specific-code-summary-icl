# Baseline Reproducibility

This directory documents our inspection of prior baseline systems referenced
in the paper. These are **not** direct executable baselines for our experiment —
our direct empirical baseline is **Generic Prompting**.

## Referenced Systems

| System | Paper | Repo URL | Repo Available | Status |
|--------|-------|----------|----------------|--------|
| Few-shot Code Summarization | Ahmed and Devanbu 2022 | [toufiqueparag/few_shot_code_summarization](https://github.com/toufiqueparag/few_shot_code_summarization) | Yes | repo found; inspect/run status pending |
| NeuralCodeSum | Ahmad et al. 2020 | [wasiahmad/NeuralCodeSum](https://github.com/wasiahmad/NeuralCodeSum) | Yes | repo found; inspect/run status pending |
| P-CodeSum | Yun et al. 2024 | [Linshuhuai/P-CodeSum](https://github.com/Linshuhuai/P-CodeSum) | Yes | repo found; inspect/run status pending |

## Status Definitions

- **repo found; inspect/run status pending**: Public repository was identified.
  Local cloning, dependency installation, and execution have not yet been
  attempted or verified.
- **inspected**: Repository was cloned and briefly reviewed, but not
  executed end-to-end.
- **failed unmodified**: Repository was cloned and execution was attempted
  but failed without modification.
- **partial**: Some components ran successfully but full reproduction was
  not achieved.
- **runnable**: System was successfully executed and results were obtained.

## Notes on Each Baseline

1. **Ahmed and Devanbu 2022** ([paper](https://arxiv.org/abs/2207.04237)):
   Repository at https://github.com/toufiqueparag/few_shot_code_summarization
   contains dataset and scripts from the ASE-NIER paper. Full reproduction
   still needs local verification of dependencies and execution steps.

2. **Ahmad et al. 2020 (NeuralCodeSum)**:
   Repository at https://github.com/wasiahmad/NeuralCodeSum contains training
   and evaluation code. Full reproduction may require original datasets
   (CodeSearchNet), dependency setup, and model training/evaluation steps.

3. **Yun et al. 2024 (P-CodeSum)**:
   Repository at https://github.com/Linshuhuai/P-CodeSum. Full reproduction
   may require project-specific setup, model/API configuration, and dataset
   preparation.

## Important

- **Do not overclaim reproduction.** None of the baselines above have been
  confirmed as fully reproduced unless the `attempt_status` column in
  `baseline_attempts.csv` explicitly says so.
- Our direct empirical baseline is **Generic Prompting**.
- These prior systems are treated as **reproducibility/reference baselines**.

## How to Use

```bash
# Print baseline metadata (no network calls)
python inspect_baselines.py

# Optionally clone public repos (requires network + git)
python inspect_baselines.py --clone
```

The `external/` directory (created by `--clone`) is git-ignored.

## Files

- `baselines_config.json` — Structured metadata for each baseline.
- `baseline_attempts.csv` — Tabular summary of inspection results.
- `inspect_baselines.py` — Script to print metadata and optionally clone repos.
