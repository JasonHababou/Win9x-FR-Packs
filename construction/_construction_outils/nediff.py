# Compare deux executables 16 bits (NE) segment par segment.
import struct
import sys
from pathlib import Path


def segs(d):
    ne = struct.unpack_from("<I", d, 0x3C)[0]
    if d[ne:ne + 2] != b"NE":
        return None
    cnt = struct.unpack_from("<H", d, ne + 0x1C)[0]
    off = struct.unpack_from("<H", d, ne + 0x22)[0]
    sh = struct.unpack_from("<H", d, ne + 0x32)[0]
    out = []
    for i in range(cnt):
        so, sl, fl, mn = struct.unpack_from("<HHHH", d, ne + off + 8 * i)
        out.append((so << sh, sl or 0x10000, fl))
    return out


a, b = Path(sys.argv[1]), Path(sys.argv[2])
da, db = a.read_bytes(), b.read_bytes()
sa, sb = segs(da), segs(db)
print(f"{a.name} {len(da)} / {b.name} {len(db)}  NE: {sa is not None}/{sb is not None}")
if sa and sb:
    tot = 0
    for i, ((oa, la, fa), (ob, lb, fb)) in enumerate(zip(sa, sb)):
        n = min(la, lb)
        diff = sum(1 for k in range(n) if da[oa + k] != db[ob + k])
        if diff or la != lb:
            print(f"   segment {i + 1}: tailles {la}/{lb}, octets differents {diff}")
        tot += diff
    print(f"   {len(sa)}/{len(sb)} segments, total octets differents dans le code/donnees : {tot}")
