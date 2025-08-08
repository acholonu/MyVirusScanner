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

* The `--rules` flag points to this folder.
* The `--path` flag specifies which directory to scan.

---

## Adding Your Own Rules

* To add your own rules, simply drop `.yar` or `.yara` files into this folder.
* Check out the [YARA documentation](https://yara.readthedocs.io/) to learn more about writing rules.

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

*Note: filepath matching requires scanning tools that support the `filepath` variable, such as newer YARA versions.*

---

## Contributing Rules

If you create a useful rule, consider submitting it upstream or sharing with the security community!

* See [YARA Rules Repository](https://github.com/YARA-Rules/rules) for community-maintained rules.

---

## Disclaimer

These rules are for demonstration and educational purposes.
Detection results may include **false positives**. Always review matches carefully.

---

Happy hunting!
The macsecscan Team

```

---

Let me know if you want **more sample rules**, or a template for community contribution, or help with rule writing!
```
