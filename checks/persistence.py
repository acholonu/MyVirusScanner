from __future__ import annotations

from pathlib import Path
from typing import List, Tuple


PERSISTENCE_DIRS = [
    Path("/Library/LaunchAgents"),
    Path("/Library/LaunchDaemons"),
    Path.home() / "Library/LaunchAgents",
]


def run_check(verbose: bool = True) -> Tuple[List[str], List[str]]:
    info: List[str] = []
    threats: List[str] = []

    total = 0
    for d in PERSISTENCE_DIRS:
        if d.exists() and d.is_dir():
            count = sum(1 for _ in d.iterdir())
            info.append(f"Persistence items in {d}: {count}")
            total += count
        else:
            info.append(f"Directory not found: {d}")

    if total == 0:
        info.append("No persistence items detected in standard locations.")

    return info, threats


