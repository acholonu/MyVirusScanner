from __future__ import annotations

from typing import List, Tuple


def run_check(verbose: bool = True) -> Tuple[List[str], List[str]]:
    info: List[str] = []
    threats: List[str] = []

    # Modern macOS restricts kernel extensions; deep rootkit detection is non-trivial.
    info.append("Rootkit check: No specific indicators scanned. For advanced analysis, use specialized tools (e.g., KnockKnock, LuLu).")

    return info, threats


