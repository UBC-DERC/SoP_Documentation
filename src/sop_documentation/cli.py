"""
sop.cli

Command-line entry point for running console connectivity checks.
"""

import argparse
import sys
from pathlib import Path

from .connect import run


def main():
    parser = argparse.ArgumentParser(
        description="Check connectivity/authentication for UniFi "
        "Protect consoles listed in an inventory CSV."
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=None,
        help=(
            "Path to a local consoles inventory CSV. If omitted, "
            "attempts to fetch from GitHub using SOP_CONSOLES_REPO, "
            "SOP_CONSOLES_PATH, SOP_CONSOLES_REF, and GITHUB_TOKEN "
            "from .env."
        ),
    )
    args = parser.parse_args()

    try:
        results = run(args.csv)
    except (FileNotFoundError, RuntimeError) as e:
        print(e)
        sys.exit(1)

    print(f"{'console_id':<12} {'status':<8} details")
    print("-" * 60)
    for console_id, status, details in results:
        print(f"{console_id:<12} {status:<8} {details}")


if __name__ == "__main__":
    main()