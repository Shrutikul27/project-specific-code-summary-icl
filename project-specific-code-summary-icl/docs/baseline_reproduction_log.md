# Baseline Reproduction Log

Detailed outcomes from attempting to reproduce the three referenced baseline
systems. Our direct empirical baseline is **Generic Prompting**; these prior
systems are treated as reproducibility/reference baselines.

---

## 1. Ahmed & Devanbu (2022) — Few-shot training LLMs for project-specific code-summarization

- **Paper:** https://arxiv.org/abs/2207.04237
- **Repository:** https://github.com/toufiqueparag/few_shot_code_summarization
- **Repository Found:** Yes
- **Runs Successfully:** No (unmodified)
- **Feasible Within Semester:** Maybe, if patched
- **Baseline Results Available:** Yes (paper baselines)

### Observed Outcome

Repo cloned, environment worked, script reached API call, then **failed
because the original model `code-davinci-002` is deprecated**. The OpenAI
Codex API endpoint used in the original code is no longer available, so
the few-shot prompting pipeline cannot be executed as-is.

### Decision

Keep as **primary conceptual baseline and failed reproduction case**. The
paper's reported results are referenced but could not be independently
verified through re-execution.

---

## 2. Ahmad et al. (2020) — NeuralCodeSum / A Transformer-based Approach for Source Code Summarization

- **Repository:** https://github.com/wasiahmad/NeuralCodeSum
- **Repository Found:** Yes
- **Runs Successfully:** No (end-to-end)
- **Feasible Within Semester:** Maybe
- **Baseline Results Available:** Yes (paper baselines)

### Observed Outcome

Repo cloned, dependencies repaired, training/testing pipeline launched, then
**failed because required Java dataset files were missing** and the bundled
download path did not produce a valid archive. The CodeSearchNet dataset files
expected by the training scripts were not obtainable through the provided URLs.

### Decision

Keep as **secondary supervised baseline and failed reproduction case**. The
paper's architecture and reported BLEU scores are referenced but could not be
independently reproduced without the original dataset.

---

## 3. Yun et al. (2024) — P-CodeSum: Project-specific code summarization with in-context learning

- **Repository:** https://github.com/Linshuhuai/P-CodeSum
- **Repository Found:** Yes
- **Runs Successfully:** Partial
- **Feasible Within Semester:** Likely yes
- **Baseline Results Available:** Yes

### Observed Outcome

Repo installed successfully and scripts launched, but **default `train.sh` /
`evaluate.sh` point to nonexistent `../data/h2o-3/train_500_10`**; the repo
actually contains `train_500_5` and `train_1000_5`. Log files were created
successfully, indicating the pipeline is functional with the correct data paths.

### Decision

Keep as **most promising runnable baseline**. With minor path corrections,
this baseline appears reproducible. This is the closest prior work to our
own study's approach (project-specific ICL for code summarization).

---

## Summary Table

| System | Repo Found | Runs | Feasible | Decision |
|--------|-----------|------|----------|----------|
| Ahmed & Devanbu 2022 | Yes | No (API deprecated) | Maybe | Conceptual baseline; failed repro |
| Ahmad et al. 2020 (NeuralCodeSum) | Yes | No (missing data) | Maybe | Supervised baseline; failed repro |
| Yun et al. 2024 (P-CodeSum) | Yes | Partial | Likely yes | Most promising runnable baseline |
