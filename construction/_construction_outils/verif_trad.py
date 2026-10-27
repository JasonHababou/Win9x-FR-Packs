# Verifie un fichier traduit : textes visibles, sections de code identiques a
# l'original, imports et exports inchanges.
import re
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, r"<DOSSIER_WINDOWS>\win98se\_construction_outils")
from peres import PE  # noqa: E402
from imports import imports  # noqa: E402
from checkimports import exports  # noqa: E402


def textes(pe):
    out = []
    for (t, rid), data in pe.res.items():
        if t == 6:
            o = 0
            for _ in range(16):
                n = struct.unpack_from("<H", data, o)[0]
                s = data[o + 2:o + 2 + 2 * n].decode("utf-16-le", "replace")
                o += 2 + 2 * n
                if s.strip():
                    out.append(s)
        elif t in (4, 5):
            for m in re.finditer(rb"(?:[\x20-\x7e\xc0-\xff]\x00){3,}", data):
                out.append(m.group().decode("utf-16-le"))
    return out


def sections(path):
    d = Path(path).read_bytes()
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    n = struct.unpack_from("<H", d, pe + 6)[0]
    opt = struct.unpack_from("<H", d, pe + 20)[0]
    r = {}
    for i in range(n):
        o = pe + 24 + opt + 40 * i
        nom = d[o:o + 8].rstrip(b"\0").decode()
        vs, va, rs, raw = struct.unpack_from("<IIII", d, o + 8)
        r[nom] = d[raw:raw + rs]
    return r


orig, trad = sys.argv[1], sys.argv[2]
so, st = sections(orig), sections(trad)
for nom in so:
    if nom != ".rsrc":
        print(f"  section {nom:8} {'identique' if so[nom] == st.get(nom) else 'DIFFERENTE'}")
print("  imports", "identiques" if imports(orig) == imports(trad) else "DIFFERENTS")
print("  exports", "identiques" if exports(Path(orig)) == exports(Path(trad)) else "DIFFERENTS")
t = textes(PE(trad))
anglais = [s for s in t if re.search(r"\b(the|file|object|options|display|search|contents|index|cancel|browse)\b", s, re.I)]
print(f"  {len(t)} textes ; exemples :", [s[:30] for s in t[:6]])
print(f"  textes qui semblent encore anglais ({len(anglais)}) :", [s[:40] for s in anglais[:12]])
