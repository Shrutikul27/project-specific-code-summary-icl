# Artifact Report

## Paper

**Title:** Does Project-Specific In-Context Learning Improve the Reliability
of LLM-Generated Code Summaries?

## What Is Included

### Data
- `data/target_functions.csv` — 15 target Python functions from 3 repositories
  (Requests, pandas, scikit-learn), with source URLs.
- `data/project_examples.csv` — 9 project-specific example function–summary
  pairs (3 per repository) used for ICL prompting.
- `data/evaluation_labels.csv` — 30 manual evaluation labels (15 per method)
  with labels: Correct, Partial, Incorrect.

### Prompts
- `prompts/generic_prompt.txt` — Zero-shot summarization prompt template.
- `prompts/project_specific_prompt.txt` — Few-shot ICL prompt template with
  example placeholders.

### Outputs
- `outputs/generic_outputs.csv` — 15 summaries generated via generic prompting.
- `outputs/project_specific_outputs.csv` — 15 summaries generated via
  project-specific ICL.

### Scripts
- `scripts/compute_results.py` — Reproduces the main result table.
- `scripts/compute_knee.py` — Knee analysis on the citation curve.
- `scripts/summarize_labels.py` — Detailed label breakdown and analysis.
- `scripts/validate_artifacts.py` — Validates artifact integrity.
- `scripts/generate_latex_tables.py` — Generates LaTeX tables for the paper.

### Literature Review Data
- `data/citation_counts_top100.csv` — Top 100 papers by citation count.
- `data/search_strings.csv` — Literature search queries.
- `data/above_knee_papers.csv` — 22 above-the-knee papers.
- `data/thematic_classification.csv` — Thematic coding (P, I, M, E).
- `data/venn_counts.csv` — Disjoint Venn region counts.

### Baseline Reproducibility
- `baseline_reproducibility/` — Documentation and scripts for inspecting
  referenced baseline systems.

## What Is Not Included

- **LLM API access or credentials.** The generated summaries are provided as
  static artifacts. Reproducing the LLM generation step requires access to the
  original LLM endpoint.
- **Full baseline reproduction.** Prior systems (Ahmed and Devanbu 2022,
  Ahmad et al. 2020, Yun et al. 2024) were not fully reproduced. See
  `baseline_reproducibility/README.md` for detailed reasons.
- **Raw source code of target functions.** The target functions can be
  retrieved from their official GitHub repositories using the URLs in
  `data/target_functions.csv`.
- **Statistical significance tests.** The sample size (n=15) is too small
  for robust statistical testing. The study is exploratory.

## Limitations

1. **Small sample size.** 15 functions and 30 summaries constitute a
   small-scale exploratory study. Results should be interpreted cautiously.
2. **Manual labeling subjectivity.** Labels (Correct, Partial, Incorrect)
   were assigned manually. Different annotators may produce different labels.
   No inter-rater reliability score is reported.
3. **Single LLM.** Results reflect the behavior of one LLM at one point in
   time. Different models or API versions may produce different results.
4. **Static artifacts.** The generated summaries are frozen artifacts. They
   cannot be regenerated without the original LLM endpoint configuration.

## How This Supports the Paper

This artifact repository supports the following paper sections:

| Paper Section | Supporting Artifact |
|--------------|-------------------|
| Experimental Rig | `data/target_functions.csv`, `data/project_examples.csv`, `prompts/` |
| What Was Seen | `outputs/generic_outputs.csv`, `outputs/project_specific_outputs.csv` |
| Evaluation Rigor | `data/evaluation_labels.csv`, `scripts/validate_artifacts.py` |
| Literature Search | `data/citation_counts_top100.csv`, `data/search_strings.csv`, `docs/search_protocol.md` |
| Knee Analysis | `scripts/compute_knee.py`, `data/above_knee_papers.csv` |
| Thematic Classification | `data/thematic_classification.csv`, `data/venn_counts.csv` |
| Results | `scripts/compute_results.py`, `outputs/result_summary.csv` |
| Reproducibility | `baseline_reproducibility/`, `docs/baseline_reproduction_log.md` |
| Replication Artifacts | This entire repository |

## Why Prior Baselines Are Reference Baselines

The paper's direct empirical baseline is **Generic Prompting**. Prior systems
are cited as related work and inspected for reproducibility, but not executed
as direct comparison baselines:

1. **Ahmed and Devanbu 2022** — Repo cloned; failed because `code-davinci-002`
   API is deprecated.
2. **Ahmad et al. 2020 (NeuralCodeSum)** — Repo cloned; failed because required
   Java dataset files were missing.
3. **Yun et al. 2024 (P-CodeSum)** — Repo cloned; partial success. Scripts run
   but default data paths are incorrect. Most promising runnable baseline.

See `baseline_reproducibility/baseline_attempts.csv` and
`docs/baseline_reproduction_log.md` for full details.

## Remaining TODOs

1. **GitHub URL in paper:** Replace `<username>` in `paper/main.tex` with
   the actual GitHub username after the repo is published.
2. **Author info:** Update author name(s) and affiliation(s) in
   `paper/main.tex` if provided.
3. **Baseline verification:** After cloning and inspecting baseline repos
   locally, update `baseline_attempts.csv` with confirmed run statuses.
