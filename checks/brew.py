from __future__ import annotations

from typing import List, Tuple

from utils import run_command


def run_check(verbose: bool = True) -> Tuple[List[str], List[str]]:
    info: List[str] = []
    threats: List[str] = []

    res = run_command(["brew", "outdated", "--verbose"])
    if res.returncode == 127:
        info.append("Homebrew not found. Install with `brew install` from https://brew.sh to enable outdated software checks.")
        return info, threats
    if res.returncode not in (0, 1):
        info.append("Unable to run Homebrew outdated check.")
        return info, threats

    # brew outdated returns code 0 when there are outdated formulae; 1 when none
    if res.stdout.strip():
        lines = [ln.strip() for ln in res.stdout.splitlines() if ln.strip()]
        count = len(lines)
        info.append(f"Homebrew: {count} outdated package(s) detected. Consider `brew upgrade`." )
    else:
        info.append("No outdated Homebrew packages found. Your system is up to date!")

    return info, threats


