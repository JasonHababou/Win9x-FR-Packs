# Petit disque FAT16 partitionne (64 Mo) avec le contenu d'un dossier, pour une VM DOS.
# Usage : mk_regdisk.py <dossier> <image>   |   mk_regdisk.py --lire <image> <fichier> <dest>
import struct
import sys
from pathlib import Path

from pyfatfs.PyFat import PyFat
from pyfatfs.PyFatFS import PyFatFS

OFF = 63 * 512
if sys.argv[1] == "--lire":
    f = PyFatFS(sys.argv[2], offset=OFF, encoding="cp850")
    with f.openbin("/" + sys.argv[3], "r") as s:
        Path(sys.argv[4]).write_bytes(s.read())
    f.close()
    print("ok", sys.argv[3])
    sys.exit()
src, img = Path(sys.argv[1]), sys.argv[2]
taille = 64 * 2**20
nsect = taille // 512 - 63
mbr = bytearray(512)
# entree 1 : active, CHS factices, type 06 (FAT16 > 32 Mo), LBA 63
mbr[446:462] = bytes([0x80, 1, 1, 0, 0x06, 0xFE, 0xFF, 0xFF]) + struct.pack("<II", 63, nsect)
mbr[510:512] = b"\x55\xaa"
with open(img, "wb") as f:
    f.write(mbr)
    f.truncate(taille)
pf = PyFat(offset=OFF)
pf.mkfs(img, PyFat.FAT_TYPE_FAT16, size=nsect * 512, label="REGJOB")
pf.close()
# champ "secteurs caches" du BPB = 63 (debut de la partition)
with open(img, "r+b") as f:
    f.seek(OFF + 28)
    f.write(struct.pack("<I", 63))
fs = PyFatFS(img, offset=OFF, encoding="cp850")
for p in sorted(src.iterdir()):
    if p.is_file():
        with fs.openbin("/" + p.name.upper(), "w") as d:
            d.write(p.read_bytes())
print(fs.listdir("/"))
fs.close()
