# Verifie qu'un PE n'importe que des fonctions exportees par les DLL d'un Windows 98
# (dossiers de reference fournis, le premier trouve gagne pour chaque DLL).
# Usage : checkimports.py <fichier.dll> <dossier_ref1> [dossier_ref2 ...]
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from imports import imports  # noqa: E402


def exports(path):
    d = path.read_bytes()
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    if d[pe:pe + 2] != b"PE":
        return None
    nsec = struct.unpack_from("<H", d, pe + 6)[0]
    optsz = struct.unpack_from("<H", d, pe + 20)[0]
    opt = pe + 24
    exp_rva = struct.unpack_from("<I", d, opt + 96)[0]
    secs = []
    for i in range(nsec):
        o = opt + optsz + 40 * i
        vsize, va, rsize, raw = struct.unpack_from("<IIII", d, o + 8)
        secs.append((va, max(vsize, rsize), raw))

    def off(rva):
        for va, size, raw in secs:
            if va <= rva < va + size:
                return raw + rva - va
        return None

    o = off(exp_rva)
    if o is None:
        return set()
    base, nfun, nnames, _, names_rva, ords_rva = struct.unpack_from("<IIIIII", d, o + 16)
    names = set()
    for i in range(nnames):
        n = off(struct.unpack_from("<I", d, off(names_rva) + 4 * i)[0])
        names.add(d[n:d.index(b"\0", n)].decode("latin-1"))
    ordinals = {f"#{base + i}" for i in range(nfun)}
    return names | ordinals


def main():
    refs = [Path(p) for p in sys.argv[2:]]
    index = {}
    for r in refs:
        for f in r.iterdir():
            if f.is_file():
                index.setdefault(f.name.upper(), f)

    for dll, funcs in imports(sys.argv[1]).items():
        f = index.get(dll.upper())
        if not f:
            print(f"  {dll}: ABSENT des references")
            continue
        ex = exports(f)
        if ex is None:
            print(f"  {dll}: pas un PE ({f})")
            continue
        missing = [x for x in funcs if x not in ex]
        print(f"  {dll} ({f.parent.name}): {'OK' if not missing else 'MANQUANT ' + ', '.join(missing)}")


if __name__ == "__main__":
    main()
