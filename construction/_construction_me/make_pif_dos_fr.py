# Mode MS-DOS de Windows ME FR : PIF francais generes a partir du "Exit to DOS" de TPC
# (MS-DOS mode + "Specifier une nouvelle configuration", seul cas qui marche sous ME).
# Chaque PIF a son CONFIG.SYS / AUTOEXEC.BAT : clavier AZERTY (KEYB.COM FR de la
# disquette de demarrage, C:\WINDOWS\COMMAND\EBD), CD-ROM (OAKCDROM.SYS + MSCDEX),
# pays France. Les PIF "jeux" ajoutent EMM386 (avec IO8EMMOK, indispensable sous ME
# dont l'IO.SYS contient deja le pilote XMS : HIMEM.SYS refuse de se charger).
# Usage : make_pif_dos_fr.py <exit_dos.pi_ de TPC> <dossier de sortie>
import struct
import sys
from pathlib import Path

modele = Path(sys.argv[1]).read_bytes()
SORTIE = Path(sys.argv[2])
EBD = r"C:\WINDOWS\COMMAND\EBD"


def sections(d):
    o, res = 0x171, []
    while True:
        nom = d[o:o + 16]
        suiv, off, t = struct.unpack_from("<HHH", d, o + 16)
        res.append([nom, d[off:off + t]])
        if suiv in (0xFFFF, 0):
            return res
        o = suiv


def construire(base, secs):
    out = bytearray(base[:0x171])
    pos = 0x171
    for i, (nom, data) in enumerate(secs):
        dernier = i == len(secs) - 1
        if nom.startswith(b"MICROSOFT PIFEX"):
            suiv = 0xFFFF if dernier else pos + 22
            out += nom + struct.pack("<HHH", suiv, 0, 0x171)
            pos += 22
        else:
            suiv = 0xFFFF if dernier else pos + 22 + len(data)
            out += nom + struct.pack("<HHH", suiv, pos + 22, len(data)) + data
            pos += 22 + len(data)
    return bytes(out)


def champ(d, off, n, texte, pad=b"\0"):
    b = texte.encode("cp850")[:n]
    d[off:off + n] = b + pad * (n - len(b))


def pif(titre, config, autoexec):
    base = bytearray(modele[:0x171])
    champ(base, 0x02, 30, titre, b" ")              # titre (30 car., complete d'espaces)
    secs = sections(modele)
    for s in secs:
        if s[0].startswith(b"AUTOEXECBAT 4.0"):
            s[1] = ("\r\n".join(autoexec) + "\r\n").encode("cp850")
        elif s[0].startswith(b"CONFIG  SYS 4.0"):
            s[1] = ("\r\n".join(config) + "\r\n").encode("cp850")
    return construire(bytes(base), secs)


ENV = [r"SET winbootdir=C:\WINDOWS", r"SET WINBOOTDIR=C:\WINDOWS",
       r"SET PATH=C:\WINDOWS;C:\WINDOWS\COMMAND", "SET PROMPT=$p$g",
       r"SET TEMP=C:\WINDOWS\TEMP", r"SET TMP=C:\WINDOWS\TEMP"]
# KEYB FR (copie de C:\WINDOWS\COMMAND\EBD\KEYB.COM), CD (MSCDEX), souris (CuteMouse FR)
PERIPH = [r"C:\WINDOWS\KEYB.COM FR,,C:\WINDOWS\COMMAND\KEYBOARD.SYS",
          r"LH C:\WINDOWS\COMMAND\MSCDEX.EXE /D:MSCD001",
          r"LH C:\WINDOWS\CTMOUSE.EXE"]
PAYS = r"COUNTRY=033,850,C:\WINDOWS\COMMAND\COUNTRY.SYS"
# CD-ROM : UIDE (Jack R. Ellis) ; OAKCDROM bloquait avec EMM386 (test QEMU 2026-10-20)
CDROM = r"DEVICEHIGH=C:\WINDOWS\UIDE.SYS /D:MSCD001 /S5"
EMM = r"DEVICE=C:\WINDOWS\IO8EMMOK.SYS"
MSG = ["ECHO.", "ECHO Mode MS-DOS de Windows Millennium. Tapez EXIT pour revenir a Windows.", "ECHO."]

SORTIE.mkdir(exist_ok=True)
fichiers = {
    # "Redemarrer en mode MS-DOS" (menu Arreter) : EMS + XMS + memoire superieure
    "EXIT_DOS.PI_": pif("Commandes MS-DOS",
                        ["DOS=HIGH,UMB", EMM, r"DEVICE=C:\WINDOWS\EMM386.EXE RAM", CDROM, PAYS],
                        ENV + PERIPH + MSG),
    # jeux DOS : XMS seule (EMM386 NOEMS pour la memoire superieure)
    "JEUXXMS.PI_": pif("Mode MS-DOS pour jeux (XMS)",
                       ["DOS=HIGH,UMB", EMM, r"DEVICE=C:\WINDOWS\EMM386.EXE NOEMS", CDROM, PAYS],
                       ENV + PERIPH + MSG),
    # jeux qui refusent EMM386 : ni EMM386 ni memoire superieure
    "JEUXSANS.PI_": pif("Mode MS-DOS sans EMM386",
                        ["DOS=HIGH", CDROM.replace("DEVICEHIGH", "DEVICE"), PAYS],
                        ENV + [x.replace("LH ", "") for x in PERIPH] + MSG),
}
for n, d in fichiers.items():
    (SORTIE / n).write_bytes(d)
    print(n, len(d))
