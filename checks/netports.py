from __future__ import annotations

from typing import List, Tuple

from utils import run_command


def run_check(verbose: bool = True) -> Tuple[List[str], List[str]]:
    info: List[str] = []
    threats: List[str] = []

    res = run_command(["lsof", "-i", "-P", "-n"])
    if res.returncode == 127:
        info.append("`lsof` not found. Unable to list open network ports.")
        return info, threats

    listen_count = 0
    for line in (res.stdout or "").splitlines():
        if "LISTEN" in line:
            listen_count += 1

    if listen_count > 0:
        info.append(f"Open network listeners detected: {listen_count}. Review for unexpected services.")
    else:
        info.append("No open network listeners detected.")

    return info, threats


