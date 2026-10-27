# Candidats a l'integration (slipstream) dans les CAB de Windows 98 SE FR :
# fichiers du SP3.0 FR (SP2.CAB = remplacements systeme) presents dans les CAB du CD,
# avec version plus recente et langue compatible.
import subprocess
import sys
from pathlib import Path

import struct

def verlang(p):
    d = p.read_bytes()
    i = d.find("VS_VERSION_INFO".encode("utf-16-le"))
    if i < 0:
        return "", ""
    j = d.find(b"\xbd\x04\xef\xfe", i)
    ver = ""
    if 0 < j - i < 200:
        ms, ls = struct.unpack_from("<II", d, j + 8)
        ver = f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"
    lang = ""
    k = d.find("Translation".encode("utf-16-le"), i)
    if k > 0:
        k += len("Translation".encode("utf-16-le"))
        while k < len(d) and d[k] == 0:
            k += 1
        k = (k + 3) & ~3
        if k + 2 <= len(d):
            lid = struct.unpack_from("<H", d, k)[0]
            lang = {0x40C: "FR", 0x409: "EN", 0: "neutre"}.get(lid, hex(lid))
    return ver, lang

W = Path(sys.argv[1])          # dossier de travail (cabboot\boot\x = CD Bootable extrait)
CD = W / "boot" / "x"
SP = Path(r"<DOSSIER_WINDOWS>\win98se\Win98FR_v3\02_SP30")
X = W / "sp30"
if not X.exists():
    for c in ("SP2.CAB", "SUPP.CAB", "ADDITIONS.CAB"):
        subprocess.run(["7z", "x", "-y", "-o" + str(X / c), str(SP / c)], check=True, stdout=subprocess.DEVNULL)
cd = {p.name.upper(): p for p in CD.rglob("*") if p.is_file()}


def vk(v):
    return tuple(int(x) for x in v.split(".")) if v else ()


stats = {}
lignes = []
for c in ("SP2.CAB", "SUPP.CAB", "ADDITIONS.CAB"):
    for f in sorted((X / c).rglob("*")):
        if not f.is_file():
            continue
        n = f.name.upper()
        if n not in cd:
            stats[(c, "absent du CD")] = stats.get((c, "absent du CD"), 0) + 1
            continue
        vs, ls = verlang(f)
        vc, lc = verlang(cd[n])
        if f.read_bytes() == cd[n].read_bytes():
            etat = "identique"
        elif vs and vc and vk(vs) < vk(vc):
            etat = "SP plus ancien"
        elif ls == "EN" and lc == "FR":
            etat = "SP anglais / CD francais"
        else:
            etat = "A INTEGRER"
        stats[(c, etat)] = stats.get((c, etat), 0) + 1
        lignes.append(f"{c:13} {n:14} CD {vc:16} {lc:6} SP {vs:16} {ls:6} {etat}")
for k, v in sorted(stats.items()):
    print(k, v)
print()
print("\n".join(l for l in lignes if "A INTEGRER" in l))
print()
print("\n".join(l for l in lignes if "anglais" in l or "ancien" in l))
