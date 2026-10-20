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

Interpretation: V1 made Black and White distributions much more similar, but caused a strong global shift toward negative words.

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

Observed v2:
- Black negative-word rate: ~16.9%
- White negative-word rate: ~15.8%
- Black − White negative gap: ~1.1 percentage points
- overall negative-word rate: ~16.3%
- Jensen–Shannon divergence: ~0.0191
- valid generations: 600 / 600

Image-level inference:
- OLS HC2 p-value: ~0.283
- exact permutation p-value: ~0.342
- bootstrap 95% CI for Black − White gap: [-0.0067, 0.0300]

Interpretation: V2 reduced the descriptive Black/White IAT gap while avoiding V1's global negative shift. The 12-image sample remains small, so inferential power is limited.

## External validation — DecodingTrust

Notebook: `notebooks/04_gemma3_decodingtrust_base_vs_v2.ipynb`

Race-focused evaluation:
- 192 prompts/model
- four demographic groups
- benign, untargeted, targeted regimes

Observed overall:
- Base stereotype agreement: 0.072917
- V2 stereotype agreement: 0.546875
- Base no-response rate: 0.619792
- V2 no-response rate: 0.125000

Overall four-group disparity:
- Base: 0.166667
- V2: 0.187500
- change: +0.020833
- paired permutation p = 0.921654

Black vs White:
- Base gap: -0.083333, Welch p = 0.044261
- V2 gap: -0.187500, Welch p = 0.065847
- OLS tuning interaction: -0.104167, p = 0.119915

Interpretation: the IAT improvement did not generalize. V2 agreed with stereotype statements much more often, while the overall race-group disparity change was not statistically detectable.

## External validation — BOLD

Notebook: `notebooks/05_gemma3_bold_base_vs_v2.ipynb`

Balanced race-focused sample:
- 100 prompts/category
- 4 categories
- 400 prompts/model

Overall:
- toxicity: 0.0075 Base -> 0.0025 V2
- mean sentiment: 0.1675 Base -> 0.2250 V2
- mean regard: 0.3775 Base -> 0.4275 V2

Direct race-category disparity changes:
- toxicity: 0.00, p = 1.000000
- sentiment: +0.08, p = 0.307835
- regard: -0.09, p = 0.329534

Interpretation: BOLD is mixed/mostly neutral; no statistically detectable Base-to-V2 race-category disparity change was observed.

## External validation — VisBias

Notebook: `notebooks/06_gemma3_visbias_base_vs_v2.ipynb`

Strict matched-pair contract:
- same occupation
- same gender
- same source index
- Black/White pair

The available source repository yielded 140 strict matched pairs.
Each pair was tested on income and education with reversed image order, producing 560 comparison calls/model.

Observed V2:
- Black selection = 0.50 for income and education
- White selection = 0.50 for income and education
- cannot-determine = 0 for both
- order consistency = 0 for both

Direct disparity change:
- income: -0.023529, p = 0.705565
- education: -0.090909, p = 0.244488

OLS tuned coefficient:
- income: +0.055020, p = 0.204538
- education: +0.111039, p = 0.054063

Interpretation: aggregate selection looked balanced, but zero order consistency indicates severe position sensitivity. This is not robust evidence of debiasing.

## Cross-benchmark conclusion

V2 strongly improves the original IAT metric, but the effect does not generalize consistently:
- DecodingTrust shows a large increase in stereotype agreement.
- BOLD shows no statistically detectable race-category disparity change.
- VisBias aggregate balance is undermined by 0% order consistency.

The current evidence supports benchmark-dependent improvements with behavioral trade-offs rather than universal debiasing.

## Statistical testing

Do not treat repeated generations as independent when the underlying stimulus is shared.

Primary principles:
- preserve matched observations;
- report effect sizes and raw p-values;
- test the Base-to-V2 change directly when possible;
- report refusals, invalid outputs, and behavioral stability alongside bias metrics.
