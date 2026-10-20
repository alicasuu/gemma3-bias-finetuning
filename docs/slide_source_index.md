# Meeting-slide source index

This file maps the current **URAP 2026** meeting-slide pages to the exact GitHub notebook and lightweight result file behind each figure/table.

## Current Alica update slides

| Meeting slide page | Slide item | GitHub source notebook / doc | Result / metric file | Notes |
|---:|---|---|---|---|
| 3 | Baseline vs SFT V1 + LoRA vs SFT V2 + LoRA plots (regenerated) | `notebooks/01_gemma3_baseline.ipynb`, `notebooks/02_gemma3_sft_v1_expression.ipynb`, `notebooks/03_gemma3_sft_v2_valence_controlled.ipynb` | `results/metrics/gemma3_baseline_v1_v2_metrics.csv` | Same plotting template |
| 4 | IAT Black/White statistical significance tests | `notebooks/03_gemma3_sft_v2_valence_controlled.ipynb`; `scripts/statistical_testing.py` | `results/metrics/gemma3_baseline_v1_v2_image_level_stats.csv` | Should report difference-in-means / OLS plus permutation/randomization; image is the unit |
| 5 | DecodingTrust Base vs V2 figure | `notebooks/04_gemma3_decodingtrust_base_vs_v2.ipynb` | `results/metrics/decodingtrust_base_vs_v2_summary.csv` | Four demographic groups |
| 6 | DecodingTrust statistical significance | `notebooks/04_gemma3_decodingtrust_base_vs_v2.ipynb` | `results/metrics/decodingtrust_direct_change.csv` | Paired tuning-induced disparity change; notebook also contains Black-vs-White t-test / OLS |
| 7 | BOLD Toxicity | `notebooks/05_gemma3_bold_base_vs_v2.ipynb` | `results/metrics/bold_base_vs_v2_summary.csv` | Race-category toxicity |
| 8 | BOLD Sentiment | `notebooks/05_gemma3_bold_base_vs_v2.ipynb` | `results/metrics/bold_base_vs_v2_summary.csv` | Race-category sentiment |
| 9 | BOLD Regard | `notebooks/05_gemma3_bold_base_vs_v2.ipynb` | `results/metrics/bold_base_vs_v2_summary.csv` | Race-category regard |
| 10 | BOLD within-model African American vs European American tests | `notebooks/05_gemma3_bold_base_vs_v2.ipynb` | notebook output | Welch tests within Base and V2 |
| 11 | BOLD tuning-induced gap-change tests | `notebooks/05_gemma3_bold_base_vs_v2.ipynb` | `results/metrics/bold_direct_change.csv` | OLS interaction / direct Base-to-V2 change |
| 12 | VisBias Income | `notebooks/06_gemma3_visbias_base_vs_v2.ipynb` | `results/metrics/visbias_base_vs_v2_summary.csv` | 140 strict matched Black/White pairs; reversed order |
| 13 | VisBias Education | `notebooks/06_gemma3_visbias_base_vs_v2.ipynb` | `results/metrics/visbias_base_vs_v2_summary.csv` | 140 strict matched Black/White pairs; reversed order |
| 14 | VisBias statistical significance | `notebooks/06_gemma3_visbias_base_vs_v2.ipynb` | `results/metrics/visbias_direct_change.csv` | Paired permutation + OLS; report order consistency separately |

## Cross-benchmark summary

| Slide item | GitHub source | Result |
|---|---|---|
| IAT + DecodingTrust + BOLD + VisBias summary | `docs/external_benchmarks.md` | `results/metrics/cross_benchmark_summary.csv` |

## Documentation

| Topic | GitHub file |
|---|---|
| Project overview | `README.md` |
| Training-data construction | `docs/training_data.md` |
| Full experiment history | `docs/experiment_log.md` |
| External benchmark summary | `docs/external_benchmarks.md` |
| Statistical-test implementation | `scripts/statistical_testing.py` |
| V2 target helper | `scripts/v2_targets.py` |

## Slide citation format

Put a small source line under each figure/table. Examples:

`Source: notebooks/04_gemma3_decodingtrust_base_vs_v2.ipynb; results/metrics/decodingtrust_base_vs_v2_summary.csv`

`Source: notebooks/06_gemma3_visbias_base_vs_v2.ipynb; results/metrics/visbias_direct_change.csv`

For the summary slide:

`Source: docs/external_benchmarks.md; results/metrics/cross_benchmark_summary.csv`

Keep the plotting grammar consistent where the metric allows: wide figure, Base in blue, V2 in orange, consistent labels.
