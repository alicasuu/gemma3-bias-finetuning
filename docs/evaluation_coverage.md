# Evaluation coverage and figure index

This page maps the evaluations actually saved in the repository. The datasets, original notebooks, and raw results were copied from the research Google Drive. **A version is marked as available only when its corresponding files were located.**

## Benchmark coverage

| Version | IAT | DecodingTrust | VisBias | BOLD | FER2013 |
| --- | --- | --- | --- | --- | --- |
| Base / V2 | [historical IAT](../results/historical/iat/) | [raw + scored](../results/historical/decodingtrust/) | [raw + scored](../results/historical/visbias/) | [raw + scored](../results/historical/bold/) | — |
| V3 | [IAT outputs](../results/v3/iat/) | [held-out outputs](../results/v3/decodingtrust/) | [comparison results](../results/v3/) | Not run | — |
| V4 | [IAT outputs](../results/v4/iat/) | [held-out outputs](../results/v4/decodingtrust/) | [comparison results](../results/v4/) | Not run | — |
| V5 | [4-prompt IAT outputs](../results/v5/iat_4prompts_summary_stats.csv) | [held-out raw + summary](../results/v5/decodingtrust_heldout_raw.csv) | [frozen raw + summary](../results/v5/visbias_frozen_raw.csv) | [raw + scored](../results/v5/bold_frozen_raw.csv) | [external test results](../results/v5/fer2013_external_test_summary.csv) |

The V5 [validation notebook](../notebooks/08_gemma3_v5_validation.ipynb) includes benchmark evaluation code. V3/V4 training notebooks include the earlier evaluations, and Base/V2 benchmark notebooks live in [notebooks/](../notebooks/).

**Important distinction:** V5 has a saved BOLD evaluation and paired V5 vs Base/V2 analyses, but **V3 and V4 did not run BOLD** (confirmed by the researcher). Don't present the table as though they exist.

## Figures

See [the complete index of Alica's 48 slides](alica_slide_figures.md) for the matching source slide and its original or recreated figure. The Google Drive project contains a folder `IAT/URAP_V5_Charts_11-03_Download/`. We imported its **11 exported slide images** and the separate **V5 IAT word-distribution plot**:

The exported V5 charts are listed in the order saved in Drive:

| Figure | Topic |
| --- | --- |
| [Slide 01](../results/v5/figures/Slide_01.png) | V4 vs V5 training task composition |
| [Slide 02](../results/v5/figures/Slide_02.png) | IAT negative-word rates across model versions |
| [Slide 03](../results/v5/figures/Slide_03.png) | Paired V4–V5 IAT tests |
| [Slide 04](../results/v5/figures/Slide_04.png) | V5 IAT results under four prompt variants |
| [Slide 05](../results/v5/figures/Slide_05.png) | IAT prompt-significance tests |
| [Slide 06](../results/v5/figures/Slide_06.png) | Output validity and word diversity |
| [Slide 07](../results/v5/figures/Slide_07.png) | V4 vs V5 DecodingTrust classifications |
| [Slide 08](../results/v5/figures/Slide_08.png) | VisBias and external FER2013 |
| [Slide 09](../results/v5/figures/Slide_09.png) | BOLD sentiment and regard |
| [Slide 10](../results/v5/figures/Slide_10.png) | BOLD statistical comparisons |
| [Slide 11](../results/v5/figures/Slide_11.png) | Improvements and next steps |

- [V5 IAT word distribution](../results/v5/figures/V5_IAT_Word_Distribution_Original_Prompt.png)
- [V5 prompt variation chart](../results/v5/figures/iat_prompt_variations.png)
- [V5 DecodingTrust classification chart](../results/v5/figures/decodingtrust_classification.png)
- [V4 IAT word distribution](../results/v4/figures/iat_word_distribution.png)

The [URAP 2026 Google Slides deck](https://docs.google.com/presentation/d/1bEsHXiTRT3-JSj83314_HKY6b1U_CG4qQvUqaHernfk/edit) has many other slides and contributors. **These exported PNGs are not a claim that every figure from the entire slide deck has been copied.** Some figures are embedded only in the slide deck. Preserve that deck as the source for figures not yet exported separately.

## Handy files

- [V5 statistical results](../results/v5/iat_paired_changes_and_significance.csv) and [Holm correction](../results/v5/iat_prompts_holm_adjusted_p.csv)
- [V4 vs V5 DecodingTrust paired comparison](../results/v5/v4_vs_v5_paired_dt.csv)
- [V5 vs Base/V2 BOLD paired tests](../results/v5/bold_v5_vs_base_v2_paired_tests.csv)
- [Training configuration](../configs/v5_config.json)
- [V3/V4/V5 reproduction notes](v3_v5_handoff.md)

When reporting results, compare the exact same benchmark inputs and scoring protocol. This page indexes existing runs; it does not imply we reran them during the repository migration.
