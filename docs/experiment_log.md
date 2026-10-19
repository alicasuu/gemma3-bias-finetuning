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

**Status:** completed.

**Observed v2**
- Black negative-word rate: ~16.9%
- White negative-word rate: ~15.8%
- Black − White negative gap: ~1.1 percentage points
- Absolute negative gap: ~1.1 percentage points
- Overall negative-word rate: ~16.3%
- Jensen–Shannon divergence: ~0.0191
- Valid generations: 600 / 600

**Image-level statistical test**
- Exact permutation p-value: ~0.342
- Bootstrap 95% CI for Black − White gap: [-0.0067, 0.0300]

**Interpretation**

V2 reduced the absolute Black/White negative-word gap from ~33.2 pp at baseline and ~5.7 pp in V1 to ~1.1 pp, while avoiding V1's strong global negative shift. The overall negative rate in V2 (~16.3%) was below the baseline rate (~22.7%) and far below V1 (~68.2%). The full 61-word Black/White distributions remained close (JS divergence ~0.0191).

The image-level p-value and confidence interval do not provide evidence of a detectable Black/White negative-rate difference in this 12-image evaluation, but the small number of independent images limits inferential power.

## Statistical testing

Do not treat all 600 generations as independent samples.

Primary unit of analysis: **image**.

Report:
- Black mean image-level negative rate
- White mean image-level negative rate
- Black − White effect
- Welch difference-in-means t-test
- OLS race coefficient with HC2 robust standard error and 95% CI
- exact two-sided permutation/randomization p-value
- bootstrap 95% confidence interval

Note: p-value/CI are inferential statistics; a formal statistical power analysis is a separate item and is not yet claimed here.
