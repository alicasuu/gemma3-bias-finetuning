# Gemma-3 Multimodal Bias Fine-Tuning (UC Berkeley URAP)

Research project evaluating whether parameter-efficient fine-tuning of **google/gemma-3-12b-it** reduces race-associated response disparities **without** degrading response quality, instruction following, or performance on independent benchmarks.

> **Research status (November 2026):** V1–V5 have been explored. This is an experimental research repository, not a validated unbiased model. Improvements on one benchmark do not establish fairness or generalization.

## Research question

When a vision-language model sees a face, does it associate different negative or positive words with people in different racial groups? Can supervised fine-tuning with matched examples reduce that gap while retaining useful visual understanding and avoiding stereotypes or unsupported social inferences?

We compare the original Gemma-3-12B-IT model against successive LoRA/QLoRA adapters, test robustness to prompt wording, and independently evaluate on text and multimodal benchmarks.

## Start here

1. Read **[V3–V5 handoff and source inventory](docs/v3_v5_handoff.md)** to understand each version, available artifacts, and what still needs verification.
2. Read [training-data design](docs/training_data.md), [external benchmarks](docs/external_benchmarks.md), and [experiment log](docs/experiment_log.md) for earlier experiments.
3. For existing executable examples, inspect [notebooks](notebooks/) and [scripts](scripts/).
4. Reproduce a run using the exact version-specific dataset, adapter, prompt, decoding settings, and evaluation script. **Do not treat the V3/V4/V5 source inventory as a fully tested one-command reproduction recipe.** Some version-specific notebooks and environment details still need to be consolidated.

## Experiment timeline

| Version | Main intervention | Intended test |
| --- | --- | --- |
| Base | Untuned `google/gemma-3-12b-it` | Reference behavior |
| V1 | FairFace expression-derived matched-pair SFT | Initial reduction in Black–White IAT negative-word gap |
| V2 | Valence-controlled SFT targets | Avoid V1's global negative-word shift |
| **V3** | Multitask training: IAT, stereotype rejection, grounded description, unsupported inference | Generalization beyond the IAT |
| **V4** | Balanced-response training | Improve response behavior and robustness |
| **V5** | Optimized fresh-base training with V4-derived design | Reduce global negative valence and assess external retention |

These labels describe the experiment lineage, **not proof of causal improvement**. For version-specific data files and artifacts, see [handoff](docs/v3_v5_handoff.md).

## Evaluation framework

- **IAT-style face/word association:** held-out 12-image benchmark, 61-word vocabulary, exactly three selected words. Track Black and White negative-word rates, signed/absolute gap, overall valence, output validity, vocabulary diversity, and sensitivity to prompts. Repeated generations from one image are not independent samples; use image-level inference.
- **DecodingTrust:** stereotype-related agreement and behavior on held-out topics.
- **VisBias:** unsupported socioeconomic inferences from image pairs, abstention, and A/B order effects.
- **BOLD:** toxicity, sentiment, regard, and differences across demographic categories.
- **FER2013:** independent facial-expression comparison, with attention to evaluation-set independence and methodology.

### Key observations and caveats

The November 3 presentation reports that V5 reduced the overall IAT negative-word rate from **68.9% to 19.5%** in the reported comparison, while retaining low DecodingTrust stereotype agreement and appropriate VisBias abstention. It also reports **92% accuracy** on an independent FER2013 comparison. These are **experiment-specific reported metrics**, not universal model performance. BOLD sentiment decline and Black–White disparities remain concerns; further images, seeds, and prompt-sensitivity analysis are needed. See [presentation](https://docs.google.com/presentation/d/1bEsHXiTRT3-JSj83314_HKY6b1U_CG4qQvUqaHernfk/edit).

Earlier V2 experiments improved the IAT gap but worsened some external behaviors, including DecodingTrust stereotype agreement and VisBias order consistency. This motivates multi-benchmark evaluation rather than optimizing a single fairness metric.

## Repository map

- `notebooks/`: runnable notebooks already checked into this repository (historically focused on Base–V2).
- `scripts/`: evaluation, statistics, data preparation and visualization utilities.
- `docs/`: methodology, experiment history, handoff and limitations.
- `results/`: lightweight published metrics and summaries.
- **External Google Drive:** version-specific V3–V5 training/dev CSVs, model adapters/checkpoints, raw results, and V5 follow-up outputs. Consult the [handoff inventory](docs/v3_v5_handoff.md). These files are not automatically present when cloning.

## Reproduction principles

- Preserve original train/dev/test partitions and topic-level held-out splits.
- Keep the 12 historical IAT evaluation images outside training.
- Record model revision, adapter checkpoint, Python/package versions, GPU, seeds, generation parameters, prompts, and file hashes for each run.
- Distinguish training-data-derived labels from human-ground-truth annotations.
- Report both absolute disparity and global response-rate changes; include confidence intervals and multiplicity corrections where appropriate.
- Check prompt order and image order; do not interpret refusal, fixed-position choices, or global positivity as successful debiasing.
- Keep raw image datasets and large adapter weights in access-controlled storage, subject to their licenses and research permissions.

## Handoff for Peyton and collaborators

See **[docs/v3_v5_handoff.md](docs/v3_v5_handoff.md)** for the source inventory, version-to-dataset mapping, evaluation files, and a practical reproduction checklist. The source materials were located in the project's Google Drive, but this commit does **not** claim that all external notebooks, model artifacts, or datasets have been mirrored or rerun.

## Ethics, data, and publication

Race and expression annotations can be noisy, and facial appearance is not evidence of personality, intelligence, income, education, or other social attributes. Do not use this work to infer such traits about real people. The public repository excludes face-image copies, proprietary/permissioned datasets, private Drive paths, Hugging Face tokens, credentials, and large model weights. Review any external CSVs for redistribution permissions before publishing.

## Team

UC Berkeley URAP research collaboration. Project materials and version history are maintained for research reproducibility and handoff.
