# CD de transfert pour une VM : contenu d'un ou plusieurs dossiers a la racine, noms longs
# (Joliet) + noms ISO 9660 NOM.EXT lisibles sous DOS (MSCDEX). Comme make_jeux_iso.py,
# sans les jeux ni Glide.
# Usage : make_cd.py <sortie.iso> <etiquette> <dossier | NOM=dossier | fichier> [...]
import sys
from pathlib import Path

import pycdlib

# ISO_NIVEAU=4 (ISO 9660:1999) : plus de limite de 8 niveaux de dossiers (source XP :
# I386\ASMS\52\POLICY\...), mais XP lit alors les noms ISO et non Joliet -> noms reels gardes
NIVEAU = int(__import__("os").environ.get("ISO_NIVEAU", 3))
iso = pycdlib.PyCdlib()
iso.new(interchange_level=NIVEAU, joliet=3, vol_ident=sys.argv[2][:32])
noms = {}


def nom9660(parent, nom, fichier):
    if NIVEAU == 4:
        return nom
    propre = lambda x: "".join(c if (c.isascii() and c.isalnum()) or c == "_" else "_" for c in x.upper())
    if fichier and "." in nom:
        b, e = nom.rsplit(".", 1)
        s = (propre(b)[:26] or "X") + "." + propre(e)[:3]
    else:
        s = propre(nom)[:30] or "X"
    pris = noms.setdefault(parent, set())
    base, k = s, 1
    while s in pris:
        s, k = f"{base[:24]}_{k}", k + 1
    pris.add(s)
    return s


def ajoute(src, dest_iso, dest_jol):
    for p in sorted(src.iterdir()):
        n = nom9660(dest_iso, p.name, not p.is_dir())
        if p.is_dir():
            iso.add_directory(f"{dest_iso}/{n}", joliet_path=f"{dest_jol}/{p.name}")
            ajoute(p, f"{dest_iso}/{n}", f"{dest_jol}/{p.name}")
        else:
            iso.add_file(str(p), f"{dest_iso}/{n};1", joliet_path=f"{dest_jol}/{p.name}")


for d in sys.argv[3:]:
    if "=" in d:                               # NOM=dossier : place dans \NOM
        nom, src = d.split("=", 1)
        n = nom9660("", nom, False)
        iso.add_directory(f"/{n}", joliet_path=f"/{nom}")
        ajoute(Path(src), f"/{n}", f"/{nom}")
    elif Path(d).is_file():                    # fichier seul : a la racine
        iso.add_file(d, f"/{nom9660('', Path(d).name, True)};1", joliet_path=f"/{Path(d).name}")
    else:                                      # dossier : son contenu a la racine
        ajoute(Path(d), "", "")
iso.write(sys.argv[1])
iso.close()
print("ok", Path(sys.argv[1]).stat().st_size // 2**20, "Mo")
