#!/usr/bin/env python3
"""
inspect_baselines.py — Inspect referenced baseline systems.

Reads baselines_config.json and prints metadata for each baseline.
Optionally clones public repositories when --clone is passed.

This script does NOT make network calls unless --clone is explicitly used.

Usage:
    python baseline_reproducibility/inspect_baselines.py
    python baseline_reproducibility/inspect_baselines.py --clone
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = SCRIPT_DIR / "baselines_config.json"
ATTEMPTS_PATH = SCRIPT_DIR / "baseline_attempts.csv"
EXTERNAL_DIR = SCRIPT_DIR / "external"


def load_config(path: Path) -> dict:
    """Load baselines configuration."""
    if not path.exists():
        print(f"ERROR: Config file not found: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r") as f:
        return json.load(f)


def print_baseline_info(baselines: list) -> None:
    """Print metadata for each baseline."""
    print("=" * 70)
    print("REFERENCED BASELINE SYSTEMS")
    print("=" * 70)
    for i, b in enumerate(baselines, 1):
        name = b.get("paper_or_system", b.get("system_name", "Unknown"))
        print(f"\n--- Baseline {i}: {name} ---")
        print(f"  Full Citation:    {b.get('full_citation', 'N/A')}")
        if b.get("paper_url"):
            print(f"  Paper URL:        {b['paper_url']}")
        print(f"  Repo URL:         {b.get('repo_url', 'N/A')}")
        print(f"  Repo Available:   {b.get('repo_available', b.get('public_repo_found', 'Unknown'))}")
        print(f"  Attempt Status:   {b.get('attempt_status', b.get('status', 'Unknown'))}")
        print(f"  Baseline Role:    {b.get('baseline_role', 'N/A')}")
        print(f"  Observed Issue:   {b.get('observed_issue', b.get('issue_observed', 'N/A'))}")
        print(f"  Decision:         {b.get('decision', 'N/A')}")

    print()


def clone_repos(baselines: list) -> None:
    """Clone public repositories into external/ directory."""
    EXTERNAL_DIR.mkdir(parents=True, exist_ok=True)
    print("\n" + "=" * 70)
    print("CLONING PUBLIC REPOSITORIES")
    print("=" * 70)

    for b in baselines:
        repo_available = b.get("repo_available", b.get("public_repo_found", "No"))
        if repo_available != "Yes":
            name = b.get("paper_or_system", b.get("system_name", "Unknown"))
            print(f"\n  Skipping {name}: repo not confirmed available.")
            continue

        url = b["repo_url"]
        if url.startswith("TODO"):
            name = b.get("paper_or_system", b.get("system_name", "Unknown"))
            print(f"\n  Skipping {name}: repo URL is a TODO placeholder.")
            continue

        repo_name = url.rstrip("/").split("/")[-1]
        dest = EXTERNAL_DIR / repo_name

        if dest.exists():
            print(f"\n  {repo_name}: already cloned at {dest}")
            continue

        print(f"\n  Cloning {url} into {dest}...")
        try:
            subprocess.run(
                ["git", "clone", "--depth", "1", url, str(dest)],
                check=True,
                timeout=120,
            )
            print(f"  Successfully cloned {repo_name}.")
        except subprocess.CalledProcessError as e:
            print(f"  ERROR: Failed to clone {url}: {e}", file=sys.stderr)
        except subprocess.TimeoutExpired:
            print(f"  ERROR: Clone timed out for {url}", file=sys.stderr)


def update_attempts_csv(baselines: list) -> None:
    """Write/update baseline_attempts.csv from config data."""
    import csv
    headers = ["paper_or_system", "repo_url", "repo_available",
               "attempt_status", "baseline_role", "observed_issue", "decision"]
    rows = []
    for b in baselines:
        rows.append({h: b.get(h, "") for h in headers})

    with open(ATTEMPTS_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Updated: {ATTEMPTS_PATH}")


def print_next_steps(baselines: list) -> None:
    """Print next steps for manual inspection."""
    print("\n" + "=" * 70)
    print("NEXT STEPS FOR MANUAL INSPECTION")
    print("=" * 70)
    for b in baselines:
        name = b.get("paper_or_system", b.get("system_name", "Unknown"))
        repo_available = b.get("repo_available", b.get("public_repo_found", "No"))
        if repo_available == "Yes":
            print(f"\n  {name}:")
            print(f"    1. Clone: git clone {b['repo_url']}")
            print(f"    2. Read the repo's README for setup instructions.")
            print(f"    3. Check if dependencies can be installed.")
            print(f"    4. Attempt to run any provided evaluation scripts.")
            print(f"    5. Update baseline_attempts.csv with actual run status.")
        else:
            print(f"\n  {name}:")
            print(f"    - Repo not confirmed available. Contact authors or check proceedings.")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Inspect referenced baseline systems for reproducibility."
    )
    parser.add_argument(
        "--clone",
        action="store_true",
        help="Clone public repositories into baseline_reproducibility/external/. "
             "Requires network access and git.",
    )
    args = parser.parse_args()

    config = load_config(CONFIG_PATH)
    baselines = config.get("baselines", [])

    if not baselines:
        print("No baselines found in config.", file=sys.stderr)
        sys.exit(1)

    print_baseline_info(baselines)

    if args.clone:
        clone_repos(baselines)

    update_attempts_csv(baselines)
    print_next_steps(baselines)
    print("Done.")


if __name__ == "__main__":
    main()
