import os
from pathlib import Path
from .fetch_csv_from_github import fetch_csv_from_github

def resolve_csv_source(csv_arg: Path | None) -> str:
    """Return raw CSV text, from a local file if given, otherwise from
    a configured GitHub source. Fails loudly if neither is available."""
    if csv_arg is not None:
        if not csv_arg.exists():
            raise FileNotFoundError(f"Could not find {csv_arg}")
        return csv_arg.read_text()

    repo = os.environ.get("SOP_CONSOLES_REPO")
    path = os.environ.get("SOP_CONSOLES_PATH")
    ref = os.environ.get("SOP_CONSOLES_REF", "main")
    token = os.environ.get("GITHUB_TOKEN")

    if not (repo and path and token):
        raise RuntimeError(
            "No --csv provided, and GitHub source is not fully "
            "configured. Set SOP_CONSOLES_REPO, SOP_CONSOLES_PATH, "
            "and GITHUB_TOKEN in your .env, or pass --csv explicitly."
        )

    content, sha = fetch_csv_from_github(repo, path, ref, token)
    print(f"Fetched consoles CSV from {repo}@{ref} (sha {sha[:8]})")
    return content
