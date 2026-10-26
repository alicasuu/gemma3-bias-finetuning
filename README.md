# Gemma-3 Bias Fine-Tuning

Research code for evaluating and refining `google/gemma-3-12b-it` on race-associated multimodal and text bias benchmarks.

## Current focus

This project currently focuses on **Gemma-3-12B-IT**.

Experimental sequence:

1. **Baseline** — evaluate the original Gemma-3-12B-IT model.
2. **SFT v1** — fine-tune with FairFace matched Black/White pairs using expression-derived 3-word targets.
3. **SFT v2** — keep the same images and QLoRA settings, but control the positive/negative target distribution to test whether the race gap can be reduced without causing a global valence shift.
4. **IAT statistical testing** — compare image-level Black vs. White negative-word rates using Welch t-tests, OLS, permutation inference, and confidence intervals.
5. **External validation** — compare the same Base and V2 models on DecodingTrust, BOLD, and VisBias.
6. **V3 multi-task pilot** — add more diverse debiasing tasks and test whether the IAT improvement generalizes, with DecodingTrust topics held out from training.

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

## IAT-12 evaluation

Held-out IAT-style benchmark:

- **12 images**
- **61-word vocabulary**
- exactly **3 output words**
- **50 generations per image**
- **600 generations total**
- temperature = **1.0**

The 12 benchmark images are never used for fine-tuning.

Observed Black − White negative-rate gaps:
- Baseline: ~33.2 percentage points
- V1: ~-5.7 percentage points
- V2: ~1.1 percentage points

V2 strongly reduced the original IAT gap without reproducing V1's large global negative shift.

## External benchmark validation

The same Base model and saved V2 LoRA adapter were evaluated on three external benchmarks.

### DecodingTrust

- 192 race-focused stereotype prompts/model
- Base overall stereotype agreement: **7.3%**
- V2 overall stereotype agreement: **54.7%**
- overall four-group disparity change p = **0.922**

V2 answered more often but agreed with stereotype statements much more often.

### BOLD

- 400 race-focused prompts/model
- toxicity: **0.75% -> 0.25%**
- mean sentiment: **0.1675 -> 0.2250**
- mean regard: **0.3775 -> 0.4275**
- no statistically detectable race-category disparity change on toxicity, sentiment, or regard

### VisBias

- 140 strict matched Black/White image pairs
- income + education comparisons
- reversed A/B image order
- 560 comparison calls/model

V2 produced 50/50 aggregate Black/White selection on both attributes, but **order consistency fell to 0%**, indicating strong position sensitivity rather than robust debiasing.

See [`docs/external_benchmarks.md`](docs/external_benchmarks.md).

## Current next experiment: V3 diverse-task supervision

The next pilot tests whether broader supervision improves cross-benchmark robustness.

Planned task mixture:
- IAT-style valence-controlled image association
- DecodingTrust-style stereotype rejection
- grounded neutral image description
- unsupported social-inference comparison with both A/B orders

DecodingTrust text supervision uses a deterministic **topic-level holdout** so final evaluation topics are not used for training.

See [`docs/v3_multitask_training_plan.md`](docs/v3_multitask_training_plan.md).

For the VisBias follow-up, the repository now includes:
- [`results/metrics/visbias_order_effect_summary.csv`](results/metrics/visbias_order_effect_summary.csv)
- [`scripts/plot_visbias_order_effect.py`](scripts/plot_visbias_order_effect.py)

## Main conclusion

V2 substantially improves the original IAT gap, but the debiasing effect does **not** generalize uniformly across external benchmarks and can introduce behavioral trade-offs.

## Metrics and statistical unit

For IAT we report:
- Black negative-word rate
- White negative-word rate
- Black − White negative-rate gap
- absolute Black/White gap
- overall negative-word rate
- Jensen–Shannon divergence
- vocabulary diversity
- valid output count
- image-level Welch t-test
- OLS race coefficient with robust inference
- exact permutation/randomization p-value
- bootstrap 95% confidence interval

The 600 IAT generations are repeated outputs from only 12 images, so they are **not** treated as 600 independent samples. Statistical tests use the **image** as the primary unit.

External benchmark notebooks additionally preserve matched prompts/images and directly test Base-to-V2 changes when possible.

## Repository structure

```text
gemma3-bias-finetuning/
├── README.md
├── requirements.txt
├── .gitignore
├── docs/
│   ├── training_data.md
│   ├── experiment_log.md
│   ├── external_benchmarks.md
│   ├── v3_multitask_training_plan.md
│   └── slide_source_index.md
├── scripts/
│   ├── statistical_testing.py
│   ├── v2_targets.py
│   ├── plot_visbias_order_effect.py
│   └── build_v3_decodingtrust_supervision.py
├── notebooks/
│   ├── 01_gemma3_baseline.ipynb
│   ├── 02_gemma3_sft_v1_expression.ipynb
│   ├── 03_gemma3_sft_v2_valence_controlled.ipynb
│   ├── 04_gemma3_decodingtrust_base_vs_v2.ipynb
│   ├── 05_gemma3_bold_base_vs_v2.ipynb
│   └── 06_gemma3_visbias_base_vs_v2.ipynb
└── results/
    ├── README.md
    └── metrics/
```

## Reproducibility / data policy

This public repository intentionally does **not** contain FairFace images, IAT face images, VisBias image copies, raw model weights, LoRA adapter weights, Hugging Face tokens, or other credentials. Raw generation files are kept out of Git when they are large; lightweight summary metrics and completed notebooks are committed.

## Collaboration

Project code is maintained through GitHub so experiment changes are reviewable and reproducible.

Debbie's GitHub handle: `Debbieliang9`.
