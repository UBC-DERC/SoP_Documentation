"""
sop.connectivity

Coordinates reading the consoles inventory (from a local file or
GitHub) and checking connectivity/authentication for each console.
"""

import csv
import io
from pathlib import Path

from dotenv import load_dotenv

from .check_console import check_console
from .resolve_csv_source import resolve_csv_source


def run(csv_arg: Path | None) -> list[tuple[str, str, str]]:
    """Run connectivity checks for every console in the resolved CSV."""
    load_dotenv()
    content = resolve_csv_source(csv_arg)
    reader = csv.DictReader(io.StringIO(content))
    return [check_console(row) for row in reader]
