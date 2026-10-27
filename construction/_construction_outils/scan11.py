# Decompresse recursivement des paquets (7z : exe/cab/zip/msi) et cherche les 11 fichiers
# restes anglais ; affiche version + langue (mots FR/EN dans les ressources).
# Usage : scan11.py <sortie> <paquet ou dossier>...
import re
import struct
import subprocess
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
NAMES = {"COMDLG32.DLL", "CONTROL.EXE", "NOTEPAD.EXE", "REGEDIT.EXE", "SNDVOL32.EXE", "SYSMON.EXE",
         "GDI.EXE", "KERNEL32.DLL", "SYSTRAY.EXE", "HOTPLUG.DLL", "WRITE32.WPC"}
ARCH = re.compile(r"(?i)\.(exe|cab|zip|7z|msi|rar)$")
COMP = {n[:-1] + "_" for n in NAMES}


def ver(d):
    i = d.find(b"\xbd\x04\xef\xfe")
    if i < 0:
        return "?"
    ms, ls = struct.unpack_from("<II", d, i + 8)
    return f"{ms >> 16}.{ms & 0xffff}.{ls >> 16}.{ls & 0xffff}"


def lang(d):
    fr = sum(d.count(w.encode("utf-16-le")) + d.count(w.encode("cp1252"))
             for w in ("Annuler", "Fichier", "Erreur", "Impossible", "Fermer", "Aide", "Affichage", "Volume"))
    en = sum(d.count(w.encode("utf-16-le")) + d.count(w.encode("cp1252"))
             for w in ("Cancel", "Error", "Unable to", "Close", "Help", "View"))
    return f"FR{fr}/EN{en}"


seen = set()


def scan(path, label, depth=0):
    for p in sorted(path.rglob("*")) if path.is_dir() else [path]:
        if not p.is_file():
            continue
        n = p.name.upper()
        if n in NAMES:
            d = p.read_bytes()
            key = (n, ver(d), len(d))
            if key not in seen:
                seen.add(key)
                print(f"{n:13} {ver(d):16} {lang(d):10} {label} :: {p.relative_to(OUT) if OUT in p.parents else p.name}")
        elif depth < 4 and (ARCH.search(n) or n in COMP) and p.stat().st_size > 1000:
            x = OUT / f"x{abs(hash(str(p))) % 10**9}"
            if x.exists():
                continue
            r = subprocess.run(["7z", "x", "-y", f"-o{x}", str(p)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if x.exists():
                scan(x, f"{label} > {p.name}", depth + 1)


for a in sys.argv[2:]:
    scan(Path(a), Path(a).name)
print("fin")
