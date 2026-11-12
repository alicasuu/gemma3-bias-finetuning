# November 11, 2026 URAP wrap-up — Alica (5-slide speaking guide)

This is a short walkthrough of the **five actual Alica slides at current slide numbers 7–11** in [the shared 453-slide URAP deck](https://docs.google.com/presentation/d/1bEsHXiTRT3-JSj83314_HKY6b1U_CG4qQvUqaHernfk/edit), reviewed on November 11, 2026. It is designed for a ~3-minute team update and technical handoff. This document does **not** modify the Google Slides presentation.

## P1 / deck slide 7 — V5: IAT Prompt Variations

[Open source slide](https://docs.google.com/presentation/d/1bEsHXiTRT3-JSj83314_HKY6b1U_CG4qQvUqaHernfk/edit#slide=id.h537b1346fea3f701_0_0) · [Full literal four prompts](v5_iat_prompt_variants.md) · [V5 prompt summary](../results/v5/iat_4prompts_summary_stats.csv)

**What the slide actually shows:** a table of four prompt variants (Original, Paraphrased, Image-grounded, Format-focused), each with the change in instructions and a sample of its *actual prompt wording*. The slide abbreviates the identical 61-word vocabulary as `[61-word list]`; use [the verbatim templates](v5_iat_prompt_variants.md) for reproduction.

**Speaker script:**

> This first slide is a quick follow-up from last week. For V5, I tested four versions of our IAT prompt to see how much the results depended on wording. We kept the same 12 held-out face images and the same 61-word list, with 50 generations for each image and prompt. The original version used our standard instruction. Paraphrased changed the wording and required three different words. Image-grounded told the model to rely on visible information, rather than guessing personality or social status. Format-focused made the output format more strict. I documented all four exact prompts in GitHub, so the team can reproduce these conditions.

**Optional follow-up if asked about significance:** None of the four Black–White negative-word gaps reached statistical significance after Holm correction in the V5 slide results; this does not establish that the model has no bias. The image-grounded condition had raw `p = 0.026` and Holm-adjusted `p = 0.104`.

## P2 / deck slide 8 — GitHub Repository Structure

[Open source slide](https://docs.google.com/presentation/d/1bEsHXiTRT3-JSj83314_HKY6b1U_CG4qQvUqaHernfk/edit#slide=id.h6a3a099d1b2fca31_0_1) · [Repository homepage](https://github.com/alicasuu/gemma3-bias-finetuning)

**What the slide actually shows:** a text tree with `README.md`, `datasets/`, `notebooks/`, `configs/`, `results/`, `scripts/`, `docs/`, and `requirements.txt`.

**Speaker script:**

> This week, I also organized my work from V1 through V5 into one GitHub repository, so other people can pick up the project. The datasets folder contains the training and evaluation tables, notebooks has the model training and testing code, and configs keeps the LoRA settings. Results has the saved outputs, statistical tests and plots. Scripts contains the supporting data checks and analysis code, while docs records the experiment history and instructions. The README gives the overview, and requirements lists the Python dependencies. The goal is to make the inputs, code, and outputs easy to find for each version.

**One concrete example per section:** [README](../README.md), [V5 train CSV](../datasets/v5/train.csv), [V5 training notebook](../notebooks/v5/V5_Optimized_FreshBase_Colab.ipynb), [V5 config](../configs/v5_config.json), [V5 IAT results](../results/v5/iat_4prompts_summary_stats.csv), [CPU checks](../scripts/check_reproducibility.py), [handoff doc](v3_v5_handoff.md), [dependencies](../requirements.txt).

## P3 / deck slide 9 — README: Where to Start

[Open source slide](https://docs.google.com/presentation/d/1bEsHXiTRT3-JSj83314_HKY6b1U_CG4qQvUqaHernfk/edit#slide=id.h6a3a099d1b2fca31_0_26) · [README](../README.md)

**What the screenshot actually shows:** the top of the repo README, including the research question (*Can we make a vision-language model less biased without making it worse at other tasks?*), the IAT-style test explanation, benchmark names, and the start of the experiment-version section.

**Speaker script:**

> For anyone new to the project, I would start with the README. It explains the main research question and how our IAT-style test works: the model sees a face and chooses three words, and we compare the negative-word rates across groups. It also introduces the other benchmarks, like DecodingTrust, VisBias, BOLD, and FER2013, so people understand why we evaluate more than one metric. Below this section, the README summarizes what changed from the base model through V5 and how to get started.

**Concrete action for a new teammate:** clone the repo and run `python scripts/check_reproducibility.py`. That is a *CPU-only data/split check*; it is not a complete GPU reproduction.

## P4 / deck slide 10 — Notebooks: How to Reproduce

[Open source slide](https://docs.google.com/presentation/d/1bEsHXiTRT3-JSj83314_HKY6b1U_CG4qQvUqaHernfk/edit#slide=id.h6a3a099d1b2fca31_0_34) · [Notebook directory](../notebooks/) · [V5 train notebook](../notebooks/v5/V5_Optimized_FreshBase_Colab.ipynb) · [V5 no-retraining validation](../notebooks/v5/V5_Final_Validation_No_Retrain.ipynb)

**What the screenshot actually shows:** the GitHub `notebooks/` directory listing, including numbered early-version notebooks and `v3/`, `v4/`, and `v5/` subfolders.

**Speaker script:**

> Next is the notebooks folder. I kept the original Colab code organized by experiment version. You can see the earlier baseline and V1/V2 notebooks here, and the separate V3, V4, and V5 folders. For example, someone who wants to reproduce V5 can open the optimized fresh-base training notebook to see how the model was fine-tuned, or open the V5 validation notebook to evaluate an existing checkpoint without retraining. V5 starts from the original Gemma-3 base rather than continuing the V4 adapter. The larger model weights and image datasets still need to be loaded from our shared Drive.

**Important limitation:** Three older Base/V2 benchmark notebooks (`04_gemma3_decodingtrust_base_vs_v2.ipynb`, `05_gemma3_bold_base_vs_v2.ipynb`, `06_gemma3_visbias_base_vs_v2.ipynb`) currently fail the GitHub Actions notebook-JSON check and should be restored from full originals before claiming the entire repository is CI-clean. This does not change the V5 notebook entry points above.

## P5 / deck slide 11 — Results & Docs: Where to Verify

[Open source slide](https://docs.google.com/presentation/d/1bEsHXiTRT3-JSj83314_HKY6b1U_CG4qQvUqaHernfk/edit#slide=id.h6a3a099d1b2fca31_0_40) · [Results directory](../results/) · [Handoff docs](v3_v5_handoff.md)

**What the screenshot actually shows:** the `results/` directory, with `derived/`, `historical/`, `metrics/`, `slides/alica_original/`, `v3/`, `v4/`, and `v5/`. The slide heading says Results & Docs, but the screenshot itself displays **Results**, not an open Docs page.

**Speaker script:**

> Finally, this is where people can check whether they reproduced the same results. In the results folder, historical has earlier experiments, and the V3, V4, and V5 folders keep the later outputs separate. We also have saved statistical summaries, derived plots, and the original figures used in my meeting slides. For example, the V5 folder includes the four-prompt IAT summary, so people can compare a new run against the reported results. For instructions and experimental details, the docs folder has the V3-to-V5 handoff guide and the exact V5 prompt text. That way, teammates can check both how something was run and what it produced.

**Concrete files to open:** [V5 four-prompt summary](../results/v5/iat_4prompts_summary_stats.csv), [V5 raw IAT](../results/v5/iat_4prompts_raw.csv), [34 archived pre-wrap-up slide figures](../results/slides/alica_original/), [V3–V5 reproduction guide](v3_v5_handoff.md), and [verbatim prompt definitions](v5_iat_prompt_variants.md).

## Closing, if useful

> That's the handoff I wanted to share. The code, configs, datasets, and saved results are linked by version, and the README and docs explain how to continue. A full GPU rerun still requires access to the team's saved adapters and original image datasets.

## Reproduction constraints and attribution

- **V3 and V4:** IAT, DecodingTrust and VisBias were evaluated; **BOLD was not run** for V3 or V4. BOLD results are available for Base/V2 and V5.
- **V5:** trained from a fresh Gemma-3-12B-IT base with a rebalanced task mixture, not from the V4 LoRA weights.
- **Artifacts:** stored CSVs and code are available in GitHub; the large adapter weights, FairFace photos, IAT face images, and FER2013 images are controlled separately in Drive/original datasets.
- **Checks:** `scripts/check_reproducibility.py` validates row counts and held-out topic separation without a GPU. GitHub Actions additionally validates notebooks and is currently failing for the three malformed historical notebooks mentioned above. Full end-to-end GPU training/evaluation was not rerun during this repository handoff.
- **Figures:** the 34 images in `results/slides/alica_original/` were archived from the prior 446-page slide export. Three *new screenshots of GitHub pages* now appear on slides 9–11 of the 453-page deck; those are a documentation walkthrough, not experimental plots.
