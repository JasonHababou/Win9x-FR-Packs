# Plus! 98 FR du pack : retire de PLUS98.CAB les fichiers des composants jamais
# installes (Lecteur CD Deluxe, Picture It! Express, Assistant Maintenance, Golf,
# Lose Your Marbles, Organic Art, VirusScan). Un fichier n'est retire que s'il
# n'apparait dans AUCUNE section CopyFiles d'un autre composant. Les INF ne sont
# pas modifies (les composants restent decoches dans MSBATCH.INF).
# Usage : plus98_allege.py <dossier plus98 du pack> <dossier de travail> [--ecrire]
import re
import shutil
import subprocess
import sys
from pathlib import Path

P98, W = Path(sys.argv[1]), Path(sys.argv[2])
ECRIRE = "--ecrire" in sys.argv
CAB = P98 / "PLUS98.CAB"
RETIRES = {("PLUS98.INF", "WEBCD"), ("PLUS98.INF", "TUNEUP"), ("PLS98APP.INF", "PIE"),
           ("PLS98GAM.INF", "GOLF"), ("PLS98GAM.INF", "LYM"), ("PLS98APP.INF", "OA"),
           ("PLS98APP.INF", "VS")}

if W.exists():
    shutil.rmtree(W)
(W / "x").mkdir(parents=True)
out = subprocess.run(["7z", "l", "-slt", str(CAB)], capture_output=True, text=True,
                     encoding="utf-8", errors="replace", check=True).stdout
names = [l[7:] for l in out.splitlines() if l.startswith("Path = ")][1:]
subprocess.run(["7z", "x", "-y", "-o" + str(W / "x"), str(CAB)], check=True, stdout=subprocess.DEVNULL)
up = {n.upper(): n for n in names}


def sections(path):
    secs, cur = {}, None
    for l in path.read_bytes().decode("cp1252", "replace").splitlines():
        s = l.split(";", 1)[0].strip()
        m = re.match(r"^\[([^\]]+)\]", s)
        if m:
            cur = m.group(1).strip().upper()
            secs.setdefault(cur, [])
        elif cur and s:
            secs[cur].append(s)
    return secs


infs = {n.upper(): sections(W / "x" / up[n.upper()]) for n in ("PLUS98.INF", "PLS98APP.INF", "PLS98GAM.INF", "PLS98THM.INF")}


def copy_sections(inf, sec):
    res = []
    for l in infs[inf].get(sec, []):
        k, _, v = l.partition("=")
        if k.strip().upper() in ("COPYFILES", "RENFILES"):
            res += [x.strip().upper() for x in v.split(",") if x.strip()]
    return res


def files(inf, cs):
    r = set()
    for l in infs[inf].get(cs, []):
        parts = [p.strip() for p in l.split(",")]
        for p in parts[:2]:                       # nom de destination, nom source
            if p and p.upper() in up:
                r.add(p.upper())
    return r


# sections d'installation = celles qui ont un CopyFiles ; fichiers par section
tous_inst = {(i, s) for i in infs for s in infs[i] if copy_sections(i, s)}
a_retirer, a_garder = set(), set()
for i, s in tous_inst:
    fs = set()
    for cs in copy_sections(i, s):
        fs |= files(i, cs)
    (a_retirer if (i, s) in RETIRES else a_garder).update(fs)
assert RETIRES <= tous_inst, RETIRES - tous_inst
# tout fichier cite ailleurs dans un INF (hors sections des composants retires) reste
cites = set()


def lies(inf, sec, vus):
    """Section d'installation + toutes les sections qu'elle cite (recursif)."""
    if (inf, sec) in vus or sec not in infs[inf]:
        return
    vus.add((inf, sec))
    for l in infs[inf][sec]:
        k, eq, v = l.partition("=")
        if eq:
            for x in v.split(","):
                lies(inf, x.strip().upper(), vus)


sec_ret = set()
for i, s in RETIRES:
    lies(i, s, sec_ret)
# liste de fichiers VirusScan non citee ailleurs (detection d'une installation existante)
sec_ret.add(("PLS98APP.INF", "VS.SETUP"))
for i in infs:
    for s, lines in infs[i].items():
        if (i, s) in sec_ret:
            continue
        for l in lines:
            for tok in re.split(r"[,=\s\\\"]+", l):
                if tok.upper() in up:
                    cites.add(tok.upper())
                    if tok.upper() in a_retirer and tok.upper() not in a_garder:
                        print("   cite :", tok.upper(), "dans", i, s)
retire = sorted(a_retirer - a_garder - cites)
taille = sum((W / "x" / up[f]).stat().st_size for f in retire)
print(len(retire), "fichiers a retirer,", round(taille / 2**20, 1), "Mo decompresses")
for i, s in sorted(RETIRES):
    fs = set()
    for cs in copy_sections(i, s):
        fs |= files(i, cs)
    garde = sorted(fs - set(retire))
    print(f"  {s:<7} {len(fs & set(retire)):>4} retires, gardes car partages : {garde[:12]}")

if ECRIRE:
    keep = [n for n in names if n.upper() not in set(retire)]
    ddf = [".OPTION EXPLICIT", ".Set CabinetNameTemplate=PLUS98.CAB", ".Set DiskDirectoryTemplate=" + str(W / "cab"),
           ".Set Cabinet=on", ".Set Compress=on", ".Set CompressionType=MSZIP", ".Set MaxDiskSize=0",
           ".Set CabinetFileCountThreshold=0", ".Set FolderFileCountThreshold=0", ".Set FolderSizeThreshold=0",
           ".Set MaxCabinetSize=0", ".Set UniqueFiles=on", ".Set RptFileName=NUL", ".Set InfFileName=NUL"]
    ddf += ['"%s" "%s"' % (W / "x" / n, n) for n in keep]
    (W / "p.ddf").write_text("\r\n".join(ddf) + "\r\n", encoding="cp1252")
    subprocess.run(["makecab", "/F", str(W / "p.ddf")], check=True, stdout=subprocess.DEVNULL)
    chk = W / "chk"
    subprocess.run(["7z", "x", "-y", "-o" + str(chk), str(W / "cab" / "PLUS98.CAB")], check=True, stdout=subprocess.DEVNULL)
    assert sorted(p.name for p in chk.iterdir()) == sorted(keep)
    for n in keep:
        assert (chk / n).read_bytes() == (W / "x" / n).read_bytes(), n
    (W / "retires.txt").write_text("\n".join(up[f] for f in retire) + "\n", encoding="utf-8")
    print("CAB :", CAB.stat().st_size, "->", (W / "cab" / "PLUS98.CAB").stat().st_size)
