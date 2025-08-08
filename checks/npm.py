from __future__ import annotations

from typing import List, Tuple

from utils import run_command


def run_check(verbose: bool = True) -> Tuple[List[str], List[str]]:
    info: List[str] = []
    threats: List[str] = []

    res = run_command(["npm", "-g", "outdated", "--json"])
    if res.returncode == 127:
        info.append("npm not found. Install Node.js (`brew install node`) to enable npm checks.")
        return info, threats

    if res.returncode not in (0, 1):  # npm returns 1 when outdated packages exist
        info.append("Unable to run npm outdated check.")
        return info, threats

    # parse JSON if any
    try:
        import json

        data = json.loads(res.stdout or "{}")
        count = len(data)
        if count > 0:
            info.append(f"npm (global): {count} outdated package(s) detected. Consider `npm update -g`.")
        else:
            info.append("No outdated global npm packages found.")
    except Exception:
        # Fallback: if not JSON, just report generic
        if res.stdout.strip():
            info.append("npm outdated packages detected. Consider updating globally with `npm update -g`.")
        else:
            info.append("No outdated global npm packages found.")

    return info, threats


