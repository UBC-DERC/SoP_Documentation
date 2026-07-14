import base64
import requests

def fetch_csv_from_github(repo: str, path: str, ref: str, token: str) -> tuple[str, str]:
    """Fetch a file's raw contents from a GitHub repo. Returns (content, sha)."""
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    resp = requests.get(url, headers=headers, params={"ref": ref}, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    content = base64.b64decode(data["content"]).decode("utf-8")
    return content, data["sha"]
