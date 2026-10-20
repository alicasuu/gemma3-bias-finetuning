# Results

This directory stores lightweight experiment outputs suitable for GitHub.

Current metric files under `results/metrics/` include:

### IAT
- `gemma3_baseline_v1_v2_metrics.csv`
- `gemma3_baseline_v1_v2_image_level_stats.csv`

### DecodingTrust
- `decodingtrust_base_vs_v2_summary.csv`
- `decodingtrust_direct_change.csv`

### BOLD
- `bold_base_vs_v2_summary.csv`
- `bold_direct_change.csv`

### VisBias
- `visbias_base_vs_v2_summary.csv`
- `visbias_direct_change.csv`

### Cross-benchmark
- `cross_benchmark_summary.csv`

The notebooks contain the full evaluation code; lightweight summary metrics are committed here, while large raw outputs and generated figures remain in the experiment Drive paths recorded by each notebook.

Do **not** commit:
- raw face-image datasets;
- normalized VisBias image copies;
- multi-GB model checkpoints;
- LoRA adapter weights;
- authentication tokens;
- large raw response dumps when a lightweight summary is sufficient.

Raw outputs are retained in the experiment Drive paths recorded inside each notebook.
