import requests
import os

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)

def check_console(row: dict) -> tuple[str, str, str]:
    console_id = row["console_id"]
    host = row["host_ip"]
    key_ref = row.get("api_key_ref", "").strip()

    if not key_ref:
        return console_id, "SKIPPED", "No api_key_ref set in CSV"

    api_key = os.environ.get(key_ref)
    if not api_key:
        return console_id, "SKIPPED", f"Env var {key_ref} not set"

    url = f"https://{host}/proxy/protect/integration/v1/cameras"
    headers = {"X-API-KEY": api_key}

    try:
        resp = requests.get(url, headers=headers, verify=False, timeout=5)
    except requests.exceptions.RequestException as e:
        return console_id, "FAIL", f"Connection error: {e}"

    if resp.status_code == 200:
        try:
            count = len(resp.json())
        except ValueError:
            count = "unknown (non-JSON response)"
        return console_id, "OK", f"{count} camera(s) returned"
    else:
        return console_id, "FAIL", f"HTTP {resp.status_code}: {resp.text[:200]}"
