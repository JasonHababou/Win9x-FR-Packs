# ISO Windows Me FR "classique" : CD Windows Millennium OEM FR (non amorcable) +
# disquette de demarrage FR (El Torito) + fichier de reponses + pack WinMeFR.
#  - disquette : EBD francais de Windows Me (bkpWin98\SauvegardeWinME\...\EBD, lu
#    seulement), menu avec "Installer Windows Millennium Edition depuis le CD-ROM"
#    (choix par defaut) qui lance WMEFRDOS.BAT -> WIN9X\INSTALL.EXE + MSBATCH.INF.
#    Secteur de demarrage repris de la disquette ME de reference (me_ref_floppy.img) ;
#  - CD : WIN9X du CD OEM (+ MSBATCH.INF), pack WinMeFR a la racine (CABS.VBS y trouve
#    WIN9X), WMEFRCD.BAT (pack au premier demarrage, valeur Run du MSBATCH).
# Usage : make_me_iso.py <ISO OEM> <disquette ME de reference> <EBD FR> <pack WinMeFR>
#                        <MSBATCH.INF> <iso de sortie>
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pycdlib

iso_oem, flop_ref, ebd, pack, msbatch, sortie = (Path(a) for a in sys.argv[1:7])
ICI = Path(__file__).parent
SEVEN = r"C:\Program Files\7-Zip\7z.exe"
FAT = Path(r"<scratchpad>"
           r"\5bf4683e-c344-4973-a434-228aefd021d3\scratchpad\venv_qi\Scripts\python.exe")
tmp = Path(tempfile.mkdtemp())

# --- 1. disquette de demarrage FR
cfg = (ebd / "CONFIG.SYS").read_bytes().decode("cp850").replace("\r\n", "\n")
assert "menuitem=HELP, Aide" in cfg and "menudefault=HELP,30" in cfg
cfg = cfg.replace("[menu]\n", "[menu]\nmenuitem=SETUP, Installer Windows Millennium Edition depuis le CD-ROM\n", 1)
cfg = cfg.replace("menudefault=HELP,30", "menudefault=SETUP,30")
cfg = cfg.replace("[CD]\n", "[SETUP]\ninclude=CD\n\n[CD]\n", 1)
aut = (ebd / "AUTOEXEC.BAT").read_bytes().decode("cp850").replace("\r\n", "\n")
ancien = "IF ERRORLEVEL 1 SET CDPROB=1\n::\nGOTO QUIT\n\n:HELP"
assert aut.count(ancien) == 1
aut = aut.replace(ancien, "IF ERRORLEVEL 1 SET CDPROB=1\n::\n"
                  "IF \"%config%\"==\"SETUP\" IF \"%CDPROB%\"==\"\" %CDROM%:\\WMEFRDOS.BAT %CDROM%\n"
                  "GOTO QUIT\n\n:HELP")
(tmp / "ebd").mkdir()
for p in ebd.iterdir():
    shutil.copy2(p, tmp / "ebd" / p.name)
(tmp / "ebd" / "CONFIG.SYS").write_bytes(cfg.replace("\n", "\r\n").encode("cp850"))
(tmp / "ebd" / "AUTOEXEC.BAT").write_bytes(aut.replace("\n", "\r\n").encode("cp850"))
disq = tmp / "BOOT.IMG"
script = tmp / "disquette.py"
script.write_text(
    "import shutil, sys\nfrom pathlib import Path\nfrom FATtools import Volume\n"
    "ref, dst, src = sys.argv[1:4]\nshutil.copy2(ref, dst)\nfs = Volume.vopen(dst, 'r+b')\n"
    "# MSDOS.SYS et EBD.SYS (marqueur de disquette de demarrage) : ceux de la reference\n"
    "garde = {n: fs.open(n).read() for n in ('MSDOS.SYS', 'EBD.SYS')}\n"
    "for n in fs.listdir():\n"
    "    fs.erase(n)\n"
    "# IO.SYS en premier : contigu au debut de la zone de donnees (secteur de demarrage)\n"
    "noms = ['IO.SYS'] + sorted(p.name for p in Path(src).iterdir() if p.name != 'IO.SYS')\n"
    "for n in noms:\n"
    "    f = fs.create(n); f.write((Path(src) / n).read_bytes()); f.close()\n"
    "for n, data in garde.items():\n"
    "    f = fs.create(n); f.write(data); f.close()\n"
    "Volume.vclose(fs)\nprint('disquette :', len(noms) + 2, 'fichiers')\n", encoding="utf-8")
subprocess.run([str(FAT), str(script), str(flop_ref), str(disq), str(tmp / "ebd")], check=True,
               env={**__import__("os").environ, "FATTOOLS_VFSENC": "cp850"})

# --- 2. CD
subprocess.run([SEVEN, "x", "-y", f"-o{tmp / 'oem'}", str(iso_oem)], check=True, stdout=subprocess.DEVNULL)
cd = tmp / "oem"
shutil.copy2(msbatch, cd / "WIN9X" / "MSBATCH.INF")
# CHOICE.COM (menus de WMEFRDOS.BAT) : absent de la disquette, pris dans BASE2.CAB du CD
subprocess.run([SEVEN, "e", "-y", f"-o{cd}", str(cd / "WIN9X" / "BASE2.CAB"), "choice.com"],
               check=True, stdout=subprocess.DEVNULL)
(cd / "choice.com").rename(cd / "CHOICE.COM")
for f in ("WMEFRDOS.BAT", "WMEFRC.BAT", "WMEFRCD.BAT"):
    t = (ICI / "iso" / f).read_text(encoding="utf-8").replace("\r\n", "\n")
    (cd / f).write_bytes(t.replace("\n", "\r\n").encode("cp1252"))
# lanceur du CD correctif retire (le pack part par la cle Run) ; LISEZMOI du pack renomme, comme
# pour l'ISO 98
for p in pack.iterdir():
    if p.name.upper() in ("AUTORUN.INF", "AUTORUN.EXE"):
        continue
    if p.name.upper() == "LISEZMOI.TXT":
        shutil.copy2(p, cd / "LISEZMOI_PACK.TXT")
        continue
    if (cd / p.name).exists():
        raise SystemExit(f"conflit de nom a la racine du CD : {p.name}")
    (shutil.copytree if p.is_dir() else shutil.copy2)(p, cd / p.name)

iso = pycdlib.PyCdlib()
iso.new(interchange_level=3, joliet=3, vol_ident="WINMEFR")
noms = {}


def nom9660(parent, nom, fichier):
    propre = lambda x: "".join(c if (c.isascii() and c.isalnum()) or c == "_" else "_" for c in x.upper())
    if fichier and "." in nom:
        b, e = nom.rsplit(".", 1)
        s = (propre(b)[:26] or "X") + "." + propre(e)[:3]
    else:
        s = propre(nom)[:30] or "X"
    pris = noms.setdefault(parent, set())
    base, k = s, 1
    while s in pris:
        s, k = f"{base[:24]}_{k}", k + 1
    pris.add(s)
    return s


def ajoute(src, dest_iso, dest_jol):
    for p in sorted(src.iterdir()):
        if p.name == "[BOOT]":
            continue
        n = nom9660(dest_iso, p.name, not p.is_dir())
        if p.is_dir():
            iso.add_directory(f"{dest_iso}/{n}", joliet_path=f"{dest_jol}/{p.name}")
            ajoute(p, f"{dest_iso}/{n}", f"{dest_jol}/{p.name}")
        else:
            iso.add_file(str(p), f"{dest_iso}/{n};1", joliet_path=f"{dest_jol}/{p.name}")


ajoute(cd, "", "")
iso.add_file(str(disq), "/BOOT.IMG;1", joliet_path="/BOOT.IMG")
iso.add_eltorito("/BOOT.IMG;1", "/BOOT.CAT;1", joliet_bootcatfile="/BOOT.CAT", media_name="floppy")
iso.write(str(sortie))
iso.close()
shutil.rmtree(tmp, onerror=lambda f, c, e: (__import__('os').chmod(c, 0o666), f(c)))
print("ok", sortie.stat().st_size // 2**20, "Mo")
