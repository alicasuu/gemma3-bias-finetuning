# Gemma-3 Bias Fine-Tuning

Research code for evaluating and refining `google/gemma-3-12b-it` on a race-associated 61-word IAT-style benchmark.

## Current focus

This project currently focuses only on **Gemma-3-12B-IT**.

Experimental sequence:

1. **Baseline** — evaluate the original Gemma-3-12B-IT model.
2. **SFT v1** — fine-tune with FairFace matched Black/White pairs using expression-derived 3-word targets.
3. **SFT v2** — keep the same images and QLoRA settings, but control the positive/negative target distribution to test whether the race gap can be reduced without causing a global valence shift.
4. **Statistical testing** — compare image-level Black vs. White negative-word rates using permutation testing and bootstrap confidence intervals.

## Training data

Training uses the **FairFace 4,000 matched release** used by the URAP project.

The v1 workflow:
- keeps only complete Black/White matched pairs;
- keeps high-confidence (`>= 0.80`) `happy`, `sad`, and `angry` expression labels;
- gives both members of each matched pair the exact same 3-word SFT target;
- uses the provided **train** split for SFT and **development** split for validation;
- leaves the FairFace test split untouched;
- keeps the original **12 IAT evaluation images fully held out** from training.

Current retained v1 data:
- **1,514 training images**
- **516 development images**

FairFace does not provide source-authored 3-word SFT answers. V1 targets are an experimental construction from the provided expression metadata, not human-verified emotion labels.

See [`docs/training_data.md`](docs/training_data.md).

## Model and fine-tuning

Base model:

```text
google/gemma-3-12b-it
```

Current QLoRA configuration:

| Setting | Value |
|---|---:|
| Quantization | 4-bit NF4 |
| LoRA rank | 16 |
| LoRA alpha | 32 |
| LoRA dropout | 0.05 |
| Learning rate | 2e-4 |
| Epochs | 1 |
| Train batch size | 1 |
| Gradient accumulation | 8 |
| Precision | BF16 |
| Optimizer | adamw_torch_fused |

LoRA targets:
`q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj`.

Training loss is applied only to the assistant's 3-word answer tokens; prompt and image tokens are masked.

## Evaluation

Held-out IAT-style benchmark:

- **12 images**
- **61-word vocabulary**
- exactly **3 output words**
- **50 generations per image**
- **600 generations total**
- temperature = **1.0**

The 12 benchmark images are never used for fine-tuning.

## Metrics

We report:

- Black negative-word rate
- White negative-word rate
- Black − White negative-rate gap
- absolute Black/White gap
- overall negative-word rate
- Jensen–Shannon divergence across the 61-word distributions
- vocabulary diversity
- valid output count
- image-level Welch difference-in-means t-test
- image-level OLS Black indicator coefficient with HC2 robust inference
- image-level exact permutation/randomization p-value
- bootstrap 95% confidence interval for the Black − White gap

### Statistical unit

The 600 generations are repeated outputs from only 12 images, so they are **not** treated as 600 independent samples. Statistical tests use the **image** as the primary unit: 6 Black images vs. 6 White images.

## Repository structure

```text
gemma3-bias-finetuning/
├── README.md
├── requirements.txt
├── .gitignore
├── docs/
│   ├── training_data.md
│   ├── experiment_log.md
│   └── slide_source_index.md
├── scripts/
│   └── v2_refinement_addon.py
├── notebooks/
│   ├── 01_gemma3_baseline.ipynb
│   ├── 02_gemma3_sft_v1_expression.ipynb
│   └── 03_gemma3_sft_v2_valence_controlled.ipynb
└── results/
    ├── README.md
    ├── metrics/
    └── figures/
```

## Reproducibility / data policy

This public repository intentionally does **not** contain FairFace images, IAT face images, model weights, LoRA adapter weights, Hugging Face tokens, or other credentials.

## Collaboration

Project code is maintained through GitHub so experiment changes are reviewable and reproducible.

Debbie's GitHub handle: `Debbieliang9`.
