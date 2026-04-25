#!/usr/bin/env python3
"""
compute_knee.py — Compute the knee point in the citation-count curve.

Reads data/citation_counts_top100.csv, sorts by citation_count descending,
computes the knee using maximum perpendicular distance from the line
connecting the first and last points, and validates against the
documented knee rank (22) and threshold (167).

Usage:
    python scripts/compute_knee.py
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CITATIONS_PATH = PROJECT_ROOT / "data" / "citation_counts_top100.csv"
KNEE_SUMMARY_PATH = PROJECT_ROOT / "outputs" / "knee_summary.csv"
KNEE_PLOT_PATH = PROJECT_ROOT / "outputs" / "knee_plot.png"

# Documented values from the project document
EXPECTED_KNEE_RANK = 22
EXPECTED_THRESHOLD = 167


def load_citations(path: Path) -> pd.DataFrame:
    """Load and sort citation counts."""
    if not path.exists():
        print(f"ERROR: Citation file not found: {path}", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(path)

    if "citation_count" not in df.columns:
        print("ERROR: 'citation_count' column not found.", file=sys.stderr)
        sys.exit(1)

    df["citation_count"] = pd.to_numeric(df["citation_count"], errors="coerce")
    df = df.dropna(subset=["citation_count"])
    df = df.sort_values("citation_count", ascending=False).reset_index(drop=True)
    df["rank"] = range(1, len(df) + 1)

    return df


def find_knee(ranks: np.ndarray, values: np.ndarray) -> int:
    """Find knee point using maximum perpendicular distance method.

    Draws a line from the first point (rank 1, max citations) to the last
    point (rank N, min citations). For each point, computes the perpendicular
    distance to this line. The rank with maximum distance is the knee.

    Returns the 1-based rank of the knee point.
    """
    n = len(ranks)
    if n < 3:
        return 1

    # Normalize to [0, 1] for distance computation
    x = (ranks - ranks[0]) / (ranks[-1] - ranks[0])
    y = (values - values[-1]) / (values[0] - values[-1])

    # Line from first to last point: (0, 1) to (1, 0)
    # Direction vector: (1, -1)
    # Normal: (1, 1) / sqrt(2)
    # Distance from point (xi, yi) to line x + y = 1:
    #   d = |xi + yi - 1| / sqrt(2)
    distances = np.abs(x + y - 1.0) / np.sqrt(2.0)

    knee_idx = np.argmax(distances)
    return int(ranks[knee_idx])


def save_plot(df: pd.DataFrame, knee_rank: int, threshold: int) -> bool:
    """Save citation curve plot with knee annotation. Returns True if saved."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("  matplotlib not available; skipping plot generation.")
        return False

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df["rank"], df["citation_count"], "b-", linewidth=1.5, label="Citations")
    ax.axvline(x=knee_rank, color="r", linestyle="--", linewidth=1,
               label=f"Knee (rank {knee_rank})")
    ax.axhline(y=threshold, color="g", linestyle=":", linewidth=1,
               label=f"Threshold ({threshold} citations)")

    # Shade above-the-knee region
    above = df[df["rank"] <= knee_rank]
    ax.fill_between(above["rank"], above["citation_count"], alpha=0.15, color="blue")

    ax.set_xlabel("Rank (by citation count)")
    ax.set_ylabel("Citation Count")
    ax.set_title("Citation Count Curve with Knee Analysis")
    ax.legend()
    ax.set_xlim(1, len(df))
    ax.set_ylim(0, df["citation_count"].max() * 1.05)

    KNEE_PLOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(KNEE_PLOT_PATH, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return True


def main():
    print(f"Loading citations from: {CITATIONS_PATH}")
    df = load_citations(CITATIONS_PATH)
    print(f"Loaded {len(df)} papers.\n")

    ranks = df["rank"].values
    values = df["citation_count"].values

    # Compute knee
    knee_rank = find_knee(ranks, values)
    threshold = int(df[df["rank"] == knee_rank]["citation_count"].iloc[0])

    print("=" * 60)
    print("KNEE ANALYSIS RESULTS")
    print("=" * 60)
    print(f"  Computed knee rank:       {knee_rank}")
    print(f"  Computed threshold:       {threshold} citations")
    print(f"  Expected knee rank:       {EXPECTED_KNEE_RANK}")
    print(f"  Expected threshold:       {EXPECTED_THRESHOLD}")
    print()

    # Validate against documented values
    if knee_rank == EXPECTED_KNEE_RANK:
        print(f"  ✓ Knee rank matches documented value ({EXPECTED_KNEE_RANK}).")
    else:
        print(f"  WARNING: Computed knee rank ({knee_rank}) differs from "
              f"documented value ({EXPECTED_KNEE_RANK}).")
        print(f"  The documented knee rank {EXPECTED_KNEE_RANK} has "
              f"{int(df[df['rank'] == EXPECTED_KNEE_RANK]['citation_count'].iloc[0])} citations.")

    if threshold == EXPECTED_THRESHOLD:
        print(f"  ✓ Threshold matches documented value ({EXPECTED_THRESHOLD}).")
    else:
        print(f"  WARNING: Computed threshold ({threshold}) differs from "
              f"documented value ({EXPECTED_THRESHOLD}).")

    # Papers above knee
    above_knee = df[df["rank"] <= EXPECTED_KNEE_RANK]
    below_knee_first = df[df["rank"] == EXPECTED_KNEE_RANK + 1]
    print(f"\n  Papers above the knee (rank <= {EXPECTED_KNEE_RANK}): {len(above_knee)}")
    print(f"  Citation range above knee: {above_knee['citation_count'].min()}-{above_knee['citation_count'].max()}")
    if not below_knee_first.empty:
        print(f"  First paper below knee: rank {EXPECTED_KNEE_RANK + 1}, "
              f"{int(below_knee_first['citation_count'].iloc[0])} citations")

    # Save knee summary
    KNEE_SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    summary = pd.DataFrame([{
        "computed_knee_rank": knee_rank,
        "computed_threshold": threshold,
        "documented_knee_rank": EXPECTED_KNEE_RANK,
        "documented_threshold": EXPECTED_THRESHOLD,
        "total_papers": len(df),
        "above_knee_count": len(above_knee),
        "max_citations": int(values[0]),
        "min_citations": int(values[-1]),
        "match": knee_rank == EXPECTED_KNEE_RANK and threshold == EXPECTED_THRESHOLD,
    }])
    summary.to_csv(KNEE_SUMMARY_PATH, index=False)
    print(f"\n  Knee summary saved to: {KNEE_SUMMARY_PATH}")

    # Try to save plot
    if save_plot(df, EXPECTED_KNEE_RANK, EXPECTED_THRESHOLD):
        print(f"  Knee plot saved to: {KNEE_PLOT_PATH}")

    print()


if __name__ == "__main__":
    main()
