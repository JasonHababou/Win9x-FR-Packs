# Lecteur minimal de ressources PE (icones, groupes d'icones, bitmaps, AVI) et
# reconstruction d'un fichier .ICO a partir d'un groupe d'icones.
import struct


class PE:
    def __init__(self, path):
        self.d = d = open(path, "rb").read()
        pe = struct.unpack_from("<I", d, 0x3C)[0]
        assert d[pe:pe + 4] == b"PE\0\0"
        nsec = struct.unpack_from("<H", d, pe + 6)[0]
        opt = struct.unpack_from("<H", d, pe + 20)[0]
        o = pe + 24
        magic = struct.unpack_from("<H", d, o)[0]
        dd = o + (96 if magic == 0x10B else 112)
        self.rsrc_rva = struct.unpack_from("<I", d, dd + 2 * 8)[0]
        self.secs = []
        s = pe + 24 + opt
        for i in range(nsec):
            va, vs, raw = struct.unpack_from("<III", d, s + i * 40 + 12)[0:1] + \
                struct.unpack_from("<I", d, s + i * 40 + 8) + struct.unpack_from("<I", d, s + i * 40 + 20)
            self.secs.append((va, vs, raw))
        self.res = {}
        if self.rsrc_rva:
            self._walk(self.off(self.rsrc_rva), [])

    def off(self, rva):
        for va, vs, raw in self.secs:
            if va <= rva < va + max(vs, 1):
                return rva - va + raw
        raise ValueError(hex(rva))

    def _name(self, v):
        if v & 0x80000000:
            p = self.off(self.rsrc_rva) + (v & 0x7FFFFFFF)
            n = struct.unpack_from("<H", self.d, p)[0]
            return self.d[p + 2:p + 2 + 2 * n].decode("utf-16-le")
        return v

    def _walk(self, p, path):
        nn, ni = struct.unpack_from("<HH", self.d, p + 12)
        for i in range(nn + ni):
            name, ent = struct.unpack_from("<II", self.d, p + 16 + 8 * i)
            key = self._name(name)
            if ent & 0x80000000:
                self._walk(self.off(self.rsrc_rva) + (ent & 0x7FFFFFFF), path + [key])
            else:
                rva, size = struct.unpack_from("<II", self.d, self.off(self.rsrc_rva) + ent)
                typ, rid = path[0], path[1]
                self.res.setdefault((typ, rid), self.d[self.off(rva):self.off(rva) + size])

    def groups(self):
        return {rid: data for (t, rid), data in self.res.items() if t == 14}

    def group_ico(self, rid):
        """Fichier .ICO complet du groupe d'icones rid."""
        g = self.res[(14, rid)]
        n = struct.unpack_from("<H", g, 4)[0]
        ents, imgs = [], []
        for i in range(n):
            w, h, c, r, planes, bpp, size, iid = struct.unpack_from("<BBBBHHIH", g, 6 + 14 * i)
            img = self.res[(3, iid)]
            ents.append((w, h, c, r, planes, bpp, len(img)))
            imgs.append(img)
        out = struct.pack("<HHH", 0, 1, n)
        o = 6 + 16 * n
        for (w, h, c, r, planes, bpp, size), img in zip(ents, imgs):
            out += struct.pack("<BBBBHHII", w, h, c, r, planes, bpp, size, o)
            o += size
        return out + b"".join(imgs)
