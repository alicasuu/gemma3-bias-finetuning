# V3–V5 experiment handoff and source inventory

**Updated:** November 2026  
**Purpose:** Help Peyton and future researchers locate, understand, and reproduce the Gemma-3-12B-IT debiasing experiments.  
**Status:** Source files have been located in the project Google Drive. This document is an **inventory and reproduction plan**, not a claim that all files are published to GitHub or that each run has been rerun.

## 1. What is being tested?

We test whether LoRA/QLoRA fine-tuning changes race-associated word selection and whether those changes hold up under different prompt wordings and independent benchmarks. A lower IAT gap alone can be misleading: it may come from globally avoiding negative words, invalid outputs, or order/prompt sensitivity. Therefore every version should be evaluated for **bias gap, overall valence, validity, and external-task retention**.

## 2. Version lineage and canonical data

| Version | Training data | Dev data | Design |
| --- | --- | --- | --- |
| V3 | `sft_data/v3_multitask/train_v3_multitask.csv` | `sft_data/v3_multitask/dev_v3_iat_only.csv` | Multitask SFT, including IAT-style supervision and held-out DecodingTrust topics |
| V4 | `sft_data/v4_balanced_response/train_v4_balanced_response.csv` | `sft_data/v4_balanced_response/dev_v4_iat_only.csv` | Balanced-response SFT |
| V5 | `sft_data/v5_v4_optimized_freshbase/train_v5.csv` | `sft_data/v5_v4_optimized_freshbase/dev_v5.csv` | Optimized fresh-base run; see adjacent `config.json` |

The relative paths above refer to the **Google Drive `IAT` folder**, not this GitHub repository. The V3 and V4 data folders also contain `decodingtrust_train_topics.csv` and `decodingtrust_heldout_topics.csv`; V5 has `decodingtrust_heldout_topics_REFERENCE_ONLY.csv`. Do not accidentally use held-out topics for training.

V1 and V2 training/dev CSVs also exist in `sft_data/`; consult them when documenting how supervision evolved across all five versions.

## 3. Located model artifacts

Under `IAT/models/`:

- `gemma3-12b-fairface-sft-lora-v3-multitask/` and `...-checkpoints/`
- `gemma3-12b-fairface-sft-lora-v4-balanced-response/` and `...-checkpoints/`
- `gemma3-12b-v5-v4-optimized-freshbase/` and `...-checkpoints/`
- Earlier V1/V2 adapters and `gemma_dpo_sweeps/` are available for historical comparisons.

These model directories are **not committed to this public repository**. Verify access, adapter configuration, and checkpoint selection with the team before reproduction.

## 4. Located evaluation outputs

- **V3:** `results/gemma/v3_multitask/v3_raw_responses.csv`, `comparison_summary.csv`, `order_consistency.csv`.
- **V4:** `results/gemma/gemma3_v4_balanced_response/v4_raw_responses.csv`, `comparison_summary.csv`, `order_consistency.csv`.
- **V5 follow-up:** `results/gemma/v5_v4_optimized_freshbase/` contains `training_log.csv`, `iat_4prompts_raw.csv`, `iat_4prompts_summary_stats.csv`, `iat_paired_changes_and_significance.csv`, `iat_prompts_holm_adjusted_p.csv`, `decodingtrust_heldout_raw.csv`, `decodingtrust_heldout_summary_stats.csv`, `visbias_frozen_raw.csv`, `visbias_frozen_summary_stats.csv`, `bold_frozen_raw.csv`, `bold_scored.csv`, `bold_category_summary_stats.csv`, `fer2013_test_comparison_raw.csv`, `fer2013_external_test_summary.csv`, and `manifest.json` / `v5_followup_outputs_manifest.json`.

**Note:** The path components are based on folder names observed in Drive; verify the exact nested path before using them in code. Some similarly named V5 output folders exist.

## 5. Reproduction workflow for Peyton

1. **Select the experiment version.** Record V3/V4/V5, base model `google/gemma-3-12b-it`, and the exact adapter/checkpoint.
2. **Inspect the training data.** Verify schema, row counts, data provenance, train/dev split, and any reference-only or held-out topics. Record file SHA-256.
3. **Recreate the environment.** Confirm the original training notebook/script, Python/CUDA/PyTorch/Transformers/PEFT/bitsandbytes versions, GPU type, quantization and LoRA settings, optimizer, learning rate, batch/accumulation, epochs, and random seeds. **These settings have not all been independently verified for V3–V5.**
4. **Start with evaluation-only reproduction** using a saved adapter; do not retrain merely to reproduce a published result.
5. **Match the original prompts and generation settings** (temperature, samples per image, word list, output format, image order, and prompt variant). Peyton's November 3 slides evaluate multiple prompt variants; prompt wording is a major experimental variable.
6. **Regenerate and compare summary tables.** Check IAT negative-word rate and Black–White gap, output validity, DecodingTrust stereotype agreement, VisBias abstention/order effects, BOLD sentiment/regard, and independent FER2013 results.
7. **Recompute uncertainty** using appropriate clustering/pairing and multiple-testing correction; document any discrepancies.
8. **Only then retrain** if the goal is to verify the training pipeline itself. Record a new seed and separate replicated results from original results.

## 6. What the November 3 presentation says

The URAP presentation reports V5 improved overall IAT negative-word rate from 68.9% to 19.5%, retained low DecodingTrust stereotype agreement and appropriate VisBias abstention, and achieved 92% accuracy on an independent FER2013 comparison. It also flags BOLD sentiment decline, Black–White disparities, prompt sensitivity, and need for more independent images/seeds.

These figures are reported from the presentation and **have not been independently recalculated in this handoff**. Use the raw and summary CSVs to verify denominators, exact comparison, and statistical uncertainty before quoting them in a paper.

Presentation: https://docs.google.com/presentation/d/1bEsHXiTRT3-JSj83314_HKY6b1U_CG4qQvUqaHernfk/edit

## 7. Remaining work before calling this fully reproducible

- Locate and commit **sanitized V3/V4/V5 training and evaluation notebooks/scripts**, or link controlled-access originals.
- Verify the exact V3/V4/V5 environment lockfiles, seeds, training configurations, and checkpoint IDs.
- Review training CSVs and raw outputs for redistribution permission and sensitive content; publish approved files only.
- Add stable artifact hashes and a version-to-checkpoint mapping.
- Test a fresh runtime evaluation and compare regenerated results with stored summaries.
- Document the V1→V5 training-data and prompt changes in a single checked table.

## 8. Data policy

Do not commit face-image datasets, adapter/model weights, credentials, private access tokens, or files whose licensing has not been checked. Keep heavyweight and access-controlled artifacts in Drive. Repository readers should request approved access from the project team.
