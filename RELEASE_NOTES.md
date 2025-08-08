# macsecscan v0.1.0 (2025-08-08)

Initial public release of the mac security scanner CLI.

## Highlights
- Default checks: Homebrew, npm, pip, macOS updates, FileVault, admin/user audit
- Malware scanning integration: ClamAV + YARA (optional)
- Opt-in checks: open ports, browser extensions, persistence hints, rootkit hints
- Timestamped reports written to `reports/`
- uv-based setup and pytest tests

## Install
```
uv venv
. .venv/bin/activate
uv pip install -e '.[dev]'
```

## Usage
```
uv run macsecscan scan-all            # default checks
uv run macsecscan scan-all --full     # include opt-in checks
uv run macsecscan malware-scan --path ~ --rules yara_rules
uv run macsecscan yara-scan --rules yara_rules --path ~
```
