# Report des corrections 3.66 sur un executable 16 bits (NE) francais.
#   P = diff(base FR, 3.66) par segment ; controle de langue : diff(EN ref, FR ref)
#   (references de meme numero, ex. 2222) aux memes offsets doit etre vide.
# Usage : port366ne.py <base_fr> <fichier_366> <en_ref> <fr_ref> <sortie>
import struct
import sys
from pathlib import Path


def segs(d):
    ne = struct.unpack_from("<I", d, 0x3C)[0]
    assert d[ne:ne + 2] == b"NE"
    cnt = struct.unpack_from("<H", d, ne + 0x1C)[0]
    off = struct.unpack_from("<H", d, ne + 0x22)[0]
    sh = struct.unpack_from("<H", d, ne + 0x32)[0]
    return [((so << sh), (sl or 0x10000)) for so, sl, fl, mn in
            (struct.unpack_from("<HHHH", d, ne + off + 8 * i) for i in range(cnt))]


B, S, EN, FR = (Path(a).read_bytes() for a in sys.argv[1:5])
out = Path(sys.argv[5])
sb, ss, se, sf = segs(B), segs(S), segs(EN), segs(FR)
new = bytearray(B)
ok, total = True, 0
for i, ((ob, lb), (os_, ls)) in enumerate(zip(sb, ss)):
    if lb != ls:
        print(f"segment {i + 1} : tailles differentes {lb}/{ls} -> refus")
        ok = False
        continue
    p = [k for k in range(lb) if B[ob + k] != S[os_ + k]]
    if not p:
        continue
    (oe, le), (of, lf) = se[i], sf[i]
    lang = [k for k in p if k < min(le, lf) and EN[oe + k] != FR[of + k]]
    print(f"segment {i + 1} : correctif {len(p)} octets, dont {len(lang)} a des offsets ou EN et FR different")
    if lang:
        ok = False
        continue
    for k in p:
        new[ob + k] = S[os_ + k]
    total += len(p)
if ok:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(bytes(new))
    print(f"=> ecrit {out.name} ({total} octets reportes)")
else:
    print("=> REFUSE")
