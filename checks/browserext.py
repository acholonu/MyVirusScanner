from __future__ import annotations

import os
from pathlib import Path
from typing import List, Tuple


def run_check(verbose: bool = True) -> Tuple[List[str], List[str]]:
    info: List[str] = []
    threats: List[str] = []

    home = Path(os.path.expanduser("~"))
    chrome_ext_dir = home / "Library/Application Support/Google/Chrome/Default/Extensions"
    firefox_ext_dir = home / "Library/Application Support/Firefox/Profiles"
    safari_ext_dir = home / "Library/Containers/com.apple.Safari/Data/Library/Safari/Extensions"

    def count_if_exists(p: Path) -> int:
        return sum(1 for _ in p.iterdir()) if p.exists() and p.is_dir() else 0

    chrome_count = count_if_exists(chrome_ext_dir)
    safari_count = count_if_exists(safari_ext_dir)

    firefox_count = 0
    if firefox_ext_dir.exists():
        for profile in firefox_ext_dir.iterdir():
            if profile.is_dir():
                ext_dir = profile / "extensions"
                firefox_count += count_if_exists(ext_dir)

    total = chrome_count + safari_count + firefox_count
    info.append(f"Browser extensions detected: Chrome={chrome_count}, Safari={safari_count}, Firefox={firefox_count}, Total={total}.")

    return info, threats


