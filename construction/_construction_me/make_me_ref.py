# Kit de la VM de reference Windows ME (image QuickInstall ME) : CD avec les etapes
# a lancer dans l'ordre apres une installation propre de ME (meme ordre que le pack 98) :
#   ETAPE1.BAT : IE6 SP1 FR + WMP9 FR                                  -> redemarrage
#   ETAPE2.BAT : correctifs IE6/WMP9, MDAC 2.8 SP1 FR, Me SP 2.02 Beta 9 FR
#                (RUNPOST.BAT sans ROOTSUPD/CRLUPD 2007, qui figeaient le SP3.0 sous 98)
#                                                                       -> redemarrage
#   ETAPE3.BAT : certificats 2020, KernelEx FR, applications du pack 98, source des CAB
#                (C:\WIN9X), puis mode MS-DOS FR (dosmode_fr)           -> redemarrage
# Les fichiers viennent du pack 98 (Win98FR_v3) et de _construction_me ; rien n'est modifie.
# Usage : make_me_ref.py <dossier win98se> <dossier MESP Beta 9 extrait> <dossier kit de sortie>
import shutil
import sys
from pathlib import Path

W, MESP, OUT = (Path(a) for a in sys.argv[1:4])
P = W / "Win98FR_v3"
if OUT.exists():
    raise SystemExit(f"{OUT} existe deja")


def copie(src, dest):
    d = OUT / dest
    if src.is_dir():
        shutil.copytree(src, d)
    else:
        d.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, d)


def texte(nom, lignes):
    (OUT / nom).write_bytes(("\r\n".join(lignes) + "\r\n").encode("cp1252"))


copie(P / "01_BASE/ie6sp1", "IE6SP1")
copie(P / "01_BASE/wmp9", "WMP9")
for f in ("q828750.exe", "KB819639.EXE"):
    copie(P / "01_BASE/updates" / f, "MAJ")
copie(P / "01_BASE/mdac28", "MDAC28")
copie(MESP, "MESP")
rp = OUT / "MESP/RUNPOST.BAT"
lignes = rp.read_bytes().decode("cp1252").splitlines()
retire = [l for l in lignes if "ROOTSUPD" in l.upper() or "CRLUPD" in l.upper()]
assert len(retire) == 2, retire
rp.write_bytes(("\r\n".join(l for l in lignes if l not in retire) + "\r\n").encode("cp1252"))
copie(P / "03_SYST/rootsupd", "CERTS")
copie(P / "05_EXTRA/kernelex", "KEX")
for a in ("7zip", "retrozil", "qres", "siv", "vc2005", "vc2008"):
    copie(P / "10_APPLI" / a, f"APPS/{a.upper()}")
copie(W / "_construction_me/dosmode_fr", "DOSMODE")

texte("SOURCE.REG", [
    "REGEDIT4", "",
    "; VM de reference QuickInstall ME : les CAB de Windows ME sont dans C:\\WIN9X",
    "[HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Setup]",
    '"SourcePath"="C:\\\\WIN9X\\\\"', "",
    "[HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion]",
    '"SourcePath"="C:\\\\WIN9X\\\\"', ""])

ENTETE = ["@echo off", "REM Kit VM de reference QuickInstall ME (genere par make_me_ref.py)",
          # pas de > dans un REM : COMMAND.COM l'execute comme une redirection
          "REM Lancer depuis le CD (lettre D:) : menu Executer, D:\\ETAPEn.BAT", "D:"]
FIN = ["echo.", "echo   Redemarrage...",
       "start RUNDLL32.EXE SHELL32.DLL,SHExitWindowsEx 6"]
texte("ETAPE1.BAT", ENTETE + [
    "echo [1/3] Internet Explorer 6 SP1 FR + Windows Media Player 9 FR",
    "cd \\IE6SP1",
    'start /w IE6SETUP.EXE /Q:A /R:N /C:"ie6wzd /S:""#e"" /Q:A /R:N"',
    "cd \\WMP9",
    "start /w MPSETUP.EXE /Q:U /R:N",
    "echo Etape 1 terminee>> C:\\MEREF.TXT"] + FIN)
texte("ETAPE2.BAT", ENTETE + [
    "echo [2/3] Correctifs IE6 / WMP9, MDAC 2.8 SP1, Me SP 2.02 Beta 9 FR",
    "cd \\MAJ",
    "start /w Q828750.EXE /q:u /r:n",
    "start /w KB819639.EXE /q:a /r:n",
    "cd \\MDAC28",
    'start /w MDAC_TYP.EXE /Q /C:"DASETUP /Q /N"',
    "cd \\MESP",
    "start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\\SPUPDATE.INF,DefaultInstall",
    "echo Etape 2 terminee>> C:\\MEREF.TXT"] + FIN)
texte("ETAPE3.BAT", ENTETE + [
    "echo [3/3] Certificats 2020, KernelEx, applications, mode MS-DOS FR",
    "cd \\CERTS",
    "start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\\ROOTSUPD.INF,DefaultInstall",
    "start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\\RVKROOTS.INF,DefaultInstall",
    "cd \\KEX",
    "start /w KernelEx-4.5.2019.24-FR.exe /S",
    "start /w REGEDIT /s KEXOFF.REG",
    "cd \\APPS\\VC2005",
    "if not exist C:\\MEREF\\NUL md C:\\MEREF",
    "start /w VCREDIST.EXE /Q /T:C:\\MEREF /C",
    'if exist C:\\MEREF\\VCREDI~3.EXE start /w C:\\MEREF\\VCREDI~3.EXE /q:a /c:"msiexec /i vcredist.msi /qb"',
    "deltree /y C:\\MEREF > NUL",
    "cd \\APPS\\VC2008",
    "start /w VC_R_9X.EXE /q:a /r:n",
    "cd \\APPS\\QRES",
    "start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\\QRES.INF,DefaultInstall",
    "cd \\APPS\\7ZIP",
    "start /w 7Z920.EXE /S",
    "cd \\APPS\\RETROZIL",
    "start /w RZ23.EXE -ms",
    "start /w REGEDIT /s RETROZIL.REG",
    "cd \\APPS\\SIV",
    "start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\\SIV.INF,DefaultInstall",
    "cd \\",
    "start /w REGEDIT /s SOURCE.REG",
    "echo Etape 3 terminee (mode MS-DOS FR ensuite)>> C:\\MEREF.TXT",
    "REM dosmode_fr : son INSTALL.BAT corrige COMMAND.COM et REGENV32 dans son propre",
    "REM dossier (donc pas depuis le CD), et finit par DOSMODE.INF, qui redemarre",
    "if not exist C:\\MEDOS\\NUL md C:\\MEDOS",
    "xcopy D:\\DOSMODE\\*.* C:\\MEDOS > NUL",
    "C:",
    "cd \\MEDOS",
    "call INSTALL.BAT"])
texte("LISEZMOI.TXT", [
    "Kit de la VM de reference QuickInstall Windows ME FR",
    "",
    "Apres une installation propre de ME (CAB copies dans C:\\WIN9X avant Setup) :",
    "Executer > D:\\ETAPE1.BAT, puis apres le redemarrage D:\\ETAPE2.BAT, puis D:\\ETAPE3.BAT.",
    "Chaque etape redemarre Windows. Journal : C:\\MEREF.TXT.",
    "Ensuite : arret propre, puis capture avec sysprep.py (QuickInstall)."])
n = sum(1 for _ in OUT.rglob("*") if _.is_file())
print("ok", n, "fichiers,", sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file()) // 2**20, "Mo")
