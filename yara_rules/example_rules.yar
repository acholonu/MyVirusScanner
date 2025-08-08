rule Suspicious_Mac_Executables
{
    meta:
        description = "Detects Mach-O executables and common shell scripts"
        author = "macsecscan"
    strings:
        $macho = { CF FA ED FE }
        $sh = "#!/bin/sh"
        $bash = "#!/bin/bash"
    condition:
        any of them
}

