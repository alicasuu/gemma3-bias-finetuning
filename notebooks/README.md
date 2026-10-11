# Notebook workflow

Planned experiment notebooks:

1. `01_gemma3_baseline.ipynb` — held-out IAT-12 baseline evaluation.
2. `02_gemma3_sft_v1_expression.ipynb` — FairFace SFT + LoRA with expression-derived targets.
3. `03_gemma3_sft_v2_valence_controlled.ipynb` — controlled v2 experiment with baseline-matched target valence.

The active Colab notebook is still being run/refined. When syncing notebooks to this public repository:

- remove authentication tokens and private paths where possible;
- do not embed FairFace or IAT face images;
- do not commit checkpoints or LoRA adapter weights;
- keep the 12 IAT evaluation images held out from fine-tuning.

Reusable experiment logic lives under `scripts/` so results are not documented only inside Colab cells.
