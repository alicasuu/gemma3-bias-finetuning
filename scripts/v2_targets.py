"""Utilities for valence-controlled SFT v2 target construction."""

from __future__ import annotations

import hashlib
import random
from typing import Iterable

import numpy as np
import pandas as pd


def stable_seed(text: str) -> int:
    return int(hashlib.sha256(str(text).encode("utf-8")).hexdigest()[:16], 16)


def negative_rate_from_responses(
    responses: Iterable[str],
    valid_words: list[str],
    negative_words: set[str],
) -> float:
    valid = set(valid_words)
    words = []

    for response in responses:
        if pd.isna(response):
            continue
        parsed = [
            w.strip().replace(".", "")
            for w in str(response).split(",")
            if w.strip()
        ]
        words.extend([w for w in parsed if w in valid])

    if not words:
        return np.nan

    return sum(w in negative_words for w in words) / len(words)


def make_valence_controlled_targets(
    source_df: pd.DataFrame,
    split_name: str,
    positive_words: list[str],
    negative_words: list[str],
    target_negative_rate: float,
) -> pd.DataFrame:
    """Create race-invariant 3-word targets for matched Black/White pairs.

    The image subset stays fixed. Expression metadata may remain in the dataframe
    for documentation, but it does not determine v2 target valence.
    """
    d = source_df.copy().reset_index(drop=True)
    d["target_v1"] = d["target"]
    d["_pair_key"] = d["pair_id"].astype(str)

    pair_sizes = d.groupby("_pair_key").size()
    if not (pair_sizes == 2).all():
        bad = pair_sizes[pair_sizes != 2]
        raise ValueError(f"{split_name}: expected exactly 2 rows per pair.\n{bad.head()}")

    race_sets = d.groupby("_pair_key")["source_race"].agg(set)
    bad_races = race_sets[race_sets.apply(lambda x: x != {"Black", "White"})]
    if len(bad_races):
        raise ValueError(f"{split_name}: malformed Black/White matched pairs.")

    pair_ids = list(pair_sizes.index)
    n_pairs = len(pair_ids)

    desired_negative_slots = int(round(3 * n_pairs * target_negative_rate))
    base_neg_per_pair = desired_negative_slots // n_pairs
    extra_negative_pairs = desired_negative_slots % n_pairs

    ranked_pairs = sorted(
        pair_ids,
        key=lambda pid: stable_seed(f"{split_name}|extra-negative|{pid}"),
    )
    extra_set = set(ranked_pairs[:extra_negative_pairs])

    pair_to_target = {}
    pair_to_neg_count = {}

    for pair_id in pair_ids:
        n_negative = min(
            3,
            base_neg_per_pair + (1 if pair_id in extra_set else 0),
        )
        n_positive = 3 - n_negative

        rng = random.Random(stable_seed(f"{split_name}|target|{pair_id}"))
        words = []

        if n_positive:
            words.extend(rng.sample(positive_words, n_positive))
        if n_negative:
            words.extend(rng.sample(negative_words, n_negative))

        rng.shuffle(words)
        pair_to_target[pair_id] = ", ".join(words)
        pair_to_neg_count[pair_id] = n_negative

    d["target"] = d["_pair_key"].map(pair_to_target)
    d["v2_negative_count"] = d["_pair_key"].map(pair_to_neg_count)

    assert (d.groupby("_pair_key")["target"].nunique() == 1).all()

    target_table = pd.crosstab(d["target"], d["source_race"])
    assert (target_table.get("Black", 0) == target_table.get("White", 0)).all()

    return d.drop(columns=["_pair_key"])
