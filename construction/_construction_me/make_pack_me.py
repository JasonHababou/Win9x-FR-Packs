# Pack Windows Me FR (WinMeFR) : assemble le dossier du pack a partir
#  - des fichiers propres a ME de _construction_me\pack (INSTALL.BAT, CABS.VBS,
#    USB2.VBS, NOPOSTNG.INF, FINRUN.INF, PNTFS.INF) : convertis en cp1252 + CRLF ;
#  - des composants du pack 98 (Win98FR_v3) qui conviennent a ME ;
#  - du Me SP 2.02 Beta 9 FR (sources\MESP1FR_2.02b9_2007.EXE, extrait par 7-Zip) :
#    RUNPOST.BAT sans ROOTSUPD/CRLUPD de 2007 (le meme genre d'etape figeait le SP3.0
#    sous 98) ; fichiers Windows Media retires des copies : avec WMP9 installe avant,
#    le SP demandait de garder dxmasf.dll et npwmsdrm.dll (tests QEMU 2026-10-21/26) ;
#  - du lecteur NTFS UFSD corrige (framework QuickInstall\ntfs) et du module
#    USB 2.0 Microsoft (framework QuickInstall\_DRIVER_\[MBD]_sweetlow_usb2.0) ;
#  - du mode MS-DOS FR (dosmode_fr) sans question ni redemarrage propres : INSTALL.BAT
#    du pack enchaine, puis redemarre lui-meme a la fin.
# Usage : make_pack_me.py <dossier win98se> <dossier du pack a creer>
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

W, OUT = Path(sys.argv[1]), Path(sys.argv[2])
P98 = W / "Win98FR_v3"
ME = W / "_construction_me"
QI = W / "_construction_qi" / "framework"
SEVEN = r"C:\Program Files\7-Zip\7z.exe"
TEXTE = {".BAT", ".INF", ".VBS", ".TXT", ".REG", ".INI"}
if OUT.exists():
    raise SystemExit(f"{OUT} existe deja")


def copie(src, dest):
    d = OUT / dest
    if src.is_dir():
        shutil.copytree(src, d)
    else:
        d.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, d / src.name)


def texte_crlf(src, dest):
    t = src.read_text(encoding="utf-8").replace("\r\n", "\n")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(t.replace("\n", "\r\n").encode("cp1252"))


def lire(p):
    return p.read_bytes().decode("cp1252")


def ecrire(p, t):
    p.write_bytes(t.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp1252"))


# 1. composants repris du pack 98
for rel in ("01_BASE/ie6sp1", "01_BASE/wmp9", "01_BASE/mdac28", "03_SYST/rootsupd", "03_SYST/rloew",
            "03_SYST/patcher9x", "05_EXTRA/kernelex", "05_EXTRA/wsh57", "05_EXTRA/taskbarshuffle",
            "05_EXTRA/mspaintfilter", "05_EXTRA/aspi", "08_NET/net11", "09_CHIP"):
    copie(P98 / rel, rel)
for f in ("q828750.exe", "KB819639.EXE"):
    copie(P98 / "01_BASE/updates" / f, "01_BASE/updates")
# GMT.INF : appele par TIMEZONE.INF (RunPostSetupCommands) ; sans lui RUNDLL32 restait
# bloque sans fenetre (test QEMU 2026-10-26)
for f in ("TIMEZONE.INF", "GMT.INF", "TTFEXT.INF", "TTFEXT.DLL", "TTFEXT.HLP"):
    copie(P98 / "06_OPTS" / f, "06_OPTS")
for a in ("vc2005", "vc2008", "qres", "7zip", "daemon", "retrozil", "tarot", "fraps", "siv"):
    copie(P98 / "10_APPLI" / a, f"10_APPLI/{a}")
for f in ("DELPART.EXE", "PNTFS.ICO", "NTFSCFG.VBS"):
    copie(P98 / "05_EXTRA/ntfs" / f, "05_EXTRA/ntfs")

# 2. fichiers propres a ME (texte -> cp1252 + CRLF)
for src in (ME / "pack").rglob("*"):
    if src.is_file():
        rel = src.relative_to(ME / "pack")
        if src.suffix.upper() in TEXTE:
            texte_crlf(src, OUT / rel)
        else:
            (OUT / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, OUT / rel)

# 3. NTFS UFSD corrige + USB 2.0 Microsoft (fichiers du framework QuickInstall)
for f in ("UFSD.VXD", "PNTFSHLP.VXD"):
    copie(QI / "ntfs" / f, "05_EXTRA/ntfs")
# README.*.TXT (deux points) introuvables sur le CD sous ME : noms 8.3
for f, n in (("README.UFSD.TXT", "UFSD.TXT"), ("README.PNTFSHLP.TXT", "PNTFSHLP.TXT")):
    shutil.copy2(QI / "ntfs" / f, OUT / "05_EXTRA/ntfs" / n)
for f in (QI / "_DRIVER_" / "[MBD]_sweetlow_usb2.0").iterdir():
    copie(f, "05_EXTRA/usb2")

# 4. Me SP 2.02 Beta 9 FR
mesp = OUT / "02_MESP"
tmp = Path(tempfile.mkdtemp())
subprocess.run([SEVEN, "x", "-y", f"-o{tmp}", str(ME / "sources/MESP1FR_2.02b9_2007.EXE")],
               check=True, stdout=subprocess.DEVNULL)
shutil.copytree(tmp, mesp)
shutil.rmtree(tmp)
rp = mesp / "RUNPOST.BAT"
lignes = lire(rp).splitlines()
retire = [l for l in lignes if "ROOTSUPD" in l.upper() or "CRLUPD" in l.upper()]
assert len(retire) == 2, retire
ecrire(rp, "\n".join(l for l in lignes if l not in retire) + "\n")
inf = mesp / "SPUPDATE.INF"
t = lire(inf)
# Fichiers Windows Media retires des listes de copie : le drapeau 1056 n'evitait pas la
# question "Conflit de versions" (langue differente, test QEMU 2026-10-26) ; WMP9 est
# toujours installe a l'etape 1, ses versions sont plus recentes
WMF = ("dxmasf.dll", "asfsipc.dll", "drmstor.dll", "strmdll.dll", "npdsplay.dll", "mplayer2.exe", "npwmsdrm.dll")
n = 0
for nom in WMF:
    t, k = re.subn(rf"(?im)^({re.escape(nom)},,,(32|1024)\b)", r"; WMP9 : \1", t)
    n += k
assert n == len(WMF), n
ecrire(inf, t)

# 5. mode MS-DOS FR : sans question (BeginPrompt), sans redemarrage propre, ADVPACK systeme
dos = OUT / "11_DOS"
shutil.copytree(ME / "dosmode_fr", dos)
(dos / "ADVPACK.DLL").unlink()          # ADVPACK anglais de TPC : questions en anglais
d = lire(dos / "DOSMODE.INF")
assert "BeginPrompt=Install.BeginPrompt" in d
d = d.replace("[DefaultInstall]\r\n", "[DefaultInstall]\r\nSmartReboot=N\r\n", 1) if "\r\n" in d else \
    d.replace("[DefaultInstall]\n", "[DefaultInstall]\nSmartReboot=N\n", 1)
d = d.replace("BeginPrompt=Install.BeginPrompt", "; BeginPrompt retire : question deja posee par le pack", 1)
ecrire(dos / "DOSMODE.INF", d)
b = lire(dos / "INSTALL.BAT").replace("\r\n", "\n")
ancien = "RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection DOSMODE.INF,DefaultInstall\nEXIT\n"
assert ancien in b, "fin de INSTALL.BAT de dosmode_fr inattendue"
b = b.replace(ancien, "REM  Pack WinMeFR : attendre la fin de l'INF ; le pack redemarre ensuite\n"
                      "start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\\DOSMODE.INF,DefaultInstall\n")
ecrire(dos / "INSTALL.BAT", b)

nf = sum(1 for p in OUT.rglob("*") if p.is_file())
print("ok", nf, "fichiers,", sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file()) // 2**20, "Mo")
