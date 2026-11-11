# V5: exact recorded configuration

This is transcribed from the saved V5 `manifest.json` in the project's Google Drive (`IAT/results/gemma/v5_v4_optimized_freshbase/`). It describes the **recorded run**, rather than recommended defaults.

## Training

| Field | Recorded value |
| --- | --- |
| Base | `google/gemma-3-12b-it` |
| Seed | `45` |
| Training rows | `2523` |
| Development rows | `700` |
| IAT weight | `0.60` requested; `0.6000793` actual |
| DecodingTrust weight | `0.15` requested; `0.1494253` actual |
| Comparison weight | `0.25` requested; `0.2504954` actual |
| Within comparisons: answerable visual | `0.90` requested; `0.8987342` actual |
| Within comparisons: unsupported socioeconomic | `0.10` requested; `0.1012658` actual |
| Initialization | **Fresh Gemma base**; V4 adapter weights were **not** loaded |
| IAT targets | V2 targets unchanged; shared with V4 |
| DecodingTrust targets | V4 explicit targets reused |
| DecodingTrust factual fraction | `0.1007958` within DT |

### Environment captured by the manifest

```text
torch==2.11.0+cu130
transformers==5.22.1
peft==0.21.2
datasets==5.1.0
```

The values above reflect the saved run's environment. Install CUDA/PyTorch builds compatible with your GPU. Other packages, CUDA drivers and full lockfile should be verified from the original notebook.

### Drive inputs

```text
IAT/sft_data/v5_v4_optimized_freshbase/train_v5.csv
IAT/sft_data/v5_v4_optimized_freshbase/dev_v5.csv
IAT/sft_data/v5_v4_optimized_freshbase/config.json
IAT/sft_data/v3_multitask/decodingtrust_heldout_topics.csv
```

Saved adapter: `IAT/models/gemma3-12b-v5-v4-optimized-freshbase/`

## Evaluation

- IAT: 50 repeats, temperature `1.0`, top-p `1.0`
- Four prompt variants: `original`, `paraphrased`, `image_grounded`, `format_focused`
- DecodingTrust: V3 topic-held-out split
- VisBias: frozen inputs from `IAT/results/visbias/gemma3_base_vs_v2/frozen_inputs/comparison_tasks.csv`
- BOLD: frozen inputs from `IAT/results/bold/gemma3_base_vs_v2_race/frozen_inputs.csv`
- FER2013 external follow-up: `abhilash88/fer2013-enhanced`, `test` split, seed `2071`, 100 external pairs

The evaluation add-on reads the saved adapter and **does not retrain**. Its recorded output folder is `IAT/results/gemma/v5_v4_optimized_freshbase/`. Key output files are listed in [the handoff](v3_v5_handoff.md).

## Quick verification

Compare the manifest with the `config.json`, then check:

1. The model loads from the saved V5 adapter, not V4.
2. The held-out DecodingTrust topics were excluded from training.
3. Each prompt variant has its own IAT summary.
4. Paired comparison CSVs match the same frozen inputs.
5. The external FER2013 sample uses the recorded test split and seed.

Original V5 training and validation notebooks are in the research Drive; this document preserves their configuration and source locations.
