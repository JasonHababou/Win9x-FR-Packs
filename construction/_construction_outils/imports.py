# Liste les imports (DLL + fonctions) d'un PE 32 bits, sans dependance externe.
import struct
import sys


def imports(path):
    d = open(path, "rb").read()
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    nsec = struct.unpack_from("<H", d, pe + 6)[0]
    optsz = struct.unpack_from("<H", d, pe + 20)[0]
    opt = pe + 24
    imp_rva = struct.unpack_from("<I", d, opt + 104)[0]
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

    def cstr(o):
        return d[o:d.index(b"\0", o)].decode("latin-1")

    res = {}
    o = off(imp_rva)
    while o is not None:
        oft, _, _, name, ft = struct.unpack_from("<IIIII", d, o)
        if name == 0:
            break
        dll = cstr(off(name))
        funcs = []
        t = off(oft or ft)
        while t is not None:
            v = struct.unpack_from("<I", d, t)[0]
            if v == 0:
                break
            funcs.append(f"#{v & 0xFFFF}" if v & 0x80000000 else cstr(off(v) + 2))
            t += 4
        res[dll] = funcs
        o += 20
    return res


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print("==", p)
        for dll, funcs in imports(p).items():
            print(f"  {dll} ({len(funcs)})")
