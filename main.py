from __future__ import annotations

import time
from pathlib import Path
from typing import List, Tuple

import click
from colorama import Fore, Style, init as colorama_init

from utils import (
    ensure_reports_dir,
    write_reports,
)
from checks import brew, npm, pip as pip_check, mac_updates, malware, filevault, useraudit, netports, browserext, persistence, rootkit


colorama_init(autoreset=True)


def _collect_default_checks(verbose: bool) -> Tuple[List[str], List[str]]:
    info_messages: List[str] = []
    threats: List[str] = []

    # Brew
    brew_info, brew_threats = brew.run_check(verbose=verbose)
    info_messages.extend(brew_info)
    threats.extend(brew_threats)

    # npm
    npm_info, npm_threats = npm.run_check(verbose=verbose)
    info_messages.extend(npm_info)
    threats.extend(npm_threats)

    # pip
    pip_info, pip_threats = pip_check.run_check(verbose=verbose)
    info_messages.extend(pip_info)
    threats.extend(pip_threats)

    # macOS updates
    upd_info, upd_threats = mac_updates.run_check(verbose=verbose)
    info_messages.extend(upd_info)
    threats.extend(upd_threats)

    # FileVault
    fv_info, fv_threats = filevault.run_check(verbose=verbose)
    info_messages.extend(fv_info)
    threats.extend(fv_threats)

    # User audit
    ua_info, ua_threats = useraudit.run_check(verbose=verbose)
    info_messages.extend(ua_info)
    threats.extend(ua_threats)

    # Malware (ClamAV + YARA default placeholder without path)
    mw_info, mw_threats = malware.run_default(verbose=verbose)
    info_messages.extend(mw_info)
    threats.extend(mw_threats)

    return info_messages, threats


def _collect_opt_in_checks(verbose: bool) -> Tuple[List[str], List[str]]:
    info_messages: List[str] = []
    threats: List[str] = []

    # Net ports
    np_info, np_threats = netports.run_check(verbose=verbose)
    info_messages.extend(np_info)
    threats.extend(np_threats)

    # Browser extensions
    be_info, be_threats = browserext.run_check(verbose=verbose)
    info_messages.extend(be_info)
    threats.extend(be_threats)

    # Persistence
    ps_info, ps_threats = persistence.run_check(verbose=verbose)
    info_messages.extend(ps_info)
    threats.extend(ps_threats)

    # Rootkit hints
    rk_info, rk_threats = rootkit.run_check(verbose=verbose)
    info_messages.extend(rk_info)
    threats.extend(rk_threats)

    return info_messages, threats


@click.group()
@click.version_option("0.1.0", prog_name="macsecscan")
def cli() -> None:
    """Scan your Mac for security concerns."""


@cli.command("scan-all")
@click.option("--full/--no-full", default=False, help="Include opt-in checks.")
@click.option("--verbose/--quiet", default=True, help="Verbose output to terminal.")
def scan_all(full: bool, verbose: bool) -> None:
    start = time.time()
    if verbose:
        click.echo(Fore.CYAN + "Starting macsecscan..." + Style.RESET_ALL)

    info_messages, threats = _collect_default_checks(verbose=verbose)
    if full:
        oi_info, oi_threats = _collect_opt_in_checks(verbose=verbose)
        info_messages.extend(oi_info)
        threats.extend(oi_threats)

    ensure_reports_dir()
    info_path, threats_path = write_reports(info_messages, threats)

    if verbose:
        click.echo(Fore.GREEN + f"Informational report: {info_path}" + Style.RESET_ALL)
        if threats_path:
            click.echo(Fore.RED + f"Security concerns report: {threats_path}" + Style.RESET_ALL)
        else:
            click.echo(Fore.GREEN + "No security threats found. Security concerns file was not created." + Style.RESET_ALL)
        duration = time.time() - start
        click.echo(Fore.CYAN + f"Scan complete in {duration:.1f}s" + Style.RESET_ALL)


@cli.command("brew-check")
@click.option("--verbose/--quiet", default=True)
def brew_check(verbose: bool) -> None:
    info_messages, threats = brew.run_check(verbose=verbose)
    ensure_reports_dir()
    write_reports(info_messages, threats)


@cli.command("npm-check")
@click.option("--verbose/--quiet", default=True)
def npm_check(verbose: bool) -> None:
    info_messages, threats = npm.run_check(verbose=verbose)
    ensure_reports_dir()
    write_reports(info_messages, threats)


@cli.command("pip-check")
@click.option("--verbose/--quiet", default=True)
def pip_check_cmd(verbose: bool) -> None:
    info_messages, threats = pip_check.run_check(verbose=verbose)
    ensure_reports_dir()
    write_reports(info_messages, threats)


@cli.command("mac-updates")
@click.option("--verbose/--quiet", default=True)
def mac_updates_cmd(verbose: bool) -> None:
    info_messages, threats = mac_updates.run_check(verbose=verbose)
    ensure_reports_dir()
    write_reports(info_messages, threats)


@cli.command("malware-scan")
@click.option("--path", type=click.Path(exists=True, file_okay=False, path_type=Path), required=False, help="Directory to scan recursively.")
@click.option("--rules", type=click.Path(exists=True, file_okay=False, path_type=Path), required=False, help="YARA rules directory.")
@click.option("--verbose/--quiet", default=True)
def malware_scan(path: Path | None, rules: Path | None, verbose: bool) -> None:
    info_messages, threats = malware.run_scan(scan_path=path, rules_dir=rules, verbose=verbose)
    ensure_reports_dir()
    write_reports(info_messages, threats)


@cli.command("yara-scan")
@click.option("--rules", type=click.Path(exists=True, file_okay=False, path_type=Path), required=True, help="YARA rules directory.")
@click.option("--path", type=click.Path(exists=True, file_okay=False, path_type=Path), required=True, help="Directory to scan.")
@click.option("--verbose/--quiet", default=True)
def yara_scan(rules: Path, path: Path, verbose: bool) -> None:
    info_messages, threats = malware.run_yara_only(scan_path=path, rules_dir=rules, verbose=verbose)
    ensure_reports_dir()
    write_reports(info_messages, threats)


@cli.command("netports-check")
@click.option("--verbose/--quiet", default=True)
def netports_check(verbose: bool) -> None:
    info_messages, threats = netports.run_check(verbose=verbose)
    ensure_reports_dir()
    write_reports(info_messages, threats)


@cli.command("browserext-check")
@click.option("--verbose/--quiet", default=True)
def browserext_check(verbose: bool) -> None:
    info_messages, threats = browserext.run_check(verbose=verbose)
    ensure_reports_dir()
    write_reports(info_messages, threats)


@cli.command("persistence-check")
@click.option("--verbose/--quiet", default=True)
def persistence_check(verbose: bool) -> None:
    info_messages, threats = persistence.run_check(verbose=verbose)
    ensure_reports_dir()
    write_reports(info_messages, threats)


@cli.command("rootkit-check")
@click.option("--verbose/--quiet", default=True)
def rootkit_check(verbose: bool) -> None:
    info_messages, threats = rootkit.run_check(verbose=verbose)
    ensure_reports_dir()
    write_reports(info_messages, threats)


if __name__ == "__main__":
    cli()


