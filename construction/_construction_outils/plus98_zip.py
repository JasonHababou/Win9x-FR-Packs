# Plus! 98 FR du pack : Dossiers compresses a jour DANS l'installeur.
# Remplace ZIPFLDR.DLL / DZIP32.DLL / DUNZIP32.DLL de PLUS98.CAB par les versions
# du correctif Q329048 (SP3.0 FR, 06_OPTS), recompresse le CAB (MSZIP, meme ordre
# de fichiers) et met a jour taille + somme (16 bits bas du CRC32) dans LAYOUTP.INF.
# Usage : plus98_zip.py <dossier plus98 du pack> <dossier 06_OPTS> <dossier de travail>
import shutil
import subprocess
import sys
import zlib
from pathlib import Path

P98, OPTS, W = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
CAB, LAY = P98 / "PLUS98.CAB", P98 / "LAYOUTP.INF"
NEW = ["ZIPFLDR.DLL", "DZIP32.DLL", "DUNZIP32.DLL"]

if W.exists():
    shutil.rmtree(W)
(W / "x").mkdir(parents=True)

# Ordre et noms exacts des fichiers du CAB d'origine
out = subprocess.run(["7z", "l", "-slt", str(CAB)], capture_output=True, text=True,
                     encoding="utf-8", errors="replace", check=True).stdout
names = [l[7:] for l in out.splitlines() if l.startswith("Path = ")][1:]
assert len(names) == 1678 and len(set(n.upper() for n in names)) == len(names), len(names)
assert all("\\" not in n and "/" not in n for n in names)
subprocess.run(["7z", "x", "-y", "-o" + str(W / "x"), str(CAB)], check=True, stdout=subprocess.DEVNULL)

upper = {n.upper(): n for n in names}
for f in NEW:
    dst = W / "x" / upper[f]
    shutil.copy2(OPTS / f, dst)

# Recompression : un seul CAB, MSZIP comme l'original
ddf = [".OPTION EXPLICIT", ".Set CabinetNameTemplate=PLUS98.CAB", ".Set DiskDirectoryTemplate=" + str(W / "cab"),
       ".Set Cabinet=on", ".Set Compress=on", ".Set CompressionType=MSZIP", ".Set MaxDiskSize=0",
       ".Set CabinetFileCountThreshold=0", ".Set FolderFileCountThreshold=0", ".Set FolderSizeThreshold=0",
       ".Set MaxCabinetSize=0", ".Set UniqueFiles=on", ".Set RptFileName=NUL", ".Set InfFileName=NUL"]
ddf += ['"%s" "%s"' % (W / "x" / n, n) for n in names]
(W / "plus98.ddf").write_text("\r\n".join(ddf) + "\r\n", encoding="cp1252")
subprocess.run(["makecab", "/F", str(W / "plus98.ddf")], check=True, stdout=subprocess.DEVNULL)
newcab = W / "cab" / "PLUS98.CAB"

# Controle : memes noms, memes contenus sauf les 3 DLL
chk = W / "chk"
subprocess.run(["7z", "x", "-y", "-o" + str(chk), str(newcab)], check=True, stdout=subprocess.DEVNULL)
got = sorted(p.name for p in chk.iterdir())
assert got == sorted(names), "liste de fichiers differente"
for n in names:
    a, b = (W / "x" / n).read_bytes(), (chk / n).read_bytes()
    assert a == b, n

# LAYOUTP.INF : taille et somme
t = LAY.read_bytes().decode("cp1252")
for f in NEW:
    d = (OPTS / f).read_bytes()
    lines = [l for l in t.split("\r\n") if l.upper().startswith(f + "=")]
    assert len(lines) == 1, f
    parts = lines[0].split(",")
    parts[2], parts[3] = str(len(d)), "%x" % (zlib.crc32(d) & 0xFFFF)
    t = t.replace(lines[0], ",".join(parts))
    print(f, lines[0], "->", ",".join(parts))
(W / "LAYOUTP.INF").write_bytes(t.encode("cp1252"))
print("CAB :", CAB.stat().st_size, "->", newcab.stat().st_size)
