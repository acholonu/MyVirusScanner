from __future__ import annotations

from typing import List, Tuple

from utils import run_command


def run_check(verbose: bool = True) -> Tuple[List[str], List[str]]:
    info: List[str] = []
    threats: List[str] = []

    res = run_command(["softwareupdate", "-l"])
    if res.returncode == 127:
        info.append("`softwareupdate` tool not found. Unable to check macOS updates.")
        return info, threats

    # softwareupdate -l returns 0 with updates or no updates; parse stdout
    text = (res.stdout or "") + ("\n" + res.stderr if res.stderr else "")
    if "No new software available" in text:
        info.append("No macOS updates found.")
    else:
        # naive detection
        info.append("macOS updates may be available. Open System Settings > General > Software Update.")

    return info, threats


