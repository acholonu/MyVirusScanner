# macsecscan

A Python CLI to scan your Mac for common security concerns using system checks and optional malware scanning.

## Setup (uv)

- Requires Python 3.11+
- Uses `uv` for environment and installs

Commands:

```
uv venv
. .venv/bin/activate
uv pip install -e '.[dev]'
```

## Usage

```
uv run macsecscan --help
uv run macsecscan scan-all
uv run macsecscan scan-all --full
```

## Output
- Informational report written to `reports/YYYYMMDD:HHMMSS-Informational.md`
- Security concerns report written only if threats are found: `reports/YYYYMMDD:HHMMSS-security_concerns.md`
