from __future__ import annotations

from typing import List, Tuple

from utils import run_command


def run_check(verbose: bool = True) -> Tuple[List[str], List[str]]:
    info: List[str] = []
    threats: List[str] = []

    res = run_command(["fdesetup", "status"])
    if res.returncode == 127:
        info.append("`fdesetup` not found. Unable to check FileVault status.")
        return info, threats

    text = (res.stdout or "") + ("\n" + res.stderr if res.stderr else "")
    if "FileVault is On" in text:
        info.append("FileVault: Enabled.")
    elif "FileVault is Off" in text or "Off" in text:
        threats.append("FileVault is disabled. Enable disk encryption in System Settings > Privacy & Security > FileVault.")
    else:
        info.append("Unable to determine FileVault status.")

    return info, threats


