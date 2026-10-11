# Training Data Documentation

## Source

Current fine-tuning experiments use the URAP project's **FairFace 4,000 matched release**.

The workflow expects:
```text
FairFace 4000 Paired/
├── manifest.csv
├── matched_pairs.csv
└── images/
```

## Train / validation usage

- FairFace `train` split → supervised fine-tuning
- FairFace `development` split → validation
- FairFace `test` split → untouched
- Original 12 IAT benchmark images → fully held out

## V1 filtering

SFT v1 retains rows satisfying:
```text
expression_confidence >= 0.80
expression_label in {happy, sad, angry}
```

Only complete matched pairs are retained. Each pair contains exactly:
```text
1 Black image + 1 White image
```

Current retained dataset:
```text
Train: 1,514 images
Development: 516 images
```

## V1 target construction

FairFace does not provide source-authored 3-word SFT answers.

V1 constructs 3-word targets from the visible-expression metadata, for example:
```text
happy -> "Smiling, Cheerful, Joyful"
sad   -> "Sadness, Grief, Pain"
angry -> "Angry, Annoy, Negative"
```

Both members of a matched Black/White pair receive the exact same target.

The expression metadata is treated as a proxy for experimental supervision, not as human-verified ground-truth emotion.

## V2 target construction

V2 keeps the same FairFace train/dev images, pairing, base model, QLoRA hyperparameters, prompt, and held-out IAT evaluation.

Only the SFT target construction changes.

V2 controls the positive/negative target distribution so the training target negative-word rate is close to the baseline Gemma-3 global negative-word rate. Matched Black/White pair members still receive the exact same target.

## Data not committed to Git

Do not commit FairFace images, IAT face images, model checkpoints, LoRA adapter weights, or authentication tokens.
