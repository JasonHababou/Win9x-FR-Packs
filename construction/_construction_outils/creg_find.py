# Lecteur minimal du registre Windows 9x (SYSTEM.DAT / USER.DAT, format CREG) :
# reconstruit les chemins de cles (RGKN) et affiche les cles dont le chemin ou une
# valeur contient le motif. Usage : creg_find.py <fichier.DAT> <motif> [...]
import struct
import sys

d = open(sys.argv[1], "rb").read()
pats = [p.lower() for p in sys.argv[2:]]
assert d[:4] == b"CREG"
RGKN = 0x20
assert d[RGKN:RGKN + 4] == b"RGKN"
root = struct.unpack_from("<I", d, RGKN + 8)[0]

# RGDB : (id, bloc) -> (nom, valeurs)
recs = {}
o = struct.unpack_from("<I", d, 8)[0]
while o < len(d) - 4 and d[o:o + 4] == b"RGDB":
    bsize = struct.unpack_from("<I", d, o + 4)[0]
    p, end = o + 0x20, o + bsize
    while p < end - 0x14:
        size, kid, blk, used, nlen, nval = struct.unpack_from("<IHHIHH", d, p)
        if size < 0x14 or p + size > end:
            break
        if used and kid != 0xFFFF:
            name = d[p + 0x14:p + 0x14 + nlen].decode("cp1252", "replace")
            q = p + 0x14 + nlen
            vals = []
            for _ in range(nval):
                vtype, _uk, vnl, vdl = struct.unpack_from("<IIHH", d, q)
                vn = d[q + 12:q + 12 + vnl].decode("cp1252", "replace")
                vd = d[q + 12 + vnl:q + 12 + vnl + vdl]
                vals.append((vn, vtype, vd))
                q += 12 + vnl + vdl
            recs[(kid, blk)] = (name, vals)
        p += size
    o += bsize

# RGKN : arbre
out = []


def walk(off, path, depth=0):
    while off != 0xFFFFFFFF and depth < 64:
        e = RGKN + off
        _u1, _h, _u2, _par, child, nxt, kid, blk = struct.unpack_from("<IIIIIIHH", d, e)
        name, vals = recs.get((kid, blk), ("?", []))
        full = f"{path}\\{name}" if path else name
        out.append((full, vals))
        if child != 0xFFFFFFFF:
            walk(child, full, depth + 1)
        off = nxt


sys.setrecursionlimit(10000)
walk(root, "")


def show(vd, t):
    if t == 1:
        return '"' + vd.rstrip(b"\0").decode("cp1252", "replace") + '"'
    if t == 4 and len(vd) == 4:
        return f"dword:{struct.unpack('<I', vd)[0]:08x}"
    return "hex:" + vd.hex(",")


for full, vals in out:
    blob = (full + " " + " ".join(vn + " " + vd.decode("cp1252", "replace") for vn, _, vd in vals)).lower()
    if any(p in blob for p in pats):
        print(f"[{full}]")
        for vn, t, vd in vals:
            print(f'  "{vn}"={show(vd, t)}')
