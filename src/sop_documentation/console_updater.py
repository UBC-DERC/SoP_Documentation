"""
sop.connectivity

Utilities for validating connectivity to UniFi Protect consoles
listed in an inventory CSV, sourced either from a local file or
from a private GitHub repository (see .env configuration).
"""

import argparse
import csv
import io
import sys
from pathlib import Path
from .check_console import check_console
from .resolve_csv_source import resolve_csv_source


import requests
from dotenv import load_dotenv

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)



def run(csv_arg: Path | None) -> list[tuple[str, str, str]]:
    load_dotenv()
    content = resolve_csv_source(csv_arg)
    reader = csv.DictReader(io.StringIO(content))
    return [check_console(row) for row in reader]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
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