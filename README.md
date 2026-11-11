# Gemma-3 Bias Fine-Tuning

A UC Berkeley URAP research project studying **whether fine-tuning Gemma-3 changes racial bias in its responses—and whether those changes hold up outside the training benchmark.**

We use `google/gemma-3-12b-it`, a vision-language model, and compare the original model with five supervised fine-tuning experiments. The main question is simple: **can we reduce biased associations without making the model less useful or just teaching it to avoid certain words?**

## What we did

We started with a small, held-out image-and-word association test (IAT-style): the model sees a face and selects three words. We compare negative-word rates for Black and White faces. Then we check the same models on independent tasks: stereotype-related questions (DecodingTrust), text generation (BOLD), image comparisons and position bias (VisBias), and facial-expression recognition (FER2013).

| Experiment | What changed | Why |
| --- | --- | --- |
| **Base** | Original Gemma-3-12B-IT | Establish a reference |
| **V1** | Matched FairFace images with expression-derived answers | Test a first fine-tuning approach |
| **V2** | Balanced positive/negative word targets | Avoid pushing all responses toward negative words |
| **V3** | Mixed IAT, stereotype, description and comparison tasks | See whether improvements transfer to other tasks |
| **V4** | Rebalanced response types | Improve robustness and useful answers |
| **V5** | Optimized task mixture, trained from the **fresh base model** | Keep the strengths of earlier versions without stacking V4 weights |

**Important V5 detail:** V5 reuses some V4 *data design*, but starts from the original Gemma model. It does **not** load the V4 LoRA adapter. Its dataset has 2,523 training rows and 700 development rows; requested task proportions are 60% IAT, 15% DecodingTrust, and 25% comparison tasks. See [V5 configuration](docs/v5_configuration.md).

## What we learned

Early results show why measuring only the IAT gap is insufficient. V2 reduced that gap, but performance on some other tasks got worse. The later versions were designed to address those trade-offs.

The November 3 research presentation reports that V5 reduced the overall negative-word rate in the IAT comparison from **68.9% to 19.5%**, with promising results on some external tests. There are still open questions about BOLD sentiment, differences across groups, and sensitivity to how a question is phrased. Those numbers describe a particular experiment, not a universal fairness score.

[View the research slides](https://docs.google.com/presentation/d/1bEsHXiTRT3-JSj83314_HKY6b1U_CG4qQvUqaHernfk/edit).

## Where to find things

| Location | Contents |
| --- | --- |
| [`notebooks/`](notebooks/) | Original Base–V2 notebooks already in this repository |
| [`scripts/`](scripts/) | Data preparation, statistical testing and plotting |
| [`docs/v3_v5_handoff.md`](docs/v3_v5_handoff.md) | V3–V5 datasets, adapters, outputs and handoff steps |
| [`docs/v5_configuration.md`](docs/v5_configuration.md) | V5 training mixture, software versions and evaluation settings |
| [`docs/training_data.md`](docs/training_data.md) | Earlier dataset construction |
| [`docs/external_benchmarks.md`](docs/external_benchmarks.md) | External benchmark methodology |
| [`results/`](results/) | Published lightweight metrics |

**The V3–V5 datasets, saved adapters and full output folders are in the team's Google Drive under `IAT/`.** They are catalogued in the handoff document. We keep large weights and face-image datasets outside this public GitHub repository.

## How to reproduce an experiment

1. Open [the handoff guide](docs/v3_v5_handoff.md) and choose V3, V4 or V5.
2. Get that version's **train/dev CSVs** and **saved LoRA adapter** from `IAT/sft_data/` and `IAT/models/` in Drive.
3. Use the original Gemma-3-12B-IT model and the matching adapter to **evaluate first**, before spending GPU time retraining.
4. Use the same held-out prompts, image order and generation settings as the original run. For V5, compare against the saved results in `IAT/results/gemma/v5_v4_optimized_freshbase/`.
5. Compare negative-word rates **and** the Black–White gap, then check DecodingTrust, VisBias, BOLD and FER2013. Check the raw results before drawing conclusions.

The original IAT test uses 12 held-out images, 61 possible words and 50 generations per image. Since many generations come from the same image, statistical tests should account for that rather than treating all 600 responses as independent.

## For new team members

Start with this README, then [the V3–V5 handoff](docs/v3_v5_handoff.md). The goal is to understand **what changed between versions, where the exact data and model live, and how to check whether a reported improvement is real**.

The historical notebooks are in GitHub; the newer experiment artifacts are indexed in Drive. The full V3–V5 runnable notebook collection has not yet been mirrored into this repository, so use the original notebooks with the saved configurations when reproducing those versions.

## Data and credits

FairFace and other benchmark data have their own usage terms. We do not publish face-image copies, model weights or credentials here. This work is part of a UC Berkeley URAP research collaboration.
