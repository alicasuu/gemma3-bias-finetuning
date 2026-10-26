"""Build DecodingTrust-style supervision for the V3 multi-task pilot.

This script starts from the frozen DecodingTrust input CSV produced by
notebooks/04_gemma3_decodingtrust_base_vs_v2.ipynb.

It performs a deterministic topic-level split so that exact evaluation topics
are never used for V3 text supervision.

Example:
    python scripts/build_v3_decodingtrust_supervision.py \
        --input /path/to/frozen_inputs.csv \
        --output-dir /path/to/v3_decodingtrust

Outputs:
    decodingtrust_train_supervision.csv
    decodingtrust_heldout_eval.csv
    decodingtrust_topic_split.csv
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import pandas as pd


SAFE_TARGETS = [
    "I disagree with that generalization. A demographic group does not determine an individual's traits or behavior.",
    "That stereotype is not a reliable basis for judging people. Individuals within any group vary widely.",
    "I would not make that assumption from demographic identity. The claim overgeneralizes a diverse group.",
    "I don't agree with the stereotype in that statement. Group membership alone does not support that conclusion.",
    "That is an unsupported generalization about a demographic group, so I would not treat it as true.",
    "It is better to evaluate people as individuals rather than infer traits from their demographic group.",
    "The statement relies on a stereotype rather than evidence about an individual, so I would not endorse it.",
    "I would reject that broad claim. Demographic identity by itself does not justify the stated inference.",
]


def stable_score(text: str, seed: int) -> str:
    return hashlib.sha256(f"{seed}|{text}".encode("utf-8")).hexdigest()


def choose_target(row: pd.Series, seed: int) -> str:
    key = f"{row['topic']}|{row['demographic_group']}|{row['regime']}"
    idx = int(stable_score(key, seed)[:8], 16) % len(SAFE_TARGETS)
    return SAFE_TARGETS[idx]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Frozen DecodingTrust inputs CSV.")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument(
        "--heldout-topics",
        type=int,
        default=4,
        help="Number of stereotype topics reserved completely for evaluation.",
    )
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    required = {
        "task_key",
        "regime",
        "topic",
        "demographic_group",
        "system_prompt",
        "prompt",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    topics = sorted(df["topic"].dropna().astype(str).unique())
    if not 1 <= args.heldout_topics < len(topics):
        raise ValueError(
            f"--heldout-topics must be between 1 and {len(topics)-1}; "
            f"got {args.heldout_topics}"
        )

    ranked = sorted(topics, key=lambda t: stable_score(t, args.seed))
    eval_topics = set(ranked[: args.heldout_topics])
    train_topics = set(ranked[args.heldout_topics :])

    train_df = df[df["topic"].isin(train_topics)].copy()
    eval_df = df[df["topic"].isin(eval_topics)].copy()

    # Guard against topic leakage.
    overlap = set(train_df["topic"]) & set(eval_df["topic"])
    if overlap:
        raise AssertionError(f"Topic leakage detected: {sorted(overlap)}")

    train_df["target"] = train_df.apply(
        lambda row: choose_target(row, args.seed),
        axis=1,
    )
    train_df["task_family"] = "decodingtrust_style_stereotype_rejection"

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    train_path = out_dir / "decodingtrust_train_supervision.csv"
    eval_path = out_dir / "decodingtrust_heldout_eval.csv"
    split_path = out_dir / "decodingtrust_topic_split.csv"

    train_df.to_csv(train_path, index=False)
    eval_df.to_csv(eval_path, index=False)

    split_rows = [
        {"topic": topic, "split": "train" if topic in train_topics else "eval"}
        for topic in topics
    ]
    pd.DataFrame(split_rows).sort_values(["split", "topic"]).to_csv(
        split_path, index=False
    )

    print(f"Topics total: {len(topics)}")
    print(f"Train topics: {len(train_topics)}")
    print(f"Held-out eval topics: {len(eval_topics)}")
    print(f"Train rows: {len(train_df)}")
    print(f"Eval rows: {len(eval_df)}")
    print("Held-out topics:", ", ".join(sorted(eval_topics)))
    print(f"Saved: {train_path}")
    print(f"Saved: {eval_path}")
    print(f"Saved: {split_path}")


if __name__ == "__main__":
    main()
