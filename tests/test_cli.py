from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

import main


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(main.cli, ["--help"]) 
    assert result.exit_code == 0
    assert "scan-all" in result.output


def test_scan_all_creates_info_report(tmp_path: Path, monkeypatch):
    # ensure reports directory is under tmp
    from utils import REPORTS_DIR
    monkeypatch.setattr("utils.REPORTS_DIR", tmp_path / "reports")

    runner = CliRunner()
    result = runner.invoke(main.cli, ["scan-all", "--no-full", "--quiet"]) 
    assert result.exit_code == 0
    reports = list((tmp_path / "reports").glob("*-Informational.md"))
    assert len(reports) == 1

