# Plus! 98 FR du pack : masque les composants retires du CAB (installation ET
# Ajout/Suppression). INSTALL.EXE construit la liste des composants a partir des
# cles HKLM\Software\Microsoft\Plus!98\Setup\<composant> ecrites par la section
# [Components.Reg] de PLUS98.INF : on y retire les 7 composants. PLUS98.INF est
# modifie a la racine ET dans PLUS98.CAB (copie posee dans WINDOWS\INF, utilisee
# par Ajout/Suppression), LAYOUTP.INF mis a jour (taille + CRC32 bas), lignes
# correspondantes retirees de MSBATCH.INF.
# Usage : plus98_masque.py <dossier plus98 du pack> <dossier de travail>
import shutil
import subprocess
import sys
import zlib
from pathlib import Path

P98, W = Path(sys.argv[1]), Path(sys.argv[2])
CAB = P98 / "PLUS98.CAB"
CLES = ["WebCD", "Tuneup", "PIE", "LYM", "Viruscan", "Golf", "OA"]
NOMS = ["Golf 1998 Lite", "Lose Your Marbles", "Picture It! Express", "Écran de veille Organic Art",
        "VirusScan", "Lecteur CD Deluxe", "Assistant Maintenance"]


def masque(b):
    t = b.decode("cp1252")
    n = 0
    for k in CLES:
        for champ in ("INF", "Section"):
            l = "HKLM,%%KEY_PLUS98%%\\Setup\\%s,%s,," % (k, champ)
            lignes = [x for x in t.split("\r\n") if x.startswith(l)]
            assert len(lignes) == 1, (k, champ, lignes)
            t = t.replace(lignes[0] + "\r\n", "")
            n += 1
    assert n == 14
    return t.encode("cp1252")


if W.exists():
    shutil.rmtree(W)
(W / "x").mkdir(parents=True)
out = subprocess.run(["7z", "l", "-slt", str(CAB)], capture_output=True, text=True,
                     encoding="utf-8", errors="replace", check=True).stdout
names = [l[7:] for l in out.splitlines() if l.startswith("Path = ")][1:]
subprocess.run(["7z", "x", "-y", "-o" + str(W / "x"), str(CAB)], check=True, stdout=subprocess.DEVNULL)
inf_cab = W / "x" / next(n for n in names if n.upper() == "PLUS98.INF")
assert inf_cab.read_bytes() == (P98 / "PLUS98.INF").read_bytes()
nouv = masque(inf_cab.read_bytes())
inf_cab.write_bytes(nouv)

ddf = [".OPTION EXPLICIT", ".Set CabinetNameTemplate=PLUS98.CAB", ".Set DiskDirectoryTemplate=" + str(W / "cab"),
       ".Set Cabinet=on", ".Set Compress=on", ".Set CompressionType=MSZIP", ".Set MaxDiskSize=0",
       ".Set CabinetFileCountThreshold=0", ".Set FolderFileCountThreshold=0", ".Set FolderSizeThreshold=0",
       ".Set MaxCabinetSize=0", ".Set UniqueFiles=on", ".Set RptFileName=NUL", ".Set InfFileName=NUL"]
ddf += ['"%s" "%s"' % (W / "x" / n, n) for n in names]
(W / "p.ddf").write_text("\r\n".join(ddf) + "\r\n", encoding="cp1252")
subprocess.run(["makecab", "/F", str(W / "p.ddf")], check=True, stdout=subprocess.DEVNULL)
chk = W / "chk"
subprocess.run(["7z", "x", "-y", "-o" + str(chk), str(W / "cab" / "PLUS98.CAB")], check=True, stdout=subprocess.DEVNULL)
assert sorted(p.name for p in chk.iterdir()) == sorted(names)
for n in names:
    assert (chk / n).read_bytes() == (W / "x" / n).read_bytes(), n

# LAYOUTP.INF
lay = (P98 / "LAYOUTP.INF").read_bytes().decode("cp1252")
l = [x for x in lay.split("\r\n") if x.upper().startswith("PLUS98.INF=")]
assert len(l) == 2, l          # disque 0 (racine) et disque 1 (dans le CAB)
for x in l:
    p = x.split(",")
    p[2], p[3] = str(len(nouv)), "%x" % (zlib.crc32(nouv) & 0xFFFF)
    lay = lay.replace(x, ",".join(p))
    print(x, "->", ",".join(p))

# MSBATCH.INF
mb = (P98 / "MSBATCH.INF").read_bytes().decode("cp1252")
sep = "\r\n" if "\r\n" in mb else "\n"
for nom in NOMS:
    lignes = [x for x in mb.split(sep) if x.startswith('"%s"=' % nom)]
    assert len(lignes) == 1, nom
    mb = mb.replace(lignes[0] + sep, "")

(W / "PLUS98.INF").write_bytes(nouv)
(W / "LAYOUTP.INF").write_bytes(lay.encode("cp1252"))
(W / "MSBATCH.INF").write_bytes(mb.encode("cp1252"))
print("ok, CAB", (W / "cab" / "PLUS98.CAB").stat().st_size)
