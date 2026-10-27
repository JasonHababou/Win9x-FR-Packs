# Extracteur d'archive InstallShield 3 (_SETUP.1, signature 13 5D 65 8C),
# fichiers compresses PKWARE DCL "implode" (decodeur = portage de zlib/contrib/blast.c).
# Usage : is3unz.py <_SETUP.1> <dossier_sortie> [-l]
import struct
import sys
from pathlib import Path

LITLEN = [11, 124, 8, 7, 28, 7, 188, 13, 76, 4, 10, 8, 12, 10, 12, 10, 8, 23, 8,
          9, 7, 6, 7, 8, 7, 6, 55, 8, 23, 24, 12, 11, 7, 9, 11, 12, 6, 7, 22, 5,
          7, 24, 6, 11, 9, 6, 7, 22, 7, 11, 38, 7, 9, 8, 25, 11, 8, 11, 9, 12,
          8, 12, 5, 38, 5, 38, 5, 11, 7, 5, 6, 21, 6, 10, 53, 8, 7, 24, 10, 27,
          44, 253, 253, 253, 252, 252, 252, 13, 12, 45, 12, 45, 12, 61, 12, 45,
          44, 173]
LENLEN = [2, 35, 36, 53, 38, 23]
DISTLEN = [2, 20, 53, 230, 247, 151, 248]
BASE = [3, 2, 4, 5, 6, 7, 8, 9, 10, 12, 16, 24, 40, 72, 136, 264]
EXTRA = [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8]


def huff(rep):
    lengths = []
    for b in rep:
        lengths += [b & 15] * ((b >> 4) + 1)
    count = [0] * 17
    for l in lengths:
        count[l] += 1
    offs = [0] * 18
    for i in range(1, 16):
        offs[i + 1] = offs[i] + count[i]
    sym = [0] * len(lengths)
    for s, l in enumerate(lengths):
        sym[offs[l]] = s
        offs[l] += 1
    return count, sym


LIT, LEN, DIST = huff(LITLEN), huff(LENLEN), huff(DISTLEN)


def blast(data, size):
    pos, bitbuf, bitcnt = 2, 0, 0
    out = bytearray()

    def bits(n):
        nonlocal pos, bitbuf, bitcnt
        while bitcnt < n:
            bitbuf |= data[pos] << bitcnt
            pos += 1
            bitcnt += 8
        v = bitbuf & ((1 << n) - 1)
        bitbuf >>= n
        bitcnt -= n
        return v

    def decode(h):
        count, sym = h
        code = first = index = 0
        for l in range(1, 17):
            code |= bits(1) ^ 1
            c = count[l]
            if code < first + c:
                return sym[index + code - first]
            index += c
            first = (first + c) << 1
            code <<= 1
        raise ValueError("code Huffman invalide")

    lit, dic = data[0], data[1]
    assert lit in (0, 1) and dic in (4, 5, 6), (lit, dic)
    while len(out) < size:
        if bits(1):
            s = decode(LEN)
            ln = BASE[s] + bits(EXTRA[s])
            if ln == 519:
                break
            sh = 2 if ln == 2 else dic
            dist = (decode(DIST) << sh) + bits(sh) + 1
            for _ in range(ln):
                out.append(out[-dist])
        else:
            out.append(decode(LIT) if lit else bits(8))
    return bytes(out)


def entries(d):
    assert d[:4] == b"\x13\x5d\x65\x8c"
    nfiles = struct.unpack_from("<H", d, 0x0C)[0]
    dir_off = struct.unpack_from("<I", d, 0x29)[0]
    ndirs = struct.unpack_from("<H", d, 0x31)[0]
    file_off = struct.unpack_from("<I", d, 0x33)[0]
    dirs, o = [], dir_off
    for _ in range(ndirs):
        n, esz, nl = struct.unpack_from("<HHH", d, o)
        dirs.append((d[o + 6:o + 6 + nl].decode("cp1252"), n))
        o += esz
    o, res = file_off, []
    for dname, n in dirs:
        for _ in range(n):
            orig, comp, off = struct.unpack_from("<III", d, o + 3)
            date, time = struct.unpack_from("<HH", d, o + 0x0F)
            esz = struct.unpack_from("<H", d, o + 0x17)[0]
            nl = d[o + 0x1D]
            name = d[o + 0x1E:o + 0x1E + nl].decode("cp1252")
            res.append((dname, name, orig, comp, off, date, time))
            o += esz
    assert len(res) == nfiles
    return res


def main():
    d = Path(sys.argv[1]).read_bytes()
    out = Path(sys.argv[2])
    for g, name, orig, comp, off, date, time in entries(d):
        stamp = f"{1980 + (date >> 9)}-{(date >> 5) & 15:02}-{date & 31:02}"
        print(f"{g:7} {name:22} {orig:9} {stamp}")
        if "-l" in sys.argv:
            continue
        data = blast(d[off:off + comp], orig)
        assert len(data) == orig, (name, len(data), orig)
        (out / g).mkdir(parents=True, exist_ok=True)
        (out / g / name).write_bytes(data)


main()
