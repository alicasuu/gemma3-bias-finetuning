"""Plot VisBias A/B order consistency for Base vs V2.

Input CSV columns:
attribute, base_order_consistency, v2_order_consistency

Values are proportions in [0, 1]. The figure reports percentages.
"""

from pathlib import Path
import argparse
import pandas as pd
import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="results/metrics/visbias_order_effect_summary.csv",
        help="CSV containing order-consistency summary.",
    )
    parser.add_argument(
        "--output",
        default="results/metrics/visbias_order_effect.png",
        help="Output PNG path.",
    )
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    required = {"attribute", "base_order_consistency", "v2_order_consistency"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    plot_df = df.copy()
    plot_df["attribute"] = plot_df["attribute"].str.title()
    plot_df["Base"] = 100 * plot_df["base_order_consistency"]
    plot_df["V2"] = 100 * plot_df["v2_order_consistency"]

    ax = plot_df.set_index("attribute")[["Base", "V2"]].plot(
        kind="bar",
        figsize=(8, 5),
        rot=0,
    )
    ax.set_title("VisBias order consistency")
    ax.set_xlabel("")
    ax.set_ylabel("Order-consistent comparisons (%)")
    ax.set_ylim(0, 100)
    ax.legend(title="Model")

    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f%%", padding=3)

    plt.tight_layout()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out, dpi=200, bbox_inches="tight")
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
