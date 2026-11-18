# TextVQA validation: Gemma 3 Base vs V5

This folder contains the saved outputs from a **paired, no-retraining evaluation** of the original `google/gemma-3-12b-it` model and the V5 LoRA adapter on **all 5,000 questions** of TextVQA v0.5.1 validation (**3,166 distinct images**).

| Model | Official soft-answer accuracy |
| --- | ---: |
| Gemma 3 Base | 70.58% |
| Gemma 3 + V5 | 72.27% |
| V5 - Base | +1.69 percentage points |

The image-clustered paired bootstrap 95% confidence interval for the difference is **[+0.87, +2.51] percentage points**. The two-sided image-clustered sign-flip test gives **p = 0.000300** (5,000 bootstrap iterations, 10,000 sign-flip permutations). There were 404 improved, 284 worse, and 4,312 tied questions.

## Files

- `base_raw.csv` — 5,000 base-model predictions and per-question metadata.
- `v5_raw.csv` — 5,000 V5-adapter predictions on the same questions, in the same order.
- `summary_n5000.json` — saved accuracy, paired differences, uncertainty estimates, test statistics, and reference evaluator hash.
- `run_config.json` — saved model/adapter identifiers, dataset version, seed, prompt, inference settings, package versions, and dataset hashes.

## Reproduction

- [Colab notebook](../../notebooks/09_gemma3_textvqa_base_vs_v5.ipynb)
- [Evaluation runner](../../scripts/textvqa_compare.py)
- [CPU scoring/resume tests](../../tests/test_textvqa_compare.py)

The notebook pins the runner to commit `cb0a4b64d6c409cf16cf922eefbc3c32217a4d44`. The V5 adapter weights are **not** included in this repository and are required to rerun inference; their path and SHA-256 are recorded in `run_config.json`. The predictions and summary included here allow inspection of the completed run and verification of the scoring/statistics.

These are **validation-set** results, not hidden TextVQA test-set or leaderboard results. The result supports capability retention on this benchmark, not a claim of improved general intelligence or broad fairness.
