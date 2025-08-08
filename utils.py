from __future__ import annotations

import datetime as dt
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

REPORTS_DIR = Path("reports")


@dataclass
class ExecutionResult:
    command: List[str]
    returncode: int
    stdout: str
    stderr: str


def run_command(command: List[str], timeout_seconds: int = 20) -> ExecutionResult:
    try:
        completed = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout_seconds,
        )
        return ExecutionResult(command, completed.returncode, completed.stdout, completed.stderr)
    except FileNotFoundError:
        return ExecutionResult(command, 127, "", f"Command not found: {command[0]}")
    except subprocess.TimeoutExpired:
        return ExecutionResult(command, 124, "", "Command timed out")


def redact_sensitive_info(text: str) -> str:
    try:
        import re

        text = re.sub(r"/Users/[^/]+/", "/Users/[REDACTED]/", text)
        text = re.sub(r"`[^`]+`", "[REDACTED]", text)
        return text
    except Exception:
        return text


def ensure_reports_dir() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def _timestamp_prefix() -> str:
    return dt.datetime.now().strftime("%Y%m%d:%H%M%S")


def _format_info_markdown(entries: List[str]) -> str:
    header = "# macsecscan Informational Report\n\n"
    body = "\n\n".join(f"- {line}" for line in entries) if entries else "- No informational items."
    return header + body + "\n"


def _format_threats_markdown(entries: List[str]) -> str:
    header = "# macsecscan Security Concerns\n\n"
    body = "\n\n".join(f"- {line}" for line in entries)
    return header + (body + "\n" if body else "- No threats found.\n")


def write_reports(info_messages: List[str], threats: List[str]) -> Tuple[Path, Optional[Path]]:
    timestamp = _timestamp_prefix()
    info_path = REPORTS_DIR / f"{timestamp}-Informational.md"
    info_path.write_text(_format_info_markdown(info_messages))

    threats_path: Optional[Path] = None
    if threats:
        threats_path = REPORTS_DIR / f"{timestamp}-security_concerns.md"
        threats_path.write_text(_format_threats_markdown(threats))

    return info_path, threats_path


