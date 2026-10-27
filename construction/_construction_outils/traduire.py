# Traduction d'un fichier anglais recent par report des ressources francaises d'une
# version plus ancienne : dialogues et menus (si memes identifiants de controles /
# commandes), tables de chaines (chaine par chaine, la FR remplace l'EN quand
# elle existe). Ecrit un .RES (langue = celle des ressources EN) a appliquer
# avec ResHack -addoverwrite.
# Usage : traduire.py <fichier EN recent> <fichier FR ancien> <sortie.res>
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from peres import PE  # noqa: E402


class PEL(PE):
    """PE avec langue de chaque ressource : self.lres[(type, id)] = (lang, data)."""

    def _walk(self, p, path):
        nn, ni = struct.unpack_from("<HH", self.d, p + 12)
        for i in range(nn + ni):
            name, ent = struct.unpack_from("<II", self.d, p + 16 + 8 * i)
            key = self._name(name)
            if ent & 0x80000000:
                self._walk(self.off(self.rsrc_rva) + (ent & 0x7FFFFFFF), path + [key])
            else:
                rva, size = struct.unpack_from("<II", self.d, self.off(self.rsrc_rva) + ent)
                typ, rid, lang = path[0], path[1], key
                data = self.d[self.off(rva):self.off(rva) + size]
                self.res.setdefault((typ, rid), data)
                if not hasattr(self, "lres"):
                    self.lres = {}
                self.lres.setdefault((typ, rid), (lang, data))


def sz(d, o):
    """Lit un champ sz_Or_Ord (dialogues/menus) ; renvoie (valeur, nouvel offset)."""
    w = struct.unpack_from("<H", d, o)[0]
    if w == 0xFFFF:
        return struct.unpack_from("<H", d, o + 2)[0], o + 4
    e = o
    while struct.unpack_from("<H", d, e)[0]:
        e += 2
    return d[o:e].decode("utf-16-le"), e + 2


def al4(o):
    return (o + 3) & ~3


def ids_dialogue(d):
    """Identifiants des controles d'un DLGTEMPLATE ou DLGTEMPLATEEX."""
    ex = struct.unpack_from("<HH", d, 0) == (1, 0xFFFF)
    if ex:
        n = struct.unpack_from("<H", d, 16)[0]
        o = 26
        style = struct.unpack_from("<I", d, 12)[0]
    else:
        style = struct.unpack_from("<I", d, 0)[0]
        n = struct.unpack_from("<H", d, 8)[0]
        o = 18
    _, o = sz(d, o)          # menu
    _, o = sz(d, o)          # classe
    _, o = sz(d, o)          # titre
    if style & 0x40:         # DS_SETFONT
        o += 6 if ex else 2
        _, o = sz(d, o)
    ids = []
    for _ in range(n):
        o = al4(o)
        if ex:
            cid = struct.unpack_from("<I", d, o + 20)[0]
            o += 24
        else:
            cid = struct.unpack_from("<H", d, o + 16)[0]
            o += 18
        cls, o = sz(d, o)
        _, o = sz(d, o)
        extra = struct.unpack_from("<H", d, o)[0]
        o += 2 + extra
        ids.append((cid, cls if isinstance(cls, int) else cls.upper()))
    return ids


def ids_menu(d):
    """Identifiants des commandes d'un menu (MENUITEMTEMPLATE ou MENUEX)."""
    ver, off = struct.unpack_from("<HH", d, 0)
    ids = []
    if ver == 0:
        o = 4
        prof = 1
        while o < len(d) and prof > 0:
            fl = struct.unpack_from("<H", d, o)[0]
            o += 2
            if not fl & 0x10:            # MF_POPUP absent : element avec ID
                ids.append(struct.unpack_from("<H", d, o)[0])
                o += 2
            _, o = sz(d, o)
            if fl & 0x10:
                prof += 1
            if fl & 0x80:                # MF_END
                prof -= 1
        return ids
    o = 4 + off
    while o + 14 <= len(d):
        o = al4(o)
        typ, state, mid, res = struct.unpack_from("<IIIH", d, o)
        o += 14
        _, o = sz(d, o)
        o = al4(o)
        if res & 1:
            o += 4
        ids.append(mid)
    return ids


def chaines(d):
    out, o = [], 0
    for _ in range(16):
        n = struct.unpack_from("<H", d, o)[0]
        out.append(d[o + 2:o + 2 + 2 * n].decode("utf-16-le"))
        o += 2 + 2 * n
    return out


def bloc(ch):
    return b"".join(struct.pack("<H", len(s)) + s.encode("utf-16-le") for s in ch)


def entete_res(typ, nom, lang, taille):
    def ident(v):
        return struct.pack("<HH", 0xFFFF, v) if isinstance(v, int) else v.encode("utf-16-le") + b"\0\0"
    t, n = ident(typ), ident(nom)
    h = t + n
    if len(h) % 4:
        h += b"\0\0"
    h += struct.pack("<IHHII", 0, 0x1030, lang, 0, 0)
    return struct.pack("<II", taille, 8 + len(h)) + h


# 4e argument facultatif : fichier Python definissant MANUEL = {numero: "texte FR"}
MANUEL = {}
if len(sys.argv) > 4:
    exec(Path(sys.argv[4]).read_text(encoding="utf-8"))
en, fr = PEL(sys.argv[1]), PEL(sys.argv[2])
sortie = [entete_res(0, 0, 0, 0)]                # entree vide obligatoire en tete de .RES
rap = {"dialogues": [0, 0], "menus": [0, 0], "chaines": [0, 0]}
for (typ, rid), (lang, d_en) in sorted(en.lres.items(), key=lambda x: (str(x[0][0]), str(x[0][1]))):
    if (typ, rid) not in fr.lres:
        if typ != 6:
            continue
        d_fr = bytes(32)          # bloc absent de la version FR : traductions manuelles seules
    else:
        d_fr = fr.lres[(typ, rid)][1]
    neuf = None
    if typ == 5:
        rap["dialogues"][1] += 1
        try:
            if ids_dialogue(d_en) == ids_dialogue(d_fr):
                neuf = d_fr
        except Exception:
            pass
        if neuf:
            rap["dialogues"][0] += 1
        else:
            print("   dialogue", rid, "different, garde en anglais")
    elif typ == 4:
        rap["menus"][1] += 1
        try:
            if ids_menu(d_en) == ids_menu(d_fr):
                neuf = d_fr
        except Exception:
            pass
        if neuf:
            rap["menus"][0] += 1
        else:
            print("   menu", rid, "different, garde en anglais")
    elif typ == 6:
        ce, cf = chaines(d_en), chaines(d_fr)

        def fmt(s):
            # parametres de mise en forme (%s, %d, %1...) : doivent etre identiques
            import re
            return re.findall(r"%[-+ #0]*\d*(?:\.\d+)?[hlI]*[a-zA-Z]|%\d+(?:!\w+!)?", s)

        ok = [bool(f and e and fmt(f) == fmt(e)) for e, f in zip(ce, cf)]
        m = [f if k else e for e, f, k in zip(ce, cf, ok)]
        # traductions manuelles des chaines nouvelles (absentes de la version FR)
        for i in range(16):
            num = (rid - 1) * 16 + i
            if num in MANUEL and ce[i] and fmt(MANUEL[num]) == fmt(ce[i]):
                m[i] = MANUEL[num]
                ok[i] = True
        rap["chaines"][0] += sum(ok)
        rap["chaines"][1] += sum(1 for e in ce if e)
        if m != ce:
            neuf = bloc(m)
    if neuf is not None:
        donnees = neuf + b"\0" * ((4 - len(neuf) % 4) % 4)
        sortie.append(entete_res(typ, rid, lang, len(neuf)) + donnees)
Path(sys.argv[3]).write_bytes(b"".join(sortie))
for k, (a, b) in rap.items():
    print(f"{k} : {a} traduits sur {b}")
