# Compare section par section deux PE (taille, octets differents, premieres plages).
import struct
import sys
from pathlib import Path


def secs(p):
    d = p.read_bytes()
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    n = struct.unpack_from("<H", d, pe + 6)[0]
    osz = struct.unpack_from("<H", d, pe + 20)[0]
    out = {}
    for i in range(n):
        o = pe + 24 + osz + 40 * i
        name = d[o:o + 8].rstrip(b"\0").decode("latin-1")
        vs, va, rs, raw = struct.unpack_from("<IIII", d, o + 8)
        out[name] = (va, d[raw:raw + rs])
    return out


a, b = secs(Path(sys.argv[1])), secs(Path(sys.argv[2]))
for k in a:
    if k not in b:
        print(k, "absente du 2e")
        continue
    (va1, x), (va2, y) = a[k], b[k]
    n = min(len(x), len(y))
    diff = [i for i in range(n) if x[i] != y[i]]
    ranges = []
    for i in diff:
        if ranges and i - ranges[-1][1] <= 8:
            ranges[-1][1] = i
        else:
            ranges.append([i, i])
    print(f"{k:8} VA {va1:#x}/{va2:#x} tailles {len(x)}/{len(y)} octets differents {len(diff)} "
          f"plages {len(ranges)} : {[(hex(va1 + r[0]), r[1] - r[0] + 1) for r in ranges[:12]]}")
