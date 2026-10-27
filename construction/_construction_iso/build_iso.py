# ISO Windows 98 SE FR personnalisee, etape 1 : CD "Bootable" (version boite)
# allege + fichiers du SP3.0 FR integres dans les CAB (slipstream), comme les
# Slipstream Tools de R. Loew : CAB "despannes" (chaque CAB redevient autonome,
# memes noms, chaque fichier reste dans le CAB que LAYOUT*.INF lui attribue),
# fichiers remplaces par leur version SP3.0 (OLEDLG et HHCTRL : versions
# traduites en francais), tailles mises a jour dans LAYOUT*.INF, MINI.CAB et
# CHL99.CAB intacts (MINI contient des versions differentes, regle de R. Loew).
# Usage : build_iso.py <dossier de travail> <iso de sortie>
import os
import re
import stat
import shutil
import struct
import subprocess
import sys
from pathlib import Path

WIN = Path(r"<DOSSIER_WINDOWS>\win98se")
ISO_SRC = WIN / "ISO/Windows98/Windows 98 Se Fr Bootable.iso"
SP30 = WIN / "Win98FR_v3/02_SP30"
SP366 = WIN / "Win98FR_v3/03_SYST/sp366fr"
# W98_PACK / W98_CLE : version publique (pack sans cle Plus! 98, cle demandee par Setup)
PACK = Path(os.environ.get("W98_PACK", WIN / "Win98FR_v3"))
P9X = WIN / "Sources/patcher9x-0.9.91/win64/patcher9x.exe"
VBEMP = WIN / "Sources/vbemp/140214"
CLE = os.environ.get("W98_CLE", "XXXXX-XXXXX-XXXXX-XXXXX-XXXXX")          # cle de l'utilisateur (MSBATCH.INF) ; vide = demandee
TRAD = WIN / "WIN9X/Mise a jour/FR traduits (OLEDLG HHCTRL)"
W, ISO_OUT = Path(sys.argv[1]), Path(sys.argv[2])
RETIRER = ["cdsample", "add-ons", "win98/ols", "win98/tour"]
INTACTS = {"MINI.CAB", "CHL99.CAB"}
# Fichiers du SP3.0 de l'epoque IE6 : le CD n'a qu'IE 5.0 et le pack les pose apres
# IE6 SP1. Integres, WUPDMGR 5.3 ne chargeait pas MSXML 8.0.7002 ("Windows Update :
# erreur lors du chargement de msxml.dll", test QEMU 2026-10-18) ; ADVPACK 6.0
# servirait a installer les composants d'IE 5 pendant l'installation de Windows.
IE6_SEULEMENT = {"MSXML.DLL", "WUPDMGR.EXE", "ADVPACK.DLL"}
# Plus generalement, seuls les PILOTES et le NOYAU sont integres aux CAB (utiles des
# l'installation : ESDI_506 48 bits, USB, IOS, NTKERN, IFSMGR, VMM32 + patcher9x,
# WINBOOT.SYS FR...). Les DLL / programmes du SP3.0 et de la 3.66 supposent IE6
# (WSHEXT, MSPKI, CRYPTDLG... ne se chargeaient pas pendant l'installation, test QEMU
# 2026-10-18) : le pack les pose au premier demarrage, apres IE6 SP1, comme le CD V3.
PILOTES_EXT = (".VXD", ".PDR", ".SYS", ".MPD", ".386", ".PCI")


def run(*a):
    subprocess.run(list(a), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def version(p):
    d = p.read_bytes()
    i = d.find("VS_VERSION_INFO".encode("utf-16-le"))
    if i < 0:
        return ()
    j = d.find(b"\xbd\x04\xef\xfe", i)
    if not 0 < j - i < 200:
        return ()
    ms, ls = struct.unpack_from("<II", d, j + 8)
    return (ms >> 16, ms & 0xFFFF, ls >> 16, ls & 0xFFFF)


def _ecrire(f, chemin, _e):
    os.chmod(chemin, stat.S_IWRITE)             # fichiers en lecture seule du pack
    f(chemin)


if W.exists():
    shutil.rmtree(W, onexc=_ecrire)
cd = W / "cd"
run("7z", "x", "-y", "-o" + str(cd), str(ISO_SRC))
for r in RETIRER:
    for p in cd.iterdir():
        pass
    cible = [p for p in cd.rglob("*") if str(p.relative_to(cd)).replace("\\", "/").lower() == r]
    for c in cible:
        shutil.rmtree(c) if c.is_dir() else c.unlink()
boot_img = cd / "[BOOT]" / "Boot-1.44M.img"
boot = W / "boot.img"
shutil.move(str(boot_img), str(boot))
shutil.rmtree(cd / "[BOOT]")
# Disquette de demarrage : le menu "installation depuis le CD-ROM" appelle
# W98FRDOS.BAT (racine du CD : limite de memoire comme l'UBCD, puis OEMSETUP.EXE)
# au lieu d'OEMSETUP.EXE. Modification sur place : AUTOEXEC.BAT reste dans son
# unique secteur de 512 octets, seule sa taille change dans le repertoire FAT12.
img = bytearray(boot.read_bytes())
ancien, neuf = b"cd \\WIN98\r\necho.\r\nOEMSETUP.EXE\r\n", b"echo.\r\ncall %CDROM%\\W98FRDOS.BAT\r\n"
assert img.count(ancien) == 1 and img.count(b"AUTOEXECBAT") == 1
d = img.index(b"AUTOEXECBAT")
taille = struct.unpack_from("<I", img, d + 28)[0]
debut = img.index(ancien) - (img.index(ancien) % 512)          # secteur des donnees du fichier
assert img[debut:debut + 11] == b"@ECHO OFF\r\n" and taille + len(neuf) - len(ancien) <= 512
contenu_ae = bytes(img[debut:debut + taille]).replace(ancien, neuf)
img[debut:debut + 512] = contenu_ae + b"\0" * (512 - len(contenu_ae))
struct.pack_into("<I", img, d + 28, len(contenu_ae))
boot.write_bytes(bytes(img))
w98 = next(p for p in cd.iterdir() if p.name.lower() == "win98")
cabs = {p.name.upper(): p for p in w98.iterdir() if p.suffix.upper() == ".CAB"}
# groupe "Pack Windows 98 FR" (W98FRPK.INF, W98FRGO.BAT) et fichier de reponses
# (cle + composants preselectionnes, lu automatiquement par SETUP.EXE)
ICI = Path(__file__).parent
run(sys.executable, str(ICI / "make_composants.py"), str(W))
run(sys.executable, str(ICI / "make_msbatch.py"), str(ICI / "w98_composants.txt"), str(w98 / "MSBATCH.INF"),
    CLE, str(W / "W98FRPK.INF"))

# --- pack Win98FR "cible ISO", lance au premier demarrage par W98FRGO.BAT.
# DirectX, MS Agent, MMC, RegClean, SharedDLLs : retires du pack 1 lui-meme
# (2026-10-19), ils sont dans le pack 2 commun au pack et a l'ISO. WinTop, Fraps,
# .NET 1.1 et Tarot = cases ; fuseaux horaires et extension TrueType = toujours
# (CHOIX.VBS). PACK_HORS / OPTS_HORS : filet si ces dossiers revenaient.
PACK_HORS = {"07_DX", "05_EXTRA/msagent"}
OPTS_HORS = ("MMC", "REGCLEAN.", "SHAREDLL.", "SHRDLL.", "CIC.DLL", "MSVCP50.DLL")


def hors_pack(dossier, noms):
    rel = Path(dossier).relative_to(PACK).as_posix()
    r = [n for n in noms if (f"{rel}/{n}" if rel != "." else n) in PACK_HORS]
    if rel == "06_OPTS":
        r += [n for n in noms if n.upper().startswith(OPTS_HORS)]
    return r


# A la racine du CD, a cote de WIN98 (dans un dossier W98FR, les pilotes SiS
# depassaient les 8 niveaux ISO9660) : AUTORUN de Windows garde, LISEZMOI du
# pack renomme (celui de Microsoft reste).
RACINE_HORS = {"AUTORUN.INF", "AUTORUN.EXE", "LISEZMOI.TXT"} | PACK_HORS
deja = {p.name.upper() for p in cd.iterdir()}
for p in PACK.iterdir():
    if p.name.upper() in RACINE_HORS or p.name in RACINE_HORS:
        continue
    assert p.name.upper() not in deja, p.name
    if p.is_dir():
        shutil.copytree(p, cd / p.name, ignore=hors_pack)
    else:
        shutil.copy2(p, cd / p.name)
shutil.copy2(PACK / "LISEZMOI.TXT", cd / "LISEZMOI_PACK.TXT")
# VBEMP 2014.02.14 (pilote d'affichage universel VESA, bearwindows) : cartes sans pilote 98
vbemp = next(p for p in cd.iterdir() if p.name.lower() == "drivers") / "display" / "vbemp"
shutil.copytree(VBEMP, vbemp)
shutil.copy2(ICI / "vbemp_LISEZMOI.TXT", vbemp / "LISEZMOI.TXT")
shutil.copy2(ICI / "pack_iso" / "W98FRCD.BAT", cd / "W98FRCD.BAT")
for f in ("W98FRDOS.BAT", "W98FRMEM.BAT"):                         # appeles par la disquette
    shutil.copy2(ICI / "pack_iso" / f, cd / f)
shutil.copy2(W / "CHOIX.VBS", cd / "CHOIX.VBS")             # genere par make_composants.py

# --- contenu de chaque CAB (liste isolee = fichiers commencant ou contenus dans ce CAB)
def liste_isolee(cab):
    t = W / "seul"
    if t.exists():
        shutil.rmtree(t)
    t.mkdir()
    shutil.copy2(cab, t / cab.name)
    out = subprocess.run(["7z", "l", "-slt", str(t / cab.name)], capture_output=True, text=True,
                         encoding="utf-8", errors="replace").stdout
    return [l[7:] for l in out.splitlines() if l.startswith("Path = ")][1:]


membres = {n: liste_isolee(p) for n, p in cabs.items()}

# --- extraction complete (chaines entieres) dans un dossier par chaine
x = W / "x"
noms = sorted(cabs)
for n in noms:
    stem = n[:-4].rstrip("0123456789")
    num = n[len(stem):-4]
    if num and f"{stem}{int(num) - 1}.CAB" in cabs:
        continue
    run("7z", "x", "-y", "-o" + str(x / n), str(cabs[n]))
chaine_de = {}
for n in noms:
    stem = n[:-4].rstrip("0123456789")
    num = n[len(stem):-4]
    d = n
    while num and f"{stem}{int(num) - 1}.CAB" in cabs:
        num = str(int(num) - 1)
        d = f"{stem}{num}.CAB"
    chaine_de[n] = x / d

# --- attribution de chaque fichier a un CAB : LAYOUT*.INF d'abord
layouts = [p for p in x.rglob("*") if p.name.lower() in ("layout.inf", "layout1.inf", "layout2.inf")]
num_cab, attrib = {}, {}
for lf in layouts:
    t = lf.read_bytes().decode("cp1252")
    for m in re.finditer(r'^(\d+)="[^"]*","([^"]+)",', t, re.M):
        num_cab[m.group(1)] = m.group(2).upper()
    for m in re.finditer(r"^([^;\[=\s][^=\s]*)=(\d+),", t, re.M):
        if m.group(2) in num_cab:
            attrib.setdefault(m.group(1).upper(), num_cab[m.group(2)])
contenu = {n: [] for n in noms}
vus = set()
for n in noms:
    for f in membres[n]:
        u = f.upper()
        if n in INTACTS:
            continue
        cible = attrib.get(u, n)
        if cible not in contenu or u in vus:
            continue
        if u not in [m.upper() for m in membres[cible]]:
            cible = n
        vus.add(u)
        contenu[cible].append(f)

# --- fichiers du SP3.0 a integrer
sp = W / "sp30"
for c in ("SP2.CAB", "SUPP.CAB", "ADDITIONS.CAB"):
    run("7z", "x", "-y", "-o" + str(sp / c), str(SP30 / c))
remplace = {}
for f in sp.rglob("*"):
    if f.is_file():
        remplace.setdefault(f.name.upper(), f)
sp366 = set()
for f in SP366.iterdir():                            # couche 3.66 filtree FR : prioritaire sur SP3.0
    if f.is_file() and f.suffix.upper() not in (".INF", ".TXT"):
        remplace[f.name.upper()] = f
        sp366.add(f.name.upper())
for f in TRAD.iterdir():
    remplace[f.name.upper()] = f                     # OLEDLG / HHCTRL traduits en francais
rapport, faits = [], {}
for n in noms:
    if n in INTACTS:
        continue
    racine = chaine_de[n]
    for f in contenu[n]:
        u = f.upper()
        if u not in remplace:
            continue
        if u.endswith(".INF"):
            # INF du programme d'installation (MSHDC, OLE2, RNA, TIMEZONE, WSH) : ceux du
            # SP3.0 visent un systeme installe, gardes d'origine dans cette premiere version
            continue
        if u in IE6_SEULEMENT or not u.endswith(PILOTES_EXT):
            rapport.append(f"GARDE (pose par le pack apres IE6 SP1) {u}")
            continue
        orig = racine / f
        nouv = remplace[u]
        if orig.read_bytes() == nouv.read_bytes():
            continue
        vo, vn = version(orig), version(nouv)
        if vo and vn and vn < vo:
            rapport.append(f"GARDE (CD plus recent) {u} {vo} > {vn}")
            continue
        shutil.copy2(nouv, orig)
        faits[u] = (len(nouv.read_bytes()), n, vo, vn)
print(len(faits), "fichiers remplaces dans les CAB, dont", len(sp366 & set(faits)), "de la couche 3.66")

# --- patcher9x (JHRobotics) : processeurs recents (TLB), vitesse du processeur,
# registres du processeur (WIN.CNF). SANS le correctif memoire (mem) : integre aux
# CAB, il bloquait l'installation du SP3.0 par le pack (programmes console lances
# par ADVPACK : ecran noir, etape [2/11] sans fin, a 1 Go comme a 2 Go, tests QEMU
# du 2026-10-18). La memoire reste a PATCHMEM en fin de pack, comme sur le CD V3.
# Au-dela de 1 Go : retirer de la memoire le temps de l'installation (comme l'UBCD).
# Fichiers soumis a l'outil (ceux qu'il sait corriger) ; seuls ceux qu'il modifie
# reellement passent dans les CAB. Reponses : 2 = VMM32 corrige directement, Y.
P9X_FICHIERS = ["VMM32.VXD", "NDIS.VXD", "WIN.CNF", "VCACHE.VXD", "IOS.VXD", "NTKERN.VXD",
                "ESDI_506.PDR", "SCSIPORT.PDR"]
P9X_ATTENDUS = {"VMM32.VXD", "NDIS.VXD", "WIN.CNF"}
tp = W / "p9x"
tp.mkdir()
ou = {}
for n in noms:
    for f in contenu[n]:
        if f.upper() in P9X_FICHIERS and f.upper() not in ou:
            ou[f.upper()] = (n, chaine_de[n] / f)
assert set(ou) == set(P9X_FICHIERS), ou
for u, (n, p) in ou.items():
    shutil.copy2(p, tp / u)
subprocess.run([str(P9X), "-no-backup", "-unselect", "mem", str(tp)], input="2\nY\n\n", text=True,
               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
modifies = {u for u, (n, p) in ou.items() if (tp / u).read_bytes() != p.read_bytes()}
assert P9X_ATTENDUS <= modifies, ("patcher9x n'a pas tout corrige", modifies)
ou = {u: v for u, v in ou.items() if u in modifies}
for u, (n, p) in ou.items():
    nouv = (tp / u).read_bytes()
    p.write_bytes(nouv)
    v = version(p)
    faits[u] = (len(nouv), n, v, v)
    rapport.append(f"PATCHER9X {u} ({n})")
print("patcher9x :", ", ".join(ou))

# --- tailles dans LAYOUT*.INF
for lf in layouts:
    t = lf.read_bytes().decode("cp1252")
    for u, (taille, _, _, _) in faits.items():
        t = re.sub(r"(?im)^(%s=\d+,[^,\r\n]*,)\d+" % re.escape(u.lower()),
                   lambda m: m.group(1) + str(taille), t)
    lf.write_bytes(t.encode("cp1252"))

# --- composants du pack dans PRECOPY2.CAB : charges par SETUPPP.INF [load_inf],
# precopies (PRECOPY.INF), cites dans LAYOUT.INF (disque 2 = PRECOPY2.CAB)
NOUVEAUX = ["w98frpk.inf", "w98frgo.bat"]
racine_pc = chaine_de["PRECOPY2.CAB"]


def inserer(nom, apres, lignes, avant=False):
    p = next(p for p in racine_pc.iterdir() if p.name.lower() == nom)
    t = p.read_bytes().decode("cp1252").split("\r\n")
    k = next(i for i, l in enumerate(t) if l.strip().lower().startswith(apres))
    t[k + (0 if avant else 1):k + (0 if avant else 1)] = lignes
    p.write_bytes("\r\n".join(t).encode("cp1252"))


for n in NOUVEAUX:
    shutil.copy2(W / n.upper(), racine_pc / n)
    contenu["PRECOPY2.CAB"].append(n)
inserer("layout.inf", "wpwin98.inf=2,,", [f"{n}=2,,{(racine_pc / n).stat().st_size}" for n in NOUVEAUX])
inserer("precopy.inf", "wpwin98.inf=", ["w98frpk.inf="])
inserer("setuppp.inf", "certify.inf", ["w98frpk.inf"], avant=True)
# Fichiers copies par un INF dont la LayoutFile ne cite pas leur LAYOUT (NETFAM.INF :
# IENPSTUB.DLL, MSLOCUSR.DLL ; WS2ATM...) : "fichier introuvable" pendant l'installation
# du materiel (test QEMU 2026-10-18). Ligne recopiee dans le LAYOUT qu'il cite.
sys.path.insert(0, str(ICI))
from layout_manquants import manquants  # noqa: E402
for lay, lignes in manquants(racine_pc).items():
    if lignes:
        inserer(lay, "[sourcedisksfiles]", sorted(lignes.values()))
        rapport.append(f"{lay} : ajoute {', '.join(sorted(lignes))}")

# --- reconstruction des CAB (LZX:21 comme l'original), EN GARDANT LES CHAINES du CD :
# PRECOPY1-2 (W98SETUP.BIN n'ouvre que precopy1.cab, puis suit la chaine : CAB
# autonomes = "ne parvient pas a trouver Setupx.dll") et CATALOG3 a WIN98_68 (le
# moteur de copie y cherche aussi les fichiers absents du LAYOUT de leur INF, ex.
# IENPSTUB.DLL de NETFAM.INF : CAB autonomes = "fichier introuvable"). Tests QEMU
# 2026-10-18. Chaque fichier reste dans le CAB que LAYOUT*.INF lui attribue
# (.New Cabinet entre deux CAB : aucun fichier coupe), noms d'origine (CabinetName<n>).
def ensemble(cab):
    d = cab.read_bytes()[:36]
    return struct.unpack_from("<HH", d, 32)                    # (setID, iCabinet)


groupes = {}
for n in noms:
    if n not in INTACTS:
        sid, rang = ensemble(cabs[n])
        groupes.setdefault(sid, []).append((rang, n))
nouv_cabs = W / "cabs"
nouv_cabs.mkdir()
for n in INTACTS:
    shutil.copy2(cabs[n], nouv_cabs / cabs[n].name)
for sid, membres_g in groupes.items():
    ordre = [n for _, n in sorted(membres_g)]
    ddf = [".OPTION EXPLICIT", ".Set CabinetNameTemplate=W98_*.CAB",
           f".Set DiskDirectoryTemplate={nouv_cabs}", ".Set Cabinet=on", ".Set Compress=on",
           ".Set CompressionType=LZX", ".Set CompressionMemory=21", ".Set MaxDiskSize=0",
           ".Set CabinetFileCountThreshold=0", ".Set FolderFileCountThreshold=0",
           ".Set FolderSizeThreshold=0", ".Set MaxCabinetSize=0", ".Set UniqueFiles=off",
           ".Set RptFileName=NUL", ".Set InfFileName=NUL"]
    ddf += [f".Set CabinetName{i}={cabs[n].name}" for i, n in enumerate(ordre, 1)]
    for i, n in enumerate(ordre):
        if not contenu[n]:
            # CAB qui ne contenait que la suite d'un fichier commence dans le precedent
            # (ex. DRIVER14 = fin de GM16.DLS) : CAB minimal, LAYOUT le cite toujours
            vide = W / (n[:-4] + ".TXT")
            vide.write_bytes(b"CAB conserve pour LAYOUT.INF (pack Win98FR)\r\n")
            contenu[n] = [vide.name]
            chaine_de[n] = W
        if i:
            ddf.append(".New Cabinet")
        ddf += [f'"{chaine_de[n] / f}" "{f}"' for f in contenu[n]]
    (W / "c.ddf").write_text("\r\n".join(ddf) + "\r\n", encoding="cp1252")
    run("makecab", "/F", str(W / "c.ddf"))
for n in noms:
    shutil.copy2(nouv_cabs / cabs[n].name, cabs[n])
for sid, membres_g in groupes.items():                      # chaine bien refaite ?
    rangs = [ensemble(cabs[n])[1] for _, n in sorted(membres_g)]
    assert rangs == list(range(len(rangs))), (sid, rangs)
print("chaines de CAB :", ", ".join(f"{len(m)} CAB" for m in groupes.values()))

# --- controle : chaque CAB s'ouvre seul et contient ce qu'il doit
erreurs = 0
for n in noms:
    if n in INTACTS:
        continue
    l = liste_isolee(cabs[n])
    if sorted(x.upper() for x in l) != sorted(x.upper() for x in contenu[n]):
        erreurs += 1
        print("CONTENU DIFFERENT", n)
print("controle des CAB :", "OK" if not erreurs else f"{erreurs} erreurs")
tot = sum(len(contenu[n]) for n in noms if n not in INTACTS)
print("fichiers dans les CAB reconstruits :", tot)
(W / "RAPPORT.TXT").write_text("\n".join(
    [f"{u:14} {d[1]:13} {'.'.join(map(str, d[2]))} -> {'.'.join(map(str, d[3]))}" for u, d in sorted(faits.items())]
    + rapport) + "\n", encoding="utf-8")

# --- ISO bootable (El Torito disquette 1.44 Mo), ISO9660 + Joliet
import pycdlib  # noqa: E402

# Noms ISO9660 niveau 1 (8.3, lus par MSCDEX sous DOS) + Joliet (noms longs, Windows)
alias = {}


def nom83(parent, nom, dossier):
    base, _, ext = nom.rpartition(".") if (not dossier and "." in nom) else (nom, "", "")
    nettoie = lambda s: re.sub(r"[^A-Z0-9_]", "_", s.upper())
    b, e = nettoie(base)[:8] or "_", nettoie(ext)[:3]
    pris = alias.setdefault(parent, set())
    cand, k = b, 1
    while (cand + ("." + e if e else "")) in pris:
        suf = "_" + str(k)                      # "~" interdit en ISO9660 strict
        cand, k = b[:8 - len(suf)] + suf, k + 1
    r = cand + ("." + e if e else "")
    pris.add(r)
    return r


iso = pycdlib.PyCdlib()
iso.new(interchange_level=1, joliet=3, vol_ident="W98SE_FR")
iso.add_file(str(boot), "/BOOT.IMG;1", joliet_path="/BOOT.IMG")
iso.add_eltorito("/BOOT.IMG;1", "/BOOT.CAT;1", joliet_bootcatfile="/BOOT.CAT", media_name="floppy")
chemins = {cd: ""}
for p in sorted(cd.rglob("*"), key=lambda q: (len(q.relative_to(cd).parts), str(q).upper())):
    parent = chemins[p.parent]
    n83 = nom83(parent, p.name, p.is_dir())
    chemins[p] = parent + "/" + n83
    jol = "/" + str(p.relative_to(cd)).replace("\\", "/")
    if p.is_dir():
        iso.add_directory(chemins[p], joliet_path=jol)
    else:
        iso.add_file(str(p), chemins[p] + ";1", joliet_path=jol)
iso.write(str(ISO_OUT))
iso.close()
print("ISO :", ISO_OUT, ISO_OUT.stat().st_size // 2**20, "Mo")
