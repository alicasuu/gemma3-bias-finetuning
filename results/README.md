# Results

Store lightweight experiment outputs here.

Recommended layout:
```text
results/
├── metrics/
│   ├── baseline_metrics.csv
│   ├── sft_v1_metrics.csv
│   ├── sft_v2_metrics.csv
│   └── statistical_tests.csv
└── figures/
    ├── baseline.png
    ├── sft_v1.png
    └── sft_v2.png
```

Do not commit raw face-image datasets, model checkpoints, or LoRA adapter weights.
