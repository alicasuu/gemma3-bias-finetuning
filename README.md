# Gemma-3 Bias Fine-Tuning

**Can we make a vision-language model less biased without making it worse at other tasks?**

This UC Berkeley URAP project studies that question using **Gemma-3-12B-IT**. We fine-tuned the model with LoRA/QLoRA, compared five training approaches, and tested whether changes carried over to new prompts and benchmarks.

## The idea

In our main IAT-style test, the model sees a face and chooses three words from a fixed list. We measure how often it chooses negative words for Black versus White faces.

A smaller gap is useful, but it can hide a problem: a model might simply stop using negative words altogether. That's why we also measure overall word choices and run independent tests:

- **IAT:** positive/negative word associations and prompt sensitivity
- **DecodingTrust:** stereotype-related responses
- **VisBias:** unsupported judgments from images, abstention and image-order effects
- **BOLD:** sentiment, regard and toxicity in generated text
- **FER2013:** recognition of facial expressions on an external dataset

## Experiment versions

| Version | What changed | Why |
| --- | --- | --- |
| **Base** | Original `google/gemma-3-12b-it` | Starting point |
| **V1** | Fine-tuned with matched FairFace images | First IAT experiment |
| **V2** | Controlled the balance of positive and negative target words | Reduce the global negative-word shift |
| **V3** | Added stereotype, description and comparison tasks | Test whether improvements generalize |
| **V4** | Rebalanced response types | Improve response quality and robustness |
| **V5** | Optimized the task mixture and trained from a **fresh base model** | Address V4's trade-offs; V4 adapter weights were not loaded |

In the November 3 evaluation, V5 reduced the overall IAT negative-word rate from **68.9% to 19.5%** in the reported comparison. It also showed encouraging DecodingTrust, VisBias and FER2013 results. BOLD sentiment and differences between groups still need more work. [Research presentation](https://docs.google.com/presentation/d/1bEsHXiTRT3-JSj83314_HKY6b1U_CG4qQvUqaHernfk/edit).

For a quick view of **which versions were actually run on each benchmark and which figures were exported**, see the [evaluation and figure index](docs/evaluation_coverage.md). The [Alica slide index](docs/alica_slide_figures.md) links **every slide credited to Alica** to its corresponding figures and data, including [all 34 exact embedded PNGs and their checksums](results/slides/alica_original/). **V3/V4 ran IAT, VisBias and DecodingTrust—not BOLD.**

## What's in this repository?

| Folder | Contents |
| --- | --- |
| [`datasets/`](datasets/) | Actual V1–V5 training and development CSVs, plus held-out topic lists |
| [`notebooks/`](notebooks/) | Original Colab training/evaluation code and earlier notebooks |
| [`configs/`](configs/) | V5 training config and V3–V5 LoRA adapter metadata |
| [`results/`](results/) | Raw responses, summary metrics, statistical tests and research figures; all [34 original Alica slide PNGs](results/slides/alica_original/) |
| [`scripts/`](scripts/) | Data checks, preparation, statistics and plots |
| [`docs/`](docs/) | Detailed training notes and reproduction guide |

### Main notebooks

| Experiment | Open this first |
| --- | --- |
| V1–V2 | [Earlier notebooks](notebooks/) and [archived originals](notebooks/archives/) |
| V3 | [V3 multitask training](notebooks/v3/V3_MULTITASK_COMPLETE.ipynb) |
| V4 | [V4 balanced-response training](notebooks/v4/V4_MULTITASK_BALANCED_RESPONSE.ipynb) |
| V5 training | [V5 optimized fresh-base notebook](notebooks/v5/V5_Optimized_FreshBase_Colab.ipynb) |
| V5 evaluation | [V5 final validation](notebooks/08_gemma3_v5_validation.ipynb) |

Other intermediate versions are kept in the respective notebook folders so the experiment history is easy to trace.


### November 11 wrap-up: where to click during the handoff

The current [five-slide Alica wrap-up](docs/weekly_wrapup_2026-11-11.md) walks through **V5's four exact IAT prompts**, the repository tree, the README, versioned Colab notebooks, and saved results / reproduction documentation. It includes a short speaking script and concrete links for each of the five slides. [Open the shared deck](https://docs.google.com/presentation/d/1bEsHXiTRT3-JSj83314_HKY6b1U_CG4qQvUqaHernfk/edit#slide=id.h537b1346fea3f701_0_0).

**Known CI limitation (as checked November 11):** the CPU dataset/split check passes, but GitHub Actions notebook-JSON validation fails on three truncated historical Base/V2 benchmark notebooks (`04_gemma3_decodingtrust_base_vs_v2.ipynb`, `05_gemma3_bold_base_vs_v2.ipynb`, `06_gemma3_visbias_base_vs_v2.ipynb`). Restore their full source notebooks before relying on every archived notebook. V3–V5 entrypoints are separate files; a clean GPU end-to-end rerun has not been verified.

## Getting started

```bash
git clone https://github.com/alicasuu/gemma3-bias-finetuning.git
cd gemma3-bias-finetuning
python scripts/check_reproducibility.py
```

The check validates CSV row counts, V3–V5 task mixes, held-out DecodingTrust topics and key files. **It uses the Python standard library and runs without a GPU.** To run model notebooks, install the GPU-compatible dependencies from `requirements.txt` in your Colab runtime.

To run a model experiment:

1. Choose a version and open its notebook in Google Colab (an A100-class GPU is recommended for 12B QLoRA training).
2. Mount the team's Google Drive and use the matching files in `IAT/`. The training CSVs are also available under [`datasets/`](datasets/).
3. Make sure the FairFace images and held-out IAT faces are available at the paths used by the notebook. **The CSVs contain image paths, not the image pixels.**
4. For evaluation, load the saved LoRA adapter from Drive and run the benchmark cells before deciding whether to retrain.
5. Compare against the checked-in [results](results/) using the same prompts, decoding settings and held-out inputs.

See the [**V3–V5 reproduction guide**](docs/v3_v5_handoff.md) for paths, training-set sizes, checkpoints, and where to find each output.

## Model files and data access

The small configs and CSVs are committed here. Large LoRA weights and checkpoints remain in the team's Google Drive under `IAT/models/`; each V3–V5 final adapter is about **262 MB**, and normal GitHub files are limited to **100 MiB**. Publishing weights through GitHub would require Git LFS.

FairFace images, the 12 IAT face images and external FER2013 images stay with their original datasets/Drive storage. Ask the research team for the required access and follow each dataset's terms.

## Research notes

The IAT experiment uses **12 held-out images, 61 possible words and 50 generations per image**. We analyze at the **image level** rather than treating repeated generations as independent participants. Compare both the Black–White gap and the overall negative-word rate.

This repo includes the experiment code and recorded outputs. Full GPU training and evaluation have **not been rerun from scratch** during this GitHub reorganization.

**For a new team member:** read this README, run the dataset check, then follow the [V3–V5 guide](docs/v3_v5_handoff.md).
