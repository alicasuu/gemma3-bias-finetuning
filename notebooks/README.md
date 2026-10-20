# Notebook workflow

Runnable experiment notebooks:

1. `01_gemma3_baseline.ipynb` — held-out IAT-12 baseline evaluation.
2. `02_gemma3_sft_v1_expression.ipynb` — FairFace SFT + LoRA with expression-derived targets.
3. `03_gemma3_sft_v2_valence_controlled.ipynb` — valence-controlled V2 experiment and IAT statistical testing.
4. `04_gemma3_decodingtrust_base_vs_v2.ipynb` — race-focused DecodingTrust Base vs V2 evaluation.
5. `05_gemma3_bold_base_vs_v2.ipynb` — race-focused BOLD Base vs V2 evaluation.
6. `06_gemma3_visbias_base_vs_v2.ipynb` — matched Black/White VisBias Base vs V2 evaluation.

Exploratory baseline comparisons live under `comparisons/`.

The exact combined completed original training run is preserved under:

```text
archive/gemma3_sft_v1_v2_full_completed_run.ipynb
```

Public notebooks intentionally omit raw FairFace/IAT/VisBias image datasets, authentication tokens, checkpoints, and model weights. Lightweight metric tables are committed under `results/metrics/`; large raw outputs remain in the experiment Drive paths recorded by the notebooks.
