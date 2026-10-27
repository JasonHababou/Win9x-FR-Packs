# Cherche, dans une installation (dossier) et une image XP, toutes les versions des
# fichiers en conflit FR->EN de la 3.66 ; garde chaque version distincte.
# Usage : fr366_scan2.py <win98se> <sortie>
import csv
import shutil
import struct
import subprocess
import sys
from pathlib import Path

R, OUT = Path(sys.argv[1]), Path(sys.argv[2])
TARGETS = ["ADVPACK.DLL", "COMDLG32.DLL", "CONTROL.EXE", "CRYPTDLG.DLL", "DEFRAG.EXE", "DSKMAINT.DLL",
           "GDI.EXE", "HLINK.DLL", "HOTPLUG.DLL", "HTML32.CNV", "HYPERTRM.DLL", "KERNEL32.DLL",
           "MSJINT40.DLL", "NOTEPAD.EXE", "ODBCJI32.DLL", "REGEDIT.EXE", "SCANDSKW.EXE", "SETUPAPI.DLL",
           "SNDVOL32.EXE", "SYSMON.EXE", "SYSTRAY.EXE", "TWAIN.DLL", "TWAIN_32.DLL", "WRITE32.WPC",
           "XENROLL.DLL", "DESK.CPL"]
comp = {t[:-1] + "_": t for t in TARGETS}


def verlang(p):
    d = p.read_bytes()
    i = d.find(b"\xbd\x04\xef\xfe")
    v = "?"
    if i >= 0:
        ms, ls = struct.unpack_from("<II", d, i + 8)
        v = f"{ms >> 16}.{ms & 0xffff}.{ls >> 16}.{ls & 0xffff}"
    fr = sum(d.count(w.encode("utf-16-le")) + d.count(w.encode("cp1252"))
             for w in ("Annuler", "Fichier", "Erreur", "Impossible", "Fermer", "Aide"))
    en = sum(d.count(w.encode("utf-16-le")) for w in ("Cancel", "Error", "Unable to", "Close", "Help"))
    return v, ("FR" if fr > en else "EN" if en > fr else "?") + f"({fr}/{en})"


found = {}          # (nom, version) -> (langue, source, chemin)


def add(p, src):
    n = p.name.upper()
    if n not in TARGETS:
        return
    v, l = verlang(p)
    key = (n, v)
    if key not in found or (found[key][0].startswith("EN") and l.startswith("FR")):
        dst = OUT / src / f"{n}__{v.replace('?', 'sansversion')}"
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dst)
        found[key] = (l, src, str(p))


# 1. installation Windows Me (dossier)
for p in (R / "bkpWin98" / "SauvegardeWinME").rglob("*"):
    if p.is_file() and p.name.upper() in TARGETS:
        add(p, "ME_INSTALL")
# 2. nouvelle image XP
iso = R / "ISO" / "WindowsXP" / "Windows XP professional SP3 x86.iso"
tmp = OUT / "_xp2"
subprocess.run(["7z", "e", "-y", f"-o{tmp}", str(iso), *[f"I386/{t}" for t in TARGETS],
                *[f"I386/{c}" for c in comp]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
for p in list(tmp.glob("*")):
    if p.name.upper() in comp:
        x = OUT / "_xp2x"
        subprocess.run(["7z", "e", "-y", f"-o{x}", str(p)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for q in x.glob("*"):
            add(q, "XP_SP3_x86")
    else:
        add(p, "XP_SP3_x86")

rows = {r["Fichier"].upper(): r for r in csv.DictReader(open(R / "Sources/AfterLife Fr/listingExtrait/etude366_fichiers.csv", encoding="utf-8-sig"))}
for n in TARGETS:
    v366 = rows.get(n, {}).get("V366", "")
    hits = [(v, *found[(nn, v)]) for (nn, v) in found if nn == n]
    tag = " <== MEME VERSION" if any(v == v366 and l.startswith("FR") for v, l, *_ in hits) else ""
    print(f"{n:13} 3.66={v366:17}{tag}")
    for v, l, src, path in sorted(hits):
        print(f"     {'=' if v == v366 else ' '} {v:18} {l:12} {src:11} {path[-70:]}")
