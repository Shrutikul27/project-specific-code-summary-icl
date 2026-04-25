# Does Project-Specific In-Context Learning Improve the Reliability of LLM-Generated Code Summaries?

## Research Question

**RQ:** Does project-specific in-context learning improve the reliability of
LLM-generated code summaries compared to generic prompting?

## Key Result

| Method | Correct | Partial | Incorrect | Total | Correctness Rate |
|--------|---------|---------|-----------|-------|-----------------|
| Generic Prompting | 7 | 4 | 4 | 15 | 46.7% |
| Project-Specific ICL | 11 | 3 | 1 | 15 | 73.3% |

Project-specific in-context learning improved correctness rate from 46.7% to
73.3% and reduced the incorrect-summary rate from 26.7% to 6.7%.

## Artifact Structure

```
project-specific-code-summary-icl/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .gitignore
├── paper/
│   ├── main.tex                       # LaTeX paper source
│   ├── references.bib                 # BibTeX references
│   └── figures/                       # Figures directory
├── data/
│   ├── target_functions.csv           # 15 target Python functions
│   ├── project_examples.csv           # Project-specific example pairs
│   └── evaluation_labels.csv          # 30 manual evaluation labels
├── prompts/
│   ├── generic_prompt.txt             # Generic prompting template
│   └── project_specific_prompt.txt    # Project-specific ICL template
├── outputs/
│   ├── generic_outputs.csv            # 15 generic-prompt summaries
│   ├── project_specific_outputs.csv   # 15 project-specific summaries
│   ├── result_summary.csv             # Generated result table
│   └── latex_tables.tex               # Generated LaTeX tables
├── scripts/
│   ├── compute_results.py             # Compute result summary
│   ├── summarize_labels.py            # Detailed label breakdown
│   ├── validate_artifacts.py          # Artifact integrity validation
│   └── generate_latex_tables.py       # Generate LaTeX table snippets
├── baseline_reproducibility/
│   ├── README.md                      # Baseline inspection documentation
│   ├── baselines_config.json          # Baseline metadata
│   ├── baseline_attempts.csv          # Inspection results
│   └── inspect_baselines.py           # Baseline inspection script
└── docs/
    ├── artifact_report.md             # Artifact summary report
    └── reproduction_instructions.md   # Step-by-step reproduction guide
```

## Dataset

- **15 target Python functions** from 3 open-source repositories:
  - [Requests](https://github.com/psf/requests) (5 functions)
  - [pandas](https://github.com/pandas-dev/pandas) (5 functions)
  - [scikit-learn](https://github.com/scikit-learn/scikit-learn) (5 functions)
- **2 prompting methods**: Generic Prompting and Project-Specific ICL
- **30 total generated summaries** (15 per method)
- **Manual evaluation labels**: Correct, Partial, Incorrect

**Note:** The project-specific examples in `data/project_examples.csv` are
manually written summaries used for ICL prompting. They are not claimed to be
exact original docstrings from the source repositories.

## Prompting Methods

### Generic Prompting
A zero-shot prompt that provides only a summarization instruction and the
target function code. No project-specific context is included.

### Project-Specific ICL
A few-shot prompt that includes 2–3 example function–summary pairs from the
**same project** as the target function, followed by the target function code.
Examples are selected to convey the project's conventions and vocabulary.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Validate artifact integrity
python scripts/validate_artifacts.py

# 3. Compute result summary
python scripts/compute_results.py

# 4. Detailed label breakdown
python scripts/summarize_labels.py

# 5. Generate LaTeX tables
python scripts/generate_latex_tables.py

# 6. Inspect baseline systems (no network calls)
python baseline_reproducibility/inspect_baselines.py
```

## Expected Output from `compute_results.py`

```
Loading labels from: data/evaluation_labels.csv
Loaded 30 label rows.

======================================================================
RESULT SUMMARY
======================================================================
+----------------------+-----------+----------+-------------+---------+----------------------+--------------------+
| Method               |   Correct |   Partial |   Incorrect |   Total |   Correctness Rate (%) |   Incorrect Rate (%) |
+======================+===========+==========+=============+=========+======================+====================+
| Generic Prompting    |         7 |        4 |           4 |      15 |                 46.7 |               26.7 |
+----------------------+-----------+----------+-------------+---------+----------------------+--------------------+
| Project-Specific ICL |        11 |        3 |           1 |      15 |                 73.3 |                6.7 |
+----------------------+-----------+----------+-------------+---------+----------------------+--------------------+
```

## Baseline Reproducibility

The paper references three prior systems:
1. **Ahmed and Devanbu 2022** — Few-shot training LLMs for code summarization
   ([repo](https://github.com/toufiqueparag/few_shot_code_summarization))
2. **Ahmad et al. 2020** — NeuralCodeSum (Transformer-based)
   ([repo](https://github.com/wasiahmad/NeuralCodeSum))
3. **Yun et al. 2024** — P-CodeSum (project-specific ICL)
   ([repo](https://github.com/Linshuhuai/P-CodeSum))

These are treated as **reproducibility reference baselines**, not direct
executable baselines. Our direct empirical baseline is Generic Prompting.
All three repos have been identified as publicly available, but full
reproduction (cloning, dependency setup, training/evaluation) has not yet
been confirmed. See `baseline_reproducibility/README.md` for details.

## Limitations

- This is a **small-scale exploratory study** (n=15 functions, 30 summaries).
- Manual labels are subjective and should be inspected by reviewers.
- Generated summaries are artifacts of the study and may not reflect current
  LLM capabilities.
- Prior baseline systems were not fully reproduced.
- Statistical significance testing is limited by sample size.

## License

This artifact repository is provided for academic review and reproducibility
purposes.
