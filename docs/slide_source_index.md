# Meeting-slide source index

This file preserves the September 16, 2026 source-notebook mapping, now using the **current 453-page deck numbering** as of November 11, 2026. For all 52 Alica-owned pages (including the November 3 V5 results), use [the comprehensive Alica slide-to-figure index](alica_slide_figures.md). All 34 PNGs embedded on Alica's slides are available byte-for-byte in [results/slides/alica_original](../results/slides/alica_original/) with checksums.

## September 16 Alica slides — current page numbers (original archive names retain old numbers)

| Current slide page | Slide item | GitHub source notebook / doc | Result / metric file | Notes |
|---:|---|---|---|---|
| 86–88 | Baseline vs SFT V1 + LoRA vs SFT V2 + LoRA plots (regenerated) | `notebooks/01_gemma3_baseline.ipynb`, `notebooks/02_gemma3_sft_v1_expression.ipynb`, `notebooks/03_gemma3_sft_v2_valence_controlled.ipynb` | `results/metrics/gemma3_baseline_v1_v2_metrics.csv` | Same plotting template |
| 89 | IAT Black/White statistical significance tests | `notebooks/03_gemma3_sft_v2_valence_controlled.ipynb`; `scripts/statistical_testing.py` | `results/metrics/gemma3_baseline_v1_v2_image_level_stats.csv` | Should report difference-in-means / OLS plus permutation/randomization; image is the unit |
| 90 | DecodingTrust Base vs V2 figure | `notebooks/04_gemma3_decodingtrust_base_vs_v2.ipynb` | `results/metrics/decodingtrust_base_vs_v2_summary.csv` | Four demographic groups |
| 91 | DecodingTrust statistical significance | `notebooks/04_gemma3_decodingtrust_base_vs_v2.ipynb` | `results/metrics/decodingtrust_direct_change.csv` | Paired tuning-induced disparity change; notebook also contains Black-vs-White t-test / OLS |
| 92 | BOLD Toxicity | `notebooks/05_gemma3_bold_base_vs_v2.ipynb` | `results/metrics/bold_base_vs_v2_summary.csv` | Race-category toxicity |
| 93 | BOLD Sentiment | `notebooks/05_gemma3_bold_base_vs_v2.ipynb` | `results/metrics/bold_base_vs_v2_summary.csv` | Race-category sentiment |
| 94 | BOLD Regard | `notebooks/05_gemma3_bold_base_vs_v2.ipynb` | `results/metrics/bold_base_vs_v2_summary.csv` | Race-category regard |
| 95 | BOLD within-model African American vs European American tests | `notebooks/05_gemma3_bold_base_vs_v2.ipynb` | notebook output | Welch tests within Base and V2 |
| 96 | BOLD tuning-induced gap-change tests | `notebooks/05_gemma3_bold_base_vs_v2.ipynb` | `results/metrics/bold_direct_change.csv` | OLS interaction / direct Base-to-V2 change |
| 97 | VisBias Income | `notebooks/06_gemma3_visbias_base_vs_v2.ipynb` | `results/metrics/visbias_base_vs_v2_summary.csv` | 140 strict matched Black/White pairs; reversed order |
| 98 | VisBias Education | `notebooks/06_gemma3_visbias_base_vs_v2.ipynb` | `results/metrics/visbias_base_vs_v2_summary.csv` | 140 strict matched Black/White pairs; reversed order |
| 99 | VisBias statistical significance | `notebooks/06_gemma3_visbias_base_vs_v2.ipynb` | `results/metrics/visbias_direct_change.csv` | Paired permutation + OLS; report order consistency separately |

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

## Verified exact original images and prompt text

Use [Alica's complete 52-slide index](alica_slide_figures.md) for source-slide IDs, **all 34 original PNGs** (including both figures on formerly numbered slide 176 (current slide 183)), historic results and earlier derived SVGs. The files in [the original images directory](../results/slides/alica_original/) are the exact slide-embedded bytes, with a [SHA-256 manifest](../results/slides/alica_original/manifest.csv). The [four exact V5 IAT prompt templates](v5_iat_prompt_variants.md) are also preserved in the November 3 significance slide's speaker notes. **V3/V4 ran IAT, DecodingTrust and VisBias, not BOLD.**
