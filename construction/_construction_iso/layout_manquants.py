# Fichiers copies par un INF du CD (CopyFiles) dont la LayoutFile ne cite pas le
# LAYOUT qui les decrit (ex. NETFAM.INF : LayoutFile=layout.inf, mais IENPSTUB.DLL
# n'est que dans LAYOUT1.INF -> "fichier introuvable" pendant l'installation du
# materiel, test QEMU 2026-10-18). Renvoie les lignes a ajouter a chaque LAYOUT.
import re
from pathlib import Path


def sections(t):
    s, cur = {}, None
    for l in t.splitlines():
        l = l.split(";")[0].strip()
        m = re.match(r"^\[(.+)\]$", l)
        if m:
            cur = m.group(1).strip().lower()
            s.setdefault(cur, [])
        elif cur and l:
            s[cur].append(l)
    return s


def manquants(dossier):
    infs = {p.name.lower(): p for p in Path(dossier).iterdir() if p.suffix.lower() == ".inf"}
    lay = {}
    for n in ("layout.inf", "layout1.inf", "layout2.inf"):
        sec = sections(infs[n].read_bytes().decode("cp1252"))
        lay[n] = {}
        for l in sec.get("sourcedisksfiles", []):
            k, _, v = l.partition("=")
            lay[n][k.strip().lower()] = l
    ajout = {n: {} for n in lay}
    for nom, p in infs.items():
        if nom.startswith("layout"):
            continue
        sec = sections(p.read_bytes().decode("cp1252", "replace"))
        v = [l for l in sec.get("version", []) if l.lower().startswith("layoutfile")]
        if not v:
            continue
        cites = [x.strip().lower() for x in v[0].split("=", 1)[1].split(",")]
        cites = [c for c in cites if c in lay]
        if not cites:
            continue
        listes = set()
        for lignes in sec.values():
            for l in lignes:
                k, _, val = l.partition("=")
                if k.strip().lower() == "copyfiles":
                    listes |= {x.strip().lower() for x in val.split(",") if x.strip() and not x.strip().startswith("@")}
        for liste in listes:
            for l in sec.get(liste, []):
                f = l.split(",")[0].strip().strip('"').lower()
                src = l.split(",")[1].strip().lower() if l.count(",") >= 1 and l.split(",")[1].strip() else f
                for nf in {f, src}:
                    if not re.match(r"^[\w~$-]+\.\w+$", nf) or any(nf in lay[c] for c in cites):
                        continue
                    autre = next((n for n in lay if nf in lay[n]), None)
                    if autre:
                        ajout[cites[0]][nf] = lay[autre][nf]
    return ajout


if __name__ == "__main__":
    import sys
    a = manquants(sys.argv[1])
    for n, d in a.items():
        print(n, len(d), sorted(d)[:40])
