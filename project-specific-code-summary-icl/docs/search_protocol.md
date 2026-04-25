# Search Protocol

## Literature Search Strategy

### Search Engine and Tool
- **Google Scholar** via **Publish or Perish** software

### Time Period
- Primarily papers published since **2015**
- No hard cutoff; older foundational papers included if highly cited

### Search Queries

| ID | Query String | Scope |
|----|-------------|-------|
| S1 | "code summarization" OR "source code summarization" OR "code comment generation" OR "code documentation generation" | Broad |
| S2 | "project-specific code summarization" | Refined |
| S3 | "few-shot code summarization" | Refined |
| S4 | "code summarization in-context learning" | Refined |
| S5 | "project context code summarization llm" | Refined |
| S6 | "code summarization reliability" | Refined |
| S7 | "code summarization evaluation" | Refined |

### Venue Focus

**Top SE venues:**
- ICSE (International Conference on Software Engineering)
- FSE / ESEC/FSE (Foundations of Software Engineering)
- ASE (Automated Software Engineering)
- MSR (Mining Software Repositories)
- EMSE (Empirical Software Engineering)
- TSE (IEEE Transactions on Software Engineering)
- TOSEM (ACM Transactions on Software Engineering and Methodology)

**Related NLP/ML venues:**
- ACL, EMNLP, NAACL (computational linguistics)
- NeurIPS, ICML, ICLR (machine learning)
- AAAI (artificial intelligence)

### Ranking and Selection Process

1. **Collect top 100 papers** by citation count from the combined search results.
2. **Sort by citation count** in descending order.
3. **Knee analysis**: Apply the maximum perpendicular distance method to the
   citation-count curve to find the "knee" — the point of diminishing returns.
4. **Knee result**: Rank 22, citation threshold = 167.
5. **Above-the-knee set**: 22 papers with ≥ 167 citations.
6. **Thematic coding**: Classify the 22 above-the-knee papers into four themes:
   - P = Project-Specific Context
   - I = In-Context Learning and Prompting
   - M = Code Summarization Methods
   - E = Evaluation and Reliability

### Thematic Group Sizes

| Theme | Count |
|-------|-------|
| P (Project-Specific Context) | 6 |
| I (In-Context Learning and Prompting) | 4 |
| M (Code Summarization Methods) | 19 |
| E (Evaluation and Reliability) | 6 |

### Research Gap Identification

The full intersection P ∩ I ∩ M ∩ E = **0**.

No existing paper in the above-the-knee set addresses all four themes
simultaneously — project-specific context, in-context learning, code
summarization methods, and evaluation/reliability. This zero-overlap
intersection defines the research gap that our study addresses.

### Data Files

- `data/search_strings.csv` — Search query definitions
- `data/citation_counts_top100.csv` — Full 100-paper citation list
- `data/above_knee_papers.csv` — 22 above-the-knee papers
- `data/thematic_classification.csv` — Binary theme coding for 22 papers
- `data/venn_counts.csv` — Disjoint Venn region counts
