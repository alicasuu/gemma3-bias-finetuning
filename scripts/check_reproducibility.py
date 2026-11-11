#!/usr/bin/env python3
"""Check the committed V1–V5 training data and held-out splits (CPU only)."""

from collections import Counter
import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

# Counts observed in the original Drive CSV files.
EXPECTED = {
    "v1": (1514, 516),
    "v2": (1514, 516),
    "v3": (3028, 516),
    "v4": (3364, 516),
    "v5": (2523, 700),
}
EXPECTED_TASKS = {
    "v3": {"iat": 1514, "comparison": 757, "decodingtrust": 757},
    "v4": {"iat": 1514, "comparison": 1177, "decodingtrust": 673},
    "v5": {"iat": 1514, "comparison": 632, "decodingtrust": 377},
}


def rows(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"Empty CSV: {path}")
        yield from reader


def verify():
    errors = []
    print("Checking dataset row counts and held-out topics...")
    for version, (expected_train, expected_dev) in EXPECTED.items():
        folder = ROOT / "datasets" / version
        dev_name = "dev.csv" if version in ("v1", "v2", "v5") else "dev_iat.csv"
        train_path, dev_path = folder / "train.csv", folder / dev_name
        try:
            train, dev = list(rows(train_path)), list(rows(dev_path))
        except (OSError, ValueError, UnicodeError, csv.Error) as exc:
            errors.append(f"{version}: {exc}")
            continue

        if (len(train), len(dev)) != (expected_train, expected_dev):
            errors.append(
                f"{version}: got {len(train)} train / {len(dev)} dev; "
                f"expected {expected_train} / {expected_dev}"
            )
        if version in EXPECTED_TASKS:
            counts = Counter(row.get("task_type") for row in train)
            if dict(counts) != EXPECTED_TASKS[version]:
                errors.append(f"{version}: unexpected task mix {dict(counts)}")
            heldout_name = (
                "decodingtrust_heldout_topics_REFERENCE_ONLY.csv"
                if version == "v5" else "decodingtrust_heldout_topics.csv"
            )
            try:
                heldout = list(rows(folder / heldout_name))
                train_topics = {
                    row["topic"] for row in train
                    if row.get("task_type") == "decodingtrust" and row.get("topic")
                }
                heldout_topics = {row["topic"] for row in heldout if row.get("topic")}
                overlap = train_topics & heldout_topics
                if overlap:
                    errors.append(f"{version}: held-out topics seen in training: {sorted(overlap)}")
            except (OSError, ValueError, UnicodeError, csv.Error) as exc:
                errors.append(f"{version}: held-out topics check failed: {exc}")
        print(f"  {version.upper()}: {len(train)} train, {len(dev)} dev")

    for name in (
        "configs/v5_config.json",
        "results/v5/iat_4prompts_summary_stats.csv",
        "results/v5/decodingtrust_heldout_summary_stats.csv",
        "results/v5/fer2013_external_test_summary.csv",
        "notebooks/v3/V3_MULTITASK_COMPLETE.ipynb",
        "notebooks/v4/V4_MULTITASK_BALANCED_RESPONSE.ipynb",
        "notebooks/v5/V5_Optimized_FreshBase_Colab.ipynb",
    ):
        if not (ROOT / name).is_file():
            errors.append(f"Missing expected file: {name}")

    if errors:
        print("\nFAILED:")
        for message in errors:
            print(f"  - {message}")
        return 1

    print("\nPASS: row counts, task mix, held-out topics and key artifacts checked.")
    print("This checks the repository files; it does not run a GPU experiment.")
    return 0


if __name__ == "__main__":
    sys.exit(verify())
