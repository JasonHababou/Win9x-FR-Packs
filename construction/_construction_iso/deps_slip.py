# Verifie les dependances (imports normaux ET differes) des fichiers remplaces dans
# les CAB de l'ISO, par rapport aux DLL presentes dans l'ISO apres remplacement.
# Un fichier du SP3.0 / de la 3.66 peut supposer IE6 deja installe (le pack les pose
# apres IE6 SP1) : sur le CD d'origine (IE 5), Windows ne le charge pas (ex. MSXML.DLL
# 8.0.7002 : "erreur lors du chargement", test QEMU 2026-10-18).
# Usage : deps_slip.py <dossier x de build_iso> <RAPPORT.TXT de build_iso>
import struct
import sys
from pathlib import Path


def lire_pe(p):
    d = p.read_bytes()
    if d[:2] != b"MZ":
        return None
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    if d[pe:pe + 4] != b"PE\0\0":
        return None
    nsec = struct.unpack_from("<H", d, pe + 6)[0]
    optsz = struct.unpack_from("<H", d, pe + 20)[0]
    opt = pe + 24
    secs = []
    for i in range(nsec):
        o = opt + optsz + 40 * i
        vs, va, rs, raw = struct.unpack_from("<IIII", d, o + 8)
        secs.append((va, max(vs, rs), raw))

    def off(rva):
        for va, size, raw in secs:
            if va <= rva < va + size:
                return raw + rva - va
        return None

    def cstr(o):
        return d[o:d.index(b"\0", o)].decode("latin-1")

    def dd(i):
        return struct.unpack_from("<II", d, opt + 96 + 8 * i)

    def table(t, rel):
        f = []
        while t is not None:
            v = struct.unpack_from("<I", d, t)[0]
            if v == 0:
                break
            if v & 0x80000000:
                f.append(v & 0xFFFF)
            else:
                o = off(v - rel if rel else v)
                f.append(cstr(o + 2) if o is not None else None)
            t += 4
        return f

    imp = {}
    rva, _ = dd(1)
    o = off(rva) if rva else None
    while o is not None:
        oft, _, _, name, ft = struct.unpack_from("<IIIII", d, o)
        if name == 0:
            break
        imp.setdefault(cstr(off(name)).upper(), []).extend(table(off(oft or ft), 0))
        o += 20
    rva, _ = dd(13)                                    # imports differes
    o = off(rva) if rva else None
    base = struct.unpack_from("<I", d, opt + 28)[0]
    while o is not None:
        attr, name, _, _, intt = struct.unpack_from("<IIIII", d, o)[:5]
        if name == 0:
            break
        rel = 0 if attr & 1 else base                  # ancien format : VA
        dll = cstr(off(name - rel))
        imp.setdefault(dll.upper() + " (differe)", []).extend(table(off(intt - rel), rel))
        o += 32
    exp = set()
    rva, _ = dd(0)
    o = off(rva) if rva else None
    if o is not None:
        obase, nf, nn, af, an, ao = struct.unpack_from("<IIIIII", d, o + 16)
        exp |= {obase + i for i in range(nf)}
        for i in range(nn):
            exp.add(cstr(off(struct.unpack_from("<I", d, off(an) + 4 * i)[0])))
    return imp, exp


x = Path(sys.argv[1])
remplaces = {l.split()[0].upper() for l in Path(sys.argv[2]).read_text(encoding="utf-8").splitlines()
             if l.strip() and not l.startswith(("GARDE", "PATCHER9X"))}
fichiers = {}
for p in x.rglob("*"):
    if p.is_file():
        fichiers.setdefault(p.name.upper(), p)
exports = {}
for nom in remplaces:
    p = fichiers.get(nom)
    if not p:
        continue
    r = lire_pe(p)
    if not r:
        continue
    for dll, funcs in r[0].items():
        cible = dll.replace(" (differe)", "")
        if cible not in exports:
            q = fichiers.get(cible)
            rr = lire_pe(q) if q else None
            exports[cible] = rr[1] if rr else None
        ex = exports[cible]
        if ex is None:
            print(f"{nom:14} {dll:30} DLL absente du CD")
            continue
        manq = [f for f in funcs if f is not None and f not in ex]
        if manq:
            print(f"{nom:14} {dll:30} {len(manq)} manquantes : {manq[:6]}")
