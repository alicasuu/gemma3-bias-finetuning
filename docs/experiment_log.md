# Experiment Log

## Gemma-3 Baseline

**Model:** `google/gemma-3-12b-it`

Evaluation:
- 12 held-out IAT images
- 61-word vocabulary
- 3 words per output
- 50 generations per image
- 600 total generations
- temperature = 1.0

Observed baseline:
- Black negative-word rate: ~39.3%
- White negative-word rate: ~6.1%
- Black − White negative gap: ~33.2 percentage points
- Jensen–Shannon divergence: ~0.164

## SFT v1 — Expression-Derived Targets

Training data:
- FairFace matched Black/White pairs
- high-confidence `happy`, `sad`, `angry`
- train: 1,514 images
- development: 516 images
- IAT-12 fully held out

Fine-tuning:
- 4-bit QLoRA
- r = 16
- alpha = 32
- dropout = 0.05
- learning rate = 2e-4
- 1 epoch
- batch size = 1
- gradient accumulation = 8

Observed v1:
- Black negative-word rate: ~65.3%
- White negative-word rate: ~71.0%
- Black − White negative gap: ~-5.7 percentage points
- Jensen–Shannon divergence: ~0.0129

Interpretation: V1 made Black and White distributions much more similar, but caused a strong global shift toward negative words. More race-consistent does not necessarily mean more neutral.

## SFT v2 — Valence-Controlled Targets

Research question: can the Black/White distribution gap be reduced without the global negative shift observed in v1?

Controlled comparison:
- same FairFace image set
- same base model
- same LoRA architecture
- same optimizer/training hyperparameters
- same IAT prompt
- same IAT-12 evaluation
- **change only the SFT target distribution**

V2 target rule: match the overall negative-word proportion in SFT targets to the baseline Gemma-3 global negative-word rate while preserving identical targets within every Black/White matched pair.

**Status:** in progress.

## Statistical testing

Do not treat all 600 generations as independent samples.

Primary unit of analysis: **image**.

Report:
- Black mean image-level negative rate
- White mean image-level negative rate
- Black − White effect
- exact two-sided permutation p-value
- bootstrap 95% confidence interval

Note: p-value/CI are inferential statistics; a formal statistical power analysis is a separate item and is not yet claimed here.
