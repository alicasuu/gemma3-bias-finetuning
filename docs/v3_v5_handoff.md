# V3–V5: How to reproduce the experiments

This page is a handoff for anyone continuing the UC Berkeley URAP Gemma-3 project. **All V1–V5 train/dev CSVs, the original V3/V4/V5 Colab notebooks, and the saved evaluation CSVs are now in this repository.** The trained LoRA weights and image files remain in the project's Google Drive because they are large or subject to dataset usage terms.

## Pick a version

| Version | Notebook | Train CSV | Dev CSV | Saved adapter in Google Drive |
| --- | --- | --- | --- | --- |
| **V3** | [V3_MULTITASK_COMPLETE](../notebooks/v3/V3_MULTITASK_COMPLETE.ipynb) | [V3 train](../datasets/v3/train.csv) | [V3 dev](../datasets/v3/dev_iat.csv) | `IAT/models/gemma3-12b-fairface-sft-lora-v3-multitask/` |
| **V4** | [V4_MULTITASK_BALANCED_RESPONSE](../notebooks/v4/V4_MULTITASK_BALANCED_RESPONSE.ipynb) | [V4 train](../datasets/v4/train.csv) | [V4 dev](../datasets/v4/dev_iat.csv) | `IAT/models/gemma3-12b-fairface-sft-lora-v4-balanced-response/` |
| **V5** | [V5 optimized fresh-base](../notebooks/v5/V5_Optimized_FreshBase_Colab.ipynb) | [V5 train](../datasets/v5/train.csv) | [V5 dev](../datasets/v5/dev.csv) | `IAT/models/gemma3-12b-v5-v4-optimized-freshbase/` |

Direct links for team members with Drive access: [V3 adapter](https://drive.google.com/drive/folders/1NNufGW5hQiMiUxey08Ooo5JhK9svSPPS), [V4 adapter](https://drive.google.com/drive/folders/1hAucQKVskN5zvRwuFaczJJ6rr9JJfQ4T), [V5 adapter](https://drive.google.com/drive/folders/1wy61phnuvbjSBBcIZzwT4L4aCwIYlCyb). Access is controlled by the Drive owner.

The notebooks use original Colab/Drive paths, which may need to be adjusted for a new account or runtime. Open them **one at a time**. They are archived as originally authored, except that saved execution outputs were cleared before upload.

**V5 starts from the original Gemma-3-12B-IT weights.** It uses V4-informed training data but **does not continue training the V4 adapter**. Check [V5's recorded configuration](v5_configuration.md) and [the saved JSON](../configs/v5_config.json).

## Dataset sizes

| Version | Training rows | Development rows | IAT train | Comparison train | DecodingTrust train |
| --- | ---: | ---: | ---: | ---: | ---: |
| V1 | 1,514 | 516 | — | — | — |
| V2 | 1,514 | 516 | — | — | — |
| V3 | 3,028 | 516 | 1,514 | 757 | 757 |
| V4 | 3,364 | 516 | 1,514 | 1,177 | 673 |
| V5 | 2,523 | 700 | 1,514 | 632 | 377 |

V1 and V2 use a different file schema, so the task columns above only apply to V3 onward.

V3/V4 have separate [DecodingTrust train/held-out topic lists](../datasets/v3/); V5 has a [reference-only held-out list](../datasets/v5/decodingtrust_heldout_topics_REFERENCE_ONLY.csv). The checked topic labels in the V3/V4/V5 training CSVs have **no overlap** with their respective held-out topic lists.

## Where to find the evaluations

| Version | IAT | DecodingTrust | VisBias | BOLD |
| --- | --- | --- | --- | --- |
| Base / V2 | [historical IAT](../results/historical/iat/) | [Base + V2 results](../results/historical/decodingtrust/) | [Base + V2 results](../results/historical/visbias/) | [Base + V2 results](../results/historical/bold/) |
| V3 | [IAT](../results/v3/iat/) | [held-out DT](../results/v3/decodingtrust/) | [image-order comparisons](../results/v3/) | Not run |
| V4 | [IAT](../results/v4/iat/) | [held-out DT](../results/v4/decodingtrust/) | [image-order comparisons](../results/v4/) | Not run |
| V5 | [IAT](../results/v5/iat_4prompts_raw.csv) | [DT](../results/v5/decodingtrust_heldout_raw.csv) | [VisBias](../results/v5/visbias_frozen_raw.csv) | [BOLD](../results/v5/bold_frozen_raw.csv) |

V5 also includes [FER2013 evaluation](../results/v5/fer2013_external_test_summary.csv). See the complete [evaluation-and-figures index](evaluation_coverage.md) for paired tests, p-values, and all plots.

The November 3 presentation reports a reduction in V5's overall IAT negative-word rate from 68.9% to 19.5% and external FER2013 accuracy of 92% in the presented comparison. Results should always be interpreted alongside model validity, prompt sensitivity, global word valence, BOLD sentiment and Black–White differences.

## First run: check the repository

```bash
git clone https://github.com/alicasuu/gemma3-bias-finetuning.git
cd gemma3-bias-finetuning
python scripts/check_reproducibility.py
```

This **CPU-only** check validates train/dev counts, V3–V5 task mixtures, topic-level held-out separation and the presence of key files. Installing all GPU packages is *not* necessary for this check.

## Reproduce a saved model result

1. **Choose the version** and download or mount its saved adapter under Google Drive `IAT/models/`. Use `google/gemma-3-12b-it` as the base model.
2. **Get the images** used in the relevant benchmark. The CSVs provide names and paths, not image pixel data. Image files live in the original licensed datasets or team Drive.
3. **Open the version-matched evaluation notebook.** For V5, use [this no-retraining validation notebook](../notebooks/08_gemma3_v5_validation.ipynb).
4. **Match the frozen prompts and generation settings** used in the original run, including image order, output format, sampling parameters, seed and prompt variation.
5. **Compare raw rows and summary statistics** with the saved results here. IAT uses 12 historical images with 50 generations per image; the image, not each generated word, is the relevant independent unit.
6. If necessary, run the training notebook using the exact train/dev data and record the environment, selected adapter checkpoint, and seed.

The [model adapter metadata](../configs/adapters/) records V3/V4/V5 LoRA/processor settings. For V5, the original manifest in [results/v5/manifest.json](../results/v5/manifest.json) also records the task mixture and package versions.

## Figures and presentation

The team's [URAP 2026 slide deck](https://docs.google.com/presentation/d/1bEsHXiTRT3-JSj83314_HKY6b1U_CG4qQvUqaHernfk/edit) is the source presentation. We added the eleven exported **V5 charts** from `IAT/URAP_V5_Charts_11-03_Download/` to [results/v5/figures/](../results/v5/figures/), plus separate IAT, DecodingTrust and V4 figures. For the names and topics of each figure, see [evaluation_coverage.md](evaluation_coverage.md).

All 34 PNGs embedded on the 48 Alica-owned slides are individually committed in [original images](../results/slides/alica_original/), with checksums in the [manifest](../results/slides/alica_original/manifest.csv). The full presentation also contains other team members' figures; those are not all mirrored into this repo. See the [Alica slide-and-figure index](alica_slide_figures.md) for all 48 pages labeled with her name across the 446-page deck. V3/V4 BOLD runs were not performed; BOLD coverage is Base/V2 and V5.

## What still needs a runtime or team access

- **Weights and benchmark images:** final adapter files (about 262 MB each), checkpoint folders, FairFace/VisBias/IAT faces and external FER2013 images remain in Drive or their original datasets. Regular GitHub files cannot store a single 262 MB adapter; use Git LFS or the controlled project Drive.
- **V3/V4 BOLD:** these versions were not evaluated on BOLD. Their external benchmarks were DecodingTrust and VisBias, alongside IAT.
- **End-to-end repeatability:** the code and committed CSVs have been checked for syntax, counts and topic split, but **full GPU training/evaluation has not been rerun during this handoff**. A new researcher should compare their actual outputs against the archived results.

For any third-party images or benchmark datasets, follow the original usage terms before further sharing.

## Exact V5 IAT prompt reproduction

For the Holm-corrected four-condition plot on the November 3 Alica slide (current slide 17), reproduce the prompts verbatim using [the four exact prompt templates and ordered word list](v5_iat_prompt_variants.md). The deck's speaker notes for that slide also contain the complete prompts.
