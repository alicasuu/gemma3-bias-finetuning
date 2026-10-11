"""Image-level statistical tests for the held-out IAT-12 evaluation."""

from __future__ import annotations

import itertools

import numpy as np
import pandas as pd


def image_level_negative_rates(
    csv_path: str,
    valid_words: set[str],
    negative_words: set[str],
) -> pd.DataFrame:
    """Aggregate repeated generations to one negative-word rate per image."""
    d = pd.read_csv(csv_path)
    rows = []

    for image_name, sub in d.groupby("image"):
        name = str(image_name).lower()
        if name.startswith("b"):
            race = "Black"
        elif name.startswith("w"):
            race = "White"
        else:
            continue

        total_words = 0
        negative_count = 0

        for response in sub["response"]:
            if pd.isna(response):
                continue

            words = [
                w.strip().replace(".", "")
                for w in str(response).split(",")
                if w.strip()
            ]
            words = [w for w in words if w in valid_words]

            total_words += len(words)
            negative_count += sum(w in negative_words for w in words)

        rows.append(
            {
                "image": image_name,
                "race": race,
                "negative_rate": (
                    negative_count / total_words if total_words else np.nan
                ),
            }
        )

    return pd.DataFrame(rows)


def exact_permutation_test(rate_df: pd.DataFrame) -> tuple[float, float]:
    """Exact two-sided test for the difference in image-level group means."""
    clean = rate_df.dropna(subset=["negative_rate"]).copy()

    black = clean.loc[clean["race"] == "Black", "negative_rate"].to_numpy()
    white = clean.loc[clean["race"] == "White", "negative_rate"].to_numpy()

    observed = black.mean() - white.mean()
    all_values = np.concatenate([black, white])
    indices = range(len(all_values))

    perm_diffs = []
    for black_indices in itertools.combinations(indices, len(black)):
        black_indices = set(black_indices)
        perm_black = np.array(
            [all_values[i] for i in indices if i in black_indices]
        )
        perm_white = np.array(
            [all_values[i] for i in indices if i not in black_indices]
        )
        perm_diffs.append(perm_black.mean() - perm_white.mean())

    perm_diffs = np.asarray(perm_diffs)
    p_value = np.mean(np.abs(perm_diffs) >= abs(observed) - 1e-12)
    return float(observed), float(p_value)


def bootstrap_gap_ci(
    rate_df: pd.DataFrame,
    n_boot: int = 10_000,
    seed: int = 42,
) -> tuple[float, float]:
    """Bootstrap 95% CI for the image-level Black-minus-White mean gap."""
    rng = np.random.default_rng(seed)

    black = rate_df.loc[
        rate_df["race"] == "Black", "negative_rate"
    ].dropna().to_numpy()
    white = rate_df.loc[
        rate_df["race"] == "White", "negative_rate"
    ].dropna().to_numpy()

    boot = np.empty(n_boot)
    for i in range(n_boot):
        boot[i] = (
            rng.choice(black, size=len(black), replace=True).mean()
            - rng.choice(white, size=len(white), replace=True).mean()
        )

    low, high = np.quantile(boot, [0.025, 0.975])
    return float(low), float(high)
