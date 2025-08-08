from __future__ import annotations

from typing import List, Tuple

from utils import run_command


def run_check(verbose: bool = True) -> Tuple[List[str], List[str]]:
    info: List[str] = []
    threats: List[str] = []

    res = run_command(["dscl", ".", "-read", "/Groups/admin", "GroupMembership"])
    if res.returncode == 127:
        info.append("`dscl` not found. Unable to audit admin users.")
        return info, threats

    line = (res.stdout or "").strip().splitlines()[:1]
    members = []
    if line:
        parts = line[0].split(":", 1)
        if len(parts) == 2:
            members = [x for x in parts[1].split() if x]

    if members:
        info.append(f"Admin users: {len(members)} expected accounts found.")
    else:
        info.append("No admin users found or unable to parse admin group membership.")

    # Without a configured allowlist we cannot flag threats safely.
    return info, threats


