# macsecscan cheatsheet

## Install with uv
```
uv venv
. .venv/bin/activate
uv pip install -e '.[dev]'
```

## Run
```
uv run macsecscan --help
uv run macsecscan scan-all
uv run macsecscan scan-all --full
```

## Malware tools
```
brew install clamav yara
freshclam
uv run macsecscan malware-scan --path ~
uv run macsecscan yara-scan --rules yara_rules --path ~
```
