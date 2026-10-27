# Prepare le dossier regjob : SLOW.REG / FAST.REG = exactement le tmp.reg de
# sysprep.registry_add_reg (reg + 2 lignes ajoutees en mode texte Windows -> CRLF)
import sys
from pathlib import Path

F, J = Path(sys.argv[1]), Path(sys.argv[2])
ajout = ('[HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce]\r\n'
         '"QiSetup"="C:\\\\QISETUP.EXE"\r\n\r\n').encode("ascii")
for src, dst in (("slowpnp.reg", "SLOW.REG"), ("fastpnp.reg", "FAST.REG")):
    (J / dst).write_bytes((F / "registry" / src).read_bytes() + ajout)
(J / "JOB.BAT").write_bytes(b"copy SYSTEM.DAT S1.DAT\r\nREGEDIT /L:S1.DAT /R:S1.DAT SLOW.REG\r\n"
                            b"copy SYSTEM.DAT S2.DAT\r\nREGEDIT /L:S2.DAT /R:S2.DAT FAST.REG\r\ndir\r\n")
print((J / "SLOW.REG").read_bytes()[-90:])
