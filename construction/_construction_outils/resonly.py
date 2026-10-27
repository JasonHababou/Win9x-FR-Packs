import struct
import sys
from pathlib import Path

for p in map(Path, sys.argv[1:]):
    d = p.read_bytes()
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    n = struct.unpack_from("<H", d, pe + 6)[0]
    osz = struct.unpack_from("<H", d, pe + 20)[0]
    secs = []
    for i in range(n):
        o = pe + 24 + osz + 40 * i
        secs.append((d[o:o + 8].rstrip(b"\0").decode(), struct.unpack_from("<I", d, o + 16)[0]))
    imp = struct.unpack_from("<I", d, pe + 24 + 104)[0]
    print(f"{p.name[:34]:34} {secs} {'avec imports' if imp else 'AUCUN import (ressources seules)'}")
