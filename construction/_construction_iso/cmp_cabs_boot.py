# Compare le contenu complet des CAB du dossier WIN98 entre win98se.iso (original)
# et "Windows 98 Se Fr Bootable.iso" : fichiers ajoutes / retires / modifies.
# Les CAB de Windows 98 sont chaines (BASE4 -> BASE5 -> BASE6...) : on extrait
# tous les CAB puis chaque chaine depuis son premier volume.
import shutil
import struct
import subprocess
import sys
from pathlib import Path

ISO = Path(r"<DOSSIER_WINDOWS>\win98se\ISO\Windows98")
SRC = {"orig": ISO / "win98se.iso", "boot": ISO / "Windows 98 Se Fr Bootable.iso"}
W = Path(sys.argv[1])
if W.exists():
    shutil.rmtree(W)


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


arbres = {}
for tag, iso in SRC.items():
    cab = W / tag / "cab"
    cab.mkdir(parents=True)
    subprocess.run(["7z", "e", "-y", "-o" + str(cab), str(iso), "win98/*.CAB", "win98/*.cab"],
                   check=True, stdout=subprocess.DEVNULL)
    out = W / tag / "x"
    out.mkdir()
    noms = sorted(p.name for p in cab.iterdir())
    # premiers volumes : ceux dont le CAB precedent (numero - 1) n'existe pas
    for n in noms:
        u = n.upper()
        stem = u[:-4].rstrip("0123456789")
        num = u[len(stem):-4]
        if num and any(x.upper() == f"{stem}{int(num) - 1}.CAB" for x in noms):
            continue
        r = subprocess.run(["7z", "x", "-y", "-o" + str(out), str(cab / n)], capture_output=True, text=True)
        if r.returncode:
            print(tag, n, "ERREUR", r.stdout[-200:])
    arbres[tag] = {p.name.upper(): p for p in out.rglob("*") if p.is_file()}
    print(tag, len(arbres[tag]), "fichiers")

a, b = arbres["orig"], arbres["boot"]
print("retires :", sorted(set(a) - set(b)))
for n in sorted(set(b) - set(a)):
    v, l = verlang(b[n])
    print(f"+ ajoute  {n:16} {b[n].stat().st_size:>9} {v} {l}")
for n in sorted(set(a) & set(b)):
    if a[n].read_bytes() != b[n].read_bytes():
        va, la = verlang(a[n])
        vb, lb = verlang(b[n])
        print(f"* modifie {n:16} {a[n].stat().st_size:>9} {va} {la}  ->  {b[n].stat().st_size:>9} {vb} {lb}")
