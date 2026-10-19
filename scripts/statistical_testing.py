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


def welch_t_test(rate_df: pd.DataFrame) -> dict[str, float]:
    """Two-sided Welch difference-in-means t-test on image-level rates."""
    from scipy.stats import ttest_ind

    clean = rate_df.dropna(subset=["negative_rate"]).copy()
    black = clean.loc[clean["race"] == "Black", "negative_rate"].to_numpy()
    white = clean.loc[clean["race"] == "White", "negative_rate"].to_numpy()

    result = ttest_ind(black, white, equal_var=False)
    return {
        "black_mean": float(black.mean()),
        "white_mean": float(white.mean()),
        "black_minus_white_gap": float(black.mean() - white.mean()),
        "welch_t_stat": float(result.statistic),
        "welch_t_p_value": float(result.pvalue),
    }


def ols_race_effect(rate_df: pd.DataFrame) -> dict[str, float]:
    """OLS: negative_rate_i = beta0 + beta1 * Black_i + error_i.

    beta1 is the image-level Black-minus-White mean difference.
    HC2 robust standard errors are reported because n=12 is small.
    """
    import statsmodels.api as sm

    clean = rate_df.dropna(subset=["negative_rate"]).copy()
    clean["black_indicator"] = (clean["race"] == "Black").astype(int)

    X = sm.add_constant(clean[["black_indicator"]])
    fit = sm.OLS(clean["negative_rate"], X).fit(cov_type="HC2")

    beta = float(fit.params["black_indicator"])
    se = float(fit.bse["black_indicator"])
    t_stat = float(fit.tvalues["black_indicator"])
    p_value = float(fit.pvalues["black_indicator"])
    ci_low, ci_high = fit.conf_int().loc["black_indicator"]

    return {
        "ols_black_effect": beta,
        "ols_hc2_se": se,
        "ols_t_stat": t_stat,
        "ols_p_value": p_value,
        "ols_95ci_low": float(ci_low),
        "ols_95ci_high": float(ci_high),
        "ols_n_images": int(len(clean)),
    }


def summarize_image_level_tests(rate_df: pd.DataFrame) -> dict[str, float]:
    """Return Welch t-test, OLS, exact permutation, and bootstrap CI together."""
    t = welch_t_test(rate_df)
    o = ols_race_effect(rate_df)
    gap, perm_p = exact_permutation_test(rate_df)
    boot_low, boot_high = bootstrap_gap_ci(rate_df)

    return {
        **t,
        **o,
        "exact_permutation_p_value": float(perm_p),
        "bootstrap_95ci_low": float(boot_low),
        "bootstrap_95ci_high": float(boot_high),
    }
