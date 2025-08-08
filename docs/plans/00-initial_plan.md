# macsecscan: Project Plan for a Python CLI Mac Security Scanner (with ClamAV & YARA)

---

## 1. Project Structure

```plaintext
macsecscan/
│
├── README.md            # Project overview, setup, usage, FAQ
├── CHEATSHEET.md        # 1-page quickstart and advanced usage
├── cheatsheet.pdf       # PDF version of cheatsheet (generated)
├── main.py              # CLI entrypoint (Click app)
├── checks/
│   ├── __init__.py
│   ├── brew.py
│   ├── npm.py
│   ├── pip.py
│   ├── mac_updates.py
│   ├── malware.py       # Handles ClamAV & YARA
│   ├── config.py
│   ├── tcc.py           # TCC permissions check (anti-keylogger)
│   ├── filevault.py     # FileVault encryption status (default)
│   ├── useraudit.py     # Admin/user audit (default)
│   ├── netports.py      # Open ports/listeners (opt-in)
│   ├── browserext.py    # Browser extensions (opt-in)
│   ├── persistence.py   # Persistence mechanisms (opt-in)
│   └── rootkit.py       # Rootkit/persistence hints (opt-in)
          # YARA rule sets (bundled & custom)
# YARA rule sets (bundled & custom)
│   ├── README.md        # YARA rules documentation
│   └── example_rules.yar
├── utils.py
└── pyproject.toml
```

---

## 2. Task Modules & Checks

**Default Checks** (always run):

- Outdated Software (brew, npm, pip)
- macOS Updates
- Malware Scan (ClamAV, YARA)
- System Settings (firewall, SIP, Gatekeeper, TCC)
- FileVault Encryption Status
  - Check if FileVault is enabled (disk encryption).
- Admin/User Audit
  - List all admin users; flag any unknown/unexpected accounts with admin rights.

**Opt-In Checks** (run with `--full` or specific flag):

- Network Listeners & Open Ports

  - List open network ports; flag unexpected listeners.

- Browser Extensions/Plugins

  - List browser extensions for Chrome, Safari, Firefox; flag known risky extensions.

- Persistence Mechanisms

  - Check LaunchDaemons/Agents, cron jobs, login items for suspicious entries.

- Rootkit/Persistence Hints

  - Look for hidden files, unsigned kernel extensions, suspicious system hooks.

- YARA Rule Creation: Bundle example rules, provide README/docs, and optionally a CLI helper to generate rules.

---

## 3. Workflow & CLI Integration

- All default checks are implemented as Click commands in `main.py` and run with `scan-all`.
- Opt-in checks can be enabled with `--full` or individual CLI flags.
- Example usage:
  ```sh
  macsecscan scan-all                 # default
  macsecscan scan-all --full          # all checks (incl. opt-in)
  macsecscan netports-check           # individual opt-in check
  ```
- Output file protocol:
  - Always create: `YYYYMMDD:HHMMSS-Informational.md` (info and warnings, no threats)
  - Create only if threats: `YYYYMMDD:HHMMSS-security_concerns.md` (only threats)
  - If no threats found, inform user and do **not** create `security_concerns` file.
- Each output file is:
  - Well-organized markdown (sections, tables, links)
  - Each point includes: what was found, explanation, why it matters, next steps, helpful references
  - Use Claude CLI for enhanced explanations: e.g., `claude -p "Prompt about {issue}"`

---

## 4. Example YARA Rules README.md (to place in yara\_rules/)

````
# YARA Rules for macsecscan

This folder contains YARA rules for use with the `macsecscan` security scanner.  
YARA rules help identify suspicious files, known malware, or risky behaviors on your Mac by pattern matching file content or properties.

---

## What Are YARA Rules?

[YARA](https://yara.readthedocs.io/) is a powerful tool used to identify and classify malware or files by defining rules based on textual or binary patterns.

- **macsecscan** can scan your files with any rules you place in this folder.
- Both **bundled** (included here) and **custom** rules can be used.

---

## How to Use These Rules

You can run a YARA scan using the CLI:

```sh
macsecscan yara-scan --rules yara_rules/ --path ~/
````

- The `--rules` flag points to this folder.
- The `--path` flag specifies which directory to scan.

---

## Adding Your Own Rules

- To add your own rules, simply drop `.yar` or `.yara` files into this folder.
- Check out the [YARA documentation](https://yara.readthedocs.io/) to learn more about writing rules.

---

## Example Rules

Below are some example YARA rules included in this folder:

---

### 1. Suspicious Mac Executable

Detects Mach-O binaries and common shell scripts in user directories.

```yara
rule Suspicious_Mac_Executables
{
    meta:
        description = "Detects Mach-O executables and common shell scripts"
        author = "macsecscan"
        reference = "https://yara.readthedocs.io/"
    strings:
        $macho = { cf fa ed fe }     // Mach-O binary header (Mac executable)
        $sh = "#!/bin/sh"
        $bash = "#!/bin/bash"
    condition:
        any of them
}
```

---

### 2. Known Malicious Filenames

Detects files with known malicious names.

```yara
rule Known_Malware_Filename
{
    meta:
        description = "Detects files with known bad or suspicious filenames"
        author = "macsecscan"
    strings:
        $1 = "evil_malware"
        $2 = "bad_trojan"
        $3 = "suspicious_script"
    condition:
        any of them
}
```

---

### 3. Suspicious Temp Scripts

Detects scripts placed in temporary directories.

```yara
rule Suspicious_Temp_Scripts
{
    meta:
        description = "Detects scripts in /tmp or /var/folders"
        author = "macsecscan"
    strings:
        $shebang = "#!"
    condition:
        (uint16(0) == 0x2321) and
        (filepath matches /\/tmp\/|\/var\/folders\//)
}
```

*Note: filepath matching requires scanning tools that support the ****\`\`**** variable, such as newer YARA versions.*

---

## Contributing Rules

If you create a useful rule, consider submitting it upstream or sharing with the security community!

- See [YARA Rules Repository](https://github.com/YARA-Rules/rules) for community-maintained rules.

---

## Disclaimer

These rules are for demonstration and educational purposes.\
Detection results may include **false positives**. Always review matches carefully.

---

Happy hunting!\
The macsecscan Team

````

---

## 5. pyproject.toml Example (with uv)

```toml
[project]
name = "macsecscan"
version = "0.1.0"
description = "Scan your Mac for security concerns from the command line."
authors = [
    { name="Your Name", email="youremail@example.com" }
]
dependencies = [
    "click",
    # "colorama", "tabulate", "requests", etc. (if needed)
]
requires-python = ">=3.9"

[project.scripts]
macsecscan = "main:cli"
````

---

## 7. Testing Protocol

To ensure reliability, security, and usability, adopt a robust testing protocol. This focuses on **end-to-end function**, base cases, and important edge cases for your CLI tool and its modules.

### A. Testing Strategy

1. **End-to-End (E2E) Tests:**
   - Test full runs of the `scan-all` command in realistic environments (with/without ClamAV & YARA installed).
   - Validate that actionable output or installation instructions are produced.
2. **Base Case Tests:**
   - Ensure each individual command (brew-check, npm-check, etc.) returns expected results in the most common scenario (e.g., with one outdated package, or a clean system).
3. **Edge Case Tests:**
   - Run modules with missing dependencies (simulate uninstalled ClamAV/YARA).
   - Simulate empty scan targets (empty directories, empty rules folder).
   - Test with corrupted or invalid YARA rules.
   - Test with permission errors (e.g., scanning /root/ without sudo).
   - Test output with non-English macOS/locales.

### B. Testing Tools

- Use [`pytest`](https://docs.pytest.org/) for Python unit and CLI tests.
- Use [`pytest-click`](https://pypi.org/project/pytest-click/) for Click command-line interface testing.
- Consider [tox](https://tox.readthedocs.io/) for multi-Python/version test automation.

### C. Example Test Cases

1. **E2E:**

   - `macsecscan scan-all` on a fully set up system; assert all checks run and output summary is as expected.
   - `macsecscan scan-all` with ClamAV and YARA missing; assert user is prompted to install.

2. **Base Case:**

   - `macsecscan brew-check` with no outdated packages; assert "All up to date" message appears.
   - `macsecscan pip-check` with one outdated package; assert it is listed.

3. **Edge Cases:**

   - `macsecscan malware-scan` with ClamAV missing; check install guidance.
   - `macsecscan yara-scan` with empty/nonexistent rules directory; assert error message.
   - `macsecscan yara-scan` with invalid YARA file; assert error/handled failure.
   - Try scanning a directory with permission denied; assert graceful error.

### D. Test Automation

- Create a `tests/` directory in the repo:
  ```plaintext
  tests/
  ├── test_brew.py
  ├── test_npm.py
  ├── test_pip.py
  ├── test_mac_updates.py
  ├── test_malware.py
  ├── test_yara.py
  └── test_e2e.py
  ```
- Use mocks to simulate missing dependencies or error cases.
- CI/CD: Add a GitHub Actions or similar workflow to run all tests on push/PR.

---

## 8. Usability Plan & User Feedback

### A. Core Usability Goals

- Use clear, concise, and jargon-free language in all output.
- Provide actionable suggestions and next steps whenever a problem or warning is found.
- Use color and formatting to make output readable (success, warning, error, info).
- Always offer install or usage guidance if a dependency is missing or a check is skipped.
- Ensure every command has a helpful `--help` description and usage examples.

### B. Types of Feedback Provided

#### 1. Success / All-Clear Messages

- "No outdated Homebrew packages found. Your system is up to date!"
- "No malware detected with ClamAV."
- "Firewall is enabled. Good job!"

#### 2. Actionable Warnings

- "Warning: 3 outdated npm packages detected. Run `npm update -g` to update."
- "System Integrity Protection (SIP) is disabled. Run `csrutil enable` in Recovery Mode to re-enable."
- "ClamAV not found. Install it with: `brew install clamav` to enable malware scanning."

#### 3. Error and Edge Case Handling

- "Error: Could not scan directory `/System` – permission denied."
- "YARA tool is not installed. Please run: `brew install yara`."
- "No YARA rules found in `yara_rules/`. Add rules to enable YARA scans."

#### 4. Scan Summary

At the end of `scan-all`, provide a summary block, e.g.:

```
Scan Complete!
--------------
Outdated Software:      2 issues (see above)
System Updates:         No updates found
Malware Scan:           ClamAV missing (install recommended)
System Settings:        1 warning (SIP disabled)
See above for details and suggested actions.
```

### C. Usability Enhancements

- Use `colorama` or Click’s coloring features for easy-to-read output.
- Consistent formatting for all feedback, suggestions, and errors.
- Support `--quiet` (minimal output) and `--verbose` (detailed output) CLI flags.
- Optionally support output to file/log (`--output report.txt`).

### D. CLI Design

- Every command has a clear `--help` output and real-world usage examples.
- Consistent naming and documentation for commands and options.

### E. Feedback Delivery

- Real-time output as checks run.
- Immediate, actionable suggestions after each issue or warning.
- Concise summary at end of all-in-one scans.
- All install tips and next steps are presented in context, not buried in logs.

---

## 6. Next Steps

1. Create the project directory structure.
2. Add your `pyproject.toml` as above and install with `uv`.
3. Implement check modules with fallback to install instructions for ClamAV/YARA.
4. Add default and opt-in check modules as above.
5. Add YARA rules and update `yara_rules/README.md`.
6. Test all CLI commands and ensure user guidance is clear.
7. Build and automate your test suite as outlined above.
8. Create and maintain a project-level `README.md` explaining setup, features, usage, and all checks (with risk/explanation).
9. Create and maintain a 1-page `CHEATSHEET.md` (and PDF) for quick install, usage, customization, and check explanations.

---

## 9. Output Files & Reporting

- **Informational Output:** Always write a file named `YYYYMMDD:HHMMSS-Informational.md` containing all informational findings and warnings. Do not include security threats in this file.
- **Security Concerns Output:** Only write a file named `YYYYMMDD:HHMMSS-security_concerns.md` if actionable security threats are found. If no threats, inform the user and do not create this file.
- **Content Structure:**
  - Each finding must include:
    - Clear summary of what was found
    - Explanation (using plain language, ideally enhanced by Claude CLI)
    - Why it matters (risk or relevance)
    - Suggested next steps
    - Helpful references (links, docs, guides)
  - Files should use readable markdown (sections, tables, links) and be logically organized (by check or by severity).
- **Claude CLI Integration:**
  - The app can use `claude -p "your prompt"` to generate, clarify, or enhance explanations and next steps in the report files.
  - Sample use: To clarify a finding, prompt Claude: `claude -p "Explain why having admin users who are not expected is a security risk on macOS."`

---

## 10. Claude LLM Integration

- For every finding in any check, before writing to the markdown output files, the tool will invoke the Claude CLI (`claude -p "..."`) with a context-rich prompt to:
  - Explain each finding (informational or threat) in clear, plain language.
  - Suggest next steps or mitigations where appropriate.
  - Provide at least one reputable reference or link.
- Each prompt will be tailored to the specific check and result. Example prompts: ... (existing content) ...
- If Claude is unavailable (CLI error, timeout, etc.), the tool will provide a generic fallback explanation and log the error for the user.
- (Optional) The tool may cache prompts/results to avoid redundant queries for repeated findings.
- All Claude-enhanced explanations are included in the output markdown files for maximum user value and clarity.

---

## 11. Example Output File Templates

... (existing content) ...

---

## 12. PII Protection & Prompt Sanitation

- **Policy:**\
  No personally identifiable information (PII) is ever sent to the Claude LLM (or any other AI/third-party service). All data sent to Claude for explanations is sanitized and generalized.

- **What Counts as PII:**

  - Usernames (e.g., `bob`)
  - Full file paths containing usernames (e.g., `/Users/alex/Documents/`)
  - Device hostnames, email addresses, unique IDs, or other identifying data
  - Content of user files
  - Any process details or browser extension IDs that are user-specific

- **How the App Ensures PII is Not Sent:**

  - **Redaction:** All potentially identifying info is replaced with `[REDACTED]` or generalized tags before including in a Claude prompt.
    - E.g., `/Users/alex/Documents/confidential.txt` → `/Users/[REDACTED]/[file].txt`
    - E.g., `Unexpected admin user found: bob` → `Unexpected admin user found: [REDACTED]`
  - **Count/summary only:** If multiple sensitive items, only report a count or general description (e.g., “3 unknown admin users”).
  - **Explanations only:** Claude is prompted to explain *why* an issue is a concern in general, not details about your system.
  - **Sample Prompt (Safe):**\
    `claude -p "Explain why having unexpected admin users is a security risk on macOS."`
  - **Never send:** Real usernames, file content, emails, or other unique identifiers.

- **Code Implementation:**

  - Use regular expressions or a dedicated function to sanitize all data before sending to Claude.
  - Example:
    ```python
    def redact_sensitive_info(text):
        import re
        text = re.sub(r'/Users/[^/]+/', '/Users/[REDACTED]/', text)
        text = re.sub(r'`[^`]+`', '[REDACTED]', text)
        return text
    ```
  - Always use sanitized summaries/descriptions as the basis for Claude prompts.

- **Documentation:**

  - The README and user docs will clearly state:\
    *“No personally identifiable information is ever sent to Claude or any third-party AI. All prompts are sanitized for privacy.”*

---

## Outdated Software

- **Homebrew:** 1 package is outdated (`wget`).
  - **What it means:** Not all packages are on the latest secure version.
  - **Why important:** Outdated packages may be vulnerable. (see: [Homebrew Security](https://docs.brew.sh/Security))
  - **Suggestion:** Run `brew upgrade wget` to update.

---

## System Settings

- **Firewall:** Enabled.

  - **What it means:** Your Mac is protected from unsolicited network connections.
  - **Why important:** Disabling firewall can expose your system to attack.
  - **Reference:** [Apple Support: Firewall](https://support.apple.com/en-us/HT201642)

- **System Integrity Protection:** Enabled.

  - **What it means:** Critical system files are protected.
  - **Why important:** Prevents malware from modifying system files.

- **FileVault:** Enabled.

  - **What it means:** Your disk is encrypted.
  - **Why important:** Protects your data if your Mac is lost or stolen.
  - **Reference:** [Apple FileVault](https://support.apple.com/en-us/HT204837)

---

## Admin/User Audit

- **Admin users:** Only expected accounts found.
  - **Why important:** Unexpected admin users could indicate a compromised system.

---

## Malware Scan

- **ClamAV:** Not installed. Skipped scan.

  - **Suggestion:** Run `brew install clamav` to enable malware scanning.

- **YARA:** Installed, 0 matches found.

  - **Reference:** [What is YARA?](https://yara.readthedocs.io/)

---

*No security threats found. For any questions, see the references above.*

````

### 11.2 Security Concerns Output Example (YYYYMMDD\:HHMMSS-security\_concerns.md)

```markdown
# macsecscan Security Concerns

**Scan Date:** 2024-08-08 15:34:12

---

## Threats Found

### 1. FileVault is Disabled
- **Explanation:** FileVault is Apple’s disk encryption feature. If disabled, anyone with physical access can read your data.
- **Why it matters:** Disabling encryption exposes sensitive information to theft/loss.
- **Next Steps:** Enable FileVault in System Preferences > Security & Privacy > FileVault tab.
- **Reference:** [Apple FileVault Guide](https://support.apple.com/en-us/HT204837)

### 2. Unexpected Admin User Detected: `bob`
- **Explanation:** Admin users have full control over the system. Unexpected admin accounts could mean your system has been compromised.
- **Why it matters:** Unauthorized users with admin rights can install software, access sensitive data, or disable security features.
- **Next Steps:** Remove unknown admin users: `System Preferences > Users & Groups` or with `sudo dscl . -delete /Users/bob`.
- **Reference:** [Apple User Account Security](https://support.apple.com/en-us/HT201085)

### 3. Outdated Package: `openssl@1.1`
- **Explanation:** Outdated cryptography packages pose a major security risk.
- **Why it matters:** Vulnerabilities in outdated OpenSSL can allow attackers to eavesdrop or tamper with communications.
- **Next Steps:** Run `brew upgrade openssl@1.1` to update.
- **Reference:** [OpenSSL Security](https://www.openssl.org/news/vulnerabilities.html)

---

*Take action on the above issues as soon as possible. See references for guidance.*
````

- If no threats are found, inform the user in the CLI output ("No security threats found. Security concerns file was not created.").

