from __future__ import annotations

from typing import List, Tuple

from utils import run_command


def run_check(verbose: bool = True) -> Tuple[List[str], List[str]]:
    info: List[str] = []
    threats: List[str] = []

    res = run_command(["python3", "-m", "pip", "list", "--outdated", "--format=json"])
    if res.returncode == 127:
        info.append("pip not found. Use `python3 -m ensurepip` or install Python/pip to enable pip checks.")
        return info, threats
    if res.returncode not in (0,):
        info.append("Unable to run pip outdated check.")
        return info, threats

    try:
        import json

        data = json.loads(res.stdout or "[]")
        count = len(data)
        if count > 0:
            info.append(f"pip: {count} outdated package(s) detected. Consider `pip install -U <name>`. ")
        else:
            info.append("No outdated pip packages found.")
    except Exception:
        info.append("Unable to parse pip output; run `pip list --outdated` manually.")

    return info, threats


