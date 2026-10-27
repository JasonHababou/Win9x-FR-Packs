# Reporte les corrections de U98SESP3.66 sur la version FRANCAISE d'un fichier PE.
#   correctif P  = octets qui different entre l'original EN et le fichier 3.66
#   langue    L  = octets qui different entre l'original EN et l'original FR
# Conditions : memes sections (VA, taille brute) hors .rsrc ; P n'intersecte pas L ;
# le FR est identique a l'EN sur P. Alors FR_nouveau = FR + octets 3.66 sur P.
# Les sections .rsrc (textes FR) ne sont jamais touchees ; .idata : seulement si P y touche
# (alors refus, a examiner a la main).
# Usage : port366.py <en_orig> <fr_orig> <fichier_366> <sortie> [--base-fr]
#   --base-fr : pas d'original EN du meme numero ; P = diff(FR, 3.66) et on verifie
#               seulement que les sections modifiees sont hors .rsrc/.idata.
import struct
import sys
from pathlib import Path

SKIP = (".rsrc",)


def sections(d):
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    assert d[pe:pe + 4] == b"PE\0\0"
    n = struct.unpack_from("<H", d, pe + 6)[0]
    osz = struct.unpack_from("<H", d, pe + 20)[0]
    out = []
    for i in range(n):
        o = pe + 24 + osz + 40 * i
        name = d[o:o + 8].rstrip(b"\0").decode("latin-1")
        vs, va, rs, raw = struct.unpack_from("<IIII", d, o + 8)
        out.append((name, va, rs, raw))
    return out


def diffs(a, b, sa, sb):
    out = {}
    for (n1, va1, rs1, raw1), (n2, va2, rs2, raw2) in zip(sa, sb):
        if n1.lower().startswith(SKIP):
            continue
        if n1.lower().startswith(".reloc"):          # placee apres .rsrc : seule l'adresse bouge
            assert (n1, rs1) == (n2, rs2), f"sections differentes : {n1} {rs1}/{rs2}"
        else:
            assert (n1, va1, rs1) == (n2, va2, rs2), f"sections differentes : {n1} {va1:#x}/{va2:#x} {rs1}/{rs2}"
        out[n1] = {k for k in range(rs1) if a[raw1 + k] != b[raw2 + k]}
    return out


args = [a for a in sys.argv[1:] if not a.startswith("--")]
base_fr = "--base-fr" in sys.argv
en, fr, s366, outp = (Path(a) for a in args)
E, F, S = en.read_bytes() if en.exists() else None, fr.read_bytes(), s366.read_bytes()
sf, ss = sections(F), sections(S)
if base_fr:
    P = diffs(F, S, sf, ss)
    L = {k: set() for k in P}
else:
    se = sections(E)
    P = diffs(E, S, se, ss)
    L = diffs(E, F, se, sf)
new = bytearray(F)
report, ok = [], True
for (name, va, rs, raw) in sf:
    if name not in P:
        continue
    p, l = P[name], L[name]
    if not p and not l:
        continue
    inter = p & l
    report.append(f"  {name:9} correctif {len(p):4} octets | langue {len(l):4} octets | conflit {len(inter)}")
    if p and name.lower().startswith(".idata"):
        report.append(f"    -> {name} : difference de liaison des imports (horodatage), ignoree")
        continue
    if inter:
        ok = False
        report.append(f"    !! conflit aux offsets {sorted(inter)[:10]}")
        continue
    sraw = [r for (n, v, s_, r) in ss if n == name][0]
    for k in p:
        new[raw + k] = S[sraw + k]
print(f"{s366.name} :")
print("\n".join(report) if report else "  aucune difference hors ressources")
if ok:
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_bytes(bytes(new))
    # verification : code du nouveau fichier == code 3.66 (hors .rsrc et .idata)
    chk = diffs(bytes(new), S, sections(bytes(new)), ss)
    rest = {k: len(v) for k, v in chk.items() if v and not k.lower().startswith(".idata")}
    print(f"  => ecrit {outp.name} ; code restant different de la 3.66 : {rest or 'aucun'}")
else:
    print("  => REFUSE (conflit langue / correctif)")
