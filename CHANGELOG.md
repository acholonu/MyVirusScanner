# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project adheres to Semantic Versioning.

## [0.1.0] - 2025-08-08
### Added
- Initial CLI scaffold with Click
- Check modules (brew, npm, pip, mac updates, filevault, user audit, netports, browserext, persistence, rootkit)
- Malware scan commands (ClamAV/YARA) with graceful fallbacks
- Reports output to `reports/`
- Basic pytest test for CLI help and report creation
- uv-based setup guidance in README and cheatsheet
