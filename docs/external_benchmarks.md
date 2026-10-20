# External benchmark evaluation

This document summarizes Base vs. V2 LoRA evaluation beyond the held-out IAT-12 benchmark.

## Models

- Base: `google/gemma-3-12b-it`
- Tuned: the same base model plus the saved valence-controlled V2 LoRA adapter.

The V2 adapter is loaded at inference time with PEFT; it is not retrained inside the external-benchmark notebooks.

## DecodingTrust

Notebook: `notebooks/04_gemma3_decodingtrust_base_vs_v2.ipynb`

Race-focused stereotype evaluation uses matched prompts across:
- Black people
- Asians
- White people
- Latin Americans

and the benign, untargeted, and targeted regimes.

Observed overall behavior:
- Base stereotype agreement rate: 0.072917
- V2 stereotype agreement rate: 0.546875
- Base no-response rate: 0.619792
- V2 no-response rate: 0.125000

The overall four-group disparity changed from 0.166667 to 0.187500; paired permutation p = 0.921654.

Interpretation: V2's IAT improvement did not generalize to DecodingTrust. The tuned model answered more often and agreed with stereotype statements much more often. The overall race-group disparity change was not statistically detectable.

## BOLD

Notebook: `notebooks/05_gemma3_bold_base_vs_v2.ipynb`

Race-focused BOLD uses 100 prompts from each of four categories:
- African Americans
- Asian Americans
- European Americans
- Hispanic and Latino Americans

Metrics:
- Detoxify toxicity
- VADER sentiment
- regard classifier score

Observed overall behavior:
- toxicity: 0.0075 Base -> 0.0025 V2
- mean sentiment: 0.1675 Base -> 0.2250 V2
- mean regard: 0.3775 Base -> 0.4275 V2

Direct race-category disparity changes were not statistically detectable:
- toxicity: change 0.00, p = 1.000000
- sentiment: change +0.08, p = 0.307835
- regard: change -0.09, p = 0.329534

Interpretation: BOLD is mixed/mostly neutral. V2 did not show a statistically detectable race-category disparity change.

## VisBias

Notebook: `notebooks/06_gemma3_visbias_base_vs_v2.ipynb`

The repository contained 140 strict matched Black/White pairs under the Elias-style contract:
same occupation, gender, and source index.

Each pair is evaluated on:
- income
- education

and image order is reversed for each comparison unit.

This produces 560 comparison calls/model.

Observed aggregate behavior:
- V2 Black selection rate = 0.50 for both income and education
- V2 White selection rate = 0.50 for both
- V2 cannot-determine rate = 0 for both
- V2 order consistency = 0 for both

Direct disparity changes:
- income: -0.023529, paired permutation p = 0.705565
- education: -0.090909, paired permutation p = 0.244488

Interpretation: aggregate Black/White selection became more balanced, but 0% order consistency strongly suggests position sensitivity. This should not be described as robust debiasing.

## Cross-benchmark conclusion

V2 strongly reduced the original IAT Black/White negative-rate gap, but the effect did not generalize consistently:

- IAT-12: large descriptive reduction in the Black/White negative-rate gap
- DecodingTrust: stereotype agreement increased substantially
- BOLD: no statistically detectable race-category disparity change
- VisBias: aggregate balance improved, but behavior became order-sensitive

The main conclusion is therefore benchmark-dependent improvement with behavioral trade-offs, not universal debiasing.

## Lightweight result files

See `results/metrics/`:

- `cross_benchmark_summary.csv`
- `decodingtrust_base_vs_v2_summary.csv`
- `decodingtrust_direct_change.csv`
- `bold_base_vs_v2_summary.csv`
- `bold_direct_change.csv`
- `visbias_base_vs_v2_summary.csv`
- `visbias_direct_change.csv`

Raw model responses, image datasets, model weights, and adapter weights are intentionally excluded from the public repository.
